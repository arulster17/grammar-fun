import sys
import time
empty = '<>'

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
    commentstr = pieces[0]
    print("Comment: ", commentstr)
    terms = pieces[1].split(',')
    nonterms = pieces[2].split(',')
    prodRules = pieces[3].split('\n')
    prods = {}
    for nt in nonterms:
        prods[nt] = []
    for rule in prodRules:
        ruleSymbols = rule.split(' ')
        assert ruleSymbols[0] in nonterms
        assert ruleSymbols[1] == '->'
        if ruleSymbols[2] == empty:
            assert len(ruleSymbols) == 3
            prods[ruleSymbols[0]].append([empty])
            continue
        for sym in ruleSymbols[2:]:
            assert (sym in terms or sym in nonterms)
        prods[ruleSymbols[0]].append(ruleSymbols[2:])

    return terms, nonterms, prods

def FIRST(symbols, seen):
    print("FIRST("+str(symbols)+","+str(seen)+")")
    #time.sleep(2)
    # prevent infinite recursion?
    if symbols[0] in seen:
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
                ans |= FIRST(prod, seen+[sym])
            return ans

    ans = set()
    for symIndex in range(len(symbols)):
        sym = symbols[symIndex]
        if symbols[symIndex] in seen:
            return ans
        curFirst = FIRST([sym], seen)
        ans |= curFirst.difference({empty})
        if not empty in curFirst:
            # we are done here
            return ans
        # else we need to consider the next symbol so continue

    return (ans | {empty})
            


def getFirstList():
    firstlist = {}
    for t in terminals:
        firstlist[t] = {t}
    for n in nonterminals:
        firstlist[n] = set()
    firstlist[empty] = {empty}
    oldsum = -1
    newsum = 0
    while newsum != oldsum:
        print("loop iterating")
        # go again, update oldsum
        oldsum = newsum

        for nt in productions:
            for rule in productions[nt]:
                # rule of the form nt -> something
                ans = firstlist[rule[0]].difference({empty})
                
                i = 0
                while i < len(rule)-1 and empty in firstlist[rule[i]]:
                    ans |= (firstlist[rule[i+1]].difference({empty}))
                    i += 1
                if i == len(rule)-1 and empty in firstlist[rule[-1]]:
                    ans |= {empty}
                firstlist[nt] |= ans

        # compute newsum
        newsum = 0
        for f in firstlist:
            newsum += len(firstlist[f])
    return firstlist

terminals = {'A','B'}
nonterminals = {'a','b'}
productions = {'b' : [['a', 'B'], [empty]],
               'a' : [['A', 'b']]}

terminals, nonterminals, productions = processInput(sys.argv[1])


first = getFirstList()
print(first)
follow = {}

#print(FIRST(['S'], []))
'''
b -> a B
a -> A b
a -> e
'''

