from utility import Utility,Object

import re

class JavaClass:
    #Information of the java class that can create dependency is kept
    
    def __init__(self,className,startPos, endPos,document):
            self.className = className
            self.startPos  = startPos
            self.endPos = endPos
            self.parent = None
            self.code = document[startPos:endPos] 

            self.attributeObjects = [] 
            self.dynamicObjects= []
            self.parameters = []
            self.memberUsages = []
            self.dependencies = []

    def __regexTransform(self,classNames):
        # Converts class names consisting of string list into regex as seen in the example below
        # ["Person","Contact"] ---> (Person|Contact)
        names = '('
        for name in classNames:
          names += name + "|"

        names = names[:-1]
        names += ')'
        return names
            
    def setAttributeObjects(self,classNames):
        #Find and set attribute Objects belonging to the class using regular expressions
        names = self.__regexTransform(classNames)
        regex = names+'\s+(\w+)\s*;'
        attributes = re.finditer(regex,self.code)
        for att in attributes:
          startPos,endPos =att.span()
          
          self.attributeObjects.append(Object(att.group(1),att.group(2),self.startPos+endPos) )

    def setDynamicObjects(self,classNames):
      #Find and set dynamic Objects belonging to the class using regular expressions
      names = self.__regexTransform(classNames)
      regex = names + "\s+(\w+)\s*="
      dynamicObjects = re.finditer(regex,self.code)
      
      for aObject in dynamicObjects:
        startPos,endPos =aObject.span()
        self.dynamicObjects.append(Object(aObject.group(1),aObject.group(2),self.startPos+endPos) )


    def setMemberUsages(self,doc):
      #Find and set member Usages belonging to the class using regular expressions
      regex = '(?:(\w+)\.)?(\w+)\.(\w+)'   #for member usages
      regex2 = '(?:(\w+)\.)?(\w+)\.(\w+)\(' #for method usages
      memberUsagess = re.finditer(regex,self.code)
      methodUsages = re.findall(regex2,self.code)
      for usage in memberUsagess:
          if usage.group(1) != None or usage.group(2) != 'this':
            if Utility.isConsist(usage.group(3),methodUsages) == False:
              startPos,endPos =usage.span()
              line = JavaClass.getLineNumber(self.startPos+endPos,doc)
              self.memberUsages.append(usage.group()+','+str(line))

    def setParameters(self,doc):
      #Find and set parameters belonging to the class using regular expressions
      regex = '\((?:\s*(\w+)\s*(\w+)\s*,?)+\)'
      parameters =  re.finditer(regex,self.code)
      for parameter in parameters:               
          startPos,endPos =parameter.span()
          self.parameters.append(Object(parameter.group(1),parameter.group(2),self.startPos+endPos))
          
    def getVariableTypeOfObject(self,objectName):
    # return variable type of object if defined as an attribute
      for att in self.attributeObjects:
        if att.variableName == objectName:
          return att.variableType

    def printMembers(self,doc,output):
    #return all member's informations
    
      output +="---Attribute Objects---\n"
      if len(self.attributeObjects) == 0:
        output +="| None\n"
      for att in self.attributeObjects:
        output +="| "
        output += att.printObject(doc)

      output +="---Dynamic Objects---\n"
      if len(self.dynamicObjects) == 0:
        output +="| None\n"
      for att in self.dynamicObjects:
        output +="| "
        output += att.printObject(doc)

      output +="---Parameters---\n"
      if len(self.parameters) == 0:
        output +="| None\n"
      for att in self.parameters:
        output +="| "
        output += att.printObject(doc)     

      return output


    @staticmethod
    def getLineNumber(pos, document):
      #Returns the line number to which the character's position corresponds 
        return len(re.findall('\n', document[:pos])) + 1 

    @staticmethod
    def getPosition(lineNumber, document):
    #Returns the position of the first character in the line number
       lines = re.finditer('\n', document)
       pos = 0
       for aLine in lines:
         pos,_ = aLine.span()
         lineNumber -= 1
         if lineNumber == 0: 
           break
       return pos
       