#!/usr/bin/env python3
"""
build_valuation.py
Cross-references price-list with master_sheet.csv expected WC points.
Outputs analysis/valuation_sheet.md — ranked by value_score within each position bracket.
value_score = total_exp_fantasy_pts / price
value_index = (value_score / position_mean_value_score) × 100  (100 = average T1/T2 starter)
"""
import csv
from collections import defaultdict

# ──────────────────────────────────────────────────────────────────────────────
# PRICE LIST  (price_name, club, bracket_pos, price)
# bracket_pos is the position used for the competition bracket (GK/DEF/MID/FWD)
# ──────────────────────────────────────────────────────────────────────────────
PRICE_LIST = [
    ('Lamine Yamal',          'BAR', 'FWD', 0.0633),
    ('Michael Olise',         'FCB', 'MID', 0.0532),
    ('Kylian Mbappé',         'RMA', 'FWD', 0.0505),
    ('Harry Kane',            'FCB', 'FWD', 0.0423),
    ('Bruno Fernandes',       'MUN', 'MID', 0.0367),
    ('Ousmane Dembélé',       'PSG', 'FWD', 0.0307),
    ('Pedri',                 'BAR', 'MID', 0.0305),
    ('Vitinha',               'PSG', 'MID', 0.0285),
    ('Erling Haaland',        'MCI', 'FWD', 0.0270),
    ('Vinícius Júnior',       'RMA', 'FWD', 0.0268),
    ('Mike Maignan',          'MIL', 'GK',  0.0255),
    ('Jérémy Doku',           'MCI', 'FWD', 0.0246),
    ('Gabriel Magalhães',     'ARS', 'DEF', 0.0235),
    ('Unai Simón',            'ATH', 'GK',  0.0231),
    ('Declan Rice',           'ARS', 'MID', 0.0227),
    ('David Raya',            'ARS', 'GK',  0.0223),
    ('William Saliba',        'ARS', 'DEF', 0.0221),
    ('Rayan Cherki',          'MCI', 'MID', 0.0218),
    ('Emiliano Martínez',     'AVL', 'GK',  0.0211),
    ('Marc Guéhi',            'MCI', 'DEF', 0.0205),
    ('Jordan Pickford',       'EVE', 'GK',  0.0200),
    ('Bukayo Saka',           'ARS', 'FWD', 0.0200),
    ('Joshua Kimmich',        'FCB', 'MID', 0.0197),
    ('Thibaut Courtois',      'RMA', 'GK',  0.0187),
    ('Raphinha',              'BAR', 'FWD', 0.0186),
    ('Kenan Yıldız',          'JUV', 'FWD', 0.0178),
    ('Virgil van Dijk',       'LIV', 'DEF', 0.0175),
    ('Nuno Mendes',           'PSG', 'DEF', 0.0175),
    ('Rodri',                 'MCI', 'MID', 0.0174),
    ('Ezri Konsa',            'AVL', 'DEF', 0.0172),
    ('Pau Cubarsí',           'BAR', 'DEF', 0.0171),
    ('Désiré Doué',           'PSG', 'FWD', 0.0169),
    ('Dean Huijsen',          'RMA', 'DEF', 0.0168),
    ('João Neves',            'PSG', 'MID', 0.0168),
    ('Luis Díaz',             'FCB', 'FWD', 0.0167),
    ('Jude Bellingham',       'RMA', 'MID', 0.0165),
    ('Nico Schlotterbeck',    'BVB', 'DEF', 0.0158),
    ('Achraf Hakimi',         'PSG', 'DEF', 0.0156),
    ('Joško Gvardiol',        'MCI', 'DEF', 0.0156),
    ('Florian Wirtz',         'LIV', 'MID', 0.0155),
    ('Trent Alexander-Arnold','RMA', 'DEF', 0.0151),
    ('Elliot Anderson',       'NFO', 'MID', 0.0149),
    ('Jules Koundé',          'BAR', 'DEF', 0.0147),
    ('Dayot Upamecano',       'FCB', 'DEF', 0.0146),
    ('Alisson Becker',        'LIV', 'GK',  0.0144),
    ('Rúben Dias',            'MCI', 'DEF', 0.0143),
    ('Julián Álvarez',        'ATM', 'FWD', 0.0143),
    ('Jonathan Tah',          'FCB', 'DEF', 0.0138),
    ('Pedro Porro',           'TOT', 'DEF', 0.0137),
    ('Enzo Fernández',        'CHE', 'MID', 0.0132),
    ('Marc Cucurella',        'CHE', 'DEF', 0.0129),
    ('Matheus Cunha',         'MUN', 'FWD', 0.0125),
    ('Kvaratskhelia',         'PSG', 'FWD', 0.0124),   # Georgia — not in 24-country list
    ('Martin Ødegaard',       'ARS', 'MID', 0.0121),
    ('Gregor Kobel',          'BVB', 'GK',  0.0115),
    ('Viktor Gyökeres',       'ARS', 'FWD', 0.0115),
    ('Federico Valverde',     'RMA', 'MID', 0.0111),
    ('Ollie Watkins',         'AVL', 'FWD', 0.0110),
    ('Donnarumma',            'MCI', 'GK',  0.0109),   # Italy — not analysed
    ('Cole Palmer',           'CHE', 'MID', 0.0108),
    ('Phil Foden',            'MCI', 'MID', 0.0108),
    ('Eberechi Eze',          'ARS', 'MID', 0.0107),
    ('Lautaro Martínez',      'INT', 'FWD', 0.0107),
    ('Moisés Caicedo',        'CHE', 'MID', 0.0104),
    ('João Pedro',            'CHE', 'FWD', 0.0104),
    ('Christian Pulisic',     'MIL', 'MID', 0.00997),
    ('Scott McTominay',       'NAP', 'MID', 0.00997),
    ('Morgan Gibbs-White',    'NFO', 'MID', 0.00983),
    ('Kevin De Bruyne',       'NAP', 'MID', 0.00982),
    ('Fabián Ruiz',           'PSG', 'MID', 0.00966),
    ('Arda Güler',            'RMA', 'MID', 0.00958),
    ('Robin Le Normand',      'ATM', 'DEF', 0.00944),
    ('Jurriën Timber',        'ARS', 'DEF', 0.00926),
    ('Denzel Dumfries',       'INT', 'DEF', 0.00890),
    ('Dani Olmo',             'BAR', 'MID', 0.00888),
    ('Locatelli',             'JUV', 'MID', 0.00879),  # Italy — not analysed
    ('Cristian Romero',       'TOT', 'DEF', 0.00875),
    ('Joan García',           'BAR', 'GK',  0.00870),
    ('Rafael Leão',           'MIL', 'FWD', 0.00852),
    ('Dean Henderson',        'CRY', 'GK',  0.00836),
    ('Pedro Neto',            'CHE', 'FWD', 0.00833),
    ('Mason Greenwood',       'OM',  'FWD', 0.00824),
    ('Omar Marmoush',         'MCI', 'FWD', 0.00807),
    ('Ryan Gravenberch',      'LIV', 'MID', 0.00787),
    ('Neuer',                 'FCB', 'GK',  0.00768),  # Germany GK — not in CSV
    ('Mbeumo',                'MUN', 'FWD', 0.00755),  # Cameroon — not analysed
    ('Bastoni',               'INT', 'DEF', 0.00730),  # Italy — not analysed
    ('Alexander Isak',        'LIV', 'FWD', 0.00727),
    ('Rrahmani',              'NAP', 'DEF', 0.00713),  # Kosovo — not analysed
    ('Tonali',                'NEW', 'MID', 0.00698),  # Italy — not analysed
    ('Hakan Çalhanoğlu',      'INT', 'MID', 0.00682),
    ('Kerkez',                'LIV', 'DEF', 0.00658),  # Hungary — not analysed
    ('Alejandro Grimaldo',    'LEV', 'DEF', 0.00640),
    ('Matz Sels',             'NFO', 'GK',  0.00626),
    ('Mark Flekken',          'LEV', 'GK',  0.00599),
    ('Mohammed Kudus',        'TOT', 'MID', 0.00587),
    ('Guirassy',              'BVB', 'FWD', 0.00553),  # Guinea — not analysed
    ('Aina',                  'NFO', 'DEF', 0.00526),  # Nigeria — not analysed
    ('Di Gregorio',           'JUV', 'GK',  0.00520),  # Italy — not analysed
    ('Angelo Stiller',        'VFB', 'MID', 0.00509),
    ('Amad Diallo',           'MUN', 'FWD', 0.00509),
    ('Hugo Ekitiké',          'LIV', 'FWD', 0.00507),
    ('Antony',                'BET', 'FWD', 0.00499),
    ('Marcus Rashford',       'BAR', 'FWD', 0.00498),
    ('Tapsoba',               'LEV', 'DEF', 0.00483),  # Burkina Faso — not analysed
    ('Vicario',               'TOT', 'GK',  0.00479),  # Italy — not analysed
    ('Mohamed Salah',         'LIV', 'FWD', 0.00447),
    ('Maximilian Mittelstädt','VFB', 'DEF', 0.00442),
    ('Felix Nmecha',          'BVB', 'MID', 0.00431),
    ('Maghnes Akliouche',     'ASM', 'MID', 0.00428),
    ('Oblak',                 'ATM', 'GK',  0.00419),  # Slovenia — not analysed
    ('Exequiel Palacios',     'LEV', 'MID', 0.00418),
    ('Nick Woltemade',        'NEW', 'FWD', 0.00413),
    ('Jonathan David',        'JUV', 'FWD', 0.00410),
    ('Di Lorenzo',            'NAP', 'DEF', 0.00393),  # Italy — not analysed
    ('James Trafford',        'MCI', 'GK',  0.00392),
    ('Jobe Bellingham',       'BVB', 'MID', 0.00389),
    ('Daniel Svensson',       'BVB', 'DEF', 0.00375),
    ('Malik Tillman',         'LEV', 'MID', 0.00373),
    ('Robert Sánchez',        'CHE', 'GK',  0.00369),
    ('Gerónimo Rulli',        'OM',  'GK',  0.00362),
    ('Jarell Quansah',        'LEV', 'DEF', 0.00351),
    ('Pavlovic',              'MIL', 'DEF', 0.00348),  # Serbia — not analysed
    ('Nick Pope',             'NEW', 'GK',  0.00344),
    ('Álvaro Carreras',       'RMA', 'DEF', 0.00340),
    ('Romagnoli',             'LAZ', 'DEF', 0.00333),  # Italy — not analysed
    ('Romelu Lukaku',         'NAP', 'FWD', 0.00330),
    ('Serge Gnabry',          'FCB', 'FWD', 0.00310),
    ('Matías Soulé',          'ROM', 'FWD', 0.00306),
    ('Barella',               'INT', 'MID', 0.00297),  # Italy — not analysed
    ('Éder Militão',          'RMA', 'DEF', 0.00297),  # Brazil — not in CSV
    ('Simons',                'TOT', 'MID', 0.00290),  # Netherlands — not in CSV
    ('Højlund',               'NAP', 'FWD', 0.00269),  # Denmark — not analysed
    ('Karim Adeyemi',         'BVB', 'FWD', 0.00256),
    ('Jonathan Burkardt',     'SGE', 'FWD', 0.00254),
    ('Højbjerg',              'OM',  'MID', 0.00245),  # Denmark — not analysed
    ('Leny Yoro',             'MUN', 'DEF', 0.00237),
    ('Lucas Chevalier',       'PSG', 'GK',  0.00236),
    ('Rodon',                 'LEE', 'DEF', 0.00215),  # Wales — not in WC 2026
]

# Manual CSV name mapping (price_list_name → csv_player_name)
# Only needed where exact match fails
NAME_MAP = {
    'Michael Olise':         'Michael Olise',
    'Kylian Mbappé':         'Kylian Mbappé',
    'Harry Kane':            'Harry Kane',
    'Bruno Fernandes':       'Bruno Fernandes',
    'Ousmane Dembélé':       'Ousmane Dembélé',
    'Erling Haaland':        'Erling Haaland',
    'Mike Maignan':          'Mike Maignan',
    'Jérémy Doku':           'Jérémy Doku',
    'Gabriel Magalhães':     'Gabriel Magalhães',
    'Unai Simón':            'Unai Simón',
    'Declan Rice':           'Declan Rice',
    'David Raya':            'David Raya',
    'William Saliba':        'William Saliba',
    'Rayan Cherki':          'Rayan Cherki',
    'Emiliano Martínez':     'Emiliano Martínez',
    'Marc Guéhi':            'Marc Guéhi',
    'Jordan Pickford':       'Jordan Pickford',
    'Bukayo Saka':           'Bukayo Saka',
    'Joshua Kimmich':        'Joshua Kimmich',
    'Thibaut Courtois':      'Thibaut Courtois',
    'Raphinha':              'Raphinha',
    'Kenan Yıldız':          'Kenan Yıldız',
    'Virgil van Dijk':       'Virgil van Dijk',
    'Nuno Mendes':           'Nuno Mendes',
    'Rodri':                 'Rodri',
    'Ezri Konsa':            'Ezri Konsa',
    'Pau Cubarsí':           'Pau Cubarsí',
    'Désiré Doué':           'Désiré Doué',
    'Dean Huijsen':          'Dean Huijsen',
    'João Neves':            'João Neves',
    'Luis Díaz':             'Luis Díaz',
    'Jude Bellingham':       'Jude Bellingham',
    'Nico Schlotterbeck':    'Nico Schlotterbeck',
    'Achraf Hakimi':         'Achraf Hakimi',
    'Joško Gvardiol':        'Joško Gvardiol',
    'Florian Wirtz':         'Florian Wirtz',
    'Trent Alexander-Arnold':'Trent Alexander-Arnold',
    'Elliot Anderson':       'Elliot Anderson',
    'Jules Koundé':          'Jules Koundé',
    'Dayot Upamecano':       'Dayot Upamecano',
    'Alisson Becker':        'Alisson Becker',
    'Rúben Dias':            'Rúben Dias',
    'Julián Álvarez':        'Julián Álvarez',
    'Jonathan Tah':          'Jonathan Tah',
    'Pedro Porro':           'Pedro Porro',
    'Enzo Fernández':        'Enzo Fernández',
    'Marc Cucurella':        'Marc Cucurella',
    'Matheus Cunha':         'Matheus Cunha',
    'Martin Ødegaard':       'Martin Ødegaard',
    'Gregor Kobel':          'Gregor Kobel',
    'Viktor Gyökeres':       'Viktor Gyökeres',
    'Federico Valverde':     'Federico Valverde',
    'Ollie Watkins':         'Ollie Watkins',
    'Cole Palmer':           'Cole Palmer',
    'Phil Foden':            'Phil Foden',
    'Eberechi Eze':          'Eberechi Eze',
    'Lautaro Martínez':      'Lautaro Martínez',
    'Moisés Caicedo':        'Moisés Caicedo',
    'João Pedro':            'João Pedro',
    'Christian Pulisic':     'Christian Pulisic',
    'Scott McTominay':       'Scott McTominay',
    'Morgan Gibbs-White':    'Morgan Gibbs-White',
    'Kevin De Bruyne':       'Kevin De Bruyne',
    'Fabián Ruiz':           'Fabián Ruiz',
    'Arda Güler':            'Arda Güler',
    'Robin Le Normand':      'Robin Le Normand',
    'Jurriën Timber':        'Jurriën Timber',
    'Denzel Dumfries':       'Denzel Dumfries',
    'Dani Olmo':             'Dani Olmo',
    'Cristian Romero':       'Cristian Romero',
    'Joan García':           'Joan García',
    'Rafael Leão':           'Rafael Leão',
    'Dean Henderson':        'Dean Henderson',
    'Pedro Neto':            'Pedro Neto',
    'Mason Greenwood':       'Mason Greenwood',
    'Omar Marmoush':         'Omar Marmoush',
    'Ryan Gravenberch':      'Ryan Gravenberch',
    'Alexander Isak':        'Alexander Isak',
    'Hakan Çalhanoğlu':      'Hakan Çalhanoğlu',
    'Alejandro Grimaldo':    'Alejandro Grimaldo',
    'Matz Sels':             'Matz Sels',
    'Mark Flekken':          'Mark Flekken',
    'Mohammed Kudus':        'Mohammed Kudus',
    'Angelo Stiller':        'Angelo Stiller',
    'Amad Diallo':           'Amad Diallo',
    'Hugo Ekitiké':          'Hugo Ekitiké',
    'Antony':                'Antony',
    'Marcus Rashford':       'Marcus Rashford',
    'Mohamed Salah':         'Mohamed Salah',
    'Maximilian Mittelstädt':'Maximilian Mittelstädt',
    'Felix Nmecha':          'Felix Nmecha',
    'Maghnes Akliouche':     'Maghnes Akliouche',
    'Exequiel Palacios':     'Exequiel Palacios',
    'Nick Woltemade':        'Nick Woltemade',
    'Jonathan David':        'Jonathan David',
    'James Trafford':        'James Trafford',
    'Jobe Bellingham':       'Jobe Bellingham',
    'Daniel Svensson':       'Daniel Svensson',
    'Malik Tillman':         'Malik Tillman',
    'Robert Sánchez':        'Robert Sánchez',
    'Gerónimo Rulli':        'Gerónimo Rulli',
    'Jarell Quansah':        'Jarell Quansah',
    'Nick Pope':             'Nick Pope',
    'Álvaro Carreras':       'Álvaro Carreras',
    'Romelu Lukaku':         'Romelu Lukaku',
    'Serge Gnabry':          'Serge Gnabry',
    'Matías Soulé':          'Matías Soulé',
    'Karim Adeyemi':         'Karim Adeyemi',
    'Jonathan Burkardt':     'Jonathan Burkardt',
    'Leny Yoro':             'Leny Yoro',
    'Lucas Chevalier':       'Lucas Chevalier',
    'Lamine Yamal':          'Lamine Yamal',
    'Pedri':                 'Pedri',
    'Vitinha':               'Vitinha',
}


def main():
    # Load CSV
    with open('/tmp/world_cup/data/master_sheet.csv', newline='', encoding='utf-8') as f:
        csv_rows = {r['player']: r for r in csv.DictReader(f)}

    # Build lookup: price_name → csv_row (or None)
    entries = []
    for (pname, club, bracket_pos, price) in PRICE_LIST:
        csv_name = NAME_MAP.get(pname, pname)
        row = csv_rows.get(csv_name)
        if row:
            tot_pts  = float(row['total_exp_fantasy_pts'])
            nat      = row['nationality']
            tier     = row['tier']
        else:
            tot_pts  = None
            nat      = '—'
            tier     = '—'
        entries.append({
            'price_name':  pname,
            'club':        club,
            'bracket_pos': bracket_pos,
            'price':       price,
            'tot_pts':     tot_pts,
            'nat':         nat,
            'tier':        tier,
            'value':       round(tot_pts / price, 2) if tot_pts is not None else None,
        })

    # Compute position-mean value using T1/T2 players only (GK1/GK2 for keepers)
    # Excludes T3-T5 benchwarmers so "100 = average starter" not "average of all priced players"
    STARTER_TIERS = {'1', '2', 'GK1', 'GK2'}
    pos_values = defaultdict(list)
    for e in entries:
        if e['value'] is not None and e['tier'] in STARTER_TIERS:
            pos_values[e['bracket_pos']].append(e['value'])
    pos_mean = {p: sum(vs)/len(vs) for p, vs in pos_values.items()}

    for e in entries:
        if e['value'] is not None and e['bracket_pos'] in pos_mean:
            e['value_index'] = round(e['value'] / pos_mean[e['bracket_pos']] * 100)
        else:
            e['value_index'] = None

    # Portfolio allocation: 1.5% base per player, extra weighted by value_index, cutoff ≥ 100
    selected = [e for e in entries if e['value_index'] is not None and e['value_index'] >= 100]
    n_sel = len(selected)
    base_pct = 1.5
    base_total = n_sel * base_pct
    remaining = 100.0 - base_total
    sum_idx = sum(e['value_index'] for e in selected)
    for e in entries:
        if e['value_index'] is not None and e['value_index'] >= 100:
            e['alloc_pct'] = base_pct + (e['value_index'] / sum_idx) * remaining
        else:
            e['alloc_pct'] = None

    # Sort within each bracket: analysed players by value desc, unanalysed at bottom
    by_pos = defaultdict(list)
    for e in entries:
        by_pos[e['bracket_pos']].append(e)
    for pos in by_pos:
        by_pos[pos].sort(key=lambda e: (e['value'] is None, -(e['value'] or 0)))

    # Build markdown
    lines = [
        '# World Cup 2026 — Fantasy Valuation Sheet',
        f'*Players priced, ranked by WC expected pts / price within each position bracket.*',
        '',
        '**value_score** = `total_exp_fantasy_pts / price` — higher is better value.',
        '**value_index** = value_score vs T1/T2 starter average (100 = average starter; 150 = 50% above average starter).',
        '`—` = player\'s national team outside our 24-country WC analysis.',
        '',
        '---',
        '',
    ]

    pos_order = ['GK', 'DEF', 'MID', 'FWD']
    pos_label = {'GK': 'Goalkeepers', 'DEF': 'Defenders', 'MID': 'Midfielders', 'FWD': 'Forwards'}

    for pos in pos_order:
        players = by_pos[pos]
        mean_v  = pos_mean.get(pos, 0)
        lines.append(f'## {pos_label[pos]}')
        lines.append(f'*Position avg value_score: {mean_v:.1f} pts/price-unit*')
        lines.append('')
        lines.append('| # | Player | Club | Nation | WC Tier | Price | Exp Pts | value_score | value_index | Alloc % |')
        lines.append('|---|--------|------|--------|---------|------:|--------:|------------:|------------:|--------:|')

        rank = 0
        for e in players:
            rank_str = '—'
            if e['value'] is not None:
                rank += 1
                rank_str = str(rank)
            pts_str   = f"{e['tot_pts']:.0f}"    if e['tot_pts']    is not None else '—'
            val_str   = f"{e['value']:.1f}"      if e['value']      is not None else '—'
            idx_str   = str(e['value_index'])    if e['value_index'] is not None else '—'
            alloc_str = f"{e['alloc_pct']:.2f}%" if e['alloc_pct']  is not None else '—'
            lines.append(
                f"| {rank_str} | {e['price_name']} | {e['club']} | {e['nat']} | {e['tier']} "
                f"| {e['price']} | {pts_str} | {val_str} | {idx_str} | {alloc_str} |"
            )
        lines.append('')
        lines.append('---')
        lines.append('')

    # Portfolio summary
    lines.append('## Portfolio Allocation Summary')
    lines.append(f'*{n_sel} players selected (value_index ≥ 100). Base: {base_pct}% × {n_sel} = {base_total:.1f}%. '
                 f'Extra {remaining:.1f}% split proportional to value_index.*')
    lines.append('')
    for pos in pos_order:
        pos_sel = [e for e in by_pos[pos] if e['alloc_pct'] is not None]
        pos_total = sum(e['alloc_pct'] for e in pos_sel)
        lines.append(f'**{pos_label[pos]}** ({len(pos_sel)} players, {pos_total:.1f}%): ' +
                     ', '.join(f"{e['price_name']} {e['alloc_pct']:.2f}%" for e in pos_sel))
    lines.append('')
    lines.append('---')
    lines.append('')

    # Top value picks summary
    all_analysed = [e for e in entries if e['value'] is not None]
    top_value = sorted(all_analysed, key=lambda e: -e['value'])[:20]
    lines.append('## Top 20 value picks across all positions')
    lines.append('')
    lines.append('| # | Player | Pos | Club | Nation | Tier | Price | Exp Pts | value_score | value_index |')
    lines.append('|---|--------|-----|------|--------|------|------:|--------:|------------:|------------:|')
    for i, e in enumerate(top_value, 1):
        lines.append(
            f"| {i} | {e['price_name']} | {e['bracket_pos']} | {e['club']} | {e['nat']} | {e['tier']} "
            f"| {e['price']} | {e['tot_pts']:.0f} | {e['value']:.1f} | {e['value_index']} |"
        )

    lines.append('')
    lines.append('---')
    lines.append('')

    # Biggest misprices: high value_index but high enough pts to matter
    big_value = sorted([e for e in all_analysed if e['tot_pts'] >= 200],
                       key=lambda e: -e['value_index'])
    lines.append('## Biggest positive misprices (meaningful WC expected pts, high value_index)')
    lines.append('')
    lines.append('| Player | Pos | Price | Exp Pts | value_score | value_index | Note |')
    lines.append('|--------|-----|------:|--------:|------------:|------------:|------|')
    for e in big_value[:15]:
        note = 'priced on club form, WC output much higher' if e['value_index'] > 150 else (
               'solid value' if e['value_index'] > 120 else '')
        lines.append(
            f"| {e['price_name']} | {e['bracket_pos']} | {e['price']} | {e['tot_pts']:.0f} "
            f"| {e['value']:.1f} | {e['value_index']} | {note} |"
        )

    out_path = '/tmp/world_cup/analysis/valuation_sheet.md'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

    print(f"Written: {out_path}")
    print(f"\nPos averages: { {p: round(v,1) for p,v in pos_mean.items()} }")
    print(f"\nTop 10 value picks:")
    for i, e in enumerate(top_value[:10], 1):
        print(f"  {i:2}. {e['price_name']:<28} {e['bracket_pos']:<4} £{e['price']:>3}  "
              f"{e['tot_pts']:>6.0f} pts  value={e['value']:>5.1f}  idx={e['value_index']}")


if __name__ == '__main__':
    main()
