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

    if lookup_response.status_code != 200:
        print("Request failed:", lookup_response.status_code)
        print(lookup_response.text)
        return

    data = lookup_response.json()

    # Get the genomic DNA sequence for the gene.
    sequence_url = f"https://rest.ensembl.org/sequence/id/{ensembl_id}"
    sequence_response = requests.get(
        sequence_url,
        params={"type": "genomic"},
        headers=headers,
    )

    if sequence_response.status_code != 200:
        print("Request failed:", sequence_response.status_code)
        print(sequence_response.text)
        return

    data["sequence"] = sequence_response.json()["seq"]

    with open("data.json", "w") as file:
        json.dump(data, file, indent=2)

    return data


def get_gc_content(gene_name, sequence):
    if not sequence:
        raise ValueError(f"Cannot calculate GC-content for empty sequence: {gene_name}")

    sequence = sequence.upper()
    gc_count = sequence.count("G") + sequence.count("C")
    return (gc_count / len(sequence)) * 100


def get_sequence_length(sequence):
    return len(sequence)


def get_exon_intron_counts(gene_data):
    transcript_counts = []

    for transcript in gene_data.get("Transcript", []):
        exons = transcript.get("Exon", [])
        strand = transcript.get("strand", 1)

        if all("rank" in exon for exon in exons):
            transcript_exons = sorted(exons, key=lambda exon: exon["rank"])
        else:
            transcript_exons = sorted(
                exons,
                key=lambda exon: exon["start"],
                reverse=(strand == -1),
            )

        genomic_exons = sorted(exons, key=lambda exon: exon["start"])
        introns = []
        for left_exon, right_exon in zip(genomic_exons, genomic_exons[1:]):
            intron_start = left_exon["end"] + 1
            intron_end = right_exon["start"] - 1
            if intron_start <= intron_end:
                introns.append({"start": intron_start, "end": intron_end})

        transcript_counts.append({
            "transcript_id": transcript["id"],
            "exon_count": len(transcript_exons),
            "exons": [
                {
                    "id": exon["id"],
                    "start": exon["start"],
                    "end": exon["end"],
                    "rank": exon.get("rank"),
                }
                for exon in transcript_exons
            ],
            "intron_count": len(introns),
            "introns": introns,
        })

    return transcript_counts


# Runs functions in sequential order
if __name__ == "__main__":

    ensembl_id = get_ensembl_id()
    if ensembl_id is not None:
        gene_data = get_database(ensembl_id)
        if gene_data is not None:
            sequence = gene_data["sequence"]
            gc_content = get_gc_content(ensembl_id, sequence)
            sequence_length = get_sequence_length(sequence)
            print(f"GC-content for {ensembl_id}: {gc_content:.2f}%")
            print(f"Sequence length for {ensembl_id}: {sequence_length} bp")
            for counts in get_exon_intron_counts(gene_data):
                print(
                    f"{counts['transcript_id']}: "
                    f"{counts['exon_count']} exons, "
                    f"{counts['intron_count']} introns"
                )