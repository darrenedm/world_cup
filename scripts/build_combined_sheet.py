#!/usr/bin/env python3
"""
build_combined_sheet.py
Generates a single markdown sheet of all WC 2026 players grouped by
position (GK / DEF / MID / FWD) and ranked by adj. expected fantasy pts.

Output: analysis/all_players_by_position.md
"""
import csv
import os

DATA_PATH = '/tmp/wc_repo/data/master_sheet.csv'
OUT_PATH  = '/tmp/wc_repo/analysis/all_players_by_position.md'


def load_data():
    with open(DATA_PATH, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def minmax_rating(value, lo, hi, scale_lo=1.0, scale_hi=10.0):
    if hi <= lo:
        return round((scale_lo + scale_hi) / 2, 1)
    r = scale_lo + (scale_hi - scale_lo) * (value - lo) / (hi - lo)
    return round(max(scale_lo, min(scale_hi, r)), 1)


def build_tourn_ratings(all_rows):
    pos_pts = {'GK': [], 'DEF': [], 'MID': [], 'FWD': []}
    for r in all_rows:
        pts = float(r['adj_exp_fantasy_pts'])
        pos = r['position']
        if pos in pos_pts and pts > 0:
            pos_pts[pos].append(pts)
    pos_range = {pos: (min(v), max(v)) for pos, v in pos_pts.items() if v}
    ratings = {}
    for r in all_rows:
        pos  = r['position']
        pts  = float(r['adj_exp_fantasy_pts'])
        name = r['player']
        if pos in pos_range and pts > 0:
            lo, hi = pos_range[pos]
            ratings[name] = minmax_rating(pts, lo, hi)
        else:
            ratings[name] = 1.0
    return ratings


SKIP_FITNESS = {'fit', 'fit (irrelevant)', 'n/a', ''}

def fitness_flag(row):
    raw = (row.get('fitness_current') or row.get('fitness_flag') or '').strip()
    if raw.lower() in SKIP_FITNESS:
        return ''
    return raw


def tier_label(row):
    t = row['tier']
    if t in ('GK1', 'GK2', 'GK3'):
        return t
    return f'T{t}'


def fmt_note(row):
    """Short fitness/injury note; fall back to plain notes field."""
    fn = fitness_flag(row)
    if fn:
        return fn
    raw = (row.get('notes') or '').strip()
    if len(raw) > 60:
        raw = raw[:57] + '…'
    return raw


def main():
    all_rows = load_data()
    confirmed = [r for r in all_rows if int(r['wc_squad_prob_pct']) > 0]
    t_rat = build_tourn_ratings(all_rows)

    total = len(confirmed)

    pos_sections = [
        ('GK',  'Goalkeepers'),
        ('DEF', 'Defenders'),
        ('MID', 'Midfielders'),
        ('FWD', 'Forwards'),
    ]

    lines = []
    lines.append('# World Cup 2026 — All Players by Position')
    lines.append(f'*{total} confirmed squad members across 48 nations, ranked by adj. expected fantasy pts*  ')
    lines.append('*Tourn. = 1–10 vs all WC players at the same position (10 = best in tournament)*  ')
    lines.append('*Last updated: June 2026*')
    lines.append('')
    lines.append('---')
    lines.append('')

    for pos_key, pos_label in pos_sections:
        players = sorted(
            [r for r in confirmed if r['position'] == pos_key],
            key=lambda r: -float(r['adj_exp_fantasy_pts'])
        )
        if not players:
            continue

        lines.append(f'## {pos_label}')
        lines.append('')

        if pos_key == 'GK':
            lines.append(
                '| # | Player | Country | Club | Tier | Fitness | Adj Pts | Tourn. | Notes |'
            )
            lines.append(
                '|---|--------|---------|------|------|---------|--------:|-------:|-------|'
            )
            for i, r in enumerate(players, 1):
                name    = r['player']
                nat     = r['nationality']
                club    = r['club']
                tier    = tier_label(r)
                fit     = fitness_flag(r)
                pts     = float(r['adj_exp_fantasy_pts'])
                tr      = t_rat.get(name, 1.0)
                note    = fmt_note(r)
                fit_col = fit if fit else 'Fit'
                lines.append(
                    f'| {i} | {name} | {nat} | {club} | {tier} | {fit_col} '
                    f'| {pts:.1f} | {tr:.1f} | {note} |'
                )
        else:
            lines.append(
                '| # | Player | Country | Club | Pos | Tier | Fitness | Adj Pts | Tourn. | Notes |'
            )
            lines.append(
                '|---|--------|---------|------|-----|------|---------|--------:|-------:|-------|'
            )
            for i, r in enumerate(players, 1):
                name    = r['player']
                nat     = r['nationality']
                club    = r['club']
                sub_pos = r['sub_position'] or r['position']
                tier    = tier_label(r)
                fit     = fitness_flag(r)
                pts     = float(r['adj_exp_fantasy_pts'])
                tr      = t_rat.get(name, 1.0)
                note    = fmt_note(r)
                fit_col = fit if fit else 'Fit'
                lines.append(
                    f'| {i} | {name} | {nat} | {club} | {sub_pos} | {tier} | {fit_col} '
                    f'| {pts:.1f} | {tr:.1f} | {note} |'
                )

        lines.append('')

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

    print(f'Written: {OUT_PATH}  ({total} players)')
    for pos_key, pos_label in pos_sections:
        n = sum(1 for r in confirmed if r['position'] == pos_key)
        print(f'  {pos_label}: {n}')


if __name__ == '__main__':
    main()
