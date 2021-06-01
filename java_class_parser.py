from java_class import JavaClass
from utility import Object,Utility
from treelib import Node, Tree
import re


class JavaClassParser:
    def __init__(self, code):
        self.logs = ""
        self.code = code 
        self.dependencies = []
        self.__createClassTree()
        self.__checkClassHierarchy()
        self.__findAttributeObjects()
        self.__findDynamicObjects()
        self.__findParameters()
        self.__findMemberUsages()
        self.__checkClassHierarchy()
        self.__findDependencies()
        

    def __createClassTree(self):
        self.tree = Tree()
        self.tree.create_node("Root", "root", data = JavaClass("ROOT",0,0,self.code))
        regex = '(private|public|protected|internal)?\s*(abstract|final|static)?\s*class\s*(\w+)\s*[^{]*{'
        classes = re.finditer(regex,self.code)
        for aClass in classes:
            startPos,endPos = aClass.span()
            #print(startPos,endPos)
            className = aClass.group(3)
            startPos = endPos
            endPos = self.__findScope(endPos)

            #create class
            tmp_class =  JavaClass(className=className, startPos=startPos, endPos=endPos,document=self.code)

            #add node
            self.tree.create_node(className, className, parent = "root", data = tmp_class)

    def __checkClassHierarchy(self):
      #Organizes the tree according to the inner and parent classes.

      nodes = self.tree.all_nodes()
      
      for is_child_node in nodes: 
        for node in nodes:
          if self.__isInner(is_child_node.data,node.data) :
            is_child_node.data.parent = node.data.className
            self.tree.move_node(is_child_node.data.className,node.data.className)
            self.__removeSameMemberUsages(parent=node.data,child=is_child_node.data)


    def __removeSameMemberUsages(self, parent, child):
    # remove same member usages in parent
      for memberUsage in parent.memberUsages:
        if memberUsage in child.memberUsages:
          parent.memberUsages.remove(memberUsage)
      

    def __isInner(self, node1, node2):
      #if node1 is inner class return true
      if node1.startPos > node2.startPos and node1.endPos < node2.endPos:
        return True
      return False


    def __findScope(self,endPos):
      i = endPos
      openBracket = 1
      while(openBracket != 0):
          if self.code[i] == '{':
            openBracket += 1
          elif self.code[i] == '}':
            openBracket -=1
          i += 1
      return i

    def getClassNames(self):
      classNames = []
      nodes = self.tree.all_nodes()
      
      for node in nodes:
        classNames.append(node.tag)
      
      return classNames

    def __findAttributeObjects(self):
      
      nodes = self.tree.all_nodes()
      
      for node in nodes:
        node.data.setAttributeObjects(self.getClassNames())

    def __findDynamicObjects(self):
      
      nodes = self.tree.all_nodes()
      
      for node in nodes:
        node.data.setDynamicObjects(self.getClassNames())

    def __findParameters(self):
      nodes = self.tree.all_nodes()
      
      for node in nodes:
        node.data.setParameters(self.code)

    def __findMemberUsages(self):
      nodes = self.tree.all_nodes()
      
      for node in nodes:
        node.data.setMemberUsages(self.code)

    def __findDependencies(self):
      nodes = self.tree.all_nodes()
      for node in nodes:
        usages = node.data.memberUsages
        for usage in usages:

          grammer = usage.split(",")[0]
          lineNumber = int(usage.split(",")[1])
          #print("searching: "+ usage)
          found = 0         #flag value 

          if grammer[:4] == "this":
            dependency = node.data.getVariableTypeOfObject(grammer[5:])
            if dependency != None:
              self.logs += "CASE 1: Used an Attribute Object \n"
              self.logs += node.data.className +" dependent by "+ dependency + \
              " because " + usage + " is member of " + dependency + "  Object\n"
              self.dependencies.append([node.data.className,dependency])
              found = 1
          
          if found == 0:
            objects = node.data.dynamicObjects
            for aObject in objects:
              if grammer.split(".")[0] == aObject.variableName: 
                self.logs += "CASE 2: Used a Dynamically defined object\n"
                self.logs += node.data.className +" dependent by "+ aObject.variableType + \
                  " because " + usage + " is member of " + aObject.variableType + "  Object\n"
                self.dependencies.append([node.data.className,aObject.variableType])
                found = 1
                break
            
          if found == 0:
            pos = JavaClass.getPosition(lineNumber, self.code)
            parameters = node.data.parameters 
            for parameter in parameters:
              if grammer.split(".")[0] == parameter.variableName:
                self.logs += "CASE 3: Used a taken as parameter object \n"
                self.logs += node.data.className +" dependent by "+ parameter.variableType +\
                   " because " + usage + " is member of " + parameter.variableType + "  Object\n"
                self.dependencies.append([node.data.className,parameter.variableType])                
                found = 1
                break

          if found == 0:
            #CASE 4
            parent = node.data.parent
            while parent != None:
              parent_node = self.tree.get_node(parent)
              dependency = parent_node.data.getVariableTypeOfObject(grammer.split(".")[0])
              if dependency != None:
                self.logs += "CASE 4: Used an attribute object belonging to parent class\n"
                self.logs += node.data.className +" dependent by "+ dependency+\
                  " because " + usage + " is member of " + dependency + "  Object\n"
                self.dependencies.append([node.data.className,dependency])
                found = 1
                break
              parent = parent_node.data.parent
               
              
    def information(self):
      output = ""
      string_tree = self.tree.show(stdout=False)
      output +=string_tree+"\n"

      nodes = self.tree.all_nodes()
      
      for node in nodes:
        if node.tag == 'Root':
          continue

        aClass = node.data
        startLine = JavaClass.getLineNumber(aClass.startPos,self.code)
        endLine = JavaClass.getLineNumber(aClass.endPos,self.code)
        output +='------------------------------------'+"\n"
        output +="[CLASS] " + aClass.className+' : '+str(startLine)+'-'+str(endLine)+"\n"

        output = aClass.printMembers(self.code, output)
        
        output +="--Member Usages---\n"
        output +=str(aClass.memberUsages)+"\n"

      return output


