import chess.pgn

def extract_move_features(game, max_plies=20):
    """
    Extracts simple stylistic features from the first max_plies of a game.
    """
    features = {
        "e4_count": 0,
        "d4_count": 0,
        "knight_moves": 0,
        "bishop_moves": 0,
        "queen_moves_early": 0,
        "captures_early": 0,
        "early_castle": 0,
    }

    board = game.board()
    ply = 0

    for move in game.mainline_moves():
        if ply >= max_plies:
            break

        piece = board.piece_at(move.from_square)
        san = board.san(move)

        # Pawn openings
        if san.startswith("e4"):
            features["e4_count"] += 1
        if san.startswith("d4"):
            features["d4_count"] += 1

        # Piece-based features
        if piece:
            if piece.piece_type == chess.KNIGHT:
                features["knight_moves"] += 1
            elif piece.piece_type == chess.BISHOP:
                features["bishop_moves"] += 1
            elif piece.piece_type == chess.QUEEN:
                features["queen_moves_early"] += 1

        # Aggression
        if "x" in san:
            features["captures_early"] += 1

        # Castling
        if san in ["O-O", "O-O-O"]:
            features["early_castle"] = 1

        board.push(move)
        ply += 1

    return features


import pandas as pd
import chess.pgn
import os
def build_move_dataset(pgn_files, max_plies=20):
    rows = []

    for player, pgn_path in pgn_files.items():
        print(f"Processing {player}...")
        with open(pgn_path, encoding="utf-8", errors="ignore") as f:
            while True:
                game = chess.pgn.read_game(f)
                if game is None:
                    break

                features = extract_move_features(game, max_plies)
                features["player"] = player
                rows.append(features)

    return pd.DataFrame(rows)



PGN_FILES = {
    "Paul Morphy": "PGN/Paul_Morphy.pgn",
    "Jose Raul Capablanca": "PGN/Jose_Raul_Capablanca.pgn",
    "Alexander Alekhine": "PGN/Alexander_Alekhine.pgn",
    "Mikhail Tal": "PGN/Mikhail_Tal.pgn",
    "Anatoly Karpov": "PGN/Anatoly_Karpov.pgn",
    "Bobby Fischer": "PGN/Bobby_Fischer.pgn",
}



df_moves = build_move_dataset(PGN_FILES, max_plies=20)
print(df_moves.head())
print(df_moves.shape)

df_moves.to_csv("move_based_features.csv", index=False)
print("Saved move_based_features.csv")
