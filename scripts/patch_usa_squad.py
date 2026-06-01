#!/usr/bin/env python3
"""
patch_usa_squad.py — official 26-man squad (Berhalter/interim, announced May 2026).
Group D: USA(7.1), Turkey(5.8), Ecuador(5.8), Paraguay(4.6).
Advance 75%, dead rubber G3 10%.
Key fitness: Pulisic (gluteal muscle monitoring; expected fit opener),
             Richards (ankle DOUBTFUL; targeting G2),
             Adams (workload management — needs careful handling through group stage).
Musah OUT (season-ending injury, Jan 2026). Tim Ream captain.
Co-host home advantage factored into ADV boost.
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 75, 10
T1G, T1K = 87.1, 152
T2G, T2K = 74.0, 125
T3G, T3K = 42.0, 88
T4G, T4K = 16.0, 26

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Matt Turner', position='GK', sub_position='', club='Nottingham Forest', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=152,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Nottingham Forest GK; USA undisputed No.1; experienced international; reliable shot-stopper; vocal leader',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; Nottingham Forest PL', tier_revised='GK1'),
    dict(player='Ethan Horvath', position='GK', sub_position='', club='Luton Town', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=10,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Luton Town GK; USA No.2; experienced international backup; no WC starts expected unless Turner injured',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Luton Town Championship', tier_revised='GK2'),
    dict(player='Patrick Schulte', position='GK', sub_position='', club='Columbus Crew', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Columbus Crew GK; USA No.3; MLS quality; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Columbus Crew MLS', tier_revised='GK3'),
    # Defenders
    dict(player='Antonee Robinson', position='DEF', sub_position='LB', club='Fulham', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Fulham LB; USA first-choice left-back; explosive overlapping runs; PL quality; excellent crosser',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; Fulham PL', tier_revised='1'),
    dict(player='Sergiño Dest', position='DEF', sub_position='RB', club='PSV Eindhoven', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='PSV RB; USA first-choice right-back; returned to form in Eredivisie; dynamic and technically gifted',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; PSV Eredivisie', tier_revised='1'),
    dict(player='Chris Richards', position='DEF', sub_position='CB', club='Crystal Palace', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='Crystal Palace CB; USA best young CB; ankle injury May 2026; DOUBTFUL for opener June 22; '
               'targeting G2 June 26; USA staff cautious; PL-quality centre-back when fit',
         int_l5_pattern='90/90/90/DNP/sub', int_l5_starts=3, int_absence_reason='Ankle injury May 2026',
         fitness_current='Ankle injury; DOUBTFUL opener; targeting G2 June 26; cautious management', tier_revised='1'),
    dict(player='Tim Ream', position='DEF', sub_position='CB', club='Fulham', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Fulham CB; USA captain; veteran leader at 38 yrs; composed and experienced; steps up as first-choice CB '
               'if Richards misses opener; commanding vocal presence in backline',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain CB; Fulham PL', tier_revised='2'),
    dict(player='Mark McKenzie', position='DEF', sub_position='CB', club='Toulouse', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Toulouse CB; USA solid rotation centre-back; Ligue 1 quality; good in the air and on the ball',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Toulouse Ligue 1', tier_revised='2'),
    dict(player='Joe Scally', position='DEF', sub_position='RB', club='Borussia Mönchengladbach', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Gladbach RB; USA rotation right-back; Bundesliga experience; reliable and technically solid',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation RB; Gladbach Bundesliga', tier_revised='2'),
    dict(player='Aaron Long', position='DEF', sub_position='CB', club='New York Red Bulls', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='NYRB CB; USA veteran CB; experienced international; squad depth cover for Ream/McKenzie/Richards',
         int_l5_pattern='sub/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran CB depth; NYRB MLS', tier_revised='3'),
    dict(player='Sam Vines', position='DEF', sub_position='LB', club='Royal Antwerp', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Royal Antwerp LB; USA left-back depth; Belgian Pro League; squad cover for Robinson',
         int_l5_pattern='sub/90/DNP/sub/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='LB depth; Royal Antwerp Belgian Pro League', tier_revised='3'),
    dict(player='DeAndre Yedlin', position='DEF', sub_position='RB', club='Inter Miami', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Inter Miami RB; USA veteran right-back at 35; MLS experience with Messi; emergency cover; fringe selection',
         int_l5_pattern='sub/DNP/sub/DNP/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran depth RB; Inter Miami MLS', tier_revised='4'),
    dict(player='Chris Gloster', position='DEF', sub_position='LB', club='Hannover 96', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hannover 96 LB; USA fringe left-back option; Bundesliga 2 experience; depth cover behind Robinson/Vines',
         int_l5_pattern='sub/DNP/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe LB depth; Hannover 96 Bundesliga 2', tier_revised='4'),
    # Midfielders
    dict(player='Tyler Adams', position='MID', sub_position='DM', club='Bournemouth', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Bournemouth DM; USA defensive engine; workload management ongoing through season — '
               'needs careful handling; elite pressing and ball-winning; key to US structure when fit',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit; workload managed carefully; expected available throughout tournament', tier_revised='1'),
    dict(player='Malik Tillman', position='MID', sub_position='CM', club='PSV Eindhoven', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='PSV CM/AM; USA key creator; excellent at PSV with goals and assists; box-to-box quality; '
               'natural successor to Musah (OUT) as dynamic midfield presence; Eredivisie standout',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key creator; PSV Eredivisie', tier_revised='1'),
    dict(player='Weston McKennie', position='MID', sub_position='CM', club='Juventus', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Juventus CM; USA box-to-box midfielder; Serie A quality; energetic and combative; rotation behind Adams/Tillman',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Juventus Serie A', tier_revised='2'),
    dict(player='Luca de la Torre', position='MID', sub_position='DM', club='Celta Vigo', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Celta Vigo DM; USA intelligent ball-playing midfielder; La Liga experience; rotation DM cover for Adams',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation DM; Celta Vigo La Liga', tier_revised='2'),
    dict(player='Djordje Mihailovic', position='MID', sub_position='CM', club='Ajax', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Ajax CM; USA technically gifted midfielder; Eredivisie quality; squad depth in central midfield',
         int_l5_pattern='sub/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; Ajax Eredivisie', tier_revised='3'),
    dict(player='Cristian Roldan', position='MID', sub_position='CM', club='Seattle Sounders', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Seattle Sounders CM; USA veteran midfielder; experienced international; MLS stalwart; squad depth option',
         int_l5_pattern='sub/DNP/sub/sub/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran CM depth; Seattle Sounders MLS', tier_revised='3'),
    # Forwards
    dict(player='Christian Pulisic', position='FWD', sub_position='WNG', club='AC Milan', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='AC Milan LW/AM; USA star player; gluteal muscle monitoring but expected fit for June 22 opener; '
               'career-best season at Milan; deadly from wide left and centrally; WC form crucial for USA',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit; gluteal muscle monitoring; expected available for opener', tier_revised='1'),
    dict(player='Folarin Balogun', position='FWD', sub_position='CF', club='Monaco', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Monaco CF; USA first-choice centre-forward; prolific at Monaco in Ligue 1; excellent movement and finishing; '
               'key penalty box threat with Pulisic operating wide',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CF; Monaco Ligue 1', tier_revised='1'),
    dict(player='Tim Weah', position='FWD', sub_position='WNG', club='Juventus', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Juventus RW; USA right-winger son of George Weah; Serie A quality; direct and pacey; key rotation winger',
         int_l5_pattern='90/90/sub/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation RW; Juventus Serie A', tier_revised='2'),
    dict(player='Brenden Aaronson', position='FWD', sub_position='WNG', club='Leeds United', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Leeds LW; USA energetic left winger; pressing excellence; back on form after mixed Bundesliga stint; '
               'Championship quality but international-level work rate and creativity',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation LW; Leeds Championship', tier_revised='2'),
    dict(player='Alan Zendejas', position='FWD', sub_position='WNG', club='LAFC', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='LAFC AM/WNG; USA creative attacking option; Mexican-American chose USMNT; MLS quality creator; '
               'squad depth attacking option; impact sub potential',
         int_l5_pattern='sub/sub/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='AM/WNG depth; LAFC MLS', tier_revised='3'),
    dict(player='Josh Sargent', position='FWD', sub_position='CF', club='Norwich City', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Norwich CF; USA backup striker; Championship quality; physical and direct; depth behind Balogun',
         int_l5_pattern='sub/sub/DNP/90/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup CF; Norwich Championship', tier_revised='3'),
    dict(player='Caden Clark', position='FWD', sub_position='WNG', club='RB Leipzig', nationality='USA', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='RB Leipzig AM/WNG; USA exciting young attacker; Bundesliga potential; creative with pace; squad depth option',
         int_l5_pattern='sub/DNP/sub/sub/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young depth AM; RB Leipzig Bundesliga', tier_revised='3'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'USA': continue
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
