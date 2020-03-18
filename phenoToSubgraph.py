from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import networkx
import obonet

database = open('hpo.txt', 'r')
graph = obonet.read_obo(database)
inFile = open("cnvs_separated_all.tsv", "r")
outFile = open("cnvs_with_hpo.tsv", "w")

wasUsed = {"phenotype_patient": "HPO_terms", "not provided": "-"} 
name_to_id = {data.get('name'): id_ for id_, data in graph.nodes(data = True)}
all_names = [name for name in name_to_id]

def subgraph(phenotype): 
    termID = name_to_id[process.extractOne(phenotype, all_names)[0]]
    subg = networkx.descendants(graph, termID)
    subg.add(termID)
    return subg

for line in inFile:
    columns = line.split('\t')
    phenotype = columns[2].strip()
    if phenotype not in wasUsed:
        returnedTerms = subgraph(phenotype)
        newSubgraph = returnedTerms.pop()
        for term in returnedTerms:
            newSubgraph += ";" + term
        wasUsed[phenotype] = newSubgraph
    newLine = columns[0] +"\t"+ columns[1] +"\t"+ phenotype +"\t"+ wasUsed[phenotype]
    outFile.write(newLine + "\n")

database.close()
inFile.close()
outFile.close()

