
inFile = open("cnvs_separated_pheno.tsv", "r")
outFile = open("cnvs_separated_all.tsv", "w")
for line in inFile: 
    columns = line.split('\t')
    #spliting genes into a list named allGenes 
    allGenes = columns[1].split("/")
    for gene in allGenes:
        newLine = columns[0] +"\t"+ gene +"\t"+ columns[2] 
        outFile.write(newLine)
inFile.close()
outFile.close()
