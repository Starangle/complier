class irc:

    '''对函数调用的处理，采用顺序压栈，逆序出栈的方式  ?使用队列是不是更方便'''

    def __init__(self, sem):
        self.sem = sem
        self.var_name_no = 0
        self.label_name_no = 0
        

    def generate(self):
        self.out=open(r'result\code.txt',"w+")
        getattr(self, self.sem.syn.root.root["type"])(self.sem.syn.root)
        self.out.close()

    def program(self, node):
        for child in node.childs:
            getattr(self, child.root['type'])(child)

    def declaration_list(self, node):
        for child in node.childs:
            getattr(self, child.root['type'])(child)

    def declaration(self, node):
        for child in node.childs:
            getattr(self, child.root['type'])(child)

    def var_declaration(self, node):
        '''变量声明暂时对产生四元式无影响,这里不做处理'''
        pass

    def type_specifier(self, node):
        '''变量声明暂时对产生四元式无影响,这里不做处理'''
        pass

    def fun_declaration(self, node):
        fun_label = getattr(self, node.childs[1].root['type'])(node.childs[1])
        print("%s\t%s\t%s\t%s" % (fun_label, ":", "", ""),file=self.out)
        getattr(self, node.childs[3].root['type'])(node.childs[3])
        getattr(self, node.childs[5].root['type'])(node.childs[5])

    def params(self, node):
        if node.childs[0].root['type'] == 'void':
            pass
        else:
            getattr(self, node.childs[0].root['type'])(node.childs[0])

    def param_list(self, node):
        # 这里控制参数的逆序出栈
        length = len(node.childs)
        for index in range(length):
            ti = length - 1 - index  # 真正索引的下标
            if node.childs[ti].root['type'] == 'param':
                getattr(self, node.childs[ti].root['type'])(node.childs[ti])

    def param(self, node):
        var_text = getattr(self, node.childs[1].root['type'])(node.childs[1])
        print("%s\t%s\t%s\t%s" % ("subI", "@sp", "4", "@sp"),file=self.out)
        print("%s\t%s\t%s\t%s" % ("load", "", "@sp", var_text),file=self.out)

    def num(self, node):
        var_text = self.next_var_name()
        print("%s\t%s\t%s\t%s" % ("loadI", "", node.root['string'], var_text),file=self.out)
        return var_text

    def compound_stmt(self, node):
        getattr(self, node.childs[2].root['type'])(node.childs[2])

    def local_declarations(self):
        '''变量声明暂时对产生四元式无影响,这里不做处理'''
        pass

    def statement_list(self, node):
        for child in node.childs:
            getattr(self, child.root['type'])(child)

    def statement(self, node):
        for child in node.childs:
            getattr(self, child.root['type'])(child)

    def expression_stmt(self, node):
        getattr(self, node.childs[0].root['type'])(node.childs[0])

    def selection_stmt(self, node):
        true_label = self.next_label_name()
        false_label = self.next_label_name()
        break_label = self.next_label_name()

        var1_text = getattr(self, node.childs[2].root['type'])(node.childs[2])
        # 根据条件表达式的值跳转
        print("%s\t%s\t%s\t%s" % ("cbr", var1_text, true_label, false_label),file=self.out)

        # true_label的内容
        print("%s\t%s\t%s\t%s" % (true_label, ":", "", ""),file=self.out)
        var2_text = getattr(self, node.childs[4].root['type'])(node.childs[4])
        print("%s\t%s\t%s\t%s" % ("jumpI", "", "",break_label),file=self.out)

        print("%s\t%s\t%s\t%s" % (false_label, ":", "", ""),file=self.out)
        if len(node.childs) == 7:
            # false_label的内容
            var3_text = getattr(
                self, node.childs[6].root['type'])(node.childs[6])
        print("%s\t%s\t%s\t%s" % ("jumpI", "", "", break_label),file=self.out)

        print("%s\t%s\t%s\t%s" % (break_label, ":", "", ""),file=self.out)

    def iteration_stmt(self, node):
        condition_label = self.next_label_name()
        while_label = self.next_label_name()
        break_label = self.next_label_name()

        print("%s\t%s\t%s\t%s" % (condition_label, ":", "", ""),file=self.out)
        var1_text = getattr(self, node.childs[2].root['type'])(node.childs[2])

        # 决定是否跳转
        print("%s\t%s\t%s\t%s" %
              ("cbr", var1_text, while_label, break_label),file=self.out)

        # 循环体的内容
        print("%s\t%s\t%s\t%s" % (while_label, ":", "", ""),file=self.out)
        var2_text = getattr(self, node.childs[4].root['type'])(node.childs[4])
        print("%s\t%s\t%s\t%s" % ("jump", condition_label, "", ""),file=self.out)

        # 退出循环
        print("%s\t%s\t%s\t%s" % (break_label, ":", "", ""),file=self.out)

    def return_stmt(self, node):
        ret_address = self.next_var_name()
        print("%s\t%s\t%s\t%s" % ("subI", "@sp", "4", "@sp"),file=self.out)
        print("%s\t%s\t%s\t%s" % ("load", "", "@sp", ret_address),file=self.out)
        if len(node.childs) == 3:
            var_text = getattr(
                self, node.childs[1].root['type'])(node.childs[1])

            print("%s\t%s\t%s\t%s" % ("store", "", var_text, "@sp"),file=self.out)
            print("%s\t%s\t%s\t%s" % ("addI", "@sp", "4", "@sp"),file=self.out)
        else:
            print("%s\t%s\t%s\t%s" % ("store", "", "@zero", "@sp"),file=self.out)
            print("%s\t%s\t%s\t%s" % ("addI", "@sp", "4", "@sp"),file=self.out)
        print("%s\t%s\t%s\t%s" % ("jump", "", "", ret_address),file=self.out)

    def expression(self, node):
        if len(node.childs) == 3:
            var_text = getattr(
                self, node.childs[2].root['type'])(node.childs[2])
            ass_text = getattr(
                self, node.childs[0].root['type'])(node.childs[0])
            print("%s\t%s\t%s\t%s" % ("add", var_text, "@zero", ass_text),file=self.out)
        else:
            ass_text = getattr(
                self, node.childs[0].root['type'])(node.childs[0])
        return ass_text

    def var(self, node):
        return getattr(self, node.childs[0].root['type'])(node.childs[0])

    def simple_expression(self, node):
        var1_text = getattr(self, node.childs[0].root['type'])(node.childs[0])
        for i in range(1, int(len(node.childs) / 2) + 1):
            index = i * 2
            op_text = getattr(
                self, node.childs[index - 1].root['type'])(node.childs[index - 1])
            var2_text = getattr(self, node.childs[index].root['type'])(
                node.childs[index])
            ass_text = self.next_var_name()
            # 输出三地址码
            print("%s\t%s\t%s\t%s" % (op_text, var1_text, var2_text, ass_text),file=self.out)

            # 设置下一次的变量名称
            var1_text = ass_text

        return var1_text

    def relop(self, node):
        op = node.childs[0].root['type']
        if op == '>':
            return 'cmp_GT'
        elif op == '<':
            return 'cmp_LT'
        elif op == '>=':
            return 'cmp_GE'
        elif op == '<=':
            return 'cmp_LE'
        elif op == '==':
            return 'cmp_EQ'
        else:
            # 只可能是不等号
            return 'cmp_NE'

    def additive_expression(self, node):
        var1_text = getattr(self, node.childs[0].root['type'])(node.childs[0])
        for i in range(1, int(len(node.childs) / 2) + 1):
            index = i * 2
            op_text = getattr(
                self, node.childs[index - 1].root['type'])(node.childs[index - 1])
            var2_text = getattr(self, node.childs[index].root['type'])(
                node.childs[index])
            ass_text = self.next_var_name()
            # 输出三地址码
            print("%s\t%s\t%s\t%s" % (op_text, var1_text, var2_text, ass_text),file=self.out)

            # 设置下一次的变量名称
            var1_text = ass_text
        return var1_text

    def addop(self, node):
        op = node.childs[0].root['type']
        if op == '+':
            return 'add'
        else:
            # 只可能是减号
            return 'sub'

    def term(self, node):
        var1_text = getattr(self, node.childs[0].root['type'])(node.childs[0])
        for i in range(1, int(len(node.childs) / 2) + 1):
            index = i * 2
            op_text = getattr(
                self, node.childs[index - 1].root['type'])(node.childs[index - 1])
            var2_text = getattr(self, node.childs[index].root['type'])(
                node.childs[index])
            ass_text = self.next_var_name()
            # 输出三地址码
            print("%s\t%s\t%s\t%s" % (op_text, var1_text, var2_text, ass_text),file=self.out)

            # 设置下一次的变量名称
            var1_text = ass_text
        return var1_text

    def mulop(self, node):
        op = node.childs[0].root['type']
        if op == '*':
            return 'mult'
        else:
            # 只可能是除号
            return 'div'

    def factor(self, node):
        if len(node.childs) == 3:
            return getattr(self, node.childs[1].root['type'])(node.childs[1])
        else:
            return getattr(self, node.childs[0].root['type'])(node.childs[0])

    def identifier(self, node):
        return node.root['string']

    def call(self, node):
        
        ret_address=self.next_var_name()
        print("%s\t%s\t%s\t%s" % ("addI", "@pc", "4", ret_address),file=self.out) 
        print("%s\t%s\t%s\t%s" % ("store", "", "@sp", ret_address),file=self.out)
        print("%s\t%s\t%s\t%s" % ("addI", "@sp", "4", "@sp"),file=self.out)
        getattr(self, node.childs[2].root['type'])(node.childs[2])

        call_name = getattr(self, node.childs[0].root['type'])(node.childs[0])
        # 输出三地址码
        print("%s\t%s\t%s\t%s" % ("jumpI", "", "", call_name),file=self.out)

        # 取出运算结果
        var_text = self.next_var_name()
        print("%s\t%s\t%s\t%s" % ("subI", "@sp", "4", "@sp"),file=self.out)
        print("%s\t%s\t%s\t%s" % ("load", "", "@sp", var_text),file=self.out)
        return var_text

    def args(self, node):
        if node.root['type'] == 'empty':
            pass
        else:
            getattr(self, node.childs[0].root['type'])(node.childs[0])

    def arg_list(self, node):
        for i in range(0, int(len(node.childs) / 2) + 1):
            index = i * 2
            var_text = getattr(self, node.childs[index].root['type'])(
                node.childs[index])

            # 输出三地址码,将参数压栈
            print("%s\t%s\t%s\t%s" % ("store", "", var_text, "@sp"),file=self.out)
            print("%s\t%s\t%s\t%s" % ("addI", "@sp", "4", "@sp"),file=self.out)

    def empty(self,node):
        pass

    def next_var_name(self):
        '''产生一个临时变量名称,使用@符号避免和用户名称冲突'''
        self.var_name_no += 1
        return "var@" + str(self.var_name_no)

    def next_label_name(self):
        '''产生一个label以供跳转,使用@符号避免和用户名称冲突'''
        self.label_name_no += 1
        return "label@" + str(self.label_name_no)
