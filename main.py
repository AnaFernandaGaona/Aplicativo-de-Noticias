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
                data_noticia = data_tag.get('datetime', datetime.now())  
            else:
                data_noticia = datetime.now()
               
            if titulo:  
                titulos.append((titulo, data_noticia))
       
        return titulos
    else:
        print("Erro ao acessar o site")
        return []


def conectar_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  
        database='noticias' 
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



def main(tela: ft.Page):
    tela.title = "Últimas Notícias"
    tela.bgcolor = "#B0C4DE"  
    
  
    titulos = obter_titulos_db()

    # Criar lista de títulos
    lista_titulos = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True
    )
    
    
    for titulo, data_noticia in titulos:
        lista_titulos.controls.append(
            ft.Text(
                f"{titulo} - {data_noticia}",
                style="font-size: 18px; font-weight: bold; color: navy; padding-bottom: 8px;" 
            )
        )
    
   
    barraMenu = ft.AppBar(
        leading=ft.IconButton(ft.icons.MENU, icon_color="white", on_click=lambda e: tela.open(menu)),
        leading_width=40,
        title=ft.Text("Noticias", color="white"),
        bgcolor=ft.colors.ORANGE_300,
        actions=[ft.IconButton(ft.icons.SEARCH, icon_color="white", on_click=lambda e: print("Cliquei Buscar"))]
    )
    
   
    menu = ft.NavigationDrawer(
        on_change=lambda e: tela.go("/noticias"),
        controls=[
            ft.NavigationDrawerDestination(
                label="Newspaper",  # O único item no menu agora é "Newspaper"
                icon=ft.icons.NEWSPAPER
            )
        ]
    )
    
    pagina_noticias = ft.View(
        route="/noticias",
        appbar=barraMenu,
        drawer=menu,
        controls=[lista_titulos]
    )

    # Mostrar a página de notícias quando a aplicação for iniciada
    tela.go("/noticias")
    tela.views.append(pagina_noticias)
    tela.update()

# Função para rodar o scraping e salvar as notícias no banco
def rodar_scraping_e_salvar():
    titulos = obter_titulos()
    if titulos:
        salvar_titulos(titulos)
    else:
        print("Nenhuma notícia encontrada!")

# Rodar o scraping e salvar as notícias no banco
rodar_scraping_e_salvar()

# Iniciar a aplicação
ft.app(target=main)
