import re
import nltk

"""
Sentence: The quick brown fox jumped over the lazy dog
Grammar:

S   -> NP VP
NP  -> Det Nom
VP  -> V Adj | V NP | V S | V NP PP | V PP
PP  -> P NP
Nom -> Adj Nom | N
Adj -> 'quick' | 'brown' | 'lazy'
Det -> 'the'
N   -> 'fox' | 'dog'
"""

SHOW_TYPES = False


def _surrounded(s, pattern):
    return s[0:len(pattern)] == pattern and s[len(s) - len(pattern): len(s)] == pattern


class Grammar(object):
    """Class to represent a grammar"""

    def __init__(self, rules=[]):
        self.rules = rules

    def add_rule(self, rule):
        self.rules.append(rule)

    def open_symbols(self):
        open_symbols = []
        for rule in self.rules:
            for symbol in rule.right:
                if not (symbol in open_symbols) and \
                                type(symbol) == Nonterminal and \
                                len(list(filter(lambda e: type(e) == Terminal, self[symbol]))) == 0:
                    open_symbols.append(symbol)

        return open_symbols

    def valid_symbols(self):
        return [rule.left for rule in self.rules]

    def absorb_terminal(self, tagged_word):
        """Absorbs a single tagged terminal
        :param tagged_word: a single tuple of terminal, tag: ('money', 'N')
        """
        word, tag = tagged_word
        self.add_rule(Rule(Nonterminal(tag), (Terminal(word),)))


    def __getitem__(self, item):
        relevant_rules = filter(lambda rule: rule.left.value == item.value, self.rules)
        productions = list(map(lambda rule: rule.right, relevant_rules))
        return productions

    def __str__(self):
        rep = """"""
        for rule in self.rules:
            rep += str(rule) + "\n"
        return rep


class Rule(object):
    """Class to represent production rules"""

    def __init__(self, left, right):
        """
        :param left: a string
        :param right: a tuple representing a production
        """
        self.left = left
        self.right = right

    def __str__(self):
        if SHOW_TYPES:
            return "%s -> %s" % (str(self.left), " ".join(map(str, self.right)))
        return "%s -> %s" % (self.left.value, " ".join(map(lambda x: x.value if type(x) == Nonterminal else "'" + x.value + "'", self.right)))


class Nonterminal(object):
    """Class to represent an non-terminal"""

    def __init__(self, symbol):
        self.value = symbol

    def __str__(self):
        return "Non-terminal( %s )" % self.value

    def __repr__(self):
        return str(self)


class Terminal(object):
    """Class to represent a terminal"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Terminal( %s )" % self.value

    def __repr__(self):
        return str(self)


class Tree(object):
    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        return "Tree ( symbol = {} children = {})".format(self.symbol.value, [str(child) for child in self.children])


def parse_grammar(definition):
    """ Parse the grammar given a grammar definition
    :param definition: the definition of a grammar
    :return: A dictionary representing the grammar
    """

    rules = definition.split("\n")
    grammar = Grammar()

    for x in range(len(rules)):
        rules[x] = rules[x].lstrip().rstrip()
    rules = list(filter(lambda x: x, rules))

    for rule in rules:
        if rule[0] == "#": continue
        assert (re.match("\w*\s*->\s*((\w)*\s)*", rule))
        split_rule = re.split("\s*->\s*", rule)
        key = Nonterminal(split_rule[0])
        values = re.split("\s*\|\s*", split_rule[-1])

        for value in values:
            if not _surrounded(value, "'"):
                production = tuple([Nonterminal(symbol) for symbol in value.split(" ")])
            else:
                production = (Terminal(value.strip("'")),)
            rule = Rule(key, production)
            # print(rule)
            grammar.add_rule(rule)
    return grammar

class NLTKParserHelper:
    """Class to wrap an nltk parser. Contains methods to generate a grammar from pos-tagged
    text.
    """

    # VALID_POS_TAGS = ["N", "V", "NP"]

    def __init__(self, grammar: Grammar, nltk_parser_type=nltk.ChartParser):
        self.nltk_parser_type = nltk_parser_type
        self.nltk_parser = None
        self.grammar = grammar
        self.tagset = [symbol.value for symbol in self.grammar.valid_symbols()]

    def absorb_lexicon(self, tagged_sentence):
        """Absorbs a lexicon from a pos-tagged sentence
        :param tagged_sentence: a list of tuples: [("a", "DET"), ("fox", "N"), ("always", "ADV"), ("lies", "V")]
        """

        for word, tag in tagged_sentence:
            word = "'" + word + "'"
            if tag in self.tagset:
                self.grammar.add_rule(Rule(Nonterminal(tag), (Terminal(word),)))

        self.nltk_parser = self.nltk_parser_type(nltk.CFG.fromstring(str(self.grammar)))

    def parse(self, tokens):
        """Parse a list of tokens; ex: ["the", "fox" , "jumps"]"""
        if len(self.grammar.open_symbols()) == 0:
            raise Exception("Not all symbols in the grammar are closed (not all lead to a Terminal)")
        elif not self.nltk_parser:
            raise Exception("NLTKParserHelper.nltk_parser does not exist")
        return self.nltk_parser.parse(tokens)