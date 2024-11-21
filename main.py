# main.py (exemplo de execução)
import os
from dotenv import load_dotenv
from geospatial_ml_crew import run_geospatial_ml_workflow
import logging

# Configuração de log
logging.basicConfig(
    filename='logs/geospatial_analysis.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s'
)

def main():
    try:
        # Carrega variáveis de ambiente
        load_dotenv()
        
        # Executa workflow
        results = run_geospatial_ml_workflow()
        
        # Log de resultados
        logging.info(f"Modelo treinado. Métricas: {results['metrics']}")
        
    except Exception as e:
        logging.error(f"Erro na execução: {e}")

if __name__ == "__main__":
    main()
