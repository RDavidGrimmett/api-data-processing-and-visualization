#this is final_analysis.py

# Imported libraries
import requests
import json

# Get biological data from Ensembl.org
def get_ensembl_id():

    # Target url and search parameters
    url = "https://mygene.info/v3/query"
    
    params = {
        "q": "symbol:TP53",
        "species": "human",
        "fields": "symbol,ensembl"
    }

    # Captures data from database in response variable
    response = requests.get(url, params=params)

    # If connection successful, captures database as variable
    if response.status_code == 200:
        data = response.json()

        # Captures just the ensmbl_id as variable
        ensembl_id = data["hits"][0]["ensembl"]["gene"]

        # Returns the ensembl_id
        return ensembl_id

    # If connection is unsuccessful, print error
    else:
        print("Request failed:", response.status_code)
        print(response.text)

# Runs functions in sequential order
if __name__ == "__main__":

    ensembl_id = get_ensembl_id()

print(ensembl_id)