#!/usr/bin/env python3
"""
build_valuation.py
Cross-references price-list with master_sheet.csv expected WC points.
Outputs analysis/valuation_sheet.md — ranked by value_score within each position bracket.
value_score = total_exp_fantasy_pts / price
value_index = (value_score / position_mean_value_score) × 100  (100 = average)
"""
import csv
from collections import defaultdict

# ──────────────────────────────────────────────────────────────────────────────
# PRICE LIST  (price_name, club, bracket_pos, price)
# bracket_pos is the position used for the competition bracket (GK/DEF/MID/FWD)
# ──────────────────────────────────────────────────────────────────────────────
PRICE_LIST = [
    ('Lamine Yamal',         'BAR', 'FWD', 40),
    ('Michael Olise',        'FCB', 'MID', 40),
    ('Kylian Mbappé',        'RMA', 'FWD', 25),
    ('Harry Kane',           'FCB', 'FWD', 30),
    ('Bruno Fernandes',      'MUN', 'MID', 30),
    ('Ousmane Dembélé',      'PSG', 'FWD', 15),
    ('Pedri',                'BAR', 'MID', 30),
    ('Vitinha',              'PSG', 'MID', 20),
    ('Erling Haaland',       'MCI', 'FWD', 20),
    ('Vinícius Júnior',      'RMA', 'FWD', 25),
    ('Mike Maignan',         'MIL', 'GK',  15),
    ('Jérémy Doku',          'MCI', 'FWD', 35),
    ('Gabriel Magalhães',    'ARS', 'DEF', 35),
    ('Unai Simón',           'ATH', 'GK',  15),
    ('Declan Rice',          'ARS', 'MID', 25),
    ('David Raya',           'ARS', 'GK',  40),
    ('William Saliba',       'ARS', 'DEF', 30),
    ('Rayan Cherki',         'MCI', 'MID', 30),
    ('Emiliano Martínez',    'AVL', 'GK',  30),
    ('Marc Guéhi',           'MCI', 'DEF', 35),
    ('Jordan Pickford',      'EVE', 'GK',  10),
    ('Bukayo Saka',          'ARS', 'FWD', 20),
    ('Joshua Kimmich',       'FCB', 'MID', 30),
    ('Thibaut Courtois',     'RMA', 'GK',  25),
    ('Raphinha',             'BAR', 'FWD', 30),
    ('Kenan Yıldız',         'JUV', 'FWD', 15),
    ('Virgil van Dijk',      'LIV', 'DEF', 25),
    ('Nuno Mendes',          'PSG', 'DEF', 20),
    ('Rodri',                'MCI', 'MID', 25),
    ('Ezri Konsa',           'AVL', 'DEF', 15),
    ('Pau Cubarsí',          'BAR', 'DEF', 35),
    ('Désiré Doué',          'PSG', 'FWD', 25),
    ('Dean Huijsen',         'RMA', 'DEF', 20),
    ('João Neves',           'PSG', 'MID', 15),
    ('Luis Díaz',            'FCB', 'FWD', 25),
    ('Jude Bellingham',      'RMA', 'MID', 15),
    ('Nico Schlotterbeck',   'BVB', 'DEF', 25),
    ('Achraf Hakimi',        'PSG', 'DEF', 25),
    ('Joško Gvardiol',       'MCI', 'DEF', 30),
    ('Florian Wirtz',        'LIV', 'MID', 15),
    ('Trent Alexander-Arnold','RMA','DEF', 10),
    ('Elliot Anderson',      'NFO', 'MID', 25),
    ('Jules Koundé',         'BAR', 'DEF', 15),
    ('Dayot Upamecano',      'FCB', 'DEF', 20),
    ('Alisson Becker',       'LIV', 'GK',  30),
    ('Rúben Dias',           'MCI', 'DEF', 20),
    ('Julián Álvarez',       'ATM', 'FWD', 15),
    ('Jonathan Tah',         'FCB', 'DEF', 10),
    ('Pedro Porro',          'TOT', 'DEF', 15),
    ('Enzo Fernández',       'CHE', 'MID', 10),
    ('Marc Cucurella',       'CHE', 'DEF',  5),
    ('Matheus Cunha',        'MUN', 'FWD', 20),
    ('Kvaratskhelia',        'PSG', 'FWD', 35),   # Georgia — not in 24-country list
    ('Martin Ødegaard',      'ARS', 'MID', 10),
    ('Gregor Kobel',         'BVB', 'GK',  15),
    ('Viktor Gyökeres',      'ARS', 'FWD', 15),
    ('Federico Valverde',    'RMA', 'MID', 30),
    ('Ollie Watkins',        'AVL', 'FWD', 15),
    ('Donnarumma',           'MCI', 'GK',  25),   # Italy — not analysed
    ('Cole Palmer',          'CHE', 'MID', 10),
    ('Phil Foden',           'MCI', 'MID',  5),
    ('Eberechi Eze',         'ARS', 'MID', 15),
    ('Lautaro Martínez',     'INT', 'FWD', 20),
    ('Moisés Caicedo',       'CHE', 'MID', 10),
    ('João Pedro',           'CHE', 'FWD', 15),
    ('Christian Pulisic',    'MIL', 'MID',  5),
    ('Scott McTominay',      'NAP', 'MID', 15),
    ('Morgan Gibbs-White',   'NFO', 'MID', 25),
    ('Kevin De Bruyne',      'NAP', 'MID', 15),
    ('Fabián Ruiz',          'PSG', 'MID', 10),
    ('Arda Güler',           'RMA', 'MID', 15),
    ('Robin Le Normand',     'ATM', 'DEF',  5),
    ('Jurriën Timber',       'ARS', 'DEF', 15),
    ('Denzel Dumfries',      'INT', 'DEF',  5),
    ('Dani Olmo',            'BAR', 'MID', 15),
    ('Locatelli',            'JUV', 'MID', 30),   # Italy — not analysed
    ('Cristian Romero',      'TOT', 'DEF', 10),
    ('Joan García',          'BAR', 'GK',  30),
    ('Rafael Leão',          'MIL', 'FWD', 10),
    ('Dean Henderson',       'CRY', 'GK',  10),
    ('Pedro Neto',           'CHE', 'FWD', 10),
    ('Mason Greenwood',      'OM',  'FWD', 20),
    ('Omar Marmoush',        'MCI', 'FWD',  5),
    ('Ryan Gravenberch',     'LIV', 'MID', 15),
    ('Neuer',                'FCB', 'GK',  15),   # Germany GK — not in CSV
    ('Mbeumo',               'MUN', 'FWD', 10),   # Cameroon — not analysed
    ('Bastoni',              'INT', 'DEF', 15),   # Italy — not analysed
    ('Alexander Isak',       'LIV', 'FWD',  5),
    ('Rrahmani',             'NAP', 'DEF', 20),   # Kosovo — not analysed
    ('Tonali',               'NEW', 'MID', 10),   # Italy — not analysed
    ('Hakan Çalhanoğlu',     'INT', 'MID', 30),
    ('Kerkez',               'LIV', 'DEF',  5),   # Hungary — not analysed
    ('Alejandro Grimaldo',   'LEV', 'DEF', 30),
    ('Matz Sels',            'NFO', 'GK',  15),
    ('Mark Flekken',         'LEV', 'GK',  15),
    ('Mohammed Kudus',       'TOT', 'MID',  5),
    ('Guirassy',             'BVB', 'FWD', 15),   # Guinea — not analysed
    ('Aina',                 'NFO', 'DEF', 15),   # Nigeria — not analysed
    ('Di Gregorio',          'JUV', 'GK',  25),   # Italy — not analysed
    ('Angelo Stiller',       'VFB', 'MID', 20),
    ('Amad Diallo',          'MUN', 'FWD', 10),
    ('Hugo Ekitiké',         'LIV', 'FWD', 10),
    ('Antony',               'BET', 'FWD', 15),
    ('Marcus Rashford',      'BAR', 'FWD', 15),
    ('Tapsoba',              'LEV', 'DEF', 25),   # Burkina Faso — not analysed
    ('Vicario',              'TOT', 'GK',   5),   # Italy — not analysed
    ('Mohamed Salah',        'LIV', 'FWD', 15),
    ('Maximilian Mittelstädt','VFB','DEF', 25),
    ('Felix Nmecha',         'BVB', 'MID',  5),
    ('Maghnes Akliouche',    'ASM', 'MID', 10),
    ('Oblak',                'ATM', 'GK',  10),   # Slovenia — not analysed
    ('Exequiel Palacios',    'LEV', 'MID', 15),
    ('Nick Woltemade',       'NEW', 'FWD',  5),
    ('Jonathan David',       'JUV', 'FWD',  5),
    ('Di Lorenzo',           'NAP', 'DEF', 10),   # Italy — not analysed
    ('James Trafford',       'MCI', 'GK',  15),
    ('Jobe Bellingham',      'BVB', 'MID', 10),
    ('Daniel Svensson',      'BVB', 'DEF',  5),
    ('Malik Tillman',        'LEV', 'MID',  5),
    ('Robert Sánchez',       'CHE', 'GK',   5),
    ('Gerónimo Rulli',       'OM',  'GK',   5),
    ('Jarell Quansah',       'LEV', 'DEF', 10),
    ('Pavlovic',             'MIL', 'DEF', 20),   # Serbia — not analysed
    ('Nick Pope',            'NEW', 'GK',  15),
    ('Álvaro Carreras',      'RMA', 'DEF', 10),
    ('Romagnoli',            'LAZ', 'DEF', 15),   # Italy — not analysed
    ('Romelu Lukaku',        'NAP', 'FWD',  5),
    ('Serge Gnabry',         'FCB', 'FWD', 15),
    ('Matías Soulé',         'ROM', 'FWD', 15),
    ('Barella',              'INT', 'MID', 20),   # Italy — not analysed
    ('Éder Militão',         'RMA', 'DEF', 15),   # Brazil — check CSV
    ('Simons',               'TOT', 'MID', 15),   # Netherlands — check CSV
    ('Højlund',              'NAP', 'FWD', 10),   # Denmark — not analysed
    ('Karim Adeyemi',        'BVB', 'FWD',  5),
    ('Jonathan Burkardt',    'SGE', 'FWD',  5),
    ('Højbjerg',             'OM',  'MID', 15),   # Denmark — not analysed
    ('Leny Yoro',            'MUN', 'DEF',  5),
    ('Lucas Chevalier',      'PSG', 'GK',  10),
    ('Rodon',                'LEE', 'DEF',  5),   # Wales — not in WC 2026
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

    # Compute position-mean value (only players WITH pts)
    pos_values = defaultdict(list)
    for e in entries:
        if e['value'] is not None:
            pos_values[e['bracket_pos']].append(e['value'])
    pos_mean = {p: sum(vs)/len(vs) for p, vs in pos_values.items()}

    for e in entries:
        if e['value'] is not None and e['bracket_pos'] in pos_mean:
            e['value_index'] = round(e['value'] / pos_mean[e['bracket_pos']] * 100)
        else:
            e['value_index'] = None

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
        '**value_index** = value_score vs position average (100 = average; 150 = 50% above average).',
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
        lines.append('| # | Player | Club | Nation | WC Tier | Price | Exp Pts | value_score | value_index |')
        lines.append('|---|--------|------|--------|---------|------:|--------:|------------:|------------:|')

        rank = 0
        for e in players:
            rank_str = '—'
            if e['value'] is not None:
                rank += 1
                rank_str = str(rank)
            pts_str  = f"{e['tot_pts']:.0f}"  if e['tot_pts']  is not None else '—'
            val_str  = f"{e['value']:.1f}"    if e['value']    is not None else '—'
            idx_str  = str(e['value_index'])  if e['value_index'] is not None else '—'
            lines.append(
                f"| {rank_str} | {e['price_name']} | {e['club']} | {e['nat']} | {e['tier']} "
                f"| {e['price']} | {pts_str} | {val_str} | {idx_str} |"
            )
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
