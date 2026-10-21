# Bioinformatics Data Analysis and Visualization
This project is designed to analyze the human TP53 gene biological dataset using Python to explore, analyze, and visualize biological data.


## How-To-Run
*An active internet connection is required to connect the remote databases.*
1. Navigate to the directory containing final_analysis.py and Snakefile

2. Run the following command:
    > snakemake --cores 4


## Included Files
* final_analysis.py
* Snakefile
* analysis_report.md
* README.md


## Output Files
* data.json
* figure1.png
* figure2.png


## Reflection 

Which part of this final project did you find most interesting or rewarding? Which was the most challenging?
* Creating visuals from the data I extracted was definingly the most interesting part. There are a lot of variables that can be tweaked to get the look you want from the graphs. Playing around with this was a lot of fun and an invaluable skill. The most challenging part was figuring out what question to ask. I had an immense amount of data at my fingertips but struggled to figure what to pull from it.

How did integrating scripting, API use, data handling, and visualization impact your understanding of bioinformatics research?
* These projects have really opened my eyes to how bioinformatics research is done. I can see now how data can be interpreted from these online databases. It is also useful to note how creating reusable code allows us to answer questions about a wide range of different data sets, without having to rewrite scripts for each.

How would you extend or improve your analysis further with more time or resources?
* With more time, I would want to broaden the scope. Instead of just capturing one gene, I’d like to create a script that allows user input. The script would then search using that input and capture the data on that gene. This way, the script could be reused to answer the same question for any number of genes. 


## AI Use Disclosure

What AI tool did you use?
> Google Gemini

What did you use it for?
> I used it for several things on this project. First, it works well as a search assist. Anytime I would search for a question I had, it would always direct me to reliable resources. Second, I bounced ideas off of it regularly when I was trying to figure out what direction to take my project. Third, it's great at interpreting errors. When I would get an error and couldn't find the culprit, it was able to explain to me what I was doing wrong.

How did you verify or edit its output?
> Most of the outputs were either backed by links or they were code snippets that I could manipulate. Often the information it gave me was not sufficient on its own and I needed to do more research before being able to solve the issue.
