# DSA210 Term Project – Classical Chess Legends

This project analyzes the games of Paul Morphy, Jose Raul Capablanca,
Alexander Alekhine, Mikhail Tal, Anatoly Karpov, and Bobby Fischer.

## Data

- PGNs downloaded from public chess databases (PGN Mentor).
- Parsed with `python-chess` into a cleaned CSV: `masters_cleaned_final.csv`.

## Goals

- Exploratory Data Analysis (EDA) of game lengths, openings, and results.
- Hypothesis tests:
  - Do different players have significantly different average game lengths?
  - Do players prefer different ECO opening families?
  - Does win rate differ between White and Black?

## Reproducing

```bash
pip install -r requirements.txt
python parse_pgns.py
python clean_dataset.py
# then open analysis.ipynb
