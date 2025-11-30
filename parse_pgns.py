import chess.pgn
import pandas as pd
import os
from eco_dict import eco_dict   

PGN_FOLDER = "PGN"

files = {
    "Paul Morphy": "Paul_Morphy.pgn",
    "Jose Raul Capablanca": "Jose_Raul_Capablanca.pgn",
    "Alexander Alekhine": "Alexander_Alekhine.pgn",
    "Mikhail Tal": "Mikhail_Tal.pgn",
    "Anatoly Karpov": "Anatoly_Karpov.pgn",
    "Bobby Fischer": "Bobby_Fischer.pgn",
}

rows = []


def get_plycount(game):
    """Returns number of half-moves, or None if error."""
    try:
        return game.end().ply()
    except:
        return None


for player, fname in files.items():
    full_path = os.path.join(PGN_FOLDER, fname)
    print(f"\nProcessing: {player}")

    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break

            hdr = game.headers

            white = hdr.get("White")
            black = hdr.get("Black")

            # Determine color of the master
            if white and player.split()[-1].lower() in white.lower():
                color = "white"
                opponent = black
            elif black and player.split()[-1].lower() in black.lower():
                color = "black"
                opponent = white
            else:
                # fallback: assume master is White if metadata unclear
                color = "unknown"
                opponent = black if white == player else white

            eco = hdr.get("ECO")
            opening = eco_dict.get(eco, "Unknown Opening")

            row = {
                "player": player,
                "color": color,
                "opponent": opponent,
                "result": hdr.get("Result"),
                "event": hdr.get("Event"),
                "site": hdr.get("Site"),
                "date": hdr.get("Date"),
                "year": hdr.get("Date", "")[:4],
                "eco": eco,
                "opening": opening,
                "plycount": get_plycount(game),
            }

            rows.append(row)

# Convert to DataFrame
df = pd.DataFrame(rows)

# Remove broken games
df = df.dropna(subset=["plycount"])
df = df[df["year"].str.isnumeric()]  # remove weird dates like "????.??.??"

# Save final cleaned dataset
df.to_csv("masters_cleaned.csv", index=False)

print("\nDONE — Saved masters_cleaned.csv")
print("Total games:", len(df))
