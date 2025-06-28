import sys
import time
empty = '<>'
eof = 'eof'
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

def getFollowList(firstlist):
    followlist = {}
    for nt in nonterminals:
        followlist[nt] = set()
    followlist[nonterminals[0]] = {eof}

    oldsum = -1
    newsum = 0
    while newsum != oldsum:

        # logic
        for nt in productions:
            for rule in productions[nt]:
                trailer = followlist[nt].copy()
                for i in range(len(rule)-1, -1, -1):
                    if rule[i] in nonterminals:
                        followlist[rule[i]] |= trailer
                        if empty in firstlist[rule[i]]:
                            trailer |= firstlist[rule[i]].difference({empty})
                        else:
                            trailer = firstlist[rule[i]]
                    else:
                        trailer = {rule[i]}
        oldsum = newsum
        newsum = 0
        for f in followlist:
            newsum += len(followlist[f])
    return followlist

def firstForList(firstlist, rule):
    if rule[0] == empty:
        return {empty}

    ans = firstlist[rule[0]].difference({empty})
    i = 0
    while i < len(rule)-1 and empty in firstlist[rule[i]]:
        ans |= (firstlist[rule[i+1]].difference({empty}))
        i += 1
    if i == len(rule)-1 and empty in firstlist[rule[-1]]:
        ans |= {empty}
    return ans

def checkLL1(first, follow):
    for nt in productions:
        # all rules' FIRST+ must be independent
        runningFirst = set()
        for rule in productions[nt]:
            firstplus = firstForList(first, rule)
            if empty in firstForList(first, rule):
                firstplus |= follow[nt]
            
            if not runningFirst.isdisjoint(firstplus):
                return False

            runningFirst |= firstplus
    return True



terminals, nonterminals, productions = processInput(sys.argv[1])


FIRST = getFirstList()
FOLLOW = getFollowList(FIRST)

# now actually check the LL1
print("LL(1):", checkLL1(FIRST, FOLLOW))


