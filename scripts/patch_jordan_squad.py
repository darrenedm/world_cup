#!/usr/bin/env python3
"""
patch_jordan_squad.py — official 26-man squad (Jamal Sellami, announced June 2 2026).
Group J: Argentina(10.0), Austria(5.9), Algeria(4.9), Jordan(2.5).
Advance 5%, dead rubber G3 10%.
HISTORIC DEBUT — Jordan's first-ever World Cup appearance.
Captain: Ihsan Haddad (Al-Hussein, 32yo). Star: Musa Al-Taamari (Rennes, 'Jordanian Messi').
Ali Olwan — 3rd highest Asian qualifier scorer (9 goals).
Yazan Al-Naimat injured and did not make final squad.
Predominantly domestic league players with a handful of overseas-based.
Group: Austria (June 17 Santa Clara), Algeria (June 22 Santa Clara), Argentina (June 27 Arlington).
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 5, 10
T1G, T1K = 78.0, 0
T2G, T2K = 60.0, 0
T3G, T3K = 25.0, 0
T4G, T4K = 5.0,  0

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Yazeed Abulaila', position='GK', sub_position='', club='Al-Hussein', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Hussein GK; Jordan undisputed No.1; experienced domestic keeper; leads historic WC debut; '
               'most-capped GK in Jordanian football; key figure for Jordan in Group J',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; Al-Hussein Jordanian Premier League', tier_revised='GK1'),
    dict(player='Abdallah Al-Fakhouri', position='GK', sub_position='', club='Al-Wehdat', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Wehdat GK; Jordan No.2 keeper; backup behind Abulaila; no starts expected; Al-Wehdat domestic league',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Al-Wehdat Jordanian Premier League', tier_revised='GK2'),
    dict(player='Ahmad Al-Juiadi', position='GK', sub_position='', club='Shabab Al-Ordon', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Shabab Al-Ordon GK; Jordan third-choice keeper; domestic depth option; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Shabab Al-Ordon Jordanian Premier League', tier_revised='GK3'),
    # Defenders
    dict(player='Ihsan Haddad', position='DEF', sub_position='CB', club='Al-Hussein', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Hussein CB; Jordan captain (32yo); most experienced player and leader of historic WC debut squad; '
               'commanding centre-back who organises the defence; pivotal to Jordan\'s defensive solidity',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain and leader; undisputed T1 CB; Al-Hussein', tier_revised='1'),
    dict(player='Yazan Al-Arab', position='DEF', sub_position='RB', club='FC Seoul', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FC Seoul RB (South Korea K-League); Jordan first-choice right-back; highest-profile overseas defender; '
               'athletic and disciplined; key part of Jordan\'s defensive structure',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; FC Seoul K-League 1 South Korea', tier_revised='1'),
    dict(player='Saleem Obaid', position='DEF', sub_position='CB', club='Al-Hussein', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Hussein CB; Jordan regular centre-back partner for Haddad; experienced domestic defender; '
               'part of Jordan\'s solid qualifying defensive record',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB; Al-Hussein Jordanian Premier League', tier_revised='1'),
    dict(player='Saed Al-Rosan', position='DEF', sub_position='LB', club='Al-Hussein', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Hussein LB; Jordan first-choice left-back; reliable domestic defender; key in Jordan\'s left flank',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; Al-Hussein Jordanian Premier League', tier_revised='1'),
    dict(player='Mohammad Abu Hashish', position='DEF', sub_position='CB', club='Al-Karma', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Karma CB; Jordan defensive rotation option; experienced domestic defender; squad depth alongside Haddad/Obaid',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Al-Karma Jordanian Premier League', tier_revised='2'),
    dict(player='Husam Abu Dahab', position='DEF', sub_position='CB', club='Al-Samiya', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Samiya CB; Jordan defensive squad depth; rotation central defender; domestic league experience',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Al-Samiya Jordanian Premier League', tier_revised='2'),
    dict(player='Abdallah Nasib', position='DEF', sub_position='LB', club='Al-Zawraa', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Zawraa LB (Iraq); Jordan fullback rotation; Iraqi league experience adds quality; '
               'rotation option on the left flank',
         int_l5_pattern='sub/sub/90/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation LB; Al-Zawraa Iraqi Premier League', tier_revised='2'),
    dict(player='Mohammad Abualnadi', position='DEF', sub_position='RB', club='Selangor', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Selangor RB (Malaysia); Jordan fullback depth; Malaysian Super League experience; limited WC minutes expected',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='RB depth; Selangor Malaysian Super League', tier_revised='3'),
    dict(player='Mohannad Abu Taha', position='DEF', sub_position='CB', club='Al-Quwa Al-Jawiya', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Quwa Al-Jawiya CB (Iraq); Jordan defensive fringe; Iraqi league; limited WC minutes expected',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB depth; Al-Quwa Al-Jawiya Iraqi Premier League', tier_revised='3'),
    dict(player='Anas Badawi', position='DEF', sub_position='CB', club='Al-Faisaly', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Faisaly CB; Jordan defensive depth; domestic Jordan league; fringe squad selection for WC debut',
         int_l5_pattern='sub/sub/DNP/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB depth; Al-Faisaly Jordanian Premier League', tier_revised='3'),
    # Midfielders
    dict(player='Musa Al-Taamari', position='MID', sub_position='WNG', club='Rennes', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Rennes WNG (Ligue 1); Jordan star player nicknamed "Jordanian Messi"; direct dribbler with flair; '
               'highest-profile Jordanian player; previously at Montpellier; key creative threat; '
               'featured in preliminary squad announcement; Jordan\'s primary attacking weapon',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Jordan star; undisputed T1; Rennes Ligue 1', tier_revised='1'),
    dict(player='Rajaei Ayed', position='MID', sub_position='CM', club='Al-Hussein', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Hussein CM; Jordan key central midfielder; experienced domestic organiser; part of midfield spine; '
               'key contributor in qualifying campaign; reliable box-to-box option',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CM; Al-Hussein Jordanian Premier League', tier_revised='1'),
    dict(player='Mohammad Al-Dawoud', position='MID', sub_position='DM', club='Al-Wehdat', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Wehdat DM; Jordan defensive midfielder; screens the defence and wins the ball; '
               'workmanlike and disciplined; key to Jordan\'s press and shape in Group J',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice DM; Al-Wehdat Jordanian Premier League', tier_revised='1'),
    dict(player='Nizar Al-Rashdan', position='MID', sub_position='CM', club='Qatar SC', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Qatar SC CM; Jordan overseas-based midfielder; Qatar Stars League experience; '
               'quality rotation option in the centre of midfield',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Qatar SC Qatar Stars League', tier_revised='2'),
    dict(player='Noor Al-Rawabdeh', position='MID', sub_position='CM', club='Selangor', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Selangor CM (Malaysia); Jordan midfield rotation; Malaysian Super League; squad depth in central areas',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Selangor Malaysian Super League', tier_revised='2'),
    dict(player='Amer Jamous', position='MID', sub_position='CM', club='Al-Zawraa', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Zawraa CM (Iraq); Jordan midfield depth; Iraqi league experience; squad player for WC debut',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; Al-Zawraa Iraqi Premier League', tier_revised='3'),
    dict(player='Ibrahim Sadeh', position='MID', sub_position='CM', club='Al-Karma', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Karma CM; Jordan midfield fringe option; domestic league; limited WC minutes expected',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; Al-Karma Jordanian Premier League', tier_revised='3'),
    # Forwards
    dict(player='Ali Olwan', position='FWD', sub_position='CF', club='Al-Sailiya', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Sailiya CF (Qatar); Jordan leading scorer in Asian qualifying (9 goals — 3rd highest in AFC qualifying); '
               '26yo prolific finisher; Jordan\'s most dangerous striker; key to any goal-scoring ambitions in Group J',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Jordan leading scorer; undisputed T1 CF; Al-Sailiya Qatar Stars', tier_revised='1'),
    dict(player='Mahmoud Al-Mardi', position='FWD', sub_position='CF', club='Al-Hussein', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Hussein CF; Jordan striker rotation option; physical and direct target man; '
               'domestic league goals scorer; rotation option behind Olwan',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CF; Al-Hussein Jordanian Premier League', tier_revised='2'),
    dict(player='Odeh Al-Fakhouri', position='FWD', sub_position='WNG', club='Pyramids', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Pyramids WNG (Egypt); Jordan wide attacker with Egyptian league experience; direct and creative from wide; '
               'rotation option to support Al-Taamari on opposite flank',
         int_l5_pattern='90/sub/sub/90/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation WNG; Pyramids Egyptian Premier League', tier_revised='2'),
    dict(player='Ibrahim Sabra', position='FWD', sub_position='WNG', club='Lokomotiva Zagreb', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Lokomotiva Zagreb WNG (Croatia); Jordan forward overseas-based; Croatian league experience; '
               'squad depth attacker; limited WC minutes expected',
         int_l5_pattern='sub/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='WNG depth; Lokomotiva Zagreb Croatian Prva HNL', tier_revised='3'),
    dict(player='Mohammad Abu Zraiq', position='FWD', sub_position='CF', club='Al-Hussein', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Hussein CF; Jordan forward depth; domestic league striker; fringe selection for historic WC debut',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CF depth; Al-Hussein Jordanian Premier League', tier_revised='3'),
    dict(player='Ali Azaizeh', position='FWD', sub_position='WNG', club='Al-Shabab', nationality='Jordan', group='J',
         wc_squad_prob_pct=100, tier='4', playing_role='Fringe Player',
         group_mins_per_game=T4G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Shabab WNG; Jordan fringe attacker; squad depth selection; domestic league; minimal WC minutes anticipated',
         int_l5_pattern='DNP/DNP/sub/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe WNG; Al-Shabab Saudi Pro League', tier_revised='4'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Jordan': continue
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
