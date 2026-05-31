#!/usr/bin/env python3
"""
patch_turkey_squad.py  —  35-man preliminary squad (Montella, May 18 2026).
Final 26 due June 2. All listed players set to 100%; 9 fringe players set at 85%.
Group D: USA(7.1), Turkey(5.8), Australia(5.6), Paraguay(4.6).
Advance 65%, dead rubber G3 10%.
Key fitness: Çalhanoğlu (soleus strain, exp. fit), Güler (hamstring, conf. fit),
             Yıldız (calf, doubt for opener).
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 65, 10
T1G, T1K = 87.1, 101
T2G, T2K = 74.0, 83
T3G, T3K = 42.0, 47
T4G, T4K = 16.0, 12

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Uğurcan Çakır', position='GK', sub_position='', club='Galatasaray', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=101,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Galatasaray GK; Turkey undisputed No.1 under Montella; commanding presence',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; Galatasaray Turkish Super Lig', tier_revised='GK1'),
    dict(player='Altay Bayındır', position='GK', sub_position='', club='Manchester United', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=5,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Man Utd GK; Turkey No.2; experienced international; no WC starts expected',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Man Utd PL squad', tier_revised='GK2'),
    dict(player='Ersin Destanoğlu', position='GK', sub_position='', club='Beşiktaş', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Beşiktaş GK; Turkey No.3; promising young keeper; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Turkish Super Lig', tier_revised='GK3'),
    # Defenders
    dict(player='Zeki Çelik', position='DEF', sub_position='RB', club='AS Roma', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Roma RB; Turkey first-choice right-back; energetic and reliable; Serie A quality',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; Roma Serie A', tier_revised='1'),
    dict(player='Ferdi Kadıoğlu', position='DEF', sub_position='LB', club='Fulham', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Fulham LB; Turkey first-choice left-back; technical and attack-minded; PL quality',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; PL quality', tier_revised='1'),
    dict(player='Merih Demiral', position='DEF', sub_position='CB', club='Al-Ahli', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Al-Ahli CB; Turkey starting centre-back; commanding and physical; experienced international',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Starting CB; Saudi Pro League', tier_revised='1'),
    dict(player='Abdülkerim Bardakcı', position='DEF', sub_position='CB', club='Galatasaray', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Galatasaray CB; Turkey defensive partner; strong and consistent; Turkish champion experience',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB; Galatasaray Super Lig', tier_revised='2'),
    dict(player='Ozan Kabak', position='DEF', sub_position='CB', club='Hoffenheim', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Hoffenheim CB; Turkey depth CB; experienced European performer; squad cover',
         int_l5_pattern='90/sub/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Bundesliga', tier_revised='2'),
    dict(player='Mert Müldür', position='DEF', sub_position='RB', club='Fenerbahçe', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Fenerbahçe RB; Turkey rotation right-back; squad cover for Çelik',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation RB; Turkish Super Lig', tier_revised='3'),
    dict(player='Çağlar Söyüncü', position='DEF', sub_position='CB', club='Fenerbahçe', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Fenerbahçe CB; veteran Turkey international; experienced squad depth; former Leicester',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran CB depth; Super Lig', tier_revised='3'),
    dict(player='Ahmetcan Kaplan', position='DEF', sub_position='CB', club='Ajax', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Ajax CB (on loan NEC); young Turkey CB; depth option; promising Eredivisie performer',
         int_l5_pattern='90/sub/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young depth CB; Eredivisie', tier_revised='3'),
    # Midfielders
    dict(player='Hakan Çalhanoğlu', position='MID', sub_position='DM', club='Inter Milan', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='Inter Milan DM; Turkey captain; world-class regista; soleus strain April 27; '
               'tailored recovery; expected fit but needs sharpness; key player if available',
         int_l5_pattern='90/DNP/sub/90/90', int_l5_starts=3, int_absence_reason='Soleus strain April 27',
         fitness_current='Soleus strain; expected fit for tournament; monitoring closely', tier_revised='1'),
    dict(player='Arda Güler', position='MID', sub_position='AM', club='Real Madrid', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Real Madrid AM; Turkey creative genius (21); biceps femoris injury April 21; '
               'confirmed fit by Fabrizio Romano; arrives rested; expected to start',
         int_l5_pattern='90/90/DNP/sub/90', int_l5_starts=3, int_absence_reason='Biceps femoris April 21; now recovered',
         fitness_current='Fit; fully recovered; arriving rested from Real Madrid', tier_revised='1'),
    dict(player='Orkun Kökçü', position='MID', sub_position='CM', club='Beşiktaş', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Beşiktaş CM; creative Turkey midfielder; excellent technical quality; squad regular',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM; Turkish Super Lig', tier_revised='2'),
    dict(player='İsmail Yüksek', position='MID', sub_position='DM', club='Fenerbahçe', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Fenerbahçe DM; combative defensive midfield partner; reliable starter in Montella system',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular DM; Super Lig quality', tier_revised='2'),
    dict(player='Salih Özcan', position='MID', sub_position='CM', club='Borussia Dortmund', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Dortmund CM; box-to-box; Bundesliga experience; Turkey rotation option',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Dortmund Bundesliga', tier_revised='3'),
    dict(player='Atakan Karazor', position='MID', sub_position='DM', club='VfB Stuttgart', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Stuttgart DM; defensive anchor; Bundesliga quality; depth option behind Çalhanoğlu',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation DM; Stuttgart Bundesliga', tier_revised='3'),
    dict(player='Kaan Ayhan', position='MID', sub_position='CM', club='Galatasaray', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Galatasaray CM; versatile midfield depth; squad rotation option',
         int_l5_pattern='sub/90/DNP/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Turkish Super Lig', tier_revised='3'),
    dict(player='Demir Ege Tıknaz', position='MID', sub_position='CM', club='SC Braga', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Braga CM; young Turkey talent; next generation; limited WC minutes expected',
         int_l5_pattern='sub/DNP/sub/DNP/sub', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young depth CM; Braga Primeira Liga', tier_revised='4'),
    # Forwards
    dict(player='Kenan Yıldız', position='FWD', sub_position='', club='Juventus', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Doubtful',
         notes='Juventus LW (21); Turkey\'s most dangerous wide threat; calf strain in training; '
               '~3-week layoff; doubtful for June 13 opener vs Australia; key player when fit',
         int_l5_pattern='90/90/90/DNP/sub', int_l5_starts=3, int_absence_reason='Calf strain in training May 2026',
         fitness_current='Calf strain; doubt for opener; targeting return Game 2', tier_revised='1'),
    dict(player='Kerem Aktürkoğlu', position='FWD', sub_position='', club='Fenerbahçe', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Fenerbahçe winger; pacey and direct; Turkey key wide threat; under individual fitness program',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit; individual fitness supervision', tier_evidence='Regular winger; Super Lig quality', tier_revised='2'),
    dict(player='Barış Alper Yılmaz', position='FWD', sub_position='', club='Galatasaray', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Galatasaray wide attacker; key squad member; versatile across front line; Montella regular',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular wide attacker; Galatasaray Super Lig', tier_revised='2'),
    dict(player='Can Uzun', position='FWD', sub_position='', club='Eintracht Frankfurt', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Frankfurt AM/forward (20); young goal threat; direct and technically gifted; Bundesliga quality',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Goal threat; Eintracht Frankfurt Bundesliga', tier_revised='2'),
    dict(player='Deniz Gül', position='FWD', sub_position='', club='FC Porto', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Porto forward (21); young striker; confirmed in final 26; squad rotation option',
         int_l5_pattern='sub/90/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young striker; Porto Primeira Liga', tier_revised='3'),
    dict(player='Yunus Akgün', position='FWD', sub_position='', club='Galatasaray', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Galatasaray wide forward; Turkey depth option; limited WC minutes expected',
         int_l5_pattern='sub/DNP/sub/DNP/sub', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe wide forward; Super Lig', tier_revised='4'),
    dict(player='İrfan Can Kahveci', position='FWD', sub_position='', club='Kasımpaşa', nationality='Turkey', group='D',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=T4K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Kasımpaşa winger; experienced Turkey option; squad cover; limited WC minutes expected',
         int_l5_pattern='sub/DNP/DNP/sub/sub', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe winger; Super Lig', tier_revised='4'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Turkey': continue
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
