# Analysis Report


## Workflow
This project automates the retrieval, processing, and visualization of genetic data for the TP53 human gene. The analysis pipeline consists of the following steps:

1. Data Acquisition: A Python script queries the MyGene Info API to fetch genomic metadata, transcript information, and specific exon coordinates for the TP53 gene (symbol:TP53, species: human).

2. Data Processing: The response data is parsed and structured locally into data.json, calculating key metrics such as total gene span, individual exon lengths, and the proportion of the gene span dedicated to coding exons versus non-coding regions.

3. Visualization & Automation: Using a Snakemake workflow (Snakefile) and a processing script (final_analysis.py), Matplotlib generates clean statistical visualizations (figure1.png and figure2.png) which are then compiled into this summary report.


## Findings
Exon Length Distribution: The analysis of individual exons across the gene span reveals significant variance in length. Most exons cluster within specific size ranges, with a few exceptionally long or short exons contributing to the overall structural profile of the transcript (visualized in Figure 1).

Gene Span Coverage: Based on the transcript boundaries and aggregated exon coordinates, the proportion of the total genomic span actually covered by exons has been calculated. The updated Matplotlib pie chart in Figure 2 highlights that coding exons make up a distinct fraction of the total gene span compared to the intervening non-coding or intronic intervals.


## Interpritations
Functional Compactness: The distribution of exon lengths points to a tightly organized structural layout typical of crucial tumor suppressor genes like TP53, where specific functional domains correspond to conserved exon structures.

Coding Efficiency: The percentage split shown in the coverage chart demonstrates how genomic real estate is allocated between coding sequences and regulatory or intronic regions within the defined gene boundaries.

## Figure 1 - Distrabution of Exon Lengths

![Figure 1](figure1.png)

> This graph shows the lengths of all exons within the gene span.

## Figure 2 - Exon Coverage of Gene Span

![Figure 2](figure2.png)

> This graph shows how much of the gene span is deticated to genetic exon code.