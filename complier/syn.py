import traceback
class node:
    def __init__(self):
        self.root = None
        self.childs = list()

class item:
    pass
        

class syn:
    def __init__(self,lex):
        self.root = None
        self.lex = lex
        self.pointer = 0
        self.symbols = list()
        self.max_approach = 0

    def make_childs(self,node,pre_childs):
        pointer_backup = self.pointer
        for childs in pre_childs:
            self.pointer = pointer_backup
            match_res = self.match_seq(childs)
            if match_res is not None:
                node.childs = match_res
                return node
        return None

    def test(self):
        def print_node(x):
            print(x.root["string"],end=" | ")
            for child in x.childs:
                print(child.root["string"],end=" ")
            print()
            for child in x.childs:
                print_node(child)
        def print_tab(cnt):
            for i in range(cnt):
                print("  ",end='')

        def print_node2(x,deepth):
            print_tab(deepth)
            print(x.root['string'])
            for child in x.childs:
                print_node2(child,deepth+1)

        print("\nThe tree showed as below!")

        #print_node(self.root)
        print_node2(self.root,0)

        print("\nThe symbols table showed as below!")
        for symbol in self.symbols:
            print(symbol.name,end=" ")
            print(symbol.type,end=" ")
            if symbol.type == "var":
                print(symbol.var_type,end=" ")
                print(symbol.array,end=" ")
                if symbol.array:
                    print(symbol.contains,end=" ")
            else:
                print(symbol.fun_type,end=" ")
                print(symbol.params,end=" ")
            print()

    def wapper(self,token):
        ret = node()
        ret.root = token
        return ret
    
    def match_seq(self,target_seq):
        seq = list()
        for target in target_seq:
            if target in ['if','while',';','return','[',']','identifier',
                          '{','}','(',')','num','>=','>','<','<=','==','!=',
                          '+','-','*','/','int','void','=','else',',']:
                if self.pointer < len(self.lex.tokens):
                    token = self.now_look()
                    if token["type"] == target:
                        seq.append(self.wapper(token))
                        self.pointer+=1
                        self.max_approach = max(self.max_approach,self.pointer)
                    else:
                        return None
                else:
                    return None
            else:
                expected_node = getattr(self,target)()
                if expected_node is not None:
                    seq.append(expected_node)
                else:
                    return None
        return seq

    def now_look(self):
        return self.lex.tokens[self.pointer]

    def build(self):
        self.root = self.program()
        if self.pointer < len(self.lex.tokens):
            print("There's an error @ token %s %s" % 
                  (str(self.max_approach),str(self.lex.tokens[self.max_approach])))
        else:
            print("The Program is correct!")

    def program(self):
        ret = node()
        ret.root = {"type":"program","string":"program"}
        ret.childs.append(self.declaration_list())
        return ret

    def declaration_list(self):
        ret = node()
        ret.root = {"type":"declaration_list","string":"declaration_list"}
        child = self.declaration()
        while child is not None:
            ret.childs.append(child)
            child = self.declaration()
        return ret

    def declaration(self):
        ret = node()
        ret.root = {"type":"declaration","string":"declaration"}
        pre_targets = [["fun_declaration"],
                     ["var_declaration"]]
        return self.make_childs(ret,pre_targets)

    def var_declaration(self):
        ret = node()
        ret.root = {"type":"var_declaration","string":"var_declaration"}
        pre_targets = [["type_specifier","identifier",";"],
                     ["type_specifier","identifier","[","num","]",";"]]
        pnode = self.make_childs(ret,pre_targets)
        if pnode is not None:
            if len(pnode.childs) == 3:
                it = item()
                it.name = pnode.childs[1].root["string"]
                it.type = "var"
                it.var_type = pnode.childs[0].childs[0].root["type"]
                it.array = False
                self.symbols.append(it)
            else:
                it = item()
                it.name = pnode.childs[1].root["string"]
                it.type = "var"
                it.var_type = pnode.childs[0].childs[0].root["type"]
                it.array = True
                it.contains = pnode.childs[3].root["string"]
                self.symbols.append(it)
            return pnode
        else:
            return None

    def fun_declaration(self):
        ret = node()
        ret.root = {"type":"fun_declaration","string":"fun_declaration"}
        pre_targets = [["type_specifier","identifier","(","params",")","compound_stmt"],]
        pnode = self.make_childs(ret,pre_targets)
        if pnode is not None:
            it = item()
            it.name = pnode.childs[1].root["string"]
            it.type = "fun"
            it.fun_type = pnode.childs[0].childs[0].root["type"]
            it.params = list()
            if pnode.childs[3].childs[0].root["type"] != "void":
                param_list = pnode.childs[3].childs[0].childs
                for param in param_list:
                    if param.root["type"] == "param":
                        it.params.append(param.childs[0].childs[0].root["type"])

                        #把参数加入符号表中
                        pit = item()
                        pit.name = param.childs[1].root["string"]
                        pit.type = "var"
                        pit.array = False
                        pit.var_type = param.childs[0].childs[0].root["type"]
                        self.symbols.append(pit)

            self.symbols.append(it)
            return pnode
        else:
            return None

    def type_specifier(self):
        ret = node()
        ret.root = {"type":"type_specifier","string":"type_specifier"}
        pre_targets = [["int"],
                     ["void"]]
        return self.make_childs(ret,pre_targets)

    def params(self):
        ret = node()
        ret.root = {"type":"params","string":"params"}
        pre_targets = [["param_list"],
                    ["void"]]
        return self.make_childs(ret,pre_targets)

    def compound_stmt(self):
        ret = node()
        ret.root = {"type":"compound_stmt","string":"compound_stmt"}
        pre_targets = [["{","local_declarations","statement_list","}"],]
        return self.make_childs(ret,pre_targets)

    def param_list(self):
        ret = node()
        ret.root = {"type":"param_list","string":"param_list"}
        child = self.param()
        if child is None:
            return None
        else:
            ret.childs.append(child)
            pre_targets = [",","param"]
            matched = self.match_seq(pre_targets)
            while matched is not None:
                ret.childs.extend(matched)
                matched = self.match_seq(pre_targets)
            return ret

    def param(self):
        ret = node()
        ret.root = {"type":"param","string":"param"}
        pre_targets = [["type_specifier","identifier"],]
        return self.make_childs(ret,pre_targets)

    def local_declarations(self):
        ret = node()
        ret.root = {"type":"local_declarations","string":"local_declarations"}
        pre_targets = ["var_declaration"]
        matched = self.match_seq(pre_targets)
        while matched is not None:
            ret.childs.extend(matched)
            matched = self.match_seq(pre_targets)
        return ret

    def statement_list(self):
        ret = node()
        ret.root = {"type":"statement_list","string":"statement_list"}
        pre_targets = ["statement"]
        matched = self.match_seq(pre_targets)
        while matched is not None:
            ret.childs.extend(matched)
            matched = self.match_seq(pre_targets)
        return ret

    def empty(self):
        return self.wapper({"type":"empty","string":"empty"})

    def statement(self):
        ret = node()
        ret.root = {"type":"statement","string":"statement"}
        pre_targets = [["expression_stmt"],
                     ["compound_stmt"],
                     ["selection_stmt"],
                     ["iteration_stmt"],
                     ["return_stmt"]]
        return self.make_childs(ret,pre_targets)

    def expression_stmt(self):
        ret = node()
        ret.root = {"type":"expression_stmt","string":"expression_stmt"}
        pre_targets = [["expression",";"],]
        return self.make_childs(ret,pre_targets)

    def selection_stmt(self):
        ret = node()
        ret.root = {"type":"selection_stmt","string":"selection_stmt"}
        pre_targets = [["if","(","expression",")","statement","else","statement"],
                    ["if","(","expression",")","statement"]]
        return self.make_childs(ret,pre_targets)

    def iteration_stmt(self):
        ret = node()
        ret.root = {"type":"iteration_stmt","string":"iteration_stmt"}
        pre_targets = [["while","(","expression",")","statement"],]
        return self.make_childs(ret,pre_targets)

    def return_stmt(self):
        ret = node()
        ret.root = {"type":"return_stmt","string":"return_stmt"}
        pre_targets = [["return","expression",";"],
                     ["return",";"]]
        return self.make_childs(ret,pre_targets)

    def expression(self):
        ret = node()
        ret.root = {"type":"expression","string":"expression"}
        pre_targets = [["var","=","expression"],
                     ["simple_expression"],
                     ["empty"]]
        return self.make_childs(ret,pre_targets)

    def var(self):
        ret = node()
        ret.root = {"type":"var","string":"var"}
        pre_targets = [["identifier","[","expression","]"],
                       ["identifier"]]
        return self.make_childs(ret,pre_targets)

    def simple_expression(self):
        ret = node()
        ret.root = {"type":"simple_expression","string":"simple_expression"}
        child = self.additive_expression()
        if child is None:
            return None
        else:
            ret.childs.append(child)
            pre_targets = ["relop","additive_expression"]
            matched = self.match_seq(pre_targets)
            while matched is not None:
                ret.childs.extend(matched)
                matched = self.match_seq(pre_targets)
            return ret

    def additive_expression(self):
        ret = node()
        ret.root = {"type":"additive_expression","string":"additive_expression"}
        child = self.term()
        if child is None:
            return None
        else:
            ret.childs.append(child)
            pre_targets = ["addop","term"]
            matched = self.match_seq(pre_targets)
            while matched is not None:
                ret.childs.extend(matched)
                matched = self.match_seq(pre_targets)
            return ret

    def relop(self):
        ret = node()
        ret.root = {"type":"relop","string":"relop"}
        pre_targets = [["<="],
                     ["<"],
                     [">"],
                     [">="],
                     ["=="],
                     ["!="]]
        return self.make_childs(ret,pre_targets)

    def addop(self):
        ret = node()
        ret.root = {"type":"addop","string":"addop"}
        pre_targets = [["+"],
                     ["-"]]
        return self.make_childs(ret,pre_targets)

    def term(self):
        ret = node()
        ret.root = {"type":"term","string":"term"}
        child = self.factor()
        if child is None:
            return None
        else:
            ret.childs.append(child)
            pre_targets = ["mulop","factor"]
            matched = self.match_seq(pre_targets)
            while matched is not None:
                ret.childs.extend(matched)
                matched = self.match_seq(pre_targets)
            return ret

    def mulop(self):
        ret = node()
        ret.root = {"type":"mulop","string":"mulop"}
        pre_targets = [["*"],
                     ["/"]]
        return self.make_childs(ret,pre_targets)

    def factor(self):
        ret = node()
        ret.root = {"type":"factor","string":"factor"}
        pre_targets = [["(","expression",")"],
                       ["call"],
                       ["var"],
                       ["num"]]
        return self.make_childs(ret,pre_targets)

    def call(self):
        ret = node()
        ret.root = {"type":"call","string":"call"}
        pre_targets = [["identifier","(","args",")"],
                       ]
        return self.make_childs(ret,pre_targets)

    def args(self):
        ret = node()
        ret.root = {"type":"args","string":"args"}
        pre_targets = [["arg_list"],
                     ["empty"]]
        return self.make_childs(ret,pre_targets)

    def arg_list(self):
        ret = node()
        ret.root = {"type":"arg_list","string":"arg_list"}
        child = self.expression()
        if child is None:
            return child
        else:
            
            ret.childs.append(child)
            pre_targets = [",","expression"]
            matched = self.match_seq(pre_targets)
            while matched is not None:
                ret.childs.extend(matched)
                matched = self.match_seq(pre_targets)
            return ret