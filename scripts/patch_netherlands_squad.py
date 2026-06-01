#!/usr/bin/env python3
"""
patch_netherlands_squad.py — official 26-man squad (Koeman, announced May 2026).
Group F: Netherlands(8.2), Japan(6.8), Tunisia(4.5), Sweden(4.4).
Advance 78%, dead rubber G3 10%.
Key fitness: Depay (fitness concern; Koeman "must prove fitness before opener"),
             Xavi Simons OUT (ACL surgery March 2026), de Ligt OUT (sold/dropped).
Van Dijk captain; Reijnders now primary creator after Simons injury.
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 78, 10
T1G, T1K = 87.1, 171
T2G, T2K = 74.0, 140
T3G, T3K = 43.0, 99
T4G, T4K = 16.0, 29

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Bart Verbruggen', position='GK', sub_position='', club='Brighton & Hove Albion', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=171,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Brighton GK; Netherlands undisputed No.1; established himself at Premier League level; commanding presence',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; Brighton PL', tier_revised='GK1'),
    dict(player='Mark Flekken', position='GK', sub_position='', club='Brentford', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=10,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Brentford GK; Netherlands No.2; solid PL keeper; experienced international backup',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Brentford PL', tier_revised='GK2'),
    dict(player='Justin Bijlow', position='GK', sub_position='', club='Feyenoord', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Feyenoord GK; Netherlands No.3; Eredivisie experience; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Feyenoord Eredivisie', tier_revised='GK3'),
    # Defenders
    dict(player='Virgil van Dijk', position='DEF', sub_position='CB', club='Liverpool', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Liverpool CB; Netherlands captain; world-class central defender; elite aerial dominance; '
               'commanding vocal leader; Liverpool Premier League mainstay',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed captain CB; Liverpool PL', tier_revised='1'),
    dict(player='Nathan Aké', position='DEF', sub_position='CB', club='Manchester City', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Man City CB/LB; Netherlands first-choice second CB; versatile and composed; PL champion',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Man City PL', tier_revised='1'),
    dict(player='Denzel Dumfries', position='DEF', sub_position='RB', club='Inter Milan', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Inter Milan RB; Netherlands first-choice right-back; dynamic and attacking; Serie A star',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; Inter Milan Serie A', tier_revised='1'),
    dict(player='Jurriën Timber', position='DEF', sub_position='CB', club='Arsenal', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Arsenal CB/RB; Netherlands versatile second-choice defender; composed on ball; excellent positional sense',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB/RB; Arsenal PL', tier_revised='2'),
    dict(player='Tyrell Malacia', position='DEF', sub_position='LB', club='Manchester United', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Man United LB; Netherlands rotation left-back; quick and energetic; reliable defensive option',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation LB; Man United PL', tier_revised='2'),
    dict(player='Jeremie Frimpong', position='DEF', sub_position='RB', club='Manchester City', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Man City RB; Netherlands exciting attacking right-back; directness and pace; squad depth option',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth RB; Man City PL', tier_revised='3'),
    dict(player='Quilindschy Hartman', position='DEF', sub_position='LB', club='Feyenoord', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Feyenoord LB; Netherlands young left-back option; Eredivisie quality; squad depth behind Malacia/Aké',
         int_l5_pattern='sub/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth LB; Feyenoord Eredivisie', tier_revised='3'),
    # Midfielders
    dict(player='Tijjani Reijnders', position='MID', sub_position='CM', club='AC Milan', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='AC Milan CM; Netherlands primary creator following Simons ACL; box-to-box excellence; '
               'top scorer in his position at Milan; goals, assists, and pressing; stepped up to become lynchpin',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed primary creator; AC Milan Serie A', tier_revised='1'),
    dict(player='Jerdy Schouten', position='MID', sub_position='DM', club='Atlético Madrid', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atlético Madrid DM; Netherlands defensive midfielder; La Liga quality; excellent positional reading; covers Reijnders',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice DM; Atlético Madrid La Liga', tier_revised='1'),
    dict(player='Ryan Gravenberch', position='MID', sub_position='CM', club='Liverpool', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Liverpool CM; Netherlands powerful box-to-box midfielder; excellent at Liverpool under Slot; ball-carrying and pressing',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key starter; Liverpool PL', tier_revised='1'),
    dict(player='Teun Koopmeiners', position='MID', sub_position='CM', club='Juventus', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Juventus CM; Netherlands important attacking midfielder; excellent goal-scoring from midfield; Juve creative force',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular starter; Juventus Serie A', tier_revised='2'),
    dict(player='Frenkie de Jong', position='MID', sub_position='CM', club='FC Barcelona', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Barcelona CM; Netherlands creative midfielder; injury-plagued but fit for WC; elite technical quality and vision',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit; recovered from recurring injury issues', tier_evidence='Rotation CM; Barcelona La Liga', tier_revised='2'),
    dict(player='Johan Veerman', position='MID', sub_position='CM', club='PSV Eindhoven', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='PSV CM; Netherlands Eredivisie quality; industrious and combative; squad depth in central midfield',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; PSV Eredivisie', tier_revised='2'),
    dict(player='Quinten Timber', position='MID', sub_position='CM', club='Arsenal', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Arsenal CM; Netherlands younger Timber brother; box-to-box midfielder; squad depth; PL quality',
         int_l5_pattern='sub/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; Arsenal PL', tier_revised='3'),
    dict(player='Steven Berghuis', position='MID', sub_position='AM', club='Ajax', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Ajax AM; Netherlands veteran wide midfielder; experience and creativity; squad depth option',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='AM depth; Ajax Eredivisie', tier_revised='3'),
    # Forwards
    dict(player='Cody Gakpo', position='FWD', sub_position='WNG', club='Liverpool', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Liverpool LW/CF; Netherlands first-choice attacker; prolific at Liverpool; versatile — plays LW or CF; '
               'excellent off the ball movement and finishing; key threat in transition',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice forward; Liverpool PL', tier_revised='1'),
    dict(player='Donyell Malen', position='FWD', sub_position='WNG', club='Aston Villa', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Aston Villa RW; Netherlands first-choice right winger; pace and directness; excellent at Villa; '
               'prolific in transition; key wide threat alongside Gakpo',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RW; Aston Villa PL', tier_revised='1'),
    dict(player='Crysencio Summerville', position='FWD', sub_position='WNG', club='West Ham United', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='West Ham LW; Netherlands exciting wide attacker; PL quality; direct and technical; rotation winger option',
         int_l5_pattern='90/90/sub/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation LW; West Ham PL', tier_revised='2'),
    dict(player='Noa Lang', position='FWD', sub_position='WNG', club='PSV Eindhoven', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='PSV RW/LW; Netherlands technically gifted winger; Eredivisie star; direct and dribbling; rotation option',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation winger; PSV Eredivisie', tier_revised='2'),
    dict(player='Memphis Depay', position='FWD', sub_position='WNG', club='Atlético Madrid', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='Atlético Madrid CF/LW; Netherlands veteran attacker; fitness concern going into WC — '
               'Koeman: "Memphis must prove his fitness before the opener"; hamstring management ongoing',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='Hamstring management May 2026',
         fitness_current='Doubtful; Koeman: must prove fitness before opener; hamstring management', tier_revised='2'),
    dict(player='Patrick Kluivert', position='FWD', sub_position='WNG', club='Bournemouth', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Bournemouth LW/CF; Netherlands son of Patrick Kluivert Sr; good PL season; squad depth in attack',
         int_l5_pattern='sub/90/sub/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth forward; Bournemouth PL', tier_revised='3'),
    dict(player='Joshua Zirkzee', position='FWD', sub_position='CF', club='Manchester United', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Man United CF; Netherlands tall centre-forward; link-up and finishing; depth striker option behind Gakpo',
         int_l5_pattern='sub/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CF; Man United PL', tier_revised='3'),
    dict(player='Brian Brobbey', position='FWD', sub_position='CF', club='Ajax', nationality='Netherlands', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Ajax CF; Netherlands powerful striker; Eredivisie top scorer; physical and direct; fringe squad selection',
         int_l5_pattern='sub/DNP/sub/90/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CF; Ajax Eredivisie', tier_revised='3'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Netherlands': continue
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
