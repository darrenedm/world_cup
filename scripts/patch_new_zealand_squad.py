#!/usr/bin/env python3
"""
patch_new_zealand_squad.py — official 26-man squad (Darren Bazeley, announced May 14 2026).
Group G: Belgium(7.6), Iran(5.5), Egypt(5.0), New Zealand(1.0).
Advance 1%, dead rubber G3 10%.
Captain: Chris Wood (Nottingham Forest, 34yo) — NZ all-time top scorer (45 goals, 88 caps).
Tommy Smith and Chris Wood become first NZ men to play at two WCs (also 2010).
15 of 26 ply trade outside NZ and A-League.
Key: Liberato Cacace (Wrexham LB), Joe Bell (Viking FK CM), Marko Stamenic (Swansea CM).
NOTE: Cacace moved to Wrexham not Southampton as per confirmed squad announcement (May 14 2026).
Group: Iran (June 16 Los Angeles), Egypt (June 22 Vancouver), Belgium (June 27 Vancouver).
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 1, 10
T1G, T1K = 72.0, 0
T2G, T2K = 52.0, 0
T3G, T3K = 18.0, 0
T4G, T4K = 3.0,  0

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Max Crocombe', position='GK', sub_position='', club='Millwall', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Millwall GK (Championship); New Zealand undisputed No.1; EFL Championship experience; '
               'reliable shot-stopper; leads GK department for Group G campaign',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; Millwall Championship', tier_revised='GK1'),
    dict(player='Alex Paulsen', position='GK', sub_position='', club='Lechia Gdańsk', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Lechia Gdańsk GK (Poland); New Zealand No.2 keeper; Polish Ekstraklasa experience; backup behind Crocombe',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Lechia Gdańsk Polish Ekstraklasa', tier_revised='GK2'),
    dict(player='Michael Woud', position='GK', sub_position='', club='Auckland FC', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Auckland FC GK (A-League); New Zealand third-choice keeper; domestic A-League based; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Auckland FC A-League', tier_revised='GK3'),
    # Defenders
    dict(player='Tommy Smith', position='DEF', sub_position='RB', club='Braintree Town', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Braintree Town RB (England National League); New Zealand veteran (36yo); one of only two players returning '
               'from the 2010 WC alongside Chris Wood; became first NZ men to play at two WCs; '
               'legendary servant of NZ football; included on merit of legacy and experience',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran T1; 2010 and 2026 WC; Braintree Town National League', tier_revised='1'),
    dict(player='Liberato Cacace', position='DEF', sub_position='LB', club='Wrexham', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Wrexham LB (Championship); New Zealand best young defender; dynamic attacking left-back; '
               'Championship quality; one of NZ\'s most exciting players; key in wide areas',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; Wrexham Championship', tier_revised='1'),
    dict(player='Michael Boxall', position='DEF', sub_position='CB', club='Minnesota United', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Minnesota United CB (MLS); New Zealand first-choice centre-back; experienced MLS defender; '
               'physical and composed; key in NZ central defence for Group G',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Minnesota United MLS', tier_revised='1'),
    dict(player='Tyler Bindon', position='DEF', sub_position='CB', club='Nottingham Forest', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Nottingham Forest CB (Premier League); New Zealand highest-profile defender; Premier League quality; '
               'the best club in the NZ squad\'s roster; commanding young CB with top-flight pedigree',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Nottingham Forest Premier League', tier_revised='1'),
    dict(player='Nando Pijnaker', position='DEF', sub_position='CB', club='Auckland FC', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Auckland FC CB (A-League); New Zealand CB rotation; domestic A-League experience; squad depth in central defence',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Auckland FC A-League', tier_revised='2'),
    dict(player='Tim Payne', position='DEF', sub_position='RB', club='Wellington Phoenix', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Wellington Phoenix RB (A-League); New Zealand right-back rotation; domestic A-League; '
               'squad depth alongside Tommy Smith',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation RB; Wellington Phoenix A-League', tier_revised='2'),
    dict(player='Francis De Vries', position='DEF', sub_position='CB', club='Auckland FC', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Auckland FC CB (A-League); New Zealand defensive fringe; domestic A-League; limited WC minutes expected',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB depth; Auckland FC A-League', tier_revised='3'),
    dict(player='Finn Surman', position='DEF', sub_position='CB', club='Portland Timbers', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Portland Timbers CB (MLS); New Zealand defensive squad depth; MLS experience; limited WC minutes expected',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB depth; Portland Timbers MLS', tier_revised='3'),
    dict(player='Callan Elliot', position='DEF', sub_position='LB', club='Auckland FC', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Auckland FC LB (A-League); New Zealand left-back depth behind Cacace; domestic A-League; '
               'limited WC minutes expected',
         int_l5_pattern='sub/sub/DNP/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='LB depth; Auckland FC A-League', tier_revised='3'),
    # Midfielders
    dict(player='Joe Bell', position='MID', sub_position='CM', club='Viking FK', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Viking FK CM (Norway Eliteserien); New Zealand key midfield organiser; energetic and hardworking; '
               'Norwegian top-flight quality; crucial to NZ\'s midfield engine room',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CM; Viking FK Norwegian Eliteserien', tier_revised='1'),
    dict(player='Marko Stamenic', position='MID', sub_position='CM', club='Swansea City', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Swansea City CM (Championship); New Zealand creative midfielder; technically gifted; Championship quality; '
               'the most creative force in NZ\'s midfield; key to building attacks',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice creative CM; Swansea City Championship', tier_revised='1'),
    dict(player='Ryan Thomas', position='MID', sub_position='CM', club='PEC Zwolle', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='PEC Zwolle CM (Netherlands Eerste Divisie); New Zealand midfield rotation; Dutch Eerste Divisie quality; '
               'box-to-box option alongside Bell/Stamenic',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; PEC Zwolle Dutch Eerste Divisie', tier_revised='2'),
    dict(player='Sarpreet Singh', position='MID', sub_position='AM', club='Wellington Phoenix', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Wellington Phoenix AM (A-League); New Zealand creative attacking midfielder; formerly Bayern Munich II; '
               'talented and tricky; A-League quality; good rotation option in the No.10 role',
         int_l5_pattern='sub/90/sub/90/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation AM; Wellington Phoenix A-League', tier_revised='2'),
    dict(player='Matt Garbett', position='MID', sub_position='CM', club='Peterborough United', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Peterborough United CM (League One); New Zealand midfield rotation; EFL League One quality; '
               'hardworking rotation option in central midfield',
         int_l5_pattern='sub/sub/90/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Peterborough United EFL League One', tier_revised='2'),
    dict(player='Alex Rufer', position='MID', sub_position='CM', club='Wellington Phoenix', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Wellington Phoenix CM (A-League); New Zealand midfield depth; domestic A-League; limited WC minutes expected',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; Wellington Phoenix A-League', tier_revised='3'),
    dict(player='Ben Old', position='MID', sub_position='WNG', club='Saint-Étienne', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Saint-Étienne WNG (Ligue 1); New Zealand wide midfield depth; Ligue 1 quality; '
               'useful squad option from wide; limited WC minutes expected',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='WNG depth; Saint-Étienne Ligue 1', tier_revised='3'),
    dict(player='Lachlan Bayliss', position='MID', sub_position='CM', club='Newcastle Jets', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Newcastle Jets CM (A-League); New Zealand midfield depth; domestic A-League; limited WC minutes expected',
         int_l5_pattern='sub/sub/DNP/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; Newcastle Jets A-League', tier_revised='3'),
    # Forwards
    dict(player='Chris Wood', position='FWD', sub_position='CF', club='Nottingham Forest', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Nottingham Forest CF (Premier League); New Zealand captain and all-time top scorer (45 goals, 88 caps, 34yo); '
               'Premier League quality; powerful target man; veteran of 2010 WC (alongside Tommy Smith); '
               'second WC appearance 16 years apart; the undisputed centre of NZ\'s attack',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain and all-time top scorer; undisputed T1; Nottingham Forest PL', tier_revised='1'),
    dict(player='Callum McCowatt', position='FWD', sub_position='WNG', club='Silkeborg IF', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Silkeborg IF WNG (Denmark Superliga); New Zealand wide attacker; Danish Superliga quality; '
               'direct and creative from wide; regular option to support Wood',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation WNG; Silkeborg IF Danish Superliga', tier_revised='2'),
    dict(player='Eli Just', position='FWD', sub_position='WNG', club='Motherwell', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Motherwell WNG (Scottish Premiership); New Zealand wide forward; Scottish Premiership quality; '
               'pacy and direct; useful rotation option in wide attacking positions',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation WNG; Motherwell Scottish Premiership', tier_revised='2'),
    dict(player='Kosta Barbarouses', position='FWD', sub_position='WNG', club='Western Sydney Wanderers', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Western Sydney Wanderers WNG (A-League); New Zealand experienced winger; domestic A-League; '
               'veteran attacker providing squad depth; limited WC minutes expected',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='WNG depth; Western Sydney Wanderers A-League', tier_revised='3'),
    dict(player='Ben Waine', position='FWD', sub_position='CF', club='Port Vale', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Port Vale CF (League One); New Zealand striker depth; EFL League One; '
               'backup CF option behind Wood; limited WC minutes expected',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CF depth; Port Vale EFL League One', tier_revised='3'),
    dict(player='Jesse Randall', position='FWD', sub_position='WNG', club='Auckland FC', nationality='New Zealand', group='G',
         wc_squad_prob_pct=100, tier='4', playing_role='Fringe Player',
         group_mins_per_game=T4G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Auckland FC WNG (A-League); New Zealand fringe forward; domestic A-League; minimal WC minutes expected',
         int_l5_pattern='DNP/DNP/sub/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe WNG; Auckland FC A-League', tier_revised='4'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'New Zealand': continue
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
