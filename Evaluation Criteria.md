# **Evaluation Criteria**

## **MODEL EXPERIMENTATION**

Criteria   | Sub Criteria   | Max Marks
:-------|:------------------------- | :-----:
**1.0** Setup pycaret and mlflow environment | Create mlflow server with proper db location	| 1
-- | Setting up mlflow tracking uri  | 1
--  | Create pycaret's setup function  | 2
**2.0** Building all the specified models in pycaret with all the features  |  training all the models using pycaret  | 1
**3.0** Screenshot of mlflow ui | screenshot of all the experiments	| 1
--  |  screenshot of one experiments with all the artifacts visible  | 1
**4.0** Building the best pycaret with only the specified features and no transformations | Create pycaret's setup function such that it only encodes our categorical variable and does not transform our variables | 1
**5.0** Screenshot of mlflow ui after dropping features | screenshot of all the experiments	 | 1
-- | screenshot of one experiments with all the artifacts visible | 1


## **DATA PIPELINE**
Create functions for data pipeline in utils.py ( 20 marks )

Function   | Marks 
:---------------:|:-------
def build_dbs() | 4
def load_data_into_db() | 4
def map_city_tier()	| 4
def map_categorical_vars() | 4
def interactions_mapping() | 4
