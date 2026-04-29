# Inspector Web - Auditor de Seguridad

Este proyecto es una herramienta de auditoría de seguridad web construida con Django. Permite a los usuarios introducir una URL y obtener un análisis detallado en tiempo real utilizando el patrón "Mashup", integrando tres APIs diferentes para ofrecer un informe completo de seguridad, geolocalización y reconocimiento visual.

## APIs Integradas (Mashup)

Para generar el informe de cada dominio, la aplicación hace llamadas desde el backend (`views.py`) a las siguientes tres APIs externas:

### 1. Google Safe Browsing API
**Función:** Detección de amenazas, phishing y malware.
* **Uso en el proyecto:** Se utiliza para verificar si la URL introducida se encuentra en las bases de datos actualizadas de Google sobre sitios engañosos o peligrosos.
* **Implementación técnica:** Se realiza una petición `POST` enviando un objeto JSON con la URL objetivo. Si la respuesta de Google incluye el campo `matches`, el sistema clasifica inmediatamente el sitio web como **PELIGROSA**. Si no se encuentran amenazas, se clasifica como **SEGURA**.
* **Autenticación:** Requiere una clave API (Google Cloud API Key) proporcionada a través de la variable de entorno `SAFE_BROWSING_KEY`.

### 2. IP-API (Geolocalización)
**Función:** Identificación de la ubicación física del servidor y su dirección IP.
* **Uso en el proyecto:** Permite al usuario saber desde qué país está operando el servidor web, un dato crucial en auditorías de seguridad y *Threat Intelligence*.
* **Implementación técnica:** Se realiza una petición `GET` a la ruta `http://ip-api.com/json/{dominio}`. La API resuelve el dominio y devuelve un JSON del que se extraen los campos `country` (País) y `query` (Dirección IP).
* **Autenticación:** Endpoint público gratuito (no requiere API Key).

### 3. URLScan.io API
**Función:** Obtención de telemetría y captura de pantalla visual del sitio web.
* **Uso en el proyecto:** Proporciona una prueba visual (screenshot) de la página web sin que el usuario tenga que arriesgarse a visitarla manualmente en su navegador, evitando así la exposición a código malicioso en el frontend.
* **Implementación técnica:** Se realiza una petición `GET` a la ruta de búsqueda `https://urlscan.io/api/v1/search/?q=domain:{dominio}`. La aplicación busca en los resultados recientes y construye dinámicamente la URL de la imagen de la captura de pantalla usando el `uuid` del último escaneo.
* **Autenticación:** Se utiliza la variable de entorno `URLSCAN_KEY` que se inyecta en las cabeceras HTTP (`API-Key`) de la petición.

---

## Flujo de Trabajo (Caché)

Para mejorar el rendimiento y evitar agotar las cuotas gratuitas de estas APIs, el proyecto implementa un sistema de almacenamiento en caché en memoria (`LocMemCache`):
1. Cuando un usuario introduce una URL, primero se verifica si ya existe en la caché.
2. Si existe (y no ha caducado), se devuelve inmediatamente el resultado guardado con la etiqueta **"Caché"**.
3. Si no existe, se contacta a las 3 APIs (Google, IP-API, URLScan), se procesan los datos, se guardan en la caché por 10 minutos y se muestran con la etiqueta **"Datos en Tiempo Real"**.

---
Proyecto de Servidor con Django con consumo de APIs externas.

Julia N.G 💕
