outFile = open("statistics.txt", "w")
yes = 0
no = -1
phenoFound = False
ourData = open("cnvs_genes_together2.tsv", "r")
for line in ourData:
    genes = []
    columns = line.split('\t')
    expl = columns[3].strip()
    genes = columns[1].strip().split('/')
    for oneGene in genes:
        if phenoFound:
            break
        ourData2 =open("genes_to_phenotype3.tsv", "r")
        for line2 in ourData2:
            columns2 = line.split('\t')
            geneName = columns[0].strip()
            if oneGene==geneName:
                subgraph = columns[3].strip().split('\t')
                if expl in subgraph:
                    phenoFound = True
                    break
        ourData2.close()
    if phenoFound:       
        yes+=1
        phenoFound = False
    else:
        no+=1
ourData.close()
outFile.write("yes: " +str(yes) + "\n")
outFile.write("no: " +str(no) + "\n")
outFile.write("sum: " +str(no+yes) + "\n")
outFile.close()
