#!/usr/bin/env python3
"""
patch_qatar_squad.py — official 26-man squad, Julen Lopetegui, June 1 2026.
Group B: Switzerland(6.5), Canada(5.7), Qatar(3.7), Bosnia(2.2).
Advance 18%, dead rubber G3 10%.
Akram Afif (WNG) is star player; Hassan Al-Haydos (188 caps) is captain.
Almoez Ali is all-time leading scorer. Lopetegui-coached squad — more organised defensively.
Two players cut from friendly squad: Shehab Al Laithi (GK) and Rayyan Al Ali (MID).
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
    dict(player='Meshaal Barsham', position='GK', sub_position='', club='Al-Sadd SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Sadd; Qatar undisputed No.1; experienced WC keeper (was No.1 at Qatar 2022); solid shot-stopper',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; Qatar 2022 starter', tier_revised='GK1'),
    dict(player='Mahmoud Abunada', position='GK', sub_position='', club='Al-Rayyan SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=1,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Rayyan; Qatar No.2; 26yo; no WC starts expected',
         int_l5_pattern='90/DNP/90/DNP/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; domestic league', tier_revised='GK2'),
    dict(player='Salah Zakaria', position='GK', sub_position='', club='Al-Duhail SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Duhail; Qatar No.3; no WC minutes expected',
         int_l5_pattern='DNP/90/DNP/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; domestic only', tier_revised='GK3'),
    # --- Defenders ---
    dict(player='Boualem Khoukhi', position='DEF', sub_position='CB', club='Al-Sadd SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Sadd CB (35); veteran Qatar CB; experienced 2022 WC player; defensive rock; leader at the back',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; 2022 WC veteran; Qatar defensive anchor', tier_revised='1'),
    dict(player='Pedro Miguel', position='DEF', sub_position='LB', club='Al-Sadd SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Sadd LB (35); Brazilian-born naturalised Qatari; first-choice left-back; overlapping; 2022 WC starter',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; 2022 WC regular', tier_revised='1'),
    dict(player='Sultan Al Brake', position='DEF', sub_position='RB', club='Al-Duhail SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Duhail RB; first-choice Qatari right-back; combative and energetic',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; regular starter', tier_revised='1'),
    dict(player='Lucas Mendes', position='DEF', sub_position='CB', club='Al-Wakrah SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Wakrah CB (35); Brazilian-born; experienced rotation CB; 2022 WC squad member',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB rotation; domestic league', tier_revised='2'),
    dict(player='Al-Hashmi Al-Hussain', position='DEF', sub_position='CB', club='Al-Arabi SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Arabi CB (22); young Qatari CB; emerging talent; rotation option in Lopetegui system',
         int_l5_pattern='90/90/sub/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young CB rotation; domestic league', tier_revised='2'),
    dict(player='Homam Ahmed', position='DEF', sub_position='RB', club='Cultural Leonesa', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Cultural Leonesa RB (Spain); only Europe-based defender; versatile; squad cover right side',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Squad RB; Spanish football experience', tier_revised='3'),
    dict(player='Ayoub Al-Alawi', position='DEF', sub_position='CB', club='Al-Gharafa SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Gharafa CB (21); young Qatari defender; squad depth',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young CB depth; domestic league', tier_revised='3'),
    dict(player='Issa Laye', position='DEF', sub_position='CB', club='Al-Arabi SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Arabi CB (28); defensive depth; fringe selection; minimal WC minutes expected',
         int_l5_pattern='DNP/sub/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CB; domestic squad depth', tier_revised='4'),
    # --- Midfielders ---
    dict(player='Assim Madibo', position='MID', sub_position='DM', club='Al-Wakrah SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Wakrah DM (29); Senegalese-born naturalised; key Qatar holding midfielder; combative; Qatar midfield anchor',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key DM; Qatar midfield anchor', tier_revised='1'),
    dict(player='Karim Boudiaf', position='MID', sub_position='CM', club='Al-Duhail SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Duhail CM (35); French-born naturalised Qatari; experienced; 2022 WC veteran; box-to-box',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Experienced CM; 2022 WC veteran', tier_revised='1'),
    dict(player='Abdulaziz Hatem', position='MID', sub_position='AM', club='Al-Rayyan SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Rayyan AM (35); veteran attacking mid; creative; regular Qatar rotation; 2022 WC squad',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran AM rotation; 2022 WC squad', tier_revised='2'),
    dict(player='Ahmed Fathi', position='MID', sub_position='CM', club='Al-Arabi SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Arabi CM; domestic midfield squad depth; rotation cover',
         int_l5_pattern='sub/90/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Squad CM; domestic league', tier_revised='3'),
    dict(player='Jassim Gaber', position='MID', sub_position='CM', club='Al-Rayyan SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Rayyan CM (24); young domestic midfielder; squad cover',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young CM squad depth; domestic league', tier_revised='3'),
    dict(player='Mohammed Mannai', position='MID', sub_position='CM', club='Al-Shamal SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Shamal CM; fringe midfield selection; minimal WC minutes expected',
         int_l5_pattern='DNP/sub/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CM; domestic league depth', tier_revised='4'),
    # --- Forwards ---
    dict(player='Akram Afif', position='FWD', sub_position='WNG', club='Al-Sadd SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Sadd WNG (29); two-time Asian Player of the Year; Qatar star; direct, dribbling threat; key threat wide',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Qatar star; double Asian POTY; automatic starter', tier_revised='1'),
    dict(player='Almoez Ali', position='FWD', sub_position='CF', club='Al-Duhail SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Duhail CF (29); Qatar all-time leading scorer; top scorer Asian qualifying (12 goals); explosive finisher',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Qatar all-time top scorer; 12 WCQ goals', tier_revised='1'),
    dict(player='Hassan Al-Haydos', position='FWD', sub_position='AM', club='Al-Sadd SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Sadd AM; captain; 188 caps (most in Qatar history); 35yo veteran; 2022 Asian Cup winner; key creative presence',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain; 188 caps; Qatar all-time record holder', tier_revised='1'),
    dict(player='Edmílson Junior', position='FWD', sub_position='WNG', club='Al-Duhail SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Duhail WNG (31); Brazilian-born Qatari; direct wide player; 2022 WC squad; regular rotation option',
         int_l5_pattern='90/90/sub/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular WNG rotation; 2022 WC squad', tier_revised='2'),
    dict(player='Mohammed Muntari', position='FWD', sub_position='CF', club='Al-Gharafa SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Gharafa CF (32); Ghana-born naturalised; scored Qatar 2022 sole WC goal; physical target striker',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Qatar 2022 WC goalscorer; rotation CF', tier_revised='2'),
    dict(player='Tahsin Mohammed', position='FWD', sub_position='WNG', club='Al-Duhail SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Duhail WNG (19); exciting young talent; pace and directness; future Qatar star; regular rotation inclusion',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young WNG; emerging Qatar talent', tier_revised='2'),
    dict(player='Ahmed Al-Ganehi', position='FWD', sub_position='CF', club='Al-Gharafa SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Gharafa CF (25); domestic striker; squad depth option',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Squad striker depth; domestic league', tier_revised='3'),
    dict(player='Ahmed Alaaeldin', position='FWD', sub_position='WNG', club='Al-Rayyan SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Rayyan WNG/FWD (33); veteran domestic forward; squad cover',
         int_l5_pattern='sub/DNP/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran squad FWD; domestic league', tier_revised='3'),
    dict(player='Yusuf Abdurisag', position='FWD', sub_position='WNG', club='Al-Wakrah SC', nationality='Qatar', group='B',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Wakrah WNG (27); fringe wide forward; domestic league; minimal WC minutes expected',
         int_l5_pattern='DNP/sub/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe WNG; domestic squad depth', tier_revised='4'),
]

def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Qatar': continue
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
