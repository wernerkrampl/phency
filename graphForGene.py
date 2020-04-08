import networkx
import obonet
from networkx.drawing.nx_agraph import to_agraph
import graphviz as gv

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
            self.gvGraph = to_agraph(self.miniGraph)
            self.gvGraph.node_attr['style']='filled'
            self.impactScore = {node: float(0.0)  for node in self.nodes}
            self.setLabels()
            self.gvGraph.node_attr['color']='#d0f0c0'
            self.gvGraph.layout('dot')

    def setLabels(self):
        self.labels = {}
        for term, name in self.names.items():
            text = '['+ name +'; '+ str(self.impactScore[term]) +']'
            self.gvGraph.get_node(term).attr['label'] = text

    #newScore is dictionary (node : score)
    def changeScore(self, newScore):
        self.impactScore = newScore
        self.setLabels()

    def add(self, graph1, graph2):
        #we use "copy" of graph1 as template for adding graph2 to it
        self.impactScore = graph1.impactScore.copy()
        graph2copy = graph2.impactScore.copy()
        colors={node: '#d0f0c0'  for node in graph1.nodes}
        for term, score in self.impactScore.items():
            if term in graph2copy:
                self.impactScore[term] += graph2copy[term]
                graph2copy.pop(term)
                colors[term] = '#fceea7'
        for term, score in graph2copy.items():
            self.impactScore[term] = score
            colors[term] = '#ffb6c1'
        self.nodes = self.impactScore.keys()
        self.names = {term: id_to_name[term] for term in self.nodes}
        self.miniGraph = graph.subgraph(self.nodes)
        self.gvGraph = to_agraph(self.miniGraph)
        self.setLabels()
        self.gvGraph.node_attr['style']='filled'
        self.gvGraph.layout('dot')
        for term in colors:
            self.gvGraph.get_node(term).attr['color'] = colors[term]

print("Enter genes:")
genes = input().strip().split(" ")
if len(genes) == 1:
    m = MiniGraph(genes[0])
else:
    m1 = MiniGraph(genes[0])
    m2 = MiniGraph(genes[1])
    m1.gvGraph.draw('pokus1.png')
    m2.gvGraph.draw('pokus2.png')
    m = MiniGraph()
    m.add(m1, m2)
m.gvGraph.draw('pokus1a2.png')

