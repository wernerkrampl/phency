import networkx
import obonet
import matplotlib.pyplot as plt

url = 'https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo'
graph = obonet.read_obo(url)

# HPO database is saved in file hpo.txt, this was used to work without internet
#database = open('hpo.txt', 'r')
#graph = obonet.read_obo(database)

class MiniGraph:

    def __init__(self, termID='empty'):
        if termID == 'empty':
            return
        else:    
            #networkx.ancestors returns descendants - reversily directed edges  
            self.nodes = networkx.ancestors(graph, termID)
            self.nodes.add(termID)
            # in self.miniGraph is wanted subgraph
            self.miniGraph = graph.subgraph(self.nodes)
            self.impactScore = {node: float(0.0)  for node in self.nodes}

    #newScore is dictionary (node : score)
    def changeScore(self, newScore):
        self.impactScore = newScore

    def showGraph(self):
        plt.subplot(121)
        networkx.draw(self.miniGraph, labels = self.impactScore, font_size = 10)
        plt.show()

    def add(self, graph1, graph2):
        self.impactScore = graph1.impactScore.copy()
        for name, score in graph2.impactScore.items():
            if name in self.impactScore:
                self.impactScore[name] += score
            else:
               self.impactScore[name] = score
        self.nodes = self.impactScore.keys()
        self.miniGraph = graph.subgraph(self.nodes)
    
    #graph2 is subtracted from graph1
    def subtract(self, graph1, graph2):
        self.impactScore = graph1.impactScore.copy()
        for name, score in graph2.impactScore.items():
            if name in self.impactScore:
                self.impactScore[name] -= score
        self.nodes = self.impactScore.keys()
        self.miniGraph = graph.subgraph(self.nodes)


# HPOterm HP:0031264
m1 = MiniGraph('HP:0031264')
is1 = {'HP:0020133': 0.08, 'HP:0031265': 0.04, 'HP:0031266': 0.002, 'HP:0031264': 0.054}
m1.changeScore(is1)
#m1.showGraph()

# HPOterm HP:0020133
m4 = MiniGraph('HP:0020133')
is4 = {'HP:0020133': 0.08}
m4.changeScore(is4)
#m4.showGraph()

# HPOterm HP:0031266
m2 = MiniGraph('HP:0031266')
is2 = {'HP:0031266': 0.098}
m2.changeScore(is2)
#m2.showGraph()

# HPOterm HP:0000608
m5 = MiniGraph('HP:0000608')
is5 = {'HP:0007401': 0.7, 'HP:0025094': 0.024, 'HP:0025146': 0.05, 'HP:0000608': 0.12, 'HP:0200056': 0.037, 'HP:0008028': 0.004}
m5.changeScore(is5)
#m5.showGraph()

# HPOterm HP:0001105
m6 = MiniGraph('HP:0001105')
is6 = {'HP:0200056': 0.01, 'HP:0031609': 0.08, 'HP:0007791': 0.017, 'HP:0001105': 0.3, 'HP:0007401': 0.7, 'HP:0025094': 0.5, 'HP:0200070': 0.001, 'HP:0007722': 0.22}
m6.changeScore(is6)
#m6.showGraph()

# add
m3 = MiniGraph()
m3.add(m4, m2)
#m3.showGraph()

# subtract
m7 = MiniGraph()
m7.subtract(m5, m6)
#m7.showGraph()
