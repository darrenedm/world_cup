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
    ('Lamine Yamal',          'BAR', 'FWD', 0.0628),
    ('Michael Olise',         'FCB', 'MID', 0.0565),
    ('Kylian Mbappé',         'RMA', 'FWD', 0.0533),
    ('Harry Kane',            'FCB', 'FWD', 0.0431),
    ('Bruno Fernandes',       'MUN', 'MID', 0.0349),
    ('Ousmane Dembélé',       'PSG', 'FWD', 0.031),
    ('Pedri',                 'BAR', 'MID', 0.0304),
    ('Vitinha',               'PSG', 'MID', 0.0296),
    ('Erling Haaland',        'MCI', 'FWD', 0.0261),
    ('Vinícius Júnior',       'RMA', 'FWD', 0.0238),
    ('Mike Maignan',          'MIL', 'GK',  0.0268),
    ('Jérémy Doku',           'MCI', 'FWD', 0.0251),
    ('Gabriel Magalhães',     'ARS', 'DEF', 0.0221),
    ('Unai Simón',            'ATH', 'GK',  0.0218),
    ('Declan Rice',           'ARS', 'MID', 0.0233),
    ('David Raya',            'ARS', 'GK',  0.0217),
    ('William Saliba',        'ARS', 'DEF', 0.0236),
    ('Rayan Cherki',          'MCI', 'MID', 0.0219),
    ('Emiliano Martínez',     'AVL', 'GK',  0.0214),
    ('Marc Guéhi',            'MCI', 'DEF', 0.0189),
    ('Jordan Pickford',       'EVE', 'GK',  0.0234),
    ('Bukayo Saka',           'ARS', 'FWD', 0.0245),
    ('Joshua Kimmich',        'FCB', 'MID', 0.0187),
    ('Thibaut Courtois',      'RMA', 'GK',  0.0185),
    ('Raphinha',              'BAR', 'FWD', 0.0185),
    ('Kenan Yıldız',          'JUV', 'FWD', 0.0186),
    ('Virgil van Dijk',       'LIV', 'DEF', 0.0173),
    ('Nuno Mendes',           'PSG', 'DEF', 0.0189),
    ('Rodri',                 'MCI', 'MID', 0.0169),
    ('Ezri Konsa',            'AVL', 'DEF', 0.017),
    ('Pau Cubarsí',           'BAR', 'DEF', 0.0176),
    ('Désiré Doué',           'PSG', 'FWD', 0.0181),
    ('Dean Huijsen',          'RMA', 'DEF', 0.0163),
    ('João Neves',            'PSG', 'MID', 0.0159),
    ('Luis Díaz',             'FCB', 'FWD', 0.0183),
    ('Jude Bellingham',       'RMA', 'MID', 0.0211),
    ('Nico Schlotterbeck',    'BVB', 'DEF', 0.0136),
    ('Achraf Hakimi',         'PSG', 'DEF', 0.0156),
    ('Joško Gvardiol',        'MCI', 'DEF', 0.0154),
    ('Florian Wirtz',         'LIV', 'MID', 0.016),
    ('Trent Alexander-Arnold','RMA', 'DEF', 0.0142),
    ('Elliot Anderson',       'NFO', 'MID', 0.0154),
    ('Jules Koundé',          'BAR', 'DEF', 0.0152),
    ('Dayot Upamecano',       'FCB', 'DEF', 0.0153),
    ('Alisson Becker',        'LIV', 'GK',  0.0145),
    ('Rúben Dias',            'MCI', 'DEF', 0.0133),
    ('Julián Álvarez',        'ATM', 'FWD', 0.014),
    ('Jonathan Tah',          'FCB', 'DEF', 0.0146),
    ('Pedro Porro',           'TOT', 'DEF', 0.0152),
    ('Enzo Fernández',        'CHE', 'MID', 0.0133),
    ('Marc Cucurella',        'CHE', 'DEF', 0.0146),
    ('Matheus Cunha',         'MUN', 'FWD', 0.0122),
    ('Kvaratskhelia',         'PSG', 'FWD', 0.0117),   # Georgia — not in 24-country list
    ('Martin Ødegaard',       'ARS', 'MID', 0.0131),
    ('Gregor Kobel',          'BVB', 'GK',  0.0121),
    ('Viktor Gyökeres',       'ARS', 'FWD', 0.0112),
    ('Federico Valverde',     'RMA', 'MID', 0.0119),
    ('Ollie Watkins',         'AVL', 'FWD', 0.011),
    ('Donnarumma',            'MCI', 'GK',  0.00894),   # Italy — not analysed
    ('Cole Palmer',           'CHE', 'MID', 0.0116),
    ('Phil Foden',            'MCI', 'MID', 0.00852),
    ('Eberechi Eze',          'ARS', 'MID', 0.011),
    ('Lautaro Martínez',      'INT', 'FWD', 0.0117),
    ('Moisés Caicedo',        'CHE', 'MID', 0.0102),
    ('João Pedro',            'CHE', 'FWD', 0.0102),
    ('Christian Pulisic',     'MIL', 'MID', 0.01),
    ('Scott McTominay',       'NAP', 'MID', 0.01),
    ('Morgan Gibbs-White',    'NFO', 'MID', 0.00971),
    ('Kevin De Bruyne',       'NAP', 'MID', 0.0109),
    ('Fabián Ruiz',           'PSG', 'MID', 0.0103),
    ('Arda Güler',            'RMA', 'MID', 0.00953),
    ('Robin Le Normand',      'ATM', 'DEF', 0.00953),
    ('Jurriën Timber',        'ARS', 'DEF', 0.00959),
    ('Denzel Dumfries',       'INT', 'DEF', 0.0101),
    ('Dani Olmo',             'BAR', 'MID', 0.00945),
    ('Locatelli',             'JUV', 'MID', 0.00836),  # Italy — not analysed
    ('Cristian Romero',       'TOT', 'DEF', 0.00944),
    ('Joan García',           'BAR', 'GK',  0.0079),
    ('Rafael Leão',           'MIL', 'FWD', 0.00846),
    ('Dean Henderson',        'CRY', 'GK',  0.00763),
    ('Pedro Neto',            'CHE', 'FWD', 0.00815),
    ('Mason Greenwood',       'OM',  'FWD', 0.00863),
    ('Omar Marmoush',         'MCI', 'FWD', 0.00661),
    ('Ryan Gravenberch',      'LIV', 'MID', 0.00796),
    ('Neuer',                 'FCB', 'GK',  0.00762),  # Germany GK — not in CSV
    ('Mbeumo',                'MUN', 'FWD', 0.00743),  # Cameroon — not analysed
    ('Bastoni',               'INT', 'DEF', 0.0079),  # Italy — not analysed
    ('Alexander Isak',        'LIV', 'FWD', 0.0073),
    ('Rrahmani',              'NAP', 'DEF', 0.00677),  # Kosovo — not analysed
    ('Tonali',                'NEW', 'MID', 0.00648),  # Italy — not analysed
    ('Hakan Çalhanoğlu',      'INT', 'MID', 0.00733),
    ('Kerkez',                'LIV', 'DEF', 0.0064),  # Hungary — not analysed
    ('Alejandro Grimaldo',    'LEV', 'DEF', 0.00671),
    ('Matz Sels',             'NFO', 'GK',  0.00615),
    ('Mark Flekken',          'LEV', 'GK',  0.00588),
    ('Mohammed Kudus',        'TOT', 'MID', 0.00572),
    ('Guirassy',              'BVB', 'FWD', 0.00525),  # Guinea — not analysed
    ('Aina',                  'NFO', 'DEF', 0.00518),  # Nigeria — not analysed
    ('Di Gregorio',           'JUV', 'GK',  0.00571),  # Italy — not analysed
    ('Angelo Stiller',        'VFB', 'MID', 0.0051),
    ('Amad Diallo',           'MUN', 'FWD', 0.00512),
    ('Hugo Ekitiké',          'LIV', 'FWD', 0.00501),
    ('Antony',                'BET', 'FWD', 0.00422),
    ('Marcus Rashford',       'BAR', 'FWD', 0.00488),
    ('Tapsoba',               'LEV', 'DEF', 0.00492),  # Burkina Faso — not analysed
    ('Vicario',               'TOT', 'GK',  0.00477),  # Italy — not analysed
    ('Mohamed Salah',         'LIV', 'FWD', 0.00444),
    ('Maximilian Mittelstädt','VFB', 'DEF', 0.00446),
    ('Felix Nmecha',          'BVB', 'MID', 0.00441),
    ('Maghnes Akliouche',     'ASM', 'MID', 0.00425),
    ('Oblak',                 'ATM', 'GK',  0.00396),  # Slovenia — not analysed
    ('Exequiel Palacios',     'LEV', 'MID', 0.00455),
    ('Nick Woltemade',        'NEW', 'FWD', 0.00417),
    ('Jonathan David',        'JUV', 'FWD', 0.00393),
    ('Di Lorenzo',            'NAP', 'DEF', 0.00398),  # Italy — not analysed
    ('James Trafford',        'MCI', 'GK',  0.00395),
    ('Jobe Bellingham',       'BVB', 'MID', 0.00386),
    ('Daniel Svensson',       'BVB', 'DEF', 0.00376),
    ('Malik Tillman',         'LEV', 'MID', 0.00377),
    ('Robert Sánchez',        'CHE', 'GK',  0.00371),
    ('Gerónimo Rulli',        'OM',  'GK',  0.00367),
    ('Jarell Quansah',        'LEV', 'DEF', 0.0036),
    ('Pavlovic',              'MIL', 'DEF', 0.00345),  # Serbia — not analysed
    ('Nick Pope',             'NEW', 'GK',  0.00366),
    ('Álvaro Carreras',       'RMA', 'DEF', 0.00318),
    ('Romagnoli',             'LAZ', 'DEF', 0.00326),  # Italy — not analysed
    ('Romelu Lukaku',         'NAP', 'FWD', 0.00363),
    ('Serge Gnabry',          'FCB', 'FWD', 0.00302),
    ('Matías Soulé',          'ROM', 'FWD', 0.00301),
    ('Barella',               'INT', 'MID', 0.00313),  # Italy — not analysed
    ('Éder Militão',          'RMA', 'DEF', 0.0029),  # Brazil — not in CSV
    ('Simons',                'TOT', 'MID', 0.00284),  # Netherlands — not in CSV
    ('Højlund',               'NAP', 'FWD', 0.00279),  # Denmark — not analysed
    ('Karim Adeyemi',         'BVB', 'FWD', 0.00248),
    ('Jonathan Burkardt',     'SGE', 'FWD', 0.00247),
    ('Højbjerg',              'OM',  'MID', 0.00244),  # Denmark — not analysed
    ('Leny Yoro',             'MUN', 'DEF', 0.00235),
    ('Lucas Chevalier',       'PSG', 'GK',  0.00231),
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
    with open('/tmp/world_cup_fresh/data/master_sheet.csv', newline='', encoding='utf-8') as f:
        csv_rows = {r['player']: r for r in csv.DictReader(f)}

    # Build lookup: price_name → csv_row (or None)
    entries = []
    for (pname, club, bracket_pos, price) in PRICE_LIST:
        csv_name = NAME_MAP.get(pname, pname)
        row = csv_rows.get(csv_name)
        if row:
            raw_pts  = float(row['total_exp_fantasy_pts'])
            adj_pts  = float(row['adj_exp_fantasy_pts'])
            sq_prob  = int(row['wc_squad_prob_pct'])
            nat      = row['nationality']
            tier     = row['tier']
        else:
            raw_pts  = None
            adj_pts  = None
            sq_prob  = None
            nat      = '—'
            tier     = '—'
        entries.append({
            'price_name':  pname,
            'club':        club,
            'bracket_pos': bracket_pos,
            'price':       price,
            'raw_pts':     raw_pts,
            'tot_pts':     adj_pts,   # primary metric is probability-adjusted
            'sq_prob':     sq_prob,
            'nat':         nat,
            'tier':        tier,
            'value':       round(adj_pts / price, 2) if adj_pts is not None else None,
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
        f'*Players priced, ranked by probability-adjusted WC expected pts / price within each position bracket.*',
        '',
        '**Adj Pts** = `raw_exp_pts × squad_selection_probability` — discounts injured/uncertain players.',
        '**value_score** = `adj_exp_fantasy_pts / price` — higher is better value.',
        '**value_index** = value_score vs T1/T2 starter average (100 = average starter; 150 = 50% above average).',
        '**Sq%** = probability player is in their nation\'s final WC squad.',
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
        lines.append('| # | Player | Club | Nation | Tier | Sq% | Price | Adj Pts | value_score | value_index | Alloc % |')
        lines.append('|---|--------|------|--------|------|----:|------:|--------:|------------:|------------:|--------:|')

        rank = 0
        for e in players:
            rank_str = '—'
            if e['value'] is not None:
                rank += 1
                rank_str = str(rank)
            pts_str   = f"{e['tot_pts']:.0f}"    if e['tot_pts']    is not None else '—'
            sq_str    = f"{e['sq_prob']}%"        if e['sq_prob']    is not None else '—'
            val_str   = f"{e['value']:.1f}"       if e['value']      is not None else '—'
            idx_str   = str(e['value_index'])     if e['value_index'] is not None else '—'
            alloc_str = f"{e['alloc_pct']:.2f}%"  if e['alloc_pct']  is not None else '—'
            lines.append(
                f"| {rank_str} | {e['price_name']} | {e['club']} | {e['nat']} | {e['tier']} "
                f"| {sq_str} | {e['price']} | {pts_str} | {val_str} | {idx_str} | {alloc_str} |"
            )
        lines.append('')
        lines.append('---')
        lines.append('')

    # Portfolio summary
    lines.append('## Portfolio Allocation Summary')
    lines.append(f'*{n_sel} players selected (value_index ≥ 100, based on adj_exp_pts). Base: {base_pct}% × {n_sel} = {base_total:.1f}%. '
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
    lines.append('| # | Player | Pos | Club | Nation | Tier | Sq% | Price | Adj Pts | value_score | value_index |')
    lines.append('|---|--------|-----|------|--------|------|----:|------:|--------:|------------:|------------:|')
    for i, e in enumerate(top_value, 1):
        lines.append(
            f"| {i} | {e['price_name']} | {e['bracket_pos']} | {e['club']} | {e['nat']} | {e['tier']} "
            f"| {e['sq_prob']}% | {e['price']} | {e['tot_pts']:.0f} | {e['value']:.1f} | {e['value_index']} |"
        )

    lines.append('')
    lines.append('---')
    lines.append('')

    # Biggest misprices: high value_index but high enough pts to matter
    big_value = sorted([e for e in all_analysed if (e['raw_pts'] or 0) >= 200],
                       key=lambda e: -e['value_index'])
    lines.append('## Biggest positive misprices (meaningful WC expected pts, high value_index)')
    lines.append('')
    lines.append('| Player | Pos | Sq% | Price | Adj Pts | value_score | value_index | Note |')
    lines.append('|--------|-----|----:|------:|--------:|------------:|------------:|------|')
    for e in big_value[:15]:
        note = 'priced on club form, WC output much higher' if e['value_index'] > 150 else (
               'solid value' if e['value_index'] > 120 else '')
        lines.append(
            f"| {e['price_name']} | {e['bracket_pos']} | {e['sq_prob']}% | {e['price']} | {e['tot_pts']:.0f} "
            f"| {e['value']:.1f} | {e['value_index']} | {note} |"
        )

    out_path = '/tmp/world_cup_fresh/analysis/valuation_sheet.md'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

    print(f"Written: {out_path}")
    print(f"\nPos averages: { {p: round(v,1) for p,v in pos_mean.items()} }")
    print(f"\nTop 10 value picks (by adj pts / price):")
    for i, e in enumerate(top_value[:10], 1):
        print(f"  {i:2}. {e['price_name']:<28} {e['bracket_pos']:<4} {e['sq_prob']:>3}%sq  "
              f"£{e['price']:>6}  adj={e['tot_pts']:>6.0f}pts  idx={e['value_index']}")


if __name__ == '__main__':
    main()
