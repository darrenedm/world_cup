#!/usr/bin/env python3
"""
build_dashboard_data.py
Reads master_sheet.csv and enrichment dicts from price_value_lookup.py.
Outputs a JSON blob for embedding in the breakout_stars_dashboard.html.

Usage:
    python3 /private/tmp/wc_repo/scripts/build_dashboard_data.py > /tmp/wc_dashboard_data.json
"""

import csv
import json
import sys
import os

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_PATH   = os.path.join(SCRIPT_DIR, '..', 'data', 'master_sheet.csv')

# Add scripts dir to path so we can import price_value_lookup
sys.path.insert(0, SCRIPT_DIR)
from price_value_lookup import (
    PRICE_LIST,
    LIVE_STATUS,
    FRIENDLY,
    G1_WIN,
    CONFIRMED_OUT,
)

# ── Group structure (confirmed from data) ──────────────────────────────────────
GROUPS = {
    'A': ['Czech Republic', 'Mexico', 'South Africa', 'South Korea'],
    'B': ['Bosnia', 'Canada', 'Qatar', 'Switzerland'],
    'C': ['Brazil', 'Haiti', 'Morocco', 'Scotland'],
    'D': ['Australia', 'Paraguay', 'Turkey', 'USA'],
    'E': ['Curaçao', 'Ecuador', 'Germany', 'Ivory Coast'],
    'F': ['Japan', 'Netherlands', 'Sweden', 'Tunisia'],
    'G': ['Belgium', 'Egypt', 'Iran', 'New Zealand'],
    'H': ['Cape Verde', 'Saudi Arabia', 'Spain', 'Uruguay'],
    'I': ['France', 'Iraq', 'Norway', 'Senegal'],
    'J': ['Algeria', 'Argentina', 'Austria', 'Jordan'],
    'K': ['Colombia', 'DR Congo', 'Portugal', 'Uzbekistan'],
    'L': ['Croatia', 'England', 'Ghana', 'Panama'],
}

# ── Build lookup: display_name → (price, full_name) ───────────────────────────
# Only include players that actually map to WC players (full_name is not None)
price_by_fullname  = {}   # full_name → (display_name, price)
price_by_display   = {}   # display_name → price

for display, price, full_name in PRICE_LIST:
    if full_name is None:
        continue
    # Handle "Name|Nation" disambiguation (store the base name)
    base_name = full_name.split('|')[0] if '|' in full_name else full_name
    price_by_display[display] = price
    # Map full (base) name → price (prefer highest price if collisions)
    if base_name not in price_by_fullname or price > price_by_fullname[base_name][1]:
        price_by_fullname[base_name] = (display, price)

# Build display_name lookup keyed by full_name (for LIVE_STATUS / FRIENDLY lookups)
fullname_to_display = {v[0]: k for k, v in {fn: (disp, p) for fn, (disp, p) in price_by_fullname.items()}.items()}
# Invert: full_name → display_name
fullname_to_display = {}
for display, price, full_name in PRICE_LIST:
    if full_name is None:
        continue
    base_name = full_name.split('|')[0] if '|' in full_name else full_name
    fullname_to_display[base_name] = display

# ── Load master_sheet.csv ─────────────────────────────────────────────────────
def load_master():
    with open(DATA_PATH, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

# ── Fitness weight ─────────────────────────────────────────────────────────────
FITNESS_WEIGHT = {'full': 1.0, 'mostly': 0.85, 'not': 0.2}

# ── Build player record ────────────────────────────────────────────────────────
def build_player(row):
    try:
        adj_pts          = float(row['adj_exp_fantasy_pts'])
        wc_squad_prob    = float(row.get('wc_squad_prob_pct', 0))
        action_pts_per90 = float(row['action_pts_per_90'])
        group_mins       = float(row['group_mins_per_game'])
        p_advance        = int(float(row.get('country_p_advance_pct', 0)))
    except (ValueError, KeyError):
        return None

    # Confirmed only
    if wc_squad_prob <= 0 or adj_pts <= 0:
        return None

    player_name = row['player']
    nationality = row['nationality']

    # pts_per_game
    pts_per_game = action_pts_per90 * group_mins / 90.0

    # Look up price / display_name
    display_name = fullname_to_display.get(player_name)
    price        = price_by_fullname.get(player_name, (None, None))[1] if player_name in price_by_fullname else None

    # Also check confirmed-out (if display_name is in CONFIRMED_OUT, skip)
    if display_name and display_name in CONFIRMED_OUT:
        return None

    # Fitness / starter from LIVE_STATUS
    if display_name and display_name in LIVE_STATUS:
        fitness, starter = LIVE_STATUS[display_name]
    else:
        fitness, starter = '?', '?'

    # Friendly data
    if display_name and display_name in FRIENDLY:
        f_starts, f_apps = FRIENDLY[display_name]
    else:
        f_starts, f_apps = 0, 0

    # G1 win pct
    g1_win_pct = G1_WIN.get(nationality, 0)

    # ── Breakout score ─────────────────────────────────────────────────────────
    fitness_weight    = FITNESS_WEIGHT.get(fitness, 0.7)
    form_weight       = 1 + f_apps * 0.15
    established_pen   = 0.4 if price and price > 0.020 else 0.0

    if price:
        breakout_score = (
            (pts_per_game * 8 / price)
            * fitness_weight
            * form_weight
            * (1 - established_pen)
            / 1000
        )
    else:
        breakout_score = (
            pts_per_game
            * fitness_weight
            * form_weight
            * (1 - established_pen)
            / 5
        )

    # ── Breakout tier ──────────────────────────────────────────────────────────
    if price and price > 0.020:
        tier = 'star'
    elif breakout_score >= 40 and (price is None or price <= 0.012):
        tier = 'sleeper'
    elif breakout_score >= 15 and (price is None or price <= 0.020) and not (breakout_score >= 40 and (price is None or price <= 0.012)):
        tier = 'rising'
    elif p_advance < 35:
        tier = 'wildcard'
    else:
        tier = 'squad'

    return {
        'name':           player_name,
        'display_name':   display_name,
        'position':       row['position'],
        'sub_position':   row.get('sub_position', ''),
        'club':           row.get('club', ''),
        'country':        nationality,
        'group':          row.get('group', ''),
        'pts_per_game':   round(pts_per_game, 3),
        'adj_pts':        round(adj_pts, 2),
        'p_advance':      p_advance,
        'g1_win_pct':     g1_win_pct,
        'price':          price,
        'fitness':        fitness,
        'starter':        starter,
        'f_starts':       f_starts,
        'f_apps':         f_apps,
        'breakout_score': round(breakout_score, 3),
        'breakout_tier':  tier,
        'notes':          row.get('notes', ''),
    }


def build_countries(players):
    """Build the 48-country list from player data."""
    seen   = {}  # country → best p_advance
    for p in players:
        c = p['country']
        if c not in seen or p['p_advance'] > seen[c]['p_advance']:
            seen[c] = {
                'name':      c,
                'group':     p['group'],
                'p_advance': p['p_advance'],
                'g1_win_pct': p['g1_win_pct'],
            }
    return sorted(seen.values(), key=lambda x: x['name'])


def main():
    rows    = load_master()
    players = []
    for row in rows:
        rec = build_player(row)
        if rec:
            players.append(rec)

    # Sort by adj_pts descending
    players.sort(key=lambda p: -p['adj_pts'])

    countries = build_countries(players)

    output = {
        'players':   players,
        'countries': countries,
        'groups':    GROUPS,
    }

    print(json.dumps(output, ensure_ascii=False, indent=None))


if __name__ == '__main__':
    main()
