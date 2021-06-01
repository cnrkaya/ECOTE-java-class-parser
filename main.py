from utility import Utility
from java_class_parser import JavaClassParser

import sys
import argparse

def main():

    #Parsing Arguments of the program
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",metavar = "FILEPATH",required=True, help="The path of the java file.")

    parser.add_argument("--output",metavar = "FILEPATH",default=None, help="The path of the output file(s)")

    parser.add_argument('--details', help="Creates a text file that consist parsing details by default.\
             If this file is not desired, this flag is used with 'False' parameter .",metavar="BOOLEAN",type=bool,default=True)

    parser.add_argument('--labels',help= "show/hide the labels of the member that caused the dependency on the graphic.\
            This name information, shown by default, can make the graph invisible if dependency number is high."
            ,metavar="BOOLEAN",type=bool,default=True)

    parser.add_argument('--pngsize',type=int,nargs=2,default=(10,10)
        ,help ='Specifies the inches size of the output graphic [inch][inch]')

    args = parser.parse_args()

    print(args)
    
    #read the code
    try:    
        input_path = args.input 
        code = Utility.readFile(input_path)
    except:
        print("The file could not be opened")
        sys.exit(-1)

    #if not given specific path for output
    if args.output == None:
        outputPath = args.input
    
    #parse the code
    myParser = JavaClassParser(code)

    #Add parsing information to output
    output_string = myParser.information()
    
    #Add logs created while finding dependency to output
    output_string += "\n----------------LOGS----------------\n"+ myParser.logs

    #Add dependency list to output
    output_string += "\n Dependencies: " +str(myParser.dependencies)

    
    #print output
    print(output_string)

    if args.details == True:
        #write output to file 
        f = open(outputPath+"_output.txt", "w",encoding="utf-8")
        f.write(output_string)
        f.close()

    #draw graph and write to file
    nodes = myParser.getClassNames()[1:]
    edges = []
    labels = []
    [[edges.append(dep[0]),labels.append(dep[1])] for dep in myParser.dependencies]
    if args.labels == False:
        labels = None
    Utility.draw_graph(nodes=nodes, edges=edges,edge_labels=labels, path= outputPath+"_output.png",size=args.pngsize)
    

if __name__ == "__main__":
    main()