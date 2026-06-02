#!/usr/bin/env python3
"""
patch_algeria_squad.py — official 26-man squad (Vladimir Petkovic, announced May 31 2026).
Group J: Argentina(10.0), Austria(5.9), Algeria(4.9), Jordan(2.5).
Advance 22%, dead rubber G3 10%.
KEY NOTES: Riyad Mahrez (Al-Ahli, Saudi) confirmed as captain — his farewell World Cup
at age 35 (113 caps, 38 goals). Notable omission: Ismael Bennacer dropped by Petkovic.
Luca Zidane (son of Zinedine) starts in goal (Granada). Ibrahim Maza (Bayer Leverkusen,
22) is the exciting young talent. Rayan Ait-Nouri (Man City) provides attacking LB option.
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 22, 10
T1G, T1K = 87.1, 5
T2G, T2K = 74.0, 4
T3G, T3K = 42.0, 3
T4G, T4K = 16.0, 1

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Luca Zidane', position='GK', sub_position='', club='Granada CF', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Granada GK; Algeria No.1; son of Zinedine Zidane; Spanish Segunda experience; Petkovic\'s first choice',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed No.1; Granada Spanish Segunda', tier_revised='GK1'),
    dict(player='Oussama Benbot', position='GK', sub_position='', club='USM Alger', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=1,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='USM Alger GK; Algeria No.2; solid domestic Algerian league performer; backup cover',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; USM Alger Algerian Ligue Professionnelle', tier_revised='GK2'),
    dict(player='Melvin Mastil', position='GK', sub_position='', club='Stade Nyonnais', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Stade Nyonnais GK (Switzerland); Algeria No.3; Swiss lower league; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Stade Nyonnais Swiss lower leagues', tier_revised='GK3'),
    # Defenders
    dict(player='Aissa Mandi', position='DEF', sub_position='CB', club='LOSC Lille', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Lille CB; Algeria all-time caps leader (116); experienced leader at the back; Ligue 1 quality; essential defensive anchor',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Record caps holder; Lille Ligue 1', tier_revised='1'),
    dict(player='Ramy Bensebaini', position='DEF', sub_position='LB', club='Borussia Dortmund', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Borussia Dortmund LB; Algeria attacking left-back; powerful and goal-scoring; Bundesliga quality; key outlet down the left',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; BVB Bundesliga', tier_revised='1'),
    dict(player='Rayan Ait-Nouri', position='DEF', sub_position='LB', club='Manchester City', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Manchester City LB; Algeria pacy and attacking full-back; Premier League quality; can also play LWB; strong going forward',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='PL LB; Manchester City PL', tier_revised='1'),
    dict(player='Rafik Belghali', position='DEF', sub_position='CB', club='Hellas Verona', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hellas Verona CB; Algeria solid central defender; Serie A experience; rotation cover alongside Mandi',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Hellas Verona Serie A', tier_revised='2'),
    dict(player='Jaouen Hadjam', position='DEF', sub_position='LB', club='BSC Young Boys', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Young Boys LB; Algeria rotation left-back; Swiss Super League; cover for Bensebaini and Ait-Nouri',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation LB; BSC Young Boys Swiss Super League', tier_revised='2'),
    dict(player='Samir Chergui', position='DEF', sub_position='CB', club='Red Star FC', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Red Star FC (France) CB; Algeria squad depth; French lower league performer; limited WC minutes expected',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CB; Red Star FC Ligue 2', tier_revised='3'),
    dict(player='Zineddine Belaid', position='DEF', sub_position='CB', club='JS Kabylie', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='JS Kabylie CB; Algeria domestic defender; CAF presence; squad depth cover',
         int_l5_pattern='sub/DNP/DNP/90/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CB; JS Kabylie Algerian Ligue', tier_revised='3'),
    dict(player='Achref Abada', position='DEF', sub_position='RB', club='USM Alger', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='USM Alger RB; Algeria right-back option; domestic league performer; squad cover on the right',
         int_l5_pattern='sub/DNP/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth RB; USM Alger Algerian Ligue', tier_revised='3'),
    dict(player='Mohamed Amine Tougai', position='DEF', sub_position='CB', club='Esperance de Tunis', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='4', playing_role='Squad Player',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Esperance de Tunis CB; Algeria fringe defender; Tunisian league performer; very limited WC minutes expected',
         int_l5_pattern='sub/DNP/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CB; Esperance de Tunis Tunisian Ligue', tier_revised='4'),
    # Midfielders
    dict(player='Ibrahim Maza', position='MID', sub_position='AM', club='Bayer Leverkusen', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Bayer Leverkusen AM; Algeria exciting young playmaker; 22 yrs; Bundesliga title winner; creative and direct; key offensive player',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key AM; Bayer Leverkusen Bundesliga', tier_revised='1'),
    dict(player='Houssem Aouar', position='MID', sub_position='CM', club='Al-Ittihad', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Ittihad CM; Algeria experienced creative midfielder; former Lyon star; Saudi Pro League; technical and intelligent passer',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Experienced CM; Al-Ittihad Saudi Pro League', tier_revised='1'),
    dict(player='Fares Chaibi', position='MID', sub_position='CM', club='Eintracht Frankfurt', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Eintracht Frankfurt CM; Algeria dynamic box-to-box midfielder; Bundesliga quality; rotation midfield option',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Eintracht Frankfurt Bundesliga', tier_revised='2'),
    dict(player='Hicham Boudaoui', position='MID', sub_position='CM', club='OGC Nice', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='OGC Nice CM; Algeria energetic midfield presence; Ligue 1 regular; combative and box-to-box; rotation option',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; OGC Nice Ligue 1', tier_revised='2'),
    dict(player='Nabil Bentaleb', position='MID', sub_position='DM', club='LOSC Lille', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Lille DM; Algeria midfield anchor; former Spurs and Schalke; experienced holding midfielder; protects back four',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='DM anchor; LOSC Lille Ligue 1', tier_revised='2'),
    dict(player='Ramiz Zerrouki', position='MID', sub_position='DM', club='FC Twente', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FC Twente DM; Algeria solid defensive midfielder; Eredivisie performer; squad depth cover in midfield',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth DM; FC Twente Eredivisie', tier_revised='3'),
    dict(player='Yacine Titraoui', position='MID', sub_position='CM', club='Charleroi', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='4', playing_role='Squad Player',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Charleroi CM; Algeria fringe squad midfielder; Belgian Pro League; very limited WC minutes expected',
         int_l5_pattern='sub/DNP/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CM; Charleroi Belgian Pro League', tier_revised='4'),
    # Forwards
    dict(player='Riyad Mahrez', position='FWD', sub_position='WNG', club='Al-Ahli', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Ahli RW; Algeria captain; 113 caps 38 goals; former Man City; farewell WC at 35; tournament leader; exceptional dribbler and creator',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit; 35 yrs but confirmed fit for tournament', tier_evidence='Algeria captain; legend; Al-Ahli Saudi Pro League', tier_revised='1'),
    dict(player='Mohamed Amine Amoura', position='FWD', sub_position='WNG', club='VfL Wolfsburg', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Wolfsburg WNG; Algeria pacy and direct wide attacker; Bundesliga; prolific in domestic and international football; key starter',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key WNG; VfL Wolfsburg Bundesliga', tier_revised='1'),
    dict(player='Amine Gouiri', position='FWD', sub_position='CF', club='Olympique de Marseille', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Marseille CF/WNG; Algeria clinical attacker; Ligue 1 quality; can play CF or wide; technical and goal-scoring; key to frontline',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key CF/WNG; Olympique Marseille Ligue 1', tier_revised='1'),
    dict(player='Anis Hadj Moussa', position='FWD', sub_position='WNG', club='Feyenoord', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Feyenoord WNG; Algeria exciting wide attacker; Eredivisie; young and direct; rotation wide option behind Mahrez/Amoura',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation WNG; Feyenoord Eredivisie', tier_revised='2'),
    dict(player='Fares Ghedjemis', position='FWD', sub_position='CF', club='Frosinone', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Frosinone CF; Algeria squad attacker; Serie B Italy; impact sub option; limited WC minutes anticipated',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CF; Frosinone Serie B Italy', tier_revised='3'),
    dict(player='Nadhir Benbouali', position='FWD', sub_position='WNG', club='Gyor ETO FC', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='4', playing_role='Squad Player',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Gyor ETO FC (Hungary) WNG; Algeria fringe attacker; Hungarian league; very limited WC minutes expected',
         int_l5_pattern='sub/DNP/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe WNG; Gyor ETO FC Hungarian OTP Bank Liga', tier_revised='4'),
    dict(player='Adil Boulbina', position='FWD', sub_position='CF', club='Al-Duhail', nationality='Algeria', group='J',
         wc_squad_prob_pct=100, tier='4', playing_role='Squad Player',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Duhail (Qatar) CF; Algeria fringe striker; Qatar Stars League; very limited WC minutes expected',
         int_l5_pattern='sub/DNP/DNP/DNP/sub', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CF; Al-Duhail Qatar Stars League', tier_revised='4'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Algeria': continue
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
