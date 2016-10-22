from grammar_parser import *

GANTT_GRAMMAR = """
S -> CC
CC -> NP VP | CC Conj CC | SC CC | CC SC
SC -> SConj CC
PP -> P NP
NP -> Det N | Det N PP | N
VP -> V NP | V PP | VP Conj VP

V -> 'shot' | 'wore' | 'mow' | 'do' | 'watch' | 'fly' | 'run' | 'go' | 'visit' | 'give'

Det -> 'an' | 'my' | 'the' | 'a'
Conj -> 'and' | 'or'
SConj -> 'while' | 'before' | 'after' | 'if'

N -> N N | N Ger| N Ger PP | 'lawn' | 'I' | 'i' | 'laundry' | 'bats' | 'them' | 'lake' | 'store' | 'movie' | 'Charlie' | 'him' | 'gift' | 'me'
Ger -> 'fly'
HV -> 'must' | 'can'
P -> 'in' | 'like' | 'to' | 'around'
"""


def imbibe(g, path, tag):
    with open(path) as f:
        for line in f:
            if line.strip("\n ").isalpha():
                g.absorb_terminal((line.strip("\n ").lower(), tag))


def improve_grammar(g):
    imbibe(g, "pos-files/nouns/91K nouns.txt", "N")
    imbibe(g, "pos-files/verbs/31K verbs.txt", "V")
    imbibe(g, "pos-files/adverbs/6K adverbs.txt", "Adv")
    imbibe(g, "pos-files/adjectives/28K adjectives.txt", "Adj")


def main():
    g = parse_grammar(GANTT_GRAMMAR)

    with open("pos-files/nouns/91K nouns.txt") as f:
        for line in f:
            g.absorb_terminal((line.strip("\n\s"), "N"))

    with open("pos-files/verbs/31K verbs.txt") as f:
        for line in f:
            g.absorb_terminal((line.strip("\n\s"), "V"))

    with open("pos-files/verbs/31K verbs.txt") as f:
        for line in f:
            g.absorb_terminal((line.strip("\n\s"), "V"))

    print(g)


if __name__ == '__main__':
    main()
