
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
def get_exon_length(data):
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


# Captures the total exon length
def get_total_exon_length(data):
    exon_intervals = []

    # Loops through each transcript and exon to calculate unique exon coverage
    for transcript in data.get("Transcript", []):
        for exon in transcript.get("Exon", []):

            # Captures start and end positions of each exon
            start = exon.get("start")
            end = exon.get("end")

            exon_intervals.append((start, end))

    # Sorts the exon intervals by their start positions
    exon_intervals.sort()
    merged_intervals = []

    # Merges overlapping intervals
    for start, end in exon_intervals:

        # If the current interval overlaps with the previous one, merge them
        if merged_intervals and start <= merged_intervals[-1][1] + 1:
            previous_start, previous_end = merged_intervals[-1]
            merged_intervals[-1] = (previous_start, max(previous_end, end))

        # If the current interval does not overlap, add it to the list
        else:
            merged_intervals.append((start, end))

    total_exon_length = sum(end - start + 1 for start, end in merged_intervals)
    
    return total_exon_length


# Plots the distribution of exon lengths
def plot_exon_distribution(data):
    exon_lengths = get_exon_length(data)

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


# Plots exon coverage as a proportion of gene length
def plot_exon_gene_comparison(data):
    gene_length = get_gene_length(data)
    exon_coverage = get_total_exon_length(data)
    other_length = gene_length - exon_coverage

    # Creates a pie chart to visualize exon coverage vs. non-exon coverage
    plt.figure(figsize=(11, 9))
    plt.pie(
        [exon_coverage, other_length],
        labels=[
            f"Exon coverage ({exon_coverage:,} bp)",
            f"Not covered by exons ({other_length:,} bp)",
        ],
        # Sets the autopct parameter to display percentages
        autopct="%1.1f%%",
        colors=["#dbc754", "#fa4f4f"],
        startangle=90,
    )
    plt.title(f"Exon Coverage of Gene Span ({gene_length:,} bp)")

    # Adjusts layout and saves the figure
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