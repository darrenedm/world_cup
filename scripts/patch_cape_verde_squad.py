#!/usr/bin/env python3
"""
patch_cape_verde_squad.py — official 26-man squad (Bubista, announced May 18 2026).
Group H: Spain(9.7), Uruguay(7.0), Saudi Arabia(3.0), Cape Verde(2.5).
Advance 10%, dead rubber G3 10%.
HISTORIC DEBUT — Cape Verde's first-ever World Cup appearance.
Key fitness: Logan Costa (Villarreal CB) — returned from ACL (ruptured July 2025) only May 17,
             played 13 mins vs Rayo Vallecano; Bubista selected him as a gamble — biggest squad uncertainty.
Captain: Ryan Mendes (97 caps, 22 goals, age 36). Star: Dailon Livramento (Casa Pia, 24yo).
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 10, 10
T1G, T1K = 82.0, 1
T2G, T2K = 65.0, 1
T3G, T3K = 30.0, 1
T4G, T4K = 8.0,  0

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Vozinha', position='GK', sub_position='', club='GD Chaves', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=1,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='GD Chaves GK; Cape Verde No.1 and vice-captain (age 39); veteran of historic qualification campaign; '
               'experienced Portuguese Primeira Liga keeper; leads historic first WC appearance',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; GD Chaves Primeira Liga', tier_revised='GK1'),
    dict(player='Márcio Rosa', position='GK', sub_position='', club='Montana FC', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=1,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Montana FC GK (Bulgaria); Cape Verde No.2; backup for historic WC; no starts expected',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Montana FC Bulgaria', tier_revised='GK2'),
    dict(player='CJ dos Santos', position='GK', sub_position='', club='San Diego FC', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='San Diego FC GK; Cape Verde No.3; MLS-based; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; San Diego FC MLS', tier_revised='GK3'),
    # Defenders
    dict(player='Logan Costa', position='DEF', sub_position='CB', club='Villarreal', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='Villarreal CB; Cape Verde best player and only top-5-league defender; ruptured ACL pre-season July 2025; '
               'returned May 17 (13 mins vs Rayo Vallecano); Bubista selected him as a major gamble; '
               'if unfit Cape Verde lose their best defender — biggest WC uncertainty for this squad',
         int_l5_pattern='DNP/DNP/DNP/DNP/sub', int_l5_starts=0, int_absence_reason='ACL rupture July 2025; returned May 17 2026',
         fitness_current='Doubtful — ACL return; 13 mins played back; Bubista gamble; race against time', tier_revised='1'),
    dict(player='Steven Moreira', position='DEF', sub_position='RB', club='Columbus Crew', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Columbus Crew RB; Cape Verde first-choice right-back; MLS quality; attacking and energetic full-back',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; Columbus Crew MLS', tier_revised='1'),
    dict(player='Wagner Pina', position='DEF', sub_position='CB', club='Trabzonspor', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Trabzonspor CB; Cape Verde first-choice CB (especially given Logan Costa uncertainty); '
               'Turkish Süper Lig experience; physical and composed; likely to start regardless of Costa fitness',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Trabzonspor Süper Lig', tier_revised='1'),
    dict(player='João Paulo Fernandes', position='DEF', sub_position='CB', club='FCSB', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FCSB CB (Romania); Cape Verde rotation CB; Romanian Superliga experience; solid squad depth option',
         int_l5_pattern='90/90/sub/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; FCSB Romanian Superliga', tier_revised='2'),
    dict(player='Ianique Tavares', position='DEF', sub_position='CB', club='Torreense', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Torreense CB; Cape Verde veteran CB known as Stopira; experienced Portuguese second-tier performer; '
               'solid defensive stalwart; part of qualification run',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Torreense Portuguese Liga 2', tier_revised='2'),
    dict(player='Kelvin Pires', position='DEF', sub_position='LB', club='SJK Seinäjoki', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='SJK Seinäjoki LB (Finland); Cape Verde fullback option; Finnish Veikkausliiga; squad rotation',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation LB; SJK Seinäjoki Finnish Veikkausliiga', tier_revised='2'),
    dict(player='Sidny Lopes', position='DEF', sub_position='RB', club='SL Benfica B', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Benfica B RB; Cape Verde young right-back option; Portuguese football system; squad depth',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young RB depth; Benfica B Portugal', tier_revised='3'),
    dict(player='Roberto Lopes', position='DEF', sub_position='CB', club='Shamrock Rovers', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Shamrock Rovers CB; Cape Verde known as Pico; Irish League of Ireland experience; defensive depth',
         int_l5_pattern='sub/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB depth; Shamrock Rovers League of Ireland', tier_revised='3'),
    dict(player='Edilson Borges', position='DEF', sub_position='CB', club='Al-Bataeh', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Bataeh CB (UAE); Cape Verde defensive depth; UAE Pro League; fringe squad selection',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB depth; Al-Bataeh UAE Pro League', tier_revised='3'),
    # Midfielders
    dict(player='Jamiro Monteiro', position='MID', sub_position='CM', club='PEC Zwolle', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='PEC Zwolle CM; Cape Verde midfield organiser; Dutch Eredivisie experience; key in qualifying; '
               'energetic and creative in central areas',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CM; PEC Zwolle Eerste Divisie', tier_revised='1'),
    dict(player='Kevin Pina', position='MID', sub_position='CM', club='Krasnodar', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Krasnodar CM; Cape Verde key midfielder; Russian RPL experience; key contributor in qualifying campaign',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key starter CM; Krasnodar RPL', tier_revised='1'),
    dict(player='Deroy Duarte', position='MID', sub_position='CM', club='Ludogorets Razgrad', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Ludogorets CM; Cape Verde midfield rotation; Bulgarian league champion club; dynamic and technical',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Ludogorets Razgrad Bulgarian A-PFG', tier_revised='2'),
    dict(player='Telmo Arcanjo', position='MID', sub_position='CM', club='Vitória SC', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Vitória SC CM; Cape Verde Portuguese league-based midfielder; solid squad rotation option',
         int_l5_pattern='sub/90/90/sub/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Vitória SC Primeira Liga', tier_revised='2'),
    dict(player='Yannick Semedo', position='MID', sub_position='CM', club='SC Farense', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='SC Farense CM; Cape Verde Portuguese second-tier midfielder; squad depth; limited WC minutes expected',
         int_l5_pattern='sub/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; SC Farense Portuguese Segunda Liga', tier_revised='3'),
    dict(player='Laros Duarte', position='MID', sub_position='CM', club='Puskás Akadémia', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Puskás Akadémia CM (Hungary); Cape Verde squad depth midfielder; Hungarian OTP Bank Liga; fringe selection',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; Puskás Akadémia Hungarian OTP Bank Liga', tier_revised='3'),
    # Forwards
    dict(player='Dailon Livramento', position='FWD', sub_position='CF', club='Casa Pia', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Casa Pia FWD; Cape Verde main attacking threat and creative hub (age 24); scored decisive qualifying goals; '
               'the key player Bubista builds the attack around; direct and technically gifted',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Primary attacker; Casa Pia Primeira Liga', tier_revised='1'),
    dict(player='Ryan Mendes', position='FWD', sub_position='WNG', club='Iğdır FK', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Iğdır FK WNG/FWD; Cape Verde captain; all-time record scorer (22 goals) and appearance maker (97 caps); '
               'age 36 but still the inspirational leader of historic debut; experienced wide attacker',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain and record scorer; Iğdır FK Turkish Süper Lig 2', tier_revised='1'),
    dict(player='Garry Rodrigues', position='FWD', sub_position='WNG', club='Apollon Limassol', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Apollon Limassol WNG; Cape Verde experienced right winger; Cypriot First Division; part of core qualifying squad',
         int_l5_pattern='90/90/sub/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular winger; Apollon Limassol Cypriot First Division', tier_revised='2'),
    dict(player='Jovane Cabral', position='FWD', sub_position='WNG', club='Estrela da Amadora', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Estrela da Amadora WNG; Cape Verde experienced Portuguese-based winger; direct and creative from wide',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation winger; Estrela da Amadora Primeira Liga', tier_revised='2'),
    dict(player='Nuno da Costa', position='FWD', sub_position='CF', club='İstanbul Başakşehir', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Başakşehir CF; Cape Verde striker rotation; Turkish Süper Lig experience; physical target-man option',
         int_l5_pattern='sub/sub/90/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CF; Başakşehir Süper Lig', tier_revised='2'),
    dict(player='Willy Semedo', position='FWD', sub_position='WNG', club='Omonia Nicosia', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Omonia Nicosia WNG/FWD; Cape Verde attacking squad depth; Cypriot league; limited WC minutes expected',
         int_l5_pattern='sub/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='FWD depth; Omonia Nicosia Cypriot First Division', tier_revised='3'),
    dict(player='Gilson Benchimol', position='FWD', sub_position='CF', club='Akron Togliatti', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Akron Togliatti CF (Russia); Cape Verde striker depth; Russian league; fringe selection for historic WC',
         int_l5_pattern='sub/DNP/sub/sub/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CF depth; Akron Togliatti RPL', tier_revised='3'),
    dict(player='Hélio Varela', position='FWD', sub_position='WNG', club='Maccabi Tel Aviv', nationality='Cape Verde', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Maccabi Tel Aviv WNG; Cape Verde attacking fringe option; Israeli Premier League; squad depth',
         int_l5_pattern='DNP/sub/DNP/90/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='WNG depth; Maccabi Tel Aviv Israeli Premier League', tier_revised='3'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Cape Verde': continue
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
