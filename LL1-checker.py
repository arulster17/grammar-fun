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
    print(prodRules)
    prods = {}
    for nt in nonterms:
        prods[nt] = []
    for rule in prodRules:
        if rule == '':
            continue
        ruleSymbols = rule.split(' ')
        assert ruleSymbols[0] in nonterms
        assert ruleSymbols[1] == '->'

        # example format: A -> a C | b A B
        
        subrulesString = " ".join(ruleSymbols[2:])
        # subrulesString = "a C | b A B"
        subrules = subrulesString.split(" | ")
        # subrules = ["a c", "b A B"]
        for subrulestr in subrules:
            subrule = subrulestr.split(" ") 
            if subrule[0] == empty:
                assert len(subrule) == 1
                prods[ruleSymbols[0]].append([empty])
                continue
            for sym in subrule:
                assert sym in terms or sym in nonterms
            prods[ruleSymbols[0]].append(subrule)

    return terms, nonterms, prods

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

for term in first:
    print(term + ": " + str(first[term]))



follow = {}

#print(FIRST(['S'], []))
'''
b -> a B
a -> A b
a -> e
'''

