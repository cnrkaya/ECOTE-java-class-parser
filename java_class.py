from utility import Utility,Object

import re


class JavaClass:
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
        names = '('
        for name in classNames:
          names += name + "|"

        names = names[:-1]
        names += ')'
        return names
            
    def setAttributeObjects(self,classNames):

        names = self.__regexTransform(classNames)
        
        regex = names+'\s+(\w+)\s*;'
        attributes = re.finditer(regex,self.code)
        for att in attributes:
          startPos,endPos =att.span()
          
          self.attributeObjects.append(Object(att.group(1),att.group(2),self.startPos+endPos) )
            
        return 

    def setDynamicObjects(self,classNames):
      
      names = self.__regexTransform(classNames)
      regex = names + "\s+(\w+)\s*="
      dynamicObjects = re.finditer(regex,self.code)
      
      for aObject in dynamicObjects:
        startPos,endPos =aObject.span()
        self.dynamicObjects.append(Object(aObject.group(1),aObject.group(2),self.startPos+endPos) )


    def setMemberUsages(self,doc):
      
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
      regex = '\((?:\s*(\w+)\s*(\w+)\s*,?)+\)'
      parameters =  re.finditer(regex,self.code)
      for parameter in parameters:
                  
          startPos,endPos =parameter.span()
          self.parameters.append( Object(parameter.group(1),parameter.group(2),self.startPos+endPos) )
          
    def getVariableTypeOfObject(self,objectName):
      for att in self.attributeObjects:
        if att.variableName == objectName:
          return att.variableType

    def printMembers(self,doc):
      print("---Attribute Objects---")
      if len(self.attributeObjects) == 0:
        print("| None")
      for att in self.attributeObjects:
        print("| ",end="")
        att.printObject(doc)

      print("---Dynamic Objects---")
      if len(self.dynamicObjects) == 0:
        print("| None")
      for att in self.dynamicObjects:
        print("| ",end="")
        att.printObject(doc)
      print("---Parameters---")
      if len(self.parameters) == 0:
        print("| None")
      for att in self.parameters:
        print("| ",end="")
        att.printObject(doc)     


    @staticmethod
    def getLineNumber(pos, document):
        return len(re.findall('\n', document[:pos])) + 1 

    @staticmethod
    def getPosition(lineNumber, document):
       lines = re.finditer('\n', document)
       pos = 0
       for aLine in lines:
         pos,_ = aLine.span()
         lineNumber -= 1
         if lineNumber == 0: 
           break
       return pos
       