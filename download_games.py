import requests
import zipfile
import io
import os

players = {
    "Paul_Morphy": "Morphy",
    "Jose_Raul_Capablanca": "Capablanca",
    "Alexander_Alekhine": "Alekhine",
    "Mikhail_Tal": "Tal",
    "Anatoly_Karpov": "Karpov",
    "Bobby_Fischer": "Fischer"
}

BASE_URL = "https://www.pgnmentor.com/players/{}.zip"


headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/118.0.0.0 Safari/537.36"
    )
}

if not os.path.exists("PGN"):
    os.mkdir("PGN")

for outname, key in players.items():
    url = BASE_URL.format(key)
    print("Downloading:", url)

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("FAILED:", r.status_code)
        continue

    z = zipfile.ZipFile(io.BytesIO(r.content))

    # extract the PGN file
    for filename in z.namelist():
        if filename.lower().endswith(".pgn"):
            z.extract(filename, "PGN")
            os.rename(f"PGN/{filename}", f"PGN/{outname}.pgn")

    print("Saved:", f"PGN/{outname}.pgn")
