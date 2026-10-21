# Analysis Report


## Workflow
This project automates the retrieval, processing, and visualization of genetic data for the TP53 human gene. The analysis pipeline consists of the following steps:

1. The Python script queries the MyGene Info API to capture the ensembl ID. Using this ID, it fetches genomic data, transcript information, and specific exon coordinates for the TP53 gene from the Ensembl RESTful API.

2. The response data is parsed then written into data.json. Then, the total gene span, individual exon lengths, exon locations, and the proportion of the gene span dedicated to exons versus non-coding regions was calculated.

3. From this data, two visuals are created. The figure 1 shows a seaborn histplot showing the lengths of exon regions and their count. The second visual shows two things. First, how much (in base pairs) of the gene is dedicated to exons, and second, where these exons are located on the gene span.

4. Using Snakemake, the final_analysis.py script is processed and two visuals are generated, then embedded in the analysis_report.md.


## Findings
* The analysis of the exons across the gene span reveals a range of lengths. Most of the exons are clustered within a specific size range (<500 bp), with a few very long exons contributing to the overall structure.

* Using the exon start and stop points, the proportion of the total genomic span covered by exons was calculated. Figure 2 highlights that coding exons make up 31.2% of the total gene span compared to the non-coding intervals. This is important as it reveals that about a third of the genetic material is dedicated to protein formation. 

* Using the starting points of the exons, the location of the exons in the gene span could be determined. These were also listed genomic region map in figure 2. 


## Interpritations
Most of the TP53 exons fall on the smaller end of the scale, most commonly measuring under 200 base pairs. This is typical for biological systems, as cells rely on compact exon sizes to ensure accurate and efficient RNA splicing. The percentage split shown in figure 2 demonstrates how the genomic real estate is split between coding sequences and noncoding regions within the gene. If about a third of the gene span is dedicated to exons, it can be assumed that for every one exon there are two introns. This can actually be visualized in the genomic region map where each exon region is buffered by noncoding regions. Exons surrounded like this is common in genes and actually helps to protect them from mutations and to help with transcription. 


## Figure 1 - Exon Length Distribution Across TP53 Transcript Variants

![Figure 1](figure1.png)

> This graph shows the lengths of all exons within the TP53 gene's database including transcript variants. The Y-axis indicated the number of exons, while the X-axis indicated the length of the exons. 

## Figure 2 - Exon Coverage and location on Gene Span

![Figure 2](figure2.png)

> This graph shows how much of the total gene span is dedicated to genetic exon code. The locations of the exons on the gene span are also shown here in blue.