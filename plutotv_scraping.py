import json
import requests
import time
import re

# --------- CÓDIGO 1: Manejo de LiveTV ---------
# Definir las URLs de las APIs
url1 = "https://service-media-catalog.clusters.pluto.tv/v1/main-categories?includeImages=svg"
url2 = "https://service-channels.clusters.pluto.tv/v2/guide/channels?channelIds=&offset=0&limit=1000&sort=number%3Aasc"

# Definir los headers para la primera API de LiveTV (categorías)
headers1 = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "es-419,es;q=0.9",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6IjRlMDUzMjYyLWQ5YWYtNDFlZS1iOWUyLTBiNDU0MDliOTkxOSIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSUQiOiI5YWFhMmIxZC03MWNjLTExZWYtOWRlYS01NjA0ODI5NDZlYTUiLCJjbGllbnRJUCI6IjE2My4xMC4zNi40IiwiY2l0eSI6IkxhIFBsYXRhIiwicG9zdGFsQ29kZSI6ImIxOTA2IGZkYSIsImNvdW50cnkiOiJBUiIsImRtYSI6MCwiYWN0aXZlUmVnaW9uIjoiVkUiLCJkZXZpY2VMYXQiOi0zNC45MzAwMDAzMDUxNzU3OCwiZGV2aWNlTG9uIjotNTcuOTU5OTk5MDg0NDcyNjU2LCJwcmVmZXJyZWRMYW5ndWFnZSI6ImVzIiwiZGV2aWNlVHlwZSI6IndlYiIsImRldmljZVZlcnNpb24iOiIxMjguMC4wIiwiZGV2aWNlTWFrZSI6ImNocm9tZSIsImRldmljZU1vZGVsIjoid2ViIiwiYXBwTmFtZSI6IndlYiIsImFwcFZlcnNpb24iOiI5LjQuMC05Y2E1MWNhMTBjMzA0N2ZiYWZhNzI5NzcwOGYxNDYyNDMxNDZkMTI1IiwiY2xpZW50SUQiOiI5MDEwZWQ0Mi00N2FkLTQ5MGItYmI3MC1iYjczNDk1MTQxODciLCJjbUF1ZGllbmNlSUQiOiIiLCJpc0NsaWVudEROVCI6ZmFsc2UsInVzZXJJRCI6IjY2ZGI1OGQ1ZjVkMGY4ODY3YzFkZTBkZCIsInVzZXJCcmFuZCI6InBsdXRvdHYiLCJsb2dMZXZlbCI6IkRFRkFVTFQiLCJ0aW1lWm9uZSI6IkFtZXJpY2EvQXJnZW50aW5hL0J1ZW5vc19BaXJlcyIsInNlcnZlclNpZGVBZHMiOmZhbHNlLCJlMmVCZWFjb25zIjpmYWxzZSwiZmVhdHVyZXMiOnsibXVsdGlQb2RBZHMiOnsiZW5hYmxlZCI6dHJ1ZX19LCJlbnRpdGxlbWVudHMiOlsiUmVnaXN0ZXJlZCJdLCJmbXNQYXJhbXMiOnsiZndWY0lEMiI6ImYyZTk0OWNlM2Q1OWIwZTE0YWFjODUxMTQyODYzODQ5NDk3ZjAzNGI4YjJjZjg3OGYwMGEyNGM3Zjg1ODI4YzMiLCJmd1ZjSUQyQ29wcGEiOiI5MDEwZWQ0Mi00N2FkLTQ5MGItYmI3MC1iYjczNDk1MTQxODciLCJjdXN0b21QYXJhbXMiOnsiZm1zX2xpdmVyYW1wX2lkbCI6IiIsImZtc19lbWFpbGhhc2giOiJmMmU5NDljZTNkNTliMGUxNGFhYzg1MTE0Mjg2Mzg0OTQ5N2YwMzRiOGIyY2Y4NzhmMDBhMjRjN2Y4NTgyOGMzIiwiZm1zX3N1YnNjcmliZXJpZCI6IjY2ZGI1OGQ1ZjVkMGY4ODY3YzFkZTBkZCIsImZtc19pZmEiOiIiLCJmbXNfaWRmdiI6IiIsImZtc191c2VyaWQiOiI5MDEwZWQ0Mi00N2FkLTQ5MGItYmI3MC1iYjczNDk1MTQxODciLCJmbXNfdmNpZDJ0eXBlIjoiZW1haWxoYXNoIiwiZm1zX3JhbXBfaWQiOiIiLCJmbXNfaGhfcmFtcF9pZCI6IiIsImZtc19iaWRpZHR5cGUiOiIiLCJfZndfM1BfVUlEIjoiIiwiZm1zX3J1bGVpZCI6IjEwMDAwLDEwMDAzIn19LCJkcm0iOnsibmFtZSI6IndpZGV2aW5lIiwibGV2ZWwiOiJMMyJ9LCJpc3MiOiJib290LnBsdXRvLnR2Iiwic3ViIjoicHJpOnYxOnBsdXRvOnVzZXJzLXYxOlZFOk9UQXhNR1ZrTkRJdE5EZGhaQzAwT1RCaUxXSmlOekF0WW1JM016UTVOVEUwTVRnMzo2NmRiNThkNWY1ZDBmODg2N2MxZGUwZGQiLCJhdWQiOiIqLnBsdXRvLnR2IiwiZXhwIjoxNzI2MzE3MzA2LCJpYXQiOjE3MjYyMzA5MDYsImp0aSI6IjVmMWExZmRlLTIyZmMtNDM1NC04NGY1LTdjYjhjNTNiZTA0YiJ9.IM8AcfF0hNcPdLOZBhCHEOziOF-k1s5xL5nfPhCMpXM",
    "origin": "https://pluto.tv",
    "referer": "https://pluto.tv/",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

# Definir los headers para la segunda API de LiveTV (canales)
headers2 = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "es-419,es;q=0.9",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6IjRlMDUzMjYyLWQ5YWYtNDFlZS1iOWUyLTBiNDU0MDliOTkxOSIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSUQiOiI5YWFhMmIxZC03MWNjLTExZWYtOWRlYS01NjA0ODI5NDZlYTUiLCJjbGllbnRJUCI6IjE2My4xMC4zNi40IiwiY2l0eSI6IkxhIFBsYXRhIiwicG9zdGFsQ29kZSI6ImIxOTA2IGZkYSIsImNvdW50cnkiOiJBUiIsImRtYSI6MCwiYWN0aXZlUmVnaW9uIjoiVkUiLCJkZXZpY2VMYXQiOi0zNC45MzAwMDAzMDUxNzU3OCwiZGV2aWNlTG9uIjotNTcuOTU5OTk5MDg0NDcyNjU2LCJwcmVmZXJyZWRMYW5ndWFnZSI6ImVzIiwiZGV2aWNlVHlwZSI6IndlYiIsImRldmljZVZlcnNpb24iOiIxMjguMC4wIiwiZGV2aWNlTWFrZSI6ImNocm9tZSIsImRldmljZU1vZGVsIjoid2ViIiwiYXBwTmFtZSI6IndlYiIsImFwcFZlcnNpb24iOiI5LjQuMC05Y2E1MWNhMTBjMzA0N2ZiYWZhNzI5NzcwOGYxNDYyNDMxNDZkMTI1IiwiY2xpZW50SUQiOiI5MDEwZWQ0Mi00N2FkLTQ5MGItYmI3MC1iYjczNDk1MTQxODciLCJjbUF1ZGllbmNlSUQiOiIiLCJpc0NsaWVudEROVCI6ZmFsc2UsInVzZXJJRCI6IjY2ZGI1OGQ1ZjVkMGY4ODY3YzFkZTBkZCIsInVzZXJCcmFuZCI6InBsdXRvdHYiLCJsb2dMZXZlbCI6IkRFRkFVTFQiLCJ0aW1lWm9uZSI6IkFtZXJpY2EvQXJnZW50aW5hL0J1ZW5vc19BaXJlcyIsInNlcnZlclNpZGVBZHMiOmZhbHNlLCJlMmVCZWFjb25zIjpmYWxzZSwiZmVhdHVyZXMiOnsibXVsdGlQb2RBZHMiOnsiZW5hYmxlZCI6dHJ1ZX19LCJlbnRpdGxlbWVudHMiOlsiUmVnaXN0ZXJlZCJdLCJmbXNQYXJhbXMiOnsiZndWY0lEMiI6ImYyZTk0OWNlM2Q1OWIwZTE0YWFjODUxMTQyODYzODQ5NDk3ZjAzNGI4YjJjZjg3OGYwMGEyNGM3Zjg1ODI4YzMiLCJmd1ZjSUQyQ29wcGEiOiI5MDEwZWQ0Mi00N2FkLTQ5MGItYmI3MC1iYjczNDk1MTQxODciLCJjdXN0b21QYXJhbXMiOnsiZm1zX2xpdmVyYW1wX2lkbCI6IiIsImZtc19lbWFpbGhhc2giOiJmMmU5NDljZTNkNTliMGUxNGFhYzg1MTE0Mjg2Mzg0OTQ5N2YwMzRiOGIyY2Y4NzhmMDBhMjRjN2Y4NTgyOGMzIiwiZm1zX3N1YnNjcmliZXJpZCI6IjY2ZGI1OGQ1ZjVkMGY4ODY3YzFkZTBkZCIsImZtc19pZmEiOiIiLCJmbXNfaWRmdiI6IiIsImZtc191c2VyaWQiOiI5MDEwZWQ0Mi00N2FkLTQ5MGItYmI3MC1iYjczNDk1MTQxODciLCJmbXNfdmNpZDJ0eXBlIjoiZW1haWxoYXNoIiwiZm1zX3JhbXBfaWQiOiIiLCJmbXNfaGhfcmFtcF9pZCI6IiIsImZtc19iaWRpZHR5cGUiOiIiLCJfZndfM1BfVUlEIjoiIiwiZm1zX3J1bGVpZCI6IjEwMDAwLDEwMDAzIn19LCJkcm0iOnsibmFtZSI6IndpZGV2aW5lIiwibGV2ZWwiOiJMMyJ9LCJpc3MiOiJib290LnBsdXRvLnR2Iiwic3ViIjoicHJpOnYxOnBsdXRvOnVzZXJzLXYxOlZFOk9UQXhNR1ZrTkRJdE5EZGhaQzAwT1RCaUxXSmlOekF0WW1JM016UTVOVEUwTVRnMzo2NmRiNThkNWY1ZDBmODg2N2MxZGUwZGQiLCJhdWQiOiIqLnBsdXRvLnR2IiwiZXhwIjoxNzI2MzE3MzA2LCJpYXQiOjE3MjYyMzA5MDYsImp0aSI6IjVmMWExZmRlLTIyZmMtNDM1NC04NGY1LTdjYjhjNTNiZTA0YiJ9.IM8AcfF0hNcPdLOZBhCHEOziOF-k1s5xL5nfPhCMpXM",
    "origin": "https://pluto.tv",
    "referer": "https://pluto.tv/",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

# Medir el tiempo de inicio
start_time_total = time.time()

# Medir el tiempo de inicio para LiveTV
start_time = time.time()

# Obtener los datos de las categorías (LiveTV)
response1 = requests.get(url1, headers=headers1)
categories = {}
if response1.status_code == 200:
    response_json1 = response1.json()  # Parsear la respuesta a JSON
    categories = {item.get("id"): item.get("name") for item in response_json1.get("data", [])}
else:
    print(f"Error en la solicitud: {response1.status_code}")

# Obtener los datos de los canales (LiveTV)
response2 = requests.get(url2, headers=headers2)
channels = []
metadata = {}
if response2.status_code == 200:
    response_json2 = response2.json()  # Parsear la respuesta a JSON
    channels = [
        {
            "name": item.get("name"),
            "categoryIDs": item.get("categoryIDs"),
            "summary": item.get("summary"),
            "hash": item.get("hash")
        } 
        for item in response_json2.get("data", [])
    ]
    metadata = {
        "Número de Canales": len(response_json2.get("data", [])),
        "Número de Categorías": len(categories)
    }
else:
    print(f"Error en la solicitud: {response2.status_code}")

# Crear la estructura LiveTV
live_tv = {"meta": metadata, "Categorías": {}}

for channel in channels:
    for category_id in channel["categoryIDs"]:
        category_name = categories.get(category_id, "Unknown Category")
        if category_name not in live_tv["Categorías"]:
            live_tv["Categorías"][category_name] = {}
        live_tv["Categorías"][category_name][channel["name"]] = {
            "Resumen": channel["summary"],
            "hash": channel["hash"]
        }

# Medir el tiempo de finalización
end_time = time.time()
execution_time_live_tv = end_time - start_time
live_tv["meta"]["Tiempo de Ejecución (en segundos)"] = execution_time_live_tv


# --------- CÓDIGO 2: Manejo de OnDemand ---------
# Función para extraer el año del slug
def extraer_año_de_slug(slug):
    match = re.search(r'-\d{4}-', slug)
    if match:
        return match.group(0)[1:5]  # Devuelve el año encontrado
    return None

# Función para obtener las películas y series de una subcategoría
def obtener_movies_y_series(sub_category_id):
    urlondemand = f"https://service-vod.clusters.pluto.tv/v4/vod/categories/{sub_category_id}/items?offset=30&page=1"
    headers_ondemand = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "es-419,es;q=0.9",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6IjFkODRkYzg4LTcxMWItNDBkNi1hN2M4LTRlZTFjOTY4YTE5YiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSUQiOiJlYzMyYTZjZS03MTMzLTExZWYtOGM0OC1lYTM1MmM1Y2ZiZjMiLCJjbGllbnRJUCI6IjE2My4xMC4zNi40IiwiY2l0eSI6IkxhIFBsYXRhIiwicG9zdGFsQ29kZSI6ImIxOTA2IGZkYSIsImNvdW50cnkiOiJBUiIsImRtYSI6MCwiYWN0aXZlUmVnaW9uIjoiVkUiLCJkZXZpY2VMYXQiOi0zNC45MzAwMDAzMDUxNzU3OCwiZGV2aWNlTG9uIjotNTcuOTU5OTk5MDg0NDcyNjU2LCJwcmVmZXJyZWRMYW5ndWFnZSI6ImVzIiwiZGV2aWNlVHlwZSI6IndlYiIsImRldmljZVZlcnNpb24iOiIxMjguMC4wIiwiZGV2aWNlTWFrZSI6ImNocm9tZSIsImRldmljZU1vZGVsIjoid2ViIiwiYXBwTmFtZSI6IndlYiIsImFwcFZlcnNpb24iOiI5LjQuMC05Y2E1MWNhMTBjMzA0N2ZiYWZhNzI5NzcwOGYxNDYyNDMxNDZkMTI1IiwiY2xpZW50SUQiOiI5MDEwZWQ0Mi00N2FkLTQ5MGItYmI3MC1iYjczNDk1MTQxODciLCJjbUF1ZGllbmNlSUQiOiIiLCJpc0NsaWVudEROVCI6ZmFsc2UsInVzZXJJRCI6IjY2ZGI1OGQ1ZjVkMGY4ODY3YzFkZTBkZCIsInVzZXJCcmFuZCI6InBsdXRvdHYiLCJsb2dMZXZlbCI6IkRFRkFVTFQiLCJ0aW1lWm9uZSI6IkFtZXJpY2EvQXJnZW50aW5hL0J1ZW5vc19BaXJlcyIsInNlcnZlclNpZGVBZHMiOmZhbHNlLCJlMmVCZWFjb25zIjpmYWxzZSwiZmVhdHVyZXMiOnsibXVsdGlQb2RBZHMiOnsiZW5hYmxlZCI6dHJ1ZX19LCJlbnRpdGxlbWVudHMiOlsiUmVnaXN0ZXJlZCJdLCJmbXNQYXJhbXMiOnsiZndWY0lEMiI6ImYyZTk0OWNlM2Q1OWIwZTE0YWFjODUxMTQyODYzODQ5NDk3ZjAzNGI4YjJjZjg3OGYwMGEyNGM3Zjg1ODI4YzMiLCJmd1ZjSUQyQ29wcGEiOiI5MDEwZWQ0Mi00N2FkLTQ5MGItYmI3MC1iYjczNDk1MTQxODciLCJjdXN0b21QYXJhbXMiOnsiZm1zX2xpdmVyYW1wX2lkbCI6IiIsImZtc19lbWFpbGhhc2giOiJmMmU5NDljZTNkNTliMGUxNGFhYzg1MTE0Mjg2Mzg0OTQ5N2YwMzRiOGIyY2Y4NzhmMDBhMjRjN2Y4NTgyOGMzIiwiZm1zX3N1YnNjcmliZXJpZCI6IjY2ZGI1OGQ1ZjVkMGY4ODY3YzFkZTBkZCIsImZtc19pZmEiOiIiLCJmbXNfaWRmdiI6IiIsImZtc191c2VyaWQiOiI5MDEwZWQ0Mi00N2FkLTQ5MGItYmI3MC1iYjczNDk1MTQxODciLCJmbXNfdmNpZDJ0eXBlIjoiZW1haWxoYXNoIiwiZm1zX3JhbXBfaWQiOiIiLCJmbXNfaGhfcmFtcF9pZCI6IiIsImZtc19iaWRpZHR5cGUiOiIiLCJfZndfM1BfVUlEIjoiIiwiZm1zX3J1bGVpZCI6IjEwMDAwLDEwMDAzIn19LCJkcm0iOnsibmFtZSI6IndpZGV2aW5lIiwibGV2ZWwiOiJMMyJ9LCJpc3MiOiJib290LnBsdXRvLnR2Iiwic3ViIjoicHJpOnYxOnBsdXRvOnVzZXJzLXYxOlZFOk9UQXhNR1ZrTkRJdE5EZGhaQzAwT1RCaUxXSmlOekF0WW1JM016UTVOVEUwTVRnMzo2NmRiNThkNWY1ZDBmODg2N2MxZGUwZGQiLCJhdWQiOiIqLnBsdXRvLnR2IiwiZXhwIjoxNzI2MjUxNzMwLCJpYXQiOjE3MjYxNjUzMzAsImp0aSI6IjAxYjA1YjRmLTQ1YTMtNDI2Yi1iZjE1LTY5ODE2YmZiYjRkZCJ9.39rl2XvMQ_a-IvRKN-QimoS7aJVyhnX6R1LR2zu_j6o",
    "origin": "https://pluto.tv",
    "referer": "https://pluto.tv/",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}
    response = requests.get(urlondemand, headers=headers_ondemand)
    movieseries = []
    if response.status_code == 200:
        items = response.json().get("items", [])
        for item in items:
            tipo = item.get("type")
            titulo = item.get("name")
            resumen = item.get("description")
            id_contenido = item.get("_id")
            clasificacion = item.get("rating")
            genero = item.get("genre")

            if tipo == "movie":
                slug = item.get("slug")
                año = extraer_año_de_slug(slug)
                link = f"https://pluto.tv/latam/on-demand/movies/{id_contenido}"
                link_detalles = f"https://pluto.tv/latam/on-demand/movies/{id_contenido}/details"
            elif tipo == "series":
                año = None
                link = f"https://pluto.tv/latam/search/details/series/{id_contenido}/season/1"
                link_detalles = None

            movieseries.append({
                "Título": titulo,
                "Año": año,
                "Resumen": resumen,
                "Categoria_id": sub_category_id,
                "Link": link,
                "Link_detalles": link_detalles,
                "Tipo": tipo,
                "Clasificación": clasificacion,
                "Género": genero
            })
    else:
        print(f"Error al obtener movies y series de la subcategoría {sub_category_id}: {response.status_code}")
    return movieseries

# Obtener categorías principales y subcategorías
url_main_categories = "https://service-media-catalog.clusters.pluto.tv/v1/main-categories?includeImages=svg"
url_sub_categories = "https://service-vod.clusters.pluto.tv/v4/vod/categories?includeItems=false&includeCategoryFields=iconSvg&offset=1000&page=1&sort=number%3Aasc"

# Headers para la API de categorías principales
headers_main_categories = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "es-419,es;q=0.9",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6IjFkODRkYzg4LTcxMWItNDBkNi1hN2M4LTRlZTFjOTY4YTE5YiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSUQiOiJlYzMyYTZjZS03MTMzLTExZWYtOGM0OC1lYTM1MmM1Y2ZiZjMiLCJjbGllbnRJUCI6IjE2My4xMC4zNi40IiwiY2l0eSI6IkxhIFBsYXRhIiwicG9zdGFsQ29kZSI6ImIxOTA2IGZkYSIsImNvdW50cnkiOiJBUiIsImRtYSI6MCwiYWN0aXZlUmVnaW9uIjoiVkUiLCJkZXZpY2VMYXQiOi0zNC45MzAwMDAzMDUxNzU3OCwiZGV2aWNlTG9uIjotNTcuOTU5OTk5MDg0NDcyNjU2LCJwcmVmZXJyZWRMYW5ndWFnZSI6ImVzIiwiZGV2aWNlVHlwZSI6IndlYiIsImRldmljZVZlcnNpb24iOiIxMjguMC4wIiwiZGV2aWNlTWFrZSI6ImNocm9tZSIsImRldmljZU1vZGVsIjoid2ViIiwiYXBwTmFtZSI6IndlYiIsImFwcFZlcnNpb24iOiI5LjQuMC05Y2E1MWNhMTBjMzA0N2ZiYWZhNzI5NzcwOGYxNDYyNDMxNDZkMTI1IiwiY2xpZW50SUQiOiI5MDEwZWQ0Mi00N2FkLTQ5MGItYmI3MC1iYjczNDk1MTQxODciLCJjbUF1ZGllbmNlSUQiOiIiLCJpc0NsaWVudEROVCI6ZmFsc2UsInVzZXJJRCI6IjY2ZGI1OGQ1ZjVkMGY4ODY3YzFkZTBkZCIsInVzZXJCcmFuZCI6InBsdXRvdHYiLCJsb2dMZXZlbCI6IkRFRkFVTFQiLCJ0aW1lWm9uZSI6IkFtZXJpY2EvQXJnZW50aW5hL0J1ZW5vc19BaXJlcyIsInNlcnZlclNpZGVBZHMiOmZhbHNlLCJlMmVCZWFjb25zIjpmYWxzZSwiZmVhdHVyZXMiOnsibXVsdGlQb2RBZHMiOnsiZW5hYmxlZCI6dHJ1ZX19LCJlbnRpdGxlbWVudHMiOlsiUmVnaXN0ZXJlZCJdLCJmbXNQYXJhbXMiOnsiZndWY0lEMiI6ImYyZTk0OWNlM2Q1OWIwZTE0YWFjODUxMTQyODYzODQ5NDk3ZjAzNGI4YjJjZjg3OGYwMGEyNGM3Zjg1ODI4YzMiLCJmd1ZjSUQyQ29wcGEiOiI5MDEwZWQ0Mi00N2FkLTQ5MGItYmI3MC1iYjczNDk1MTQxODciLCJjdXN0b21QYXJhbXMiOnsiZm1zX2xpdmVyYW1wX2lkbCI6IiIsImZtc19lbWFpbGhhc2giOiJmMmU5NDljZTNkNTliMGUxNGFhYzg1MTE0Mjg2Mzg0OTQ5N2YwMzRiOGIyY2Y4NzhmMDBhMjRjN2Y4NTgyOGMzIiwiZm1zX3N1YnNjcmliZXJpZCI6IjY2ZGI1OGQ1ZjVkMGY4ODY3YzFkZTBkZCIsImZtc19pZmEiOiIiLCJmbXNfaWRmdiI6IiIsImZtc191c2VyaWQiOiI5MDEwZWQ0Mi00N2FkLTQ5MGItYmI3MC1iYjczNDk1MTQxODciLCJmbXNfdmNpZDJ0eXBlIjoiZW1haWxoYXNoIiwiZm1zX3JhbXBfaWQiOiIiLCJmbXNfaGhfcmFtcF9pZCI6IiIsImZtc19iaWRpZHR5cGUiOiIiLCJfZndfM1BfVUlEIjoiIiwiZm1zX3J1bGVpZCI6IjEwMDAwLDEwMDAzIn19LCJkcm0iOnsibmFtZSI6IndpZGV2aW5lIiwibGV2ZWwiOiJMMyJ9LCJpc3MiOiJib290LnBsdXRvLnR2Iiwic3ViIjoicHJpOnYxOnBsdXRvOnVzZXJzLXYxOlZFOk9UQXhNR1ZrTkRJdE5EZGhaQzAwT1RCaUxXSmlOekF0WW1JM016UTVOVEUwTVRnMzo2NmRiNThkNWY1ZDBmODg2N2MxZGUwZGQiLCJhdWQiOiIqLnBsdXRvLnR2IiwiZXhwIjoxNzI2MjUxNzMwLCJpYXQiOjE3MjYxNjUzMzAsImp0aSI6IjAxYjA1YjRmLTQ1YTMtNDI2Yi1iZjE1LTY5ODE2YmZiYjRkZCJ9.39rl2XvMQ_a-IvRKN-QimoS7aJVyhnX6R1LR2zu_j6o",
    "origin": "https://pluto.tv",
    "referer": "https://pluto.tv/",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

# Headers para la API de subcategorías
headers_sub_categories = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "es-419,es;q=0.9",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6IjFkODRkYzg4LTcxMWItNDBkNi1hN2M4LTRlZTFjOTY4YTE5YiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSUQiOiJlYzMyYTZjZS03MTMzLTExZWYtOGM0OC1lYTM1MmM1Y2ZiZjMiLCJjbGllbnRJUCI6IjE2My4xMC4zNi40IiwiY2l0eSI6IkxhIFBsYXRhIiwicG9zdGFsQ29kZSI6ImIxOTA2IGZkYSIsImNvdW50cnkiOiJBUiIsImRtYSI6MCwiYWN0aXZlUmVnaW9uIjoiVkUiLCJkZXZpY2VMYXQiOi0zNC45MzAwMDAzMDUxNzU3OCwiZGV2aWNlTG9uIjotNTcuOTU5OTk5MDg0NDcyNjU2LCJwcmVmZXJyZWRMYW5ndWFnZSI6ImVzIiwiZGV2aWNlVHlwZSI6IndlYiIsImRldmljZVZlcnNpb24iOiIxMjguMC4wIiwiZGV2aWNlTWFrZSI6ImNocm9tZSIsImRldmljZU1vZGVsIjoid2ViIiwiYXBwTmFtZSI6IndlYiIsImFwcFZlcnNpb24iOiI5LjQuMC05Y2E1MWNhMTBjMzA0N2ZiYWZhNzI5NzcwOGYxNDYyNDMxNDZkMTI1IiwiY2xpZW50SUQiOiI5MDEwZWQ0Mi00N2FkLTQ5MGItYmI3MC1iYjczNDk1MTQxODciLCJjbUF1ZGllbmNlSUQiOiIiLCJpc0NsaWVudEROVCI6ZmFsc2UsInVzZXJJRCI6IjY2ZGI1OGQ1ZjVkMGY4ODY3YzFkZTBkZCIsInVzZXJCcmFuZCI6InBsdXRvdHYiLCJsb2dMZXZlbCI6IkRFRkFVTFQiLCJ0aW1lWm9uZSI6IkFtZXJpY2EvQXJnZW50aW5hL0J1ZW5vc19BaXJlcyIsInNlcnZlclNpZGVBZHMiOmZhbHNlLCJlMmVCZWFjb25zIjpmYWxzZSwiZmVhdHVyZXMiOnsibXVsdGlQb2RBZHMiOnsiZW5hYmxlZCI6dHJ1ZX19LCJlbnRpdGxlbWVudHMiOlsiUmVnaXN0ZXJlZCJdLCJmbXNQYXJhbXMiOnsiZndWY0lEMiI6ImYyZTk0OWNlM2Q1OWIwZTE0YWFjODUxMTQyODYzODQ5NDk3ZjAzNGI4YjJjZjg3OGYwMGEyNGM3Zjg1ODI4YzMiLCJmd1ZjSUQyQ29wcGEiOiI5MDEwZWQ0Mi00N2FkLTQ5MGItYmI3MC1iYjczNDk1MTQxODciLCJjdXN0b21QYXJhbXMiOnsiZm1zX2xpdmVyYW1wX2lkbCI6IiIsImZtc19lbWFpbGhhc2giOiJmMmU5NDljZTNkNTliMGUxNGFhYzg1MTE0Mjg2Mzg0OTQ5N2YwMzRiOGIyY2Y4NzhmMDBhMjRjN2Y4NTgyOGMzIiwiZm1zX3N1YnNjcmliZXJpZCI6IjY2ZGI1OGQ1ZjVkMGY4ODY3YzFkZTBkZCIsImZtc19pZmEiOiIiLCJmbXNfaWRmdiI6IiIsImZtc191c2VyaWQiOiI5MDEwZWQ0Mi00N2FkLTQ5MGItYmI3MC1iYjczNDk1MTQxODciLCJmbXNfdmNpZDJ0eXBlIjoiZW1haWxoYXNoIiwiZm1zX3JhbXBfaWQiOiIiLCJmbXNfaGhfcmFtcF9pZCI6IiIsImZtc19iaWRpZHR5cGUiOiIiLCJfZndfM1BfVUlEIjoiIiwiZm1zX3J1bGVpZCI6IjEwMDAwLDEwMDAzIn19LCJkcm0iOnsibmFtZSI6IndpZGV2aW5lIiwibGV2ZWwiOiJMMyJ9LCJpc3MiOiJib290LnBsdXRvLnR2Iiwic3ViIjoicHJpOnYxOnBsdXRvOnVzZXJzLXYxOlZFOk9UQXhNR1ZrTkRJdE5EZGhaQzAwT1RCaUxXSmlOekF0WW1JM016UTVOVEUwTVRnMzo2NmRiNThkNWY1ZDBmODg2N2MxZGUwZGQiLCJhdWQiOiIqLnBsdXRvLnR2IiwiZXhwIjoxNzI2MjUxNzMwLCJpYXQiOjE3MjYxNjUzMzAsImp0aSI6IjAxYjA1YjRmLTQ1YTMtNDI2Yi1iZjE1LTY5ODE2YmZiYjRkZCJ9.39rl2XvMQ_a-IvRKN-QimoS7aJVyhnX6R1LR2zu_j6o",
    "origin": "https://pluto.tv",
    "referer": "https://pluto.tv/",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

# Obtener categorías principales
response_main = requests.get(url_main_categories, headers=headers_main_categories)
main_categories = response_main.json().get("data", []) if response_main.status_code == 200 else []

# Obtener subcategorías
response_sub = requests.get(url_sub_categories, headers=headers_sub_categories)
sub_categories = response_sub.json().get("categories", []) if response_sub.status_code == 200 else []

# Medir el tiempo de inicio para OnDemand
start_time_ondemand = time.time()

# Crear el diccionario OnDemand
on_demand = {}
for main_category in main_categories:
    main_category_id = main_category.get("id")
    main_category_name = main_category.get("name")
    on_demand[main_category_name] = {}

    for sub_category in sub_categories:
        main_category_ids = [mc.get("categoryID") for mc in sub_category.get("mainCategories", [])]
        if main_category_id in main_category_ids:
            sub_category_name = sub_category.get("name")
            sub_category_id = sub_category.get("_id")
            movieseries = obtener_movies_y_series(sub_category_id)
            on_demand[main_category_name][sub_category_name] = movieseries

# Medir el tiempo de finalización para OnDemand
end_time_ondemand = time.time()
execution_time_ondemand = end_time_ondemand - start_time_ondemand

# --------- Unir LiveTV y OnDemand en un solo JSON ---------
end_time_total = time.time()
execution_time_total = end_time_total - start_time_total

# Agregar el tiempo de ejecución total al principio del JSON
final_json = {
    "meta": {
        "Tiempo de Ejecución Total (en segundos)": execution_time_total
    },
    "LiveTV": live_tv,
    "OnDemand": on_demand
}

# Guardar el JSON en un archivo
with open("plutotv_scraping.json", "w", encoding="utf-8") as json_file:
    json.dump(final_json, json_file, indent=4, ensure_ascii=False)

# Imprimir el JSON final
print(json.dumps(final_json, indent=4, ensure_ascii=False))