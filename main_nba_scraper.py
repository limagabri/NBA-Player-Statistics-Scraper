import subprocess
import sys

def run_script(script_path):
    """Executa um script Python usando subprocess."""
    try:
        print(f"Executando o script: {script_path}")
        subprocess.run([sys.executable, script_path], check=True)
        print(f"Script {script_path} finalizado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script {script_path}: {e}")
    except FileNotFoundError:
        print(f"Erro: O arquivo {script_path} não foi encontrado.")

if __name__ == "__main__":
    print("Iniciando a coleta de dados da NBA 🏀")
    run_script("nba_scraper_players.py")
    run_script("nba_scraper_teams.py")
    print("Coleta de dados da NBA finalizada! 🚀")