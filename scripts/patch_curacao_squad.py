#!/usr/bin/env python3
"""
patch_curacao_squad.py — official 26-man squad (Dick Advocaat, announced May 18 2026).
Group E: Germany(7.9), Ecuador(5.8), Ivory Coast(4.4), Curaçao(1.3).
Advance 2%, dead rubber G3 10%.
HISTORIC DEBUT — Curaçao's first-ever World Cup; smallest nation ever to qualify.
Manager Dick Advocaat becomes oldest manager in WC history.
Captain: Leandro Bacuna (Iğdır, 34yo, ex-Aston Villa/Cardiff City, most-capped).
Key players: Tahith Chong (Sheffield United), Armando Obispo (PSV), Sontje Hansen (Middlesbrough).
Predominantly Dutch-passport players and Netherlands-league based.
"""
import csv
PATH = '/tmp/wc_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

ADV, DR = 2, 10
T1G, T1K = 75.0, 0
T2G, T2K = 55.0, 0
T3G, T3K = 20.0, 0
T4G, T4K = 5.0,  0

NEW_PLAYERS = [
    # Goalkeepers
    dict(player='Eloy Room', position='GK', sub_position='', club='Miami FC', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Miami FC GK (USL); Curaçao undisputed No.1; veteran keeper with Dutch football background; '
               'experienced in international football; leads GK dept for historic debut in Group E',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed GK1; Miami FC USL Championship', tier_revised='GK1'),
    dict(player='Trevor Doornbusch', position='GK', sub_position='', club='VVV-Venlo', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='VVV-Venlo GK (Netherlands Eerste Divisie); Curaçao No.2 keeper; Dutch Eerste Divisie; backup behind Room',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; VVV-Venlo Dutch Eerste Divisie', tier_revised='GK2'),
    dict(player='Tyrick Bodak', position='GK', sub_position='', club='SC Telstar', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='SC Telstar GK (Netherlands Eerste Divisie); Curaçao third-choice keeper; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; SC Telstar Dutch Eerste Divisie', tier_revised='GK3'),
    # Defenders
    dict(player='Armando Obispo', position='DEF', sub_position='CB', club='PSV Eindhoven', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='PSV Eindhoven CB (Eredivisie/Champions League); Curaçao highest-profile defender; '
               'Champions League experience; commanding and composed; the quality anchor of Curaçao\'s defence; '
               'best player in the squad defensively; made his debut in 2025 WC qualifying window',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; PSV Eindhoven Eredivisie', tier_revised='1'),
    dict(player='Shurandy Sambo', position='DEF', sub_position='CB', club='Sparta Rotterdam', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Sparta Rotterdam CB (Eredivisie); Curaçao centre-back alongside Obispo; Dutch Eredivisie quality; '
               'physical and reliable; key part of defensive unit',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Sparta Rotterdam Eredivisie', tier_revised='1'),
    dict(player='Joshua Brenet', position='DEF', sub_position='RB', club='Kayserispor', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Kayserispor RB (Turkey Süper Lig); Curaçao first-choice right-back; formerly Eindhoven and Hoffenheim; '
               'experienced Dutch-passport fullback; key in wide defensive areas',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; Kayserispor Süper Lig', tier_revised='1'),
    dict(player='Sherel Floranus', position='DEF', sub_position='LB', club='PEC Zwolle', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='PEC Zwolle LB (Netherlands Eerste Divisie); Curaçao first-choice left-back; Dutch league experience; '
               'athletic and attack-minded fullback',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; PEC Zwolle Dutch Eerste Divisie', tier_revised='1'),
    dict(player='Riechedly Bazoer', position='DEF', sub_position='CB', club='Konyaspor', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Konyaspor CB/DEF (Turkey Süper Lig); Curaçao versatile defender; formerly Ajax and Wolfsburg; '
               'experienced Dutch international-level player; rotation option across the back line',
         int_l5_pattern='90/sub/sub/90/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation DEF; Konyaspor Süper Lig', tier_revised='2'),
    dict(player='Roshon Van Eijma', position='DEF', sub_position='CB', club='RKC Waalwijk', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='RKC Waalwijk CB (Eredivisie); Curaçao defensive rotation; Eredivisie experience; squad depth option',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; RKC Waalwijk Eredivisie', tier_revised='2'),
    dict(player='Deveron Fonville', position='DEF', sub_position='RB', club='NEC Nijmegen', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='NEC Nijmegen RB (Eredivisie); Curaçao fullback depth; Dutch Eredivisie; limited WC minutes expected',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='RB depth; NEC Nijmegen Eredivisie', tier_revised='3'),
    dict(player='Juriën Gaari', position='DEF', sub_position='CB', club='Abha Club', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Abha Club CB (Saudi Pro League); Curaçao defensive squad depth; Saudi league; limited WC minutes expected',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB depth; Abha Club Saudi Pro League', tier_revised='3'),
    # Midfielders
    dict(player='Leandro Bacuna', position='MID', sub_position='CM', club='Iğdır FK', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Iğdır FK CM (Turkey); Curaçao captain and most-capped player (34yo); former Aston Villa and Cardiff City '
               '(Premier League experience); leads historic WC debut; versatile midfielder who can play right-back; '
               'inspirational figurehead of the qualification campaign',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain and most-capped; undisputed T1; Iğdır FK', tier_revised='1'),
    dict(player='Juninho Bacuna', position='MID', sub_position='CM', club='FC Volendam', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FC Volendam CM (Netherlands Eerste Divisie); Curaçao creative midfielder; younger brother of captain Leandro; '
               'former Huddersfield Town (Championship); technically gifted playmaker; key creative figure in midfield',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CM; FC Volendam Dutch Eerste Divisie', tier_revised='1'),
    dict(player='Livano Comenencia', position='MID', sub_position='DM', club='FC Zürich', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FC Zürich DM (Swiss Super League); Curaçao defensive midfielder; Swiss Super League quality; '
               'disciplined and combative; key to Curaçao\'s midfield structure',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice DM; FC Zürich Swiss Super League', tier_revised='1'),
    dict(player='Ar\'Jany Martha', position='MID', sub_position='CM', club='Rotherham United', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Rotherham United CM (League One/Championship); Curaçao midfield rotation; EFL experience; '
               'squad rotation option in central midfield',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Rotherham United EFL', tier_revised='2'),
    dict(player='Godfried Roemeratoe', position='MID', sub_position='CM', club='RKC Waalwijk', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='RKC Waalwijk CM (Eredivisie); Curaçao midfield rotation; Dutch Eredivisie experience; squad depth',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; RKC Waalwijk Eredivisie', tier_revised='2'),
    dict(player='Tyrese Noslin', position='MID', sub_position='WNG', club='SC Telstar', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='SC Telstar WNG (Netherlands Eerste Divisie); Curaçao wide midfield depth; limited WC minutes expected',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='WNG depth; SC Telstar Dutch Eerste Divisie', tier_revised='3'),
    dict(player='Kevin Felida', position='MID', sub_position='CM', club='FC Den Bosch', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FC Den Bosch CM (Netherlands); Curaçao midfield fringe option; Dutch lower-league; minimal WC minutes',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; FC Den Bosch Netherlands Eerste Divisie', tier_revised='3'),
    # Forwards
    dict(player='Tahith Chong', position='FWD', sub_position='WNG', club='Sheffield United', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Sheffield United WNG (Championship); Curaçao headline attacking talent; former Manchester United academy; '
               'fast, direct and technically gifted winger; Championship quality; made WC qualifying debut in 2025; '
               'Curaçao\'s most exciting and dangerous attacker',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Curaçao star attacker; undisputed T1; Sheffield United Championship', tier_revised='1'),
    dict(player='Sontje Hansen', position='FWD', sub_position='WNG', club='Middlesbrough', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Middlesbrough WNG (Championship); Curaçao attacking rotation; EFL Championship experience; '
               'good pace and direct play from wide; key rotation option',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation WNG; Middlesbrough Championship', tier_revised='2'),
    dict(player='Kenji Gorré', position='FWD', sub_position='WNG', club='Maccabi Haifa', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Maccabi Haifa WNG (Israeli Premier League); Curaçao veteran attacker who participated in multiple '
               'qualifying cycles; experienced international; wide attacking rotation option',
         int_l5_pattern='sub/90/90/sub/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation WNG; Maccabi Haifa Israeli Premier League', tier_revised='2'),
    dict(player='Brandley Kuwas', position='FWD', sub_position='WNG', club='FC Volendam', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FC Volendam WNG (Netherlands Eerste Divisie); Curaçao wide forward depth; limited WC minutes expected',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='WNG depth; FC Volendam Dutch Eerste Divisie', tier_revised='3'),
    dict(player='Jürgen Locadia', position='FWD', sub_position='CF', club='Miami FC', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Miami FC CF (USL); Curaçao striker depth; former Brighton (Premier League) and Hoffenheim; '
               'experienced veteran CF; limited WC minutes expected at this stage of career',
         int_l5_pattern='sub/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CF depth veteran; Miami FC USL Championship', tier_revised='3'),
    dict(player='Jeremy Antonisse', position='FWD', sub_position='CF', club='AE Kifisia', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='4', playing_role='Fringe Player',
         group_mins_per_game=T4G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='AE Kifisia CF (Greece); Curaçao forward fringe option; Greek league; minimal WC minutes expected',
         int_l5_pattern='DNP/DNP/sub/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CF; AE Kifisia Greek Football League', tier_revised='4'),
    dict(player='Gervane Kastaneer', position='FWD', sub_position='WNG', club='Terengganu FC', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='4', playing_role='Fringe Player',
         group_mins_per_game=T4G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Terengganu FC WNG (Malaysia Super League); Curaçao fringe wide forward; Malaysia-based; '
               'minimal WC minutes expected; squad depth only',
         int_l5_pattern='DNP/DNP/sub/DNP/sub', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe WNG; Terengganu FC Malaysia Super League', tier_revised='4'),
    dict(player='Jearl Margaritha', position='FWD', sub_position='WNG', club='SK Beveren', nationality='Curaçao', group='E',
         wc_squad_prob_pct=100, tier='4', playing_role='Fringe Player',
         group_mins_per_game=T4G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='SK Beveren WNG (Belgium); Curaçao fringe wide forward; Belgian football league; minimal WC minutes expected',
         int_l5_pattern='DNP/sub/DNP/DNP/sub', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe WNG; SK Beveren Belgian Pro League 1B', tier_revised='4'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Curaçao': continue
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
