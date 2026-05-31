#!/usr/bin/env python3
"""
patch_ecuador_squad.py — projected 26-man squad (Beccacece, announced ~June 1 2026).
Group E: Germany(7.9), Ecuador(5.8), Ivory Coast(4.4), Curaçao(1.3).
Advance 52%, dead rubber G3 10%.
Key fitness: Estupiñán (persistent muscle history, monitored),
             Pacho + Hincapié (UCL final May 30, joining squad late).
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 52, 10
T1G, T1K = 85.0, 54
T2G, T2K = 72.0, 44
T3G, T3K = 40.0, 31
T4G, T4K = 14.0, 9

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Hernán Galíndez', position='GK', sub_position='', club='CA Huracán', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=54,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='CA Huracán GK; Ecuador undisputed No.1; most-capped Ecuador GK; 39 yrs; commanding and experienced',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; long-serving Ecuador No.1', tier_revised='GK1'),
    dict(player='Gonzalo Valle', position='GK', sub_position='', club='LDU Quito', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=5,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='LDU Quito GK; Ecuador No.2; domestic experience; no WC starts expected',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Ecuadorian LigaPro', tier_revised='GK2'),
    dict(player='Moisés Ramírez', position='GK', sub_position='', club='Independiente del Valle', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='IDV GK; Ecuador No.3; young promising keeper; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; IDV LigaPro', tier_revised='GK3'),
    # Defenders
    dict(player='Willian Pacho', position='DEF', sub_position='CB', club='Paris Saint-Germain', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='PSG CB; elite centre-back; UCL finalist (May 30); joined squad late with compressed recovery; expected to start',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit; joined squad late after UCL final May 30', tier_evidence='First-choice CB; PSG Ligue 1 / UCL', tier_revised='1'),
    dict(player='Piero Hincapié', position='DEF', sub_position='CB', club='Arsenal', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Arsenal CB/LB; UCL finalist (May 30); joined squad late; deployed as CB for Ecuador; world-class defender',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit; joined squad late after UCL final May 30', tier_evidence='First-choice CB; Arsenal PL', tier_revised='1'),
    dict(player='Pervis Estupiñán', position='DEF', sub_position='LB', club='AC Milan', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='AC Milan LB; Ecuador first-choice left-back; pacey and attack-minded; persistent muscle injury history; closely monitored',
         int_l5_pattern='90/DNP/90/90/sub', int_l5_starts=3, int_absence_reason='Persistent muscle injury history; monitoring',
         fitness_current='Monitoring; muscle injury history; expected to feature but fitness uncertain', tier_revised='1'),
    dict(player='Joel Ordóñez', position='DEF', sub_position='RB', club='Club Brugge', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Club Brugge RB; excellent young right-back pushing for starting spot; Belgian Pro League quality',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular RB; Club Brugge Belgian Pro League', tier_revised='2'),
    dict(player='Ángelo Preciado', position='DEF', sub_position='RB', club='Atlético Mineiro', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atlético Mineiro RB; competes with Ordóñez for RB slot; experienced international; Brazilian Série A',
         int_l5_pattern='90/90/sub/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation RB; Atlético Mineiro Série A Brazil', tier_revised='2'),
    dict(player='Félix Torres', position='DEF', sub_position='CB', club='SC Internacional', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='SC Internacional CB; depth centre-back; Brazilian Série A experience; squad cover',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CB; SC Internacional Série A Brazil', tier_revised='3'),
    dict(player='Jackson Porozo', position='DEF', sub_position='CB', club='Club Tijuana', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Club Tijuana CB; versatile squad centre-back; Liga MX experience; rotation cover',
         int_l5_pattern='sub/DNP/90/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Liga MX', tier_revised='3'),
    dict(player='José Andrés Hurtado', position='DEF', sub_position='RB', club='Red Bull Bragantino', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Red Bull Bragantino RB/CB; depth cover; limited WC minutes expected',
         int_l5_pattern='sub/DNP/sub/DNP/sub', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe defender; Bragantino Série A Brazil', tier_revised='4'),
    # Midfielders
    dict(player='Moisés Caicedo', position='MID', sub_position='DM', club='Chelsea', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Chelsea DM; Ecuador heartbeat; world-class; 4th most expensive PL signing ever; key to everything Ecuador do',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed starter; Chelsea PL', tier_revised='1'),
    dict(player='Alan Franco', position='MID', sub_position='CM', club='Atlético Mineiro', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atlético Mineiro CM; regular midfield partner for Caicedo in qualifying; reliable and experienced',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM; Atlético Mineiro Série A Brazil', tier_revised='1'),
    dict(player='Kendry Páez', position='MID', sub_position='AM', club='River Plate', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='River Plate AM (loan from Chelsea); 19 yrs; creative no.10 and future of Ecuador; exceptional talent',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key creative starter; Chelsea-owned / River Plate loan', tier_revised='1'),
    dict(player='Pedro Vite', position='MID', sub_position='CM', club='UNAM Pumas', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='UNAM Pumas CM/LW; featured regularly under Beccacece; versatile midfield option; Liga MX',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular midfield option; UNAM Pumas Liga MX', tier_revised='2'),
    dict(player='Jeremy Sarmiento', position='MID', sub_position='AM', club='Burnley', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Burnley AM/LW (Brighton-to-Burnley loan); left-channel creative option; Ecuador regular; Championship form',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular AM/LW; Burnley Championship', tier_revised='2'),
    dict(player='Denil Castillo', position='MID', sub_position='CM', club='FC Midtjylland', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FC Midtjylland CM; energetic box-to-box depth option; Danish Superliga; squad rotation',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Danish Superliga', tier_revised='3'),
    dict(player='John Yeboah', position='MID', sub_position='AM', club='Venezia', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Venezia AM/RW; pace and directness from wide; Serie A experience; squad depth',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation winger/AM; Venezia Serie A', tier_revised='3'),
    dict(player='Jordy Alcívar', position='MID', sub_position='CM', club='Independiente del Valle', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='IDV CM; domestic depth option; fringe squad member; limited WC minutes expected',
         int_l5_pattern='sub/DNP/sub/DNP/sub', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CM; IDV LigaPro', tier_revised='4'),
    # Forwards
    dict(player='Enner Valencia', position='FWD', sub_position='', club='Pachuca', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Pachuca ST; Ecuador all-time top scorer (42 goals); 36 yrs; irreplaceable captain and leader; fitness managed carefully',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit; age-managed; 36 yrs', tier_evidence='Undisputed captain-striker; Ecuador all-time top scorer', tier_revised='1'),
    dict(player='Gonzalo Plata', position='FWD', sub_position='', club='Flamengo', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Flamengo RW; key wide threat; pace and directness; Brazilian Série A quality; Ecuador regular starter',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice winger; Flamengo Série A Brazil', tier_revised='1'),
    dict(player='Nilson Angulo', position='FWD', sub_position='', club='Sunderland', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Sunderland LW; left wing option; Championship quality; strong market value; regular Ecuador option',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular LW; Sunderland Championship', tier_revised='2'),
    dict(player='Kevin Rodríguez', position='FWD', sub_position='', club='Union Saint-Gilloise', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Union Saint-Gilloise RW/ST; versatile attacker; 18 qualifying appearances; Belgian Pro League quality',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular attacker; Union Saint-Gilloise Belgian Pro League', tier_revised='2'),
    dict(player='Leonardo Campana', position='FWD', sub_position='', club='New England Revolution', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='New England Revolution ST; backup striker; MLS experience; physical depth option behind Valencia',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup ST; New England Revolution MLS', tier_revised='3'),
    dict(player='Jordy Caicedo', position='FWD', sub_position='', club='CA Huracán', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='CA Huracán ST; depth striker; Argentine Primera División; squad rotation option',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth ST; Argentine Primera División', tier_revised='3'),
    dict(player='Jeremy Arévalo', position='FWD', sub_position='', club='VfB Stuttgart', nationality='Ecuador', group='E',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='VfB Stuttgart ST/RW; 21 yrs; developing talent; Bundesliga depth; fringe squad selection',
         int_l5_pattern='sub/DNP/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young fringe forward; Stuttgart Bundesliga', tier_revised='4'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Ecuador': continue
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
