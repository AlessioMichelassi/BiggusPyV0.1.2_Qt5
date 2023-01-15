def parseCode(self, _code: str):
# sourcery skip: for-index-underscore
    tree = ast.parse(_code)
    for _node in ast.walk(tree):
        if isinstance(_node, ast.FunctionDef):
            self.createFunction(_code, _node, tree)
            break
        elif isinstance(_node, ast.Assign):
            for target in _node.targets:
                if isinstance(target, ast.Name) and isinstance(_node.value, ast.Call):
                    # crea un VariableNode
                    variableName = target.id
                    callNode = self.getNodeByName(_node.value.func.id)
                    self.createVariableNode(variableName, callNode)
                    for i, arg in enumerate(_node.value.args):
                        # Crea un NumberNode
                        if isinstance(arg, ast.Num):
                            self.createNumberNode(arg, variableName, callNode)
        if isinstance(_node, ast.BinOp) and isinstance(_node.op, (ast.Add, ast.Mult, ast.Sub, ast.Div)):
            leftNode = self.getNodeByName(_node.left.id)
            rightNode = self.getNodeByName(_node.right.id)
            if leftNode and rightNode:
                self.createSumNode(_node.op, leftNode, rightNode)
                variableDict = {"variable": variableName, "nodes": [leftNode, rightNode, SumNode_0]}
                self.NodeToBeCreated.append(variableDict)