rule all:
    input:
        "data.json",
        "figure1.png",
        "figure2.png"


rule run_analysis:
    input:
        script="final_analysis.py"
    output:
        data="data.json",
        exon_plot="figure1.png",
        comparison_plot="figure2.png"
    shell:
        "python {input.script}"
