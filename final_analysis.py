#this is final_analysis.py

# Imported libraries
import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns


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
            start = exon.get("start")
            end = exon.get("end")
            if start is not None and end is not None:
                exon_lengths.append(end - start + 1)
    return exon_lengths


def get_gene_length(data):
    return data["end"] - data["start"] + 1


def get_exon_coverage_length(data):
    gene_start = data["start"]
    gene_end = data["end"]
    if gene_start > gene_end:
        raise ValueError("Gene start must not be greater than gene end.")

    exon_intervals = []
    for transcript in data.get("Transcript", []):
        for exon in transcript.get("Exon", []):
            start = exon.get("start")
            end = exon.get("end")
            if start is None or end is None:
                continue

            start = max(start, gene_start)
            end = min(end, gene_end)
            if start <= end:
                exon_intervals.append((start, end))

    exon_intervals.sort()
    merged_intervals = []
    for start, end in exon_intervals:
        if merged_intervals and start <= merged_intervals[-1][1] + 1:
            previous_start, previous_end = merged_intervals[-1]
            merged_intervals[-1] = (previous_start, max(previous_end, end))
        else:
            merged_intervals.append((start, end))

    return sum(end - start + 1 for start, end in merged_intervals)


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


# Plots unique exon coverage against the remaining gene span
def plot_exon_gene_comparison(data):
    gene_length = get_gene_length(data)
    exon_coverage = get_exon_coverage_length(data)
    other_length = gene_length - exon_coverage
    exon_percentage = exon_coverage / gene_length * 100

    plt.figure(figsize=(8, 5))
    sns.set_theme(style="whitegrid")

    plt.barh(
        ["Gene Architecture"],
        [exon_coverage],
        color="#53a9b4",
        label=f"Unique exon coverage ({exon_coverage:,} bp, {exon_percentage:.1f}%)",
    )
    plt.barh(
        ["Gene Architecture"],
        [other_length],
        left=[exon_coverage],
        color="#0051ff",
        label=f"Not covered by exons ({other_length:,} bp)",
    )
    plt.xlim(0, gene_length)
    plt.xlabel("Length in Base Pairs (bp)")
    plt.title(f"Exon Coverage of Gene Span ({gene_length:,} bp)")
    plt.legend(loc="upper right")

    plt.tight_layout()
    plt.savefig("figure2.png", dpi=300)
    plt.show()


# Runs functions in sequential order
if __name__ == "__main__":

    ensembl_id = get_ensembl_id()
    data = get_database(ensembl_id)
    create_file(data)

    plot_exon_distribution(data)
    plot_exon_gene_comparison(data)