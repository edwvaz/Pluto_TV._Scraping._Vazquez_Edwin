import json
import requests
import time
import re

# --------- CÓDIGO 1: Manejo de LiveTV ---------
# Definir las URLs de las APIs
url1 = "https://service-media-catalog.clusters.pluto.tv/v1/main-categories?includeImages=svg"
url2 = "https://service-channels.clusters.pluto.tv/v2/guide/channels?channelIds=&offset=0&limit=1000&sort=number%3Aasc"

# Definir los headers para la primera API de LiveTV (categorías)
headers1 = {}

# Definir los headers para la segunda API de LiveTV (canales)
headers2 = {}

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
    headers_ondemand = {}
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
headers_main_categories = {}

# Headers para la API de subcategorías
headers_sub_categories = {}

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
