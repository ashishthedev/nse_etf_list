import requests
import pandas as pd
from io import StringIO

# ETF_DOWNLOAD_LINK = "https://www.nseindia.com/api/etf?csv=true&selectValFormat=crores"
# ETF_DOWNLOAD_LINK_PAGE = "https://www.nseindia.com/market-data/exchange-traded-funds-etf""

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
    print("_" * 100)
    print("Removed symbols with volume less than 10000")
    print("_" * 100)
    # Sort the data by Symbol
    data = data.sort_values(by="SYMBOL")
    # Convert symbol to uppercase and remove any leading or trailing spaces and prepend "NSE:" to the symbol
    data["SYMBOL"] = "NSE:" + data["SYMBOL"].str.upper().str.strip()
    # print(data[['SYMBOL', 'UNDERLYING ASSET']])
    # for i in range(len(data)):
    # print(data.iloc[i]['SYMBOL'], data.iloc[i]['UNDERLYING ASSET'], sep='\t')
    # Print symbol and underlying asset so that
    # it can be copied to the excel sheet
    # Save it in a csv file
    DEST_DIR = "outputs"
    # Ensure the directory exists
    import os

    os.makedirs(DEST_DIR, exist_ok=True)
    with open("outputs/new_etf.csv", "w") as f:
        for index, row in data.iterrows():
            f.write(row["SYMBOL"] + "," + row["UNDERLYING ASSET"] + "\n")
    for index, row in data.iterrows():
        print(row["SYMBOL"], row["UNDERLYING ASSET"], sep="|")
    print("_" * 100)
    print(
        f"Count of symbols were 154 as on 7Aug24. Today it is: {len(data)}. To refresh, download the latest file from NSE(https://www.nseindia.com/market-data/exchange-traded-funds-etf) and run the script again. Paste the output in some excel sheet Split the data in excel sheet using delimiter as `|`"
    )
    print("_" * 100)


if __name__ == "__main__":
    main()
