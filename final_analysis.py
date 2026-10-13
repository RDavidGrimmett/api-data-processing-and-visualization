#this is final_analysis.py

# Imported libraries
import requests
import json

# Find Ensembl ID from mygene.info
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

# Get database from Ensembl.org
def get_database(ensembl_id):
    headers = {
        "Content-type": "application/json"
    }

    # Get the gene annotation, including transcripts and their exon records.
    lookup_url = f"https://rest.ensembl.org/lookup/id/{ensembl_id}"
    lookup_response = requests.get(
        lookup_url,
        params={"expand": 1},
        headers=headers,
    )
    # if commection fail print error code
    if lookup_response.status_code != 200:
        print("Request failed:", lookup_response.status_code)
        print(lookup_response.text)
        return

    data = lookup_response.json()

    return data

# Write data to data.json
def create_file(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=2)

#  Reads data.json
def load_data():
    with open ("data.json") as f:
        data = json.load(f)

# Captures exon lengths
def get_exon_length():
    exon_lengths = []
    for transcript in data.get("Transctipt", []):
        for exon in transcript.get("Exon", []):
            length = exon["end"] - exon["start"]
            exon_lengths.append(length)


# Runs functions in sequential order
if __name__ == "__main__":

    ensembl_id = get_ensembl_id()
    data = get_database(ensembl_id)
    file =  create_file(data)