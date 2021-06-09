import matplotlib.pyplot as plt
import networkx as nx

import re

class Utility:

  @staticmethod
  def readFile(path):
  #reads and returns the given file
    file = open(path,"r")
    code = file.read()
    file.close()
    return  code

  @staticmethod
  def draw_graph(nodes, edges,edge_labels,size, path=None, save = True):
    #draw networkx graph with given settings
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    #print(nx.info(G))
    plt.figure(figsize=size)
    
    formatted_edge_labels = None
    if edge_labels != None:
      formatted_edge_labels = dict([((n[0], n[1]), edge_labels[i]) for  i, n in enumerate(G.edges(data=True))])

    pos = nx.planar_layout(G)
    nx.draw(G, pos, with_labels=True,node_size=2250,node_color = '#86D3D4',node_shape='o',font_size="12",arrowsize=18)
    nx.draw_networkx_edge_labels(G, pos = pos,edge_labels=formatted_edge_labels, label_pos=0.5,
                             font_color='red', font_size=10)
    if save:
      plt.savefig(path,transparent=True)

  @staticmethod
  def getLineNumber(pos, document):
    #Returns the line number to which the character's position corresponds
      return len(re.findall('\n', document[:pos])) + 1 

  @staticmethod 
  def isConsist(var,lists):
  #Returns true if the variable is exist inside the nested list's second element
    for aList in lists:
      if var == aList[2]:
        return True
    return False

class Object:
  #instance of object
    def __init__(self,variableType, variableName, pos):
      self.pos = pos
      self.variableType = variableType
      self.variableName = variableName   

    def printLineNumber(self,doc):
      return str(Utility.getLineNumber(self.pos,doc))+"\n"

    def printObject(self,doc):
      return self.variableType +" "+ self.variableName + ' : '+ self.printLineNumber(doc)
    