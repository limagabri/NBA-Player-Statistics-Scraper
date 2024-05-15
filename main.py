import time
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from io import StringIO

def get_element(driver, xpath):
    # Função para localizar um elemento na página pelo xpath
    # Function to locate an element on the page by xpath
    try:
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        return element
    except StaleElementReferenceException:
        return None

def get_html_content(driver, xpath):
    # Função para obter o conteúdo HTML de um elemento na página pelo xpath
    # Function to get HTML content of an element on the page by xpath
    element = get_element(driver, xpath)
    return element.get_attribute('outerHTML') if element else None

def parse_html_table(html_content):
    # Função para analisar a tabela HTML e converter em DataFrame do Pandas
    # Function to parse the HTML table and convert it to a Pandas DataFrame
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find(name='table')
        html_string = str(table)
        html_io = StringIO(html_string)
        return pd.read_html(html_io)[0]
    return None

def scrape_nba_stats(url):
    # Função principal para realizar o scraping dos dados de estatísticas da NBA
    # Main function to scrape NBA statistics data
    option = Options()
    option.headless = True
    driver = webdriver.Firefox(options=option)
    driver.maximize_window()

    driver.get(url)

    dropdown1_xpath = '//*[@id="__next"]/div[2]/div[2]/div[3]/section[1]/div/div/div[2]/label/div/select'
    dropdown1_option_xpath = f'{dropdown1_xpath}/option[2]'
    dropdown2_xpath = '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[3]/div/label/div/select'
    dropdown2_option_xpath = f'{dropdown2_xpath}/option[1]'
    table_xpath = '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table'

    # Clique no dropdown 1 para selecionar a primeira opção
    # Click on dropdown 1 to select the first option
    dropdown1 = get_element(driver, dropdown1_xpath)
    if dropdown1:
        dropdown1.click()
        dropdown1_option = get_element(driver, dropdown1_option_xpath)
        if dropdown1_option:
            dropdown1_option.click()

    # Clique no dropdown 2 para selecionar a primeira opção
    # Click on dropdown 2 to select the first option
    dropdown2 = get_element(driver, dropdown2_xpath)
    if dropdown2:
        dropdown2.click()
        dropdown2_option = get_element(driver, dropdown2_option_xpath)
        if dropdown2_option:
            dropdown2_option.click()

    # Obter o conteúdo HTML da tabela de estatísticas
    # Get the HTML content of the statistics table
    html_content = get_html_content(driver, table_xpath)
    df_full = parse_html_table(html_content)

    # Verificar se a tabela foi carregada corretamente e formatá-la
    # Check if the table was loaded correctly and format it
    df = df_full[['Player', 'Team', 'PTS', 'AST', 'REB', 'BLK', 'STL', '3P%']] if df_full is not None else None
    if df is not None:
        df.columns = ['Player', 'Team', 'PTS','AST', 'REB', 'BLK', 'STL', '3P%']
        stats_players = {'Points': df.to_dict('records')}
    else:
        stats_players = {}

    driver.quit()

    return stats_players

if __name__ == "__main__":
    # URL da página de estatísticas da NBA
    # URL of the NBA statistics page
    url = "https://www.nba.com/stats/players/traditional"
    # Chamar a função principal para realizar o scraping e obter as estatísticas dos jogadores
    # Call the main function to perform scraping and obtain player statistics
    stats_players = scrape_nba_stats(url)

    # Salvar os dados em um arquivo JSON
    # Save the data to a JSON file
    with open('Stats_Players_NBA.json', 'w') as fp:
        json.dump(stats_players, fp, indent=4)

    # Imprimir os dados obtidos
    # Print the obtained data
    print('Finalizado')
