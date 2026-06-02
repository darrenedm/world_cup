#!/usr/bin/env python3
"""
patch_uruguay_squad.py — official 26-man squad (Marcelo Bielsa, announced May 31 2026).
Group H: Spain(9.7), Uruguay(7.0), Saudi Arabia(3.0), Cape Verde(2.5).
Advance 52%, dead rubber G3 10%.
Key fitness: Rodrigo Bentancur (hamstring surgery Jan 2026; returned April; selected but doubtful
             for group-stage games — race against time for full fitness),
             Darwin Núñez (limited club minutes at Al-Hilal since Feb; still trusted by Bielsa),
             Ronald Araújo (injury-disrupted Barcelona season; fit for tournament).
Notable: Luis Suárez omitted for first time since 2010; Fernando Muslera (39) pulled out of
         retirement for record fifth Uruguayan WC; José María Giménez captain (99 caps).
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 52, 10
T1G, T1K = 87.1, 53
T2G, T2K = 74.0, 43
T3G, T3K = 42.0, 31
T4G, T4K = 16.0, 9

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Sergio Rochet', position='GK', sub_position='', club='Internacional', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Internacional GK; Uruguay undisputed No.1; reliable and commanding shot-stopper; '
               'consistent performer in Brazilian Série A; first-choice throughout qualifying.',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed No.1; Internacional Série A Brazil', tier_revised='GK1'),
    dict(player='Fernando Muslera', position='GK', sub_position='', club='Estudiantes', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=1,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Estudiantes GK; legendary 39-year-old veteran pulled out of retirement by Bielsa; '
               'record fifth World Cup for a Uruguayan; backup role only, no starts expected.',
         int_l5_pattern='90/90/DNP/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran backup; Estudiantes Argentine Primera', tier_revised='GK2'),
    dict(player='Santiago Mele', position='GK', sub_position='', club='Monterrey', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Monterrey GK; third-choice goalkeeper; no WC minutes expected; performing in Liga MX '
               'with Mexican club Monterrey.',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Monterrey Liga MX', tier_revised='GK3'),
    # Defenders
    dict(player='Ronald Araújo', position='DEF', sub_position='CB', club='Barcelona', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Barcelona CB; Uruguay elite centre-back; injury-disrupted Barcelona season but fit for tournament; '
               'powerful, aggressive, and dominant in the air; one of Europe\'s best defenders when fully fit.',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='Injury-disrupted 2025-26 season at Barca',
         fitness_current='Fit; injury-disrupted season but returned and fit for WC', tier_revised='1'),
    dict(player='José María Giménez', position='DEF', sub_position='CB', club='Atlético Madrid', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atlético Madrid CB; Uruguay captain with 99 caps; fierce leader and commanding presence; '
               'La Liga champion with Atleti; the defensive anchor around whom Bielsa builds.',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain, first-choice CB; Atlético Madrid La Liga', tier_revised='1'),
    dict(player='Mathías Olivera', position='DEF', sub_position='LB', club='Napoli', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Napoli LB; Uruguay first-choice left-back; dynamic and offensive-minded; excellent Serie A '
               'season; key weapon in wide areas under Bielsa\'s high-intensity pressing system.',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; Napoli Serie A', tier_revised='1'),
    dict(player='Guillermo Varela', position='DEF', sub_position='RB', club='Flamengo', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Flamengo RB; Uruguay right-back option; experienced Brasileirão performer; '
               'solid and dependable in the defensive phase with ability to contribute going forward.',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular RB; Flamengo Série A Brazil', tier_revised='2'),
    dict(player='Santiago Bueno', position='DEF', sub_position='CB', club='Wolverhampton Wanderers', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Wolverhampton CB; solid Premier League defender; third-choice CB who can step in; '
               'physical and reliable defensive option behind Araújo and J.M. Giménez.',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB rotation; Wolves Premier League', tier_revised='2'),
    dict(player='Joaquín Piquerez', position='DEF', sub_position='LB', club='Palmeiras', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Palmeiras LB; backup left-back option; Brazilian Série A regular with Palmeiras; '
               'cover behind Olivera; solid and experienced squad option.',
         int_l5_pattern='90/sub/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup LB; Palmeiras Série A Brazil', tier_revised='3'),
    dict(player='Sebastián Cáceres', position='DEF', sub_position='CB', club='Club América', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Club América CB; defensive depth from Liga MX; fourth-choice centre-back providing cover; '
               'fringe squad selection with limited WC minutes expected.',
         int_l5_pattern='sub/90/sub/DNP/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB depth; Club América Liga MX', tier_revised='3'),
    dict(player='Matías Viña', position='DEF', sub_position='LB', club='River Plate', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='4', playing_role='Fringe',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='River Plate LB; third LB option in the squad; returned to River Plate in Argentina; '
               'fringe selection as extra defensive cover, minimal WC minutes expected.',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe LB depth; River Plate Argentine Primera', tier_revised='4'),
    # Midfielders
    dict(player='Federico Valverde', position='MID', sub_position='CM', club='Real Madrid', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Real Madrid CM; Uruguay\'s best player and one of the world\'s elite midfielders; '
               'tireless engine with power, technique, and goals; cornerstone of Bielsa\'s system.',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Uruguay talisman; Real Madrid La Liga', tier_revised='1'),
    dict(player='Manuel Ugarte', position='MID', sub_position='DM', club='Manchester United', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Manchester United DM; tenacious defensive midfielder who dominates the midfield battle; '
               'elite ball-winner and pressing machine; Bielsa\'s first-choice defensive anchor.',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice DM; Manchester United Premier League', tier_revised='1'),
    dict(player='Giorgian de Arrascaeta', position='MID', sub_position='AM', club='Flamengo', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Flamengo AM; Uruguay\'s creative playmaker; exceptional technical quality, vision, and '
               'goal threat from midfield; one of South America\'s most influential players.',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice AM; Flamengo Série A Brazil', tier_revised='1'),
    dict(player='Rodrigo Bentancur', position='MID', sub_position='CM', club='Tottenham Hotspur', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='Tottenham CM; key box-to-box midfielder; hamstring surgery January 2026; returned April with '
               'faster-than-expected recovery; selected by Bielsa but fitness for group games still doubtful; '
               'critical player if available.',
         int_l5_pattern='90/DNP/DNP/sub/sub', int_l5_starts=1, int_absence_reason='Hamstring surgery Jan 2026; returned April',
         fitness_current='Doubtful; hamstring surgery Jan; returned April; fitness race for group stage', tier_revised='2'),
    dict(player='Nicolás de la Cruz', position='MID', sub_position='CM', club='Flamengo', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Flamengo CM; technical and creative central midfielder; strong vision and passing ability; '
               'regular Uruguay international who can also play more advanced; rotation and backup for Bentancur.',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM; Flamengo Série A Brazil', tier_revised='2'),
    dict(player='Maximiliano Araújo', position='MID', sub_position='WNG', club='Sporting CP', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Sporting CP WNG; electric left winger with pace and directness; outstanding Primeira Liga '
               'season with Sporting; key wide threat and rotation starter in Uruguay\'s attack.',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular WNG; Sporting CP Primeira Liga Portugal', tier_revised='2'),
    dict(player='Facundo Pellistri', position='MID', sub_position='WNG', club='Panathinaikos', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Panathinaikos WNG; pacey right winger who moved to Greece after leaving Manchester United; '
               'direct and capable wide attacker; squad rotation behind Maximiliano Araújo.',
         int_l5_pattern='90/sub/90/sub/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='WNG rotation; Panathinaikos Super League Greece', tier_revised='3'),
    dict(player='Brian Rodríguez', position='MID', sub_position='WNG', club='Club América', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Club América WNG; direct and pacey left winger; solid Liga MX performer; squad depth option '
               'on the wide left as impact sub or rotation starter.',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='WNG squad player; Club América Liga MX', tier_revised='3'),
    dict(player='Emiliano Martínez', position='MID', sub_position='CM', club='Palmeiras', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Palmeiras CM; solid central midfielder providing depth and competition in the engine room; '
               'Brazilian Série A regular; backup option behind Valverde-Ugarte-De Arrascaeta axis.',
         int_l5_pattern='sub/90/sub/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM squad depth; Palmeiras Série A Brazil', tier_revised='3'),
    dict(player='Agustín Canobbio', position='MID', sub_position='WNG', club='Fluminense', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Fluminense WNG; versatile wide midfielder who can play both wings; solid Brazilian Série A '
               'performer; squad depth option providing cover across the attacking line.',
         int_l5_pattern='sub/sub/90/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='WNG squad depth; Fluminense Série A Brazil', tier_revised='3'),
    dict(player='Rodrigo Zalazar', position='MID', sub_position='CM', club='Braga', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='4', playing_role='Fringe',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Braga CM; energetic central midfielder performing in the Portuguese Primeira Liga; '
               'fringe squad selection with limited WC minutes expected.',
         int_l5_pattern='sub/90/sub/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CM depth; Braga Primeira Liga Portugal', tier_revised='4'),
    dict(player='Juan Manuel Sanabria', position='MID', sub_position='CM', club='Atlético San Luis', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='4', playing_role='Fringe',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atlético San Luis CM; defensive-minded midfielder based in Liga MX; fringe squad pick '
               'providing extra depth; minimal WC minutes expected.',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CM depth; Atlético San Luis Liga MX', tier_revised='4'),
    # Forwards
    dict(player='Darwin Núñez', position='FWD', sub_position='CF', club='Al-Hilal', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='Al-Hilal CF; Uruguay\'s leading striker and top qualifier scorer (5 goals); has not featured '
               'for Al-Hilal since February 2026; significant fitness concern despite Bielsa\'s trust; '
               'physical presence and pace remain a major threat when fit.',
         int_l5_pattern='90/DNP/DNP/DNP/DNP', int_l5_starts=1, int_absence_reason='No club appearances since Feb 2026 (Al-Hilal)',
         fitness_current='Doubtful; no Al-Hilal appearances since Feb 2026; fitness concern', tier_revised='1'),
    dict(player='Rodrigo Aguirre', position='FWD', sub_position='CF', club='UANL Tigres', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='UANL Tigres CF; clinical finisher performing well in Liga MX; second-choice striker who steps '
               'up as Darwin Núñez cover; could get significant minutes if Núñez is not fully fit.',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup CF; UANL Tigres Liga MX', tier_revised='3'),
    dict(player='Federico Viñas', position='FWD', sub_position='CF', club='Real Oviedo', nationality='Uruguay', group='H',
         wc_squad_prob_pct=100, tier='4', playing_role='Fringe',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Real Oviedo CF; third-choice striker performing in Spain\'s Segunda División; fringe selection '
               'providing cover behind Núñez and R.Aguirre; minimal WC minutes expected.',
         int_l5_pattern='sub/90/sub/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe third CF; Real Oviedo Segunda División Spain', tier_revised='4'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Uruguay': continue
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
