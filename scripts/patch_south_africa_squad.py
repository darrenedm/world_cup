#!/usr/bin/env python3
"""
patch_south_africa_squad.py — official 26-man squad (Hugo Broos, announced May 27 2026).
Group A: Mexico(7.1), South Korea(5.9), Czech Republic(4.3), South Africa(2.9).
Advance 14%, dead rubber G3 10%.
19 of 26 players from PSL (domestic). Sundowns and Pirates have 8 players each.
Key fitness: Thapelo Maseko (returning from 2-year competitive absence, limited game time),
             Themba Zwane (age/fitness managed, cannot do full 90 regularly).
Notable absences: Thapelo Morena (injured), Sipho Mbule (injured), Mohau Nkota (injured).
Ronwen Williams captain — famous for 4 penalty saves in single AFCON shootout (2023).
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 14, 10
T1G, T1K = 85.0, 2
T2G, T2K = 68.0, 2
T3G, T3K = 35.0, 1
T4G, T4K = 10.0, 0

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Ronwen Williams', position='GK', sub_position='', club='Mamelodi Sundowns', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=2,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Mamelodi Sundowns GK; South Africa captain and best player; world-class penalty stopper — '
               'saved 4 penalties in single AFCON 2023 shootout; vocal leader and commanding presence',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain GK; Mamelodi Sundowns DSTV Premiership', tier_revised='GK1'),
    dict(player='Sipho Chaine', position='GK', sub_position='', club='Orlando Pirates', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=1,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Orlando Pirates GK; South Africa No.2; PSL quality; reliable backup; no WC starts expected',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Orlando Pirates DSTV Premiership', tier_revised='GK2'),
    dict(player='Ricardo Goss', position='GK', sub_position='', club='Siwelele FC', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Siwelele FC GK (loan from Sundowns); South Africa No.3; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Siwelele FC DSTV Premiership', tier_revised='GK3'),
    # Defenders
    dict(player='Khuliso Mudau', position='DEF', sub_position='RB', club='Mamelodi Sundowns', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Mamelodi Sundowns RB; South Africa first-choice right-back; aggressive and energetic; AFCON experience',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; Sundowns DSTV Premiership', tier_revised='1'),
    dict(player='Aubrey Modiba', position='DEF', sub_position='LB', club='Mamelodi Sundowns', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Mamelodi Sundowns LB; South Africa regular left-back; attack-minded and dynamic; key in wide areas',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; Sundowns DSTV Premiership', tier_revised='1'),
    dict(player='Nkosinathi Sibisi', position='DEF', sub_position='CB', club='Orlando Pirates', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Orlando Pirates CB; South Africa first-choice centre-back; physical and commanding; PSL elite level',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Orlando Pirates DSTV Premiership', tier_revised='1'),
    dict(player='Mbekezeli Mbokazi', position='DEF', sub_position='CB', club='Chicago Fire', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Chicago Fire CB; South Africa first-choice second CB; MLS experience; strong in the air; partners Sibisi',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Chicago Fire MLS', tier_revised='1'),
    dict(player='Ime Okon', position='DEF', sub_position='CB', club='Hannover 96', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hannover 96 CB; South Africa rotation centre-back; Bundesliga 2 quality; reliable defensive cover',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Hannover 96 Bundesliga 2', tier_revised='2'),
    dict(player='Khulumani Ndamane', position='DEF', sub_position='RB', club='Mamelodi Sundowns', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Mamelodi Sundowns RB/RWB; South Africa rotation right-back; energetic and attacking; covers Mudau',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation RB; Sundowns DSTV Premiership', tier_revised='2'),
    dict(player='Samukele Kabini', position='DEF', sub_position='CB', club='Molde FK', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Molde FK CB; South Africa rotation CB; Norwegian Eliteserien quality; solid squad depth',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Molde FK Eliteserien', tier_revised='2'),
    dict(player='Thabang Matuludi', position='DEF', sub_position='CB', club='Polokwane City', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Polokwane City CB; South Africa rotation CB; domestic stalwart; squad cover option',
         int_l5_pattern='90/sub/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Polokwane City DSTV Premiership', tier_revised='2'),
    dict(player='Bradley Cross', position='DEF', sub_position='CB', club='Kaizer Chiefs', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Kaizer Chiefs CB; South Africa uncapped squad player; domestic talent; limited WC minutes expected',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Uncapped CB depth; Kaizer Chiefs DSTV Premiership', tier_revised='3'),
    dict(player='Olwethu Makhanya', position='DEF', sub_position='LB', club='Philadelphia Union', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Philadelphia Union LB; South Africa uncapped left-back; MLS-based; fringe squad selection',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Uncapped LB depth; Philadelphia Union MLS', tier_revised='3'),
    dict(player='Kamogelo Sebelebele', position='DEF', sub_position='CB', club='Orlando Pirates', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Orlando Pirates CB/DM; South Africa versatile squad player; domestic stalwart; depth option',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Versatile depth; Orlando Pirates DSTV Premiership', tier_revised='3'),
    # Midfielders
    dict(player='Teboho Mokoena', position='MID', sub_position='CM', club='Mamelodi Sundowns', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Mamelodi Sundowns CM; South Africa midfield engine; energetic and combative; key in pressing and ball-winning',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key starter CM; Sundowns DSTV Premiership', tier_revised='1'),
    dict(player='Relebohile Mofokeng', position='MID', sub_position='WNG', club='Orlando Pirates', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Orlando Pirates WNG; South Africa most highly rated young player; electric winger; direct dribbler; '
               'key attacking threat expected to make impact on big stage at WC 2026',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Star young winger; Orlando Pirates DSTV Premiership', tier_revised='1'),
    dict(player='Oswin Appollis', position='MID', sub_position='WNG', club='Orlando Pirates', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Orlando Pirates WNG; South Africa dangerous wide attacker; pacey and direct; rotation winger partner',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular winger; Orlando Pirates DSTV Premiership', tier_revised='1'),
    dict(player='Thalente Mbatha', position='MID', sub_position='CM', club='Orlando Pirates', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Orlando Pirates CM; South Africa midfield rotation; combative and industrious; domestic quality',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Orlando Pirates DSTV Premiership', tier_revised='2'),
    dict(player='Jayden Adams', position='MID', sub_position='CM', club='Mamelodi Sundowns', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Mamelodi Sundowns CM; South Africa rotation midfielder; restored after year exclusion (late camp arrival); '
               'technically gifted; monitor match form carefully',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit; restored after 1-year exclusion; monitor form', tier_revised='2'),
    dict(player='Sphephelo Sithole', position='MID', sub_position='CM', club='CD Tondela', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='CD Tondela CM; South Africa European-based midfielder; Portuguese Segunda Liga; squad depth',
         int_l5_pattern='sub/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; CD Tondela Portuguese Segunda Liga', tier_revised='3'),
    dict(player='Themba Zwane', position='MID', sub_position='AM', club='Mamelodi Sundowns', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Mamelodi Sundowns AM; South Africa veteran creative playmaker; physical management required — '
               'cannot do full 90 regularly; impact sub role; experienced in big occasions',
         int_l5_pattern='sub/90/sub/sub/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit; age/fitness managed; cannot do 90 regularly; impact sub role', tier_revised='3'),
    # Forwards
    dict(player='Lyle Foster', position='FWD', sub_position='CF', club='Burnley', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Burnley CF; South Africa first-choice striker and only consistent top-flight European attacker; '
               'focal point of Bafana Bafana attack; physical, direct, and clinical in the box',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CF; Burnley PL/Championship', tier_revised='1'),
    dict(player='Evidence Makgopa', position='FWD', sub_position='CF', club='Orlando Pirates', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Orlando Pirates CF; South Africa second striker option; physical and direct; PSL prolific scorer; '
               'rotation partner/backup for Foster',
         int_l5_pattern='90/90/sub/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CF; Orlando Pirates DSTV Premiership', tier_revised='1'),
    dict(player='Iqraam Rayners', position='FWD', sub_position='CF', club='Mamelodi Sundowns', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Mamelodi Sundowns CF/WNG; South Africa rotation forward; versatile attacker; squad depth option',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation FWD; Sundowns DSTV Premiership', tier_revised='2'),
    dict(player='Tshepang Moremi', position='FWD', sub_position='WNG', club='Orlando Pirates', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Orlando Pirates WNG/FWD; South Africa wide forward option; direct and energetic; squad depth',
         int_l5_pattern='sub/sub/90/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation FWD/WNG; Orlando Pirates DSTV Premiership', tier_revised='2'),
    dict(player='Thapelo Maseko', position='FWD', sub_position='WNG', club='AEL Limassol', nationality='South Africa', group='A',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='AEL Limassol WNG (loan from Sundowns); South Africa returning from 2-year competitive absence; '
               'limited game time; selection a gamble by Broos; used sparingly if at all',
         int_l5_pattern='DNP/sub/DNP/sub/90', int_l5_starts=1, int_absence_reason='2-year competitive absence',
         fitness_current='Fit but match-unsharp; returning from 2-year absence; Broos gamble', tier_revised='3'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'South Africa': continue
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
