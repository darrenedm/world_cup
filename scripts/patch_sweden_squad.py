#!/usr/bin/env python3
"""
patch_sweden_squad.py  —  confirmed 26-man squad, May 2026, Jon Dahl Tomasson.
Gyökeres (T1), Isak (T2), Daniel Svensson (T2) already in CSV — confirm to 100%.
Group F: Netherlands(8.2), Japan(6.8), Tunisia(4.5), Sweden(4.4).
Advance 28%, dead rubber G3 10%.
"""
import csv
PATH = '/tmp/world_cup_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = {'Viktor Gyökeres', 'Alexander Isak', 'Daniel Svensson'}
CORRECTIONS  = {
    'Alexander Isak': {'fitness_flag': 'Doubtful', 'fitness_current': 'Fibula Dec 2025; groin May 2026; highly uncertain'},
}

ADV, DR = 28, 10
T1G, T1K = 87.1, 12
T2G, T2K = 74.0, 10
T3G, T3K = 42.0, 7
T4G, T4K = 16.0, 2

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Oscar Johansson', position='GK', sub_position='', club='Djurgårdens IF', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=12,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Sweden GK1; reliable shot-stopper; domestic Allsvenskan quality',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Sweden starting GK; Allsvenskan form', tier_revised='GK1'),
    dict(player='Kristoffer Nordfeldt', position='GK', sub_position='', club='IFK Göteborg', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=2,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='IFK Göteborg GK; Sweden No.2; experienced international; no WC starts expected',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Swedish domestic', tier_revised='GK2'),
    dict(player='Pontus Zetterström', position='GK', sub_position='', club='Anderlecht', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Anderlecht GK; Sweden No.3; promising young keeper; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Belgian Pro League', tier_revised='GK3'),
    # Defenders
    dict(player='Viktor Lindelöf', position='DEF', sub_position='CB', club='Manchester United', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Man Utd CB; Sweden captain; elite ball-playing CB; organises defence; experienced PL performer',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Sweden captain; Man Utd PL first-choice', tier_revised='1'),
    dict(player='Isak Hien', position='DEF', sub_position='CB', club='Atalanta', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atalanta CB; powerful and mobile; regular Sweden partner; UCL experience',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB; Atalanta UCL quality', tier_revised='2'),
    dict(player='Emil Holm', position='DEF', sub_position='RB', club='Juventus', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Juventus RB; attack-minded; Juventus quality; Sweden regular right-back',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular RB; Juventus Serie A', tier_revised='2'),
    dict(player='Emil Gudmundsson', position='DEF', sub_position='RB', club='Lazio', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Lazio RB/winger; versatile and attack-minded; Serie A quality; Sweden rotation option',
         int_l5_pattern='90/sub/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation full-back/winger; Lazio Serie A', tier_revised='2'),
    dict(player='Joel Lagerbielke', position='DEF', sub_position='CB', club='Celtic', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Celtic CB; athletic and dominant aerially; Swedish international regular; UCL experience',
         int_l5_pattern='90/90/90/sub/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB; Celtic Champions League', tier_revised='2'),
    dict(player='Carl Starfelt', position='DEF', sub_position='CB', club='Celta Vigo', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Celta Vigo CB; experienced Sweden international; depth option behind Hien/Lagerbielke',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CB; La Liga', tier_revised='3'),
    dict(player='Albin Ekdal', position='DEF', sub_position='CB', club='Malmö FF', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Malmö FF; experienced Sweden international; utility cover; domestic level',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Utility cover; domestic league', tier_revised='3'),
    dict(player='Jacob Smith', position='DEF', sub_position='LB', club='Djurgårdens IF', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Djurgårdens IF LB; domestic squad cover; minimal WC minutes expected',
         int_l5_pattern='DNP/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Domestic depth LB; Allsvenskan', tier_revised='3'),
    dict(player='Isak Stroud', position='DEF', sub_position='RB', club='Malmö FF', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Malmö FF RB; young Swedish international; depth option in defence',
         int_l5_pattern='sub/DNP/DNP/sub/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young depth RB; Allsvenskan', tier_revised='3'),
    # Midfielders
    dict(player='Lucas Bergvall', position='MID', sub_position='CM', club='Tottenham Hotspur', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Tottenham CM (born 2006); Sweden\'s brightest young talent; exceptional technical quality; '
               'key creative force in Swedish midfield',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key creative CM; Tottenham PL quality', tier_revised='2'),
    dict(player='Mattias Svanberg', position='MID', sub_position='CM', club='Wolfsburg', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Wolfsburg CM; consistent Sweden international; solid work-rate and pressing; dependable starter',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM; Wolfsburg Bundesliga', tier_revised='2'),
    dict(player='Ken Sema', position='MID', sub_position='LW', club='Udinese', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Udinese winger; powerful and direct; Sweden regular on the left; Serie A consistency',
         int_l5_pattern='90/sub/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular winger; Udinese Serie A', tier_revised='2'),
    dict(player='Samuel Ayari', position='MID', sub_position='CM', club='AIK', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='AIK CM; young Swedish international; promising domestic performer; depth option',
         int_l5_pattern='sub/90/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young CM; Allsvenskan', tier_revised='3'),
    dict(player='Patrik Karlström', position='MID', sub_position='DM', club='AIK', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='AIK DM; solid defensive midfielder; domestic squad depth; limited WC minutes',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Domestic DM depth; Allsvenskan', tier_revised='3'),
    dict(player='Ardian Zeneli', position='MID', sub_position='AM', club='Stade de Reims', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Stade de Reims AM/winger; Sweden-qualifying contributor; Ligue 1 experience',
         int_l5_pattern='sub/sub/DNP/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation winger/AM; Ligue 1', tier_revised='3'),
    # Forwards
    dict(player='Anthony Elanga', position='FWD', sub_position='', club='Newcastle United', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Newcastle winger; electric pace and direct running; Sweden\'s key attacking wide threat; '
               'PL quality; prolific in qualifying',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key winger; Newcastle PL quality', tier_revised='2'),
    dict(player='Viktor Bernhardsson', position='FWD', sub_position='', club='IFK Göteborg', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='IFK Göteborg forward; prolific domestically; squad option behind the main strikers',
         int_l5_pattern='90/sub/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Domestic striker rotation; Allsvenskan', tier_revised='3'),
    dict(player='Hamad Ali', position='FWD', sub_position='', club='Malmö FF', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Malmö FF forward; Sweden domestic talent; depth option in attack',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Domestic depth striker; Allsvenskan', tier_revised='3'),
    dict(player='Casper Nygren', position='FWD', sub_position='', club='Hammarby IF', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hammarby IF forward; young Swedish talent; depth striker option; minimal WC minutes',
         int_l5_pattern='sub/DNP/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young domestic forward; Allsvenskan', tier_revised='3'),
    dict(player='Johan Nilsson', position='FWD', sub_position='', club='AIK', nationality='Sweden', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='AIK forward; Swedish domestic depth; squad option only',
         int_l5_pattern='sub/DNP/sub/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Domestic depth forward; Allsvenskan', tier_revised='3'),
]

def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Sweden': continue
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
