# Attention

A masked language model and transformer attention visualizer built with BERT, as part of [CS50's Introduction to Artificial Intelligence with Python](https://cs50.harvard.edu/ai/).

---

## Overview

This project explores the **attention mechanism** inside transformer models. Using a pre-trained `bert-base-uncased` model via HuggingFace, the program:

- Takes a sentence containing a `[MASK]` token as input
- Predicts the top most likely words to fill in the mask
- Generates a visual diagram of attention scores across all 12 attention heads in a given transformer layer, saved as a `.png` file

---

## Files

```
.
├── mask.py          # Main script: masked LM predictions + attention diagram generation
├── analysis.pdf     # Written analysis interpreting attention head behaviors
└── README.md
```

---

## Requirements

- Python 3.10+
- `transformers`
- `tensorflow`
- `Pillow`

Install dependencies:

```bash
pip install transformers tensorflow Pillow
```

---

## Usage

```bash
python mask.py
```

You will be prompted to enter a sentence with a `[MASK]` token somewhere in it.

**Example:**

```
$ python mask.py
Text: The cat sat on the [MASK].

[MASK]: floor | bed | couch | ground | table
```

An attention diagram will be saved to `attention_layer{N}_head{M}.png` showing how each of BERT's 12 attention heads distributes focus across the input tokens.

---

## Attention Diagrams

Each diagram visualizes a single attention head — darker/stronger connections between tokens indicate higher attention weights. By examining these across different heads and layers, you can begin to see patterns:

- Some heads attend to **adjacent tokens**
- Some focus on **syntactic relationships** (e.g., subject → verb)
- Some heads specialize in **punctuation or separator tokens**

See `analysis.pdf` for a detailed breakdown of observed patterns.

---

## Background

BERT (**B**idirectional **E**ncoder **R**epresentations from **T**ransformers) is trained on a masked language modeling objective — randomly masking words in a sentence and learning to predict them from context. Its transformer architecture relies on **self-attention**, allowing every token to attend to every other token simultaneously, in both directions.

This project was built as part of **CS50 AI — Problem Set 6**.

---

## Acknowledgements

- [CS50's Introduction to AI with Python](https://cs50.harvard.edu/ai/) by Harvard University
- [HuggingFace Transformers](https://huggingface.co/docs/transformers)
- BERT: *Pre-training of Deep Bidirectional Transformers for Language Understanding* — Devlin et al., 2018
