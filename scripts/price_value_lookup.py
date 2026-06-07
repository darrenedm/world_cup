#!/usr/bin/env python3
"""
price_value_lookup.py
Cross-references the fantasy price list against master_sheet.csv.
Outputs adj_exp_fantasy_pts / price (pts per price unit), sorted descending.
"""
import csv

DATA_PATH = '/tmp/wc_repo/data/master_sheet.csv'

SHEETED = {
    # All 48 WC 2026 nations — sheets complete
    'Argentina','Australia','Austria','Belgium','Bosnia','Brazil','Canada',
    'Cape Verde','Colombia','Croatia','Curaçao','Czech Republic','DR Congo',
    'Ecuador','Egypt','England','France','Germany','Ghana','Haiti','Iran',
    'Iraq','Ivory Coast','Japan','Jordan','Mexico','Morocco','Netherlands',
    'New Zealand','Norway','Panama','Paraguay','Portugal','Qatar','Saudi Arabia',
    'Scotland','Senegal','South Africa','South Korea','Spain','Sweden',
    'Switzerland','Tunisia','Turkey','Uruguay','USA','Uzbekistan',
}

NOT_IN_WC = {
    # Nation didn't qualify — player has no WC expected pts by definition
    'Italy','Georgia','Slovenia','Kosovo','Burkina Faso','Cameroon',
    'Guinea','Denmark','Hungary','Wales','Scotland (no)','Senegal (no)',
}

# price_list: display_name → (price, full_name_in_master_sheet or None to auto-search)
# None means use the display_name fragment to find the player
PRICE_LIST = [
    # ── prices updated June 2 2026 ───────────────────────────────────────────
    ("Lamine Yamal",     0.0888,  "Lamine Yamal"),
    ("Mbappé",           0.0730,  "Kylian Mbappé"),
    ("Olise",            0.0637,  "Michael Olise"),
    ("Kane",             0.0562,  "Harry Kane"),
    ("Bruno Fernandes",  0.0513,  "Bruno Fernandes"),
    ("Pedri",            0.0368,  "Pedri"),
    ("Vitinha",          0.0359,  "Vitinha"),
    ("Haaland",          0.0332,  "Erling Haaland"),
    ("Vinícius Júnior",  0.0306,  "Vinícius Júnior"),
    ("Kimmich",          0.0302,  "Joshua Kimmich"),
    ("Rice",             0.0293,  "Declan Rice"),
    ("Doku",             0.0288,  "Jérémy Doku"),
    ("Wirtz",            0.0285,  "Florian Wirtz"),
    ("Dembélé",          0.0281,  "Ousmane Dembélé"),
    ("Raphinha",         0.0278,  "Raphinha"),
    ("Maignan",          0.0274,  "Mike Maignan"),
    ("Nuno Mendes",      0.0249,  "Nuno Mendes"),
    ("Alvarez",          0.0245,  "Julián Álvarez"),
    ("Díaz",             0.0244,  "Luis Díaz"),
    ("Gabriel Magalhães",0.0242,  "Gabriel Magalhães"),
    ("Schlotterbeck",    0.0240,  "Nico Schlotterbeck"),
    ("Cubarsí",          0.0237,  "Pau Cubarsí"),
    ("Upamecano",        0.0232,  "Dayot Upamecano"),
    ("Simón",            0.0228,  "Unai Simón"),
    ("Cucurella",        0.0227,  "Marc Cucurella"),
    ("Rúben Dias",       0.0224,  "Rúben Dias"),
    ("Tah",              0.0224,  "Jonathan Tah"),
    ("Hakimi",           0.0223,  "Achraf Hakimi"),
    ("Bellingham",       0.0223,  "Jude Bellingham"),
    ("Pickford",         0.0222,  "Jordan Pickford"),
    ("Martínez (AR)",    0.0221,  "Emiliano Martínez"),
    ("Guéhi",            0.0215,  "Marc Guéhi"),
    ("Rodri",            0.0212,  "Rodri"),
    ("João Neves",       0.0211,  "João Neves"),
    ("van Dijk",         0.0210,  "Virgil van Dijk"),
    ("Saka",             0.0209,  "Bukayo Saka"),
    ("Konsa",            0.0207,  "Ezri Konsa"),
    ("Saliba",           0.0206,  "William Saliba"),
    ("Anderson",         0.0203,  "Elliot Anderson"),
    ("Doué",             0.0198,  "Désiré Doué|France"),
    ("Matheus Cunha",    0.0185,  "Matheus Cunha"),
    ("Koundé",           0.0185,  "Jules Koundé"),
    ("Courtois",         0.0182,  "Thibaut Courtois"),
    ("Porro",            0.0180,  "Pedro Porro"),
    ("Cherki",           0.0178,  "Rayan Cherki"),
    ("Romero",           0.0172,  "Cristian Romero"),
    ("Kobel",            0.0170,  "Gregor Kobel"),
    ("Alisson Becker",   0.0169,  "Alisson Becker"),
    ("Fernández",        0.0167,  "Enzo Fernández"),
    ("Yildiz",           0.0160,  "Kenan Yıldız"),
    ("Güler",            0.0159,  "Arda Güler"),
    ("Dumfries",         0.0154,  "Denzel Dumfries"),
    ("Ruiz",             0.0153,  "Fabián Ruiz"),
    ("Raya",             0.0151,  "David Raya"),
    ("Valverde",         0.0151,  "Federico Valverde"),
    ("Ødegaard",         0.0149,  "Martin Ødegaard"),
    ("Gvardiol",         0.0146,  "Joško Gvardiol"),
    ("De Bruyne",        0.0144,  "Kevin De Bruyne"),
    ("Neuer",            0.0139,  "Manuel Neuer"),
    ("Jurriën Timber",   0.0138,  "Jurriën Timber"),
    ("Çalhanoğlu",       0.0135,  "Hakan Çalhanoğlu"),
    ("Pulisic",          0.0126,  "Christian Pulisic"),
    ("Pedro Neto",       0.0125,  "Pedro Neto"),
    ("Olmo",             0.0125,  "Dani Olmo"),
    ("Lautaro Martínez", 0.0120,  "Lautaro Martínez"),
    ("Gyökeres",         0.0118,  "Viktor Gyökeres"),
    ("McTominay",        0.0114,  "Scott McTominay"),
    ("Caicedo",          0.0105,  "Moisés Caicedo"),
    ("Gravenberch",      0.0105,  "Ryan Gravenberch"),
    ("Rafael Leão",      0.00996, "Rafael Leão"),
    ("Isak",             0.00923, "Alexander Isak"),
    ("Nmecha",           0.00865, "Felix Nmecha"),
    ("Watkins",          0.00812, "Ollie Watkins"),
    ("Kvaratskhelia",    0.00809, None),   # Georgia — not in WC
    ("Joan García",      0.00783, "Joan García"),
    ("Omar Marmoush",    0.00765, "Omar Marmoush"),
    ("Woltemade",        0.00748, "Nick Woltemade"),
    ("Grimaldo",         0.00734, "Alejandro Grimaldo"),
    ("Rashford",         0.00722, "Marcus Rashford"),
    ("Huijsen",          0.00722, "Dean Huijsen"),
    ("Palmer",           0.00721, "Cole Palmer"),
    ("Diallo",           0.00706, "Amad Diallo"),
    ("Mohamed Salah",    0.00691, "Mohamed Salah"),
    ("Donnarumma",       0.00655, None),   # Italy — not in WC
    ("Eze",              0.00653, "Eberechi Eze"),
    ("Bastoni",          0.00636, None),   # Italy — not in WC
    ("Lukaku",           0.00635, "Romelu Lukaku"),
    ("Amir Rrahmani",    0.00573, None),   # Kosovo — not in WC
    ("Svensson",         0.00547, "Daniel Svensson"),
    ("Greenwood",        0.00544, "Mason Greenwood"),
    ("Le Normand",       0.00539, "Robin Le Normand"),
    ("Jonathan David",   0.00537, "Jonathan David"),
    ("Akliouche",        0.00536, "Maghnes Akliouche"),
    ("Tillman",          0.00533, "Malik Tillman"),
    ("Stiller",          0.00509, "Angelo Stiller"),
    ("João Pedro",       0.00506, "João Pedro"),
    ("Alexander-Arnold", 0.00498, "Trent Alexander-Arnold"),
    ("Quansah",          0.00488, "Jarell Quansah"),
    ("Foden",            0.00486, "Phil Foden"),
    ("Trafford",         0.00463, "James Trafford"),
    ("Palacios",         0.00461, "Exequiel Palacios"),
    ("Dean Henderson",   0.00461, "Dean Henderson"),
    ("Locatelli",        0.00450, None),   # Italy — not in WC
    ("Flekken",          0.00401, "Mark Flekken"),
    ("Gibbs-White",      0.00395, "Morgan Gibbs-White"),
    ("Tapsoba",          0.00392, None),   # Burkina Faso — not in WC
    ("Mittelstädt",      0.00359, "Maximilian Mittelstädt"),
    ("Ekitiké",          0.00343, "Hugo Ekitiké"),
    ("Mbeumo",           0.00333, None),   # Cameroon — not in WC
    ("Antony",           0.00327, "Antony"),
    ("Oblak",            0.00322, None),   # Slovenia — not in WC
    ("Di Lorenzo",       0.00320, None),   # Italy — not in WC
    ("Carreras",         0.00302, "Álvaro Carreras"),
    ("Rulli",            0.00297, "Gerónimo Rulli"),
    ("Kerkez",           0.00291, None),   # Hungary — not in WC
    ("Barella",          0.00287, None),   # Italy — not in WC
    ("Tonali",           0.00287, None),   # Italy — not in WC
    ("Romagnoli",        0.00276, None),   # Italy — not in WC
    ("Vicario",          0.00276, None),   # Italy — not in WC
    ("Di Gregorio",      0.00269, None),   # Italy — not in WC
    ("Guirassy",         0.00269, None),   # Guinea — not in WC
    ("Kudus",            0.00250, "Mohammed Kudus"),
    ("Éder Militão",     0.00247, None),   # Brazil — not tracked (not in squad)
    ("Burkardt",         0.00245, "Jonathan Burkardt"),
    ("Bellingham (BVB)", 0.00240, "Jobe Bellingham"),
    ("Pavlovic (ACM)",   0.00213, None),   # Serbia (didn't qualify)
    ("Sánchez",          0.00233, "Robert Sánchez"),
    ("Soulé",            0.00226, "Matías Soulé"),
    ("Højlund",          0.00214, None),   # Denmark — not in WC
    ("Chevalier",        0.00214, "Lucas Chevalier"),
    ("Højbjerg",         0.00206, None),   # Denmark — not in WC
    ("Gnabry",           0.00198, "Serge Gnabry"),
    ("Sels",             0.00197, "Matz Sels"),
    ("Adeyemi",          0.00192, "Karim Adeyemi"),
    ("Yoro",             0.00190, "Leny Yoro"),
    ("Simons",           0.00186, None),   # Netherlands — OUT ACL, not in squad
    ("Aina",             0.00172, None),   # Nigeria — not in WC
    ("Rodon",            0.00158, None),   # Wales — not in WC
    ("Pope",             0.00149, "Nick Pope"),
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

# Players with stale (non-100%) squad probabilities — not in confirmed 26-man squad
STALE_PROB = {
    "Álvaro Carreras":   10,
}

# Confirmed not in WC squad as of June 2 2026 (web-verified, overrides master sheet)
CONFIRMED_OUT = {
    "Le Normand",   # Spain — omitted from final 26 (knee injury)
    "Kudus",        # Ghana — quad surgery + hamstring relapse, absent
    "Huijsen",      # Spain — surprise cut from final 26
    "Soulé",        # Argentina — cut from final 26
    "Sánchez",      # Spain — three GKs are Simón, Raya, Joan García
}

# Web-verified fitness (full/mostly/not) and national-team starter (yes/sometimes/no)
# Sourced from June 2026 reports; overrides master-sheet static fields
LIVE_STATUS = {
    "Palacios":          ("mostly",  "yes"),    # adductor surgery Sep; returned
    "Tillman":           ("full",    "yes"),
    "Le Normand":        ("not",     "no"),     # confirmed not in squad
    "Woltemade":         ("full",    "yes"),
    "Grimaldo":          ("full",    "yes"),
    "Lukaku":            ("mostly",  "yes"),    # 69 mins all season; rebuilding
    "Rafael Leão":       ("mostly",  "yes"),    # recurring adductor issues
    "Jonathan David":    ("mostly",  "yes"),    # hip surgery Feb; poor form
    "Gravenberch":       ("full",    "yes"),
    "Mohamed Salah":     ("mostly",  "yes"),    # hamstring ended Liverpool season
    "Lautaro Martínez":  ("mostly",  "yes"),    # two muscle injuries Feb & Apr
    "Kudus":             ("not",     "no"),     # confirmed not in squad
    "Diallo":            ("full",    "yes"),
    "Svensson":          ("full",    "yes"),
    "Pulisic":           ("mostly",  "yes"),    # gluteal strain late May
    "Ruiz":              ("full",    "yes"),
    "Stiller":           ("full",    "sometimes"),
    "De Bruyne":         ("mostly",  "yes"),    # high-grade thigh tear Oct; in friendlies
    "Çalhanoğlu":        ("mostly",  "yes"),    # soleus strain May; in final squad
    "Fernández":         ("full",    "yes"),
    "Akliouche":         ("full",    "sometimes"),
    "Olmo":              ("full",    "yes"),
    "Caicedo":           ("full",    "yes"),
    "Koundé":            ("mostly",  "yes"),    # minor pre-tournament issue
    "Eze":               ("mostly",  "sometimes"), # calf injury Mar; recovered
    "Romero":            ("mostly",  "yes"),    # knee sprain Apr; targeting Jun 6
    "Porro":             ("full",    "sometimes"),  # Cucurella/Grimaldo likely ahead
    "McTominay":         ("full",    "yes"),
    "Rodri":             ("mostly",  "yes"),    # ACL recovery complete; managed
    "Neuer":             ("mostly",  "yes"),    # calf injury May 16; back in training
    "Rashford":          ("full",    "sometimes"),
    "João Neves":        ("full",    "sometimes"),  # competing with Vitinha/R.Neves
    "Bellingham":        ("full",    "yes"),    # hamstring resolved; No.10
    "Jurriën Timber":    ("mostly",  "yes"),    # groin Mar; carefully managed
    "Saliba":            ("mostly",  "yes"),    # back injury aggravated UCL final
    "Saka":              ("mostly",  "yes"),    # Achilles; rested NZ friendly
    "Gvardiol":          ("mostly",  "yes"),    # recovered from broken leg Jan
    "Dumfries":          ("full",    "yes"),
    "Anderson":          ("full",    "yes"),
    "Valverde":          ("mostly",  "yes"),    # lumbosciatica; named in squad May 31
    "Güler":             ("full",    "yes"),    # biceps femoris recovered
    "Omar Marmoush":     ("full",    "yes"),
    "Upamecano":         ("full",    "yes"),
    "Yildiz":            ("full",    "yes"),    # confirmed fit by Montella
    "Cucurella":         ("full",    "yes"),
    "Guéhi":             ("full",    "yes"),
    "Kimmich":           ("full",    "yes"),
    "Konsa":             ("full",    "yes"),
    "Rúben Dias":        ("mostly",  "yes"),    # hamstring since mid-Mar; in squad
    "Nuno Mendes":       ("mostly",  "yes"),    # injury history; managed
    "van Dijk":          ("full",    "yes"),
    "Cubarsí":           ("mostly",  "yes"),    # finger splint; not affecting availability
    "Tah":               ("full",    "yes"),
    "Ødegaard":          ("mostly",  "yes"),    # injury-plagued season; squad captain
    "Watkins":           ("full",    "no"),     # Kane's backup
    "Raphinha":          ("mostly",  "yes"),    # hamstring mid-May Brazil friendly
    "Dembélé":           ("mostly",  "yes"),    # cramped off CL final May 30
    "Díaz":              ("full",    "yes"),
    "Alisson Becker":    ("mostly",  "yes"),    # hamstring; targeting Jun 16
    "Rice":              ("full",    "yes"),
    "Schlotterbeck":     ("mostly",  "yes"),    # torn meniscus Apr; recovered ahead of schedule
    "Courtois":          ("mostly",  "yes"),    # thigh Mar; recovered
    "Huijsen":           ("not",     "no"),     # confirmed not in squad
    "Gyökeres":          ("full",    "yes"),
    "Martínez (AR)":     ("mostly",  "yes"),    # broken finger Europa League final
    "Isak":              ("mostly",  "yes"),    # fibula/ankle Dec; scored Jun 1
    "Pedri":             ("full",    "yes"),
    "Wirtz":             ("mostly",  "yes"),    # back issue; says 'really sharp'
    "Pickford":          ("full",    "yes"),
    "Vitinha":           ("mostly",  "yes"),    # heel inflammation; healing
    "Kobel":             ("full",    "yes"),
    "Gabriel Magalhães": ("full",    "yes"),
    "Simón":             ("full",    "yes"),
    "Vinícius Júnior":   ("mostly",  "yes"),    # minor calf/fatigue May 22
    "Hakimi":            ("mostly",  "yes"),    # hamstring Apr; precautionary rest
    "Quansah":           ("full",    "no"),
    "Alvarez":           ("mostly",  "yes"),    # ankle; cleared June 2
    "Maignan":           ("full",    "yes"),
    "Pedro Neto":        ("mostly",  "sometimes"),
    "Doku":              ("full",    "yes"),
    "Olise":             ("full",    "yes"),
    "Cherki":            ("full",    "no"),     # clear impact-sub behind Dembélé/Olise/Barcola
    "Bruno Fernandes":   ("full",    "yes"),
    "Kane":              ("full",    "yes"),
    "Doué":              ("full",    "no"),     # behind confirmed starters
    "Mbappé":            ("mostly",  "yes"),    # hamstring re-aggravated ~Jun 1; doubt G1
    "Nmecha":            ("mostly",  "no"),     # knee ligament Mar; 2 games back
    "Haaland":           ("full",    "yes"),
    "Lamine Yamal":      ("mostly",  "yes"),    # misses G1; doubt G2; targets G3 Jun 26
    "Matheus Cunha":     ("mostly",  "yes"),    # adductor managed; projects as starter
    "Soulé":             ("not",     "no"),     # confirmed not in squad
    "Rulli":             ("full",    "no"),
    "Flekken":           ("mostly",  "no"),     # missed much of second half injured
    "Dean Henderson":    ("full",    "no"),
    "Carreras":          ("full",    "no"),
    "Trafford":          ("full",    "no"),
    "Raya":              ("full",    "no"),
    "Sánchez":           ("not",     "no"),     # confirmed not in Spain squad
}


# G1 win probability (%) per nation — Polymarket/Dimers, June 7 2026
# Key: nationality string as it appears in master_sheet
G1_WIN = {
    'Argentina':     70,   # vs Algeria Jun 16       (Polymarket/Dimers)
    'USA':           50,   # vs Paraguay Jun 12       (Polymarket)
    'Germany':       95,   # vs Curaçao Jun 14        (Polymarket)
    'Spain':         91,   # vs Cape Verde Jun 15     (Polymarket)
    'Belgium':       59,   # vs Egypt Jun 15          (Polymarket)
    'Portugal':      73,   # vs DR Congo Jun 17       (Dimers)
    'Canada':        55,   # vs Bosnia Jun 12         (Polymarket)
    'Netherlands':   49,   # vs Japan Jun 14          (Polymarket)
    'Egypt':         17,   # vs Belgium Jun 15        (Polymarket)
    'Ivory Coast':   27,   # vs Ecuador Jun 14        (Polymarket)
    'Sweden':        51,   # vs Tunisia Jun 14        (Polymarket)
    'Turkey':        56,   # vs Australia Jun 14      (Polymarket)
    'France':        63,   # vs Senegal Jun 16        (Dimers)
    'Ecuador':       40,   # vs Ivory Coast Jun 14    (Polymarket)
    'Scotland':      66,   # vs Haiti Jun 13          (Polymarket)
    'England':       56,   # vs Croatia Jun 17        (Dimers/bet365)
    'Croatia':       19,   # vs England Jun 17        (Dimers/bet365)
    'Uruguay':       67,   # vs Saudi Arabia Jun 15   (Polymarket)
    'Morocco':       17,   # vs Brazil Jun 13         (Polymarket)
    'Brazil':        61,   # vs Morocco Jun 13        (Polymarket)
    'Colombia':      67,   # vs Uzbekistan Jun 17     (Dimers)
    'Norway':        76,   # vs Iraq Jun 16           (Dimers)
    'Switzerland':   80,   # vs Qatar Jun 13          (Polymarket)
    'Mexico':        69,   # vs South Africa Jun 11   (Polymarket)
    'South Korea':   37,   # vs Czechia Jun 11        (Polymarket)
    'Czech Republic':34,   # vs South Korea Jun 11    (Polymarket)
    'Japan':         27,   # vs Netherlands Jun 14    (Polymarket)
    'Tunisia':       23,   # vs Sweden Jun 14         (Polymarket)
    'Iran':          53,   # vs New Zealand Jun 15    (Dimers)
    'New Zealand':   21,   # vs Iran Jun 15           (Dimers)
    'Saudi Arabia':  13,   # vs Uruguay Jun 15        (Polymarket)
    'Qatar':          7,   # vs Switzerland Jun 13    (Polymarket)
    'Ghana':         41,   # vs Panama Jun 17         (Dimers)
    'Panama':        33,   # vs Ghana Jun 17          (Dimers)
    'Australia':     19,   # vs Turkey Jun 14         (Polymarket)
    'South Africa':  11,   # vs Mexico Jun 11         (Polymarket)
    'Senegal':       15,   # vs France Jun 16         (Dimers)
    'Algeria':       11,   # vs Argentina Jun 16      (Dimers)
    'Bosnia':        20,   # vs Canada Jun 12         (Polymarket)
    'DR Congo':       9,   # vs Portugal Jun 17       (Dimers)
    'Uzbekistan':    13,   # vs Colombia Jun 17       (Dimers)
    'Iraq':           9,   # vs Norway Jun 16         (Dimers)
    'Jordan':        13,   # vs Austria Jun 16        (Dimers)
    'Paraguay':      24,   # vs USA Jun 12            (Polymarket)
    'Curaçao':        2,   # vs Germany Jun 14        (Polymarket)
    'Haiti':         15,   # vs Scotland Jun 13       (Polymarket)
    'Cape Verde':     4,   # vs Spain Jun 15          (Polymarket)
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

        # Confirmed not in final WC squad (web-verified June 2 2026)
        if display in CONFIRMED_OUT:
            not_wc.append((display, price, f"⛔ confirmed not in WC squad ({nat})"))
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

        # ── Live fitness & starter (web-verified) ─────────────────────────────
        live = LIVE_STATUS.get(display, ("?", "?"))
        fit_label     = live[0]   # full / mostly / not
        starter_label = live[1]   # yes / sometimes / no

        g1_win = G1_WIN.get(nat, 0)

        results.append((display, full_name, nat, pos, price, adj_pts, pts_per_price, status, fit_label, starter_label, g1_win))

    # Sort by pts/price descending
    results.sort(key=lambda x: -x[6])

    # ── Print main table ─────────────────────────────────────────────────────
    print("# Fantasy Value Table — Adj Pts per Price Unit")
    print("# Fitness: full/mostly/not  |  Starter: yes/sometimes/no  |  G1 Win%: Polymarket/Dimers Jun 7 2026\n")
    print(f"{'#':<4} {'Player':<24} {'Nat':<14} {'Pos':<4} {'Price':>8} {'Adj Pts':>8} {'Pts/$':>8}  {'Fitness':<8} {'Starter':<10} {'G1 Win%':>7}  Status")
    print("─" * 115)
    for i, (disp, full, nat, pos, price, pts, ppp, status, fit, starter, g1) in enumerate(results, 1):
        print(f"{i:<4} {disp:<24} {nat:<14} {pos:<4} {price:>8.5f} {pts:>8.1f} {ppp:>8.0f}  {fit:<8} {starter:<10} {g1:>6}%  {status}")

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
