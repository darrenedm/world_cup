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
    # ── prices updated June 7 2026 (tenero.io) ──────────────────────────────
    ("Lamine Yamal",     0.0613,  "Lamine Yamal"),
    ("Olise",            0.0516,  "Michael Olise"),
    ("Mbappé",           0.0496,  "Kylian Mbappé"),
    ("Bruno Fernandes",  0.0411,  "Bruno Fernandes"),
    ("Kane",             0.0396,  "Harry Kane"),
    ("Vitinha",          0.0310,  "Vitinha"),
    ("Pedri",            0.0299,  "Pedri"),
    ("Kimmich",          0.0276,  "Joshua Kimmich"),
    ("Haaland",          0.0270,  "Erling Haaland"),
    ("Vinícius Júnior",  0.0261,  "Vinícius Júnior"),
    ("Doku",             0.0251,  "Jérémy Doku"),
    ("Wirtz",            0.0248,  "Florian Wirtz"),
    ("Rice",             0.0248,  "Declan Rice"),
    ("Maignan",          0.0245,  "Mike Maignan"),
    ("Raphinha",         0.0224,  "Raphinha"),
    ("Díaz",             0.0213,  "Luis Díaz"),
    ("Cubarsí",          0.0211,  "Pau Cubarsí"),
    ("Gabriel Magalhães",0.0211,  "Gabriel Magalhães"),
    ("Dembélé",          0.0209,  "Ousmane Dembélé"),
    ("Schlotterbeck",    0.0204,  "Nico Schlotterbeck"),
    ("Nuno Mendes",      0.0204,  "Nuno Mendes"),
    ("van Dijk",         0.0202,  "Virgil van Dijk"),
    ("Simón",            0.0201,  "Unai Simón"),
    ("Anderson",         0.0201,  "Elliot Anderson"),
    ("João Neves",       0.0195,  "João Neves"),
    ("Tah",              0.0194,  "Jonathan Tah"),
    ("Cucurella",        0.0194,  "Marc Cucurella"),
    ("Rodri",            0.0191,  "Rodri"),
    ("Bellingham",       0.0189,  "Jude Bellingham"),
    ("Alvarez",          0.0188,  "Julián Álvarez"),
    ("Upamecano",        0.0187,  "Dayot Upamecano"),
    ("Konsa",            0.0185,  "Ezri Konsa"),
    ("Saka",             0.0185,  "Bukayo Saka"),
    ("Rúben Dias",       0.0185,  "Rúben Dias"),
    ("Pickford",         0.0185,  "Jordan Pickford"),
    ("Martínez (AR)",    0.0183,  "Emiliano Martínez"),
    ("Hakimi",           0.0181,  "Achraf Hakimi"),
    ("Guéhi",            0.0178,  "Marc Guéhi"),
    ("Saliba",           0.0176,  "William Saliba"),
    ("Matheus Cunha",    0.0174,  "Matheus Cunha"),
    ("Doué",             0.0169,  "Désiré Doué|France"),
    ("Porro",            0.0169,  "Pedro Porro"),
    ("Fernández",        0.0163,  "Enzo Fernández"),
    ("Koundé",           0.0162,  "Jules Koundé"),
    ("Ødegaard",         0.0162,  "Martin Ødegaard"),
    ("Alisson Becker",   0.0162,  "Alisson Becker"),
    ("Courtois",         0.0158,  "Thibaut Courtois"),
    ("Yildiz",           0.0154,  "Kenan Yıldız"),
    ("Kobel",            0.0146,  "Gregor Kobel"),
    ("Cherki",           0.0142,  "Rayan Cherki"),
    ("Güler",            0.0138,  "Arda Güler"),
    ("Dumfries",         0.0133,  "Denzel Dumfries"),
    ("Lautaro Martínez", 0.0131,  "Lautaro Martínez"),
    ("Ruiz",             0.0131,  "Fabián Ruiz"),
    ("De Bruyne",        0.0128,  "Kevin De Bruyne"),
    ("Gvardiol",         0.0128,  "Joško Gvardiol"),
    ("Romero",           0.0127,  "Cristian Romero"),
    ("Olmo",             0.0121,  "Dani Olmo"),
    ("Pedro Neto",       0.0121,  "Pedro Neto"),
    ("Jurriën Timber",   0.0120,  "Jurriën Timber"),
    ("Valverde",         0.0120,  "Federico Valverde"),
    ("Pulisic",          0.0116,  "Christian Pulisic"),
    ("Gyökeres",         0.0114,  "Viktor Gyökeres"),
    ("Neuer",            0.0113,  "Manuel Neuer"),
    ("Rafael Leão",      0.0109,  "Rafael Leão"),
    ("McTominay",        0.0107,  "Scott McTominay"),
    ("Raya",             0.0104,  "David Raya"),
    ("Çalhanoğlu",       0.0101,  "Hakan Çalhanoğlu"),
    ("Gravenberch",      0.0100,  "Ryan Gravenberch"),
    ("Rashford",         0.00900, "Marcus Rashford"),
    ("Caicedo",          0.00896, "Moisés Caicedo"),
    ("Isak",             0.00887, "Alexander Isak"),
    ("Nmecha",           0.00884, "Felix Nmecha"),
    ("Singo",            0.00856, "Wilfried Singo"),
    ("Joan García",      0.00823, "Joan García"),
    ("Grimaldo",         0.00781, "Alejandro Grimaldo"),
    ("Watkins",          0.00776, "Ollie Watkins"),
    ("Kvaratskhelia",    0.00760, None),   # Georgia — not in WC
    ("Omar Marmoush",    0.00733, "Omar Marmoush"),
    ("Diallo",           0.00730, "Amad Diallo"),
    ("Palmer",           0.00727, "Cole Palmer"),
    ("Huijsen",          0.00697, "Dean Huijsen"),
    ("Donnarumma",       0.00633, None),   # Italy — not in WC
    ("Mohamed Salah",    0.00630, "Mohamed Salah"),
    ("Bastoni",          0.00628, None),   # Italy — not in WC
    ("Woltemade",        0.00621, "Nick Woltemade"),
    ("Eze",              0.00615, "Eberechi Eze"),
    ("Lukaku",           0.00567, "Romelu Lukaku"),
    ("Amir Rrahmani",    0.00564, None),   # Kosovo — not in WC
    ("Svensson",         0.00542, "Daniel Svensson"),
    ("Akliouche",        0.00528, "Maghnes Akliouche"),
    ("Le Normand",       0.00527, "Robin Le Normand"),
    ("João Pedro",       0.00520, "João Pedro"),
    ("Jonathan David",   0.00518, "Jonathan David"),
    ("Alexander-Arnold", 0.00495, "Trent Alexander-Arnold"),
    ("Tillman",          0.00491, "Malik Tillman"),
    ("Foden",            0.00491, "Phil Foden"),
    ("Palacios",         0.00469, "Exequiel Palacios"),
    ("Quansah",          0.00469, "Jarell Quansah"),
    ("Locatelli",        0.00469, None),   # Italy — not in WC
    ("Trafford",         0.00458, "James Trafford"),
    ("Dean Henderson",   0.00457, "Dean Henderson"),
    ("Stiller",          0.00455, "Angelo Stiller"),
    ("Greenwood",        0.00433, "Mason Greenwood"),
    ("Gibbs-White",      0.00414, "Morgan Gibbs-White"),
    ("Flekken",          0.00406, "Mark Flekken"),
    ("Tapsoba",          0.00392, None),   # Burkina Faso — not in WC
    ("Mittelstädt",      0.00372, "Maximilian Mittelstädt"),
    ("Mbeumo",           0.00360, None),   # Cameroon — not in WC
    ("Ekitiké",          0.00340, "Hugo Ekitiké"),
    ("Oblak",            0.00334, None),   # Slovenia — not in WC
    ("Vicario",          0.00332, None),   # Italy — not in WC
    ("Barella",          0.00330, None),   # Italy — not in WC
    ("Di Lorenzo",       0.00322, None),   # Italy — not in WC
    ("Antony",           0.00317, "Antony"),
    ("Kerkez",           0.00305, None),   # Hungary — not in WC
    ("Tonali",           0.00303, None),   # Italy — not in WC
    ("Rulli",            0.00300, "Gerónimo Rulli"),
    ("Carreras",         0.00299, "Álvaro Carreras"),
    ("Guirassy",         0.00273, None),   # Guinea — not in WC
    ("Kudus",            0.00250, "Mohammed Kudus"),
    ("Éder Militão",     0.00247, None),   # Brazil — not in squad
    ("Burkardt",         0.00245, "Jonathan Burkardt"),
    ("Bellingham (BVB)", 0.00240, "Jobe Bellingham"),
    ("Sánchez",          0.00233, "Robert Sánchez"),
    ("Soulé",            0.00226, "Matías Soulé"),
    ("Romagnoli",        0.00220, None),   # Italy — not in WC
    ("Chevalier",        0.00214, "Lucas Chevalier"),
    ("Pavlovic (ACM)",   0.00213, None),   # Serbia (didn't qualify)
    ("Højlund",          0.00210, None),   # Denmark — not in WC
    ("Di Gregorio",      0.00200, None),   # Italy — not in WC
    ("Gnabry",           0.00198, "Serge Gnabry"),
    ("Sels",             0.00197, "Matz Sels"),
    ("Adeyemi",          0.00192, "Karim Adeyemi"),
    ("Yoro",             0.00190, "Leny Yoro"),
    ("Højbjerg",         0.00185, None),   # Denmark — not in WC
    ("Simons",           0.00180, None),   # Netherlands — OUT ACL
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
STALE_PROB = {}

# Confirmed not in WC squad as of June 2 2026 (web-verified, overrides master sheet)
CONFIRMED_OUT = {
    "Le Normand",   # Spain — omitted from final 26 (knee injury)
    "Kudus",        # Ghana — quad surgery + hamstring relapse, absent
    "Huijsen",      # Spain — surprise cut from final 26
    "Soulé",        # Argentina — cut from final 26
    "Sánchez",      # Spain — three GKs are Simón, Raya, Joan García
    "Carreras",     # Spain — no country flag on tenero; confirmed not in final squad
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
    "Singo":             ("full",    "yes"),    # Ivory Coast first-choice RB; no injury concerns
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


# Friendly lineup data — last 2 pre-WC 2026 friendlies (confirmed lineups only)
# (F.Starts, F.Apps) — starts=times in starting XI, apps=times played any minute
# Unconfirmed/future games (G2 not yet played) count as 0; max possible = 2
# Sources: official FA sites, Sky Sports, ESPN, Vavel, FotMob, 101greatgoals (June 2026)
FRIENDLY = {
    # ARGENTINA (G1: Apr 1 vs Zambia, G2: Jun 6 vs Honduras)
    "Alvarez":          (1, 1),  # started G1; absent G2
    "Fernández":        (1, 2),  # started G1; sub 61' G2
    "Romero":           (1, 2),  # started G1; sub 61' G2
    "Palacios":         (1, 1),  # started G2; absent G1
    "Lautaro Martínez": (1, 1),  # started G2; absent G1
    "Martínez (AR)":    (1, 1),  # started G1; Musso in G2
    "Rulli":            (0, 0),  # backup GK, neither game
    # USA (G1: May 31 vs Senegal, G2: Jun 6 vs Germany)
    "Pulisic":          (2, 2),  # started both
    "Tillman":          (1, 2),  # sub 46' G1; started G2
    # GERMANY (G1: May 31 vs Finland, G2: Jun 6 vs USA)
    "Kimmich":          (2, 2),  # started both
    "Wirtz":            (2, 2),  # started both
    "Schlotterbeck":    (2, 2),  # started both
    "Tah":              (2, 2),  # started both
    "Nmecha":           (2, 2),  # started both
    "Woltemade":        (0, 1),  # sub 73' G1; not in G2
    "Neuer":            (0, 0),  # absent both (calf injury)
    "Stiller":          (0, 0),  # not confirmed in either game
    "Mittelstädt":      (0, 0),
    "Gnabry":           (0, 0),
    "Adeyemi":          (0, 0),
    "Burkardt":         (0, 0),
    # SPAIN (G1: Jun 4 vs Iraq — rotated; G2 vs Peru Jun 8 not yet played)
    "Lamine Yamal":     (0, 0),  # rested both games
    "Pedri":            (0, 0),  # rested vs Iraq; G2 not played
    "Simón":            (0, 0),  # Joan García started; G2 not played
    "Cubarsí":          (0, 0),  # not in Iraq lineup
    "Cucurella":        (0, 0),  # not in Iraq lineup
    "Rodri":            (0, 0),  # rested
    "Porro":            (1, 1),  # started vs Iraq; G2 not played
    "Grimaldo":         (1, 1),  # started vs Iraq; G2 not played
    "Ruiz":             (0, 0),  # not in Iraq lineup; G2 not played
    "Olmo":             (1, 1),  # started vs Iraq; G2 not played
    "Raya":             (0, 0),  # Joan García started
    # BELGIUM (G1: Jun 2 vs Croatia, G2: Jun 6 vs Tunisia)
    "Courtois":         (2, 2),  # started both
    "Doku":             (2, 2),  # started both
    "De Bruyne":        (2, 2),  # started both
    "Lukaku":           (0, 2),  # sub 73' G1, sub 66' G2
    # PORTUGAL (G1: Jun 6 vs Chile; G2 vs Nigeria Jun 10 not played)
    "Bruno Fernandes":  (1, 1),  # started vs Chile; G2 not played
    "Vitinha":          (0, 0),  # not in Chile lineup; G2 not played
    "Nuno Mendes":      (0, 0),  # not in Chile lineup; G2 not played
    "João Neves":       (0, 0),  # not in Chile lineup; G2 not played
    "Rúben Dias":       (1, 1),  # started vs Chile; G2 not played
    "Rafael Leão":      (1, 1),  # started vs Chile; sent off; G2 not played
    "Pedro Neto":       (0, 1),  # sub vs Chile; G2 not played
    # CANADA (G1: Jun 1 vs Uzbekistan, G2: Jun 5 vs Ireland)
    "Jonathan David":   (2, 2),  # started both
    # NETHERLANDS (G1: Jun 3 vs Algeria; G2 vs Uzbekistan Jun 8 not played)
    "van Dijk":         (1, 1),  # started G1; G2 not played
    "Dumfries":         (0, 0),  # not in G1; G2 not played
    "Gravenberch":      (1, 1),  # started G1; G2 not played
    "Jurriën Timber":   (0, 0),  # not in G1; G2 not played
    "Flekken":          (0, 0),  # Verbruggen started; G2 not played
    # EGYPT (G1: May 28 vs Russia, G2: Jun 6 vs Brazil)
    "Omar Marmoush":    (2, 2),  # started both
    "Mohamed Salah":    (0, 1),  # absent G1; sub 2nd half G2
    # IVORY COAST (G1: Jun 4 vs France; no 2nd official friendly)
    "Diallo":           (0, 1),  # sub 46' G1; no G2
    "Singo":            (1, 1),  # started G1; no G2
    # SWEDEN (G1: Jun 1 vs Norway, G2: Jun 4 vs Greece)
    "Gyökeres":         (1, 1),  # absent G1; started G2
    "Isak":             (1, 2),  # sub 62' G1; started G2
    "Svensson":         (2, 2),  # started both (Daniel Svensson)
    # TURKEY (G1: Jun 1 vs N.Macedonia, G2: Jun 6 vs Venezuela)
    "Çalhanoğlu":       (0, 2),  # sub 88' G1; sub 71' G2
    "Güler":            (1, 2),  # sub 63' G1; started G2
    "Yildiz":           (0, 0),  # not in either Turkey lineup
    # FRANCE (G1: Jun 4 vs Ivory Coast; G2 vs N.Ireland Jun 8 not played)
    "Mbappé":           (1, 1),  # started G1; G2 not played
    "Olise":            (1, 1),  # started G1; G2 not played
    "Maignan":          (1, 1),  # started G1; G2 not played
    "Dembélé":          (0, 0),  # not in G1 lineup; G2 not played
    "Koundé":           (1, 1),  # started G1; G2 not played
    "Upamecano":        (1, 1),  # started G1; G2 not played
    "Saliba":           (0, 0),  # not in G1 (Konaté+Upamecano); G2 not played
    "Cherki":           (1, 1),  # started G1; G2 not played
    "Doué":             (0, 0),  # not in G1; G2 not played
    "Akliouche":        (0, 1),  # sub 45' G1; G2 not played
    # ECUADOR (G1: May 30 vs Saudi Arabia — Moisés Caicedo not listed; G2 today unconfirmed)
    "Caicedo":          (0, 0),  # not confirmed in either game
    # SCOTLAND (G1: May 30 vs Curaçao, G2: Jun 6 vs Bolivia)
    "McTominay":        (1, 1),  # started G2; not in G1
    # ENGLAND (G1: Jun 6 vs NZ — Tuchel rotated full XI at HT; G2 vs Costa Rica Jun 10 not played)
    "Kane":             (1, 1),  # started G1; G2 not played
    "Rice":             (0, 0),  # not in G1; G2 not played
    "Anderson":         (0, 1),  # sub 46' G1; G2 not played
    "Bellingham":       (0, 1),  # sub 46' G1; G2 not played
    "Konsa":            (0, 1),  # sub 46' G1; G2 not played
    "Saka":             (0, 0),  # rested G1; G2 not played
    "Pickford":         (1, 1),  # started G1; G2 not played
    "Guéhi":            (1, 1),  # started G1; G2 not played
    "Rashford":         (1, 1),  # started G1; G2 not played
    "Watkins":          (1, 1),  # started G1; G2 not played
    "Quansah":          (1, 1),  # started G1; G2 not played
    "Trafford":         (0, 1),  # sub 46' G1; G2 not played
    "Dean Henderson":   (0, 0),
    "Foden":            (0, 0),
    "Alexander-Arnold": (0, 0),
    "Eze":              (0, 0),
    "Gibbs-White":      (0, 0),
    "Palmer":           (0, 0),
    "Greenwood":        (0, 0),
    # CROATIA (G1: Jun 2 vs Belgium; G2 vs Slovenia Jun 7 unconfirmed)
    "Gvardiol":         (1, 1),  # started G1; G2 today unconfirmed
    # URUGUAY (no May/Jun 2026 friendlies; last: Mar 27 vs England, Mar 31 vs Algeria)
    "Valverde":         (0, 0),
    # MOROCCO (G1: Jun 2 vs Madagascar — Hakimi rested; G2 vs Norway today unconfirmed)
    "Hakimi":           (0, 0),  # precautionary rest G1; G2 today unconfirmed
    # BRAZIL (G1: May 31 vs Panama, G2: Jun 6 vs Egypt)
    "Vinícius Júnior":  (2, 2),  # started both
    "Raphinha":         (2, 2),  # started both
    "Gabriel Magalhães":(0, 0),  # not in either starting XI
    "Alisson Becker":   (2, 2),  # started both
    "Matheus Cunha":    (1, 2),  # started G1; sub 45' G2
    "Antony":           (0, 0),
    "João Pedro":       (0, 0),
    # COLOMBIA (G1: Jun 1 vs Costa Rica; G2 vs Jordan today unconfirmed)
    "Díaz":             (1, 1),  # started G1; G2 today unconfirmed
    # NORWAY (G1: Jun 1 vs Sweden — Haaland+Ødegaard rested; G2 vs Morocco today unconfirmed)
    "Haaland":          (0, 0),  # rested G1; G2 today unconfirmed
    "Ødegaard":         (0, 0),  # rested G1; G2 today unconfirmed
    # SWITZERLAND (G1: May 31 vs Jordan — Mvogo GK; G2: Jun 6 vs Australia — Kobel GK)
    "Kobel":            (1, 1),  # started G2; Mvogo in G1
}


# G1 actual performance
# Scoring: Goal=6, Assist=3, GK CS=6, DEF CS=4, MID CS=1, FWD CS=0, Started=+2, Sub=+1
# Tuple: (g1_pts, goals, assists, cs_bonus, notes)
G1_ACTUAL = {
    # ARGENTINA 3-0 Algeria (Jun 16) — CS
    "Martínez (AR)":    (8,  0, 0, 6, "GK CS; started"),
    "Romero":           (6,  0, 0, 4, "DEF CS; started"),
    "Fernández":        (3,  0, 0, 1, "MID CS; started"),
    "Lautaro Martínez": (2,  0, 0, 0, "started; no g/a"),
    "Alvarez":          (0,  0, 0, 0, "bench"),
    "Palacios":         (0,  0, 0, 0, "bench — Almada started"),
    "Rulli":            (0,  0, 0, 0, "backup GK"),
    # USA 4-1 Paraguay (Jun 12)
    "Pulisic":          (5,  0, 1, 0, "started; 1 assist"),
    "Tillman":          (2,  0, 0, 0, "started"),
    # GERMANY 7-1 Curaçao (Jun 14)
    "Kimmich":          (2,  0, 0, 0, "started"),
    "Wirtz":            (2,  0, 0, 0, "started"),
    "Schlotterbeck":    (8,  1, 0, 0, "started; 1 goal"),
    "Tah":              (2,  0, 0, 0, "started"),
    "Nmecha":           (8,  1, 0, 0, "started; 1 goal"),
    "Woltemade":        (1,  0, 0, 0, "sub"),
    "Neuer":            (0,  0, 0, 0, "DNP — Baumann started"),
    "Stiller":          (0,  0, 0, 0, "DNP/sub unconfirmed"),
    # SPAIN 0-0 Cape Verde (Jun 15) — CS
    "Lamine Yamal":     (0,  0, 0, 0, "DNP — hamstring"),
    "Pedri":            (3,  0, 0, 1, "MID CS; started"),
    "Simón":            (8,  0, 0, 6, "GK CS; started"),
    "Cubarsí":          (6,  0, 0, 4, "DEF CS; started"),
    "Cucurella":        (6,  0, 0, 4, "DEF CS; started"),
    "Rodri":            (3,  0, 0, 1, "MID CS; started"),
    "Porro":            (6,  0, 0, 4, "DEF CS; started"),
    "Grimaldo":         (6,  0, 0, 4, "DEF CS; started"),
    "Ruiz":             (3,  0, 0, 1, "MID CS; started"),
    "Olmo":             (2,  0, 0, 0, "started; FWD no CS"),
    "Raya":             (0,  0, 0, 0, "DNP — Simón started"),
    "Joan García":      (0,  0, 0, 0, "bench"),
    # BELGIUM 1-1 Egypt (Jun 15)
    "Courtois":         (2,  0, 0, 0, "started; no CS"),
    "Doku":             (2,  0, 0, 0, "started"),
    "De Bruyne":        (5,  0, 1, 0, "started; assist (OG)"),
    "Lukaku":           (1,  0, 0, 0, "sub ~66'"),
    "Sels":             (0,  0, 0, 0, "bench GK"),
    # PORTUGAL 1-1 DR Congo (Jun 17)
    "Bruno Fernandes":  (2,  0, 0, 0, "started"),
    "Vitinha":          (2,  0, 0, 0, "started"),
    "Rúben Dias":       (2,  0, 0, 0, "started; DEF no CS"),
    "Nuno Mendes":      (2,  0, 0, 0, "started; DEF no CS"),
    "João Neves":       (2,  0, 0, 0, "started"),
    "Rafael Leão":      (2,  0, 0, 0, "started"),
    "Pedro Neto":       (1,  0, 0, 0, "sub"),
    # CANADA 1-1 Bosnia (Jun 12)
    "Jonathan David":   (1,  0, 0, 0, "sub 61'; hat trick was G2"),
    # NETHERLANDS 2-2 Japan (Jun 14)
    "van Dijk":         (8,  1, 0, 0, "started; 1 goal"),
    "Gravenberch":      (2,  0, 0, 0, "started"),
    "Dumfries":         (2,  0, 0, 0, "started"),
    "Jurriën Timber":   (2,  0, 0, 0, "started"),
    "Flekken":          (0,  0, 0, 0, "DNP — Verbruggen started"),
    # EGYPT 1-1 Belgium (Jun 15)
    "Mohamed Salah":    (5,  0, 1, 0, "started; 1 assist"),
    "Omar Marmoush":    (2,  0, 0, 0, "started"),
    # IVORY COAST 1-0 Ecuador (Jun 14) — CS
    "Diallo":           (8,  1, 0, 0, "started; 1 goal; FWD no CS"),
    "Singo":            (6,  0, 0, 4, "DEF CS; started"),
    # SWEDEN 5-1 Tunisia (Jun 14)
    "Gyökeres":         (8,  1, 0, 0, "started; 1 goal"),
    "Isak":             (8,  1, 0, 0, "started; 1 goal"),
    "Svensson":         (0,  0, 0, 0, "DNP — not in Sweden XI"),
    # TURKEY 0-2 Australia (Jun 14)
    "Çalhanoğlu":       (2,  0, 0, 0, "started; lost 0-2"),
    "Güler":            (2,  0, 0, 0, "started; lost 0-2"),
    "Yildiz":           (2,  0, 0, 0, "started; lost 0-2"),
    # FRANCE 3-1 Senegal (Jun 16)
    "Mbappé":           (14, 2, 0, 0, "started; 2 goals"),
    "Olise":            (5,  0, 1, 0, "started; 1 assist"),
    "Maignan":          (2,  0, 0, 0, "started; GK no CS"),
    "Dembélé":          (2,  0, 0, 0, "started"),
    "Koundé":           (2,  0, 0, 0, "started; DEF no CS"),
    "Upamecano":        (2,  0, 0, 0, "started; DEF no CS"),
    "Saliba":           (0,  0, 0, 0, "bench — Konaté started"),
    "Cherki":           (0,  0, 0, 0, "bench"),
    "Doué":             (0,  0, 0, 0, "bench"),
    "Akliouche":        (0,  0, 0, 0, "bench"),
    "Yoro":             (0,  0, 0, 0, "bench"),
    "Chevalier":        (0,  0, 0, 0, "bench GK"),
    # ECUADOR 0-1 Ivory Coast (Jun 14)
    "Caicedo":          (2,  0, 0, 0, "started"),
    # SCOTLAND 1-0 Haiti (Jun 13) — CS
    "McTominay":        (3,  0, 0, 1, "MID CS; started"),
    # ENGLAND 4-2 Croatia (Jun 17)
    "Kane":             (14, 2, 0, 0, "started; 2 goals"),
    "Rice":             (5,  0, 1, 0, "started; 1 assist"),
    "Anderson":         (5,  0, 1, 0, "started; 1 assist"),
    "Bellingham":       (8,  1, 0, 0, "started; 1 goal"),
    "Rashford":         (7,  1, 0, 0, "sub; 1 goal"),
    "Saka":             (4,  0, 1, 0, "sub; 1 assist"),
    "Pickford":         (2,  0, 0, 0, "started; GK no CS"),
    "Guéhi":            (0,  0, 0, 0, "bench — Konsa started"),
    "Konsa":            (2,  0, 0, 0, "started; DEF no CS"),
    "Watkins":          (0,  0, 0, 0, "bench"),
    "Quansah":          (0,  0, 0, 0, "bench"),
    "Trafford":         (0,  0, 0, 0, "bench"),
    "Dean Henderson":   (0,  0, 0, 0, "bench"),
    "Foden":            (0,  0, 0, 0, "bench"),
    "Palmer":           (0,  0, 0, 0, "bench"),
    "Alexander-Arnold": (0,  0, 0, 0, "bench"),
    "Eze":              (0,  0, 0, 0, "bench"),
    "Gibbs-White":      (0,  0, 0, 0, "bench"),
    "Pope":             (0,  0, 0, 0, "bench GK3"),
    "Bellingham (BVB)": (0,  0, 0, 0, "bench"),
    # CROATIA 2-4 England (Jun 17)
    "Gvardiol":         (2,  0, 0, 0, "started; DEF conceded 4"),
    # URUGUAY 1-1 Saudi Arabia (Jun 15)
    "Valverde":         (2,  0, 0, 0, "started"),
    # MOROCCO 1-1 Brazil (Jun 13)
    "Hakimi":           (2,  0, 0, 0, "started; DEF no CS"),
    # BRAZIL 1-1 Morocco (Jun 13)
    "Vinícius Júnior":  (8,  1, 0, 0, "started; 1 goal"),
    "Raphinha":         (2,  0, 0, 0, "started"),
    "Gabriel Magalhães":(2,  0, 0, 0, "started; DEF no CS"),
    "Alisson Becker":   (2,  0, 0, 0, "started; GK no CS"),
    "Matheus Cunha":    (2,  0, 0, 0, "started"),
    # COLOMBIA 3-1 Uzbekistan (Jun 17)
    "Díaz":             (11, 1, 1, 0, "started; 1G+1A"),
    # NORWAY 4-1 Iraq (Jun 16)
    "Haaland":          (14, 2, 0, 0, "started; 2 goals"),
    "Ødegaard":         (5,  0, 1, 0, "started; 1 assist"),
    # SWITZERLAND 1-1 Qatar (Jun 13 — Khoukhi eq 90+4')
    "Kobel":            (2,  0, 0, 0, "started; GK no CS (late eq.)"),
    # GERMANY 7-1 Curaçao (Jun 14) — bench/late subs
    "Gnabry":           (1,  0, 0, 0, "sub"),
    "Adeyemi":          (1,  0, 0, 0, "sub"),
    "Burkardt":         (1,  0, 0, 0, "sub"),
    "Mittelstädt":      (1,  0, 0, 0, "sub"),
    "Ekitiké":          (1,  0, 0, 0, "sub"),
    # BRAZIL 1-1 Morocco (Jun 13)
    "Antony":           (1,  0, 0, 0, "sub"),
    "João Pedro":       (1,  0, 0, 0, "sub"),
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

        frd = FRIENDLY.get(display, (0, 0))
        f_starts, f_apps = frd

        # ── G1 actual vs expected ──────────────────────────────────────────────
        # Δ = G1 Pts minus appearance expectation (starter=2, sometimes=1, no/bench=0)
        # Shows goals/assists/CS value above just showing up
        g1_data = G1_ACTUAL.get(display)
        if g1_data is not None:
            g1_pts_actual = g1_data[0]
            if starter_label == "yes":
                g1_exp = 2.0
            elif starter_label == "sometimes":
                g1_exp = 1.0
            else:
                g1_exp = 0.0
            g1_delta = g1_pts_actual - g1_exp
        else:
            g1_pts_actual = None
            g1_delta      = None

        results.append((display, full_name, nat, pos, price, adj_pts, pts_per_price, status,
                        fit_label, starter_label, g1_win, f_starts, f_apps,
                        g1_pts_actual, g1_delta))

    # Sort by pts/price descending
    results.sort(key=lambda x: -x[6])

    # ── Print main table ─────────────────────────────────────────────────────
    print("# Fantasy Value Table — Adj Pts per Price Unit")
    print("# Fitness: full/mostly/not  |  Starter: yes/sometimes/no  |  G1 Win%: Polymarket/Dimers Jun 7 2026")
    print("# F.Start/F.App: times started / times played in last 2 pre-WC friendlies (max 2)")
    print("# G1 Pts: actual G1 fantasy pts  |  Δ: G1 Pts minus expected pts/game (+=over, -=under)\n")
    print(f"{'#':<4} {'Player':<24} {'Nat':<14} {'Pos':<4} {'Price':>8} {'Adj Pts':>8} {'Pts/$':>8}  {'Fitness':<8} {'Starter':<10} {'G1 Win%':>7}  {'F.St':>4} {'F.Ap':>4}  {'G1 Pts':>6} {'Δ':>6}  Status")
    print("─" * 138)
    for i, (disp, full, nat, pos, price, pts, ppp, status, fit, starter, g1, fst, fap, g1pts, g1d) in enumerate(results, 1):
        g1pts_str = f"{g1pts:>6}"   if g1pts is not None else "     —"
        g1d_str   = f"{g1d:>+6.1f}" if g1d   is not None else "     —"
        print(f"{i:<4} {disp:<24} {nat:<14} {pos:<4} {price:>8.5f} {pts:>8.1f} {ppp:>8.0f}  {fit:<8} {starter:<10} {g1:>6}%  {fst:>4} {fap:>4}  {g1pts_str} {g1d_str}  {status}")

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
