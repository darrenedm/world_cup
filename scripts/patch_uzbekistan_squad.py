#!/usr/bin/env python3
"""
patch_uzbekistan_squad.py — official 26-man squad, Fabio Cannavaro, June 2 2026.
Group K: Portugal(8.6), Colombia(7.3), Uzbekistan(3.9), DR Congo(3.3).
Advance 12%, dead rubber G3 10%.
Uzbekistan's first-ever World Cup. Captain Eldor Shomurodov (Istanbul Başakşehir/ex-AS Roma).
Abdukodir Khusanov (Manchester City) is the highest-profile defender.
Cannavaro trimmed from 30-man provisional to 26. Four cut: Jakhongir Urozov, Behruz Karimov,
Ruslanbek Jiyanov, Umarali Rakhmonaliev (defenders from 30-man list absent in confirmed 26).
IMPORTANT: T4K=0 — T4 players get exp_post_group_mins_total=0.
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 12, 10
T1G, T1K = 85.0, 1
T2G, T2K = 68.0, 1
T3G, T3K = 35.0, 1
T4G, T4K = 10.0, 0

NEW_PLAYERS = [
    # --- Goalkeepers ---
    dict(player='Utkir Yusupov', position='GK', sub_position='', club='Foolad FC', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Foolad (Iran); Uzbekistan undisputed No.1; experienced stopper; marshals Cannavaro defensive shape',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; consistent WCQ starter', tier_revised='GK1'),
    dict(player='Botirali Ergashev', position='GK', sub_position='', club='Neftchi Fergana', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=1,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Neftchi Fergana; Uzbekistan No.2; no WC starts expected',
         int_l5_pattern='DNP/90/DNP/DNP/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; domestic league', tier_revised='GK2'),
    dict(player='Abduvohid Nematov', position='GK', sub_position='', club='Nasaf', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Nasaf; Uzbekistan No.3; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; domestic only', tier_revised='GK3'),
    # --- Defenders ---
    dict(player='Abdukodir Khusanov', position='DEF', sub_position='CB', club='Manchester City', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Manchester City CB; highest-profile Uzbek player; Premier League quality; commanding; Uzbekistan defensive cornerstone',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Man City CB; PL starter; Uzbekistan No.1 CB', tier_revised='1'),
    dict(player='Rustam Ashurmatov', position='DEF', sub_position='CB', club='Esteghlal FC', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Esteghlal (Iran) CB; first-choice CB partner to Khusanov; experienced; solid in defensive line',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Iran league experience', tier_revised='1'),
    dict(player='Avazbek Ulmasaliev', position='DEF', sub_position='RB', club='AGMK', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='AGMK RB; first-choice Uzbek right-back; energetic; attack-minded; consistent WCQ performer',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; consistent WCQ', tier_revised='1'),
    dict(player='Husniddin Aliqulov', position='DEF', sub_position='LB', club='Çaykur Rizespor', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Rizespor LB (Turkey); first-choice Uzbek left-back; Turkish league quality; overlap threat',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; Turkish Süper Lig', tier_revised='1'),
    dict(player='Umar Eshmurodov', position='DEF', sub_position='CB', club='Selangor FC', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Selangor (Malaysia) CB; regular rotation defender; experienced Uzbek international',
         int_l5_pattern='90/sub/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB rotation; Asian league experience', tier_revised='2'),
    dict(player='Abdulla Abdullaev', position='DEF', sub_position='CB', club='Khor Fakkan FC', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Khor Fakkan (UAE) CB; squad cover; fringe defensive option',
         int_l5_pattern='sub/DNP/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Squad CB depth; UAE league', tier_revised='3'),
    dict(player='Sherzod Nasrullaev', position='DEF', sub_position='CB', club='Nasaf', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Nasaf CB; domestic squad depth; cover option',
         int_l5_pattern='sub/DNP/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB squad depth; domestic league', tier_revised='3'),
    dict(player='Farrukh Sayfiev', position='DEF', sub_position='RB', club='Navbahor', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Navbahor RB; fringe defensive selection; minimal WC minutes expected',
         int_l5_pattern='DNP/sub/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe RB; domestic league depth', tier_revised='4'),
    dict(player='Muhammadkodir Hamraliev', position='DEF', sub_position='CB', club='Pakhtakor', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Pakhtakor CB; domestic depth; fringe WC selection',
         int_l5_pattern='DNP/sub/DNP/DNP/sub', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CB; Pakhtakor domestic', tier_revised='4'),
    # --- Midfielders ---
    dict(player='Otabek Shukurov', position='MID', sub_position='DM', club='Kayserispor', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Kayserispor DM (Turkey); Uzbekistan midfield anchor; combative; covers defence; Cannavaro favourite',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key DM; Turkish Süper Lig; WCQ anchor', tier_revised='1'),
    dict(player='Jaloliddin Masharipov', position='MID', sub_position='AM', club='Esteghlal FC', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Esteghlal AM (Iran); creative playmaker; Uzbekistan key attacking midfielder; technical and inventive',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key AM playmaker; Iran league experience', tier_revised='1'),
    dict(player='Sherzod Esanov', position='MID', sub_position='CM', club='FC Pari Nizhny Novgorod', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Nizhny Novgorod CM (Russia); box-to-box; regular Uzbek midfield rotation; energetic',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM; Russian Premier League', tier_revised='2'),
    dict(player='Akmal Mozgovoy', position='MID', sub_position='CM', club='Nasaf', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Nasaf CM; domestic league regular; key domestic midfield option; technical player',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM; Nasaf domestic', tier_revised='2'),
    dict(player='Aziz Ganiev', position='MID', sub_position='CM', club='Shabab Al Ahli', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Shabab Al Ahli CM (UAE); energetic; drives forward; regular Uzbek inclusion',
         int_l5_pattern='90/sub/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM; UAE league quality', tier_revised='2'),
    dict(player='Odiljon Hamrobekov', position='MID', sub_position='DM', club='Navbahor', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Navbahor DM; domestic defensive midfield cover; squad depth',
         int_l5_pattern='sub/90/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Squad DM; domestic league', tier_revised='3'),
    dict(player='Jamshid Iskanderov', position='MID', sub_position='CM', club='Neftchi Fergana', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Neftchi Fergana CM; domestic squad cover; rotation depth',
         int_l5_pattern='sub/DNP/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Squad CM; domestic league depth', tier_revised='3'),
    dict(player='Jasur Jaloliddinov', position='MID', sub_position='CM', club='Sogdiana', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Sogdiana CM; fringe midfield selection; domestic league; minimal WC minutes expected',
         int_l5_pattern='DNP/sub/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CM; domestic league depth', tier_revised='4'),
    # --- Forwards ---
    dict(player='Eldor Shomurodov', position='FWD', sub_position='CF', club='Istanbul Başakşehir', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Istanbul Başakşehir CF; captain; all-time Uzbekistan leading scorer; ex-Roma; powerful, mobile striker; WC debut leader',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain; Uzbekistan all-time top scorer; Turkish league', tier_revised='1'),
    dict(player='Abbosbek Fayzullaev', position='FWD', sub_position='WNG', club='Istanbul Başakşehir', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=T1K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Istanbul Başakşehir WNG; ex-CSKA Moscow; pacy direct winger; Uzbekistan key wide threat; highly regarded',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key WNG; Turkish Süper Lig; automatic starter', tier_revised='1'),
    dict(player='Oston Urunov', position='FWD', sub_position='WNG', club='Persepolis FC', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=T2K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Persepolis WNG (Iran); versatile wide/attacking option; regular Uzbek rotation',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular WNG rotation; Iran ACL quality', tier_revised='2'),
    dict(player='Igor Sergeev', position='FWD', sub_position='CF', club='BG Pathum United', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='BG Pathum United CF (Thailand); Russian-born Uzbek; squad backup striker; depth cover',
         int_l5_pattern='sub/90/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Squad CF; Asian league depth', tier_revised='3'),
    dict(player='Sherzod Temirov', position='FWD', sub_position='WNG', club='Kitchee SC', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=T3K,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Kitchee (Hong Kong) WNG; fringe wide option; squad cover',
         int_l5_pattern='sub/DNP/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Squad WNG; Hong Kong league', tier_revised='3'),
    dict(player='Aziz Amonov', position='FWD', sub_position='CF', club='Khor Fakkan FC', nationality='Uzbekistan', group='K',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=T4G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Khor Fakkan CF (UAE); fringe forward; minimal WC minutes expected',
         int_l5_pattern='DNP/sub/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CF; UAE league depth', tier_revised='4'),
]

def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Uzbekistan': continue
        name = row['player']
        if name in NOT_SELECTED:
            row['wc_squad_prob_pct'] = '0'; updated += 1
        elif name in CONFIRMED_IN:
            row['wc_squad_prob_pct'] = '100'; updated += 1
            print(f'  Set 100%: {name}')
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
