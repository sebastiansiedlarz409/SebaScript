from lexer.tokens import *
from parser.nodes import *

class SSParser:
    def __init__(self):
        self.tokens = []

    def iseof(self) -> bool:
        return self.tokens[0].type == SSTokens.EOFToken
    
    def get(self) -> str:
        t = self.tokens[0]
        self.tokens.pop(0)
        return t
    
    def peak(self, offset: int = 0) -> str:
        return self.tokens[offset]

    """
    program:
        variableassignnode |
        functiondeclarationnode
    """
    def parseProgram(self, tokens: list[SSToken]) -> Node:
        self.tokens = tokens

        #prepare main node
        program = ProgramNode()

        while not self.iseof():
            node = None

            #parse variable assign
            node = self.parseVariableAssign()
            if node != None:
                program.appendChild(node)
                continue
            
            #parse function declaration
            node = self.parseFunctionDeclaration()
            if node != None:
                program.appendChild(node)
                continue

            #testing only
            node = self.parseUnaryExpression()
            if node != None:
                program.appendChild(node)
                continue

        return program
    
    """
    factor -> [IdentifierNode, NumberNode, arithmeticexpression]:
        numbertoken | identifiertoken
    """
    def parseFactor(self) -> Node:
        #check for exp inside paren
        if self.peak().type == SSTokens.LParenToken:
            self.get()
            n = self.parseUnaryExpression()
            if self.get().type != SSTokens.RParenToken:
                raise Exception(f"SSParser: Expected RParenToken")
            return n

        #number token
        if self.peak().type == SSTokens.NumberToken:
            n = NumberNode()
            n.setValue(self.get().value)
            return n
        
        #identifier
        if self.peak().type == SSTokens.IdentifierToken:
            n = IdentifierNode()
            n.setIdentifier(self.get().value)
            return n
        
        #null
        if self.peak().type == SSTokens.NullKwToken:
            n = NullNode()
            n.setValue(self.get().value)
            return n
        
        #true false
        if self.peak().type == SSTokens.TrueKwToken or self.peak().type == SSTokens.FalseKwToken:
            n = BoolNode()
            n.setValue(self.get().value)
            return n
        
        raise Exception(f"SSParser: Unexpected token {self.peak().value}")

    """
    term -> [BinaryOperatorNode, factor]:
        factor (binaryoperatortoken(mul, div, mod) factor)
    """
    def parseMulArithmeticExpression(self) -> Node:
        left = self.parseFactor()
        while self.peak().value in "*/%":
            operator = self.get().value #operator
            right = self.parseFactor()
            temp = BinaryExpressionNode()
            temp.lChild = left
            temp.rChild = right
            temp.operator = operator
            left = temp

        return left

    """
    arithmeticexpression -> [BinaryOperatorNode, mularithmeticexpression]:
        mularithmeticexpression (binaryoperatortoken(add, sub) mularithmeticexpression)
    """
    def parseAddArithmeticExpression(self) -> Node:
        left = self.parseMulArithmeticExpression()
        while self.peak().value in "+-":
            operator = self.get().value #operator
            right = self.parseMulArithmeticExpression()
            temp = BinaryExpressionNode()
            temp.lChild = left
            temp.rChild = right
            temp.operator = operator
            left = temp

        return left

    """
    comparasionexpression -> [BinaryOperatorNode, addarithmeticexpression]:
        addarithmeticexpression (binaryoperatortoken(comparasion) addarithmeticexpression)
    """
    def parseComparasionExpression(self) -> Node:
        left = self.parseAddArithmeticExpression()
        while self.peak().value in ["eq", "neq", "gr", "ge", "ls", "le"]:
            operator = self.get().value #operator
            right = self.parseAddArithmeticExpression()
            temp = BinaryExpressionNode()
            temp.lChild = left
            temp.rChild = right
            temp.operator = operator
            left = temp

        return left

    """
    bitewiseexpression -> [BinaryOperatorNode, camparasionexpression]:
        comparasionexpression (binaryoperatortoken(comparasion) comparasionexpression)
    """
    def parseBitewiseExpression(self) -> Node:
        left = self.parseComparasionExpression()
        while self.peak().value in "|&<>^":
            operator = self.get().value #operator
            right = self.parseComparasionExpression()
            temp = BinaryExpressionNode()
            temp.lChild = left
            temp.rChild = right
            temp.operator = operator
            left = temp

        return left

    """
    logicalexpression -> [BinaryOperatorNode, bitewiseexpression]:
        bitewisexpression (binaryoperatortoken(comparasion) bitewisexpression)
    """
    def parseLogicalExpression(self) -> Node:
        left = self.parseBitewiseExpression()
        while self.peak().value in ["and", "or"]:
            operator = self.get().value #operator
            right = self.parseBitewiseExpression()
            temp = BinaryExpressionNode()
            temp.lChild = left
            temp.rChild = right
            temp.operator = operator
            left = temp

        return left
    
    """
    
    """
    def parseUnaryExpression(self) -> Node:
        if self.peak().type == SSTokens.UnaryOperatorToken:
            u = UnaryExpressionNode()
            u.setOperator(self.get().value)

            child = self.parseLogicalExpression()
            
            u.setChild(child)
            return u
        
        return self.parseLogicalExpression()


    """
    variableassign -> [VariableAssignNode]:
        letkwtoken identifiertoken assignoperatortoken logicalexpression
    """
    def parseVariableAssign(self) -> Node:
        pass

    def parseFunctionDeclaration(self) -> Node:
        pass