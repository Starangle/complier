import re
from lex import lex
from syn import syn
from semantics import semantics
from irc import irc
from treeOptimizer import treeOptimizer
from codeOptimizer import codeOptimizer

def print_line():
    print('--------------------------------------------------')

if __name__ == '__main__':

    print('Complier Start')

    print('Lex')
    print_line()
    
    lex_obj = lex('test/case_09.txt')
    lex_obj.test()

    print('\nSyn')
    print_line()
    syn_obj = syn(lex_obj)
    syn_obj.build()
    syn_obj.test()

    print('\nSemantics')
    print_line()
    semantics_obj=semantics(syn_obj)
    semantics_obj.check()

    print('\nIrGenerate')
    print_line()
    irc_obj=irc(semantics_obj)
    irc_obj.generate()

    print('\nTreeOptimizer')
    print_line()
    topt_obj=treeOptimizer(semantics_obj)
    topt_obj.generate()

    print('\nCodeOptimizer')
    print_line()
    copt_obj=codeOptimizer(r"result\treeOptimizeCode.txt")
    copt_obj.optimize()
