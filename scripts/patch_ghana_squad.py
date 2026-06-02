#!/usr/bin/env python3
"""
patch_ghana_squad.py — official 26-man squad (Carlos Queiroz, announced June 1 2026).
Group L: England(9.3), Croatia(7.4), Panama(5.3), Ghana(2.1).
Advance 5%, dead rubber G3 10%.
Captain: Jordan Ayew (Leicester City, 133 caps — Ghana all-time record).
Star: Antoine Semenyo (Manchester City); Thomas Partey (Villarreal) key in midfield.
KEY ABSENCES: Mohammed Kudus (Tottenham) — quad injury requiring surgery; Andre Ayew — not selected.
15 debutants in the 26-man squad. Squad heavy with overseas-based players.
Group: Panama (June 17 Toronto), England (June 23 Foxborough), Croatia (June 27 Philadelphia).
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 5, 10
T1G, T1K = 78.0, 0
T2G, T2K = 60.0, 0
T3G, T3K = 25.0, 0
T4G, T4K = 5.0,  0

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Lawrence Ati-Zigi', position='GK', sub_position='', club='St. Gallen', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='St. Gallen GK (Swiss Super League); Ghana undisputed No.1; consistent performer in Switzerland; '
               'excellent shot-stopper; leads GK department for Group L campaign',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; St. Gallen Swiss Super League', tier_revised='GK1'),
    dict(player='Joseph Anang', position='GK', sub_position='', club='St. Patrick\'s Athletic', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='St. Patrick\'s Athletic GK (Ireland); Ghana No.2 keeper; League of Ireland experience; backup behind Ati-Zigi',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; St. Patrick\'s Athletic League of Ireland', tier_revised='GK2'),
    dict(player='Benjamin Asare', position='GK', sub_position='', club='Accra Hearts of Oak', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Accra Hearts of Oak GK (Ghana); domestic-based third keeper; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Accra Hearts of Oak Ghana Premier League', tier_revised='GK3'),
    # Defenders
    dict(player='Alidu Seidu', position='DEF', sub_position='RB', club='Rennes', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Rennes RB (Ligue 1); Ghana first-choice right-back; quick and aggressive; Ligue 1 quality; '
               'previously at Clermont; key in Ghana\'s defensive structure',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; Rennes Ligue 1', tier_revised='1'),
    dict(player='Gideon Mensah', position='DEF', sub_position='LB', club='Auxerre', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Auxerre LB (Ligue 1); Ghana first-choice left-back; attacking and energetic; Ligue 1 quality; '
               'important in wide areas for Ghana\'s attacking play',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; Auxerre Ligue 1', tier_revised='1'),
    dict(player='Abdul Mumin', position='DEF', sub_position='CB', club='Rayo Vallecano', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Rayo Vallecano CB (La Liga); Ghana first-choice centre-back; La Liga experience; commanding in the air; '
               'key defensive leader following Aidoo injury absence',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Rayo Vallecano La Liga', tier_revised='1'),
    dict(player='Baba Abdul Rahman', position='DEF', sub_position='LB', club='PAOK', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='PAOK LB (Greek Super League); Ghana veteran left-back returning after 3-year absence from national team; '
               'former Chelsea player; physical and experienced; welcome return adds depth',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation LB/veteran return; PAOK Greek Super League', tier_revised='1'),
    dict(player='Jerome Opoku', position='DEF', sub_position='CB', club='Istanbul Basaksehir', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Istanbul Basaksehir CB (Süper Lig); Ghana rotation centre-back; Turkish Süper Lig experience; '
               'squad depth option to cover Mumin',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Istanbul Basaksehir Süper Lig', tier_revised='2'),
    dict(player='Marvin Senaya', position='DEF', sub_position='CB', club='Auxerre', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Auxerre CB (Ligue 1); Ghana defensive rotation; Ligue 1 experience; rotation option in central defence',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Auxerre Ligue 1', tier_revised='2'),
    dict(player='Derrick Luckassen', position='DEF', sub_position='CB', club='Pafos', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Pafos CB (Cyprus); Ghana defensive squad depth; Cypriot First Division experience; rotation option',
         int_l5_pattern='sub/sub/90/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Pafos Cypriot First Division', tier_revised='2'),
    dict(player='Jonas Adjetey', position='DEF', sub_position='RB', club='VfL Wolfsburg', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='VfL Wolfsburg RB (Bundesliga); Ghana right-back depth; Bundesliga quality; squad depth option',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='RB depth; VfL Wolfsburg Bundesliga', tier_revised='3'),
    dict(player='Kojo Oppong Peprah', position='DEF', sub_position='CB', club='OGC Nice', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='OGC Nice CB (Ligue 1); Ghana defensive fringe option; Ligue 1 quality but limited WC minutes expected',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB depth; OGC Nice Ligue 1', tier_revised='3'),
    # Midfielders
    dict(player='Thomas Partey', position='MID', sub_position='DM', club='Villarreal', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Villarreal DM (La Liga); Ghana midfield anchor and key experienced midfielder; former Arsenal star; '
               'La Liga experience; dominant defensive midfielder who dictates tempo; '
               'Ghana\'s most experienced and important midfield player',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Ghana midfield anchor; undisputed T1; Villarreal La Liga', tier_revised='1'),
    dict(player='Kamaldeen Sulemana', position='MID', sub_position='WNG', club='Atalanta', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atalanta WNG (Serie A); Ghana pacy and direct winger; previously Southampton and Rennes; '
               'Serie A quality; exciting attacking threat from wide; key in wide areas with Kudus absent',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice WNG; Atalanta Serie A', tier_revised='1'),
    dict(player='Abdul Fatawu', position='MID', sub_position='WNG', club='Leicester City', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Leicester City WNG (Championship); Ghana key winger; excellent 2024-25 season at Leicester; '
               'direct and quick from wide; one of Ghana\'s prime attacking outlets in Group L',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice WNG; Leicester City Championship', tier_revised='1'),
    dict(player='Elisha Owusu', position='MID', sub_position='DM', club='Auxerre', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Auxerre DM (Ligue 1); Ghana midfield rotation; French-born Ghanaian; capable of playing alongside Partey; '
               'combative and physical holding midfielder',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation DM; Auxerre Ligue 1', tier_revised='2'),
    dict(player='Kwasi Sibo', position='MID', sub_position='CM', club='Real Oviedo', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Real Oviedo CM (Spain Segunda); Ghana midfield rotation; Spanish second-tier experience; '
               'energetic box-to-box option in central midfield',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Real Oviedo Spanish Segunda División', tier_revised='2'),
    dict(player='Augustine Boakye', position='MID', sub_position='WNG', club='Saint-Étienne', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Saint-Étienne WNG (Ligue 1); Ghana wide midfield depth; Ligue 1 experience; limited WC minutes expected',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='WNG depth; Saint-Étienne Ligue 1', tier_revised='3'),
    dict(player='Caleb Yirenkyi', position='MID', sub_position='CM', club='Nordsjaelland', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Nordsjaelland CM (Denmark); Ghana midfield fringe; Danish Superliga; limited WC minutes expected',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; Nordsjaelland Danish Superliga', tier_revised='3'),
    # Forwards
    dict(player='Jordan Ayew', position='FWD', sub_position='WNG', club='Leicester City', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Leicester City WNG/FWD (Championship); Ghana captain and all-time caps record holder (133 caps, 34yo); '
               'experienced leader and inspirational figure; clinical when given opportunities; '
               'son of Abedi Pele; third WC appearance; key leadership figure',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain, record caps; T1 starter; Leicester City Championship', tier_revised='1'),
    dict(player='Antoine Semenyo', position='FWD', sub_position='WNG', club='Manchester City', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Manchester City WNG (Premier League); Ghana headline star replacing injured Kudus as primary threat; '
               'exceptional 2024-25 Premier League season after move from Bournemouth; direct, pacy, clinical; '
               'Ghana\'s most dangerous player at this tournament',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Ghana star striker; undisputed T1; Manchester City Premier League', tier_revised='1'),
    dict(player='Iñaki Williams', position='FWD', sub_position='WNG', club='Athletic Club', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Athletic Club FWD (La Liga); Ghana attacking leader; switched from Spain national team; '
               'powerful and direct winger; La Liga quality; emotional and footballing leader of the squad; '
               'first WC appearance for Ghana; key attacking weapon',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Ghana attacking leader; undisputed T1; Athletic Club La Liga', tier_revised='1'),
    dict(player='Ernest Nuamah', position='FWD', sub_position='WNG', club='Lyon', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Lyon WNG (Ligue 1); Ghana pacy young forward; strong Ligue 1 season; rotation option from wide; '
               'one of the more exciting young forwards in the squad',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation WNG; Lyon Ligue 1', tier_revised='2'),
    dict(player='Christopher Bonsu Baah', position='FWD', sub_position='WNG', club='Al-Qadisiyah', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Qadisiyah WNG (Saudi Pro League); Ghana wide forward rotation; Saudi Pro League experience; '
               'useful attacking depth option',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation WNG; Al-Qadisiyah Saudi Pro League', tier_revised='2'),
    dict(player='Brandon Thomas-Asante', position='FWD', sub_position='CF', club='Coventry City', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Coventry City CF (Championship); Ghana striker depth; Championship experience; limited WC minutes expected',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CF depth; Coventry City Championship', tier_revised='3'),
    dict(player='Prince Kwabena Adu', position='FWD', sub_position='CF', club='Viktoria Plzen', nationality='Ghana', group='L',
         wc_squad_prob_pct=100, tier='4', playing_role='Fringe Player',
         group_mins_per_game=T4G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Viktoria Plzen CF (Czech Fortuna Liga); Ghana fringe forward; Czech league; minimal WC minutes expected',
         int_l5_pattern='DNP/DNP/sub/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CF; Viktoria Plzen Czech Fortuna Liga', tier_revised='4'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Ghana': continue
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
