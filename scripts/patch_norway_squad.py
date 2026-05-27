#!/usr/bin/env python3
"""
patch_norway_squad.py  —  confirmed 26-man squad, May 21 2026, Ståle Solbakken.
Haaland (T1) and Ødegaard (T2) already in CSV — confirm to 100%.
Group I: France(10.0), Senegal(7.1), Norway(5.3), Iraq(3.2).
Advance 58%, dead rubber G3 10%.
"""
import csv
PATH = '/tmp/world_cup_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = {'Erling Haaland', 'Martin Ødegaard'}
CORRECTIONS  = {}

ADV, DR = 58, 10
T1G, T1K = 87.1, 73
T2G, T2K = 74.0, 65
T3G, T3K = 42.0, 40
T4G, T4K = 16.0, 10

NEW_PLAYERS = [
    dict(player='Ørjan Nyland', position='GK', sub_position='', club='Sevilla', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=78,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Norway No.1; Sevilla; experienced shot-stopper; GK chaos in qualifying but undisputed No.1',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1', tier_revised='GK1'),
    dict(player='Egil Selvik', position='GK', sub_position='', club='Watford', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=8,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Watford GK; Norway No.2; no WC starts expected',
         int_l5_pattern='90/DNP/90/DNP/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK', tier_revised='GK2'),
    dict(player='Sander Tangvik', position='GK', sub_position='', club='Hamburger SV', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hamburg GK; Norway No.3; no WC minutes',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK', tier_revised='GK3'),
    # Defenders
    dict(player='Julian Ryerson', position='DEF', sub_position='RB', club='Borussia Dortmund', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Dortmund RB; Norway first-choice right-back; dynamic overlapper; solid defensively',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; Dortmund CL regular', tier_revised='1'),
    dict(player='Kristoffer Ajer', position='DEF', sub_position='CB', club='Brentford', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Brentford CB; Norway defensive rock; commanding aerially; '
               'experienced Premier League performer',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Brentford PL quality', tier_revised='1'),
    dict(player='Leo Østigård', position='DEF', sub_position='CB', club='Genoa', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Genoa CB; Norway regular CB partner; physical and aerially strong; Serie A experience',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB; Genoa Serie A', tier_revised='2'),
    dict(player='Fredrik Bjørkan', position='DEF', sub_position='LB', club='Bodø/Glimt', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Bodø/Glimt LB; Norway left-back; attack-minded; reliable domestic performer',
         int_l5_pattern='90/90/90/DNP/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular LB; domestic league form', tier_revised='2'),
    dict(player='Torbjørn Heggem', position='DEF', sub_position='RB', club='Bologna', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Bologna RB/wing; versatile; rotation option in Solbakken system',
         int_l5_pattern='90/sub/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation RB; Bologna Serie A', tier_revised='2'),
    dict(player='Marcus Holmgren Pedersen', position='DEF', sub_position='RB', club='Torino', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Torino RB; 3rd/4th defensive option; squad cover',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation cover; Serie A', tier_revised='3'),
    dict(player='Sondre Langås', position='DEF', sub_position='CB', club='Derby County', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Derby County CB; 4th/5th CB option; Championship level',
         int_l5_pattern='90/sub/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CB; Championship', tier_revised='3'),
    dict(player='Henrik Falchener', position='DEF', sub_position='CB', club='Viking FK', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Viking FK CB; domestic selection; depth option',
         int_l5_pattern='sub/DNP/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Domestic depth CB', tier_revised='3'),
    dict(player='David Møller Wolfe', position='DEF', sub_position='LB', club='Wolverhampton Wanderers', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Wolves LB; 4th LB option; squad depth only',
         int_l5_pattern='DNP/sub/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe LB; PL squad depth', tier_revised='4'),
    # Midfielders
    dict(player='Fredrik Aursnes', position='MID', sub_position='DM', club='Benfica', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Benfica DM; key Norway midfield anchor; tenacious tackler; excellent pressing; '
               'partners Ødegaard in central midfield',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key DM starter; Benfica Champions League', tier_revised='1'),
    dict(player='Sander Berge', position='MID', sub_position='DM', club='Fulham', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Fulham DM; physical and athletic; good range of passing; regular Norway option',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular DM; Fulham PL form', tier_revised='2'),
    dict(player='Oscar Bobb', position='MID', sub_position='AM', club='Fulham', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Fulham AM/winger; creative and direct; key attacking rotation for Solbakken',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular AM; Fulham PL form', tier_revised='2'),
    dict(player='Kristian Thorstvedt', position='MID', sub_position='CM', club='Sassuolo', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Sassuolo CM; box-to-box; versatile; regular Norway rotation player',
         int_l5_pattern='90/sub/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM rotation; Serie B', tier_revised='2'),
    dict(player='Antonio Nusa', position='MID', sub_position='AM', club='RB Leipzig', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Leipzig winger/AM (21); explosive and direct; impact threat from wide; exciting young talent',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Impact winger; Leipzig Bundesliga', tier_revised='3'),
    dict(player='Andreas Schjelderup', position='MID', sub_position='AM', club='Benfica', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Benfica AM/winger; young talent; attacking rotation option',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young AM; Benfica squad depth', tier_revised='3'),
    dict(player='Jens Petter Hauge', position='MID', sub_position='AM', club='Bodø/Glimt', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Bodø/Glimt winger; Norwegian domestic talent; squad rotation option',
         int_l5_pattern='90/sub/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation winger; domestic league', tier_revised='3'),
    dict(player='Thelonious Aasgaard', position='MID', sub_position='CM', club='Rangers', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Rangers CM; young Norwegian international; creative and progressive',
         int_l5_pattern='sub/90/DNP/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young CM; Scottish Prem', tier_revised='3'),
    dict(player='Patrick Berg', position='MID', sub_position='DM', club='Bodø/Glimt', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Bodø/Glimt DM; defensive cover in midfield; domestic base',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation DM; Norwegian Eliteserien', tier_revised='3'),
    dict(player='Morten Thorsby', position='MID', sub_position='CM', club='Cremonese', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Cremonese CM; 5th/6th midfield option; minimal WC minutes expected',
         int_l5_pattern='DNP/sub/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CM; Serie B', tier_revised='4'),
    # Forwards
    dict(player='Alexander Sørloth', position='FWD', sub_position='', club='Atlético Madrid', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atlético Madrid striker; powerful CF; clinical and physical; '
               'key second striker option behind Haaland in Norway\'s system',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Second choice striker; Atlético LaLiga', tier_revised='2'),
    dict(player='Jørgen Strand Larsen', position='FWD', sub_position='', club='Crystal Palace', nationality='Norway', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Crystal Palace striker; direct and physical; prolific in qualifying; '
               'quality third-striker option; PL experience',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular striker rotation; Palace PL', tier_revised='2'),
]

def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Norway': continue
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
