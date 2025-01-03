import requests

# URL do seu servidor Flask (substitua pelo endereço correto)
url = "http://127.0.0.1:52046/api/recommend"

musicas_entrada = ["Purpose", "Sorry", "Into You", "Save Your Tears"]
dados = {"songs": musicas_entrada}

resposta = requests.post(url, json=dados)

if resposta.status_code == 200:
    musicas_recomendadas = resposta.json()
    print("resposta: ", musicas_recomendadas)
else:
    print(f"Erro na requisição: {resposta.status_code}")
