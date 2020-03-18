inFile = open("pathogenic.tsv", "r")
outFile = open("cnvs_separated_pheno.tsv", "w")
toChange = "Developmental delay AND/OR other significant developmental or morphological phenotypes"
newPheno = "Developmental delay"
for line in inFile:
    columns = line.split('\t')
    #spliting phenotype_patient into a list named allPheno 
    allPheno = columns[2].split("|")
    for phenotype in allPheno:
        if phenotype.strip() == toChange:
            phenotype = newPheno
        newLine = columns[0] +"\t"+ columns[1] +"\t"+ phenotype.strip()
        outFile.write(newLine + "\n")
        
inFile.close()
outFile.close()

