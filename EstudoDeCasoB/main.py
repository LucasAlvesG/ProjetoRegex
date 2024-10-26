import requests
import re
import pandas as pd
import os

# URL do edital
url = "https://www.in.gov.br/web/dou/-/edital-n-10/2024-589442586"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

# Caminho para salvar os arquivos dentro da pasta EstudoDeCasoB
diretorio = "EstudoDeCasoB"
os.makedirs(diretorio, exist_ok=True)  # Cria a pasta EstudoDeCasoB se não existir

# Acessa o site e captura o código-fonte
response = requests.get(url, headers=headers)
nome_arquivo = os.path.join(diretorio, "codigo_fonte_edital.txt")

if response.status_code == 200:
    codigo_fonte = response.text
    
    # Salvar o código-fonte em um arquivo de texto dentro da pasta EstudoDeCasoB
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

# --- Extração dos Dados da Tabela de Pessoas (MATRÍCULA, NOME, ÓRGÃO, TIPO) ---

# Expressão regular para capturar MATRÍCULA, NOME, ÓRGÃO e TIPO
regex_dados_pessoas = r'<td rowspan="1" colspan="1"><p class="dou-paragraph" ?>(\d+)</p></td>\s*' + \
                      r'<td rowspan="1" colspan="1"><p class="dou-paragraph" ?>(.*?)</p></td>\s*' + \
                      r'<td rowspan="1" colspan="1"><p class="dou-paragraph" ?>(\d+)</p></td>\s*' + \
                      r'<td rowspan="1" colspan="1"><p class="dou-paragraph" ?>(.*?)</p></td>'

# Encontrar todas as ocorrências correspondentes para a tabela de pessoas
dados_pessoas = re.findall(regex_dados_pessoas, conteudo, re.DOTALL)

# Armazenar os dados das pessoas em um DataFrame no formato especificado
dados_formatados_pessoas = []
for pessoa in dados_pessoas:
    matricula = pessoa[0].strip()
    nome = pessoa[1].strip()
    orgao = pessoa[2].strip()
    tipo = pessoa[3].strip()
    dados_formatados_pessoas.append({"MATRÍCULA": matricula, "NOME": nome, "ORGÃO": orgao, "TIPO": tipo})

# Criar o DataFrame para as pessoas
df_pessoas = pd.DataFrame(dados_formatados_pessoas)

# Caminho do arquivo CSV para salvar os dados das pessoas
caminho_pessoas_csv = os.path.join(diretorio, "dados_pessoas.csv")

# Salvar o DataFrame das pessoas em um arquivo CSV com o formato desejado
df_pessoas.to_csv(caminho_pessoas_csv, index=False, encoding="utf-8", sep=";")
print(f"Arquivo '{caminho_pessoas_csv}' criado com sucesso.")

# --- Extração dos Dados dos Gestores (Gestor, Telefone, CEP, Cidade, UF) ---

# Expressão regular para capturar os dados do Gestor, Telefone, CEP, Cidade e UF
regex_gestor = r'Gestor(?:a)? da CAPE:\s*([\w\sÀ-ú]+?)(?:\s*-\s*)?(?:<\/p><p.*?>)?\s*Tel(?:\.|:)?\s*\(?(\d{2})\)?\s*(\d{4,5}-\d{4}).*?CEP:\s*(\d{5}-\d{3})\s*([\wÀ-ú\s]+)\s*/\s*([A-Z]{2})'

# Encontrar todas as ocorrências correspondentes para os gestores
dados_gestores = re.findall(regex_gestor, conteudo)

# Armazenar os dados dos gestores em um DataFrame no formato especificado
dados_formatados_gestores = []
for gestor in dados_gestores:
    nome = gestor[0].strip()
    telefone = f"({gestor[1]}) {gestor[2].strip()}"
    cep = gestor[3].strip()
    cidade = gestor[4].strip()
    uf = gestor[5].strip()
    dados_formatados_gestores.append({"Gestor": nome, "Telefone": telefone, "CEP": cep, "Cidade": cidade, "UF": uf})

# Criar o DataFrame para os gestores
df_gestores = pd.DataFrame(dados_formatados_gestores)

# Caminho do arquivo CSV para salvar os dados dos gestores
caminho_gestores_csv = os.path.join(diretorio, "dados_gestores.csv")

# Salvar o DataFrame dos gestores em um arquivo CSV com o formato desejado
df_gestores.to_csv(caminho_gestores_csv, index=False, encoding="utf-8", sep=";")
print(f"Arquivo '{caminho_gestores_csv}' criado com sucesso.")
