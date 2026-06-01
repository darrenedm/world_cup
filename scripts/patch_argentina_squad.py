#!/usr/bin/env python3
"""
patch_argentina_squad.py — official 26-man squad (Scaloni, announced May 28 2026).
Group J: Argentina(10.0), Austria(5.9), Algeria(4.9), Jordan(2.5).
Advance 90%, dead rubber G3 10%.
Key fitness: Romero (partial MCL, may miss opener; Scaloni "hopeful just in time"),
             Paredes (hamstring May 30; opener serious doubt),
             Messi (minor muscular fatigue; expected fully fit).
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 90, 10
T1G, T1K = 89.0, 256
T2G, T2K = 76.0, 210
T3G, T3K = 48.0, 148
T4G, T4K = 18.0, 44

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Emiliano Martínez', position='GK', sub_position='', club='Aston Villa', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=256,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Aston Villa GK; Argentina undisputed No.1; world-class shot-stopper; hero from 2022 WC penalty shootout',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; Aston Villa PL', tier_revised='GK1'),
    dict(player='Gerónimo Rulli', position='GK', sub_position='', club='Olympique Marseille', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=5,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Marseille GK; Argentina No.2; experienced European performer; no WC starts expected',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Marseille Ligue 1', tier_revised='GK2'),
    dict(player='Juan Musso', position='GK', sub_position='', club='Atlético Madrid', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atlético Madrid GK; Argentina No.3; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Atlético Madrid La Liga', tier_revised='GK3'),
    # Defenders
    dict(player='Cristian Romero', position='DEF', sub_position='CB', club='Tottenham Hotspur', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='Spurs CB; Argentina first-choice CB; partial MCL tear April; targeting opener June 16; '
               'Scaloni "hopeful he makes it just in time"; no pre-tournament friendly; most important defensive player',
         int_l5_pattern='90/90/DNP/sub/90', int_l5_starts=3, int_absence_reason='Partial MCL tear April 2026',
         fitness_current='Partial MCL; targeting June 16 opener; Scaloni cautiously optimistic', tier_revised='1'),
    dict(player='Lisandro Martínez', position='DEF', sub_position='CB', club='Manchester United', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Man Utd CB; Argentina elite centre-back; returned from long injury; fierce tackler and leader',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit; returned from extended injury; match-sharp', tier_evidence='First-choice CB; Man Utd PL', tier_revised='1'),
    dict(player='Nahuel Molina', position='DEF', sub_position='RB', club='Atlético Madrid', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atlético Madrid RB; Argentina first-choice right-back; energetic and attacking; La Liga quality',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; Atlético Madrid La Liga', tier_revised='1'),
    dict(player='Nicolás Otamendi', position='DEF', sub_position='CB', club='Benfica', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Benfica CB; veteran Argentina international; experienced cover; steps up if Romero misses',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran CB cover; Benfica Primeira Liga', tier_revised='2'),
    dict(player='Leonardo Balerdi', position='DEF', sub_position='CB', club='Olympique Marseille', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Marseille CB; Argentina rotation centre-back; solid Ligue 1 performer; squad depth',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Marseille Ligue 1', tier_revised='2'),
    dict(player='Nicolás Tagliafico', position='DEF', sub_position='LB', club='Olympique Lyonnais', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Lyon LB; experienced Argentina left-back; attacking full-back; solid squad option',
         int_l5_pattern='90/90/sub/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular LB; Lyon Ligue 1', tier_revised='2'),
    dict(player='Gonzalo Montiel', position='DEF', sub_position='RB', club='River Plate', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='River Plate RB; penalty hero from 2022 WC final; rotation cover for Molina; returned to Argentina',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation RB; River Plate Argentine Primera', tier_revised='3'),
    dict(player='Facundo Medina', position='DEF', sub_position='CB', club='Olympique Marseille', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Marseille CB/LB; versatile defensive depth; squad cover behind main CB pairing',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CB/LB; Marseille Ligue 1', tier_revised='3'),
    dict(player='Valentín Barco', position='DEF', sub_position='LB', club='Strasbourg', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Strasbourg LB/LW; officially listed as MID by Argentina FA but primarily a left-back/wing-back hybrid; versatile squad depth',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Versatile LB/LW depth; Strasbourg Ligue 1', tier_revised='3'),
    # Midfielders
    dict(player='Alexis Mac Allister', position='MID', sub_position='CM', club='Liverpool', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Liverpool CM/DM; Argentina midfield anchor; superb technical quality; key Premier League performer',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed starter; Liverpool PL', tier_revised='1'),
    dict(player='Enzo Fernández', position='MID', sub_position='CM', club='Chelsea', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Chelsea CM; Argentina creative midfielder; excellent technical quality and vision; key creative link',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key starter; Chelsea PL', tier_revised='1'),
    dict(player='Rodrigo De Paul', position='MID', sub_position='CM', club='Inter Miami', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Inter Miami CM; Argentina engine; moved to Inter Miami alongside Messi; combative and dynamic; WC 2022 hero',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Automatic starter; Inter Miami MLS', tier_revised='1'),
    dict(player='Exequiel Palacios', position='MID', sub_position='DM', club='Bayer Leverkusen', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Leverkusen DM/CM; defensive cover in midfield; Bundesliga quality; rotation and depth option',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation DM/CM; Leverkusen Bundesliga', tier_revised='2'),
    dict(player='Giovani Lo Celso', position='MID', sub_position='AM', club='Real Betis', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Real Betis AM/CM; creative midfield depth; technical quality; rotation option behind main trio',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation AM/CM; Real Betis La Liga', tier_revised='2'),
    dict(player='Leandro Paredes', position='MID', sub_position='DM', club='Boca Juniors', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='Boca Juniors DM; hamstring tear May 30; misses both pre-WC friendlies; '
               'opener June 16 in serious doubt; Scaloni "hopeful"; key midfield screen if fit',
         int_l5_pattern='90/90/DNP/sub/90', int_l5_starts=3, int_absence_reason='Hamstring tear May 30 2026',
         fitness_current='Hamstring; misses friendlies; June 16 opener in serious doubt', tier_revised='2'),
    dict(player='Thiago Almada', position='MID', sub_position='AM', club='Atlético Madrid', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atlético Madrid AM/CM; creative attacking midfielder; technical and direct; quality rotation option',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation AM; Atlético Madrid La Liga', tier_revised='2'),
    # Forwards
    dict(player='Lionel Messi', position='FWD', sub_position='', club='Inter Miami', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Inter Miami RW/AM; greatest of all time; 8th WC; "muscular overload" fatigue flagged May 25 — '
               'not a tear; Scaloni and Inter Miami both downplayed; expected fully fit for June 6 friendly and tournament',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit; minor muscular fatigue flag (May 25); expected fully fit', tier_evidence='GOAT; Inter Miami MLS', tier_revised='1'),
    dict(player='Lautaro Martínez', position='FWD', sub_position='', club='Inter Milan', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Inter Milan ST; Argentina first-choice striker; prolific goalscorer; clinical and physical; Inter Serie A star',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice striker; Inter Milan Serie A', tier_revised='1'),
    dict(player='Julián Álvarez', position='FWD', sub_position='', club='Atlético Madrid', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atlético Madrid ST; Argentina world-class forward; 2022 WC golden boot co-winner; explosive and goalscoring',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key forward; Atlético Madrid La Liga', tier_revised='1'),
    dict(player='Nico Paz', position='FWD', sub_position='', club='Como', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Como AM/RW; breakout Serie A season; 21 yrs; Real Madrid-owned; exciting creative option; carries a threat',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation AM/RW; Como Serie A', tier_revised='2'),
    dict(player='Nicolás González', position='FWD', sub_position='', club='Atlético Madrid', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atlético Madrid LW/ST; dynamic wide attacker; goals and assists; versatile forward cover',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation LW/ST; Atlético Madrid La Liga', tier_revised='2'),
    dict(player='Giuliano Simeone', position='FWD', sub_position='', club='Atlético Madrid', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Atlético Madrid RW/LW; son of Diego Simeone; new call-up; energetic and pacey wide option; squad depth',
         int_l5_pattern='sub/90/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young depth winger; Atlético Madrid La Liga', tier_revised='3'),
    dict(player='José Manuel López', position='FWD', sub_position='', club='Palmeiras', nationality='Argentina', group='J',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Palmeiras ST; depth striker; Brazilian Série A; fringe squad selection; limited WC minutes expected',
         int_l5_pattern='sub/DNP/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe depth striker; Palmeiras Série A Brazil', tier_revised='4'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Argentina': continue
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
