#!/usr/bin/env python3
"""
patch_paraguay_squad.py — official 26-man squad (Gustavo Alfaro, announced June 1 2026).
Group D: USA(7.1), Turkey(5.8), Australia(5.6), Paraguay(4.6).
Advance 20%, dead rubber G3 10%.
KEY NOTES: Captain Gustavo Gomez (Palmeiras, 88 caps) anchors a well-travelled squad —
7 players from Brazil, 6 from Argentina, only 3 from domestic Paraguayan league.
Julio Enciso (Strasbourg) and Miguel Almiron (Atlanta United) lead attack.
Notable exclusions: Angel Romero, Mathias Villasanti (ACL), Lucas Romero all cut.
Isidro Pitta (Red Bull Bragantino) claimed final squad spot. 'Gatito' Fernandez
(Roberto Jr. Fernandez, Cerro Porteno) is first-choice GK.
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 20, 10
T1G, T1K = 87.1, 4
T2G, T2K = 74.0, 3
T3G, T3K = 42.0, 2
T4G, T4K = 16.0, 1

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Roberto Fernandez', position='GK', sub_position='', club='Cerro Porteno', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Cerro Porteno GK; Paraguay No.1 nicknamed Gatito; experienced international; reliable shot-stopper; domestic Paraguayan League',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed No.1; Cerro Porteno Paraguayan Division Profesional', tier_revised='GK1'),
    dict(player='Orlando Gill', position='GK', sub_position='', club='San Lorenzo', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=1,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='San Lorenzo GK; Paraguay No.2; Argentine Primera Division; backup cover; no starts expected',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; San Lorenzo Argentine Primera', tier_revised='GK2'),
    dict(player='Gaston Olveira', position='GK', sub_position='', club='Club Olimpia', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Club Olimpia GK; Paraguay No.3; selected based on recent form; no WC minutes expected; new call-up',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Club Olimpia Paraguayan Division Profesional', tier_revised='GK3'),
    # Defenders
    dict(player='Gustavo Gomez', position='DEF', sub_position='CB', club='Palmeiras', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Palmeiras CB; Paraguay captain; 88 caps; dominant and commanding; Serie A Brazil; strongest and most experienced defender; set-piece threat',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain; first-choice CB; Palmeiras Série A Brazil', tier_revised='1'),
    dict(player='Junior Alonso', position='DEF', sub_position='CB', club='Atletico Mineiro', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atletico Mineiro CB; Paraguay regular starter; strong Brazilian Série A performer; forms first-choice CB pairing with Gomez',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Atletico Mineiro Série A Brazil', tier_revised='1'),
    dict(player='Fabian Balbuena', position='DEF', sub_position='CB', club='Gremio', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Gremio CB; Paraguay experienced veteran; former West Ham and Norwich; Brazilian Série A; rotation behind main CB pairing',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran rotation CB; Gremio Série A Brazil', tier_revised='2'),
    dict(player='Omar Alderete', position='DEF', sub_position='CB', club='Sunderland', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Sunderland CB; Paraguay rotation centre-back; English Championship; versatile and physical; squad depth behind Gomez/Alonso',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Sunderland Championship England', tier_revised='2'),
    dict(player='Juan Caceres', position='DEF', sub_position='RB', club='Dynamo Moscow', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Dynamo Moscow RB; Paraguay first-choice right-back; Russian Premier League; energetic and experienced going forward',
         int_l5_pattern='90/90/sub/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; Dynamo Moscow Russian Premier League', tier_revised='2'),
    dict(player='Gustavo Velazquez', position='DEF', sub_position='LB', club='Cerro Porteno', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Cerro Porteno LB; Paraguay regular left-back option; domestic league performer; solid and reliable',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular LB; Cerro Porteno Paraguayan Division Profesional', tier_revised='2'),
    dict(player='Jose Canale', position='DEF', sub_position='CB', club='Lanus', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Lanus CB; Paraguay new call-up selected on recent form; Argentine Primera; missed qualification but good current form',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='New call-up CB; Lanus Argentine Primera', tier_revised='3'),
    dict(player='Alexandro Maidana', position='DEF', sub_position='LB', club='Talleres', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Talleres LB; Paraguay new call-up; Argentine Primera; missed qualification; named on current form; defensive depth',
         int_l5_pattern='sub/DNP/DNP/90/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='New call-up LB; Talleres Argentine Primera', tier_revised='3'),
    # Midfielders
    dict(player='Diego Gomez', position='MID', sub_position='CM', club='Brighton & Hove Albion', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Brighton CM; Paraguay best young midfielder; Premier League quality; technical and creative; key midfield component',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key CM; Brighton PL', tier_revised='1'),
    dict(player='Andres Cubas', position='MID', sub_position='DM', club='Vancouver Whitecaps', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Vancouver Whitecaps DM; Paraguay midfield anchor; MLS; combative and disciplined; screens defence; regular starter',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Midfield anchor DM; Vancouver Whitecaps MLS', tier_revised='1'),
    dict(player='Damian Bobadilla', position='MID', sub_position='CM', club='Sao Paulo', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Sao Paulo CM; Paraguay rotation midfielder; Brazilian Série A; energetic and contributing; reliable midfield option',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Sao Paulo Série A Brazil', tier_revised='2'),
    dict(player='Matias Galarza', position='MID', sub_position='CM', club='Atlanta United', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atlanta United CM; Paraguay young creative midfielder; MLS; recently returned to River Plate on loan; rotation midfield option',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young rotation CM; Atlanta United MLS', tier_revised='2'),
    dict(player='Alejandro Romero Gamarra', position='MID', sub_position='AM', club='Al Ain', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al Ain (UAE) AM; Paraguay nicknamed Kaku; creative attacking midfielder; UAE Pro League; rotation and link-up between midfield and attack',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation AM; Al Ain UAE Pro League', tier_revised='2'),
    dict(player='Braian Ojeda', position='MID', sub_position='DM', club='Orlando City', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Orlando City DM; Paraguay squad midfielder; MLS; depth cover in defensive midfield; limited WC minutes expected',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth DM; Orlando City MLS', tier_revised='3'),
    dict(player='Mauricio Magalhaes', position='MID', sub_position='CM', club='Palmeiras', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Palmeiras CM; Paraguay new call-up based on recent form; Brazilian Série A; missed qualification but earned squad spot; depth cover',
         int_l5_pattern='sub/DNP/DNP/90/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='New call-up depth CM; Palmeiras Série A Brazil', tier_revised='3'),
    # Forwards
    dict(player='Miguel Almiron', position='FWD', sub_position='WNG', club='Atlanta United', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atlanta United WNG; Paraguay marquee attacker; former Newcastle; MLS; direct, pacey and creative; key to Paraguay\'s attacking play',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Star WNG; Atlanta United MLS', tier_revised='1'),
    dict(player='Julio Enciso', position='FWD', sub_position='WNG', club='Strasbourg', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Strasbourg WNG; Paraguay exciting young attacker; former Brighton; Ligue 1; technical and goal-scoring; major tournament threat',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key young WNG; Strasbourg Ligue 1', tier_revised='1'),
    dict(player='Ramon Sosa', position='FWD', sub_position='WNG', club='Palmeiras', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Palmeiras WNG; Paraguay rotation winger; Brazilian Série A; direct and pacey; rotation cover behind Almiron/Enciso on the flanks',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation WNG; Palmeiras Série A Brazil', tier_revised='2'),
    dict(player='Antonio Sanabria', position='FWD', sub_position='CF', club='Cremonese', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Cremonese CF; Paraguay experienced striker; former Torino; Italian Serie B; physical and aerial threat; rotation striker option',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CF; Cremonese Serie B Italy', tier_revised='2'),
    dict(player='Alex Arce', position='FWD', sub_position='CF', club='Independiente Rivadavia', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Independiente Rivadavia CF; Paraguay squad striker; Argentine Primera; domestic scorer; depth option up front',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CF; Independiente Rivadavia Argentine Primera', tier_revised='3'),
    dict(player='Gabriel Avalos', position='FWD', sub_position='CF', club='Independiente', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Independiente CF; Paraguay squad striker; Argentine Primera; physical presence up front; limited WC minutes anticipated',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CF; Independiente Argentine Primera', tier_revised='3'),
    dict(player='Gustavo Caballero', position='FWD', sub_position='WNG', club='Portsmouth', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Portsmouth WNG; Paraguay new call-up based on recent form; English Championship; missed qualification; squad depth wide cover',
         int_l5_pattern='sub/DNP/DNP/90/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='New call-up depth WNG; Portsmouth Championship England', tier_revised='3'),
    dict(player='Isidro Pitta', position='FWD', sub_position='CF', club='Red Bull Bragantino', nationality='Paraguay', group='D',
         wc_squad_prob_pct=100, tier='4', playing_role='Squad Player',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Red Bull Bragantino CF; Paraguay last squad spot winner; Brazilian Série A; pipped Angel Romero for final spot; limited WC role',
         int_l5_pattern='sub/DNP/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CF; Red Bull Bragantino Série A Brazil', tier_revised='4'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Paraguay': continue
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
