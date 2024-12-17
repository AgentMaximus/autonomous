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
        url = "https://www.eia.gov/dnav/ng/xls/NG_PRI_SUM_DCU_NUS_M.xls"
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        excel_data = BytesIO(response.content)
        df = pd.read_excel(excel_data, engine='openpyxl')  # Specify the engine explicitly
        return df.to_dict(orient='records')
    except Exception as e:
        return {"error": f"Failed to fetch data: {str(e)}"}