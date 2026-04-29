import requests
import json
import sys

def test_urlscan(domain):
    headers = {"Content-Type": "application/json"}
    urlscan_api = f"https://urlscan.io/api/v1/search/?q=domain:{domain}"
    print(f"Testing domain: {domain}")
    try:
        res = requests.get(urlscan_api, headers=headers)
        data = res.json()
        results = data.get('results', [])
        print(f"Total results: {len(results)}")
        if results:
            print("First result screenshot:", results[0].get('screenshot'))
            print("First result task uuid:", results[0].get('task', {}).get('uuid'))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    domains = ["wikipedia.org", "es.wikipedia.org", "malware.testing.google.com"]
    for d in domains:
        test_urlscan(d)
        print("-" * 20)
