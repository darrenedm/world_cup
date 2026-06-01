#!/usr/bin/env python3
"""
patch_colombia_squad.py — official 26-man squad (Néstor Lorenzo, announced May 2026).
Group K: Portugal(8.6), Colombia(7.3), Uzbekistan(3.9), DR Congo(3.3).
Advance 72%, dead rubber G3 10%.
Key notes: James Rodríguez captain and creative force; Luis Díaz at Bayern Munich (26G+23A season);
           Durán OUT (disciplinary reasons); Richard Ríos now at Benfica;
           Cucho Hernández at Real Betis; Colombian attack loaded despite Durán absence.
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 72, 10
T1G, T1K = 87.1, 136
T2G, T2K = 74.0, 112
T3G, T3K = 42.0, 79
T4G, T4K = 16.0, 23

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Camilo Vargas', position='GK', sub_position='', club='Atlas FC', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=136,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atlas FC GK; Colombia undisputed No.1; experienced international; solid shot-stopper',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; Atlas FC Liga MX', tier_revised='GK1'),
    dict(player='Aldaír Quintana', position='GK', sub_position='', club='Atlético Nacional', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=5,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atlético Nacional GK; Colombia No.2; experienced domestic backup; no WC starts expected',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Atlético Nacional Primera A', tier_revised='GK2'),
    dict(player='Kevin Mier', position='GK', sub_position='', club='Atlético Nacional', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atlético Nacional GK; Colombia No.3; young domestic talent; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Atlético Nacional Primera A', tier_revised='GK3'),
    # Defenders
    dict(player='Dávinson Sánchez', position='DEF', sub_position='CB', club='Atlético Madrid', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atlético Madrid CB; Colombia first-choice veteran CB; experienced European defender; physical and commanding',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Atlético Madrid La Liga', tier_revised='1'),
    dict(player='Daniel Muñoz', position='DEF', sub_position='RB', club='Crystal Palace', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Crystal Palace RB; Colombia first-choice right-back; dynamic and attacking; Premier League quality',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; Crystal Palace PL', tier_revised='1'),
    dict(player='Jhon Lucumí', position='DEF', sub_position='CB', club='Bologna', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Bologna CB; Colombia second first-choice CB; Serie A quality; composed and dominant in the air',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Bologna Serie A', tier_revised='1'),
    dict(player='Johan Mojica', position='DEF', sub_position='LB', club='Girona FC', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Girona LB; Colombia first-choice left-back; attacking full-back; La Liga quality; overlapping runs',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; Girona La Liga', tier_revised='2'),
    dict(player='Carlos Cuesta', position='DEF', sub_position='CB', club='Genk', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Genk CB; Colombia rotation centre-back; Belgian Pro League experience; solid squad depth option',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Genk Belgian Pro League', tier_revised='2'),
    dict(player='Óscar Murillo', position='DEF', sub_position='CB', club='Watford', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Watford CB; Colombia experienced third CB option; depth cover behind Sánchez/Lucumí pairing',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB depth; Watford Championship', tier_revised='2'),
    dict(player='Déiver Machado', position='DEF', sub_position='LB', club='Espanyol', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Espanyol LB; Colombia squad left-back; La Liga experience; covers Mojica; limited WC minutes expected',
         int_l5_pattern='sub/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='LB depth; Espanyol La Liga', tier_revised='3'),
    dict(player='William Tesillo', position='DEF', sub_position='CB', club='Club Nacional', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Club Nacional CB; Colombia veteran defensive stalwart; depth option; Uruguayan Primera Liga',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran CB depth; Club Nacional Uruguay', tier_revised='3'),
    # Midfielders
    dict(player='James Rodríguez', position='MID', sub_position='AM', club='Rayo Vallecano', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Rayo Vallecano AM; Colombia captain; 2014 WC golden boot winner; still Colombia\'s creative heartbeat; '
               'playmaking excellence; key to unlocking defences from deep',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain and playmaker; Rayo Vallecano La Liga', tier_revised='1'),
    dict(player='Richard Ríos', position='MID', sub_position='CM', club='Benfica', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Benfica CM; Colombia box-to-box midfielder; impressive Copa América 2024; now establishing at Benfica; '
               'powerful runner with excellent pressing and carrying',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key starter; Benfica Primeira Liga', tier_revised='1'),
    dict(player='Jefferson Lerma', position='MID', sub_position='DM', club='Crystal Palace', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Crystal Palace DM; Colombia defensive midfielder anchor; combative ball-winner; experienced PL performer',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Defensive anchor DM; Crystal Palace PL', tier_revised='1'),
    dict(player='Wilmar Barrios', position='MID', sub_position='DM', club='Tigres UANL', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Tigres DM; Colombia veteran DM rotation; solid ball-winner; experienced international; covers Lerma',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation DM; Tigres UANL Liga MX', tier_revised='2'),
    dict(player='Gustavo Puerta', position='MID', sub_position='CM', club='Bayer Leverkusen', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Leverkusen CM; Colombia young midfield talent; Bundesliga quality; dynamic and technically gifted; emerging force',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Leverkusen Bundesliga', tier_revised='2'),
    dict(player='Jorge Carrascal', position='MID', sub_position='AM', club='River Plate', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='River Plate AM; Colombia creative squad option; explosive dribbler and creator; rotation behind James',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation AM; River Plate Argentine Primera', tier_revised='2'),
    dict(player='Andrés Andrade', position='MID', sub_position='CM', club='Millonarios', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Millonarios CM; Colombia domestic squad depth; unlikely to feature unless injury crisis',
         int_l5_pattern='DNP/sub/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; Millonarios Primera A', tier_revised='3'),
    dict(player='Jorman Campuzano', position='MID', sub_position='DM', club='San Lorenzo', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='San Lorenzo DM; Colombia squad depth DM; combative midfielder; fringe selection',
         int_l5_pattern='sub/DNP/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='DM depth; San Lorenzo Argentine Primera', tier_revised='3'),
    # Forwards
    dict(player='Luis Díaz', position='FWD', sub_position='WNG', club='Bayern Munich', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Bayern Munich LW; Colombia and tournament-level superstar; extraordinary 2025-26 at Bayern (26G+23A); '
               'electric pace, dribbling, and finishing; one of the most dangerous players at WC 2026',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='World-class LW; Bayern Munich Bundesliga', tier_revised='1'),
    dict(player='Cucho Hernández', position='FWD', sub_position='CF', club='Real Betis', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Real Betis CF; Colombia first-choice No.9 post-Durán exclusion; electric and powerful; acrobatic goals; '
               'La Liga quality; key to pressing and direct play under Lorenzo',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CF; Real Betis La Liga', tier_revised='1'),
    dict(player='Rafael Santos Borré', position='FWD', sub_position='CF', club='Eintracht Frankfurt', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Frankfurt CF; Colombia rotation striker; solid Bundesliga performer; physical and aerial threat; covers Cucho',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CF; Frankfurt Bundesliga', tier_revised='2'),
    dict(player='Daniel Campaz', position='FWD', sub_position='WNG', club='Tigres UANL', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Tigres RW; Colombia electric right winger; exceptional dribbler; pacey and direct; rotation with Ezzalzouli',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation RW; Tigres UANL Liga MX', tier_revised='2'),
    dict(player='Jhon Córdoba', position='FWD', sub_position='CF', club='Krasnodar', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Krasnodar CF; Colombia physical striker; prolific scorer in Russian Premier League; depth option behind Cucho',
         int_l5_pattern='sub/sub/90/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CF; Krasnodar RPL', tier_revised='2'),
    dict(player='Yaser Asprilla', position='FWD', sub_position='WNG', club='Watford', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Watford WNG; Colombia son of Faustino Asprilla; exciting young winger; direct and energetic; squad depth',
         int_l5_pattern='sub/sub/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young winger depth; Watford Championship', tier_revised='3'),
    dict(player='Brayan Rodríguez', position='FWD', sub_position='WNG', club='Gent', nationality='Colombia', group='K',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Gent WNG; Colombia exciting young winger; Belgian Pro League; pace and directness; fringe squad selection',
         int_l5_pattern='sub/DNP/sub/90/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young winger depth; Gent Belgian Pro League', tier_revised='3'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Colombia': continue
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
