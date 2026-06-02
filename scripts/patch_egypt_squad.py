#!/usr/bin/env python3
"""
patch_egypt_squad.py — official 26-man squad (Hossam Hassan, announced May 30 2026).
Group G: Belgium(7.6), Iran(5.5), Egypt(5.0), New Zealand(1.0).
Advance 28%, dead rubber G3 10%.
KEY NOTES: Egypt carry 4 GKs (officially registered). Mohamed Salah leads as captain.
Omar Marmoush (Man City) is the second marquee attacker. 18-year-old Hamza Abdelkarim
(Barcelona B) earns surprise call-up. Mahmoud Trezeguet and Emam Ashour provide
midfield creativity. Strong Al-Ahly domestic backbone.
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 28, 10
T1G, T1K = 87.1, 9
T2G, T2K = 74.0, 7
T3G, T3K = 42.0, 5
T4G, T4K = 16.0, 2

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Mohamed El Shenawy', position='GK', sub_position='', club='Al-Ahly', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Ahly GK; Egypt undisputed No.1; experienced and commanding; Africa\'s most successful club; leads from the back',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed No.1; Al-Ahly Egyptian PL', tier_revised='GK1'),
    dict(player='Mostafa Shobeir', position='GK', sub_position='', club='Al-Ahly', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=1,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Ahly GK; Egypt No.2; solid domestic performer; unlikely to start unless El Shenawy injured',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Al-Ahly Egyptian PL', tier_revised='GK2'),
    dict(player='El Mahdy Soliman', position='GK', sub_position='', club='Al-Zamalek', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Zamalek GK; Egypt No.3; no WC minutes expected; squad depth cover',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Al-Zamalek Egyptian PL', tier_revised='GK3'),
    dict(player='Mohamed Alaa', position='GK', sub_position='', club='El Gouna', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='El Gouna GK; Egypt fourth GK (rare 4-GK selection); no WC minutes expected',
         int_l5_pattern='DNP/DNP/DNP/DNP/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fourth GK; El Gouna Egyptian PL', tier_revised='GK3'),
    # Defenders
    dict(player='Mohamed Abdelmonem', position='DEF', sub_position='CB', club='OGC Nice', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Nice CB; Egypt first-choice centre-back; Ligue 1 experience; composed and strong in the air',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; OGC Nice Ligue 1', tier_revised='1'),
    dict(player='Yasser Ibrahim', position='DEF', sub_position='CB', club='Al-Ahly', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Ahly CB; Egypt regular starter; dominant domestic performer; key part of CAF Champions League-winning defence',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB starter; Al-Ahly Egyptian PL', tier_revised='1'),
    dict(player='Hamdy Fathy', position='DEF', sub_position='RB', club='Al-Wakrah', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Wakrah (Qatar) RB; Egypt first-choice right-back; energetic and attacking; experienced Qatar Stars League performer',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; Al-Wakrah Qatar Stars League', tier_revised='1'),
    dict(player='Mohamed Hany', position='DEF', sub_position='LB', club='Al-Ahly', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Ahly LB/CB; Egypt versatile defender; reliable starter; strong Al-Ahly backbone',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular LB/CB; Al-Ahly Egyptian PL', tier_revised='1'),
    dict(player='Ramy Rabia', position='DEF', sub_position='CB', club='Al Ain', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al Ain (UAE) CB; Egypt rotation centre-back; UAE Pro League experience; solid defensive cover',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Al Ain UAE Pro League', tier_revised='2'),
    dict(player='Hossam Abdelmaguid', position='DEF', sub_position='CB', club='Al-Zamalek', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Zamalek CB; Egypt squad defender; physical presence; domestic rotation cover',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Al-Zamalek Egyptian PL', tier_revised='2'),
    dict(player='Tarek Alaa', position='DEF', sub_position='CB', club='ZED FC', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='ZED FC CB; Egypt squad depth defender; domestic league performer; limited WC minutes expected',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CB; ZED FC Egyptian PL', tier_revised='3'),
    dict(player='Ahmed El Fotouh', position='DEF', sub_position='RB', club='Al-Zamalek', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Zamalek RB; Egypt defensive cover; rotation option at right-back; squad depth',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth RB; Al-Zamalek Egyptian PL', tier_revised='3'),
    dict(player='Karim Hafez', position='DEF', sub_position='CB', club='Pyramids FC', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='4', playing_role='Squad Player',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Pyramids FC CB; Egypt fringe squad member; limited international minutes expected',
         int_l5_pattern='sub/DNP/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CB; Pyramids FC Egyptian PL', tier_revised='4'),
    # Midfielders
    dict(player='Mohamed Salah', position='MID', sub_position='WNG', club='Liverpool', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Liverpool RW; Egypt captain and all-time great; 100+ caps; PL Golden Boot contender; world-class; tournament focal point',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Egypt captain; world-class RW; Liverpool PL', tier_revised='1'),
    dict(player='Emam Ashour', position='MID', sub_position='CM', club='Al-Ahly', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Ahly CM; Egypt midfield engine; creative and energetic; key Al-Ahly performer and Egypt regular',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key CM; Al-Ahly Egyptian PL', tier_revised='1'),
    dict(player='Mahmoud Trezeguet', position='MID', sub_position='WNG', club='Al-Ahly', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Ahly WNG; Egypt experienced winger; long-time international; clubs include Aston Villa; direct and dangerous wide option',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular WNG starter; Al-Ahly Egyptian PL', tier_revised='1'),
    dict(player='Ahmed Zizo', position='MID', sub_position='WNG', club='Al-Ahly', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Ahly WNG; Egypt regular; direct and pacey wide attacker; strong domestic form',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular WNG; Al-Ahly Egyptian PL', tier_revised='2'),
    dict(player='Marwan Attia', position='MID', sub_position='CM', club='Al-Ahly', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Ahly CM; Egypt midfield option; reliable domestic performer; rotation in central midfield',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Al-Ahly Egyptian PL', tier_revised='2'),
    dict(player='Ibrahim Adel', position='MID', sub_position='WNG', club='Nordsjaelland', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Nordsjaelland WNG; Egypt young wide attacker; Danish Superliga; exciting European-based talent; rotation option',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation WNG; Nordsjaelland Danish Superliga', tier_revised='2'),
    dict(player='Haitham Hassan', position='MID', sub_position='WNG', club='Real Oviedo', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Real Oviedo WNG; Egypt European-based winger; Spanish segunda experience; rotation wide option',
         int_l5_pattern='90/sub/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation WNG; Real Oviedo Spanish Segunda', tier_revised='2'),
    dict(player='Mohanad Lasheen', position='MID', sub_position='AM', club='Pyramids FC', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Pyramids FC AM; Egypt squad option; domestic league performer; limited WC minutes anticipated',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Squad AM; Pyramids FC Egyptian PL', tier_revised='3'),
    dict(player='Mostafa Ziko', position='MID', sub_position='CM', club='Pyramids FC', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Pyramids FC CM; Egypt squad depth midfielder; domestic performer; fringe WC minutes',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CM; Pyramids FC Egyptian PL', tier_revised='3'),
    dict(player='Nabil Emad Donga', position='MID', sub_position='DM', club='Al Najma', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al Najma (Bahrain) DM; Egypt squad midfielder; overseas-based; depth option in holding role',
         int_l5_pattern='sub/DNP/DNP/90/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth DM; Al Najma Bahrain', tier_revised='3'),
    dict(player='Mahmoud Saber', position='MID', sub_position='CM', club='ZED FC', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='4', playing_role='Squad Player',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='ZED FC CM; Egypt fringe squad player; domestic league performer; very limited WC minutes expected',
         int_l5_pattern='sub/DNP/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CM; ZED FC Egyptian PL', tier_revised='4'),
    # Forwards
    dict(player='Omar Marmoush', position='FWD', sub_position='CF', club='Manchester City', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Manchester City CF; Egypt second key attacker; explosive season in PL; versatile forward who can play CF or wide; partners Salah',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Star attacker; Man City PL', tier_revised='1'),
    dict(player='Hamza Abdelkarim', position='FWD', sub_position='CF', club='Barcelona B', nationality='Egypt', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Barcelona B CF; Egypt surprise call-up aged 18; La Masia product; huge future talent; limited WC role expected',
         int_l5_pattern='sub/DNP/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young talent; Barcelona B Spanish Segunda', tier_revised='3'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Egypt': continue
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
