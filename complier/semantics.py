class semantics:
    def __init__(self, syn):
        self.syn = syn
        self.now_func = None
        pass

    def dfs_tree(self,node):
        self.set_env_fun(node)

        for child in node.childs:
            self.dfs_tree(child)

        ignore_keywords=["int","(",")","<=",">=",",",";","[","]",
                         "void","else","!=","==",">","<","{","}",
                         "=","+","-","*","/","if","while","return",
                         'identifier']

        if node.root["type"] not in ignore_keywords:
            getattr(self,node.root["type"])(node)


    def program(self,node):
        pass

    def declaration_list(self,node):
        pass

    def declaration(self,node):
        pass

    def var_declaration(self,node):
        pass

    def type_specifier(self,node):
        pass

    def fun_declaration(self,node):
        pass

    def params(self,node):
        pass

    def param_list(self,node):
        pass

    def param(self,node):
        pass

    def compound_stmt(self,node):
        pass

    def local_declarations(self,node):
        pass

    def statement_list(self,node):
        pass

    def statement(self,node):
        pass

    def expression_stmt(self,node):
        pass

    def selection_stmt(self,node):
        '''检查选择的条件语句的条件是否是bool型'''
        if node.childs[2].exp_type != "bool":
            print("error : the type of expression about 'if' must be bool")
        pass

    def iteration_stmt(self,node):
        '''检查选择的循环语句的条件是否是bool型'''
        if node.childs[2].exp_type != "bool":
            print("error : the type of expression about 'while' must be bool")
        pass

    def return_stmt(self,node):
        '''检查函数中出现的返回值类型是否正确'''
        if self.now_func.fun_type == "void":
            if len(node.childs) != 2:
                if node.childs[1].childs[0].root['type']!='empty':
                    print("error : the function %s should return %s ,but it returned %s" % 
                        (self.now_func.name,"void",node.childs[1].exp_type))
        pass
    
    def empty(self,node):
        pass

    def var(self,node):
        '''判定变量是否在符号表中以及数组下标的类型'''
        this_var = self.find_var(node.childs[0].root["string"])
        if this_var is not None:
            node.exp_type = this_var.var_type
        else:
            print("error : variable '%s' is not defined!" % node.childs[0].root["string"])
            exit(0)

        #如果是数组，检查数组下标是否为整数
        if len(node.childs) == 4:
            if node.childs[2].exp_type != "int":
                print("error : the index must be integer!")

    def expression(self,node):
        '''计算表达式类型'''
        if len(node.childs) == 1:
            if node.childs[0].root['type']=='empty':
                return
            node.exp_type = node.childs[0].exp_type
        else:
            node.exp_type = node.childs[2].exp_type
            # if node.childs[0].exp_type != node.childs[2].exp_type:
            #     print("error : type cast must be used specifically in assignment statement!")

    def simple_expression(self,node):
        '''计算表达式类型'''
        #长度大于1的simple_expression一定是bool型
        if len(node.childs) != 1:
            node.exp_type = "bool"
        else:
            node.exp_type = node.childs[0].exp_type
        pass

    def relop(self,node):
        pass

    def additive_expression(self,node):
        '''计算表达式类型'''
        #可和表达式的类型由所有由relop连接的项目决定
        node.exp_type = node.childs[0].exp_type
        index = 2
        max_index = len(node.childs)
        while index < max_index:
            node.exp_type = self.type_cast(node.exp_type,node.childs[index].exp_type)
            index+=2
        pass

    def addop(self,node):
        pass

    def term(self,node):
        #term表达式的类型有所有由mulop连接的项目决定
        node.exp_type = node.childs[0].exp_type
        index = 2
        max_index = len(node.childs)
        while index < max_index:
            node.exp_type = self.type_cast(node.exp_type,node.childs[index].exp_type)
            index+=2
        pass

    def mulop(self,node):
        pass

    def factor(self,node):
        if len(node.childs) == 3:
            node.exp_type = node.childs[1].exp_type
        else:
            node.exp_type = node.childs[0].exp_type
        pass

    def call(self,node):
        #查找fun的定义，用函数类型作为该节点的计算类型
        this_fun = self.find_fun(node.childs[0].root["string"])
        if this_fun is not None:
            node.exp_type = this_fun.fun_type
        else:
            print("error : function %s is not defined!" % node.childs[0].root["string"])
        #检查参数个数与类型是否与函数定义一致
        args_node=node.childs[2].childs[0]
        called_fun=self.find_fun(node.childs[0].root["string"])
        if args_node.childs[0].childs[0].root["type"]=="empty":
            if called_fun is not None:
                print("error : the function need %d args, but the call given 0 args" %
                      len(called_fun.params))
        else:
            given_types=list()
            index=0
            while index<len(args_node.childs):
                given_types.append(args_node.childs[index].exp_type)
                index+=2

            if given_types!=called_fun.params:
                print("error : the function %s need ["% called_fun.name,end="")
                for arg_type in called_fun.params:
                    print(arg_type,end=",")
                print("], but the call given [",end="")
                for arg_type in given_types:
                    print(arg_type,end=",")
                print("]") 
        pass

    def num(self,node):
        #假设只有int常量
        node.exp_type = "int"
        pass

    def args(self,node):
        pass

    def arg_list(self,node):
        pass

    def identifier(self,node):
        pass

    def find_var(self,name):
        symbols = self.syn.symbols
        for symbol in symbols:
            if symbol.name == name and symbol.type == "var":
                return symbol
        return None

    def find_fun(self,name):
        symbols = self.syn.symbols
        for symbol in symbols:
            if symbol.name == name and symbol.type == "fun":
                return symbol
        return none

    def check_symbols_table(self):
        #检查是否有被声明为空的变量
        symbols = self.syn.symbols
        for symbol in symbols:
            if symbol.type == "var":
                if symbol.var_type == "void":
                    print("error : the type of variable %s can't be void" % symbol.name)
        pass

    def type_cast(self,type_a,type_b):
        if "float" in [type_a,type_b]:
            return "float"
        if "int" in [type_a,type_b]:
            return "int"
        return None

    def set_env_fun(self,node):
        if node.root["type"] == "fun_declaration":
            symbols = self.syn.symbols
            for symbol in symbols:
                if symbol.name == node.childs[1].root["string"] and symbol.type == "fun":
                    self.now_func = symbol

    def check(self):
        self.check_symbols_table()
        self.dfs_tree(self.syn.root)