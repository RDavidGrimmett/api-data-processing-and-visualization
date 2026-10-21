
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

    # Get the gene data from Ensembl using the Ensembl ID
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

    data = lookup_response.json()

    return data


# Write data to data.json
def create_file(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=2)
    

# Captures exon lengths
def get_exon_lengths(data):
    exon_lengths = []

    # Loops through each transcript and exon to calculate exon lengths
    for transcript in data.get("Transcript", []):
        for exon in transcript.get("Exon", []):

            # Captures start and end positions of each exon
            start = exon.get("start")
            end = exon.get("end")

            # Calculates the length of each exon and appends it to the list
            exon_lengths.append(end - start + 1)

    return exon_lengths


# Captures the gene length
def get_gene_length(data):
    gene_length = data["end"] - data["start"] + 1
    
    return gene_length


# Captures merged exon intervals across all transcripts
def get_merged_exon_intervals(data):
    exon_intervals = []

    # Loops through each transcript and exon to capture start and end positions
    for transcript in data.get("Transcript", []):
        for exon in transcript.get("Exon", []):

            # Captures start and end positions of each exon and appends them to the exon_intervals list
            start = exon.get("start")
            end = exon.get("end")
            exon_intervals.append((start, end))

    # Sorts the exon intervals and merges overlapping intervals
    exon_intervals.sort()
    merged_intervals = []

    # Loops through the sorted exon intervals to merge overlapping intervals
    for start, end in exon_intervals:

        # If the merged_intervals list is not empty and the current interval overlaps with the last merged interval, merge them
        if merged_intervals and start <= merged_intervals[-1][1] + 1:
            previous_start, previous_end = merged_intervals[-1]
            merged_intervals[-1] = (previous_start, max(previous_end, end))

        else:
            # If there is no overlap, adds the current interval to the merged intervals
            merged_intervals.append((start, end))

    return merged_intervals


# Captures the total exon length
def get_total_exon_length(merged_intervals):
    total_exon_length = sum(end - start + 1 for start, end in merged_intervals)
    return total_exon_length


# Plots the distribution of exon lengths
def plot_exon_distribution(exon_lengths):

    # Creates a histogram of exon lengths using seaborn
    plt.figure(figsize=(8, 6))
    sns.set_theme(style="whitegrid")

    sns.histplot(exon_lengths, bins=30, color='blue')
    plt.title("Distribution of Exon Lengths")
    plt.xlabel("Length (bp)")
    plt.ylabel("Count")
    
    # Adjusts layout and saves the figure
    plt.tight_layout()
    plt.savefig("figure1.png")
    plt.show()


# Plots exon regions in genomic order across the gene span
def plot_exon_gene_comparison(data, gene_length, merged_intervals, total_exon_length):
    gene_start = data["start"]

    exon_regions = [
        (start - gene_start, end - start + 1)
        for start, end in merged_intervals
    ]

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.broken_barh(
        [(0, gene_length)],
        (0.35, 0.3),
        facecolors="#E5E7EB",
        label="Non-exon gene span",
    )
    ax.broken_barh(
        exon_regions,
        (0.35, 0.3),
        facecolors="#4C78A8",
        label="Exon regions",
    )
    ax.set_xlim(0, gene_length)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("Position within gene (bp)")
    ax.set_title(
        f"Exon Regions In Gene Span "
        f"({total_exon_length / gene_length:.1%} covered)"
    )
    ax.grid(axis="x", color="#D1D5DB", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="upper center", ncol=2)

    # Adjusts layout and saves the figure
    fig.tight_layout()
    fig.savefig("figure2.png", dpi=300)
    plt.show()


# Runs functions in sequential order
if __name__ == "__main__":

    ensembl_id = get_ensembl_id()
    data = get_database(ensembl_id)
    create_file(data)
    exon_lengths = get_exon_lengths(data)
    plot_exon_distribution(exon_lengths)
    merged_intervals = get_merged_exon_intervals(data)
    total_exon_length = get_total_exon_length(merged_intervals)
    plot_exon_gene_comparison(data, get_gene_length(data), merged_intervals, total_exon_length)