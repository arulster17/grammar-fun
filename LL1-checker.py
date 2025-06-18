import sys
import time
empty = 'ε'

# Objects needed
# terminals - set of terminals
# nonterminals - set of non-terminals
# prods - map of nonterminal to list of terminal/nonterminals
# terminals = {}
# nonterminals = {}
# productions = {}

# examples

def processInput(filename):
    with open(filename) as file:
        filetext = file.read()
    pieces = filetext.split("\n>>>\n")
    print(pieces)
    commentstr = pieces[0]
    print("Comment: ", commentstr)
    terms = pieces[1].split(',')
    nonterms = pieces[2].split(',')
    prodRules = pieces[3].split('\n')
    prods = {}
    for rule in prodRules:
        ruleSymbols = rule.split(' ')
        

    return terms, nonterms, prods

def FIRST(symbols, initialNT):
    # prevent infinite recursion?
    if symbols[0] == initialNT:
        return set()
    if len(symbols) == 1:
        sym = symbols[0]
        if sym == empty:
            return {sym}
        if sym in terminals:
            return {sym}
        if sym in nonterminals:
            ans = set()
            for prod in productions[sym]:
                ans = ans | FIRST(prod, sym)
            return ans

    ans = set()
    for symIndex in range(len(symbols)):
        sym = symbols[symIndex]
        if symbols[symIndex] == initialNT:
            return ans
        curFirst = FIRST(sym, initialNT)
        hasE = empty in curFirst
        print("CURFIRST: " + str(curFirst))
        ans = ans | curFirst.difference({empty})
        print("ans: " + str(ans))
        if not empty in curFirst:
            # we are done here
            return ans
        # else we need to consider the next symbol so continue

    return (ans | empty)
            




terminals, nonterminals, productions = processInput(sys.argv[1])

terminals = {'A','B'}
nonterminals = {'a','b'}
productions = {'b' : [['a', 'B'], [empty]],
               'a' : [['A', 'b']]}

print(FIRST(['b'], None))


'''
b -> a B
a -> A b
a -> e
'''