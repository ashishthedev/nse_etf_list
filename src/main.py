import requests
import pandas as pd
from io import StringIO

# ETF_DOWNLOAD_LINK = "https://www.nseindia.com/api/etf?csv=true&selectValFormat=crores"

ETF_DOWNLOADED_FILE_PATH = "downloads/etf.csv"


def read_etf_data(file_path):
    data = pd.read_csv(file_path)
    print(data.head())
    return data


def remove_rows_with_volume_less_than_minimum(minimum, data):
    # remove newline from the column name
    data.columns = data.columns.str.replace(" \n", "")

    # Remove rows having "-" in volume column
    data = data[data["VOLUME"] != "-"]

    # Convert the string to float
    data["VOLUME"] = data["VOLUME"].str.replace(",", "").astype(float)
    data = data[data["VOLUME"] > minimum]
    return data


def main():
    data = read_etf_data(file_path=ETF_DOWNLOADED_FILE_PATH)
    data = remove_rows_with_volume_less_than_minimum(minimum=10000, data=data)
    # Sort the data by Symbol
    data = data.sort_values(by="SYMBOL")
    # Convert symbol to uppercase and remove any leading or trailing spaces and prepend "NSE:" to the symbol
    data["SYMBOL"] = "NSE:" + data["SYMBOL"].str.upper().str.strip()
    # print(data[['SYMBOL', 'UNDERLYING ASSET']])
    # for i in range(len(data)):
    # print(data.iloc[i]['SYMBOL'], data.iloc[i]['UNDERLYING ASSET'], sep='\t')
    # Print symbol and underlying asset so that
    # it can be copied to the excel sheet
    for index, row in data.iterrows():
        print(row["SYMBOL"], row["UNDERLYING ASSET"], sep="|")


if __name__ == "__main__":
    main()
