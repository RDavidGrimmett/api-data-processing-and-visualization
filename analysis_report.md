# Analysis Report


## Workflow
This project automates the retrieval, processing, and visualization of genetic data for the TP53 human gene. The analysis pipeline consists of the following steps:

1. The Python script queries the MyGene Info API to capture the ensembl ID. Using this ID, it fetches genomic data, transcript information, and specific exon coordinates for the TP53 gene from the Ensembl RESTful API.

2. The response data is parsed then written into data.json. Then, the total gene span, individual exon lengths, and the proportion of the gene span dedicated to exons versus non-coding regions was calculated.

3. From this data, two visuals are created. The first shows a seaborn histplot showing the lengths of exon regions and the count. The second visual shows how much (in base pairs) of the gene span is dedicated to exons. 

4. Using Snakemake, the final_analysis.py script is processed and two visuals are generated, then embedded in the analysis_report.md.


## Findings
* The analysis of the exons across the gene span reveals a range of lengths. Most of the exons are clustered within a specific size range (<500 bp), with a few very long exons contributing to the overall structure.

* Using the exon start and stop points, the proportion of the total genomic span covered by exons was calculated. The pie chart in Figure 2 highlights that coding exons make up 31.2% of the total gene span compared to the non-coding intervals. This is important as it reveals that about a third of the genetic material is dedicated to protein formation. 


## Interpritations
* Most of the exons fall on the smaller end of the scale, most commonly measuring under 200 base pairs. This is typical for biological systems, as cells rely on compact exon sizes to ensure accurate and efficient RNA splicing.

* The percentage split shown in figure 2 demonstrates how the genomic real estate is allocated between coding sequences and regulatory or intronic regions within the gene. If about a third of the gene span is dedicated to exons, it can be assumed that for every one exon there are two introns. 

## Figure 1 - Distrabution of Exon Lengths

![Figure 1](figure1.png)

> This graph shows the lengths of all exons within the gene span.

## Figure 2 - Exon Coverage of Gene Span

![Figure 2](figure2.png)

> This graph shows how much of the total gene span is deticated to genetic exon code.