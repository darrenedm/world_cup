#!/usr/bin/env python3
"""
patch_ivory_coast_squad.py  —  confirmed squad, May 2026, Emerse Faé.
Amad Diallo (T1) already in CSV — confirm to 100%.
25 of 26 tracked; 1 player TBC.
Group E: Germany(7.9), Ecuador(5.8), Ivory Coast(4.4), Curaçao(1.3).
Advance 44%, dead rubber G3 10%.
"""
import csv
PATH = '/tmp/world_cup_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = {'Amad Diallo'}
CORRECTIONS  = {}

ADV, DR = 44, 10
T1G, T1K = 87.1, 33
T2G, T2K = 74.0, 27
T3G, T3K = 42.0, 20
T4G, T4K = 16.0, 6

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Yahia Fofana', position='GK', sub_position='', club='Leicester City', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=33,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Leicester GK; Ivory Coast No.1; strong shot-stopper; PL experience; reliable between the posts',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; Leicester PL quality', tier_revised='GK1'),
    dict(player='Ibrahim Koné', position='GK', sub_position='', club='ASEC Mimosas', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=3,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='ASEC Mimosas GK; Ivory Coast No.2; domestic keeper; no WC starts expected',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Ivorian domestic league', tier_revised='GK2'),
    dict(player='Alban Lafont', position='GK', sub_position='', club='Nantes', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Nantes GK; Ligue 1 experience; third-choice keeper; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Nantes Ligue 1', tier_revised='GK3'),
    # Defenders
    dict(player='Wilfried Singo', position='DEF', sub_position='RB', club='Monaco', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Monaco RB; powerful overlapping right-back; Ivory Coast first-choice; electric pace and crossing',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; Monaco Ligue 1 quality', tier_revised='1'),
    dict(player='Odilon Kossounou', position='DEF', sub_position='CB', club='Bayer Leverkusen', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Bayer Leverkusen CB; elite technical defender; Bundesliga champion; Ivory Coast\'s best CB',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Elite CB; Leverkusen Bundesliga/UCL', tier_revised='1'),
    dict(player='Evan Ndicka', position='DEF', sub_position='CB', club='Roma', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Roma CB/LB; versatile and composed; Serie A quality; regular Ivory Coast partner',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB/LB; Roma Serie A', tier_revised='2'),
    dict(player='Ghislain Konan', position='DEF', sub_position='LB', club='Montpellier', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Montpellier LB; attack-minded and experienced; consistent Ivory Coast left-back option',
         int_l5_pattern='90/sub/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular LB; Ligue 1', tier_revised='2'),
    dict(player='Emmanuel Agbadou', position='DEF', sub_position='CB', club='Wolverhampton Wanderers', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Wolves CB; commanding in the air; solid PL experience; regular Ivory Coast defensive option',
         int_l5_pattern='90/90/sub/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB; Wolves PL quality', tier_revised='2'),
    dict(player='Jean-Noël Akpa Akpro', position='DEF', sub_position='RB', club='Lazio', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Lazio utility player; versatile across wide roles; rotation cover; Serie A experience',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Utility rotation; Lazio Serie A', tier_revised='3'),
    dict(player='Désiré Doué', position='DEF', sub_position='LB', club='Paris Saint-Germain', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='PSG winger/wing-back; highly talented; playing wide-back role for Ivory Coast; exciting prospect',
         int_l5_pattern='sub/90/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young talent wing-back; PSG Ligue 1', tier_revised='3'),
    # Midfielders
    dict(player='Ibrahim Sangaré', position='MID', sub_position='DM', club='Nottingham Forest', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Nottm Forest DM; dominant holding midfielder; tenacious tackler; Ivory Coast midfield anchor',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key DM; Nottm Forest PL anchor', tier_revised='1'),
    dict(player='Seko Fofana', position='MID', sub_position='CM', club='Al-Qadsiah', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Qadsiah CM; former Lens/Leicester; box-to-box quality; key Ivory Coast midfield creative',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key CM; former Ligue 1/PL quality', tier_revised='2'),
    dict(player='Franck Kessié', position='MID', sub_position='CM', club='Atalanta', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='Atalanta CM; formerly Barcelona/AC Milan; powerful midfield engine; hamstring concern May 2026',
         int_l5_pattern='90/sub/DNP/90/sub', int_l5_starts=2, int_absence_reason='Hamstring concern May 2026',
         fitness_current='Hamstring concern; participation uncertain', tier_evidence='Quality CM if fit; fitness TBC', tier_revised='2'),
    dict(player='Jean Michael Seri', position='MID', sub_position='DM', club='Hull City', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hull City DM; experienced veteran; former Nice/Fulham; squad depth in midfield',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran DM rotation; Championship', tier_revised='3'),
    dict(player='Oumar Oulai', position='MID', sub_position='CM', club='Strasbourg', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Strasbourg CM; young Ivorian international; Ligue 1 experience; rotation depth',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young CM depth; Ligue 1', tier_revised='3'),
    dict(player='Flavien Guiagon', position='MID', sub_position='CM', club='Lens', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Lens CM; young Ivory Coast international; solid Ligue 1 form; squad rotation option',
         int_l5_pattern='sub/sub/DNP/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Ligue 1', tier_revised='3'),
    # Forwards
    dict(player='Simon Adingra', position='FWD', sub_position='', club='Brighton', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Brighton winger; electric pace and direct running; Ivory Coast key wide threat; '
               'excellent dribbler and finisher; PL quality',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key winger; Brighton PL quality', tier_revised='1'),
    dict(player='Nicolas Pépé', position='FWD', sub_position='', club='Angers', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Angers winger; former Arsenal/Lille; experienced at highest level; Ivory Coast wide option',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Experienced winger; Ligue 1', tier_revised='2'),
    dict(player='Oumar Diomandé', position='FWD', sub_position='', club='Sporting CP', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Sporting CP striker; powerful and direct; prolific in Portugal; Ivory Coast key striker option',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key striker; Sporting CP Primeira Liga', tier_revised='2'),
    dict(player='Evann Guessand', position='FWD', sub_position='', club='Nice', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='Nice striker; powerful and mobile; knee injury concern May 2026; Ivory Coast striker if fit',
         int_l5_pattern='90/sub/DNP/90/sub', int_l5_starts=2, int_absence_reason='Knee concern May 2026',
         fitness_current='Knee concern; availability uncertain', tier_evidence='Key striker if fit; Nice Ligue 1', tier_revised='2'),
    dict(player='Amine Gouiri', position='FWD', sub_position='', club='Rennes', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Rennes forward/winger; technically gifted; Ligue 1 quality; rotation cover in attack',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Attack rotation; Rennes Ligue 1', tier_revised='3'),
    dict(player='Jean-Philippe Diakite', position='FWD', sub_position='', club='Toulouse', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Toulouse forward; young Ivory Coast attacker; Ligue 1 depth option',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young squad forward; Ligue 1', tier_revised='3'),
    dict(player='Elye Wahi', position='FWD', sub_position='', club='Marseille', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Marseille striker; young Ivory Coast forward; Ligue 1 quality; squad option',
         int_l5_pattern='sub/90/DNP/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young striker; Marseille Ligue 1', tier_revised='3'),
    dict(player='Kévin Bonny', position='FWD', sub_position='', club='Parma', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Parma forward; young Ivory Coast talent; Serie A experience; depth option in attack',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young depth forward; Serie A', tier_revised='3'),
    dict(player='Dango Ouattara', position='FWD', sub_position='', club='Bournemouth', nationality='Ivory Coast', group='E',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Bournemouth winger; 26th-man cover; fringe selection; depth only',
         int_l5_pattern='DNP/sub/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe winger; PL depth', tier_revised='4'),
]

def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Ivory Coast': continue
        name = row['player']
        if name in NOT_SELECTED:
            row['wc_squad_prob_pct'] = '0'; updated += 1
        elif name in CONFIRMED_IN:
            row['wc_squad_prob_pct'] = '100'; updated += 1
            print(f'  Set 100%: {name}')
        if name in CORRECTIONS:
            for k, v in CORRECTIONS[name].items(): row[k] = str(v)
    blank_pts = {'action_pts_per_90':'0','exp_pts_per_90':'0','total_exp_fantasy_pts':'0','adj_exp_fantasy_pts':'0'}
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
