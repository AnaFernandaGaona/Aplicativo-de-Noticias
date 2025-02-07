import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime
import flet as ft

def obter_titulos():
    url = 'https://g1.globo.com/'
    response = requests.get(url)
   
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        titulos = []
       
        for tag in soup.find_all('a', class_='feed-post-link'):
            titulo = tag.get_text(strip=True)
            data_tag = tag.find_previous('time', class_='content-publication-data')
            if data_tag:
                data_noticia = data_tag.get('datetime', datetime.now())  # Captura o atributo datetime
            else:
                data_noticia = datetime.now()
               
            if titulo:  # evita título vazio
                titulos.append((titulo, data_noticia))
       
        return titulos
    else:
        print("Erro ao acessar o site")
        return []

def conectar_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # Preencha com a senha do seu MySQL, se necessário
        database='noticias'  # O nome do banco de dados
    )
    return conn

def salvar_titulos(titulos):
    conn = conectar_db()
    cursor = conn.cursor()
   
    for titulo, data_noticia in titulos:
        query = "INSERT INTO noticias (titulo, data_noticia) VALUES (%s, %s)"
        cursor.execute(query, (titulo, data_noticia))
   
    conn.commit()
    cursor.close()
    conn.close()

def obter_titulos_db():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT titulo, data_noticia FROM noticias ORDER BY data_noticia DESC")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def main(page: ft.Page):
    page.title = "Últimas Notícias"
    titulos = obter_titulos_db()
 
    lista_titulos = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True
    )
    for titulo, data_noticia in titulos:
        lista_titulos.controls.append(ft.Text(f"{titulo} - {data_noticia}", style="font-size: 20px; font-weight: bold; color: black;"))
   
    page.add(lista_titulos)

def rodar_scraping_e_salvar():
    titulos = obter_titulos()
    if titulos:
        salvar_titulos(titulos)
    else:
        print("Nenhuma notícia encontrada!")

rodar_scraping_e_salvar()
ft.app(target=main)
