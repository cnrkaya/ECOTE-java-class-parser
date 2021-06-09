from java_class import JavaClass
from utility import Utility,Object
from java_class_parser import JavaClassParser
import os 

import unittest

class UtilityTestCases(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
    #Call after every test case.
        pass
    
    @staticmethod #method will be used for another test case classes
    def readTestFile():  
        dir_path = os.path.dirname(os.path.realpath(__file__))
        code = Utility.readFile(dir_path+"\\tests\\test1.java")
        return code

    def testReadTestFile(self):
        code = UtilityTestCases.readTestFile()
        assert code != None, "Reading File Error"
    
    def testLineNumber(self):
        #numbers are equals character positions in this example
        document = '123\n' \
                    '5\n'   \
                    '7\n'    \
                    '9\n'
        assert Utility.getLineNumber(1,document) == 1, "Line Error"
        assert Utility.getLineNumber(5,document) == 2, "Line Error"
        assert Utility.getLineNumber(7,document) == 3, "Line Error"                                
        assert Utility.getLineNumber(9,document) == 4, "Line Error"

    def testCreateAttribute(self):
        anObject = Object(variableType="int",variableName="test",pos=10)
        assert anObject != None, "Object Creating Error"


class JavaClassTestCases(unittest.TestCase):
    def setUp(self):
        self.code = UtilityTestCases.readTestFile()
    
    def tearDown(self):
    #Call after every test case.
        pass

    def testCreateObject(self):
        assert JavaClass("TestClass",0,100,self.code) != None, "Creating JavaClass Object Error"

    def test2CreateObject(self):
        anObject = JavaClass("TestClass",0,100,self.code)
        len(anObject.code) == 100, "Code Parsing Error"


class SimpleTestCase(unittest.TestCase):
    def setUp(self):
        self.code = UtilityTestCases.readTestFile()
    
    def tearDown(self):
    #Call after every test case.
        pass


    def testParser(self):
        code  = self.code
        myParser = JavaClassParser(code)
        assert myParser != None, "Parser Creating Error"
        return myParser
    
    def testParserTree(self):
        myParser = self.testParser()
        myParser.createClassTree()
        assert myParser.tree.get_node('root') != None, "Tree Creating Error"

    def testDependency(self):
        myParser = self.testParser()
        myParser.findDependencies()
        #print(myParser.dependencies)
        assert len(myParser.dependencies) != 0, "Dependency could not find"

if __name__ == "__main__":
     unittest.main() # run all tests
    