#!/usr/bin/env python3
"""
patch_panama_squad.py — CONFIRMED official 26-man squad (Christiansen, announced May 26 2026).
Group L: England(9.3), Croatia(7.4), Panama(5.3), Ghana(2.1).
Advance 22%, dead rubber G3 10%.
Note: Rolando Blackburn NOT selected. Édgar Bárcenas NOT selected (Yoel Bárcenas IS).
Key fitness: Carrasquilla — fitness described as critical concern heading into tournament.
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 22, 10
T1G, T1K = 78.0, 5
T2G, T2K = 62.0, 4
T3G, T3K = 30.0, 3
T4G, T4K = 8.0,  1

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Orlando Mosquera', position='GK', sub_position='', club='Al-Fayha', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=5,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Fayha GK; Panama undisputed No.1; Saudi Pro League experience; experienced international',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; Al-Fayha Saudi Pro League', tier_revised='GK1'),
    dict(player='Luis Mejía', position='GK', sub_position='', club='Club Nacional', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=1,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Club Nacional GK (Uruguay); Panama No.2; experienced backup; no WC starts expected',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Club Nacional Uruguayan Primera', tier_revised='GK2'),
    dict(player='César Samudio', position='GK', sub_position='', club='CD Marathón', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='CD Marathón GK; Panama No.3; Honduran league experience; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; CD Marathón Liga Nacional Honduras', tier_revised='GK3'),
    # Defenders
    dict(player='Michael Murillo', position='DEF', sub_position='RB', club='Beşiktaş', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Beşiktaş RB; Panama best outfield player; top-level European experience; dynamic and attacking right-back',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; Beşiktaş Turkish Super Lig', tier_revised='1'),
    dict(player='Fidel Escobar', position='DEF', sub_position='CB', club='Deportivo Saprissa', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Deportivo Saprissa CB; Panama veteran defensive leader; commanding and experienced; anchors backline',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran CB leader; Saprissa Costa Rican Primera', tier_revised='1'),
    dict(player='Andrés Andrade', position='DEF', sub_position='CB', club='LASK Linz', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='LASK Linz CB; Austria Bundesliga experience; reliable Panama starting centre-back; composed on the ball',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Starting CB; LASK Austrian Bundesliga', tier_revised='1'),
    dict(player='José Córdoba', position='DEF', sub_position='CB', club='Norwich City', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Norwich City CB; rising star; Championship experience; youngest regular starter in Panama defence; strong in the air',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB; Norwich City Championship', tier_revised='1'),
    dict(player='César Blackman', position='DEF', sub_position='RB', club='Slovan Bratislava', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Slovan Bratislava RB/CB; versatile defender; Slovak Super Liga experience; rotation cover for Murillo',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation RB/CB; Slovan Bratislava Slovak Super Liga', tier_revised='2'),
    dict(player='Éric Davis', position='DEF', sub_position='CB', club='CD Plaza Amador', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='CD Plaza Amador CB; domestic experience; Panama rotation CB; reliable squad depth',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; CD Plaza Amador LPF', tier_revised='2'),
    dict(player='Edgardo Fariña', position='DEF', sub_position='LB', club='Pari Nizhny Novgorod', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Pari Nizhny Novgorod LB; Russia league experience; Panama regular left-back; solid and reliable',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular LB; Pari Nizhny Novgorod RPL', tier_revised='2'),
    dict(player='Jorge Gutiérrez', position='DEF', sub_position='LB', club='Deportivo La Guaira', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Deportivo La Guaira LB/CB; Venezuelan league experience; squad depth; rotation cover',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth LB/CB; Deportivo La Guaira Venezuelan Primera', tier_revised='3'),
    dict(player='Jiovany Ramos', position='DEF', sub_position='CB', club='Puerto Cabello', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Puerto Cabello CB; Venezuelan league; defensive depth; limited WC minutes expected',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CB; Puerto Cabello Venezuelan Primera', tier_revised='3'),
    dict(player='Roderick Miller', position='DEF', sub_position='CB', club='Turan Tovuz', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Turan Tovuz CB/RB; Azerbaijani league; fringe depth option; minimal WC minutes expected',
         int_l5_pattern='sub/DNP/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CB/RB; Turan Tovuz Azerbaijani Premier League', tier_revised='4'),
    # Midfielders
    dict(player='Aníbal Godoy', position='MID', sub_position='DM', club='San Diego FC', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='San Diego FC DM; Panama captain; record 159 caps; warrior in midfield; leads by example; MLS experience',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain; record-holder 159 caps; San Diego FC MLS', tier_revised='1'),
    dict(player='Adalberto Carrasquilla', position='MID', sub_position='CM', club='UNAM Pumas', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='UNAM Pumas CM/AM; Panama creative engine; fitness described as critical concern heading into tournament; vital if fit',
         int_l5_pattern='90/sub/90/DNP/90', int_l5_starts=3, int_absence_reason='Fitness concern (undisclosed)',
         fitness_current='Critical fitness concern; closely monitored; vital player if available', tier_revised='1'),
    dict(player='Yoel Bárcenas', position='MID', sub_position='CM', club='Mazatlán FC', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Mazatlán FC CM/AM; creative option in wide areas; Liga MX experience; Panama regular',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM/AM; Mazatlán FC Liga MX', tier_revised='2'),
    dict(player='Carlos Harvey', position='MID', sub_position='CM', club='Minnesota United', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Minnesota United CM; MLS experience; Panama regular midfielder; box-to-box engine',
         int_l5_pattern='90/90/sub/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM; Minnesota United MLS', tier_revised='2'),
    dict(player='Cristian Martínez', position='MID', sub_position='CM', club='Hapoel Ironi Kiryat Shmona', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hapoel Ironi Kiryat Shmona CM; Israeli league experience; Panama squad regular; reliable midfield cover',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Israeli Premier League', tier_revised='2'),
    dict(player='Alberto Quintero', position='MID', sub_position='AM', club='CD Plaza Amador', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='CD Plaza Amador AM/LW; 38 yrs; veteran winger returning from injury; Panama experience and quality; wide creative option',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit; returning from injury; 38 yrs, fitness managed', tier_evidence='Veteran LW; Plaza Amador LPF', tier_revised='2'),
    dict(player='José Luis Rodríguez', position='MID', sub_position='CM', club='FC Juárez', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FC Juárez CM; Liga MX experience; Panama depth midfielder; squad rotation option',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CM; FC Juárez Liga MX', tier_revised='3'),
    dict(player='César Yanis', position='MID', sub_position='DM', club='Cobresal', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Cobresal CM/DM; Chilean Primera experience; Panama depth option; defensive midfield cover',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth DM/CM; Cobresal Chilean Primera', tier_revised='3'),
    dict(player='Azarías Londoño', position='MID', sub_position='CM', club='Universidad Católica', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Universidad Católica CM; Chilean Primera experience; Panama squad depth; limited WC minutes expected',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CM; Universidad Católica Chilean Primera', tier_revised='3'),
    # Forwards
    dict(player='Ismael Díaz', position='FWD', sub_position='', club='Club León', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Club León ST/LW; Panama top scorer and key attacker; Liga MX quality; direct and dangerous in front of goal',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice attacker; Club León Liga MX', tier_revised='1'),
    dict(player='José Fajardo', position='FWD', sub_position='', club='Universidad Católica', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Universidad Católica ST; joint top scorer in CONCACAF qualifying; clinical finisher; Chilean Primera quality',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Joint top qualifier scorer; U. Católica Chilean Primera', tier_revised='1'),
    dict(player='Cecilio Waterman', position='FWD', sub_position='', club='Universidad de Concepción', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='U. de Concepción RW/ST; physical wide attacker; pace and power; Panama regular; Chilean Primera',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular wide attacker; U. de Concepción Chilean Primera', tier_revised='2'),
    dict(player='Tomás Rodríguez', position='FWD', sub_position='', club='Deportivo Saprissa', nationality='Panama', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Deportivo Saprissa ST/RW; known as "Puma"; joint top scorer in qualifying alongside Fajardo; Costa Rican Primera',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Joint top qualifier scorer; Saprissa Costa Rican Primera', tier_revised='2'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Panama': continue
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
