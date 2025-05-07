# 🏀 NBA Statistics Scraper

Um script Python para coletar dados de estatísticas da NBA 🌐 do site oficial, com opções de configuração separadas para jogadores e times. Os arquivos JSON serão salvos em pastas dedicadas. Utiliza Selenium ⚙️ para automação web e BeautifulSoup 🥣 para análise de HTML. Um script principal (`main_nba_scraper`) facilita a execução de todos os scripts de coleta.

A Python script to scrape NBA statistics data from the official NBA website 🌐, with separate configuration options for players and teams. The JSON files will be saved in dedicated folders. It uses Selenium ⚙️ for web automation and BeautifulSoup 🥣 for HTML parsing. A main script (`main_nba_scraper`) facilitates the execution of all scraping scripts.

## ⚙️ Configuração / Configuration

Antes de executar os scripts, você precisará configurar suas preferências nos arquivos `config_players.ini` e `config_teams.ini`:

Before running the scripts, you need to configure your preferences in the `config_players.ini` and `config_teams.ini` files:

1.  **Crie os arquivos `config_players.ini` e `config_teams.ini`** no mesmo diretório dos scripts `nba_scraper_players.py`, `nba_scraper_teams.py` e `main_nba_scraper`.
    / **Create the `config_players.ini` and `config_teams.ini` files** in the same directory as the `nba_scraper_players.py`, `nba_scraper_teams.py`, and `main_nba_scraper` scripts.

2.  **Edite o arquivo `config_players.ini`** com as opções para a coleta de dados dos jogadores (veja a seção anterior para detalhes).
    / **Edit the `config_players.ini` file** with the options for scraping player data (see the previous section for details).

3.  **Edite o arquivo `config_teams.ini`** com as opções para a coleta de dados dos times (veja a seção anterior para detalhes).
    / **Edit the `config_teams.ini` file** with the options for scraping team data (see the previous section for details).

## 🚀 Como Usar / How to Use

1.  **🛠️ Pré-requisitos / Prerequisites:**
    * Python 3.x instalado / Python 3.x installed.
    * Dependências instaladas do arquivo `requirements.txt` com `pip install -r requirements.txt`. / Dependencies installed from the `requirements.txt` file using `pip install -r requirements.txt`.
    * Navegador Firefox instalado / Firefox browser installed.

2.  **⚙️ Configuração do Ambiente / Environment Setup:**
    * Certifique-se de ter o navegador Firefox instalado no seu sistema. / Ensure that the Firefox browser is installed on your system.
    * Configure suas preferências nos arquivos `config_players.ini` e `config_teams.ini`. / Configure your preferences in the `config_players.ini` and `config_teams.ini` files.

3.  **▶️ Execução dos Scripts (Usando o Script Principal) / Running the Scripts (Using the Main Script):**
    * Execute o script principal `main_nba_scraper` para iniciar a coleta de dados de jogadores e times. / Run the main script `main_nba_scraper` to start scraping data for both players and teams.

    ```bash
    python main_nba_scraper
    ```

4.  **📊 Resultados / Results:**
    * Os arquivos JSON dos jogadores serão salvos na pasta `json/json_players`. / Player JSON files will be saved in the `json/json_players` folder.
    * Os arquivos JSON dos times serão salvos na pasta `json/json_teams`. / Team JSON files will be saved in the `json/json_teams` folder.
    * Veja a seção anterior para os detalhes dos nomes dos arquivos e seus conteúdos. / See the previous section for details on file names and their contents.

## 📝 Nota / Note

Estes scripts foram desenvolvidos para fins educacionais como uma demonstração de web scraping. Utilize-os de forma responsável e em conformidade com os termos de serviço do site da NBA.

These scripts were developed for educational purposes as a web scraping demonstration. Use them responsibly and in accordance with the NBA website's terms of service.

## 🤝 Contribuição / Contribution

Contribuições são sempre bem-vindas! Se você tiver alguma sugestão de melhoria, correção de bugs ou novas funcionalidades, sinta-se à vontade para abrir uma **Pull Request**.

Contributions are always welcome! If you have any suggestions for improvements, bug fixes, or new features, feel free to open a **Pull Request**.