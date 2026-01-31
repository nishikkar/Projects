import nltk
import sys


TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> N V | NP | VP | NP VP | S S | S Conj S | S P S | VP NP | Cl V | Cl
NP -> N | Det NP | NP P | NP NP | P NP | Adj NP 
VP -> V NP | NP V | V Adv 
Cl -> NP Adv | NP VP | Cl P Cl
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    lower=sentence.lower()
    tokens=nltk.tokenize.word_tokenize(lower)
    final=list()
    for token in tokens:
        for ch in token:
            if ch.isalpha():
                final.append(token)
                break
    return final
    raise NotImplementedError


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []
    
    for subtree in tree.subtrees():
        # Check if this subtree is an NP
        if subtree.label() == 'NP':
            # Check if it contains any other NPs
            contains_other_np = False
            
            # Look at all proper subtrees (excluding the current subtree itself)
            for subsubtree in subtree.subtrees(lambda t: t != subtree):
                if subsubtree.label() == 'NP':
                    contains_other_np = True
                    break  # Found another NP inside, so not a base chunk
            
            # If no other NPs inside, it's a base NP chunk
            if not contains_other_np:
                chunks.append(subtree)
    
    return chunks
    raise NotImplementedError


if __name__ == "__main__":
    main()
