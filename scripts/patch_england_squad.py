#!/usr/bin/env python3
"""
patch_england_squad.py
One-off script to sync England dataset rows with the confirmed 26-man WC squad.
  - Sets wc_squad_prob_pct=100 for all confirmed squad members already in the CSV
  - Sets wc_squad_prob_pct=0  for players confirmed NOT selected
  - Appends the 12 squad members not yet in the CSV
Run ONCE, then re-run compute_pts_per_90.py to rebuild adj pts.
"""
import csv, os

PATH = '/tmp/world_cup_repo/data/master_sheet.csv'

# Players confirmed NOT in the England squad
NOT_SELECTED = {
    'Nick Pope', 'Trent Alexander-Arnold', 'Cole Palmer',
    'Morgan Gibbs-White', 'Phil Foden', 'Jobe Bellingham',
    'Mason Greenwood',
}

# Players confirmed IN the England squad (already in CSV)
CONFIRMED_IN = {
    'Jordan Pickford', 'Dean Henderson', 'James Trafford',
    'Marc Guéhi', 'Ezri Konsa', 'Jarell Quansah',
    'Declan Rice', 'Jude Bellingham', 'Elliot Anderson', 'Eberechi Eze',
    'Harry Kane', 'Bukayo Saka', 'Ollie Watkins', 'Marcus Rashford',
}

# 12 new players to add — metadata cols only; pts cols computed afterwards
# Columns: player, position, sub_position, club, nationality, group,
#          wc_squad_prob_pct, tier, playing_role,
#          group_mins_per_game, exp_post_group_mins_total,
#          country_p_advance_pct, country_p_dead_rubber_g3_pct,
#          fitness_flag, notes,
#          action_pts_per_90, exp_pts_per_90, total_exp_fantasy_pts,
#          int_l5_pattern, int_l5_starts, int_absence_reason,
#          fitness_current, tier_evidence, tier_revised, adj_exp_fantasy_pts
NEW_PLAYERS = [
    # ── Defenders ──────────────────────────────────────────────────────────
    dict(
        player='Reece James', position='DEF', sub_position='RB',
        club='Chelsea', nationality='England', group='L',
        wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
        group_mins_per_game=71.0, exp_post_group_mins_total=222,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=55,
        fitness_flag='Injury',
        notes='First-choice RB in absence of TAA; hamstring surgery Jan 2026; '
              'on track for Jun 11 opener; Tuchel trusts him implicitly when fit',
        int_l5_pattern='90/DNP/90/90/DNP', int_l5_starts=3,
        int_absence_reason='Hamstring Jan 2026',
        fitness_current='Injury: on track for Jun 11; hamstring surgery Jan 2026',
        tier_evidence='First-choice RB; fitness concern but confirmed Tuchel No.1',
        tier_revised='2',
    ),
    dict(
        player='John Stones', position='DEF', sub_position='CB',
        club='Manchester City', nationality='England', group='L',
        wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
        group_mins_per_game=71.0, exp_post_group_mins_total=222,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=55,
        fitness_flag='Injury',
        notes='Quality ball-playing CB; persistent knee issue missed final 7 weeks; '
              'targeting WC; Tuchel knows him well; strong aerial presence',
        int_l5_pattern='90/DNP/90/DNP/DNP', int_l5_starts=2,
        int_absence_reason='Knee injury Mar–May 2026',
        fitness_current='Injury: targeting Jun 11; knee managed',
        tier_evidence='Tier 1 quality but injury-managed; paired with Guéhi',
        tier_revised='2',
    ),
    dict(
        player='Nico O\'Reilly', position='DEF', sub_position='LB',
        club='Manchester City', nationality='England', group='L',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=39.0, exp_post_group_mins_total=64,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=55,
        fitness_flag='Fit',
        notes='Man City versatile LB/CM; England\'s only natural LB option; '
              'may feature more than Tier 3 suggests due to squad LB scarcity; '
              'first senior WC',
        int_l5_pattern='90/90/DNP/90/DNP', int_l5_starts=3,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Surprise call-up; England\'s de facto LB option',
        tier_revised='3',
    ),
    dict(
        player='Tino Livramento', position='DEF', sub_position='RB',
        club='Newcastle United', nationality='England', group='L',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=30.0, exp_post_group_mins_total=50,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=55,
        fitness_flag='Fit',
        notes='Quick, attack-minded RB; Newcastle first team regular; '
              'backup to Reece James; can play on either flank',
        int_l5_pattern='90/90/90/DNP/90', int_l5_starts=4,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Backup RB behind Reece James; rotation option',
        tier_revised='3',
    ),
    dict(
        player='Djed Spence', position='DEF', sub_position='RB',
        club='Tottenham Hotspur', nationality='England', group='L',
        wc_squad_prob_pct=100, tier='4', playing_role='Depth',
        group_mins_per_game=10.0, exp_post_group_mins_total=20,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=55,
        fitness_flag='Fit',
        notes='Squad depth RB; Spurs this season; minimal expected minutes',
        int_l5_pattern='DNP/90/DNP/DNP/90', int_l5_starts=2,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='4th-choice RB; squad cover',
        tier_revised='4',
    ),
    dict(
        player='Dan Burn', position='DEF', sub_position='CB',
        club='Newcastle United', nationality='England', group='L',
        wc_squad_prob_pct=100, tier='4', playing_role='Depth',
        group_mins_per_game=10.0, exp_post_group_mins_total=20,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=55,
        fitness_flag='Fit',
        notes='Veteran utility CB/LB (32); aerial threat; squad depth and '
              'leadership; unlikely to start unless injuries mount',
        int_l5_pattern='90/DNP/90/90/DNP', int_l5_starts=3,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Veteran squad cover; 4th-choice CB',
        tier_revised='4',
    ),
    # ── Midfielders ────────────────────────────────────────────────────────
    dict(
        player='Kobbie Mainoo', position='MID', sub_position='CM',
        club='Manchester United', nationality='England', group='L',
        wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
        group_mins_per_game=71.0, exp_post_group_mins_total=222,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=55,
        fitness_flag='Fit',
        notes='England\'s most exciting young CM (20); strong Euro 2024 and '
              'Man Utd season; key rotation alongside Rice/Bellingham',
        int_l5_pattern='90/90/90/90/90', int_l5_starts=5,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Regular England starter; Euro 2024 performer; Tuchel favourite',
        tier_revised='2',
    ),
    dict(
        player='Jordan Henderson', position='MID', sub_position='DM',
        club='Brentford', nationality='England', group='L',
        wc_squad_prob_pct=100, tier='4', playing_role='Depth',
        group_mins_per_game=10.0, exp_post_group_mins_total=20,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=55,
        fitness_flag='Fit',
        notes='Veteran DM (35); resurgent Brentford season earned recall; '
              'squad leadership and experienced DM depth; minimal play time expected',
        int_l5_pattern='90/DNP/90/DNP/90', int_l5_starts=3,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Veteran recall; squad depth DM',
        tier_revised='4',
    ),
    dict(
        player='Morgan Rogers', position='MID', sub_position='AM',
        club='Aston Villa', nationality='England', group='L',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=30.0, exp_post_group_mins_total=50,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=55,
        fitness_flag='Fit',
        notes='Breakout Villa AM season; creative off-the-bench option; '
              'surprising Palmer/Foden over; good pressing and dribbling',
        int_l5_pattern='90/90/DNP/90/90', int_l5_starts=4,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Impact sub AM; selected over Palmer and Foden',
        tier_revised='3',
    ),
    # ── Forwards ───────────────────────────────────────────────────────────
    dict(
        player='Anthony Gordon', position='FWD', sub_position='',
        club='Newcastle United', nationality='England', group='L',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=30.0, exp_post_group_mins_total=55,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=55,
        fitness_flag='Fit',
        notes='Direct left winger; Newcastle regular; pace and pressing assets; '
              'rotation option behind Saka; excellent 2025-26 season',
        int_l5_pattern='90/90/90/90/DNP', int_l5_starts=4,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Regular impact sub winger; consistent England option',
        tier_revised='3',
    ),
    dict(
        player='Noni Madueke', position='FWD', sub_position='',
        club='Arsenal', nationality='England', group='L',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=25.0, exp_post_group_mins_total=40,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=55,
        fitness_flag='Fit',
        notes='Arsenal winger after summer move from Chelsea; strong 2025-26; '
              'direct and technical; can play right wing or as No.10',
        int_l5_pattern='90/90/DNP/90/90', int_l5_starts=4,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Impact sub winger; Arsenal form earned call-up',
        tier_revised='3',
    ),
    dict(
        player='Ivan Toney', position='FWD', sub_position='',
        club='Al-Ahli', nationality='England', group='L',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=30.0, exp_post_group_mins_total=55,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=55,
        fitness_flag='Fit',
        notes='Powerful target CF; recalled from Saudi Arabia; '
              'physical alternative to Kane; useful off the bench for set-pieces',
        int_l5_pattern='90/90/90/90/90', int_l5_starts=5,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Impact sub CF; recall justified by squad need for physical striker',
        tier_revised='3',
    ),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    updated = 0
    for row in rows:
        name = row['player']
        if row['nationality'] == 'England':
            if name in NOT_SELECTED:
                row['wc_squad_prob_pct'] = '0'
                updated += 1
                print(f'  Set 0%:   {name}')
            elif name in CONFIRMED_IN:
                row['wc_squad_prob_pct'] = '100'
                updated += 1
                print(f'  Set 100%: {name}')

    # Build template row from an existing England player for defaults
    template = next(r for r in rows if r['nationality'] == 'England')
    blank_pts = {'action_pts_per_90': '0', 'exp_pts_per_90': '0',
                 'total_exp_fantasy_pts': '0', 'adj_exp_fantasy_pts': '0'}

    for p in NEW_PLAYERS:
        new_row = {k: '' for k in fieldnames}
        new_row.update(blank_pts)
        new_row.update({str(k): str(v) for k, v in p.items()})
        rows.append(new_row)
        print(f'  Added:    {p["player"]}')

    with open(PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f'\nDone — {updated} rows updated, {len(NEW_PLAYERS)} rows added.')
    print(f'Total rows: {len(rows)}')


if __name__ == '__main__':
    main()
