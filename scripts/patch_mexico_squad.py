#!/usr/bin/env python3
"""
patch_mexico_squad.py — official 26-man squad (Javier Aguirre, announced June 1 2026).
Group A: Mexico(7.1), South Korea(5.9), Czech Republic(4.3), South Africa(2.9).
Advance 72%, dead rubber G3 10%.
Key fitness: Edson Álvarez (ankle surgery Feb; building minutes; cautious for opener June 11),
             Alexis Vega (knee concern; made squad; monitored),
             Luis Chávez (limited appearances due to injury),
             César Huerta (limited appearances since October).
Notable: Ochoa called up after Luis Malagón suffered torn ACL; Hirving 'Chucky' Lozano omitted
         (reported disciplinary tension with San Diego FC); Henry Martín not selected.
         Gilberto Mora (17) could become Mexico's youngest-ever World Cup player.
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 72, 10
T1G, T1K = 87.1, 137
T2G, T2K = 74.0, 112
T3G, T3K = 42.0, 79
T4G, T4K = 16.0, 23

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Raúl Rangel', position='GK', sub_position='', club='Guadalajara', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Guadalajara GK; Mexico undisputed No.1 after Malagón ACL ruled out; 26-year-old commanding presence '
               'between the posts; strong reflexes and commanding in the box.',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed No.1 starter; Chivas Liga MX', tier_revised='GK1'),
    dict(player='Guillermo Ochoa', position='GK', sub_position='', club='AEL Limassol', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=1,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='AEL Limassol GK; legendary veteran called up as emergency replacement after Malagón ACL; '
               'record sixth World Cup appearance, matching Messi and Ronaldo; iconic but limited role expected.',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Emergency call-up backup; sixth WC; AEL Limassol', tier_revised='GK2'),
    dict(player='Carlos Acevedo', position='GK', sub_position='', club='Santos Laguna', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Santos Laguna GK; third-choice goalkeeper; no WC minutes expected; domestic Liga MX performer.',
         int_l5_pattern='90/DNP/90/DNP/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Santos Laguna Liga MX', tier_revised='GK3'),
    # Defenders
    dict(player='Jorge Sánchez', position='DEF', sub_position='RB', club='PAOK', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='PAOK RB; Mexico first-choice right-back; athletic and attacking; strong Greek Super League season; '
               'key outlet on the right flank for Aguirre.',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; PAOK Super League Greece', tier_revised='1'),
    dict(player='César Montes', position='DEF', sub_position='CB', club='Lokomotiv Moscow', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Lokomotiv Moscow CB; Mexico first-choice centre-back; dominant in the air; set-piece threat; '
               'one of two pillars of Aguirre\'s defensive unit.',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Lokomotiv Moscow RPL', tier_revised='1'),
    dict(player='Johan Vásquez', position='DEF', sub_position='CB', club='Genoa', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Genoa CB; Mexico starting centre-back; aerial presence and composure on the ball; '
               'solid Serie A performer and key partner for Montes.',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Starting CB; Genoa Serie A', tier_revised='1'),
    dict(player='Jesús Gallardo', position='DEF', sub_position='LB', club='Toluca', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Toluca LB; Mexico first-choice left-back; experienced international; attacking-minded full-back '
               'who supports well in transition.',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; Toluca Liga MX', tier_revised='1'),
    dict(player='Israel Reyes', position='DEF', sub_position='CB', club='Club América', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Club América CB; third-choice centre-back; solid defensive cover; Liga MX regular who provides '
               'depth behind Montes and Vásquez.',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB depth; Club América Liga MX', tier_revised='3'),
    dict(player='Mateo Chávez', position='DEF', sub_position='RB', club='AZ Alkmaar', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='AZ Alkmaar RB/LB; 22-year-old versatile full-back; strong Eredivisie campaign; youth and pace '
               'to cover either flank; depth behind Sánchez and Gallardo.',
         int_l5_pattern='90/sub/90/sub/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Versatile FB depth; AZ Alkmaar Eredivisie', tier_revised='3'),
    # Midfielders
    dict(player='Edson Álvarez', position='MID', sub_position='DM', club='Fenerbahçe', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='Fenerbahçe DM; Mexico captain and midfield anchor; pivotal in Aguirre\'s 4-2-3-1 double pivot; '
               'returned from ankle surgery February 2026; building fitness but missed recent Mexico-Ghana friendly; '
               'opener June 11 is doubtful but targeting tournament.',
         int_l5_pattern='90/sub/DNP/sub/90', int_l5_starts=2, int_absence_reason='Ankle surgery Feb 2026; building fitness',
         fitness_current='Doubtful for opener; ankle surgery recovery; being managed carefully', tier_revised='1'),
    dict(player='Erik Lira', position='MID', sub_position='DM', club='Cruz Azul', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Cruz Azul DM; Mexico midfield partner for Álvarez in double pivot; industrious and defensively solid; '
               'first-choice DM if Álvarez is unavailable for opener.',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular DM starter; Cruz Azul Liga MX', tier_revised='2'),
    dict(player='Álvaro Fidalgo', position='MID', sub_position='AM', club='Real Betis', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Real Betis AM; Spain-born playmaker who chose Mexico; technically excellent with vision and passing '
               'to control tempo; key creative force in Aguirre\'s attacking midfield.',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Automatic AM starter; Real Betis La Liga', tier_revised='1'),
    dict(player='Obed Vargas', position='MID', sub_position='CM', club='Atlético Madrid', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atlético Madrid CM; 20-year-old former USMNT prospect who chose Mexico; energetic box-to-box '
               'midfielder who joined Atleti in 2024; exciting young talent in Spain\'s top division.',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young rotation CM; Atlético Madrid La Liga', tier_revised='2'),
    dict(player='Luis Romo', position='MID', sub_position='CM', club='Guadalajara', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Guadalajara CM; veteran midfielder providing experience and squad depth; consistent Liga MX performer; '
               'third-choice central midfielder.',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran CM depth; Guadalajara Liga MX', tier_revised='3'),
    dict(player='Orbelín Pineda', position='MID', sub_position='AM', club='AEK Athens', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='AEK Athens AM/WNG; creative and direct attacking midfielder; experienced Mexico international; '
               'impact sub and squad rotation option behind Fidalgo.',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation AM; AEK Athens Super League Greece', tier_revised='3'),
    dict(player='Brian Gutiérrez', position='MID', sub_position='CM', club='Guadalajara', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Guadalajara CM; 22-year-old former USMNT prospect who switched allegiance to Mexico; dynamic '
               'and press-resistant; Aguirre backed him as a next-generation starter.',
         int_l5_pattern='sub/90/sub/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young CM squad player; Guadalajara Liga MX', tier_revised='3'),
    dict(player='Luis Chávez', position='MID', sub_position='CM', club='Dynamo Moscow', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='4', playing_role='Fringe',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='Dynamo Moscow CM; set-piece specialist known for powerful free kicks; limited appearances this season '
               'due to injury; fitness a concern heading into tournament.',
         int_l5_pattern='sub/DNP/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='Injury-limited appearances 2025-26',
         fitness_current='Doubtful; limited appearances due to injury this season', tier_revised='4'),
    dict(player='Gilberto Mora', position='MID', sub_position='WNG', club='Tijuana', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='4', playing_role='Fringe',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Tijuana WNG; 17-year-old phenom who could become Mexico\'s youngest-ever World Cup player; '
               'lightning pace and direct dribbling; development pick, limited tournament minutes expected.',
         int_l5_pattern='sub/sub/DNP/sub/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Teenage winger prospect; Tijuana Liga MX', tier_revised='4'),
    # Forwards
    dict(player='Santiago Giménez', position='FWD', sub_position='CF', club='AC Milan', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='AC Milan CF; Mexico\'s most lethal striker; prolific scorer in Serie A; clinical finisher with '
               'excellent movement; co-leads attack with Jiménez as Mexico\'s standout attacking talent.',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice striker; AC Milan Serie A', tier_revised='1'),
    dict(player='Raúl Jiménez', position='FWD', sub_position='CF', club='Fulham', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Fulham CF; veteran Mexico captain contender with 125 caps and 44 goals; hold-up play, link-up '
               'and leadership make him indispensable; 35 years old but still Premier League sharp.',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran starter CF; Fulham Premier League', tier_revised='1'),
    dict(player='Julián Quiñones', position='FWD', sub_position='WNG', club='Al-Qadsiah', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Qadsiah WNG; Colombia-born attacker who chose Mexico; pacey and direct wide forward; '
               'important wide attacking option and regular rotation choice in Aguirre\'s system.',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular WNG starter; Al-Qadsiah Saudi Pro League', tier_revised='2'),
    dict(player='Roberto Alvarado', position='FWD', sub_position='WNG', club='Guadalajara', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Guadalajara WNG; electric winger and one of Liga MX\'s most dangerous attackers; '
               'direct dribbler who can beat defenders; rotation wide option for Mexico.',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular WNG; Guadalajara Liga MX', tier_revised='2'),
    dict(player='César Huerta', position='FWD', sub_position='WNG', club='Anderlecht', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='Anderlecht WNG; tricky wide attacker who joined Belgian Pro League; limited appearances since '
               'October 2025 due to injury; fitness concern heading into the tournament.',
         int_l5_pattern='sub/DNP/DNP/DNP/sub', int_l5_starts=0, int_absence_reason='Limited since October 2025; injury',
         fitness_current='Doubtful; limited appearances since October 2025', tier_revised='3'),
    dict(player='Alexis Vega', position='FWD', sub_position='WNG', club='Toluca', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='Toluca WNG/FWD; versatile attacker who made squad despite knee injury concerns; '
               'creative and direct on the wing; fitness being closely monitored ahead of June 11 opener.',
         int_l5_pattern='sub/90/DNP/sub/sub', int_l5_starts=1, int_absence_reason='Knee concern; fitness monitored',
         fitness_current='Doubtful; knee concern flagged at squad announcement; monitored', tier_revised='3'),
    dict(player='Guillermo Martínez', position='FWD', sub_position='CF', club='Pumas UNAM', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='4', playing_role='Fringe',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Pumas UNAM CF; domestic striker depth providing cover behind Giménez and Jiménez; '
               'Liga MX performer but fringe selection; limited WC minutes expected.',
         int_l5_pattern='90/sub/sub/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CF depth; Pumas UNAM Liga MX', tier_revised='4'),
    dict(player='Armando González', position='FWD', sub_position='WNG', club='Guadalajara', nationality='Mexico', group='A',
         wc_squad_prob_pct=100, tier='4', playing_role='Fringe',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Guadalajara WNG; 23-year-old former USMNT dual-national who committed to Mexico; '
               'direct and pacey but fringe pick; development selection with limited WC minutes expected.',
         int_l5_pattern='sub/sub/DNP/sub/sub', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe young WNG; Guadalajara Liga MX', tier_revised='4'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Mexico': continue
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
