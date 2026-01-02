# Comparative Data Analysis of Chess Masters Using PGN Archives

## Purpose and Motivation
- This project aims to perform a structured, data-driven analysis of the playing styles and statistical tendencies of several classical chess masters, using their complete game archives in PGN format. While the games of legends such as Paul Morphy, José Raúl Capablanca, Alexander Alekhine, Mikhail Tal, Anatoly Karpov, and Bobby Fischer have been studied extensively from a historical and strategic perspective, they are rarely examined through a modern data-science lens.

- Chess literature often focuses on qualitative commentary, personal impressions, or selected landmark games. However, with thousands of games now digitized, there is an opportunity to complement traditional chess theory with quantitative insights. By cleaning, filtering, and analyzing these datasets, we can answer questions such as:

  - Which openings did each player favor, and how did their opening choices evolve?
  - How long were their games on average?
  - How do their win rates differ when playing White vs. Black?
  - Are certain ECO families strongly associated with specific players’ styles?
  - Do historical narratives (e.g., “Capablanca’s clarity”, “Tal’s aggression”, “Karpov’s precision”) show measurable patterns in the data?

- The motivation behind this project is not only to validate or challenge widely-held beliefs about these players but also to demonstrate how classical game data can be transformed into meaningful visual analytics using Python, Pandas, Matplotlib, and Seaborn.

- This work showcases how data science techniques can extract trends from large historical datasets, turning raw PGN files into interpretable insights about some of the greatest chess players of all time.


## Data

- A PGN (Portable Game Notation) is the standard text-based file format used to store chess games.
- A PGN file contains:
  - Game metadata (player names, event, site, date, result, ECO code, etc.)
  - Move list recorded in algebraic notation
  - Optional annotations or comments

- PGNs are widely used because they are both machine-readable (easy to parse programmatically) and human-readable (you can open them in any text editor).
- This format makes PGNs ideal for large-scale data extraction and statistical analysis.

### Data Source

- The PGN files for each player were downloaded from PGN Mentor, one of the most complete and standardized archives of classical players’ games. I selected this source for three main reasons:

  - **1. High completeness**  
    PGN Mentor provides nearly all recorded games for historical players like Morphy, Capablanca, Alekhine, Tal, Karpov, and Fischer.

  - **2. Standardized metadata**  
    The PGNs from PGN Mentor follow consistent formatting conventions, making them easier to parse with Python's `chess.pgn` module.  
    Fields such as:
    - Event  
    - Site  
    - Date  
    - ECO  
    - Result  
    are usually available and structured.

  - **3. Offline, stable dataset**  
    Unlike web scraping from Chess.com or ChessGames.com (which may fail due to rate limits or inconsistent formatting), the PGN Mentor files:
    - Are already zipped and downloadable  
    - Do not change over time  
    - Require no API key  
    This ensures reproducibility of the study.

### Data Cleaning & Preparation

- After parsing ~9,200 raw games, a cleaning process was necessary before performing meaningful analysis.  
- The steps below describe how the dataset was prepared and filtered:

#### 1. Parsing all PGNs into a unified DataFrame

- For each player, every game was parsed using Python’s python-chess library.
- From each game, the following fields were extracted:
  - Player  
  - Color (white/black)  
  - Opponent  
  - Result (1-0, 0-1, 1/2-1/2)  
  - Event  
  - Site  
  - Date  
  - Year (first 4 characters of Date)  
  - ECO code (PGN files contain ECO codes instead of direct opening names, the opening name will be derived from `eco_dict.py` by finding what their ECO codes correspond to)  
  - Opening name (via ECO lookup)  
  - Number of half-moves (plycount as used in the code)

- This produced a raw master dataset of 9,256 games.

#### 2. Removing invalid or uninformative games

- Some games needed to be excluded:

  - **Incomplete or corrupted PGNs**  
    Games missing essential fields (ECO, result, or valid plycount) were removed.

  - **Games with “NN” opponents**  
    “NN” stands for “No Name,” typically used in:
    - casual games  
    - practice games  
    - unrecorded opponent games  
    These are not suitable for competitive statistical comparison.

  - **Simuls, Blindfold, Odds, and Exhibition games**  
    These were detected via keywords in the Event field:
    - “Simul”  
    - “Blindfold”  
    - “Odds”  
    - “Exhibition”  
    - "Handicap"  
    - “Training”  
    These formats do not represent standard tournament play and would distort win-rate or opening-preference statistics.

#### 3. Filtering by valid year

- Games with missing or placeholder dates like `"????.??.??"` were removed.
- Only games with a numeric 4-digit year were kept.

#### 4. Final Dataset

- After cleaning:
  - Initial size: **9,256**
  - Final size: **8,612** games

- All games are:
  - Standard competitive games  
  - Played against real opponents  
  - With valid ECO codes  
  - With valid move counts  
  - Free of simul/exhibition/odds formats

- Parsed with `python-chess` into a cleaned CSV:  
  **`masters_cleaned_final.csv`**

---

## Goals

- Exploratory Data Analysis (EDA) of game lengths, openings, and results.
- Hypothesis tests:
  - Do different players have significantly different average game lengths?
  - Do players prefer different ECO opening families?
  - Does win rate differ between White and Black?

---

### 1. Average Game Length Differences (half-moves)

**Research Question:**  
Do different players tend to play longer games on average?

**Hypotheses:**

- **H₀:** All six players have the same average plycount.  
- **H₁:** At least one player’s average plycount differs.  
  (There is a significant difference in game length between players.)

- **Testing Method:** The average plycount for each player was computed and visualized using a bar plot. Differences in mean game length across players were examined visually to assess whether substantial variation exists.

**Visualization:**  
![Average Game Length](images/avg_plycount.png)

**Findings and Interpretation:** The figure shows noticeable differences in average game length (measured by plycount) among the six chess masters.

Paul Morphy has the shortest games on average, reflecting the tactical, fast-developing style of 19th-century chess, where decisive attacks often concluded games quickly. Mikhail Tal also exhibits relatively shorter games compared to most other players, which is consistent with his highly aggressive and sacrificial style that frequently led to early decisive outcomes.

In contrast, José Raúl Capablanca, Alexander Alekhine, Anatoly Karpov, and Bobby Fischer all display longer average game lengths. Among these, Anatoly Karpov has the longest games on average, aligning with his well-known positional and prophylactic approach, where games were often decided after long strategic maneuvering. Bobby Fischer and Alexander Alekhine also show high average plycounts, suggesting a balance between tactical play and deep endgame or middlegame struggles. Capablanca’s games are slightly shorter than Karpov’s and Fischer’s but still notably longer than Morphy’s and Tal’s.

**Conclusion:**  The observed differences in average plycount across players indicate meaningful variation in game length. Therefore, the null hypothesis (H₀) that all players have the same average game length is rejected. The results support the idea that historical playing styles and eras are reflected in measurable differences in game duration.


---

### 2. Opening Family Preferences (ECO Letter A–E)

**Research Question:**  
Do players differ in the types of openings they prefer (ECO families A–E)?

**Hypotheses:**

- **H₀:** The distribution of ECO opening families is the same for all players.  
  (No player shows a unique opening preference.)

- **H₁:** At least one player has a different opening family distribution.  
  (Players prefer different openings.)

- **Testing Method:** The distribution of ECO opening families (A–E) was compared across players using grouped count plots.

**Visualization:**  
![Opening Distribution](images/opening_distribution.png)

**Findings and Interpretation:** The results show strong variation in opening family preferences.
For example, Mikhail Tal exhibits a higher frequency of aggressive open games (ECO C), while Anatoly Karpov shows a broader distribution including positional systems (ECO D and E). These differences suggest that opening preferences are player-specific rather than random.

**Conclusion:** The observed distributions differ notably across players.
Therefore, H₀ is rejected in favor of H₁.

---

## 3. Win Rate Differences Between White and Black

**Research Question:**  
Is a player's win rate significantly different when playing White vs. playing Black?

**Hypotheses:**

- **H₀:** Win rate(White) = Win rate(Black)  
  (Playing White does not change the probability of winning.)

- **H₁:** Win rate(White) ≠ Win rate(Black)  
  (There is a difference in win rate based on color.)

- **Testing Method:** Win rates were computed separately for games played as White and Black and compared visually across players.

**Visualization:**  
![Win Rate by Color](images/winrate_white_black.png)

**Findings and Interpretation:** Across all players, win rates are consistently higher when playing White.
This aligns with established chess theory regarding the first-move advantage. However, the magnitude of this difference varies by player, with some players (e.g., Karpov) showing a stronger Black performance than others.

**Conclusion:**  Since win rates differ between White and Black, H₀ is rejected.
Playing color has a measurable effect on winning probability.

---


## Machine Learning Analysis

In addition to exploratory data analysis and hypothesis testing, supervised machine learning models were applied to investigate whether game-level statistics can be used to predict outcomes, players, or historical eras. The objective of these models is exploratory rather than predictive perfection: to assess whether measurable statistical signals exist in the data.

All models were implemented using scikit-learn pipelines to ensure consistent preprocessing and reproducibility.

---

### ML Task 1: Predicting Game Outcome (Win vs. Non-Win)

**Research Question:**  
Can game-level features be used to predict whether a game results in a win?

**Target Variable:**
- `win`  
  - 1 = win  
  - 0 = loss or draw  

**Features Used:**
- Player  
- Color (White / Black)  
- ECO opening family (A–E)  
- Game length (plycount)

**Model:**
- Logistic Regression  
- One-hot encoding for categorical variables  
- 75% training / 25% testing split  

**Evaluation Metrics:**
- Accuracy  
- Precision  
- Recall  
- F1-score  

**Results:**
- Accuracy ≈ **70%**
- Performance significantly exceeds random guessing (≈50%)

**Interpretation:**  
The model successfully captures well-known chess factors such as White’s first-move advantage and the relationship between game length and decisive results. This indicates that aggregate game statistics contain meaningful predictive information about outcomes.

---

### ML Task 2: Predicting Chess Era from Aggregate Game Features

**Research Question:**  
Can aggregate game statistics distinguish between different historical chess eras?

**Target Variable:**
- Era category:
  - Classical Era  
  - Hypermodern Era  
  - Fischer Era  
  - Soviet School  

**Features Used:**
- ECO opening family  
- Game length (plycount)  
- Color  

**Model:**
- Logistic Regression  
- Class imbalance handled using `class_weight="balanced"`  
- Stratified train-test split  

**Evaluation Metrics:**
- Accuracy  
- Precision  
- Recall  
- F1-score (weighted average)

**Results:**
- Accuracy ≈ **45%**
- Weighted F1-score ≈ **0.48**
- Random baseline weighted F1 ≈ **0.29**

**Interpretation:**  
Although absolute accuracy is moderate, the model significantly outperforms random guessing. This suggests that historical eras leave measurable statistical fingerprints in opening choices and game structure, even when using only high-level features.

---

### ML Task 3: Move-Based Era Classification

**Research Question:**  
Do move-level features provide stronger signals for identifying historical chess eras than aggregate statistics?

**Feature Construction from Move Sequences:**
- Early-game move patterns  
- Capture rates  
- Development-related move frequencies  
- Normalized game length  

(Extracted into a separate move-level dataset.)

**Model:**
- Logistic Regression  
- Balanced class weights  
- Same evaluation framework as ML Task 2  

**Results:**
- Accuracy improved from ≈ **37% → 45%**
- Weighted F1-score ≈ **0.48**

**Interpretation:**  
Move-level features improve era classification performance, indicating that stylistic differences are partially encoded in how pieces are moved, not only in opening choices or game length. However, substantial overlap remains between eras, reflecting the nuanced and evolving nature of chess styles.

---

### Limitations

- Class imbalance, particularly dominance of the Soviet School era  
- Absence of engine-based evaluation features (e.g., centipawn loss)  
- Logistic regression cannot model deep sequential dependencies  
- Chess style exhibits natural overlap across eras  

---

### Future Work

- Incorporate engine evaluation metrics   
- Expand to modern grandmasters  
- Perform per-opening or per-era sub-analyses  

---

## Reproducing

```bash
pip install -r requirements.txt
python parse_pgns.py
python clean_dataset.py
#  Generate move-level features for ML 
python move_based.py
# then open analysis.ipynb
