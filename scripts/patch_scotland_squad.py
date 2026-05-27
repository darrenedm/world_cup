#!/usr/bin/env python3
"""
patch_scotland_squad.py  —  confirmed 26-man squad, May 2026, Steve Clarke.
McTominay (T1) already in CSV — confirm to 100%.
Group C: Morocco(8.3), Brazil(7.9), Scotland(5.0), Haiti(1.2).
Advance 40%, dead rubber G3 10%.
"""
import csv
PATH = '/tmp/world_cup_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = {'Scott McTominay'}
CORRECTIONS  = {}

ADV, DR = 40, 10
T1G, T1K = 87.1, 25
T2G, T2K = 74.0, 20
T3G, T3K = 42.0, 15
T4G, T4K = 16.0, 5

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Craig Gordon', position='GK', sub_position='', club='Hearts', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=25,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hearts GK; Scotland undisputed No.1; vastly experienced; crucial in qualifying',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; Hearts Scottish Prem', tier_revised='GK1'),
    dict(player='Angus Gunn', position='GK', sub_position='', club='Norwich City', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=3,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Norwich GK; Scotland No.2; Championship level; no WC starts expected',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Championship', tier_revised='GK2'),
    dict(player='Liam Kelly', position='GK', sub_position='', club='Coventry City', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Coventry GK; Scotland No.3; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Championship', tier_revised='GK3'),
    # Defenders
    dict(player='Andrew Robertson', position='DEF', sub_position='LB', club='Liverpool', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Liverpool LB; Scotland captain; elite delivery and pressing; world-class at position',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='World-class LB; Liverpool PL', tier_revised='1'),
    dict(player='Nathan Patterson', position='DEF', sub_position='RB', club='Everton', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Everton RB; first-choice right-back; strong attacking and defensive output',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; Everton PL', tier_revised='1'),
    dict(player='Scott McKenna', position='DEF', sub_position='CB', club='Nottingham Forest', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Nottm Forest CB; first-choice Scotland centre-back; commanding and ball-playing',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Nottm Forest PL', tier_revised='1'),
    dict(player='Jack Hendry', position='DEF', sub_position='CB', club='Club Brugge', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Club Brugge CB; regular Scotland partner; physical and experienced; UCL level',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB; Brugge Champions League', tier_revised='2'),
    dict(player='Aaron Hickey', position='DEF', sub_position='RB', club='Brentford', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Brentford RB/LB; quality PL player; versatile and energetic; rotation option',
         int_l5_pattern='90/sub/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Versatile PL full-back; Brentford', tier_revised='2'),
    dict(player='Kieran Tierney', position='DEF', sub_position='LB', club='Real Sociedad', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Real Sociedad LB; experienced Scotland international; injury history but quality player',
         int_l5_pattern='90/sub/90/DNP/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Experienced LB; La Liga form', tier_revised='2'),
    dict(player='Grant Hanley', position='DEF', sub_position='CB', club='Norwich City', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Norwich CB; veteran Scotland cap holder; depth option; past prime but reliable',
         int_l5_pattern='90/sub/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran CB; Championship', tier_revised='3'),
    dict(player='John Souttar', position='DEF', sub_position='CB', club='Rangers', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Rangers CB; Scotland depth option; solid domestically; injury-prone historically',
         int_l5_pattern='sub/90/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Rangers SPFL', tier_revised='3'),
    dict(player='Anthony Ralston', position='DEF', sub_position='RB', club='Celtic', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Celtic RB; domestic depth option; reliable in SPFL; limited international ceiling',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Domestic depth RB; Celtic', tier_revised='3'),
    dict(player='Doug Hyam', position='DEF', sub_position='CB', club='Coventry City', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Coventry CB; fringe selection; Championship level; unlikely to feature',
         int_l5_pattern='DNP/sub/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CB; Championship', tier_revised='4'),
    # Midfielders
    dict(player='John McGinn', position='MID', sub_position='CM', club='Aston Villa', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Aston Villa CM; Scotland vice-captain; box-to-box dynamism; huge qualifying role',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key CM; Villa PL; Scotland vice-captain', tier_revised='1'),
    dict(player='Billy Gilmour', position='MID', sub_position='CM', club='Napoli', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Napoli CM; technical and composed; excellent pressing; Scotland regular in midfield',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM; Napoli Serie A quality', tier_revised='2'),
    dict(player='Ryan Christie', position='MID', sub_position='AM', club='Bournemouth', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Bournemouth AM/winger; creative and direct; solid WC qualifier contributor',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular AM; Bournemouth PL', tier_revised='2'),
    dict(player='Kenny McLean', position='MID', sub_position='CM', club='Hearts', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hearts CM; experienced Scotland international; domestic-level quality; depth option',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Experienced CM rotation; SPFL', tier_revised='3'),
    dict(player='Lewis Ferguson', position='MID', sub_position='CM', club='Bologna', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Bologna CM; emerging Scotland international; good Serie A form; rotation option',
         int_l5_pattern='90/sub/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Emerging CM; Bologna Serie A', tier_revised='3'),
    dict(player='Stuart Curtis', position='MID', sub_position='CM', club='Kilmarnock', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Kilmarnock CM; domestic selection; squad depth; unlikely WC minutes',
         int_l5_pattern='sub/DNP/sub/DNP/sub', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Domestic fringe CM; SPFL', tier_revised='4'),
    dict(player='Ben Doak', position='MID', sub_position='AM', club='Middlesbrough', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Middlesbrough AM (Liverpool loan); exciting young winger; future star; impact option only',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young impact winger; Championship loan', tier_revised='4'),
    # Forwards
    dict(player='Che Adams', position='FWD', sub_position='', club='Celtic', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Celtic striker; Scotland first-choice forward; prolific in qualifying; clinical and mobile',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice ST; Celtic SPFL quality', tier_revised='1'),
    dict(player='Lawrence Shankland', position='FWD', sub_position='', club='Hearts', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hearts striker; prolific SPFL scorer; key backup striker; rotation starter option',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Prolific SPFL striker; Hearts', tier_revised='2'),
    dict(player='Lyndon Dykes', position='FWD', sub_position='', club='Millwall', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Millwall striker; physical aerial target; Scotland qualifier contributor; rotation option',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Physical striker rotation; Championship', tier_revised='2'),
    dict(player='George Hirst', position='FWD', sub_position='', club='Ipswich Town', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Ipswich Town striker; squad depth option; PL/Championship experience',
         int_l5_pattern='sub/90/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth striker; PL level', tier_revised='3'),
    dict(player='Ross Stewart', position='FWD', sub_position='', club='Southampton', nationality='Scotland', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Southampton striker; physical and direct; injury history limits ceiling; squad cover',
         int_l5_pattern='sub/DNP/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth physical striker; PL/Champ', tier_revised='3'),
]

def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Scotland': continue
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
