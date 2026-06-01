#!/usr/bin/env python3
"""
patch_tunisia_squad.py — official 26-man squad (Lamouchi, announced May 15 2026).
Group F: Netherlands(8.2), Japan(6.8), Tunisia(4.5), Sweden(4.4).
Advance 25%, dead rubber G3 10%.
No fitness concerns in selected squad.
Notable absence: Mohamed Ali Ben Romdhane (top qualifier scorer — tactical omission by Lamouchi).
Tunisia qualified without conceding a single goal in CAF qualifying.
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 25, 10
T1G, T1K = 87.1, 7
T2G, T2K = 74.0, 6
T3G, T3K = 42.0, 4
T4G, T4K = 16.0, 1

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Aymen Dahmen', position='GK', sub_position='', club='CS Sfaxien', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=7,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='CS Sfaxien GK; Tunisia undisputed No.1; solid domestic performer; experienced international',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; CS Sfaxien CAF', tier_revised='GK1'),
    dict(player='Sabri Ben Hassan', position='GK', sub_position='', club='Étoile du Sahel', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=1,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Étoile du Sahel GK; Tunisia No.2; domestic backup; no WC starts expected',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Étoile du Sahel CAF', tier_revised='GK2'),
    dict(player='Abdelmouhib Chamakh', position='GK', sub_position='', club='Club Africain', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Club Africain GK; Tunisia No.3; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Club Africain CAF', tier_revised='GK3'),
    # Defenders
    dict(player='Yan Valéry', position='DEF', sub_position='RB', club='Young Boys', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Young Boys RB; Tunisia first-choice right-back; Swiss Super League quality; attacking and energetic',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; Young Boys Super League', tier_revised='1'),
    dict(player='Dylan Bronn', position='DEF', sub_position='CB', club='Servette FC', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Servette FC CB; Tunisia first-choice centre-back; Swiss Super League quality; commanding and experienced',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Servette FC Super League', tier_revised='1'),
    dict(player='Montassar Talbi', position='DEF', sub_position='CB', club='FC Lorient', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Lorient CB; Tunisia second first-choice CB; Ligue 1 experience; solid in the air and on the ball',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Lorient Ligue 1', tier_revised='1'),
    dict(player='Moutaz Neffati', position='DEF', sub_position='LB', club='IFK Norrköping', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='IFK Norrköping LB; Tunisia regular left-back; Swedish Allsvenskan; reliable and disciplined',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular LB; IFK Norrköping Allsvenskan', tier_revised='2'),
    dict(player='Adem Arous', position='DEF', sub_position='FB', club='Kasımpaşa', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Kasımpaşa FB; Tunisia versatile fullback; Turkish Süper Lig experience; rotation option',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation FB; Kasımpaşa Süper Lig', tier_revised='2'),
    dict(player='Omar Rekik', position='DEF', sub_position='CB', club='NK Maribor', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='NK Maribor CB; Tunisia rotation centre-back; Slovenian league; squad depth behind main pairing',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; NK Maribor Slovenian PrvaLiga', tier_revised='2'),
    dict(player='Raed Chikhaoui', position='DEF', sub_position='CB', club='US Monastir', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='US Monastir CB; Tunisia domestic squad depth; Botola/CAF-level; limited WC minutes expected',
         int_l5_pattern='sub/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB depth; US Monastir Tunisia Ligue 1', tier_revised='3'),
    dict(player='Ali Abdi', position='DEF', sub_position='LB', club='OGC Nice', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='OGC Nice LB; Tunisia depth fullback; Ligue 1 experience; rotation cover for Neffati',
         int_l5_pattern='sub/90/DNP/sub/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='LB depth; OGC Nice Ligue 1', tier_revised='3'),
    dict(player='Mohamed Amine Ben Hamida', position='DEF', sub_position='CB', club='Espérance de Tunis', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Espérance de Tunis CB; Tunisia domestic defensive depth; experienced in CAF competition; squad cover',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB depth; Espérance de Tunis CAF', tier_revised='3'),
    # Midfielders
    dict(player='Ellyes Skhiri', position='MID', sub_position='DM', club='Eintracht Frankfurt', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Frankfurt DM; Tunisia captain and best player; Bundesliga quality; elite ball-winner and press; '
               'Tunisia qualified without conceding a single CAF qualifying goal — Skhiri the engine',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain and best player; Frankfurt Bundesliga', tier_revised='1'),
    dict(player='Hannibal Mejbri', position='MID', sub_position='CM', club='Burnley', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Burnley CM; Tunisia second consecutive WC; combative and energetic Premier League midfielder; '
               'box-to-box quality; key partner alongside Skhiri in double pivot',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key starter; Burnley PL/Championship', tier_revised='1'),
    dict(player='Anis Ben Slimane', position='MID', sub_position='CM', club='Norwich City', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Norwich CM; Tunisia creative midfield option; Championship quality; technical and forward-thinking',
         int_l5_pattern='90/90/sub/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM; Norwich Championship', tier_revised='2'),
    dict(player='Rani Khedira', position='MID', sub_position='DM', club='Union Berlin', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Union Berlin DM; Tunisia midfield depth; Bundesliga quality; brother of Sami Khedira; combative DM',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular DM; Union Berlin Bundesliga', tier_revised='2'),
    dict(player='Ismaël Gharbi', position='MID', sub_position='AM', club='FC Augsburg', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Augsburg AM; Tunisia young creative midfielder; Bundesliga experience; technically gifted; rotation option',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation AM; Augsburg Bundesliga', tier_revised='2'),
    dict(player='Mohamed Hadj-Mahmoud', position='MID', sub_position='CM', club='FC Lugano', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Lugano CM; Tunisia squad depth midfielder; Swiss Super League; limited WC minutes expected',
         int_l5_pattern='sub/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; FC Lugano Super League', tier_revised='3'),
    dict(player='Mortadha Ben Ouanes', position='MID', sub_position='CM', club='Kasımpaşa', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Kasımpaşa CM; Tunisia domestic/Turkish league midfielder; squad depth; fringe selection',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; Kasımpaşa Süper Lig', tier_revised='3'),
    # Forwards
    dict(player='Khalil Ayari', position='FWD', sub_position='WNG', club='Paris Saint-Germain', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='PSG WNG/FWD; Tunisia most exciting young attacker (21 yrs); plays in Ligue 1 champion environment; '
               'creative and direct; set to be Tunisia\'s primary attacking threat at WC 2026',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key young attacker; PSG Ligue 1', tier_revised='1'),
    dict(player='Elias Achouri', position='FWD', sub_position='WNG', club='FC Copenhagen', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FC Copenhagen FWD/WNG; Tunisia reliable wide attacker; Danish Superliga quality; direct and pacey',
         int_l5_pattern='90/90/sub/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular winger; FC Copenhagen Danish Superliga', tier_revised='1'),
    dict(player='Elias Saâd', position='FWD', sub_position='WNG', club='Hannover 96', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hannover 96 WNG; Tunisia wide attacker; Bundesliga 2 quality; pacey and direct from wide areas',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation WNG; Hannover 96 Bundesliga 2', tier_revised='2'),
    dict(player='Sebastian Tounekti', position='FWD', sub_position='WNG', club='Celtic FC', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Celtic FC WNG/FWD; Tunisia exciting wide forward; Scottish Premiership champion club; direct and creative',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation FWD/WNG; Celtic FC Scottish Premiership', tier_revised='2'),
    dict(player='Rayan Elloumi', position='FWD', sub_position='WNG', club='Vancouver Whitecaps', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Vancouver Whitecaps FWD; Tunisia MLS-based attacker; squad rotation option; direct and energetic',
         int_l5_pattern='sub/sub/90/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation FWD; Vancouver Whitecaps MLS', tier_revised='2'),
    dict(player='Hazem Mastouri', position='FWD', sub_position='CF', club='Dynamo Makhachkala', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Dynamo Makhachkala CF; Tunisia striker depth; Russian league; squad depth behind main forwards',
         int_l5_pattern='sub/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CF depth; Dynamo Makhachkala RPL', tier_revised='3'),
    dict(player='Firas Chaouat', position='FWD', sub_position='CF', club='Club Africain', nationality='Tunisia', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Club Africain CF; Tunisia domestic striker; experience in CAF competition; fringe squad selection',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CF depth; Club Africain Tunisia Ligue 1', tier_revised='3'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Tunisia': continue
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
