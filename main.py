from utility import Utility
from java_class_parser import JavaClassParser


import os
def main():
    print("Hello")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)

    #read the code
    code = Utility.readFile(dir_path+"\\test2.java")
    
    #parse the code
    myParser = JavaClassParser(code)

    #draw graph
    nodes = myParser.getClassNames()[1:]
    edges = myParser.dependencies

    Utility.draw_graph(nodes=nodes, edges=edges, path= dir_path+"\\aaa.png")
    

if __name__ == "__main__":
    main()