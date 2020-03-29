import networkx
import obonet
import matplotlib.pyplot as plt

#url = 'https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo'
#graph = obonet.read_obo(url)

# HPO database is saved in file hpo.txt, this was used to work without internet
database = open('hpo.txt', 'r')
graph = obonet.read_obo(database)
ourData = open("cnvs_with_hpo.tsv", "r")
id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data = True)}

def findGene(geneName):
    for line in ourData:
        columns = line.split('\t')
        gene = columns[1]
        if geneName == gene:
            terms = columns[3].strip().split(";")
            return terms

class MiniGraph:

    def __init__(self, geneName='empty'):
        if geneName == 'empty':
            self.geneName = ""
            return
        else:  
            self.geneName = geneName
            self.nodes = findGene(geneName)
            self.names = {term: id_to_name[term] for term in self.nodes}
            # in self.miniGraph is wanted subgraph
            self.miniGraph = graph.subgraph(self.nodes)
            self.impactScore = {node: float(0.0)  for node in self.nodes}

    #newScore is dictionary (node : score)
    def changeScore(self, newScore):
        self.impactScore = newScore

    def showGraph(self):
        plt.subplot(121)
        networkx.draw(self.miniGraph, labels = self.names)
        plt.show()

    def add(self, graph1, graph2):
        self.impactScore = graph1.impactScore.copy()
        for term, score in graph2.impactScore.items():
            if term in self.impactScore:
                self.impactScore[term] += score
            else:
               self.impactScore[term] = score
        self.nodes = self.impactScore.keys()
        self.names = {term: id_to_name[term] for term in self.nodes}
        self.miniGraph = graph.subgraph(self.nodes)

print("Enter genes:")
genes = input().strip().split(" ")
if len(genes) == 1:
    m = MiniGraph(genes[0])
else:
    m1 = MiniGraph(genes[0])
    m2 = MiniGraph(genes[1])
    #m1.showGraph()
    #m2.showGraph()
    m = MiniGraph()
    m.add(m1, m2)
m.showGraph()
