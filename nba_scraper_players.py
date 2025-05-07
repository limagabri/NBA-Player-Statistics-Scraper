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
import configparser
import os

def get_element(driver, xpath):
    """ Localiza um elemento na página pelo XPath com espera explícita. """
    for _ in range(3):
        try:
            return WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        except StaleElementReferenceException:
            time.sleep(1)
    return None

def safe_click(driver, xpath):
    """ Garante que o elemento seja reencontrado antes de clicar. """
    for _ in range(3):
        try:
            element = get_element(driver, xpath)
            if element:
                element.click()
                return True
        except StaleElementReferenceException:
            time.sleep(1)
    return False

def get_html_content(driver, xpath):
    """ Obtém o conteúdo HTML de um elemento na página pelo XPath. """
    element = get_element(driver, xpath)
    return element.get_attribute('outerHTML') if element else None

def parse_html_table(html_content):
    """ Analisa a tabela HTML e converte em DataFrame do Pandas. """
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find(name='table')
        html_string = str(table)
        html_io = StringIO(html_string)
        return pd.read_html(html_io)[0]
    return None

def scrape_nba_players_stats(config):
    """ Realiza o scraping dos dados de estatísticas dos jogadores da NBA com base na configuração. """
    option = Options()
    option.headless = True
    driver = webdriver.Firefox(options=option)
    driver.maximize_window()
    driver.get(config['url'])

    season_dropdown_xpath = '//*[@id="__next"]/div[2]/div[2]/div[3]/section[1]/div/div/div[1]/label/div/select'
    season_type_xpath = '//*[@id="__next"]/div[2]/div[2]/div[3]/section[1]/div/div/div[2]/label/div/select'
    per_mode_xpath = '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[3]/div/label/div/select'
    table_xpath = '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table'
    loading_overlay_xpath = '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/div[@class="LoadingOverlay_loader__iZ0Nm"]'

    season_dropdown = get_element(driver, season_dropdown_xpath)
    season_options = season_dropdown.find_elements(By.TAG_NAME, "option")

    season_types_to_scrape = [st.strip() for st in config['season_types'].split(',')]
    configured_stats = [stat.strip() for stat in config['statistics'].split(',')]
    stats_to_scrape = ['Player', 'Team'] + configured_stats

    output_directory = 'json'
    players_output_directory = os.path.join(output_directory, 'json_players')
    if not os.path.exists(players_output_directory):
        os.makedirs(players_output_directory)
        print(f"Pasta '{players_output_directory}' criada.")

    for option in season_options:
        season_text = option.text.strip()
        season_value = option.get_attribute("value")

        if season_text in [s.strip() for s in config['seasons'].split(',')]:
            print(f"Coletando dados de jogadores para a temporada: {season_text}...")

            safe_click(driver, season_dropdown_xpath)
            safe_click(driver, f'{season_dropdown_xpath}/option[@value="{season_value}"]')

            season_type_dropdown = get_element(driver, season_type_xpath)
            season_type_options = season_type_dropdown.find_elements(By.TAG_NAME, "option")

            for type_option in season_type_options:
                season_type_text = type_option.text.strip()

                if season_type_text in season_types_to_scrape:
                    print(f"  Coletando dados de jogadores para o tipo de temporada: {season_type_text}")
                    safe_click(driver, season_type_xpath)
                    safe_click(driver, f'{season_type_xpath}/option[text()="{season_type_text}"]')

                    time.sleep(2)

                    if safe_click(driver, per_mode_xpath):
                        safe_click(driver, f'{per_mode_xpath}/option[1]')

                    html_content = get_html_content(driver, table_xpath)
                    df_full = parse_html_table(html_content)

                    if df_full is not None:
                        existing_columns = [col for col in stats_to_scrape if col in df_full.columns]
                        df = df_full[existing_columns]
                        stats_players = {'Players': df.to_dict('records')}

                        filename = os.path.join(players_output_directory, f"Stats_Players_NBA_{season_text.replace('-', '_')}_{season_type_text.replace(' ', '_')}.json")
                        with open(filename, 'w') as fp:
                            json.dump(stats_players, fp, indent=4)

                        print(f"    Dados de jogadores salvos em {filename} ✅")

    driver.quit()

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config_players.ini')
    settings = config['settings']

    scrape_nba_players_stats(settings)

    print("Finalizado coleta de jogadores 🏀")