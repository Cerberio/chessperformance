import pandas as pd

df = pd.read_csv("masters_cleaned.csv")

print("Initial size:", len(df))

#FIX YEAR COLUMN
df["year"] = df["year"].astype(str).str.extract(r"(\d{4})")
df = df.dropna(subset=["year"])
df["year"] = df["year"].astype(int)

#REMOVE SIMULTANEOUS, BLINDFOLD, ODDS, EXHIBITIONS, CASUAL, TRAINING 
filters = [
    "simul",
    "blind",
    "odds",
    "exhib",
    "casual",
    "training",
    "friendly",
    "handicap"
]

for word in filters:
    df = df[~df["event"].str.contains(word, case=False, na=False)]

#REMOVE GAMES AGAINST UNKNOWN/NONSERIOUS OPPONENTS 
df = df[~df["opponent"].str.contains("NN", case=False, na=False)]
df = df[~df["opponent"].str.contains("anonymous", case=False, na=False)]

#REMOVE WEIRD EMPTY ECO CODES 
df = df.dropna(subset=["eco"])
df = df[df["eco"] != "?"]

#REMOVE VERY SHORT / CORRUPTED GAMES 
df = df[df["plycount"] >= 8]

#REMOVE DUPLICATES
df = df.drop_duplicates()

#SAVE CLEANED DATASET
df.to_csv("masters_cleaned_final.csv", index=False)

print("Final size:", len(df))
print("Saved: masters_cleaned_final.csv")
