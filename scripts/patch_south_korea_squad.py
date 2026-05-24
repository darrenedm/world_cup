#!/usr/bin/env python3
"""
patch_south_korea_squad.py
Sync South Korea rows with confirmed 26-man WC 2026 squad.
Announced by Hong Myung-bo on May 16, 2026.
Run ONCE, then re-run compute_pts_per_90.py to rebuild adj pts.
"""
import csv

PATH = '/tmp/world_cup_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

# Group A: Mexico(7.1), South Korea(5.9), Czech Republic(4.3), South Africa(2.9)
# Advance ~56%, dead rubber G3 ~22%
ADV = 56
DR  = 22

NEW_PLAYERS = [
    # ── Goalkeepers ──────────────────────────────────────────────────────
    dict(player='Jo Hyeon-woo', position='GK', sub_position='',
         club='Ulsan HD FC', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=144,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='South Korea No.1; Ulsan HD regular; experienced shot-stopper; '
               'strong WC pedigree; commanding on set pieces',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed No.1', tier_revised='GK1'),
    dict(player='Kim Seung-gyu', position='GK', sub_position='',
         club='FC Tokyo', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=8,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='South Korea No.2; FC Tokyo; veteran backup; no starts expected',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; J-League', tier_revised='GK2'),
    dict(player='Song Bum-keun', position='GK', sub_position='',
         club='Jeonbuk Hyundai Motors', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Jeonbuk GK; South Korea No.3; no WC minutes expected',
         int_l5_pattern='DNP/90/DNP/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; K-League', tier_revised='GK3'),
    # ── Defenders ────────────────────────────────────────────────────────
    dict(player='Kim Min-jae', position='DEF', sub_position='CB',
         club='Bayern Munich', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=78.0, exp_post_group_mins_total=140,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Bayern Munich CB; South Korea\'s best player (28); '
               'dominant aerial presence, incredible reading of the game; '
               'world-class CB; set-piece danger',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed No.1 CB; Bayern world-class', tier_revised='1'),
    dict(player='Kim Moon-hwan', position='DEF', sub_position='RB',
         club='Daejeon Hana Citizen FC', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=60.0, exp_post_group_mins_total=94,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Daejeon RB; regular right-back for South Korea; solid defensively; '
               'experienced international',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular RB starter; K-League form', tier_revised='2'),
    dict(player='Seol Young-woo', position='DEF', sub_position='CB',
         club='FK Crvena Zvezda', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=60.0, exp_post_group_mins_total=90,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Red Star Belgrade CB; physical and powerful; Kim Min-jae partner; '
               'good distribution from the back',
         int_l5_pattern='90/90/sub/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB partner to Kim Min-jae', tier_revised='2'),
    dict(player='Cho Yu-min', position='DEF', sub_position='LB',
         club='Sharjah FC', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=58.0, exp_post_group_mins_total=88,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Sharjah FC LB; first-choice Korea left-back; attack-minded; '
               'UAE Pro League experience',
         int_l5_pattern='90/90/DNP/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular LB starter; intl form solid', tier_revised='2'),
    dict(player='Jens Castrop', position='DEF', sub_position='CB',
         club='Borussia Mönchengladbach', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=38.0, exp_post_group_mins_total=42,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Gladbach CB; first dual-heritage (German-Korean) player called up; '
               'strong Bundesliga experience; squad CB rotation',
         int_l5_pattern='90/sub/90/DNP/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB rotation; Gladbach Bundesliga quality', tier_revised='3'),
    dict(player='Lee Han-beom', position='DEF', sub_position='LB',
         club='Midtjylland', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=36.0, exp_post_group_mins_total=38,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Midtjylland LB; squad cover for Cho Yu-min',
         int_l5_pattern='sub/90/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup LB; Danish Superliga', tier_revised='3'),
    dict(player='Kim Tae-hyeon', position='DEF', sub_position='CB',
         club='Kashima Antlers', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=34.0, exp_post_group_mins_total=36,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Kashima Antlers CB; squad depth; domestic-league selection',
         int_l5_pattern='90/DNP/sub/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CB; J-League selection', tier_revised='3'),
    dict(player='Lee Gi-hyuk', position='DEF', sub_position='RB',
         club='Gangwon FC', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=16.0, exp_post_group_mins_total=10,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Gangwon FC RB; fringe K-League selection; depth cover only',
         int_l5_pattern='sub/DNP/DNP/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe RB; K-League depth', tier_revised='4'),
    dict(player='Park Jin-seob', position='DEF', sub_position='CB',
         club='Zhejiang FC', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=14.0, exp_post_group_mins_total=8,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Zhejiang FC (China) CB; squad depth; minimal mins expected',
         int_l5_pattern='DNP/sub/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CB; Chinese league', tier_revised='4'),
    dict(player='Lee Tae-seok', position='DEF', sub_position='LB',
         club='Austria Wien', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=14.0, exp_post_group_mins_total=8,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Austria Wien LB; lower-tier European selection; depth cover',
         int_l5_pattern='sub/DNP/sub/DNP/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe LB; Austrian league depth', tier_revised='4'),
    # ── Midfielders ──────────────────────────────────────────────────────
    dict(player='Lee Kang-in', position='MID', sub_position='AM',
         club='Paris Saint-Germain', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=78.0, exp_post_group_mins_total=140,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='PSG AM; South Korea\'s most creative player; elite dribbler and chance creator; '
               'key attacking hub; regular starter under Hong',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key creative starter; PSG quality', tier_revised='1'),
    dict(player='Hwang Hee-chan', position='MID', sub_position='AM',
         club='Wolverhampton Wanderers', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=60.0, exp_post_group_mins_total=94,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Wolves winger/forward; pace and direct; clinical goal scorer; '
               'key attacking rotation; plays wide or as second striker',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular wide forward; Wolves PL form', tier_revised='2'),
    dict(player='Yang Hyun-jun', position='MID', sub_position='AM',
         club='Celtic FC', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=60.0, exp_post_group_mins_total=92,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Celtic winger; quick and direct; left-wing option; '
               'useful in wide positions for South Korea',
         int_l5_pattern='90/sub/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular left wing rotation; Celtic form', tier_revised='2'),
    dict(player='Hwang In-beom', position='MID', sub_position='CM',
         club='Feyenoord', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=58.0, exp_post_group_mins_total=88,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Feyenoord CM; energetic box-to-box; Eredivisie quality; '
               'regular Korean midfield anchor alongside Lee/Bae',
         int_l5_pattern='90/90/sub/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM; Feyenoord Eredivisie', tier_revised='2'),
    dict(player='Lee Jae-sung', position='MID', sub_position='CM',
         club='Mainz 05', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=56.0, exp_post_group_mins_total=86,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Mainz CM; experienced Korea international; technical and intelligent; '
               'key rotation in Korea\'s midfield',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM; Mainz Bundesliga form', tier_revised='2'),
    dict(player='Bae Jun-ho', position='MID', sub_position='CM',
         club='Stoke City', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=38.0, exp_post_group_mins_total=42,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Stoke City CM; energetic; Championship experience; squad depth',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM rotation; Championship squad level', tier_revised='3'),
    dict(player='Paik Seung-ho', position='MID', sub_position='DM',
         club='Birmingham City', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=36.0, exp_post_group_mins_total=38,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Birmingham City DM; defensive midfield cover; Championship',
         int_l5_pattern='90/sub/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='DM cover; Championship level', tier_revised='3'),
    dict(player='Eom Ji-sung', position='MID', sub_position='CM',
         club='Swansea City', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=34.0, exp_post_group_mins_total=36,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Swansea City CM; squad depth option; limited WC starts expected',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CM; Championship', tier_revised='3'),
    dict(player='Lee Dong-gyeong', position='MID', sub_position='CM',
         club='Ulsan HD FC', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=32.0, exp_post_group_mins_total=34,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Ulsan HD CM; K-League domestic selection; squad depth',
         int_l5_pattern='sub/DNP/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='K-League rotation; domestic depth', tier_revised='3'),
    dict(player='Kim Jin-gyu', position='MID', sub_position='CM',
         club='Jeonbuk Hyundai Motors', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=14.0, exp_post_group_mins_total=8,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Jeonbuk CM; K-League depth; minimal WC minutes expected',
         int_l5_pattern='DNP/sub/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='K-League depth only', tier_revised='4'),
    # ── Forwards ─────────────────────────────────────────────────────────
    dict(player='Son Heung-min', position='FWD', sub_position='',
         club='LAFC', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=78.0, exp_post_group_mins_total=140,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='LAFC (ex-Tottenham); South Korea captain; 4th World Cup; '
               '54 international goals; talismanic winger/striker; '
               'left Spurs for MLS but still world-class pace and finishing',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed captain and key attacker', tier_revised='1'),
    dict(player='Oh Hyeon-gyu', position='FWD', sub_position='',
         club='Besiktas', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=60.0, exp_post_group_mins_total=92,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Besiktas striker; 6 international goals; strong form in Turkish league; '
               'physical presence and clinical finisher; backup to Son',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular striker rotation; Besiktas form strong', tier_revised='2'),
    dict(player='Cho Gue-sung', position='FWD', sub_position='',
         club='Midtjylland', nationality='South Korea', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=58.0, exp_post_group_mins_total=88,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Midtjylland striker; 10 international goals; physical target man; '
               'WC 2022 brace scorer vs Ghana; aerial threat',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular striker rotation; aerial set-piece threat', tier_revised='2'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    updated = 0
    for row in rows:
        if row['nationality'] != 'South Korea':
            continue
        name = row['player']
        if name in NOT_SELECTED:
            row['wc_squad_prob_pct'] = '0'
            updated += 1
        elif name in CONFIRMED_IN:
            row['wc_squad_prob_pct'] = '100'
            updated += 1
        if name in CORRECTIONS:
            for k, v in CORRECTIONS[name].items():
                row[k] = str(v)

    blank_pts = {'action_pts_per_90': '0', 'exp_pts_per_90': '0',
                 'total_exp_fantasy_pts': '0', 'adj_exp_fantasy_pts': '0'}
    for p in NEW_PLAYERS:
        new_row = {k: '' for k in fieldnames}
        new_row.update(blank_pts)
        new_row.update({str(k): str(v) for k, v in p.items()})
        rows.append(new_row)
        print(f'  Added:    {p["player"]}')

    with open(PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f'\nDone — {updated} rows updated, {len(NEW_PLAYERS)} rows added. Total: {len(rows)}')


if __name__ == '__main__':
    main()
