import json
import requests
import time

# Definir las URLs de las APIs
url1 = "https://service-media-catalog.clusters.pluto.tv/v1/main-categories?includeImages=svg"
url2 = "https://service-channels.clusters.pluto.tv/v2/guide/channels?channelIds=&offset=0&limit=1000&sort=number%3Aasc"

# Definir los headers necesarios

headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "es-419,es;q=0.9",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6IjJmNzg3YmJjLWFkYTgtNGE1YS1hNTZmLTdmMDNkYTFkMTczYSIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSUQiOiI0ZjMxNjExMi02ZWE1LTExZWYtYTNmMi1jNmMwOTQ0NThkNzQiLCJjbGllbnRJUCI6IjE5MC4xMDYuNDUuMTQxIiwiY2l0eSI6IkJlcmlzc28iLCJwb3N0YWxDb2RlIjoiYjE5MjMgZmJlIiwiY291bnRyeSI6IkFSIiwiZG1hIjowLCJhY3RpdmVSZWdpb24iOiJWRSIsImRldmljZUxhdCI6LTM0Ljg4OTk5OTM4OTY0ODQ0LCJkZXZpY2VMb24iOi01Ny45MDAwMDE1MjU4Nzg5MDYsInByZWZlcnJlZExhbmd1YWdlIjoiZXMiLCJkZXZpY2VUeXBlIjoid2ViIiwiZGV2aWNlVmVyc2lvbiI6IjEyOC4wLjAiLCJkZXZpY2VNYWtlIjoiY2hyb21lIiwiZGV2aWNlTW9kZWwiOiJ3ZWIiLCJhcHBOYW1lIjoid2ViIiwiYXBwVmVyc2lvbiI6IjkuMy4wLTY5MTQ2ZTk2NjgxYTcwZTBlNWY0ZjQwOTQyZDBhYmM2N2YwNDg2NGEiLCJjbGllbnRJRCI6IjkwMTBlZDQyLTQ3YWQtNDkwYi1iYjcwLWJiNzM0OTUxNDE4NyIsImNtQXVkaWVuY2VJRCI6IiIsImlzQ2xpZW50RE5UIjpmYWxzZSwidXNlcklEIjoiNjZkYjU4ZDVmNWQwZjg4NjdjMWRlMGRkIiwidXNlckJyYW5kIjoicGx1dG90diIsImxvZ0xldmVsIjoiREVGQVVMVCIsInRpbWVab25lIjoiQW1lcmljYS9BcmdlbnRpbmEvQnVlbm9zX0FpcmVzIiwic2VydmVyU2lkZUFkcyI6ZmFsc2UsImUyZUJlYWNvbnMiOmZhbHNlLCJmZWF0dXJlcyI6eyJtdWx0aVBvZEFkcyI6eyJlbmFibGVkIjp0cnVlfX0sImVudGl0bGVtZW50cyI6WyJSZWdpc3RlcmVkIl0sImZtc1BhcmFtcyI6eyJmd1ZjSUQyIjoiZjJlOTQ5Y2UzZDU5YjBlMTRhYWM4NTExNDI4NjM4NDk0OTdmMDM0YjhiMmNmODc4ZjAwYTI0YzdmODU4MjhjMyIsImZ3VmNJRDJDb3BwYSI6IjkwMTBlZDQyLTQ3YWQtNDkwYi1iYjcwLWJiNzM0OTUxNDE4NyIsImN1c3RvbVBhcmFtcyI6eyJmbXNfbGl2ZXJhbXBfaWRsIjoiIiwiZm1zX2VtYWlsaGFzaCI6ImYyZTk0OWNlM2Q1OWIwZTE0YWFjODUxMTQyODYzODQ5NDk3ZjAzNGI4YjJjZjg3OGYwMGEyNGM3Zjg1ODI4YzMiLCJmbXNfc3Vic2NyaWJlcmlkIjoiNjZkYjU4ZDVmNWQwZjg4NjdjMWRlMGRkIiwiZm1zX2lmYSI6IiIsImZtc19pZGZ2IjoiIiwiZm1zX3VzZXJpZCI6IjkwMTBlZDQyLTQ3YWQtNDkwYi1iYjcwLWJiNzM0OTUxNDE4NyIsImZtc192Y2lkMnR5cGUiOiJlbWFpbGhhc2giLCJmbXNfcmFtcF9pZCI6IiIsImZtc19oaF9yYW1wX2lkIjoiIiwiZm1zX2JpZGlkdHlwZSI6IiIsIl9md18zUF9VSUQiOiIiLCJmbXNfcnVsZWlkIjoiMTAwMDAsMTAwMDMifX0sImRybSI6eyJuYW1lIjoid2lkZXZpbmUiLCJsZXZlbCI6IkwzIn0sImlzcyI6ImJvb3QucGx1dG8udHYiLCJzdWIiOiJwcmk6djE6cGx1dG86dXNlcnMtdjE6VkU6T1RBeE1HVmtOREl0TkRkaFpDMDBPVEJpTFdKaU56QXRZbUkzTXpRNU5URTBNVGczOjY2ZGI1OGQ1ZjVkMGY4ODY3YzFkZTBkZCIsImF1ZCI6IioucGx1dG8udHYiLCJleHAiOjE3MjU5NzA1NzYsImlhdCI6MTcyNTg4NDE3NiwianRpIjoiZmY4ZmFhODgtMGUwZS00YWFjLWEyMjMtYTAzODc4YWRiNmUxIn0.J0wetAuali1xXmCZk8qjQyUcu53iFqHytA4mMMkl-tQ",
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

headers2 = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "es-419,es;q=0.9",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6IjJmNzg3YmJjLWFkYTgtNGE1YS1hNTZmLTdmMDNkYTFkMTczYSIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSUQiOiI0ZjMxNjExMi02ZWE1LTExZWYtYTNmMi1jNmMwOTQ0NThkNzQiLCJjbGllbnRJUCI6IjE5MC4xMDYuNDUuMTQxIiwiY2l0eSI6IkJlcmlzc28iLCJwb3N0YWxDb2RlIjoiYjE5MjMgZmJlIiwiY291bnRyeSI6IkFSIiwiZG1hIjowLCJhY3RpdmVSZWdpb24iOiJWRSIsImRldmljZUxhdCI6LTM0Ljg4OTk5OTM4OTY0ODQ0LCJkZXZpY2VMb24iOi01Ny45MDAwMDE1MjU4Nzg5MDYsInByZWZlcnJlZExhbmd1YWdlIjoiZXMiLCJkZXZpY2VUeXBlIjoid2ViIiwiZGV2aWNlVmVyc2lvbiI6IjEyOC4wLjAiLCJkZXZpY2VNYWtlIjoiY2hyb21lIiwiZGV2aWNlTW9kZWwiOiJ3ZWIiLCJhcHBOYW1lIjoid2ViIiwiYXBwVmVyc2lvbiI6IjkuMy4wLTY5MTQ2ZTk2NjgxYTcwZTBlNWY0ZjQwOTQyZDBhYmM2N2YwNDg2NGEiLCJjbGllbnRJRCI6IjkwMTBlZDQyLTQ3YWQtNDkwYi1iYjcwLWJiNzM0OTUxNDE4NyIsImNtQXVkaWVuY2VJRCI6IiIsImlzQ2xpZW50RE5UIjpmYWxzZSwidXNlcklEIjoiNjZkYjU4ZDVmNWQwZjg4NjdjMWRlMGRkIiwidXNlckJyYW5kIjoicGx1dG90diIsImxvZ0xldmVsIjoiREVGQVVMVCIsInRpbWVab25lIjoiQW1lcmljYS9BcmdlbnRpbmEvQnVlbm9zX0FpcmVzIiwic2VydmVyU2lkZUFkcyI6ZmFsc2UsImUyZUJlYWNvbnMiOmZhbHNlLCJmZWF0dXJlcyI6eyJtdWx0aVBvZEFkcyI6eyJlbmFibGVkIjp0cnVlfX0sImVudGl0bGVtZW50cyI6WyJSZWdpc3RlcmVkIl0sImZtc1BhcmFtcyI6eyJmd1ZjSUQyIjoiZjJlOTQ5Y2UzZDU5YjBlMTRhYWM4NTExNDI4NjM4NDk0OTdmMDM0YjhiMmNmODc4ZjAwYTI0YzdmODU4MjhjMyIsImZ3VmNJRDJDb3BwYSI6IjkwMTBlZDQyLTQ3YWQtNDkwYi1iYjcwLWJiNzM0OTUxNDE4NyIsImN1c3RvbVBhcmFtcyI6eyJmbXNfbGl2ZXJhbXBfaWRsIjoiIiwiZm1zX2VtYWlsaGFzaCI6ImYyZTk0OWNlM2Q1OWIwZTE0YWFjODUxMTQyODYzODQ5NDk3ZjAzNGI4YjJjZjg3OGYwMGEyNGM3Zjg1ODI4YzMiLCJmbXNfc3Vic2NyaWJlcmlkIjoiNjZkYjU4ZDVmNWQwZjg4NjdjMWRlMGRkIiwiZm1zX2lmYSI6IiIsImZtc19pZGZ2IjoiIiwiZm1zX3VzZXJpZCI6IjkwMTBlZDQyLTQ3YWQtNDkwYi1iYjcwLWJiNzM0OTUxNDE4NyIsImZtc192Y2lkMnR5cGUiOiJlbWFpbGhhc2giLCJmbXNfcmFtcF9pZCI6IiIsImZtc19oaF9yYW1wX2lkIjoiIiwiZm1zX2JpZGlkdHlwZSI6IiIsIl9md18zUF9VSUQiOiIiLCJmbXNfcnVsZWlkIjoiMTAwMDAsMTAwMDMifX0sImRybSI6eyJuYW1lIjoid2lkZXZpbmUiLCJsZXZlbCI6IkwzIn0sImlzcyI6ImJvb3QucGx1dG8udHYiLCJzdWIiOiJwcmk6djE6cGx1dG86dXNlcnMtdjE6VkU6T1RBeE1HVmtOREl0TkRkaFpDMDBPVEJpTFdKaU56QXRZbUkzTXpRNU5URTBNVGczOjY2ZGI1OGQ1ZjVkMGY4ODY3YzFkZTBkZCIsImF1ZCI6IioucGx1dG8udHYiLCJleHAiOjE3MjU5NzA1NzYsImlhdCI6MTcyNTg4NDE3NiwianRpIjoiZmY4ZmFhODgtMGUwZS00YWFjLWEyMjMtYTAzODc4YWRiNmUxIn0.J0wetAuali1xXmCZk8qjQyUcu53iFqHytA4mMMkl-tQ",
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
start_time = time.time()

# Obtener los datos de las categorías (Código1)
response1 = requests.get(url1, headers=headers)
if response1.status_code == 200:
    response_json1 = response1.json()  # Parsear la respuesta a JSON
    categories = {item.get("id"): item.get("name") for item in response_json1.get("data", [])}
else:
    print(f"Error en la solicitud: {response1.status_code}")

# Obtener los datos de los canales (Código2) y la metadata
response2 = requests.get(url2, headers=headers2)
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
        #"totalCount": response_json2.get("totalCount"),
        #"limit": response_json2.get("limit"),
        "Número de Canales": len(response_json2.get("data", [])),
        "Número de Categorías": len(categories)
    }
else:
    print(f"Error en la solicitud: {response2.status_code}")

# Crear la estructura final
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
execution_time = end_time - start_time
live_tv["meta"]["Tiempo de Ejecución (en segundos)"] = execution_time

# Crear el JSON final
final_json = {"LiveTV": live_tv}

# Guardar el JSON en un archivo
with open("live_tv.json", "w", encoding="utf-8") as json_file:
    json.dump(final_json, json_file, indent=4, ensure_ascii=False)

# Imprimir el JSON final
print(json.dumps(final_json, indent=4, ensure_ascii=False))