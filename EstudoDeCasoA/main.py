import requests
import re
import pandas as pd
import os

# URL do site
url = "https://noticias.uol.com.br/blogs-e-colunas/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

# Caminho para salvar os arquivos dentro da pasta EstudoDeCasoA
diretorio = "EstudoDeCasoA"
os.makedirs(diretorio, exist_ok=True)  # Cria a pasta EstudoDeCasoA se não existir

# Acessa o site e captura o código-fonte
response = requests.get(url, headers=headers)
nome_arquivo = os.path.join(diretorio, "codigo_fonte_uol.txt")

if response.status_code == 200:
    codigo_fonte = response.text
    
    # Salvar o código-fonte em um arquivo de texto dentro da pasta EstudoDeCasoA
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(codigo_fonte)
        print(f"Arquivo '{nome_arquivo}' salvo com sucesso.")
    except IOError as e:
        print(f"Erro ao salvar o arquivo: {e}")
else:
    print("Erro ao acessar a página.")
    exit()

# Passo 2: Ler o conteúdo do arquivo de texto para análise
try:
    with open(nome_arquivo, "r", encoding="utf-8") as file:
        conteudo = file.read()
except FileNotFoundError:
    print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
    exit()

# --- Extração das Notícias ---

# Regex para capturar Título, Texto e Autor das notícias
regex_noticia = r'<span class="thumb-kicker.*?>(.*?)<\/span>.*?<h3 class="thumb-title.*?>(.*?)<\/h3>.*?<p class="author.*?>(.*?)<\/p>'
noticias = re.findall(regex_noticia, conteudo, re.DOTALL)

# Armazenar os dados das notícias em um DataFrame no formato especificado
dados_noticias = []
for noticia in noticias:
    titulo = noticia[0].strip()
    texto = noticia[1].strip()
    autor = noticia[2].strip()
    dados_noticias.append({"Título": titulo, "Texto": texto, "Autor": autor})

df_noticias = pd.DataFrame(dados_noticias)

# Salvar o DataFrame das notícias em um arquivo CSV dentro da pasta EstudoDeCasoA
caminho_noticias_csv = os.path.join(diretorio, "noticias_uol.csv")
df_noticias.to_csv(caminho_noticias_csv, index=False, encoding="utf-8", sep=";")
print(f"Arquivo '{caminho_noticias_csv}' criado com sucesso.")

# --- Extração dos Colunistas ---

# Regex para capturar Nome e Imagem dos colunistas
regex_colunista = r'<li class="blogger.*?<h4 class="h-components">(.*?)<\/h4>.*?data-src="(https:\/\/conteudo\.imguol\.com\.br\/[^"]+)"'
colunistas = re.findall(regex_colunista, conteudo, re.DOTALL)

# Armazenar os dados dos colunistas em um DataFrame no formato especificado
dados_colunistas = []
for colunista in colunistas:
    nome = colunista[0].strip()
    imagem = colunista[1].strip()
    dados_colunistas.append({"Nome": nome, "Imagem": imagem})

df_colunistas = pd.DataFrame(dados_colunistas)

# Salvar o DataFrame dos colunistas em um arquivo CSV dentro da pasta EstudoDeCasoA
caminho_colunistas_csv = os.path.join(diretorio, "colunistas_uol.csv")
df_colunistas.to_csv(caminho_colunistas_csv, index=False, encoding="utf-8", sep=";")
print(f"Arquivo '{caminho_colunistas_csv}' criado com sucesso.")
