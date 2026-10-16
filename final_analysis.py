#this is final_analysis.py

# Imported libraries
import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


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
    

# Reads data.json
def load_data():
    with open ("data.json") as f:
        data = json.load(f)
    return data


# Captures exon lengths
def get_exon_length(data):
    exon_lengths = []
    for transcript in data.get("Transcript", []):
        for exon in transcript.get("Exon", []):
            length = exon["end"] - exon["start"]
            exon_lengths.append(length)
    return exon_lengths


# Captures transcript lengths
def get_transcript_length(data):
    transcript_lengths = []
    for transcript in data.get("Transcript", []):
        length = transcript["end"] - transcript["start"]
        transcript_lengths.append(length)
    return transcript_lengths


# Captures intron lengths
def get_intron_length(data):
    intron_lengths = []
    for transcript in data.get("Transcript", []):
        exons = transcript.get("Exon", [])
        for i in range(len(exons) - 1):
            intron_length = exons[i + 1]["start"] - exons[i]["end"]
            intron_lengths.append(intron_length)
    return intron_lengths


# Plots the distribution of exon lengths
def plot_exon_distribution(data):
    exon_lengths = get_exon_length(data)
    
    plt.figure(figsize=(8, 6))
    sns.set_theme(style="whitegrid")
    
    sns.histplot(exon_lengths, bins=30, kde=True, color='blue')
    plt.title("Distribution of Exon Lengths")
    plt.xlabel("Length (bp)")
    plt.ylabel("Count")
    
    plt.tight_layout()
    plt.savefig("figure1.png")
    plt.show()


# Plots the comparison between exon and intron lengths
def plot_intron_exon_comparison(data):
    exon_lengths = get_exon_length(data)
    intron_lengths = get_intron_length(data)
    
    plt.figure(figsize=(8, 6))
    sns.set_theme(style="whitegrid")
    
    df_exons = pd.DataFrame({'Length': exon_lengths, 'Type': 'Exon'})
    df_introns = pd.DataFrame({'Length': intron_lengths, 'Type': 'Intron'})
    df_combined = pd.concat([df_exons, df_introns])
    
    sns.boxplot(x='Type', y='Length', data=df_combined, palette='Set2')
    plt.title("Comparison of Exon vs Intron Lengths")
    plt.yscale('log')
    plt.ylabel("Length (bp - Log Scale)")
    plt.xlabel("Feature Type")
    
    plt.tight_layout()
    plt.savefig("figure2.png")
    plt.show()


# Runs functions in sequential order
if __name__ == "__main__":

    ensembl_id = get_ensembl_id()
    data = get_database(ensembl_id)
    file =  create_file(data)
    exon_lengths = get_exon_length(data)
    transcript_lengths = get_transcript_length(data)
    intron_lengths = get_intron_length(data)

    plot_exon_distribution(data)
    plot_intron_exon_comparison(data)