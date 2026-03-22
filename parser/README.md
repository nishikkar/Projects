# Parser

A context-free grammar (CFG) sentence parser and noun phrase chunk extractor built with NLTK, as part of [CS50's Introduction to Artificial Intelligence with Python](https://cs50.harvard.edu/ai/).

---

## Overview

This project explores how **context-free grammars** can model the structure of natural language. Using Python's `nltk` library, the program:

- Accepts an English sentence as input (typed or from a file)
- Parses it against a hand-written CFG
- Prints all valid **syntax trees** for the sentence
- Extracts and prints all **noun phrase (NP) chunks** — noun phrases that contain no nested noun phrases

---

## Files

```
.
├── parser.py          # Main script: CFG definition, parsing logic, NP chunk extraction
├── sentences/         # Sample .txt sentences used for testing
│   ├── 1.txt
│   ├── 2.txt
│   └── ...
└── README.md
```

---

## Requirements

- Python 3.10+
- `nltk`

Install dependencies:

```bash
pip install nltk
```

---

## Usage

Run with a sentence file:

```bash
python parser.py sentences/1.txt
```

Or run without arguments to type a sentence manually:

```bash
python parser.py
```

**Example:**

```
$ python parser.py sentences/7.txt
        S
   _____|___
  NP        VP
  |      ___|___
Holmes   V      NP
         |    __|___
        sat  Det    N
              |     |
             the   dog

Noun Phrase Chunks:
Holmes
the dog
```
                S
   _____________|___
  |                 S
  |                 |
  |                 VP
  |        _________|___
  S       |             NP
  |       |          ___|_____
  NP      |         |         NP
  |       |         |         |
  N       V         P         N
  |       |         |         |
holmes arrived      on     thursday

Noun Phrase Chunks
holmes
thursday
                    S
         ___________|_______
        S                   S
        |                   |
        VP                  NP
   _____|_____           ___|_____
  NP          |         |         NP
  |           |         |         |
  N           V         P         N
  |           |         |         |
holmes     arrived      on     thursday

Noun Phrase Chunks
holmes
thursday
                    S
         ___________|_______
        |                   S
        |                   |
        |                   NP
        |                ___|_____
        S               |         NP
   _____|_____          |         |
  N           V         P         N
  |           |         |         |
holmes     arrived      on     thursday

Noun Phrase Chunks
thursday
              S
         _____|___________
        S           |     |
        |           |     |
        VP          |     S
   _____|_____      |     |
  NP          |     |     NP
  |           |     |     |
  N           V     P     N
  |           |     |     |
holmes     arrived  on thursday

Noun Phrase Chunks
holmes
holmes
thursday
holmes
holmes
holmes
holmes
holmes
thursday
              S
         _____|___________
        |           |     S
        |           |     |
        S           |     NP
   _____|_____      |     |
  N           V     P     N
  |           |     |     |
holmes     arrived  on thursday

Noun Phrase Chunks
thursday
---

## Grammar

The CFG is defined inside `parser.py` and covers a range of English sentence structures. A simplified excerpt:

```
S -> N V | NP | VP | NP VP | S S | S Conj S | S P S | VP NP | Cl V | Cl
NP -> N | Det NP | NP P | NP NP | P NP | Adj NP 
VP -> V NP | NP V | V Adv 
Cl -> NP Adv | NP VP | Cl P Cl
```

**Terminals** (words) are mapped to their respective parts of speech — nouns, verbs, adjectives, determiners, prepositions, adverbs, and conjunctions.

---

## Noun Phrase Chunks

A **noun phrase chunk** is defined as a noun phrase (`NP`) that does not itself contain any other noun phrase as a subtree. These are extracted by traversing each parse tree and collecting `NP` nodes with no nested `NP` children.

---

## Background

**Context-free grammars** define a set of recursive rewrite rules that describe how sentences can be broken down into constituent parts. They are a foundational tool in computational linguistics and NLP, enabling programs to assign structure and meaning to raw text.

This project was built as part of **CS50 AI — Problem Set 6**.

---

## Acknowledgements

- [CS50's Introduction to AI with Python](https://cs50.harvard.edu/ai/) by Harvard University
- [NLTK — Natural Language Toolkit](https://www.nltk.org/)
- *Speech and Language Processing* — Jurafsky & Martin
