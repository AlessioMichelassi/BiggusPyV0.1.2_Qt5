import ast

from PyQt5.QtCore import QPoint


code = '''def SieveOfEratosthenes(n):
    prime_list = []
    for i in range(2, n+1):
        if i not in prime_list:
            print (i)
            for j in range(i*i, n+1, i):
                prime_list.append(j)'''


class nodeCreator:

    def __init__(self, graphicView: 'graphicViewOverride'):
        self.graphicView = graphicView
        self.canvas = self.graphicView.canvas

    def createNodeFromCode(self, code: str):
        # parse the code into an AST
        parsed_code = ast.parse(code)

        # define a variable to keep track of the nodes
        nodes = []

        # iterate over the AST and create nodes for each statement
        for node in ast.walk(parsed_code):
            if isinstance(node, ast.FunctionDef):
                # _function_node = FunctionNode(node.name, None)
                _functionNode = AbstractNodeInterface(node.name, view=self.graphicView)
                nodes.append(_functionNode)
            elif isinstance(node, ast.For):
                # _for_node = ForNode(None)
                _for_node = AbstractNodeInterface("ForNode", view=self.graphicView)
                nodes.append(_for_node)
            elif isinstance(node, ast.If):
                if_node = AbstractNodeInterface("IfNode", view=self.graphicView)
                nodes.append(if_node)
            elif isinstance(node, ast.Call):
                try:
                    if isinstance(node.func, ast.Name):
                        # call_node = CallNode(node.func.id, None)
                        call_node = AbstractNodeInterface("CallNode", value=node.func.id, view=self.graphicView)
                    elif isinstance(node.func, ast.Attribute):
                        # call_node = CallNode(node.func.attr, None)
                        call_node = AbstractNodeInterface("CallNode", value=node.func.attr, view=self.graphicView)
                    nodes.append(call_node)
                except Exception as e:
                    print("*" * 20)
                    print(e)
                    print("*" * 20)
            elif isinstance(node, ast.Name):
                # _variable_node = VariableNode(node.id, None, None)
                _variable_node = AbstractNodeInterface("VariableNode", view=self.graphicView)
                nodes.append(_variable_node)
            elif isinstance(node, ast.Num):
                # number_node = NumberNode(node.n, None)
                number_node = AbstractNodeInterface("VariableNode", value=node.id, view=self.graphicView)
                nodes.append(number_node)
        return nodes

    def createNodes(self, _code: str):
        # create the nodes from the code
        nodes = self.createNodeFromCode(_code)

        # connect the nodes together to represent the flow of the original code
        for_node = None
        for node in nodes:
            if isinstance(node, ForNode):
                for_node = node
            elif isinstance(node, CallNode) and node.name == 'append':
                if for_node:
                    variable_node = next(
                        filter(lambda x: isinstance(x, VariableNode) and x.name == 'prime_list', nodes))
                    for_node.connect(variable_node, 0, 0)
                    variable_node.connect(node, 0, 0)
        return nodes

    def pasteCode(self, code):
        nodes = self.createNodeFromCode(code)
        for node in nodes:
            x = 200
            y = 200
            centerPoint = QPoint(x, y)
            self.canvas.createNodeFromDialog(node, centerPoint)
            y += 300
        print(nodes)
