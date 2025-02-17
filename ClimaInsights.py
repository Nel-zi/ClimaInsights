import requests
import datetime
import logging 
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from datetime import datetime
import os
import requests
import psycopg2



load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.weatherstack.com/current"
locations =  ["New York", "Los Angeles", "Chicago", "Philadelphia", "California" ]

def extract_data(**kwargs):
    weather_data = []
    for location in locations:
        params = {
            "access_key" : API_KEY,
            "query" : location
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        weather_data.append({
            "location" : location,
            "temperature" : data["current"]["temperature"],
            "humidity" : data["current"]["humidity"],
            "pressure" : data["current"]["pressure"],
            "weather_descriptions" : data["current"]["weather_descriptions"]
        })

        weather_df = pd.DataFrame(weather_data)
        kwargs['ti'].xcom_push(key='extract_data', value=weather_df)
        return weather_data
    

def load_data(**kwargs ):
    ti = kwargs['ti']
    weather_df = ti.xcom_pull(task_id='extract_weather_data', key='extract_data')


    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")

    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    con = engine.connect()

    weather_df.head(0).to_sql('weather_data', con=con, if_exists='replace', index=False)
    weather_df.to_sql('weather_data', con=con, if_exists='append', index=False)
    con.close()




# # Define the API key, the city, and the base URL
# load_dotenv()
# API_KEY = os.getenv('API_KEY')
# BASE_URL = "http://api.weatherstack.com/current"
# locations = locations = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]


# def fetch_data(locations):
#     weather_data = []

#     for location in locations:
#         params = {
#             "key": API_KEY,
#             "q": location
#         }

#         try:
#             response = requests.get(BASE_URL, params=params)
#             response.raise_for_status()  # Raise an error for non-200 status codes

#             data = response.json()
#             weather_data.append(data)

#             logging.info(f"Fetched weather data successfully for {location}")
#         except requests.exceptions.RequestException as e:
#             logging.error(f"Failed to fetch data for {location}: {e}")
    
#     return weather_data





# def transform_data(data):
#     transformed_data = []

#     for weather_data in data:
#         try:
#             if "location" in weather_data and "current" in weather_data:
#                 location = weather_data["location"]["name"]
#                 country = weather_data["location"]["country"]
#                 temperature = weather_data["current"]["temperature"]
#                 wind_speed = weather_data["current"]["wind_speed"]
#                 pressure = weather_data["current"]["pressure"]
#                 humidity = weather_data["current"]["humidity"]
#                 observation_time = weather_data["current"]["observation_time"]

#                 # Convert observation_time to time
#                 observation_time = datetime.strptime(observation_time, "%I:%M %p").time()

#                 transformed_data.append([location, country, temperature, wind_speed, pressure, humidity, observation_time])
#             else:
#                 logging.warning(f"Skipping incomplete data for {weather_data.get('location', {}).get('name')}")
#         except KeyError as e:
#             logging.error(f"KeyError: {e} occurred while processing data for {weather_data.get('location', {}).get('name')}")
#         except Exception as e:
#             logging.error(f"An error occurred while processing data: {e}")

#     # Define columns for the DataFrame
#     columns = ["location", "country", "temperature", "wind_speed", "pressure", "humidity", "observation_time"]

#     # Create DataFrame
#     df = pd.DataFrame(transformed_data, columns=columns)

#     return df




# def load_data_to_db(df, first_time=False):
#     """
#     Load the provided DataFrame into a PostgreSQL database using SQLAlchemy.
    
#     Parameters:
#         df (DataFrame): The DataFrame containing the weather data.
#         first_time (bool): If True, replace the 'weather' table if it exists.
#                            If False, append the data to the existing table.
#     """
#     # Build the database connection URL from environment variables
#     # Adjust the environment variable names as needed
#     db_params = {
#         'username': os.getenv('DB_USER'),
#         'password': os.getenv('DB_PASSWORD'),
#         'host': os.getenv('DB_HOST'),
#         'port': int(os.getenv('DB_PORT', 5432)),  # Default port 5432 if not provided
#         'database': os.getenv('DB_NAME')
#     }
    
#     db_url = f"postgresql://{db_params['username']}:{db_params['password']}@" \
#              f"{db_params['host']}:{db_params['port']}/{db_params['database']}"

#     # Create the SQLAlchemy engine
#     engine = create_engine(db_url)

#     # If first_time is True, we replace the table (i.e., create a new one)
#     # Otherwise, we append the data to the existing table.
#     if_exists_option = 'replace' if first_time else 'append'

#     try:
#         # Load the DataFrame into the 'weather' table
#         df.to_sql('weather', con=engine, index=False, if_exists=if_exists_option)
#         print("Data successfully loaded into PostgreSQL database.")
#     except SQLAlchemyError as e:
#         print(f"Error occurred while loading data to database: {e}")
