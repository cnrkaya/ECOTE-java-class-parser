import matplotlib.pyplot as plt
import networkx as nx

import re

class Utility:

  @staticmethod
  def readFile(path):
    file = open(path,"r")
    return  file.read()

  @staticmethod 
  def isConsist(var,lists):
    for aList in lists:
      if var == aList[2]:
        return True
    return False

  @staticmethod
  def draw_graph(nodes, edges, path=None, save = True):
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    print(nx.info(G))
    plt.figure()
    nx.draw_planar(G, with_labels=True,node_size=2000,node_color = '#86D3D4',node_shape='o',font_size="15",arrowsize=18)
    plt.show()
    if save:
      plt.savefig(path,transparent=True)

    @staticmethod
    def getLineNumber(pos, document):
        return len(re.findall('\n', document[:pos])) + 1 

class Object:
    def __init__(self,variableType, variableName, pos):
      self.pos = pos
      self.variableType = variableType
      self.variableName = variableName   

    def printObject(self,doc):
      print(self.variableType +" "+ self.variableName + ' : '+ str(Utility.getLineNumber(self.pos,doc)))
    