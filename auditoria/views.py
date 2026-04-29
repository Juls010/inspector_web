from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache 
import requests 

def home(request):
    resultado = None
    url_a_analizar = request.GET.get('url')

    if url_a_analizar:
        cache_key = f"full_audit_{url_a_analizar}"
        resultado = cache.get(cache_key)

        if not resultado:
            google_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={settings.SAFE_BROWSING_KEY}"
            google_payload = {
                "client": {"clientId": "inspector-web", "clientVersion": "1.0.0"},
                "threatInfo": {
                    "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
                    "platformTypes": ["ANY_PLATFORM"],
                    "threatEntryTypes": ["URL"],
                    "threatEntries": [{"url": url_a_analizar}]
                }
            }
            res_google = requests.post(google_url, json=google_payload)
            es_peligrosa = "matches" in res_google.json()

            dominio = url_a_analizar.replace("https://", "").replace("http://", "").split("/")[0]
            res_ip = requests.get(f"http://ip-api.com/json/{dominio}")
            data_ip = res_ip.json()

            headers_urlscan = {"Content-Type": "application/json"}
            if settings.URLSCAN_KEY and settings.URLSCAN_KEY != 'llave_no_encontrada':
                headers_urlscan["API-Key"] = settings.URLSCAN_KEY
                
            urlscan_api = f"https://urlscan.io/api/v1/search/?q=domain:{dominio}"
            res_scan = requests.get(urlscan_api, headers=headers_urlscan)
            data_scan = res_scan.json()

            screenshot = None
            if data_scan.get('results') and len(data_scan['results']) > 0:
                screenshot = data_scan['results'][0].get('screenshot')
                if not screenshot:
                    task_id = data_scan['results'][0].get('task', {}).get('uuid')
                    if task_id:
                        screenshot = f"https://urlscan.io/screenshots/{task_id}.png"

            resultado = {
                'url': url_a_analizar,
                'seguridad': "PELIGROSA" if es_peligrosa else "SEGURA",
                'pais': data_ip.get('country', 'Desconocido'),
                'ip': data_ip.get('query', 'N/A'),
                'captura': screenshot,
                'fuente': 'Datos en Tiempo Real'
            }

            cache.set(cache_key, resultado, timeout=600)
        else:
            resultado['fuente'] = 'Caché (Requisito RA9 cumplido)'

    return render(request, 'index.html', {'resultado': resultado})