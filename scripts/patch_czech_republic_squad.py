#!/usr/bin/env python3
"""
patch_czech_republic_squad.py — official 26-man squad, Miroslav Koubek, May 31 2026.
Group A: Mexico(7.1), South Korea(5.9), Czech Republic(4.3), South Africa(2.9).
Advance 18%, dead rubber G3 10%.
Domestic-heavy squad (17 Czech league players, 9 abroad). Captain Ladislav Krejčí (Wolves CB).
Patrik Schick leads attack. Tomáš Souček anchors midfield. Matěj Kovář (PSV) is No.1 GK.
Jiří Pavlenka and Lukáš Horníček (Braga) — note Pavlenka NOT in final 26; Horníček is backup.
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 18, 10
T1G, T1K = 85.0, 3
T2G, T2K = 68.0, 2
T3G, T3K = 35.0, 2
T4G, T4K = 10.0, 1

NEW_PLAYERS = [
    # --- Goalkeepers ---
    dict(player='Matěj Kovář', position='GK', sub_position='', club='PSV Eindhoven', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='PSV No.1; Czech Republic undisputed starter; excellent shot-stopper; 26 years old; strong season in Eredivisie',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed No.1 GK; PSV Eredivisie starter', tier_revised='GK1'),
    dict(player='Lukáš Horníček', position='GK', sub_position='', club='SC Braga', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=1,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Braga GK (Primeira Liga); Czech No.2; young (24); no WC starts expected',
         int_l5_pattern='90/DNP/90/DNP/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Braga squad player', tier_revised='GK2'),
    dict(player='Jindřich Staněk', position='GK', sub_position='', club='SK Slavia Prague', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Slavia Prague No.1; Czech No.3 at WC despite being domestic No.1; Kovář preferred',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; domestic league only', tier_revised='GK3'),
    # --- Defenders ---
    dict(player='Ladislav Krejčí', position='DEF', sub_position='CB', club='Wolverhampton Wanderers', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Captain; Wolves CB; 27yo; commanding in air; leader of Czech defence; Premier League quality',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain; first-choice CB; PL Wolves', tier_revised='1'),
    dict(player='Vladimír Coufal', position='DEF', sub_position='RB', club='TSG Hoffenheim', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hoffenheim RB; 34yo veteran; first-choice Czech right-back; 61 caps; overlapping threat',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; experienced; Bundesliga', tier_revised='1'),
    dict(player='Robin Hranáč', position='DEF', sub_position='CB', club='TSG Hoffenheim', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hoffenheim CB (25); strong partner to Krejčí; powerful aerial defender',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB partner; Bundesliga quality', tier_revised='1'),
    dict(player='David Jurásek', position='DEF', sub_position='LB', club='SK Slavia Prague', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Slavia Prague LB; 26yo; Czech first-choice left-back; attack-minded; strong domestic season',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; consistent Slavia starter', tier_revised='1'),
    dict(player='Tomáš Holeš', position='DEF', sub_position='CB', club='SK Slavia Prague', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Slavia Prague CB/DM (32); versatile; covers CB and defensive mid; experienced Czech international',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB/DM utility; Slavia Prague', tier_revised='2'),
    dict(player='David Zima', position='DEF', sub_position='CB', club='SK Slavia Prague', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Slavia Prague CB (25); good in build-up; regular Czech defensive rotation',
         int_l5_pattern='90/sub/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB rotation; Slavia domestic league', tier_revised='2'),
    dict(player='David Douděra', position='DEF', sub_position='RB', club='SK Slavia Prague', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Slavia Prague RB/WB; backup to Coufal; versatile wide defender; domestic cover',
         int_l5_pattern='90/sub/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup RB; Slavia squad player', tier_revised='3'),
    dict(player='Štěpán Chaloupek', position='DEF', sub_position='CB', club='SK Slavia Prague', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Slavia Prague CB (23); young defensive depth; squad cover only',
         int_l5_pattern='sub/DNP/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young CB depth; domestic league', tier_revised='3'),
    dict(player='Jaroslav Zelený', position='DEF', sub_position='LB', club='AC Sparta Prague', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Sparta Prague LB (34); veteran domestic left-back; depth cover only',
         int_l5_pattern='sub/DNP/sub/DNP/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran depth LB; domestic league', tier_revised='4'),
    # --- Midfielders ---
    dict(player='Tomáš Souček', position='MID', sub_position='DM', club='West Ham United', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='West Ham DM (31); 89 caps, 19 goals; imposing aerial threat from CM/DM; cornerstone of Czech midfield',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='89-cap Czech veteran; PL regular; automatic starter', tier_revised='1'),
    dict(player='Lukáš Provod', position='MID', sub_position='CM', club='SK Slavia Prague', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Slavia Prague CM; creative box-to-box; key Czech playmaker; strong at Euros 2024; reliable starter',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key Czech CM; Slavia Prague engine room', tier_revised='1'),
    dict(player='Pavel Šulc', position='MID', sub_position='AM', club='Olympique Lyonnais', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Lyon AM/WNG (25); technically gifted; regular Czech attacking mid option; Ligue 1 quality',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular AM; Lyon Ligue 1', tier_revised='2'),
    dict(player='Michal Sadílek', position='MID', sub_position='CM', club='SK Slavia Prague', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Slavia Prague CM (26); reliable ball-winner; good transition play; regular midfield rotation',
         int_l5_pattern='90/sub/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM rotation; Slavia Prague', tier_revised='2'),
    dict(player='Lukáš Červ', position='MID', sub_position='CM', club='Viktoria Plzeň', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Plzeň CM; energetic midfield option; squad depth cover',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Squad CM; Plzeň domestic', tier_revised='3'),
    dict(player='Alexandr Sojka', position='MID', sub_position='WNG', club='Viktoria Plzeň', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Plzeň winger (23); pacy wide option; squad rotation; young domestic talent',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young WNG squad depth; Plzeň', tier_revised='3'),
    dict(player='Hugo Sochůrek', position='MID', sub_position='CM', club='AC Sparta Prague', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Sparta Prague CM (18); remarkable inclusion — youngest player at WC 2026; creative; long-term prospect',
         int_l5_pattern='sub/DNP/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Exceptional young talent; WC debut at 18', tier_revised='3'),
    dict(player='Denis Višinský', position='MID', sub_position='WNG', club='Viktoria Plzeň', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Plzeň winger (23); fringe wide option; minimal WC minutes expected',
         int_l5_pattern='DNP/sub/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe WNG; Plzeň domestic', tier_revised='4'),
    dict(player='Vladimír Darida', position='MID', sub_position='CM', club='FC Hradec Králové', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hradec Králové CM (36); veteran Czech international; 100+ caps; farewell WC selection; minimal expected minutes',
         int_l5_pattern='sub/DNP/sub/DNP/sub', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran depth; 100-cap farewell selection', tier_revised='4'),
    # --- Forwards ---
    dict(player='Patrik Schick', position='FWD', sub_position='CF', club='Bayer Leverkusen', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Bayer Leverkusen CF; Czech star striker; 25 goals in 52 caps; clinical finisher; Euro 2020 hero; T1 automatic',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Star striker; 25 international goals; Leverkusen UCL', tier_revised='1'),
    dict(player='Adam Hložek', position='FWD', sub_position='WNG', club='TSG Hoffenheim', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hoffenheim WNG/FWD (23); explosive wide forward; injury recovery complete; creative threat from right',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular wide FWD; Bundesliga; injury recovery confirmed', tier_revised='2'),
    dict(player='Jan Kuchta', position='FWD', sub_position='CF', club='AC Sparta Prague', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Sparta Prague CF (29); physical target striker; rotation option behind Schick; strong domestic scorer',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Second-choice CF; Sparta Prague Europa League', tier_revised='2'),
    dict(player='Tomáš Chorý', position='FWD', sub_position='CF', club='SK Slavia Prague', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Slavia Prague CF (31); tall powerful target man; aerial threat; squad striker depth',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CF; Slavia domestic league', tier_revised='3'),
    dict(player='Mojmír Chytil', position='FWD', sub_position='CF', club='SK Slavia Prague', nationality='Czech Republic', group='A',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Slavia Prague CF (27); fringe forward option; minimal WC minutes expected',
         int_l5_pattern='sub/DNP/sub/DNP/sub', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CF; domestic squad depth', tier_revised='4'),
]

def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Czech Republic': continue
        name = row['player']
        if name in NOT_SELECTED:
            row['wc_squad_prob_pct'] = '0'; updated += 1
        elif name in CONFIRMED_IN:
            row['wc_squad_prob_pct'] = '100'; updated += 1
            print(f'  Set 100%: {name}')
        if name in CORRECTIONS:
            for k, v in CORRECTIONS[name].items(): row[k] = str(v)
    blank_pts = {'action_pts_per_90': '0', 'exp_pts_per_90': '0', 'total_exp_fantasy_pts': '0', 'adj_exp_fantasy_pts': '0'}
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
