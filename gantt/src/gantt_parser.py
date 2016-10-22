import nltk
from grammar_parser import *
import string
import nltk
from improvements import *



OLD_GRAMMAR = """
S -> CC
CC -> NP VP | CC Conj CC | SC CC | CC SC
SC -> SConj CC
PP -> P NP
NP -> Det N | Det N PP | 'I'
VP -> V NP | VP PP | VP Conj VP
Det -> 'an' | 'my'
Conj -> 'and' | 'or'
SConj -> 'while' | 'before'
N -> 'elephant' | 'pajamas'
V -> 'shot' | 'wore'
P -> 'in'
"""

IMPROVED_GANTT_GRAMMAR = GANTT_GRAMMAR = """
S -> CC
CC -> NP VP | CC Conj CC | SC CC | CC SC
SC -> SConj CC
PP -> P NP
NP -> Det N | Det N PP | N | N PP | NP Conj NP
VP -> V NP | V PP | VP Conj VP | V

V -> 'shot' | 'wore' | 'mow' | 'do' | 'watch' | 'fly' | 'run' | 'go' | 'visit' | 'give'

Det -> 'an' | 'my' | 'the' | 'a'
Conj -> 'and' | 'or'
SConj -> 'while' | 'before' | 'after' | 'if'

N -> N Ger| N Ger PP | 'lawn' | 'I' | 'i' | 'laundry' | 'bats' | 'them' | 'lake' | 'store' | 'movie' | 'Charlie' | 'him' | 'gift' | 'me' | 'work'
Ger -> 'fly' | N
HV -> 'must' | 'can'
P -> 'in' | 'like' | 'to' | 'around' | 'at'
"""

GANTT_GRAMMAR = """
S -> CC
CC -> NP VP | CC Conj CC | SC CC | CC SC
SC -> SConj CC
PP -> P NP
NP -> Det N | Det N PP | N | N PP | NP Conj NP
VP -> V NP | V PP | VP Conj VP | V

V -> 'shot' | 'wore' | 'mow' | 'do' | 'watch' | 'fly' | 'run' | 'go' | 'visit' | 'give'

Det -> 'an' | 'my' | 'the' | 'a'
Conj -> 'and' | 'or'
SConj -> 'while' | 'before' | 'after' | 'if'

N -> N Ger| N Ger PP | 'lawn' | 'I' | 'i' | 'laundry' | 'bats' | 'them' | 'lake' | 'store' | 'movie' | 'Charlie' | 'him' | 'gift' | 'me' | 'work'
Ger -> 'fly'
HV -> 'must' | 'can'
P -> 'in' | 'like' | 'to' | 'around' | 'at'
"""


class Task:
    def __init__(self, desc, priority):
        self.desc = desc
        self.priority = priority
    def __eq__(self, other):
        print("desc" + self.desc)
        i = 0
        words = nltk.word_tokenize(self.desc)
        for word in words:
            if word in other.desc: i += 1
        return i > len(words) / 2

    def __str__(self):
        return "Task( " + self.desc + ", " + str(self.priority) + " )"


def draw_span(text):
    return """
    <span class="box">
        {}
    </span>
    """.format(text)

def indexOf(tree, symbol):
    for i, element in enumerate(tree):
        if element._label == symbol:
            return i, element

    return -1

def draw_div(text):
    return """
    <div class="level">
        {}
    </div>
    """.format(text)

def draw_ul(l):
    s = """
    <ul>
    """
    for e in l:
        s += "<li>" + e + "</li>"

    s += "</ul>"
    return s


def collapse(cc):
    clauses = []
    # print(cc)
    if cc._label == "CC":
        if len(cc) == 3 and cc[1]._label == "Conj":
            for entity in cc:
                if entity._label == "CC":
                    clauses.append(collapse(entity))
        else:
            clauses.append(cc)

    elif cc._label == "VP":
        # print(clauses)
        if len(cc) == 3 and cc[1]._label == "Conj":
            for entity in cc:
                if entity._label == "VP":
                    clauses.append(collapse(entity))
        else:
            clauses.append(cc)

    return clauses

def search(tasks, desc):
    for i, task in enumerate(tasks):
        if task == Task(desc, 0):
            return i, task

    return -1


def find_verb_phrases(tree, tasks=[]):
    for clause in tree:
            # print(clause)
            if clause[0]._label == "SC":
                # print(len(collapse(clause[1][1])))
                CC = [get_terminals(x, []) for x in collapse(clause[1][1]) if x._label != "Conj" and not "N" in x._label]
                conj = get_terminals(clause[0][0], [])
                # conj = [get_terminals(x, []) for x in clause[0][0]]
                sub_cc = [get_terminals(x, []) for x in clause[0][1] if x._label != "Conj"and not "N" in x._label]
                print(sub_cc)
                # CC = get_terminals(clause[1][1], [])
                # conj = get_terminals(clause[0][0], [])
                # sub_cc = get_terminals(clause[0][1], [])

            elif clause[1]._label == "SC":
                # print(len(collapse(clause[0][1])))
                CC = [get_terminals(x, []) for x in collapse(clause[0][1]) if x._label != "Conj"and not "N" in x._label]
                conj = get_terminals(clause[1][0], [])
                sub_cc = [get_terminals(x, []) for x in clause[1][1] if x._label != "Conj"and not "N" in x._label]

            elif clause._label == "CC":
                find_verb_phrases(tree, tasks)

                # CC = get_terminals(clause[0][1], [])
                # conj = get_terminals(clause[1][0], [])
                # sub_cc = get_terminals(clause[1][1], [])
            if conj[0] == "before":
                print("First, " + (" " + conj[0] + " ").join([" ".join(x) for x in CC]) + " then " + " ".join([" ".join(x) for x in sub_cc]))
                s = draw_span(draw_ul([" ".join(c) for c in CC])) + draw_span(draw_ul([" ".join(c) for c in sub_cc]))

                cc_list = [" ".join(c) for c in CC]
                sub_cc_list = [" ".join(x) for x in sub_cc]

                # print("lists: ", cc_list, sub_cc_list)

                for sub in sub_cc_list:
                    for cc in cc_list:
                        found = search(tasks, sub)
                        if found != -1:
                            tasks.append(Task(cc, found[1].priority - 1))
                        else:
                            tasks.append(Task(sub, 0))
                            tasks.append(Task(cc, 1))

                # print("\n".join([draw_div(" ".join(x)) for x in CC]))
                return s

            if conj[0] == "after" or conj[0] == "if":
                print("First, " + (" " + conj[0] + " ").join([" ".join(x) for x in sub_cc]) + " then " + " ".join([" ".join(x) for x in CC]))
                # print("First, " + " ".join(sub_cc) + " then " + " ".join(CC))
                # s = draw_span(" ".join(sub_cc)) + draw_span(" ".join(CC))
                s = draw_span(draw_ul([" ".join(c) for c in sub_cc])) + draw_span(draw_ul([" ".join(c) for c in CC]))

                cc_list = [" ".join(c) for c in CC]
                sub_cc_list = [" ".join(x) for x in sub_cc]

                for cc in cc_list:
                    for sub in sub_cc_list:
                        found = search(tasks, sub)
                        if found != -1:
                            tasks.append(Task(cc, found[1].priority + 1))
                        else:
                            tasks.append(Task(sub, 0))
                            tasks.append(Task(cc, 1))

                print("lists: ", cc_list, sub_cc_list)
                return s


def get_terminals(tree, res):
    # print("res: ", res)
    for subtree in tree:
        if type(subtree) == str:
            res.append(subtree)
        else:
            res = get_terminals(subtree, res)
    return res


def get_text(filepath):
    with open(filepath) as f:
        return f.read()


def gantt_main():
    text = get_text("src/in.txt")
    sentences = nltk.sent_tokenize(text)
    for x in range(len(sentences)):
        sentences[x] = nltk.word_tokenize(sentences[x])

    # Strip punctuation
    sentences = [list(filter(lambda s: s.isalpha(), sentence)) for sentence in sentences]

    grammar = parse_grammar(GANTT_GRAMMAR)
    improve_grammar(grammar)


    parser = nltk.ChartParser(nltk.CFG.fromstring(str(grammar)))

    s = """"""
    s += """
    <!DOCTYPE html>
    <html>
    <style>
        .level {
            background-color: lightgrey;
            width: 300px;
            border: 5px solid green;
            padding: 5px;
            margin: 15px;
        }
        ul {
            float: left;
        }
        li {
            background-color: lightgrey;
            margin: 15px;
        }
    </style>

    <body>
    """
    tasks = []

    for sentence in sentences:
        tree = list(parser.parse(sentence))[0]

        # print(tree)

        # s += find_verb_phrases(tree, tasks)
        find_verb_phrases(tree, tasks)
    print("Tasks:")
    for task in tasks:
        print(task)
    maxp = 0, tasks[0].priority
    minp = 0, tasks[0].priority
    for i, task in enumerate(tasks):
        if task.priority < minp[1]:
            minp = i, task.priority
        if task.priority > maxp[1]:
            maxp = i, task.priority


    curr_priority = tasks[0].priority
    s += "<ul> \n"
    for task in tasks:
        if task.priority > curr_priority:
            s += "<ul> \n"
        s += "<li>" + task.desc + "</li>\n"
        curr_priority = task.priority
    s += (maxp[1] - minp[1]) * "</ul>\n"
    s += "</ul>\n"



    # [print(task) for task in tasks]

    s += """
    </body>
    </html>
    """

    # print(s)
    with open("html_out.html", "w") as f:
        f.write(s)


if __name__ == "__main__":
    gantt_main()
