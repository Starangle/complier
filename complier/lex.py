class lex:
    def __init__(self,source_file):
        self.tokens = list()
        self.iterator = 0
        self.source = open(source_file).read()
        self.max_iter = len(self.source)
        
        token=self.next_token()
        while token is not None:
            self.tokens.append(token)
            token=self.next_token()
        
    def next_token(self):
        """
        state:
        -2  error
        -1  end
        0   begin
        1   num
        2   identifier
        3   int
        4   float*
        5   double*
        7   if
        8   else
        9   while
        10  return
        11  void
        """
        state = 0
        item = ""
        while(True):
            isend = self.iterator >= self.max_iter
            if not isend:
                ch = self.source[self.iterator]
            else:
                ch = None

            if state == -2:
                self.iterator = self.iterator - 1
                return {"type":"error","string":"error"}
            elif state == 0:
                if ch is None:
                    return None
                elif ch.isalpha() or ch == '_':
                    item = item + ch
                    state = 107
                elif ch=='{':
                    item=item+ch
                    state=108
                elif ch=='}':
                    item=item+ch
                    state=109
                elif ch=='(':
                    item=item+ch
                    state=110
                elif ch==')':
                    item=item+ch
                    state=111
                elif ch=='+':
                    item=item+ch
                    state=112
                elif ch=='-':
                    item=item+ch
                    state=113
                elif ch=='*':
                    item=item+ch
                    state=114
                elif ch=='/':
                    item=item+ch
                    state=115
                elif ch=='>':
                    item=item+ch
                    state=116
                elif ch=='<':
                    item=item+ch
                    state=117
                elif ch=='=':
                    item=item+ch
                    state=118
                elif ch==';':
                    item=item+ch
                    state=122
                elif ch==',':
                    item=item+ch
                    state=127
                elif ch=='!':
                    item=item+ch
                    state=128
                elif ch=='[':
                    item=item+ch
                    state=130
                elif ch==']':
                    item=item+ch
                    state=131
                elif ch == '.':
                    item = item + ch
                    state = 106
                elif ch.isdigit():
                    item = item + ch
                    state = 101
                else:
                    state = 0
                    item = ""
            elif state == 1:
                self.iterator = self.iterator - 1
                return {"type":"num","string":item}
            elif state == 2:
                self.iterator = self.iterator - 1
                if item == "if":
                    return {"type":"if","string":"if"}
                elif item == "else":
                    return {"type":"else","string":"else"}
                elif item == "while":
                    return {"type":"while","string":"while"}
                elif item == "return":
                    return {"type":"return","string":"return"}
                elif item == "void":
                    return {"type":"void","string":"void"}
                elif item == "int":
                    return {"type":"int","string":"int"}
                else:
                    return {"type":"identifier","string":item}
            elif state == 101:
                if ch is None:
                    state = 1
                elif ch.isdigit():
                    item = item + ch
                    state = 101
                elif ch == '.':
                    item = item + ch
                    state = 102
                elif ch == 'e' or ch == 'E':
                    item = item + ch
                    state = 103
                else:
                    state = 1
            elif state == 102:
                if ch is None:
                    state = 1
                elif ch.isdigit():
                    item = item + ch
                    state = 102
                elif ch == 'E' or ch == 'e':
                    item = item + ch
                    state = 103
                else:
                    state = 1
            elif state == 103:
                if ch is None:
                    state = -2
                elif ch == '+' or ch == '-':
                    item = item + ch
                    state = 104
                elif ch.isdigit():
                    item = item + ch
                    state = 105
                else:
                    state = -2
            elif state == 104:
                if ch is None:
                    state = -2
                elif ch.isdigit():
                    item = item + ch
                    state = 105
                else:
                    state = -2
            elif state == 105:
                if ch is None:
                    state = 1
                elif ch.isdigit():
                    item = item + ch
                    state = 105
                else:
                    state = 1
            elif state == 106:
                if ch is None:
                    state = -2
                elif ch.isdigit():
                    item = item + ch
                    state = 102
                else:
                    state = -2
            elif state == 107:
                if ch is None:
                    state = 2
                elif ch.isdigit() or ch.isalpha() or ch == '_':
                    item = item + ch
                    state = 107
                else:
                    state = 2
            elif state==108:
                return {"type":"{","string":"{"}
            elif state==109:
                return {"type":"}","string":"}"}
            elif state==110:
                return {"type":"(","string":"("}
            elif state==111:
                return {"type":")","string":")"}
            elif state==112:
                if ch is None:
                    return {"type":"+","string":"+"}
                elif ch=='=':
                    item+='='
                    state=125
                else:
                    return {"type":"+","string":"+"}
            elif state==113:
                if ch is None:
                    return {"type":"-","string":"-"}
                elif ch=='=':
                    item+='='
                    state=126
                else:
                    return {"type":"-","string":"-"}
            elif state==114:
                if ch is None:
                    return {"type":"*","string":"*"}
                elif ch=='=':
                    item+='='
                    state=123
                else:
                    return {"type":"*","string":"*"}
            elif state==115:
                if ch is None:
                    return {"type":"/","string":"/"}
                elif ch=='=':
                    item+='='
                    state=124
                else:
                    return {"type":"/","string":"/"}
            elif state==116:
                if ch is None:
                    return {"type":">","string":">"}
                elif ch=='=':
                    item+='='
                    state=119
                else:
                    return {"type":">","string":">"}
            elif state==117:
                if ch is None:
                    return {"type":"<","string":"<"}
                elif ch=='=':
                    item+='='
                    state=120
                else:
                    return {"type":"<","string":"<"}
            elif state==118:
                if ch is None:
                    return {"type":"=","string":"="}
                elif ch=='=':
                    item+='='
                    state=121
                else:
                    return {"type":"=","string":"="}
            elif state==119:
                return {"type":">=","string":">="}
            elif state==120:
                return {"type":"<=","string":"<="}
            elif state==121:
                return {"type":"==","string":"=="}
            elif state==122:
                return {"type":";","string":";"}
            elif state==123:
                return {"type":"*=","string":"*="}
            elif state==124:
                return {"type":"/=","string":"/="}
            elif state==125:
                return {"type":"+=","string":"+="}
            elif state==126:
                return {"type":"-=","string":"-="}
            elif state==127:
                return {"type":",","string":","}
            elif state==128:
                if ch is None:
                    return {"type":"!","string":"!"}
                elif ch=='=':
                    item+=ch
                    state=129
                else:
                    return {"type":"!","string":"!"}
            elif state==129:
                return {"type":"!=","string":"!="}
            elif state==130:
                return {"type":"[","string":"["}
            elif state==131:
                return {"type":"]","string":"]"}
            else:
                state = -2
            self.iterator = self.iterator + 1

    def test(self):
        i=0
        for token in self.tokens:
            print(str(i)+"\t"+str(token))
            i+=1