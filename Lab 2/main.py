import nltk
import spacy
from spacy import displacy

"""
Get familiar with syntactic and dependency parsing by generating the corresponding trees for
the following sentences:
The chicken is ready to eat.
John saw the chicken in the street.
The old chicken and ducks eat.
John is an old ducks enthusiast.

Steps:
1. (0.25p) Write a suitable constituency grammar, able to correctly parse all sentences, with all
their senses. Use as inspiration the grammars discussed in class.

2. (0,25p) Use existing modules to extract phrase structure trees for these sentences.

3. (0.25p) Implement a dependency parser (using, for instance, spaCY, NLTK or Stanza) and
parse the three sentences above.

https://towardsdatascience.com/natural-language-processing-dependency-parsing-cf094bbbe3f7

4. (0,25p) Describe an application which needs syntactic and/or dependency parsing. Explain
why, also providing concrete examples. (1/2 pag.)
"""

"""
1. The chicken is ready to eat
S -> NP VP (the chicken; is ready to eat)
NP -> A N
VP -> VP VP
VP -> P V
VP -> V ADJ
ADJ -> ready
P -> to
V -> eat | is
A -> the
N -> chicken

John saw the chicken in the street.
S -> NP VP
NP -> N
NP -> A N
N -> John
VP -> V OP
OP -> NP PP
PP -> P NP
V -> saw
A -> the
N -> John | chicken | street
P -> in

The old chicken and ducks ;eat.
S -> NP VP
VP -> V
NP -> NP NP
NP -> P NP
NP -> ADJ N
NP -> CONJ N

ADJ -> old
N -> chicken | ducks
V -> eat
P -> the
CONJ -> and

John ;is an old ducks enthusiast.
S -> NP VP
NP -> N
NP -> A NP
NP -> ADJ N
VP -> V AP
AP -> NP N

ADJ -> old
A -> an
N -> John | ducks | enthusiast
V -> is


all

S -> NP VP
NP -> A N
NP -> N
NP -> A NP
NP -> ADJ N
VP -> VP VP
VP -> V AP
VP -> P V
VP -> V ADJ
VP -> V OP
VP -> V
AP -> NP N

CONJ -> and
ADJ -> ready | old
P -> to | in
V -> eat | is | saw
A -> the | a
N -> chicken | John | street | ducks | enthusiast
"""


def preprocess(text):
    sentences2 = nltk.sent_tokenize(text)
    sentences2 = [nltk.word_tokenize(s) for s in sentences2]
    # sentences2 = [nltk.pos_tag(s) for s in sentences2]

    return sentences2


if __name__ == '__main__':
    sentences = ['The chicken is ready to eat',
                 'John saw the chicken in the street',
                 'The old chicken and ducks eat',
                 'John is an old ducks enthusiast']

    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('maxent_ne_chunker', quiet=True)
    nltk.download('words', quiet=True)
    nltk.download('comparative_sentences', quiet=True)

    preprocessed = [preprocess(s) for s in sentences]

    grammar = nltk.CFG.fromstring("""
    S -> NP VP
    VP -> V | P V | V NP | V Adj P V
    NP -> N | Det NP | Det NP ADJP | Adj NP | NP PP | N Conj NP | N N | Det NP CJP | ADJP NP
    CJP -> Conj NP
    ADJP -> V Adj | Adj NP
    PP -> P NP
    Det -> 'The' | 'an' | 'the'
    N -> 'chicken' | 'street' | 'ducks' | 'enthusiast' | 'John'
    Adj -> 'old' | 'ready'
    P -> 'in' | 'to'
    V -> 'is' | 'eat' | 'saw'
    Conj -> 'and' 
        """)

    # Create a parser
    parser = nltk.ChartParser(grammar)

    # Parse and print the trees
    for i, sentence in enumerate(preprocessed):
        print(f"Parse Tree for Sentence {i + 1}:")
        # words = nltk.word_tokenize(sentence)
        for tree in parser.parse(sentence[0]):
            tree.pretty_print()
        print()

    # Implement a dependency parser (using, for instance, spaCY, NLTK or Stanza) and
    # parse the three sentences above.

    nlp = spacy.load("en_core_web_sm")

    for i, sentence in enumerate(sentences):
        print(f"Dependency Parse Tree for Sentence {i+1}: {sentence}")
        doc = nlp(sentence)
        print("{:<15} | {:<8} | {:<15} | {:<20}".format('Token', 'Relation', 'Head', 'Children'))
        print("-" * 70)
        for token in doc:
            print("{:<15} | {:<8} | {:<15} | {:<20}"
                  .format(str(token.text), str(token.dep_), str(token.head.text),
                          str([child for child in token.children])))
        html_file = f"sentence_{i+1}_dependency_parse.html"
        html = displacy.render(doc, style='dep', jupyter=False, page=True)
        with open(html_file, "w") as file:
            file.write(html)
        print()
