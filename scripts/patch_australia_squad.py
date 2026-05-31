#!/usr/bin/env python3
"""
patch_australia_squad.py — projected 26-man squad (Popovic, final due June 1 2026).
Group D: USA(7.1), Turkey(5.8), Australia(5.6), Paraguay(4.6).
Advance 40%, dead rubber G3 10%.
Key fitness: Riley McGree — OUT (hamstring, Middlesbrough); Alex Robertson — released from camp.
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 40, 10
T1G, T1K = 83.0, 25
T2G, T2K = 68.0, 21
T3G, T3K = 36.0, 15
T4G, T4K = 10.0, 4

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Mathew Ryan', position='GK', sub_position='', club='Levante', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=25,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Levante GK; Australia captain; experienced international; commanding shot-stopper; Socceroos No.1',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1 and captain; Levante La Liga 2', tier_revised='GK1'),
    dict(player='Patrick Beach', position='GK', sub_position='', club='Melbourne City', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=5,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Melbourne City GK; Australia No.2; domestic experience; no WC starts expected',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Melbourne City A-League', tier_revised='GK2'),
    dict(player='Paul Izzo', position='GK', sub_position='', club='Randers FC', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Randers FC GK; Australia No.3; Danish Superliga experience; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Randers FC Danish Superliga', tier_revised='GK3'),
    # Defenders
    dict(player='Harry Souttar', position='DEF', sub_position='CB', club='Leicester City', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Leicester City CB; Australia defensive leader; powerful and commanding; injury-prone history but fit now; key to backline',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Leicester City Championship', tier_revised='1'),
    dict(player='Cameron Burgess', position='DEF', sub_position='CB', club='Swansea City', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Swansea City CB; regular Australia starting CB partner; Championship quality; reliable and consistent',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB; Swansea City Championship', tier_revised='1'),
    dict(player='Aziz Behich', position='DEF', sub_position='LB', club='Melbourne City', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Melbourne City LB; Australia first-choice left-back; experienced international; attacking and reliable',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; Melbourne City A-League', tier_revised='1'),
    dict(player='Jason Geria', position='DEF', sub_position='RB', club='Albirex Niigata', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Albirex Niigata RB; Australia regular right-back starter; solid defensive presence; J-League experience',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular RB; Albirex Niigata J-League', tier_revised='1'),
    dict(player='Alessandro Circati', position='DEF', sub_position='CB', club='Parma', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Parma CB; young and improving Australia defender; Serie A experience; rotation CB cover',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Parma Serie A', tier_revised='2'),
    dict(player='Jordan Bos', position='DEF', sub_position='LB', club='Feyenoord', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Feyenoord LB; young Australia left-back option; Eredivisie quality; covers for Behich',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation LB; Feyenoord Eredivisie', tier_revised='2'),
    dict(player='Milos Degenek', position='DEF', sub_position='CB', club='APOEL', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='APOEL CB; veteran Australia international; experienced squad depth; reliable cover',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran depth CB; APOEL Cypriot First Division', tier_revised='3'),
    dict(player='Kye Rowles', position='DEF', sub_position='CB', club='DC United', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='DC United CB/RB; versatile squad defender; MLS experience; can cover multiple defensive positions',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Versatile depth defender; DC United MLS', tier_revised='3'),
    dict(player='Lucas Herrington', position='DEF', sub_position='CB', club='Unattached', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='18 yrs; young Australia CB call-up; developmental squad inclusion; no WC minutes expected',
         int_l5_pattern='sub/DNP/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young depth CB; developmental call-up', tier_revised='4'),
    dict(player='Kai Trewin', position='DEF', sub_position='CB', club='New York City FC', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='NYCFC CB; depth cover; MLS experience; limited WC minutes expected',
         int_l5_pattern='sub/DNP/sub/DNP/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe depth CB; NYCFC MLS', tier_revised='4'),
    # Midfielders
    dict(player='Jackson Irvine', position='MID', sub_position='CM', club='St Pauli', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='St Pauli CM; Australia vice-captain; engine of the team; box-to-box quality; Bundesliga experience',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Vice-captain; St Pauli Bundesliga', tier_revised='1'),
    dict(player='Ajdin Hrustic', position='MID', sub_position='CM', club='Heracles Almelo', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Heracles Almelo CM; key creator; 6 assists in Eredivisie season; technical quality and vision; Australia starter',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key creator; Heracles Almelo Eredivisie', tier_revised='1'),
    dict(player='Aiden O\'Neill', position='MID', sub_position='DM', club='New York City FC', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='NYCFC CM/DM; regular Australia starter; industrious defensive midfielder; anchors midfield',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular DM/CM; NYCFC MLS', tier_revised='1'),
    dict(player='Connor Metcalfe', position='MID', sub_position='CM', club='St Pauli', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='St Pauli CM; squad regular; Bundesliga experience alongside club teammate Irvine; rotation option',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; St Pauli Bundesliga', tier_revised='2'),
    dict(player='Cameron Devlin', position='MID', sub_position='CM', club='Hearts', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hearts CM; squad rotation option; Scottish Premiership experience; depth midfield cover',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CM; Hearts Scottish Prem', tier_revised='3'),
    # Forwards
    dict(player='Martin Boyle', position='FWD', sub_position='', club='Hibernian', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hibernian RW/LW; key wide attacker; direct and pacy; Socceroos regular; Scottish Prem form',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice winger; Hibernian Scottish Prem', tier_revised='1'),
    dict(player='Mohamed Toure', position='FWD', sub_position='', club='Norwich City', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Norwich City ST; Australia main striker option; Championship quality; physical and effective in front of goal',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice striker; Norwich City Championship', tier_revised='1'),
    dict(player='Nestory Irankunda', position='FWD', sub_position='', club='Watford', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Watford winger (loan from Bayern Munich); exciting 20yo; started season at Bayern; direct and pacy; major talent',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Exciting rotation winger; Watford / Bayern Munich', tier_revised='2'),
    dict(player='Mathew Leckie', position='FWD', sub_position='', club='Melbourne City', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Melbourne City RW; veteran winger (35); experienced Socceroos attacker; rotation wide option alongside Boyle',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit; 35 yrs, managed carefully', tier_evidence='Veteran winger; Melbourne City A-League', tier_revised='2'),
    dict(player='Kusini Yengi', position='FWD', sub_position='', club='Machida Zelvia', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Machida Zelvia ST (J-League loan); backup striker option; physical and direct; Australia squad depth',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation striker; Machida Zelvia J-League', tier_revised='2'),
    dict(player='Jacob Italiano', position='FWD', sub_position='', club='Grazer AK', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Grazer AK ST/RW; Austrian Bundesliga experience; squad depth option; limited WC minutes expected',
         int_l5_pattern='sub/90/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth forward; Grazer AK Austrian Bundesliga', tier_revised='3'),
    dict(player='Brandon Borrello', position='FWD', sub_position='', club='Western Sydney Wanderers', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Western Sydney Wanderers LW; experienced A-League winger; squad depth and rotation cover',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth LW; Western Sydney Wanderers A-League', tier_revised='3'),
    dict(player='Nishan Velupillay', position='FWD', sub_position='', club='Melbourne Victory', nationality='Australia', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Melbourne Victory LW/RW; squad rotation winger; A-League experience; limited WC minutes expected',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe winger; Melbourne Victory A-League', tier_revised='3'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Australia': continue
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
