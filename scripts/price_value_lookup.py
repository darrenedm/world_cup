#!/usr/bin/env python3
"""
price_value_lookup.py
Cross-references the fantasy price list against master_sheet.csv.
Outputs adj_exp_fantasy_pts / price (pts per price unit), sorted descending.
"""
import csv

DATA_PATH = '/tmp/wc_repo/data/master_sheet.csv'

SHEETED = {
    'Argentina','Australia','Austria','Belgium','Brazil','Canada','Cape Verde',
    'Colombia','Croatia','DR Congo','Ecuador','England','France','Germany',
    'Iran','Ivory Coast','Japan','Morocco','Netherlands','Norway','Panama',
    'Portugal','Scotland','Senegal','South Africa','South Korea','Spain',
    'Sweden','Switzerland','Tunisia','Turkey','USA',
}

NOT_IN_WC = {
    # Nation didn't qualify — player has no WC expected pts by definition
    'Italy','Georgia','Slovenia','Kosovo','Burkina Faso','Cameroon',
    'Guinea','Denmark','Hungary','Wales','Scotland (no)','Senegal (no)',
}

# price_list: display_name → (price, full_name_in_master_sheet or None to auto-search)
# None means use the display_name fragment to find the player
PRICE_LIST = [
    # ── Page 1 ──────────────────────────────────────────────────────────────
    ("Mbappé",           0.0706,  "Kylian Mbappé"),
    ("Lamine Yamal",     0.0675,  "Lamine Yamal"),
    ("Olise",            0.0650,  "Michael Olise"),
    ("Kane",             0.0581,  "Harry Kane"),
    ("Bruno Fernandes",  0.0495,  "Bruno Fernandes"),
    ("Pedri",            0.0343,  "Pedri"),
    ("Haaland",          0.0340,  "Erling Haaland"),
    ("Vitinha",          0.0327,  "Vitinha"),
    ("Dembélé",          0.0318,  "Ousmane Dembélé"),
    ("Maignan",          0.0300,  "Mike Maignan"),
    ("Rice",             0.0300,  "Declan Rice"),
    ("Kimmich",          0.0288,  "Joshua Kimmich"),
    ("Doku",             0.0287,  "Jérémy Doku"),
    ("Saliba",           0.0277,  "William Saliba"),
    ("Raphinha",         0.0275,  "Raphinha"),
    ("Wirtz",            0.0271,  "Florian Wirtz"),
    ("Alvarez",          0.0269,  "Julián Álvarez"),
    ("Vinícius Júnior",  0.0267,  "Vinícius Júnior"),
    ("Nuno Mendes",      0.0266,  "Nuno Mendes"),
    ("Gabriel Magalhães",0.0250,  "Gabriel Magalhães"),
    # ── Page 2 ──────────────────────────────────────────────────────────────
    ("Cubarsí",          0.0234,  "Pau Cubarsí"),
    ("Simón",            0.0233,  "Unai Simón"),
    ("Schlotterbeck",    0.0230,  "Nico Schlotterbeck"),
    ("Saka",             0.0229,  "Bukayo Saka"),
    ("Hakimi",           0.0228,  "Achraf Hakimi"),
    ("Martínez (AVL)",   0.0224,  "Emiliano Martínez"),
    ("Upamecano",        0.0223,  "Dayot Upamecano"),
    ("Pickford",         0.0223,  "Jordan Pickford"),
    ("Bellingham (RMD)", 0.0222,  "Jude Bellingham"),
    ("Doué",             0.0217,  "Désiré Doué|France"),  # two entries exist; use France one
    ("Guéhi",            0.0215,  "Marc Guéhi"),
    ("Cucurella",        0.0210,  "Marc Cucurella"),
    ("Rúben Dias",       0.0209,  "Rúben Dias"),
    ("João Neves",       0.0208,  "João Neves"),
    ("Tah",              0.0205,  "Jonathan Tah"),
    ("Rodri",            0.0203,  "Rodri"),
    ("van Dijk",         0.0203,  "Virgil van Dijk"),
    ("Díaz (FCB)",       0.0200,  "Luis Díaz"),
    ("Cherki",           0.0197,  "Rayan Cherki"),
    ("Anderson (NFO)",   0.0187,  "Elliot Anderson"),
    # ── Page 3 ──────────────────────────────────────────────────────────────
    ("Courtois",         0.0182,  "Thibaut Courtois"),
    ("Porro",            0.0179,  "Pedro Porro"),
    ("Koundé",           0.0175,  "Jules Koundé"),
    ("Raya",             0.0172,  "David Raya"),
    ("Alisson Becker",   0.0170,  "Alisson Becker"),
    ("Konsa",            0.0170,  "Ezri Konsa"),
    ("Matheus Cunha",    0.0168,  "Matheus Cunha"),
    ("Fernández (CHE)",  0.0165,  "Enzo Fernández"),
    ("Ødegaard",         0.0163,  "Martin Ødegaard"),
    ("Kobel",            0.0162,  "Gregor Kobel"),
    ("Ruiz",             0.0160,  "Fabián Ruiz"),
    ("Yildiz",           0.0149,  "Kenan Yıldız"),
    ("De Bruyne",        0.0147,  "Kevin De Bruyne"),
    ("Valverde",         0.0144,  "Federico Valverde"),
    ("Güler",            0.0144,  "Arda Güler"),
    ("Romero",           0.0143,  "Cristian Romero"),
    ("Jurriën Timber",   0.0138,  "Jurriën Timber"),
    ("Gvardiol",         0.0138,  "Joško Gvardiol"),
    ("Neuer",            0.0138,  "Manuel Neuer"),
    ("Çalhanoglu",       0.0137,  "Hakan Çalhanoğlu"),
    # ── Page 4 ──────────────────────────────────────────────────────────────
    ("Dumfries",         0.0133,  "Denzel Dumfries"),
    ("Gyökeres",         0.0130,  "Viktor Gyökeres"),
    ("Pedro Neto",       0.0125,  "Pedro Neto"),
    ("Lautaro Martínez", 0.0123,  "Lautaro Martínez"),
    ("Olmo",             0.0121,  "Dani Olmo"),
    ("McTominay",        0.0116,  "Scott McTominay"),
    ("Pulisic",          0.0115,  "Christian Pulisic"),
    ("Gravenberch",      0.0108,  "Ryan Gravenberch"),
    ("Caicedo",          0.00998, "Moisés Caicedo"),
    ("Kvaratskhelia",    0.00856, None),   # Georgia — not in WC
    ("Rafael Leão",      0.00827, "Rafael Leão"),
    ("Nmecha",           0.00822, "Felix Nmecha"),
    ("Watkins",          0.00809, "Ollie Watkins"),
    ("Huijsen",          0.00803, "Dean Huijsen"),
    ("Joan García",      0.00786, "Joan García"),
    ("Rashford",         0.00779, "Marcus Rashford"),
    ("Omar Marmoush",    0.00752, "Omar Marmoush"),
    ("Woltemade",        0.00751, "Nick Woltemade"),
    ("Palmer",           0.00724, "Cole Palmer"),
    ("Grimaldo",         0.00709, "Alejandro Grimaldo"),
    # ── Page 5 ──────────────────────────────────────────────────────────────
    ("Mohamed Salah",    0.00687, "Mohamed Salah"),
    ("Isak",             0.00683, "Alexander Isak"),
    ("Donnarumma",       0.00682, None),   # Italy — not in WC
    ("Diallo",           0.00664, "Amad Diallo"),
    ("Eze",              0.00662, "Eberechi Eze"),
    ("Bastoni",          0.00612, None),   # Italy — not in WC
    ("Amir Rrahmani",    0.00577, None),   # Kosovo — not in WC
    ("Stiller",          0.00564, "Angelo Stiller"),
    ("Le Normand",       0.00552, "Robin Le Normand"),
    ("Greenwood",        0.00536, "Mason Greenwood"),
    ("Tillman",          0.00524, "Malik Tillman"),
    ("Jonathan David",   0.00520, "Jonathan David"),
    ("Lukaku",           0.00511, "Romelu Lukaku"),
    ("Akliouche",        0.00498, "Maghnes Akliouche"),
    ("Alexander-Arnold", 0.00493, "Trent Alexander-Arnold"),
    ("João Pedro",       0.00491, "João Pedro"),
    ("Svensson",         0.00488, "Daniel Svensson"),
    ("Foden",            0.00486, "Phil Foden"),
    ("Quansah",          0.00478, "Jarell Quansah"),
    ("Trafford",         0.00466, "James Trafford"),
    # ── Page 6 ──────────────────────────────────────────────────────────────
    ("Dean Henderson",   0.00464, "Dean Henderson"),
    ("Palacios",         0.00450, "Exequiel Palacios"),
    ("Locatelli",        0.00437, None),   # Italy — not in WC
    ("Flekken",          0.00401, "Mark Flekken"),
    ("Tapsoba",          0.00398, None),   # Burkina Faso — not in WC
    ("Gibbs-White",      0.00388, "Morgan Gibbs-White"),  # England — NOT in squad (0%)
    ("Mittelstädt",      0.00353, "Maximilian Mittelstädt"),
    ("Ekitiké",          0.00340, "Hugo Ekitiké"),
    ("Antony",           0.00337, "Antony"),
    ("Mbeumo",           0.00330, None),   # Cameroon — not in WC
    ("Oblak",            0.00329, None),   # Slovenia — not in WC
    ("Di Lorenzo",       0.00319, None),   # Italy — not in WC
    ("Carreras",         0.00311, "Álvaro Carreras"),
    ("Barella",          0.00290, None),   # Italy — not in WC
    ("Tonali",           0.00287, None),   # Italy — not in WC
    ("Romagnoli",        0.00277, None),   # Italy — not in WC
    ("Kerkez",           0.00274, None),   # Hungary — not in WC
    ("Vicario",          0.00271, None),   # Italy — not in WC
    ("Rulli",            0.00271, "Gerónimo Rulli"),
    ("Guirassy",         0.00258, None),   # Guinea — not in WC
    # ── Page 7 ──────────────────────────────────────────────────────────────
    ("Di Gregorio",      0.00253, None),   # Italy — not in WC
    ("Kudus",            0.00251, "Mohammed Kudus"),
    ("Éder Militão",     0.00248, None),        # Brazil DEF — not in squad / not tracked
    ("Burkardt",         0.00245, "Jonathan Burkardt"),
    ("Bellingham (BVB)", 0.00240, "Jobe Bellingham"),
    ("Pavlovic (ACM)",   0.00240, None),    # Strahinja Pavlović — Serbia (didn't qualify)
    ("Sánchez",          0.00229, "Robert Sánchez"),
    ("Soulé",            0.00227, "Matías Soulé"),
    ("Højlund",          0.00215, None),   # Denmark — not in WC
    ("Chevalier",        0.00212, "Lucas Chevalier"),
    ("Højbjerg",         0.00202, None),   # Denmark — not in WC
    ("Gnabry",           0.00198, "Serge Gnabry"),
    ("Sels",             0.00195, "Matz Sels"),
    ("Yoro",             0.00190, "Leny Yoro"),
    ("Simons",           0.00183, None),        # Xavi Simons — Netherlands, OUT (ACL), not in squad
    ("Adeyemi",          0.00175, "Karim Adeyemi"),
    ("Aina",             0.00170, None),   # Nigeria — not in WC
    ("Rodon",            0.00158, None),   # Wales — not in WC
    ("Pope",             0.00150, "Nick Pope"),
]

# Players not in WC at all (name→reason)
NOT_WC_NAMES = {
    "Pavlovic (ACM)":      "Serbia/Strahinja Pavlović (didn't qualify)",
    "Simons":              "Netherlands — OUT ACL, not in squad",
    "Éder Militão":        "Brazil — not in squad / not tracked",
    "Kvaratskhelia":       "Georgia (didn't qualify)",
    "Donnarumma":          "Italy (didn't qualify)",
    "Bastoni":             "Italy (didn't qualify)",
    "Locatelli":           "Italy (didn't qualify)",
    "Di Lorenzo":          "Italy (didn't qualify)",
    "Barella":             "Italy (didn't qualify)",
    "Tonali":              "Italy (didn't qualify)",
    "Romagnoli":           "Italy (didn't qualify)",
    "Vicario":             "Italy (didn't qualify)",
    "Di Gregorio":         "Italy (didn't qualify)",
    "Tapsoba":             "Burkina Faso (didn't qualify)",
    "Mbeumo":              "Cameroon (didn't qualify)",
    "Oblak":               "Slovenia (didn't qualify)",
    "Guirassy":            "Guinea (didn't qualify)",
    "Kerkez":              "Hungary (didn't qualify)",
    "Aina":                "Nigeria (didn't qualify)",
    "Rodon":               "Wales (didn't qualify)",
    "Højlund":             "Denmark (didn't qualify)",
    "Højbjerg":            "Denmark (didn't qualify)",
    "Amir Rrahmani":       "Kosovo (didn't qualify)",
}

# Untracked nations (qualified but no sheet yet)
UNTRACKED = {'Mexico', 'Uruguay', 'Egypt', 'Algeria', 'Paraguay',
             'Czech Republic', 'Uzbekistan', 'Qatar', 'Iraq', 'Saudi Arabia',
             'Jordan', 'Bosnia', 'Ghana', 'Curaçao', 'Haiti', 'New Zealand'}


# Players with stale (non-100%) squad probabilities — not in confirmed 26-man squad
STALE_PROB = {
    "Robin Le Normand":  82,
    "Dean Huijsen":      78,
    "Matías Soulé":      22,
    "Álvaro Carreras":   10,
    "Robert Sánchez":    10,
}


def load_data():
    with open(DATA_PATH, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    # Build lookup: player → row (prefer higher adj_pts when duplicates exist)
    db = {}
    db_by_nat = {}   # (player, nationality) → row
    for r in rows:
        name = r['player']
        nat  = r['nationality']
        db_by_nat[(name, nat)] = r
        if name not in db or float(r['adj_exp_fantasy_pts']) > float(db[name]['adj_exp_fantasy_pts']):
            db[name] = r
    return db, db_by_nat


def main():
    db, db_by_nat = load_data()

    results  = []
    not_wc   = []
    not_found = []

    for display, price, full_name in PRICE_LIST:
        # Explicitly flagged as not in WC
        if full_name is None:
            not_wc.append((display, price, NOT_WC_NAMES.get(display, "Nation not in WC")))
            continue

        # Handle "Name|Nation" disambiguation
        force_nat = None
        if '|' in full_name:
            full_name, force_nat = full_name.split('|', 1)

        if force_nat:
            row = db_by_nat.get((full_name, force_nat))
        else:
            row = db.get(full_name)

        if row is None:
            not_found.append((display, price, full_name))
            continue

        adj_pts = float(row['adj_exp_fantasy_pts'])
        nat     = row['nationality']
        pos     = row['position']
        squad_p = int(float(row.get('wc_squad_prob_pct', '100')))

        if adj_pts == 0.0:
            if squad_p == 0:
                status = f"NOT IN SQUAD ({nat})"
            else:
                status = f"0 pts — OUT/unconfirmed ({nat})"
            not_wc.append((display, price, status))
            continue

        pts_per_price = adj_pts / price
        sheeted = nat in SHEETED

        stale_pct = STALE_PROB.get(full_name)
        if stale_pct:
            status = f"⚠️ unconfirmed ({stale_pct}% prob, {nat})"
        elif not sheeted:
            status = f"⚠️ not sheeted ({nat})"
        else:
            status = "✅"

        results.append((display, full_name, nat, pos, price, adj_pts, pts_per_price, status))

    # Sort by pts/price descending
    results.sort(key=lambda x: -x[6])

    # ── Print main table ─────────────────────────────────────────────────────
    print("# Fantasy Value Table — Adj Pts per Price Unit\n")
    print(f"{'#':<4} {'Player':<24} {'Nat':<14} {'Pos':<4} {'Price':>8} {'Adj Pts':>8} {'Pts/$':>8}  Status")
    print("─" * 85)
    for i, (disp, full, nat, pos, price, pts, ppp, status) in enumerate(results, 1):
        print(f"{i:<4} {disp:<24} {nat:<14} {pos:<4} {price:>8.5f} {pts:>8.1f} {ppp:>8.0f}  {status}")

    # ── Not in WC ────────────────────────────────────────────────────────────
    print(f"\n{'─'*60}")
    print("## Players not in WC / not in squad (excluded from ranking)\n")
    for disp, price, reason in not_wc:
        print(f"  {disp:<24} {price:.5f}  {reason}")

    # ── Not found ────────────────────────────────────────────────────────────
    if not_found:
        print(f"\n{'─'*60}")
        print("## Name not found in master_sheet (needs investigation)\n")
        for disp, price, fn in not_found:
            print(f"  {disp:<24} {price:.5f}  tried: '{fn}'")

    print(f"\nTotal ranked: {len(results)}  |  Excluded (not WC/squad): {len(not_wc)}  |  Not found: {len(not_found)}")


if __name__ == '__main__':
    main()
