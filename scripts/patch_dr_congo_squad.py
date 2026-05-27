#!/usr/bin/env python3
"""
patch_dr_congo_squad.py  —  confirmed 26-man squad, May 2026.
No existing players in CSV — all 26 are new.
Group K: Portugal(8.6), Colombia(7.3), Uzbekistan(3.9), DR Congo(3.3).
Advance 22%, dead rubber G3 15%.
"""
import csv
PATH = '/tmp/world_cup_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 22, 15
T1G, T1K = 87.1, 6
T2G, T2K = 74.0, 5
T3G, T3K = 42.0, 3
T4G, T4K = 16.0, 1

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Joël Epolo', position='GK', sub_position='', club='Royal Antwerp', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=6,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Royal Antwerp GK; DR Congo No.1; young talented keeper; Belgian Pro League quality',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Starting GK; Antwerp Belgian Pro League', tier_revised='GK1'),
    dict(player='Parfait Fayulu', position='GK', sub_position='', club='Beerschot', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=2,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Beerschot GK; DR Congo No.2; experienced veteran keeper; no WC starts expected',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Belgian Pro League', tier_revised='GK2'),
    dict(player='Lionel Mpasi', position='GK', sub_position='', club='Anderlecht', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Anderlecht GK; DR Congo No.3; domestic/Belgian-based; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Belgian Pro League', tier_revised='GK3'),
    # Defenders
    dict(player='Chancel Mbemba', position='DEF', sub_position='CB', club='Marseille', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Marseille CB; DR Congo captain; experienced defender; commanding presence; former Porto',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain CB; Marseille Ligue 1', tier_revised='1'),
    dict(player='Aaron Wan-Bissaka', position='DEF', sub_position='RB', club='West Ham United', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='West Ham RB; elite one-on-one defender; DR Congo key player; PL quality; excellent tackling',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key RB; West Ham PL quality; elite 1v1 defender', tier_revised='1'),
    dict(player='Axel Tuanzebe', position='DEF', sub_position='CB', club='Stade de Reims', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Stade de Reims CB; former Man Utd; composure on the ball; DR Congo CB partner',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB; Ligue 1', tier_revised='2'),
    dict(player='Jordan Bushiri', position='DEF', sub_position='CB', club='Nice', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Nice CB; aerial dominance and physicality; regular DR Congo defensive option; Ligue 1 quality',
         int_l5_pattern='90/sub/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB; Nice Ligue 1', tier_revised='2'),
    dict(player='Arthur Masuaku', position='DEF', sub_position='LB', club='Besiktas', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Besiktas LB; former West Ham; attack-minded; DR Congo first-choice left-back',
         int_l5_pattern='90/90/90/sub/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular LB; Super Lig', tier_revised='2'),
    dict(player='Jonas Kayembe', position='DEF', sub_position='RB', club='Anderlecht', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Anderlecht RB; DR Congo depth option; domestic Belgian quality; rotation cover',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation RB; Belgian Pro League', tier_revised='3'),
    dict(player='Joël Kapuadi', position='DEF', sub_position='CB', club='RC Lens', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Lens CB; solid Ligue 1 performer; DR Congo depth at centre-back',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CB; Ligue 1', tier_revised='3'),
    dict(player='Harold Batubinsika', position='DEF', sub_position='CB', club='Strasbourg', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Strasbourg CB; young DR Congo international; Ligue 1 experience; depth option',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young depth CB; Ligue 1', tier_revised='3'),
    dict(player='Guillaume Kalulu', position='DEF', sub_position='CB', club='Marseille', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Marseille CB; DR Congo-eligible defender; Ligue 1 quality; squad depth',
         int_l5_pattern='DNP/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CB; Ligue 1', tier_revised='3'),
    # Midfielders
    dict(player='Yvan Moutoussamy', position='MID', sub_position='CM', club='Nottingham Forest', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Nottm Forest CM; energetic and combative; DR Congo midfield regular; PL quality',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM; Nottm Forest PL', tier_revised='2'),
    dict(player='Gaël Kakuta', position='MID', sub_position='AM', club='RC Lens', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Lens AM; DR Congo creative hub; dribbling and vision; former Chelsea; Ligue 1 consistency',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Creative AM; Lens Ligue 1 quality', tier_revised='2'),
    dict(player='Loïs Sadiki', position='MID', sub_position='DM', club='Anderlecht', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Anderlecht DM; defensive midfield anchor; DR Congo rotation option; Belgian Pro League quality',
         int_l5_pattern='90/sub/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation DM; Belgian Pro League', tier_revised='3'),
    dict(player='Ange-Yoan Mukau', position='MID', sub_position='CM', club='FC Metz', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FC Metz CM; young DR Congo international; Ligue 2 experience; squad depth',
         int_l5_pattern='sub/90/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young CM; French second tier', tier_revised='3'),
    dict(player='Eddy Kayembe', position='MID', sub_position='CM', club='Watford', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Watford CM; Championship experience; DR Congo squad depth in midfield',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CM; Championship', tier_revised='3'),
    dict(player='Nathanaël Mbuku', position='MID', sub_position='LW', club='RC Lens', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Lens winger; DR Congo-eligible wide player; direct and pacy; Ligue 1 experience',
         int_l5_pattern='sub/90/DNP/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation winger; Lens Ligue 1', tier_revised='3'),
    dict(player='Théo Bongonda', position='MID', sub_position='LW', club='Girona', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Girona winger; DR Congo wide option; La Liga experience; fringe selection',
         int_l5_pattern='sub/DNP/sub/DNP/sub', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe winger; La Liga', tier_revised='4'),
    dict(player='Théo Cipenga', position='MID', sub_position='CM', club='Anderlecht', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Anderlecht CM; young DR Congo international; squad depth; minimal WC minutes',
         int_l5_pattern='DNP/sub/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe young CM; Belgian Pro League', tier_revised='4'),
    dict(player='Florent Pickel', position='MID', sub_position='DM', club='Strasbourg', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Strasbourg DM; Ligue 1 experience; DR Congo fringe selection; depth cover',
         int_l5_pattern='DNP/sub/sub/DNP/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe DM; Ligue 1', tier_revised='4'),
    # Forwards
    dict(player='Yoane Wissa', position='FWD', sub_position='', club='Brentford', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Brentford winger/striker; DR Congo standout player; clinical and pacy; PL quality; key threat',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='DR Congo best player; Brentford PL', tier_revised='1'),
    dict(player='Cédric Bakambu', position='FWD', sub_position='', club='Panathinaikos', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Panathinaikos striker; experienced DR Congo forward; former Villarreal/Beijing; key striker option',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Experienced striker; Greek Super League', tier_revised='2'),
    dict(player='Simon Banza', position='FWD', sub_position='', club='SC Braga', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Braga striker; clinical and powerful; Primeira Liga goals record; DR Congo key forward',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Clinical striker; Braga Primeira Liga', tier_revised='2'),
    dict(player='Alfred Elia', position='FWD', sub_position='', club='Standard Liège', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Standard Liège forward; DR Congo domestic/Belgian depth option; fringe selection',
         int_l5_pattern='sub/DNP/sub/DNP/sub', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe forward; Belgian Pro League', tier_revised='4'),
    dict(player='Fiston Mayele', position='FWD', sub_position='', club='Panathinaikos', nationality='DR Congo', group='K',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Panathinaikos striker; DR Congo forward depth; Greek Super League; fringe selection',
         int_l5_pattern='sub/DNP/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe striker; Greek Super League', tier_revised='4'),
]

def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'DR Congo': continue
        name = row['player']
        if name in NOT_SELECTED:
            row['wc_squad_prob_pct'] = '0'; updated += 1
        elif name in CONFIRMED_IN:
            row['wc_squad_prob_pct'] = '100'; updated += 1
            print(f'  Set 100%: {name}')
        if name in CORRECTIONS:
            for k, v in CORRECTIONS[name].items(): row[k] = str(v)
    blank_pts = {'action_pts_per_90':'0','exp_pts_per_90':'0','total_exp_fantasy_pts':'0','adj_exp_fantasy_pts':'0'}
    for p in NEW_PLAYERS:
        r = {k: '' for k in fieldnames}; r.update(blank_pts)
        r.update({str(k): str(v) for k, v in p.items()})
        rows.append(r); print(f'  Added:    {p["player"]}')
    with open(PATH, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader(); w.writerows(rows)
    print(f'\nDone — {updated} updated, {len(NEW_PLAYERS)} added. Total: {len(rows)}')

if __name__ == '__main__':
    main()
