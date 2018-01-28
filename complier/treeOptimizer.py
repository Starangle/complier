from irc import irc


class treeOptimizer(irc):
    def __init__(self, sem_obj):
        irc.__init__(self, sem_obj)

    # def generate(self):
    #     print("这是优化的代码生成器")

    def generate(self):
        self.out = open(r'result\treeOptimizeCode.txt', "w+")
        getattr(self, self.sem.syn.root.root["type"])(self.sem.syn.root)
        self.out.close()

    def additive_expression(self, node):
        return self.bal_tree(node)

    def term(self, node):
        return self.bal_tree(node)

    def bal_tree(self, node):
        '''模拟树高平衡'''

        # 只有可交换和可结合的运算才可以进行并行计算
        var_text_list = list()
        op_text_list = list()
        for i in range(len(node.childs)):
            text = getattr(self, node.childs[i].root['type'])(node.childs[i])
            if i % 2 == 0:
                var_text_list.append(text)
            else:
                op_text_list.append(text)

        can_bal=True
        for item in op_text_list:
            if item not in ["mult","add"]:
                can_bal=False
                break

        if can_bal==False:
            if node.root['type']=='term':
                return irc.term(self,node);
            elif node.root['type']=='additive_expression':
                return irc.additive_expression(self,node)
            else:
                pass

        while len(var_text_list) != 1:
            next_level_op = list()
            next_level_var = list()
            assert len(var_text_list) == len(op_text_list) + 1
            it = 0
            max_it = len(var_text_list) - 1
            while it <= max_it:
                if it < max_it:
                    ass_text = self.next_var_name()
                    print("%s\t%s\t%s\t%s" % (
                        op_text_list[it], var_text_list[it], var_text_list[it + 1], ass_text), file=self.out)
                    if it != max_it - 1:
                        next_level_op.append(op_text_list[it + 1])
                    next_level_var.append(ass_text)
                    it += 2
                else:
                    next_level_var.append(var_text_list[it])
                    it += 2

            var_text_list = next_level_var
            op_text_list = next_level_op

        return var_text_list[0]
