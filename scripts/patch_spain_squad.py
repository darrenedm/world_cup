#!/usr/bin/env python3
"""
patch_spain_squad.py — official 26-man squad (De la Fuente, announced May 25 2026).
Group H: Spain(9.7), Uruguay(7.0), Saudi Arabia(3.0), Cape Verde(2.5).
Advance 87%, dead rubber G3 10%.
Key fitness: Yamal (hamstring; likely misses G1-G2, targets Uruguay G3),
             Nico Williams (hamstring scare; expected fit for opener),
             Gavi (returning from double ACL surgery; managed carefully).
Note: No Real Madrid players — historic first. Rodri fully fit (prior ACL recovery complete).
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 87, 10
T1G, T1K = 88.5, 233
T2G, T2K = 75.0, 191
T3G, T3K = 47.0, 135
T4G, T4K = 17.0, 40

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Unai Simón', position='GK', sub_position='', club='Athletic Club', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=233,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Athletic Club GK; Spain undisputed No.1; commanding and ball-playing GK; key to Spain build-up',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; Athletic Club La Liga', tier_revised='GK1'),
    dict(player='David Raya', position='GK', sub_position='', club='Arsenal', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=5,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Arsenal GK; Spain No.2; elite-level GK at club level; no WC starts expected unless Simón injured',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Arsenal PL', tier_revised='GK2'),
    dict(player='Joan García', position='GK', sub_position='', club='FC Barcelona', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Barcelona GK; Spain No.3; first senior WC call-up; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Barcelona La Liga', tier_revised='GK3'),
    # Defenders
    dict(player='Pau Cubarsí', position='DEF', sub_position='CB', club='FC Barcelona', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Barcelona CB; only 17 yrs — already an automatic Spain starter; composed on ball; exceptional talent',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Automatic CB at 17; Barcelona La Liga', tier_revised='1'),
    dict(player='Aymeric Laporte', position='DEF', sub_position='CB', club='Athletic Club', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Athletic Club CB; Spain first-choice CB partner; commanding and elegant; returned from Saudi Arabia',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Athletic Club La Liga', tier_revised='1'),
    dict(player='Marc Cucurella', position='DEF', sub_position='LB', club='Chelsea', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Chelsea LB; Spain first-choice left-back under De la Fuente; energetic and pressing; key in wide press',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; Chelsea PL', tier_revised='1'),
    dict(player='Pedro Porro', position='DEF', sub_position='RB', club='Tottenham Hotspur', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Spurs RB; Spain first-choice right-back; dynamic and attack-minded; delivers dangerous crosses',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; Spurs PL', tier_revised='1'),
    dict(player='Alejandro Grimaldo', position='DEF', sub_position='LB', club='Bayer Leverkusen', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Leverkusen LB; Spain elite left-back option; competing with Cucurella; prolific from left flank',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Elite rotation LB; Leverkusen Bundesliga', tier_revised='2'),
    dict(player='Marcos Llorente', position='DEF', sub_position='RB', club='Atlético Madrid', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atlético Madrid RB/CM; versatile — covers right-back and central midfield; solid rotation option',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Versatile rotation; Atlético Madrid La Liga', tier_revised='2'),
    dict(player='Eric García', position='DEF', sub_position='CB', club='FC Barcelona', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Barcelona CB; Spain rotation centre-back; experienced international; depth cover behind Cubarsí/Laporte',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Barcelona La Liga', tier_revised='2'),
    dict(player='Marc Pubill', position='DEF', sub_position='RB', club='FC Barcelona', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Barcelona RB; young Spain option; squad depth; limited WC minutes expected',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young depth RB; Barcelona La Liga', tier_revised='3'),
    # Midfielders
    dict(player='Rodri', position='MID', sub_position='DM', club='Manchester City', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Man City DM; world\'s best defensive midfielder; fully recovered from 2024-25 ACL; '
               'De la Fuente\'s first name on team sheet; no confirmed groin issue as of squad announcement',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit; ACL recovery complete; undisputed pivot', tier_evidence='Best DM in world; Man City PL', tier_revised='1'),
    dict(player='Pedri', position='MID', sub_position='CM', club='FC Barcelona', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Barcelona CM; Spain creative heartbeat; exceptional technical quality; drives Spain\'s possession game',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed starter; Barcelona La Liga', tier_revised='1'),
    dict(player='Fabián Ruiz', position='MID', sub_position='CM', club='Paris Saint-Germain', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='PSG CM; Spain elegant box-to-box midfielder; excellent passing range and goal threat; key starter',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key starter; PSG Ligue 1', tier_revised='1'),
    dict(player='Martín Zubimendi', position='MID', sub_position='DM', club='Arsenal', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Arsenal DM; Spain excellent holding midfielder; cover and competition for Rodri; PL quality',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key DM rotation; Arsenal PL', tier_revised='1'),
    dict(player='Mikel Merino', position='MID', sub_position='CM', club='Arsenal', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Arsenal CM; Spain important box-to-box midfielder; goal threat and pressing; versatile in multiple positions',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular starter; Arsenal PL', tier_revised='1'),
    dict(player='Gavi', position='MID', sub_position='CM', club='FC Barcelona', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Barcelona CM; returned from double ACL surgery nightmare (2 surgeries, 2+ years); back since March 2026; '
               '8 appearances; included but load carefully managed by De la Fuente',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit; returning from double ACL; load managed carefully', tier_evidence='Elite rotation CM; Barcelona La Liga', tier_revised='2'),
    dict(player='Álex Baena', position='MID', sub_position='AM', club='Villarreal', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Villarreal AM/RW; attacking wide midfield option; creative threat; covers for Yamal in early games',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular rotation AM/RW; Villarreal La Liga', tier_revised='2'),
    # Forwards
    dict(player='Lamine Yamal', position='FWD', sub_position='', club='FC Barcelona', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='Barcelona RW; Spain\'s most dangerous attacker; hamstring (biceps femoris, April 22); '
               'expected to miss G1 (Cape Verde June 15) and G2 (Saudi Arabia); targeting return G3 vs Uruguay June 26',
         int_l5_pattern='90/90/90/DNP/sub', int_l5_starts=3, int_absence_reason='Hamstring biceps femoris April 22',
         fitness_current='Hamstring; likely misses G1-G2; targeting G3 vs Uruguay June 26', tier_revised='1'),
    dict(player='Nico Williams', position='FWD', sub_position='', club='Athletic Club', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Athletic Club LW; Spain elite wide threat; hamstring scare May 10 vs Valencia; scan ruled out serious injury; '
               '~3 weeks recovery = expected fit for June 15 opener; De la Fuente: "he should be OK"',
         int_l5_pattern='90/90/90/90/DNP', int_l5_starts=4, int_absence_reason='Hamstring scare May 10; recovered',
         fitness_current='Fit; hamstring scare resolved; expected for opener', tier_evidence='First-choice LW; Athletic Club La Liga', tier_revised='1'),
    dict(player='Mikel Oyarzabal', position='FWD', sub_position='', club='Real Sociedad', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Real Sociedad ST/AM; Spain reliable attacking option; clinical finisher; versatile across forward positions',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular striker/AM; Real Sociedad La Liga', tier_revised='1'),
    dict(player='Dani Olmo', position='FWD', sub_position='', club='FC Barcelona', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Barcelona AM/ST; Spain key attacking option; versatile — covers RW during Yamal absence; creative and goalscoring',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key AM/FWD; Barcelona La Liga', tier_revised='1'),
    dict(player='Ferran Torres', position='FWD', sub_position='', club='FC Barcelona', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Barcelona LW/RW; Spain rotation wide attacker; covers both flanks; key rotation during Yamal absence',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation winger; Barcelona La Liga', tier_revised='2'),
    dict(player='Yeremy Pino', position='FWD', sub_position='', club='Crystal Palace', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Crystal Palace RW; Spain wide attacker; direct and pacey; rotation option across forward line',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation RW; Crystal Palace PL', tier_revised='2'),
    dict(player='Borja Iglesias', position='FWD', sub_position='', club='Celta Vigo', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Celta Vigo ST; Spain backup striker; physical target-man; depth option behind Oyarzabal',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup ST; Celta Vigo La Liga', tier_revised='2'),
    dict(player='Víctor Muñoz', position='FWD', sub_position='', club='Osasuna', nationality='Spain', group='H',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Osasuna ST; Spain depth striker; squad rotation option; limited WC minutes expected',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth ST; Osasuna La Liga', tier_revised='3'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Spain': continue
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
