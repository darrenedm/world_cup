#!/usr/bin/env python3
"""
build_country_sheet.py
Generates a per-country player rating sheet from master_sheet.csv.

Ratings:
  Tourn. (1–10, 1dp) — adj_exp_fantasy_pts normalised against all players
                        in the same position group (GK/DEF/MID/FWD) across
                        the full dataset. 10 = best at that position in the
                        tournament, 1 = lowest in the dataset.
  Squad  (1–10, 1dp) — adj_exp_fantasy_pts normalised against all tracked
                        players on this specific squad regardless of position.
                        10 = this team's highest-expected-pts player, 1 = lowest.

Usage:
  python3 build_country_sheet.py             → generates England
  python3 build_country_sheet.py "Germany"   → generates Germany
  python3 build_country_sheet.py all         → generates every country in dataset
"""
import csv
import os
import sys

DATA_PATH = '/tmp/world_cup_repo/data/master_sheet.csv'
OUT_DIR   = '/tmp/world_cup_repo/countries'


def load_data():
    with open(DATA_PATH, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def minmax_rating(value, lo, hi, scale_lo=1.0, scale_hi=10.0):
    if hi <= lo:
        return round((scale_lo + scale_hi) / 2, 1)
    r = scale_lo + (scale_hi - scale_lo) * (value - lo) / (hi - lo)
    return round(max(scale_lo, min(scale_hi, r)), 1)


def build_tournament_ratings(all_rows):
    """1–10 rating within each position group across the entire dataset."""
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


def build_squad_ratings(squad_rows):
    """1–10 rating across all tracked players on this squad."""
    pts_vals = [float(r['adj_exp_fantasy_pts']) for r in squad_rows]
    if not pts_vals:
        return {}
    lo, hi = min(pts_vals), max(pts_vals)
    return {r['player']: minmax_rating(float(r['adj_exp_fantasy_pts']), lo, hi)
            for r in squad_rows}


SKIP_FITNESS_NOTES = {'fit', 'fit (irrelevant)', 'n/a', ''}


def fitness_note(row):
    raw = (row.get('fitness_current') or '').strip()
    if raw.lower() in SKIP_FITNESS_NOTES:
        return None
    return raw


ROLE_SHORT = {
    'Automatic Starter': 'Starter',
    'Regular Starter':   'Starter',
    'Starting GK':       'Starter',
    'Backup GK':         'Backup',
    'Third GK':          'Backup',
    'Impact Sub':        'Impact',
    'Sporadic':          'Sporadic',
    'Depth':             'Depth',
}


def fmt_role(role):
    for k, v in ROLE_SHORT.items():
        if k.lower() in role.lower():
            return v
    return role


def build_sheet(country, all_rows):
    squad = [r for r in all_rows if r['nationality'] == country]
    if not squad:
        print(f'No players found for {country}')
        return None

    confirmed = [r for r in squad if int(r['wc_squad_prob_pct']) > 0]
    t_rat = build_tournament_ratings(all_rows)
    s_rat = build_squad_ratings(confirmed)
    not_sel   = [r for r in squad if int(r['wc_squad_prob_pct']) == 0]

    sample  = squad[0]
    group   = sample.get('group', '?')
    adv     = sample.get('country_p_advance_pct', '?')
    dead_rb = sample.get('country_p_dead_rubber_g3_pct', '?')

    lines = []
    lines.append(f'# {country} — World Cup 2026')
    lines.append(
        f'**Group {group}** · Advancement {adv}% · Dead rubber risk {dead_rb}%  '
    )
    lines.append(
        f'*{len(confirmed)}/26 squad members tracked · '
        f'{len(not_sel)} tracked players not selected*'
    )
    lines.append('')
    lines.append(
        '**Tourn.** = 1–10 vs all WC players at the same position '
        '(10 = best at that position in the tournament)  '
    )
    lines.append(
        '**Squad** = 1–10 across all tracked players on this squad '
        '(10 = highest adj. expected pts on the team)'
    )
    lines.append('')
    lines.append('---')
    lines.append('')

    pos_sections = [
        ('GK',  'Goalkeepers'),
        ('DEF', 'Defenders'),
        ('MID', 'Midfielders'),
        ('FWD', 'Forwards'),
    ]

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
                '| Tier | Player | Club | Sq% | Fitness | Role | '
                'Act/90 | Adj Pts | Tourn. | Squad |'
            )
            lines.append(
                '|------|--------|------|----:|---------|------|'
                '-------:|--------:|-------:|------:|'
            )
            for r in players:
                lines.append(
                    f"| {r['tier']} | {r['player']} | {r['club']} "
                    f"| {r['wc_squad_prob_pct']}% | {r['fitness_flag']} "
                    f"| {fmt_role(r['playing_role'])} "
                    f"| {r['action_pts_per_90']} | {r['adj_exp_fantasy_pts']} "
                    f"| {t_rat[r['player']]} | {s_rat[r['player']]} |"
                )
                note = fitness_note(r)
                if note:
                    lines.append(f"  > *{note}*")
        else:
            lines.append(
                '| Tier | Player | Club | Sub-Pos | Role | Sq% | Fitness | '
                'Act/90 | Adj Pts | Tourn. | Squad |'
            )
            lines.append(
                '|------|--------|------|---------|------|----:|---------|'
                '-------:|--------:|-------:|------:|'
            )
            for r in players:
                sub = r.get('sub_position') or '—'
                lines.append(
                    f"| {r['tier']} | {r['player']} | {r['club']} | {sub} "
                    f"| {fmt_role(r['playing_role'])} "
                    f"| {r['wc_squad_prob_pct']}% | {r['fitness_flag']} "
                    f"| {r['action_pts_per_90']} | {r['adj_exp_fantasy_pts']} "
                    f"| {t_rat[r['player']]} | {s_rat[r['player']]} |"
                )
                note = fitness_note(r)
                if note:
                    lines.append(f"  > *{note}*")
        lines.append('')

    # Squad summary table (confirmed players only, top 12)
    confirmed_sorted = sorted(confirmed, key=lambda r: -float(r['adj_exp_fantasy_pts']))
    lines.append('---')
    lines.append('')
    lines.append('## Squad summary — top players by expected pts')
    lines.append('')
    lines.append('| # | Player | Pos | Club | Adj Pts | Tourn. | Squad |')
    lines.append('|---|--------|-----|------|--------:|-------:|------:|')
    for i, r in enumerate(confirmed_sorted[:12], 1):
        lines.append(
            f"| {i} | {r['player']} | {r['position']} | {r['club']} "
            f"| {r['adj_exp_fantasy_pts']} "
            f"| {t_rat[r['player']]} | {s_rat[r['player']]} |"
        )

    # Not-selected section
    if not_sel:
        lines.append('')
        lines.append('---')
        lines.append('')
        lines.append('## Not selected')
        lines.append('')
        lines.append('*Tracked players confirmed NOT in the final squad.*')
        lines.append('')
        lines.append('| Player | Pos | Club | Notes |')
        lines.append('|--------|-----|------|-------|')
        for r in sorted(not_sel, key=lambda r: r['position']):
            note = (r.get('notes') or '').split(';')[0][:80]
            lines.append(f"| {r['player']} | {r['position']} | {r['club']} | {note} |")

    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append(
        '*Squad members not in this dataset (unlisted fringe/backup players) '
        'have not been rated.*'
    )

    os.makedirs(OUT_DIR, exist_ok=True)
    slug     = country.lower().replace(' ', '_')
    out_path = os.path.join(OUT_DIR, f'{slug}.md')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'Written: {out_path}  ({len(squad)} players)')
    return out_path


def main():
    all_rows = load_data()

    if len(sys.argv) < 2 or sys.argv[1] == 'England':
        build_sheet('England', all_rows)
    elif sys.argv[1] == 'all':
        from collections import Counter
        countries = [k for k, _ in Counter(r['nationality'] for r in all_rows).most_common()]
        for c in countries:
            build_sheet(c, all_rows)
    else:
        build_sheet(sys.argv[1], all_rows)


if __name__ == '__main__':
    main()
