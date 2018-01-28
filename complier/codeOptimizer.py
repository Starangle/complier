import re
from collections import deque


class codeOptimizer:
    def __init__(self, path):
        self.codes = list()
        with open(path, "r") as f:
            lines = f.readlines()
        for line in lines:
            self.codes.append(re.split('[\t\n]', line)[0:4])

    def optimize(self):
        def print_code():
            for code in self.codes:
                for item in code:
                    print(item,end='\t')
                print()
            print("____________Finish____________")
            
        print_code()
        # self.lvn()
        # print_code()
        print("____________SVN____________")
        self.svn()
        print_code()
        print("____________PPA____________")
        self.ppa()
        print_code()
    
    def ppa(self):
        '''process place algorithm # 过程放置算法'''

        #拆分过程块，以供交换顺序的需要
        procs=dict()
        graph=dict()
        
        proc_content=list()
        proc_names=dict()
        proc_name=""
        called_name=""

        for code in self.codes:

            #按过程拆分中间代码,拆分的结果存放到procs中，用代码段名作为下标
            if code[1]==":" and ('@' not in code[0]):
                procs[proc_name]=proc_content
                proc_content=list()
                proc_name=code[0]

                #该节点还没有被使用,记录下程序中出现了多少个过程
                proc_names[proc_name]=0
            proc_content.append(code)
        
        #追加最后一个函数
        procs[proc_name]=proc_content

        #初始化图结构
        for i1 in proc_names:
            graph[i1]=dict()
            for i2 in proc_names:
                graph[i1][i2]=0
        

        proc_name=""
        #构建图
        for code in self.codes:
            if code[1]==":" and ('@' not in code[0]):
                proc_name=code[0]

            #调用频率关系图
            if code[0]=='jumpI' and ('@' not in code[3]):#调用关系的指令

                #无向图
                graph[proc_name][code[3]]+=1
                graph[code[3]][proc_name]+=1
        
        '''
        根据设计，应当将main函数先放到程序起始位置
        '''

        placed_code=list()
        placed_code.append(procs['main'])
        proc_names['main']=1
        placed_count=1
        last='main'

        while placed_count<len(proc_names):
            best_v=-1
            best_k=""
            for k,v in graph[last].items():
                if proc_names[k]==0 and k!=last:#避免重复
                    if v>best_v:
                        best_v=v
                        best_k=k
            
            if best_k=="":
                for k,v in proc_names:
                    if v==0:
                        best_k=k
                        break
            
            placed_code.append(procs[best_k])
            placed_count+=1
            proc_names[best_k]=1
            last=best_k
        
        #用重排的代码替换原来的代码
        code=list()
        for item in placed_code:
            code.extend(item)
        
        self.codes=code

    def svn(self):
        
        
        def next_graph(line_no):

            #设置变量并初始化
            label_rel=dict()
            ret_label_rel=dict()

            if line_no>=len(self.codes):
                return None,None

            now_label=self.codes[line_no][0]
            label_rel[now_label]=list()
            ret_label_rel[now_label]=list()
            line_no+=1

            while line_no<len(self.codes):
                code=self.codes[line_no]
                if code[1]==':':
                    if '@' not in code[0]:
                        break
                    else:
                        now_label=code[0]
                        label_rel[now_label]=list()
                        ret_label_rel[now_label]=list()

                elif code[0]=='cbr':
                    label_rel[now_label].append(code[2])
                    label_rel[now_label].append(code[3])
                elif code[0]=='jumpI':
                    #将函数调用视为算数指令
                    if '@' in code[3]:
                        label_rel[now_label].append(code[3])
                else:
                    pass
                line_no+=1
            
            
            for k,v in label_rel.items():
                for sv in v:
                    ret_label_rel[sv].append(k)

            return ret_label_rel,line_no
        
        def next_svn(line_no,rel,lim):
            #由next_graph函数保证，这里的line_no初始不会越界
            def find_var(vno, ht):
                for k, v in ht.items():
                    if v == vno:
                        return k
                return None

            def make_index(op, v1, v2):
                return str(v1) + op + str(v2)

            now_label=""
            adno=0
            vn=dict()
            ht=dict()
            eht=dict()
            up_code=list()
            while line_no<lim:
                code=self.codes[line_no]
                if code[1] == ':':
                    #遇到新的基本块，保存上一个基本块的值编号情况
                    vn[now_label]=ht,eht

                    #更新当前块名称
                    now_label=code[0]
                    
                    #查询新的基本块是否有唯一前驱，如果有，加载其前驱的值编号情况，否则，重置hash表
                    if len(rel[now_label])==1:
                        ht,eht=vn[rel[now_label][0]]
                    else:
                        ht=dict()
                        eht=dict()

                elif code[0] in ["sub", "add", "mult", "div"]:
                    # 查询值编号，如果不存在就创建值编号
                    vno1 = ht.get(code[1], None)
                    vno2 = ht.get(code[2], None)
                    if vno1 is None:
                        ht[code[1]] = adno
                        adno += 1
                        vno1 = ht[code[1]]
                    if vno2 is None:
                        ht[code[2]] = adno
                        adno += 1
                        vno2 = ht[code[2]]
                    # 查询结果的值编号
                    vno = eht.get(make_index(code[0], vno1, vno2), None)

                    '''允许加法和乘法交换律'''
                    if vno is None:
                        if code[0] in ['add', 'mult']:
                            vno = eht.get(make_index(code[0], vno2, vno1), None)
                    '''允许加法和乘法交换律'''

                    if vno is None:
                        vno = adno
                        adno += 1
                        # 创建结果的值编号，散列运算和结果到已经存在的值编号上
                        ht[code[3]] = vno
                        eht[make_index(code[0], vno1, vno2)] = vno
                    else:
                        # 查询值编号对应的变量名
                        symbol = find_var(vno, ht)
                        if symbol is not None:
                            # 如果该还有变量保持该值，那么修改原来指令为赋值
                            code[0] = "add"
                            code[1] = symbol
                            code[2] = "@zero"
                        # 将解果变量散列到值编号上
                        ht[code[3]] = vno
                
                up_code.append(code)
                line_no+=1
            return up_code,lim

        line_no1=0
        line_no2=0
        codes=list()
        graph,line_no1=next_graph(line_no1)
        while line_no1 is not None:
            code,line_no2=next_svn(line_no2,graph,line_no1)
            codes.extend(code)
            graph,line_no1=next_graph(line_no1)
        self.codes=codes
        

    def lvn(self):
        ht = dict()
        eht = dict()
        up_code=list()
        adno = 0

        def find_var(vno, ht):
            for k, v in ht.items():
                if v == vno:
                    return k
            return None

        def make_index(op, v1, v2):
            return str(v1) + op + str(v2)

        for code in self.codes:
            
            if code[1] == ':':
                # 重置基本块的散列表
                ht = dict()
                eht = dict()

            if code[0] in ["sub", "add", "mult", "div"]:
                # 查询值编号，如果不存在就创建值编号
                vno1 = ht.get(code[1], None)
                vno2 = ht.get(code[2], None)
                if vno1 is None:
                    ht[code[1]] = adno
                    adno += 1
                    vno1 = ht[code[1]]
                if vno2 is None:
                    ht[code[2]] = adno
                    adno += 1
                    vno2 = ht[code[2]]
                # 查询结果的值编号
                vno = eht.get(make_index(code[0], vno1, vno2), None)

                '''允许加法和乘法交换律'''
                if vno is None:
                    if code[0] in ['add', 'mult']:
                        vno = eht.get(make_index(code[0], vno2, vno1), None)
                '''允许加法和乘法交换律'''

                if vno is None:
                    vno = adno
                    adno += 1
                    # 创建结果的值编号，散列运算和结果到已经存在的值编号上
                    ht[code[3]] = vno
                    eht[make_index(code[0], vno1, vno2)] = vno
                else:
                    # 查询值编号对应的变量名
                    symbol = find_var(vno, ht)
                    if symbol is not None:
                        # 如果该还有变量保持该值，那么修改原来指令为赋值
                        code[0] = "add"
                        code[1] = symbol
                        code[2] = "@zero"
                    # 将解果变量散列到值编号上
                    ht[code[3]] = vno
            
            up_code.append(code)
        self.codes=up_code