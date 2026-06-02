#!/usr/bin/env python3
"""
patch_saudi_arabia_squad.py — official 26-man squad (Georgios Donis, announced June 1 2026).
Group H: Spain(9.7), Uruguay(7.0), Saudi Arabia(3.0), Cape Verde(2.5).
Advance 8%, dead rubber G3 10%.
25 of 26 players from Saudi Pro League; Saud Abdulhamid (RC Lens) sole overseas player.
Salem Al-Dawsari captain (108 caps, 34yo); Mohammed Al-Owais undisputed GK1.
Al-Hilal provide 7, Al-Nassr 6, Al-Qadisiyah 4.
Group opener vs Uruguay (June 15 Miami), then Spain (June 21 Atlanta), Cape Verde (June 26 Houston).
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 8, 10
T1G, T1K = 82.0, 0
T2G, T2K = 65.0, 0
T3G, T3K = 30.0, 0
T4G, T4K = 8.0,  0

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Mohammed Al-Owais', position='GK', sub_position='', club='Al-Hilal', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Hilal GK; Saudi Arabia undisputed No.1 and most-capped GK; experienced AFC Champions League keeper; '
               'key figure in historic 2022 WC win over Argentina; leads GK department for Group H campaign',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; Al-Hilal Saudi Pro League', tier_revised='GK1'),
    dict(player='Nawaf Al-Aqidi', position='GK', sub_position='', club='Al-Nassr', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Nassr GK; Saudi Arabia No.2 keeper; backup behind Al-Owais; no starts expected in group stage',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Al-Nassr Saudi Pro League', tier_revised='GK2'),
    dict(player='Ahmed Al-Kassar', position='GK', sub_position='', club='Al-Qadisiyah', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Qadisiyah GK; Saudi Arabia third-choice keeper; domestic league depth option; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Al-Qadisiyah Saudi Pro League', tier_revised='GK3'),
    # Defenders
    dict(player='Saud Abdulhamid', position='DEF', sub_position='RB', club='RC Lens', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='RC Lens RB; sole overseas player in squad; highest-profile Saudi export playing in Ligue 1; '
               'athletic and combative right-back; key figure in Saudi defence; previously linked with Serie A move',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; RC Lens Ligue 1', tier_revised='1'),
    dict(player='Hassan Tambakti', position='DEF', sub_position='CB', club='Al-Hilal', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Hilal CB; Saudi Arabia first-choice centre-back; physical and commanding defender; '
               'key in Saudi defensive structure for group stage',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Al-Hilal Saudi Pro League', tier_revised='1'),
    dict(player='Ali Al-Bulayhi', position='DEF', sub_position='LB', club='Al-Hilal', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Hilal LB; Saudi Arabia first-choice left-back; experienced and reliable; key defensive starter; '
               'veteran of 2022 WC squad; part of Al-Hilal dominant domestic campaign',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; Al-Hilal Saudi Pro League', tier_revised='1'),
    dict(player='Ali Lajami', position='DEF', sub_position='CB', club='Al-Hilal', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Hilal CB; Saudi Arabia rotation centre-back alongside Tambakti; experienced Saudi Pro League defender; '
               'part of compact Saudi defensive unit',
         int_l5_pattern='90/90/sub/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Al-Hilal Saudi Pro League', tier_revised='1'),
    dict(player='Hassan Kadesh', position='DEF', sub_position='CB', club='Al-Ittihad', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Ittihad CB; Saudi Arabia defensive rotation; physical defender; good domestic form; squad option',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Al-Ittihad Saudi Pro League', tier_revised='2'),
    dict(player='Abdulelah Al-Amri', position='DEF', sub_position='RB', club='Al-Nassr', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Nassr RB/DEF; Saudi Arabia defensive squad depth; backup fullback option; Al-Nassr Saudi Pro League',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation DEF; Al-Nassr Saudi Pro League', tier_revised='2'),
    dict(player='Nawaf Boushal', position='DEF', sub_position='LB', club='Al-Nassr', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Nassr LB/DEF; Saudi Arabia left-back rotation; direct and energetic; squad depth alongside Al-Bulayhi',
         int_l5_pattern='sub/sub/90/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation LB; Al-Nassr Saudi Pro League', tier_revised='2'),
    dict(player='Mohammed Abu Al-Shamat', position='DEF', sub_position='CB', club='Al-Qadisiyah', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Qadisiyah CB; Saudi Arabia defensive depth; domestic league backup; limited WC minutes expected',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB depth; Al-Qadisiyah Saudi Pro League', tier_revised='3'),
    dict(player='Jehad Thikri', position='DEF', sub_position='CB', club='Al-Qadisiyah', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Qadisiyah CB; Saudi Arabia defensive fringe option; domestic squad depth; no major WC minutes expected',
         int_l5_pattern='sub/sub/DNP/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB depth; Al-Qadisiyah Saudi Pro League', tier_revised='3'),
    dict(player='Ali Majrashi', position='DEF', sub_position='FB', club='Al-Ahli', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Ahli FB; Saudi Arabia fullback depth option; fringe squad selection; limited minutes expected',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='FB depth; Al-Ahli Saudi Pro League', tier_revised='3'),
    # Midfielders
    dict(player='Salem Al-Dawsari', position='MID', sub_position='WNG', club='Al-Hilal', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Hilal WNG; Saudi Arabia captain (108 caps, age 34); most experienced player in squad; all-time leading scorer; '
               'scored famous winner vs Argentina in 2022 WC; the definitive Saudi star — key to everything going forward; '
               'direct, pacy, creative left winger',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain and star; undisputed T1; Al-Hilal Saudi Pro League', tier_revised='1'),
    dict(player='Abdulelah Al-Malki', position='MID', sub_position='DM', club='Al-Hilal', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Hilal DM; Saudi Arabia midfield anchor; Nasser Al-Dawsari is his cousin; '
               'combative and disciplined defensive midfielder; key to Saudi press and shape',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice DM; Al-Hilal Saudi Pro League', tier_revised='1'),
    dict(player='Mohammed Kanno', position='MID', sub_position='CM', club='Al-Hilal', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Hilal CM; Saudi Arabia key midfielder; experienced AFC Champions League performer; '
               'technical and hard-working box-to-box midfielder; part of Al-Hilal core',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CM; Al-Hilal Saudi Pro League', tier_revised='1'),
    dict(player='Nasser Al-Dawsari', position='MID', sub_position='WNG', club='Al-Hilal', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Hilal WNG; Saudi Arabia attacking rotation; shares surname with captain Salem but unrelated to the star; '
               'rotation winger providing attacking width',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation WNG; Al-Hilal Saudi Pro League', tier_revised='2'),
    dict(player='Abdullah Al-Khaibari', position='MID', sub_position='CM', club='Al-Nassr', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Nassr CM; Saudi Arabia midfield rotation; experienced domestic midfielder; squad option in central areas',
         int_l5_pattern='90/sub/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Al-Nassr Saudi Pro League', tier_revised='2'),
    dict(player='Ziyad Al-Johani', position='MID', sub_position='CM', club='Al-Ahli', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Ahli CM; Saudi Arabia midfield depth; creative and energetic; rotation option for Group H fixtures',
         int_l5_pattern='sub/sub/90/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Al-Ahli Saudi Pro League', tier_revised='2'),
    dict(player='Musab Al-Juwayr', position='MID', sub_position='WNG', club='Al-Qadisiyah', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Qadisiyah WNG; Saudi Arabia wide midfield depth; domestic league performer; fringe squad selection',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='WNG depth; Al-Qadisiyah Saudi Pro League', tier_revised='3'),
    dict(player='Khalid Al-Ghannam', position='MID', sub_position='CM', club='Al-Ettifaq', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Ettifaq CM; Saudi Arabia midfield fringe option; domestic league squad depth; limited WC minutes expected',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; Al-Ettifaq Saudi Pro League', tier_revised='3'),
    dict(player='Alaa Al-Hajji', position='MID', sub_position='AM', club='Neom', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Neom AM; Saudi Arabia attacking midfield depth; Neom SC Saudi Pro League; squad depth option',
         int_l5_pattern='sub/sub/DNP/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='AM depth; Neom Saudi Pro League', tier_revised='3'),
    dict(player='Ayman Yahya', position='MID', sub_position='CM', club='Al-Nassr', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Nassr CM; Saudi Arabia squad depth midfielder; domestic league utility man; fringe WC selection',
         int_l5_pattern='DNP/sub/DNP/sub/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; Al-Nassr Saudi Pro League', tier_revised='3'),
    # Forwards
    dict(player='Saleh Al-Shehri', position='FWD', sub_position='CF', club='Al-Ittihad', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Ittihad CF; Saudi Arabia first-choice striker; prolific goalscorer in Saudi Pro League; '
               'target man with good movement; led Saudi line in qualifying; physically strong CF',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CF; Al-Ittihad Saudi Pro League', tier_revised='1'),
    dict(player='Firas Al-Buraikan', position='FWD', sub_position='CF', club='Al-Ahli', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Ahli CF; Saudi Arabia forward rotation; quick and direct; capable of playing wide or central; '
               'strong scorer in Saudi Pro League; rotation option behind Al-Shehri',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CF/FWD; Al-Ahli Saudi Pro League', tier_revised='2'),
    dict(player='Abdullah Al-Hamdan', position='FWD', sub_position='CF', club='Al-Nassr', nationality='Saudi Arabia', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Nassr CF; Saudi Arabia featured prominently in squad announcement; strong domestic form; '
               'clinical finisher in Saudi Pro League; solid rotation option for Group H',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CF; Al-Nassr Saudi Pro League', tier_revised='2'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Saudi Arabia': continue
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
