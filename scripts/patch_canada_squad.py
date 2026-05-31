#!/usr/bin/env python3
"""
patch_canada_squad.py — official 26-man squad (Marsch, announced May 29 2026).
Group B: Switzerland(6.5), Qatar(3.7), Bosnia(2.2), Canada(5.7). Co-host.
Advance 63%, dead rubber G3 10%.
Key fitness: Davies (hamstring, NOT for opener; exp. back G2+),
             Bombito (broken leg Oct 2025; fit), Promise David (hip surgery; tight).
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 63, 10
T1G, T1K = 87.5, 93
T2G, T2K = 74.0, 76
T3G, T3K = 42.0, 54
T4G, T4K = 16.0, 16

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Maxime Crépeau', position='GK', sub_position='', club='Orlando City SC', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=93,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Orlando City GK; Canada No.1 with slight edge over St. Clair; experienced WC GK; reliable and commanding',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; Orlando City MLS', tier_revised='GK1'),
    dict(player='Dayne St. Clair', position='GK', sub_position='', club='Inter Miami CF', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=10.0, exp_post_group_mins_total=10,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Inter Miami GK; strong competition with Crépeau for starting role; capable of stepping in',
         int_l5_pattern='90/DNP/90/DNP/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Inter Miami MLS', tier_revised='GK2'),
    dict(player='Owen Goodman', position='GK', sub_position='', club='Barnsley', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Barnsley GK (Crystal Palace loan); Canada No.3; developmental pick; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Barnsley Championship', tier_revised='GK3'),
    # Defenders
    dict(player='Alphonso Davies', position='DEF', sub_position='LB', club='Bayern Munich', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='Bayern Munich LB; Canada captain and best player; hamstring strain (May, UCL semi); '
               'confirmed in squad; NOT for opener vs Bosnia; targeting return G2 vs Qatar',
         int_l5_pattern='90/90/DNP/sub/90', int_l5_starts=3, int_absence_reason='Hamstring strain May 2026 (UCL semi)',
         fitness_current='Hamstring; confirmed in squad; NOT opener; targeting G2+ return', tier_revised='1'),
    dict(player='Alistair Johnston', position='DEF', sub_position='RB', club='Celtic', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Celtic RB; Canada first-choice right-back; missed most of season with hamstring but now fit; solid and reliable',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit; returned from hamstring; match-sharp', tier_evidence='First-choice RB; Celtic Scottish Prem', tier_revised='1'),
    dict(player='Moïse Bombito', position='DEF', sub_position='CB', club='OGC Nice', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='OGC Nice CB; Canada best centre-back by distance; broken leg Oct 2025; recovered and expected fit; Ligue 1 quality',
         int_l5_pattern='90/90/90/DNP/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit; returned from broken leg Oct 2025; expected to start', tier_evidence='First-choice CB; OGC Nice Ligue 1', tier_revised='1'),
    dict(player='Derek Cornelius', position='DEF', sub_position='CB', club='Rangers', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Rangers CB; experienced Canada international; covers for Bombito; no club football since November 2025 — match-sharpness concern',
         int_l5_pattern='sub/DNP/90/DNP/sub', int_l5_starts=1, int_absence_reason='No club football since Nov 2025',
         fitness_current='Fit but match-sharpness uncertain; no club football since Nov 2025', tier_evidence='Rotation CB; Rangers Scottish Prem', tier_revised='2'),
    dict(player='Richie Laryea', position='DEF', sub_position='LB', club='Toronto FC', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Toronto FC LB/RB; will start opener at LB covering for Davies; versatile full-back; Canada regular',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Starter with Davies out; Toronto FC MLS', tier_revised='2'),
    dict(player='Luc de Fougerolles', position='DEF', sub_position='CB', club='FCV Dender', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FCV Dender CB; 20 yrs; improving young option; Belgian First Division B; rotation CB cover',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young rotation CB; FCV Dender Belgian Pro League', tier_revised='2'),
    dict(player='Niko Sigur', position='DEF', sub_position='RB', club='Hajduk Split', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hajduk Split RB/CM; versatile; covers right-back and midfield; HNL experience; squad depth',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Versatile depth; Hajduk Split HNL', tier_revised='3'),
    dict(player='Joel Waterman', position='DEF', sub_position='CB', club='Chicago Fire', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Chicago Fire CB; veteran depth CB; MLS experience; squad rotation cover',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CB; Chicago Fire MLS', tier_revised='3'),
    # Midfielders
    dict(player='Stephen Eustáquio', position='MID', sub_position='CM', club='LAFC', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='LAFC CM; Canada heartbeat and captain for opener; Porto-owned; returned from hematoma injury; commanding presence',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit; returned from hematoma injury', tier_evidence='Undisputed starter; LAFC MLS', tier_revised='1'),
    dict(player='Ismaël Koné', position='MID', sub_position='CM', club='US Sassuolo', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Sassuolo CM; breakout Serie A season; key midfield partner for Eustáquio; dynamic box-to-box quality',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key starter; Sassuolo Serie A', tier_revised='1'),
    dict(player='Ali Ahmed', position='MID', sub_position='AM', club='Norwich City', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Norwich City AM/LW; 4 goals/3 assists in Championship season; strong form; left-channel creative option',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular AM/LW; Norwich City Championship', tier_revised='2'),
    dict(player='Jonathan Osorio', position='MID', sub_position='CM', club='Toronto FC', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Toronto FC CM; veteran culture leader; experienced Canadian international; reliable depth option',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran rotation CM; Toronto FC MLS', tier_revised='2'),
    dict(player='Mathieu Choinière', position='MID', sub_position='AM', club='LAFC', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='LAFC AM/LW; rotation winger option; squad depth in wide creative areas',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation AM/LW; LAFC MLS', tier_revised='3'),
    dict(player='Nathan Saliba', position='MID', sub_position='CM', club='RSC Anderlecht', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Anderlecht CM; young depth option; Belgian Pro League experience; limited WC minutes expected',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young depth CM; RSC Anderlecht Belgian Pro League', tier_revised='3'),
    dict(player='Marcelo Flores', position='MID', sub_position='AM', club='Tigres UANL', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Tigres UANL AM; creative playmaker; major talent despite limited competitive intl appearances; squad rotation',
         int_l5_pattern='sub/90/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Creative rotation AM; Tigres UANL Liga MX', tier_revised='3'),
    # Forwards
    dict(player='Jonathan David', position='FWD', sub_position='', club='Juventus', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Juventus ST; Canada best player; prolific goalscorer; joined Juventus summer 2025; should play every minute available',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed No.1 striker; Juventus Serie A', tier_revised='1'),
    dict(player='Tajon Buchanan', position='FWD', sub_position='', club='Villarreal', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Villarreal RW; rock-solid starter; 7 goals / 1 assist in 32 La Liga matches; pace and directness key weapon',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice winger; Villarreal La Liga', tier_revised='1'),
    dict(player='Cyle Larin', position='FWD', sub_position='', club='Southampton', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Southampton ST; 9 goals in 21 Championship matches; David main backup; physical target-man presence',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Main backup striker; Southampton Championship', tier_revised='2'),
    dict(player='Liam Millar', position='FWD', sub_position='', club='Hull City', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hull City LW; promotion playoff finalist; adds left-side width and versatility; Canada regular',
         int_l5_pattern='90/sub/90/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular LW; Hull City Championship', tier_revised='2'),
    dict(player='Tani Oluwaseyi', position='FWD', sub_position='', club='Villarreal', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Villarreal ST/RW; Larin understudy; pace and pressing; young and developing; La Liga experience',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation forward; Villarreal La Liga', tier_revised='2'),
    dict(player='Promise David', position='FWD', sub_position='', club='Union Saint-Gilloise', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='Union Saint-Gilloise LW/ST; hip surgery; recovering ahead of schedule but fitness timeline tight for group stage',
         int_l5_pattern='sub/DNP/sub/DNP/90', int_l5_starts=1, int_absence_reason='Hip surgery recovery',
         fitness_current='Hip surgery; recovering ahead of schedule; tight fitness timeline for group stage', tier_revised='3'),
    dict(player='Daniel Jebbison', position='FWD', sub_position='', club='Preston North End', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Preston North End ST; physical depth striker; Championship experience; squad rotation option',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth ST; Preston Championship', tier_revised='3'),
    dict(player='Jacen Russell-Rowe', position='FWD', sub_position='', club='Toulouse FC', nationality='Canada', group='B',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Toulouse FC ST; fringe selection; Ligue 1 experience; limited WC minutes expected',
         int_l5_pattern='sub/DNP/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe striker; Toulouse Ligue 1', tier_revised='4'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Canada': continue
        name = row['player']
        if name in NOT_SELECTED:
            row['wc_squad_prob_pct'] = '0'; updated += 1
        elif name in CONFIRMED_IN:
            row['wc_squad_prob_pct'] = '100'; updated += 1
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
