from fastapi import FastAPI
import pandas as pd

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "https://stonk-list-api.p.rapidapi.com",
    "http://localhost:3000"
]

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

us_tickers = pd.read_csv(
                "https://raw.githubusercontent.com/dli-invest/eod_tickers/main/data/us_stock_data.csv", index_col=False
            )

cad_tickers = pd.read_csv(
            "https://raw.githubusercontent.com/FriendlyUser/cad_tickers_list/main/static/latest/stocks.csv", index_col=False
        )
@app.get("/tickers")
async def get_spreadsheet(exchange: str = "US"):
    """
    """
    if exchange == "US":
    # return spreadsheets from github here
        return us_tickers.to_csv()
    else: 
        return cad_tickers.to_csv()

