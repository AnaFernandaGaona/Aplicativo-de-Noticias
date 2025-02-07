Scraping de Notícias e Exibição com Flet
Este projeto realiza scraping do site G1, coleta os títulos das notícias e suas datas, e exibe essas informações em uma interface gráfica usando Flet.

Tecnologias
Python 3.x
Requests (para fazer o scraping)
BeautifulSoup (para analisar o HTML)
MySQL (para armazenar as notícias)
Flet (para exibir as notícias na interface gráfica)
Como Usar
Instale as dependências: Execute o seguinte comando para instalar as bibliotecas necessárias:

bash
Copiar
pip install requests beautifulsoup4 mysql-connector-python flet
Configuração do Banco de Dados: No MySQL, crie o banco de dados e a tabela:

sql
Copiar
CREATE DATABASE noticias;
USE noticias;

CREATE TABLE noticias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    data_noticia DATE NOT NULL
);
Edite as configurações de conexão: No código Python, verifique se as configurações de conexão com o MySQL estão corretas:

python
Copiar
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',  # Coloque sua senha do MySQL, se necessário
    database='noticias'
)
Execute o projeto: Rode o script Python:

bash
Copiar
python seu_arquivo.py
Isso fará o scraping das notícias, salvará no banco de dados e exibirá a interface gráfica com os títulos das notícias.

Estrutura do Código
obter_titulos(): Faz o scraping do site G1 e coleta os títulos e datas.
salvar_titulos(): Salva as notícias no banco de dados.
obter_titulos_db(): Obtém as notícias do banco de dados.
main(page): Cria a interface gráfica com Flet.
rodar_scraping_e_salvar(): Faz o scraping e salva as notícias no banco de dados.
