#!/usr/bin/env python3
"""
patch_morocco_squad.py — official 26-man squad (Regragui, announced May 2026).
Group C: Morocco(8.3), Brazil(7.9), Scotland(5.0), Haiti(1.2).
Advance 68%, dead rubber G3 10%.
Key fitness: Hakimi (thigh strain May 2026; doubt for opener June 10 vs Haiti; targeting G2 June 13).
Generational shift: En-Nesyri, Ziyech, Saiss all OUT — new generation takes over.
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 68, 10
T1G, T1K = 87.1, 115
T2G, T2K = 74.0, 94
T3G, T3K = 42.0, 67
T4G, T4K = 16.0, 20

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Yassine Bounou', position='GK', sub_position='', club='Al-Hilal', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=115,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Hilal GK; Morocco undisputed No.1; WC 2022 penalty shootout hero; elite shot-stopper',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; Al-Hilal Saudi Pro League', tier_revised='GK1'),
    dict(player='Anas Zniti', position='GK', sub_position='', club='Raja Casablanca', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=5,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Raja Casablanca GK; Morocco No.2; experienced domestic backup; no WC starts expected',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Raja Casablanca Botola Pro', tier_revised='GK2'),
    dict(player='Ahmad Reda Tagnaouti', position='GK', sub_position='', club='Wydad AC', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Wydad AC GK; Morocco No.3; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Wydad AC Botola Pro', tier_revised='GK3'),
    # Defenders
    dict(player='Achraf Hakimi', position='DEF', sub_position='RWB', club='Paris Saint-Germain', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='PSG RWB; Morocco captain and best player; thigh strain May 2026; doubt for opener June 10 vs Haiti; '
               'targeting G2 June 13 vs Scotland; Regragui cautiously optimistic about G2 return',
         int_l5_pattern='90/90/sub/sub/90', int_l5_starts=3, int_absence_reason='Thigh strain May 2026',
         fitness_current='Thigh strain; doubt for opener; targeting G2; Regragui cautiously optimistic', tier_revised='1'),
    dict(player='Nayef Aguerd', position='DEF', sub_position='CB', club='Crystal Palace', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Crystal Palace CB; Morocco first-choice centre-back; commanding aerial presence; Premier League quality',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Crystal Palace PL', tier_revised='1'),
    dict(player='Noussair Mazraoui', position='DEF', sub_position='LWB', club='Manchester United', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Man United LWB/RB; Morocco versatile first-choice full-back; covers LWB; Premier League quality',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice full-back; Man United PL', tier_revised='1'),
    dict(player='Yahia Attiyat Allah', position='DEF', sub_position='LB', club='Wydad AC', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Wydad AC LB; Morocco regular left-back; reliable in Regragui defensive system; strong in set-pieces',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular LB; Wydad AC Botola Pro', tier_revised='2'),
    dict(player='Jawad El Yamiq', position='DEF', sub_position='CB', club='Real Betis', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Real Betis CB; Morocco second-choice CB; experienced La Liga defender; partners Aguerd',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Second-choice CB; Real Betis La Liga', tier_revised='2'),
    dict(player='Adam Aznou', position='DEF', sub_position='LWB', club='Bayern Munich', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Bayern Munich LWB; Morocco exciting young full-back; Bundesliga quality; powerful overlapping runs',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young LWB; Bayern Munich Bundesliga', tier_revised='2'),
    dict(player='Samy Mmaee', position='DEF', sub_position='CB', club='Sparta Prague', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Sparta Prague CB; Morocco CB depth; reliable cover for Aguerd/El Yamiq',
         int_l5_pattern='90/sub/DNP/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB depth; Sparta Prague Czech Fortuna Liga', tier_revised='3'),
    dict(player='Badr Benoun', position='DEF', sub_position='CB', club='Wydad AC', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Wydad AC CB; Morocco domestic stalwart; squad depth CB; covers if Aguerd/El Yamiq injured',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB depth; Wydad AC Botola Pro', tier_revised='3'),
    dict(player='Abdourahmane Sidibé', position='DEF', sub_position='RB', club='Boavista', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Boavista RB; Morocco right-back cover; Portuguese Primeira Liga experience; covers Hakimi/Mazraoui',
         int_l5_pattern='sub/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='RB depth; Boavista Primeira Liga', tier_revised='3'),
    # Midfielders
    dict(player='Sofyan Amrabat', position='MID', sub_position='DM', club='Al-Ittihad', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Ittihad DM; Morocco defensive engine; WC 2022 standout; elite ball-winner and presser; anchors midfield',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed DM starter; Al-Ittihad Saudi Pro League', tier_revised='1'),
    dict(player='Azzedine Ounahi', position='MID', sub_position='CM', club='Olympique Marseille', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Marseille CM; Morocco first-choice box-to-box midfielder; dynamic and tireless; creative spark in transition',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CM; Marseille Ligue 1', tier_revised='1'),
    dict(player='Selim Amallah', position='MID', sub_position='CM', club='Sevilla FC', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Sevilla CM; Morocco regular central midfielder; progressive ball-carrier; useful in transition',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM; Sevilla La Liga', tier_revised='2'),
    dict(player='Ilias Chair', position='MID', sub_position='AM', club='Queens Park Rangers', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='QPR AM; Morocco creative attacking midfielder; technical dribbler; key link between midfield and attack',
         int_l5_pattern='90/90/sub/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular AM; QPR Championship', tier_revised='2'),
    dict(player='Amine Harit', position='MID', sub_position='AM', club='Olympique Marseille', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Marseille AM; Morocco second attacking midfielder option; creative and technically gifted; Ligue 1 quality',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation AM; Marseille Ligue 1', tier_revised='2'),
    dict(player='Yahya Jabrane', position='MID', sub_position='DM', club='Wydad AC', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Wydad AC DM; Morocco veteran midfielder; domestic stalwart; squad depth cover for Amrabat',
         int_l5_pattern='sub/sub/90/DNP/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='DM depth; Wydad AC Botola Pro', tier_revised='3'),
    dict(player='Abdelouahab Benhaima', position='MID', sub_position='CM', club='FUS Rabat', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FUS Rabat CM; Morocco domestic midfielder; squad depth; unlikely to feature unless injury crisis',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; FUS Rabat Botola Pro', tier_revised='3'),
    # Forwards
    dict(player='Ayoub El Kaabi', position='FWD', sub_position='CF', club='Olympiacos', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Olympiacos CF; Morocco first-choice striker; prolific goal-scorer; Europa Conference League top scorer; '
               'replaces En-Nesyri as No.9; clinical in the box',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CF; Olympiacos Super League/ECL', tier_revised='1'),
    dict(player='Brahim Díaz', position='FWD', sub_position='WNG', club='AC Milan', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='AC Milan WNG/AM; Morocco star attacker; Spanish-born choosing Morocco; Regragui favourite; '
               'creative and direct; plays left wing or #10; key playmaker in new-look Morocco attack',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice WNG/AM; AC Milan Serie A', tier_revised='1'),
    dict(player='Abdessamad Ezzalzouli', position='FWD', sub_position='WNG', club='Real Betis', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Real Betis RW; Morocco pacey right winger; direct dribbler; La Liga experience; rotation with Brahim Díaz',
         int_l5_pattern='90/90/sub/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular RW; Real Betis La Liga', tier_revised='2'),
    dict(player='Soufiane Rahimi', position='FWD', sub_position='WNG', club='Al-Ain', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Ain WNG; Morocco pacey wide attacker; former AFC Champions League top scorer; electric pace; direct threat',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular winger; Al-Ain UAE Pro League', tier_revised='2'),
    dict(player='Ilias Talbi', position='FWD', sub_position='WNG', club='Stade Rennais', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Rennais WNG; Morocco young winger; Ligue 1 talent; impact sub option; brings pace from the bench',
         int_l5_pattern='sub/sub/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young winger; Stade Rennais Ligue 1', tier_revised='3'),
    dict(player='Bilal Amaimouni', position='FWD', sub_position='WNG', club='Wydad AC', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Wydad AC WNG; Morocco domestic attacker; squad depth in wide areas; unlikely to feature unless injuries',
         int_l5_pattern='sub/DNP/90/sub/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Winger depth; Wydad AC Botola Pro', tier_revised='3'),
    dict(player='Nassim Gessime', position='FWD', sub_position='WNG', club='Stade de Reims', nationality='Morocco', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Reims WNG; Morocco French-born winger; Ligue 1 experience; fringe squad selection; attacking depth option',
         int_l5_pattern='sub/DNP/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe winger depth; Reims Ligue 1', tier_revised='3'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Morocco': continue
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
