empty = 'ε'

# Objects needed
# terminals - set of terminals
# nonterminals - set of non-terminals
# prods - map of nonterminal to list of terminal/nonterminals
# terminalCanEmpty - set of terminals that can resolve to ε
# terminals = {}
# nonterminals = {}
# terminalCanEmpty = {}
# productions = {}

# examples
terminals = {'A'}
nonterminals = {'ap'}
terminalCanEmpty = {}
productions = {'ap' : [['A', 'ap'], ['a']]}


# determine first set of a list of terminals
def FIRST(termlist):
    if len(termlist) == 0:
        return {empty}
    else:
        first = termlist[0]
        if first in terminals:
            if first in terminalCanEmpty:
                # terminal can be empty, resolve rest
                print("e")
                return ({first} | FIRST(termlist[1:]))
            else:
                return {first}
        elif first in nonterminals:
            if first not in productions:
                print("Unrecognized non-terminal symbol: " + first)
                exit(1)
            ans = {}
            for prodRule in productions[first]:
                ans = ans | FIRST(prodRule)
            if empty in ans:
                return ans | FIRST(termlist[1:])
            else:
                return ans
        else:
            print("Unrecognized symbol in termlist: " + first)
            exit(1)




with open("grammar.arg") as file:
    print(file.read())


print(FIRST(['A', 'ap']))