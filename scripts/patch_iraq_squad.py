#!/usr/bin/env python3
"""
patch_iraq_squad.py — official 26-man squad, Graham Arnold, June 1 2026.
Group I: France(10.0), Senegal(7.1), Norway(5.3), Iraq(3.2).
Advance 7%, dead rubber G3 10%.
Iraq's first World Cup in 40 years. Captain Jalal Hassan (GK, 100+ caps, Al-Zawraa).
Aymen Hussein leads attack (33 international goals). Zidane Iqbal (Utrecht, ex-Man Utd) key creative mid.
Ali Al-Hamadi (Ipswich Town) is highest-profile European-based forward.
Ali Adnan NOT selected — confirmed retired from international football before announcement.
IMPORTANT: T1K=0 — ALL tiers get exp_post_group_mins_total=0 (Iraq ADV=7%, very unlikely to advance).
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 7, 10
T1G, T1K = 82.0, 0
T2G, T2K = 65.0, 0
T3G, T3K = 30.0, 0
T4G, T4K = 8.0, 0

NEW_PLAYERS = [
    # --- Goalkeepers ---
    dict(player='Jalal Hassan', position='GK', sub_position='', club='Al-Zawraa', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Zawraa; captain; 100+ caps; most experienced Iraq player; veteran No.1; authoritative presence',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain; 100+ caps; Iraq undisputed GK1', tier_revised='GK1'),
    dict(player='Fahad Talib', position='GK', sub_position='', club='Al-Talaba', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Talaba; Iraq No.2; no WC starts expected',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; domestic league', tier_revised='GK2'),
    dict(player='Ahmed Basil', position='GK', sub_position='', club='Al-Shorta', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Shorta; Iraq No.3; no WC minutes expected',
         int_l5_pattern='DNP/90/DNP/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; domestic only', tier_revised='GK3'),
    # --- Defenders ---
    dict(player='Hussein Ali', position='DEF', sub_position='CB', club='Pogoń Szczecin', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Pogoń Szczecin CB (Poland); Iraq first-choice centre-back; highest-profile European-based defender; solid',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Polish Ekstraklasa', tier_revised='1'),
    dict(player='Merchas Doski', position='DEF', sub_position='CB', club='Viktoria Plzeň', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Viktoria Plzeň CB (Czech Republic); Kurdistan-born Iraqi; first-choice CB partner; European league quality',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Czech top-flight', tier_revised='1'),
    dict(player='Rebin Sulaka', position='DEF', sub_position='LB', club='Port FC', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Port FC LB (Thailand); first-choice Iraq left-back; attack-minded; Kurdish-Iraqi',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; Asian league experience', tier_revised='1'),
    dict(player='Akam Hashem', position='DEF', sub_position='RB', club='Al-Zawraa', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Zawraa RB; Iraq first-choice right-back; experienced domestic defender',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; domestic league', tier_revised='1'),
    dict(player='Manaf Younis', position='DEF', sub_position='CB', club='Al-Shorta', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Shorta CB; regular Iraq defensive rotation; experienced domestic defender',
         int_l5_pattern='90/90/sub/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB rotation; domestic league', tier_revised='2'),
    dict(player='Ahmed Yahya', position='DEF', sub_position='CB', club='Al-Shorta', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Shorta CB; regular Iraq defensive option; domestic league quality',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB; domestic league', tier_revised='2'),
    dict(player='Zaid Tahseen', position='DEF', sub_position='CB', club='Pakhtakor', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Pakhtakor CB (Uzbekistan); Iraq squad defensive depth; rotation cover',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Squad CB; Central Asian league', tier_revised='3'),
    dict(player='Frans Putros', position='DEF', sub_position='CB', club='Port FC', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Port FC CB (Thailand); Assyrian-Iraqi; squad depth defender; versatile',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Squad CB depth; Asian league', tier_revised='3'),
    dict(player='Zaid Ismail', position='DEF', sub_position='CB', club='Al-Talaba', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Talaba CB/utility; versatile defender; squad depth; can cover multiple positions',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Squad utility DEF; domestic league', tier_revised='3'),
    dict(player='Mustafa Saadoon', position='DEF', sub_position='CB', club='Al-Shorta', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Shorta CB; fringe defensive selection; domestic league; minimal WC minutes expected',
         int_l5_pattern='DNP/sub/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CB; domestic league depth', tier_revised='4'),
    # --- Midfielders ---
    dict(player='Zidane Iqbal', position='MID', sub_position='CM', club='FC Utrecht', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FC Utrecht CM (Netherlands); ex-Manchester United academy; 22yo; Iraq creative engine; technically gifted',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key creative CM; Eredivisie; ex-Man Utd academy', tier_revised='1'),
    dict(player='Amir Al-Ammari', position='MID', sub_position='DM', club='Cracovia', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Cracovia DM (Poland); Iraq defensive midfield anchor; disciplined; covers defence; Arnold favourite',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key DM; Polish Ekstraklasa; Iraq midfield base', tier_revised='1'),
    dict(player='Kevin Yakob', position='MID', sub_position='CM', club='AGF Aarhus', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='AGF Aarhus CM (Denmark); Assyrian-Iraqi; Superliga quality; box-to-box; regular Iraq rotation',
         int_l5_pattern='90/90/sub/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM; Danish Superliga', tier_revised='2'),
    dict(player='Aimar Sher', position='MID', sub_position='CM', club='Sarpsborg 08', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Sarpsborg 08 CM (Norway); Norway-born Iraqi; Norwegian Eliteserien; technically comfortable; regular rotation',
         int_l5_pattern='90/sub/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM; Norwegian Eliteserien', tier_revised='2'),
    dict(player='Marko Farji', position='MID', sub_position='WNG', club='Strømsgodset', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Strømsgodset WNG (Norway); Assyrian-Iraqi; pacy direct wide midfielder; Norwegian league quality',
         int_l5_pattern='90/90/sub/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular WNG; Norwegian Eliteserien', tier_revised='2'),
    dict(player='Ahmed Qasim', position='MID', sub_position='CM', club='IF Elfsborg', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Elfsborg CM (Sweden); Allsvenskan quality; Iraq squad midfield rotation cover',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Squad CM; Swedish Allsvenskan', tier_revised='3'),
    dict(player='Ibrahim Bayesh', position='MID', sub_position='CM', club='Al-Dhafra FC', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Dhafra CM (UAE); Iraqi squad midfield depth; domestic cover',
         int_l5_pattern='sub/DNP/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Squad CM; UAE league', tier_revised='3'),
    dict(player='Youssef Amyn', position='MID', sub_position='AM', club='Eintracht Braunschweig', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Braunschweig AM (Germany); fringe attacking mid; 2. Bundesliga; minimal WC minutes expected',
         int_l5_pattern='DNP/sub/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe AM; German 2. Bundesliga', tier_revised='4'),
    # --- Forwards ---
    dict(player='Aymen Hussein', position='FWD', sub_position='CF', club='Al-Karma', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Karma CF; Iraq all-time leading scorer (33 international goals); veteran target man; WC talisman',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Iraq all-time top scorer (33 goals); automatic CF', tier_revised='1'),
    dict(player='Ali Al-Hamadi', position='FWD', sub_position='CF', club='Ipswich Town', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Ipswich Town CF; highest-profile Iraq attacker; Premier League quality; pacy, direct; second-choice CF',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Premier League CF; Iraq key attacker; automatic starter', tier_revised='1'),
    dict(player='Ali Jassim', position='FWD', sub_position='WNG', club='Como 1907', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Como 1907 WNG (Italy); ex-Al-Najma; pacy wide forward; Serie A quality; rotation wide threat',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular WNG; Italian Serie A Como', tier_revised='2'),
    dict(player='Mohanad Ali', position='FWD', sub_position='CF', club='Al-Shorta', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Shorta CF; domestic striker; squad depth third forward option',
         int_l5_pattern='sub/90/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Squad CF; domestic league', tier_revised='3'),
    dict(player='Ali Yousef', position='FWD', sub_position='CF', club='Al-Talaba', nationality='Iraq', group='I',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Talaba CF; fringe forward; domestic league; minimal WC minutes expected',
         int_l5_pattern='DNP/sub/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CF; domestic league depth', tier_revised='4'),
]

def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Iraq': continue
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
