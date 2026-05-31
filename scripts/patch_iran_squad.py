#!/usr/bin/env python3
"""
patch_iran_squad.py — projected 26-man squad from 30-man preliminary (Ghalenoei, final ~June 1 2026).
Group G: Belgium(7.6), Iran(5.5), Egypt(5.0), New Zealand(1.0).
Advance 48%, dead rubber G3 10%.
Key absences: Sardar Azmoun (disciplinary), Ali Gholizadeh (ACL),
              Rouzbeh Cheshmi (hamstring, injured Antalya camp May 2026).
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 48, 10
T1G, T1K = 85.0, 43
T2G, T2K = 70.0, 35
T3G, T3K = 37.0, 25
T4G, T4K = 12.0, 7

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Alireza Beiranvand', position='GK', sub_position='', club='Tractor SC', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=43,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Tractor SC GK; Iran undisputed No.1; experienced and commanding; strong shot-stopper',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; Tractor SC Iranian Pro League', tier_revised='GK1'),
    dict(player='Hossein Hosseini', position='GK', sub_position='', club='Sepahan', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=5,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Sepahan GK; Iran No.2; domestic league experience; no WC starts expected',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Sepahan Iranian Pro League', tier_revised='GK2'),
    dict(player='Payam Niazmand', position='GK', sub_position='', club='Persepolis', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Persepolis GK; Iran No.3; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Persepolis Iranian Pro League', tier_revised='GK3'),
    # Defenders
    dict(player='Ehsan Hajsafi', position='DEF', sub_position='LB', club='Sepahan', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Sepahan LB; Iran captain; experienced leader and set-piece specialist; 4th World Cup; vital presence',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain and first-choice LB; Sepahan Iranian Pro League', tier_revised='1'),
    dict(player='Ramin Rezaeian', position='DEF', sub_position='RB', club='Foolad', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Foolad RB; Iran regular right-back; experienced international; consistent defensive performer',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; Foolad Iranian Pro League', tier_revised='1'),
    dict(player='Shojae Khalilzadeh', position='DEF', sub_position='CB', club='Tractor SC', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Tractor SC CB; key Iran centre-back; physical and commanding; experienced international',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key CB; Tractor SC Iranian Pro League', tier_revised='1'),
    dict(player='Hossein Kanaanizadegan', position='DEF', sub_position='CB', club='Persepolis', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Persepolis CB; regular Iran defensive partner; strong and well-organized; Persepolis captain',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB; Persepolis Iranian Pro League', tier_revised='1'),
    dict(player='Milad Mohammadi', position='DEF', sub_position='LB', club='Persepolis', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Persepolis LB; rotation left-back; covers for Hajsafi; experienced Iranian league performer',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation LB; Persepolis Iranian Pro League', tier_revised='2'),
    dict(player='Ali Nemati', position='DEF', sub_position='CB', club='Foolad', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Foolad CB; rotation centre-back; squad depth behind main CB pairing; reliable domestic performer',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Foolad Iranian Pro League', tier_revised='2'),
    dict(player='Saleh Hardani', position='DEF', sub_position='CB', club='Esteghlal', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Esteghlal CB; squad depth defender; domestic experience; rotation cover',
         int_l5_pattern='sub/DNP/90/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CB; Esteghlal Iranian Pro League', tier_revised='3'),
    dict(player='Danial Eiri', position='DEF', sub_position='CB', club='Malavan Bandar Anzali', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Malavan CB/RB; versatile defensive depth; domestic experience; squad rotation option',
         int_l5_pattern='sub/90/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CB/RB; Malavan Iranian Pro League', tier_revised='3'),
    dict(player='Omid Noorafkan', position='DEF', sub_position='RB', club='Foolad', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Foolad RB/CB; squad rotation defender; covers right-back and CB; domestic experience',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation RB/CB; Foolad Iranian Pro League', tier_revised='3'),
    # Midfielders
    dict(player='Saeid Ezatolahi', position='MID', sub_position='DM', club='Shabab Al-Ahli', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Shabab Al-Ahli DM; anchors Iran midfield; experienced in UAE Pro League; industrious and disciplined',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Midfield anchor; Shabab Al-Ahli UAE Pro League', tier_revised='1'),
    dict(player='Alireza Jahanbakhsh', position='MID', sub_position='AM', club='FCV Dender', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FCV Dender AM/RW; key Iran European player; experienced Brighton/Feyenoord veteran; creative wide threat',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key European player; FCV Dender Belgian Pro League', tier_revised='1'),
    dict(player='Saman Ghoddos', position='MID', sub_position='AM', club='Kalba FC', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Kalba FC AM; formerly Brentford; creative and technical; regular Iran squad member; quality in tight spaces',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular AM; Kalba FC UAE Pro League', tier_revised='2'),
    dict(player='Mehdi Torabi', position='MID', sub_position='CM', club='Tractor SC', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Tractor SC CM/RW; Iran midfield regular; versatile right-side option; domestic top performer',
         int_l5_pattern='90/90/sub/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM/RW; Tractor SC Iranian Pro League', tier_revised='2'),
    dict(player='Mohammad Ghorbani', position='MID', sub_position='CM', club='Al Wahda', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al Wahda CM; UAE Pro League experience; Iran midfield depth option; regular squad contributor',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Al Wahda UAE Pro League', tier_revised='2'),
    dict(player='Mehdi Ghayedi', position='MID', sub_position='AM', club='Al-Nasr', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Nasr AM; technically gifted attacking midfielder; UAE Pro League; creative option behind Taremi',
         int_l5_pattern='90/sub/90/sub/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation AM; Al-Nasr UAE Pro League', tier_revised='2'),
    dict(player='Mohammad Mohebi', position='MID', sub_position='CM', club='FK Rostov', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FK Rostov CM; Russian Premier League experience; Iran depth midfielder; squad rotation option',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CM; FK Rostov RPL', tier_revised='3'),
    dict(player='Amir Mohammad Razzaghinia', position='MID', sub_position='CM', club='Esteghlal', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Esteghlal CM; domestic depth option; squad rotation cover; limited WC minutes expected',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CM; Esteghlal Iranian Pro League', tier_revised='3'),
    # Forwards
    dict(player='Mehdi Taremi', position='FWD', sub_position='', club='Olympiacos', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Olympiacos ST; Iran star striker (3rd WC); moved from Inter to Olympiacos; prolific goalscorer; unplayable at his best',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed striker; Olympiacos Greek Super League', tier_revised='1'),
    dict(player='Ali Alipour', position='FWD', sub_position='', club='Persepolis', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Persepolis ST; backup striker to Taremi; domestic top scorer; physical and goalscoring threat',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup ST; Persepolis Iranian Pro League', tier_revised='2'),
    dict(player='Amirhossein Hosseinzadeh', position='FWD', sub_position='', club='Tractor SC', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Tractor SC ST/LW; versatile attacker; can play wide left or as second striker; domestic experience',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation attacker; Tractor SC Iranian Pro League', tier_revised='2'),
    dict(player='Amirhossein Mahmoudi', position='FWD', sub_position='', club='Persepolis', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Persepolis ST; depth striker; domestic experience; squad rotation option behind Taremi and Alipour',
         int_l5_pattern='sub/90/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth ST; Persepolis Iranian Pro League', tier_revised='3'),
    dict(player='Dennis Eckert Dargahi', position='FWD', sub_position='', club='Standard Liège', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Standard Liège ST; Iranian-German; called up as Azmoun replacement option; Belgian Pro League; physical depth',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth ST; Standard Liège Belgian Pro League', tier_revised='3'),
    dict(player='Shahriyar Moghanlou', position='FWD', sub_position='', club='Kalba FC', nationality='Iran', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Kalba FC ST; called up to replace injured Rouzbeh Cheshmi; UAE Pro League; fringe depth option',
         int_l5_pattern='sub/DNP/sub/DNP/sub', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Replacement call-up; Kalba FC UAE Pro League', tier_revised='3'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Iran': continue
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
