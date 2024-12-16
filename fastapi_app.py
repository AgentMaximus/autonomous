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
    url = "https://www.eia.gov/dnav/ng/xls/NG_PRI_SUM_DCU_NUS_M.xls"
    response = requests.get(url)
    if response.status_code == 200:
        excel_data = BytesIO(response.content)
        df = pd.read_excel(excel_data)
        return df.to_dict(orient='records')
    else:
        return {"error": "Failed to fetch data"}