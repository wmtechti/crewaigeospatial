import numpy as np
import pandas as pd
import geopandas as gpd
from crewai import Agent, Task, Crew
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import xarray as xr

class GeospatialMachineLearningCrew:
    def __init__(self, climate_data: xr.Dataset, land_use_data: gpd.GeoDataFrame):
        self.climate_data = climate_data
        self.land_use_data = land_use_data
    
    def prepare_ml_dataset(self):
        """
        Preparação avançada de dataset para machine learning geoespacial
        """
        # Conversão de dados climáticos para DataFrame
        df_climate = self.climate_data.to_dataframe().reset_index()
        
        # Integração com dados de uso do solo
        merged_data = gpd.sjoin(
            self.land_use_data, 
            gpd.GeoDataFrame(df_climate, geometry=gpd.points_from_xy(df_climate.longitude, df_climate.latitude))
        )
        
        return merged_data
    
    def create_predictive_modeling_crew(self):
        # Agente de Preparação de Dados
        data_prep_agent = Agent(
            role='Especialista em Preparação de Dados Geoespaciais',
            goal='Processar e transformar dados para modelagem preditiva',
            backstory='Cientista de dados com expertise em machine learning geoespacial'
        )
        
        # Agente de Modelagem Preditiva
        predictive_agent = Agent(
            role='Modelador Preditivo Geoespacial',
            goal='Desenvolver modelos de machine learning para previsão',
            backstory='Especialista em modelos preditivos para análise territorial'
        )
        
        # Tarefa de Preparação de Dados
        data_prep_task = Task(
            description='Preparar e limpar dataset para modelagem preditiva',
            agent=data_prep_agent,
            expected_output='Dataset processado e estruturado para machine learning'
        )
        
        # Tarefa de Modelagem Preditiva
        modeling_task = Task(
            description='Desenvolver modelo preditivo com RandomForest',
            agent=predictive_agent,
            expected_output='Modelo treinado com métricas de performance'
        )
        
        return Crew(
            agents=[data_prep_agent, predictive_agent],
            tasks=[data_prep_task, modeling_task]
        )
    
    def train_predictive_model(self, target_variable='temperature'):
        """
        Treina modelo preditivo usando RandomForest
        """
        # Preparação do dataset
        dataset = self.prepare_ml_dataset()
        
        # Seleção de features
        features = [
            'latitude', 'longitude', 'elevation', 
            'land_use_type', 'vegetation_density'
        ]
        
        # Preparação dos dados para machine learning
        X = dataset[features]
        y = dataset[target_variable]
        
        # Split de treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Treinamento do modelo
        rf_model = RandomForestRegressor(n_estimators=100)
        rf_model.fit(X_train, y_train)
        
        # Avaliação do modelo
        y_pred = rf_model.predict(X_test)
        
        metrics = {
            'mse': mean_squared_error(y_test, y_pred),
            'r2_score': r2_score(y_test, y_pred),
            'feature_importances': dict(zip(features, rf_model.feature_importances_))
        }
        
        return {
            'model': rf_model,
            'metrics': metrics
        }
    
    def generate_spatial_predictions(self, model, new_data):
        """
        Gera predições espaciais usando modelo treinado
        """
        predictions = model.predict(new_data)
        return predictions

# Função de demonstração
def run_geospatial_ml_workflow():
    # Simulação de dados (substituir por dados reais)
    climate_data = xr.Dataset({
        'temperature': (['latitude', 'longitude'], np.random.rand(100, 100)),
        'precipitation': (['latitude', 'longitude'], np.random.rand(100, 100))
    }, coords={
        'latitude': np.linspace(-90, 90, 100),
        'longitude': np.linspace(-180, 180, 100)
    })
    
    land_use_data = gpd.GeoDataFrame({
        'land_use_type': np.random.choice(['urban', 'agricultural', 'forest'], 100),
        'vegetation_density': np.random.rand(100)
    }, geometry=[Point(x, y) for x, y in zip(np.random.rand(100)*360-180, np.random.rand(100)*180-90)])
    
    # Inicialização do crew
    geo_ml_crew = GeospatialMachineLearningCrew(climate_data, land_use_data)
    
    # Criação e execução do crew
    ml_crew = geo_ml_crew.create_predictive_modeling_crew()
    
    # Treinamento do modelo
    ml_results = geo_ml_crew.train_predictive_model()
    
    return ml_results
