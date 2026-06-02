#!/usr/bin/env python3
"""
patch_bosnia_squad.py — official 26-man squad (Sergej Barbarez, announced May 11 2026).
Group B: Switzerland(6.5), Canada(5.7), Qatar(3.7), Bosnia(2.2).
Advance 8%, dead rubber G3 10%.
First of 48 nations to announce final squad. 2nd-ever WC appearance (first since 2014).
Qualified dramatically — beat Italy on penalties in playoff final (Bajraktarevic scored winner).
Captain: Edin Džeko (Schalke 04, 40yo) — record goalscorer, still included as veteran leader.
Star: Esmir Bajraktarević (PSV Eindhoven, 21yo) — scored decisive playoff penalty vs Italy.
Key: Ermedin Demirović (Stuttgart), Sead Kolašinac (Atalanta), Amar Dedić (Benfica).
Miralem Pjanić NOT selected — retired from international football.
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 8, 10
T1G, T1K = 80.0, 0
T2G, T2K = 62.0, 0
T3G, T3K = 28.0, 0
T4G, T4K = 7.0,  0

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Nikola Vasilj', position='GK', sub_position='', club='FC St. Pauli', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FC St. Pauli GK (Bundesliga); Bosnia undisputed No.1; Bundesliga experience brings top quality; '
               'commanding presence; experienced in high-pressure European matches; key for Group B campaign',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; FC St. Pauli Bundesliga', tier_revised='GK1'),
    dict(player='Martin Zlomislić', position='GK', sub_position='', club='HNK Rijeka', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='HNK Rijeka GK (Croatia); Bosnia No.2 keeper; Croatian Prva HNL experience; backup behind Vasilj; '
               'no starts expected in group stage',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; HNK Rijeka Croatian Prva HNL', tier_revised='GK2'),
    dict(player='Osman Hadžikić', position='GK', sub_position='', club='Slaven Belupo', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Slaven Belupo GK (Croatia); Bosnia third-choice keeper; Croatian HNL domestic level; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Slaven Belupo Croatian HNL', tier_revised='GK3'),
    # Defenders
    dict(player='Sead Kolašinac', position='DEF', sub_position='LB', club='Atalanta', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atalanta LB (Serie A); Bosnia veteran left-back; only player alongside Džeko remaining from 2014 WC squad; '
               'Premier League (Arsenal) and Serie A experience; physical and combative LB; key leader for Group B',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; Atalanta Serie A', tier_revised='1'),
    dict(player='Amar Dedić', position='DEF', sub_position='RB', club='SL Benfica', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='SL Benfica RB (Portugal); Bosnia first-choice right-back; Primeira Liga and Champions League quality; '
               'dynamic, attacking fullback; one of Bosnia\'s most prestigious club players',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; SL Benfica Primeira Liga', tier_revised='1'),
    dict(player='Tarik Muharemović', position='DEF', sub_position='CB', club='US Sassuolo', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='US Sassuolo CB (Serie B); Bosnia first-choice centre-back; commanding and composed; Serie B experience; '
               'key defensive pillar of Barbarez\'s system',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; US Sassuolo Serie B', tier_revised='1'),
    dict(player='Dennis Hadžikadunić', position='DEF', sub_position='CB', club='UC Sampdoria', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='UC Sampdoria CB (Serie B); Bosnia regular centre-back partner; physical and aerial presence; '
               'Italian league experience; part of Bosnia\'s defensive setup for Group B',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; UC Sampdoria Serie B', tier_revised='1'),
    dict(player='Nidal Čelik', position='DEF', sub_position='CB', club='RC Lens', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='RC Lens CB (Ligue 1); Bosnia rotation CB; Ligue 1 quality brings depth; squad rotation alongside Muharemović',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; RC Lens Ligue 1', tier_revised='2'),
    dict(player='Nikola Katić', position='DEF', sub_position='CB', club='Schalke 04', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Schalke 04 CB (Germany 2. Bundesliga); Bosnia defensive rotation; 2. Bundesliga experience; '
               'squad depth behind the starting CB pairing',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Schalke 04 2. Bundesliga', tier_revised='2'),
    dict(player='Nihad Mujakić', position='DEF', sub_position='FB', club='Gaziantep FK', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Gaziantep FK FB (Turkey); Bosnia fullback depth option; Süper Lig experience; limited WC minutes expected',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='FB depth; Gaziantep FK Süper Lig', tier_revised='3'),
    dict(player='Stjepan Radeljić', position='DEF', sub_position='LB', club='HNK Rijeka', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='HNK Rijeka LB (Croatia); Bosnia left-back fringe option; Croatian Prva HNL; limited WC minutes expected',
         int_l5_pattern='DNP/sub/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='LB depth; HNK Rijeka Croatian Prva HNL', tier_revised='3'),
    # Midfielders
    dict(player='Esmir Bajraktarević', position='MID', sub_position='WNG', club='PSV Eindhoven', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='PSV Eindhoven WNG (Eredivisie); Bosnia star winger (21yo); scored decisive penalty vs Italy in WC playoff final; '
               'dazzling direct winger with exceptional pace and skill; PSV Eredivisie quality; '
               'Bosnia\'s most exciting young talent and the hero of qualification',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Bosnia star; WC qualification hero; PSV Eindhoven Eredivisie', tier_revised='1'),
    dict(player='Amir Hadžiahmetović', position='MID', sub_position='CM', club='Hull City', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hull City CM (Championship); Bosnia midfield engine; Championship experience; energetic and combative; '
               'key in centre of park; drives play forward from deep',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CM; Hull City Championship', tier_revised='1'),
    dict(player='Kerim Alajbegović', position='MID', sub_position='AM', club='RB Salzburg', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='RB Salzburg AM (Austria Bundesliga / Champions League); Bosnia creative attacking midfielder; '
               'quality from elite European football; key creative link between midfield and attack',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice AM; RB Salzburg Austrian Bundesliga', tier_revised='1'),
    dict(player='Benjamin Tahirović', position='MID', sub_position='CM', club='Brøndby IF', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Brøndby IF CM (Denmark); Bosnia midfield rotation; previously at Roma; Danish Superliga; '
               'technically proficient; squad rotation option in central midfield',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Brøndby IF Danish Superliga', tier_revised='2'),
    dict(player='Armin Gigović', position='MID', sub_position='CM', club='BSC Young Boys', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='BSC Young Boys CM (Switzerland); Bosnia midfield rotation; Swiss Super League quality; '
               'energetic squad option in central areas',
         int_l5_pattern='sub/90/sub/90/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; BSC Young Boys Swiss Super League', tier_revised='2'),
    dict(player='Ivan Šunjić', position='MID', sub_position='DM', club='Pafos FC', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Pafos FC DM (Cyprus); Bosnia defensive midfield option; previous Birmingham City Championship experience; '
               'disciplined holding midfielder; rotation option in pivot role',
         int_l5_pattern='sub/sub/90/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation DM; Pafos FC Cypriot First Division', tier_revised='2'),
    dict(player='Dženis Burnić', position='MID', sub_position='CM', club='Karlsruher SC', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Karlsruher SC CM (Germany 2. Bundesliga); Bosnia midfield squad depth; 2. Bundesliga quality; '
               'limited WC minutes expected',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; Karlsruher SC 2. Bundesliga', tier_revised='3'),
    dict(player='Ermin Mahmić', position='MID', sub_position='CM', club='FC Slovan Liberec', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FC Slovan Liberec CM (Czech Republic); Bosnia midfield fringe option; Czech league; limited WC minutes expected',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; FC Slovan Liberec Czech Fortuna Liga', tier_revised='3'),
    dict(player='Amar Memić', position='MID', sub_position='AM', club='FC Viktoria Plzen', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FC Viktoria Plzen AM (Czech Republic); Bosnia attacking midfield depth; Czech league; '
               'limited WC minutes expected',
         int_l5_pattern='sub/sub/DNP/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='AM depth; FC Viktoria Plzen Czech Fortuna Liga', tier_revised='3'),
    dict(player='Ivan Bašić', position='MID', sub_position='CM', club='FC Astana', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FC Astana CM (Kazakhstan); Bosnia midfield depth; Kazakhstan Premier League; squad padding; '
               'unlikely to feature unless squad rotation emergency',
         int_l5_pattern='DNP/sub/DNP/sub/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; FC Astana Kazakhstan Premier League', tier_revised='3'),
    # Forwards
    dict(player='Ermedin Demirović', position='FWD', sub_position='CF', club='VfB Stuttgart', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='VfB Stuttgart CF (Bundesliga); Bosnia primary striker; prolific Bundesliga scorer — highly regarded '
               'in German football; powerful and clinical; Bosnia\'s best and most dangerous striker; '
               'key to Bosnia\'s scoring ambitions in Group B',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Primary striker; undisputed T1; VfB Stuttgart Bundesliga', tier_revised='1'),
    dict(player='Edin Džeko', position='FWD', sub_position='CF', club='Schalke 04', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Schalke 04 CF (2. Bundesliga); Bosnia captain and all-time record goalscorer (63 goals, 40yo); '
               'two-time Premier League winner (Man City); veteran of 2014 WC; still selected by Barbarez as inspirational leader; '
               'physical target man; likely used as rotation/impact sub at 40 given age — not the T1 starter',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran captain rotation CF; 40yo; Schalke 04 2. Bundesliga', tier_revised='2'),
    dict(player='Haris Tabaković', position='FWD', sub_position='CF', club='Borussia Mönchengladbach', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Borussia Mönchengladbach CF (Bundesliga); Bosnia striker rotation; clinical finisher; '
               'Bundesliga experience; strong rotation option alongside Demirović',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CF; Borussia Mönchengladbach Bundesliga', tier_revised='2'),
    dict(player='Samed Baždar', position='FWD', sub_position='WNG', club='Jagiellonia Białystok', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Jagiellonia Białystok WNG (Poland Ekstraklasa); Bosnia wide forward depth; Polish league; '
               'limited WC minutes expected; squad padding',
         int_l5_pattern='sub/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='WNG depth; Jagiellonia Białystok Polish Ekstraklasa', tier_revised='3'),
    dict(player='Jovo Lukić', position='FWD', sub_position='CF', club='FC Universitatea Cluj', nationality='Bosnia', group='B',
         wc_squad_prob_pct=100, tier='4', playing_role='Fringe Player',
         group_mins_per_game=T4G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FC Universitatea Cluj CF (Romania); Bosnia forward fringe option; Romanian Superliga; '
               'minimal WC minutes anticipated; squad depth only',
         int_l5_pattern='DNP/DNP/sub/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CF; FC Universitatea Cluj Romanian Superliga', tier_revised='4'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Bosnia': continue
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
