import networkx
import obonet
import matplotlib.pyplot as plt

url = 'https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo'
graph = obonet.read_obo(url)

#nasledujuce dva prikazy som pouzivala abz som mohla pracovat bez internetu, cela hpo je v subore hpo.txt
#database = open('hpo.txt', 'r')
#graph = obonet.read_obo(database)

print('Enter gene ID:')
geneID = input()

#networkx.ancestors - vracia potomkov, .descendants - vracia predkov - hrany su opacne orientovane
sub = networkx.ancestors(graph, geneID)
sub.add(geneID)
# v G mame subgraf ktory hladame
G = graph.subgraph(sub)

#graph.nodes(data = True) oznacuje ze chceme vsetky atributy nodov
id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data = True)}
labelsDict = {superterm: id_to_name[superterm] for superterm in sub}

plt.subplot(121)
networkx.draw(G, labels = labelsDict, font_size = 10)
plt.show()

