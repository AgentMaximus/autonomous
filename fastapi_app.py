from fastapi import FastAPI
import pandas as pd
import requests
from io import BytesIO

app = FastAPI()

@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.get('/natural_gas_prices')
def get_natural_gas_prices():
    try:
        url = "https://www.eia.gov/state/seds/sep_use/total/csv/use_US.csv"
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = BytesIO(response.content)
        df = pd.read_csv(data)
        # If needed filter or manipulate the dataframe
        # Example for demonstration: Return only the State and Data_Status columns
        return df[['State', 'Data_Status']].to_dict(orient='records')
    except Exception as e:
        return {"error": f"Failed to fetch data: {str(e)}"}