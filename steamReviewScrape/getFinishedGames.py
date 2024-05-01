# Titles that finished
from datetime import datetime
import json
import pandas as pd
finished = ["Baldur's Gate 3", "Streets Of Rogue", "Vampire Survivors", "Kenshi", "Subnautica", "Prison Architect", "Darkest Dungeon", "Slay The Spire", "Kerbal Space Program",
            "RimWorld",
            "Hades",
            "Dead Cells",
            "Factorio",
            "Oxygen Not Included",
            "Raft",
            "Risk of Rain 2",
            "Rust",
            "The Forest",
            "Besiege",
            "Space Engineers",
            "Baba Is You",
            "Terraria",
            "Graveyard Keeper",
            "Celeste",
            "Noita",
            "Stardew Valley",
            "Outer Wilds",
            "Battle Brothers",
            "The Long Dark",
            "Mount & Blade II: Bannerlord",
            "Hollow Knight",
            "Among Us",
            "The Escapists 2",
            "Northgard",
            "Rivals of Aether",
            "Grim Dawn",
            "Barotrauma",
            "Golf With Your Friends",
            "Frostpunk",
            "DayZ",
            "Overgrowth",
            "Gorn",
            "Squad",
            "Mount & Blade: Warband",
            "Inscryption",
            "Don't Starve Together",
            "Blackwake",
            "Garry's Mod",
            "Ghostrunner",
            "Astroneer",
            "Path of Exile",
            "Surviving Mars",
            "ARK: Survival Evolved",
            "Dead by Daylight",
            "PULSAR: Lost Colony",
            "GTFO",
            "Mordhau",
            "Farming Simulator 19",
            "Hardspace: Shipbreaker",
            "Viscera Cleanup Detail",
            "Holdfast: Nations At War",
            "Insurgency: Sandstorm",
            "Foxhole",
            "Darkwood",
            "Unturned",
            ]

ids = [1086940, 512900, 1794680, 233860, 264710, 233450, 262060, 2868840, 220200, 294100, 1145360, 588650,
       427520, 457140, 648800, 632360, 252490, 242760, 346010, 244850, 736260, 105600, 599140, 504230, 881100,
       413150, 753640, 365360, 305620, 261550, 367520, 945360, 641990, 466560, 383980, 219990, 602960, 431240,
       323190, 221100, 25000, 578620, 393380, 48700, 1092790, 322330, 420290, 4000, 1139900, 361420, 238960, 464920, 346110, 381210, 252870, 493520, 629760, 787860, 1161580, 246900, 589290, 581320, 505460, 274520, 304930]

df = pd.read_json('betaGames.json')
df['Review Summary'] = df['Reviews'].str.split('|').str[0]
df['Review Number'] = df['Reviews'].str.split('|').str[1]
df['Categories'] = df['Categories'].apply(lambda x: x.split(', '))
df['Discount'] = df['Discount'].apply(lambda x: float(
    x.replace('%', '').replace('-', '')) / 100 if isinstance(x, str) and x != '0' else float(x))
df['Description'] = df['Description'].str.strip()


def format_date(date_str):
    date_str = date_str.strip()
    date_obj = datetime.strptime(date_str, '%d %b, %Y')
    return date_obj.strftime('%B %d, %Y')


df['Release Date'] = df['Release Date'].apply(format_date)

new_order = ['Title', 'Description', 'Discount', 'Previous Price', 'Current Price',
             'Categories', 'Release Date', 'Reviews', 'Review Summary', 'Review Number', 'Link', 'ID']

# Reorder the columns
df = df.reindex(columns=new_order)

print(df.columns)
# Convert the DataFrame to a list of dictionaries
data = df.to_dict('records')

# Open a new JSON file and write the data to it
with open('betaGamesFormatted.json', 'w') as f:
    json.dump(data, f)
