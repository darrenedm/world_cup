#!/usr/bin/env python3
"""
patch_belgium_squad.py
Sync Belgium rows with confirmed 26-man WC 2026 squad.
Announced by Rudi Garcia on May 15, 2026.
Run ONCE, then re-run compute_pts_per_90.py to rebuild adj pts.
"""
import csv

PATH = '/tmp/world_cup_repo/data/master_sheet.csv'

NOT_SELECTED = set()   # Matz Sels already at 0% in CSV

CONFIRMED_IN = {'Thibaut Courtois', 'Kevin De Bruyne', 'Jérémy Doku', 'Romelu Lukaku'}

CORRECTIONS = {
    'Romelu Lukaku': {
        'tier': '1', 'playing_role': 'Automatic Starter',
        'group_mins_per_game': '82.4', 'exp_post_group_mins_total': '207',
        'tier_revised': '1',
        'tier_evidence': 'Garcia confirmed starter; Napoli form backed up selection',
    },
}

NEW_PLAYERS = [
    # ── Goalkeepers ────────────────────────────────────────────────────────
    dict(player='Senne Lammens', position='GK', sub_position='',
         club='Manchester United', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=10.0, exp_post_group_mins_total=10,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='Man Utd backup; Belgium No.2 behind Courtois',
         int_l5_pattern='DNP/90/DNP/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='No.2 GK; no starts expected', tier_revised='GK2'),
    dict(player='Mike Penders', position='GK', sub_position='',
         club='Strasbourg', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=2.0, exp_post_group_mins_total=3,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='Chelsea loan at Strasbourg; third-choice only',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; no minutes expected', tier_revised='GK3'),
    # ── Defenders ──────────────────────────────────────────────────────────
    dict(player='Zeno Debast', position='DEF', sub_position='CB',
         club='Sporting CP', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=71.7, exp_post_group_mins_total=184,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='Young Sporting CP CB (22); Belgium\'s first-choice CB partner; '
                                   'comfortable in possession; key to Garcia\'s build-out',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Sporting form excellent', tier_revised='2'),
    dict(player='Koni De Winter', position='DEF', sub_position='CB',
         club='AC Milan', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=71.7, exp_post_group_mins_total=184,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='AC Milan CB; strong and dominant in the air; '
                                   'competes with Debast/Theate for CB spots',
         int_l5_pattern='90/90/DNP/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB starter; AC Milan quality', tier_revised='2'),
    dict(player='Timothy Castagne', position='DEF', sub_position='RB',
         club='Fulham', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=71.7, exp_post_group_mins_total=184,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='Fulham RB; experienced Belgium right back; '
                                   'solid defensively, contributes going forward',
         int_l5_pattern='90/90/90/DNP/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; regular Belgium starter', tier_revised='2'),
    dict(player='Maxim De Cuyper', position='DEF', sub_position='LB',
         club='Brighton', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=71.7, exp_post_group_mins_total=184,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='Brighton LB; quick and attack-minded; '
                                   'first-choice left back; good crossing and dribbling',
         int_l5_pattern='90/90/90/90/DNP', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; Brighton form strong', tier_revised='2'),
    dict(player='Arthur Theate', position='DEF', sub_position='CB',
         club='Eintracht Frankfurt', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=32.0, exp_post_group_mins_total=48,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='Frankfurt CB/LB; physical and commanding; rotation defender',
         int_l5_pattern='90/DNP/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB/LB; squad depth', tier_revised='3'),
    dict(player='Thomas Meunier', position='DEF', sub_position='RB',
         club='Lille', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=12.0, exp_post_group_mins_total=12,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='Veteran RB (34); Lille; squad depth behind Castagne',
         int_l5_pattern='DNP/90/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup RB; veteran squad cover', tier_revised='4'),
    dict(player='Brandon Mechele', position='DEF', sub_position='CB',
         club='Club Brugge', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=12.0, exp_post_group_mins_total=12,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='Club Brugge CB veteran; squad depth only',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='4th CB; depth cover', tier_revised='4'),
    dict(player='Nathan Ngoy', position='DEF', sub_position='LB',
         club='Lille', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=12.0, exp_post_group_mins_total=12,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='Lille LB/FB; young versatile backup; minimal expected minutes',
         int_l5_pattern='DNP/90/DNP/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup LB; squad depth', tier_revised='4'),
    dict(player='Joaquin Seys', position='DEF', sub_position='CB',
         club='Club Brugge', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=12.0, exp_post_group_mins_total=12,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='Club Brugge CB; young squad option; depth cover only',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='5th CB; depth only', tier_revised='4'),
    # ── Midfielders ────────────────────────────────────────────────────────
    dict(player='Amadou Onana', position='MID', sub_position='DM',
         club='Everton', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=82.4, exp_post_group_mins_total=207,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='Everton DM; Belgium\'s engine room — elite ball-winner, '
                                   'powerful and technical; anchors the midfield alongside De Bruyne',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed first-choice DM; world-class at 23', tier_revised='1'),
    dict(player='Youri Tielemans', position='MID', sub_position='CM',
         club='Aston Villa', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=71.7, exp_post_group_mins_total=184,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='Villa CM; experienced Belgian midfielder; '
                                   'good range of passing; regular rotation alongside Onana/De Bruyne',
         int_l5_pattern='90/90/90/DNP/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM starter; Villa form keeps him relevant', tier_revised='2'),
    dict(player='Axel Witsel', position='MID', sub_position='DM',
         club='Girona', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=32.0, exp_post_group_mins_total=48,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='Veteran DM (36); Girona; Belgium legend; '
                                   'squad cover and leadership; minimal expected minutes',
         int_l5_pattern='90/DNP/90/DNP/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran leadership; 3rd DM option', tier_revised='3'),
    dict(player='Hans Vanaken', position='MID', sub_position='CM',
         club='Club Brugge', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=12.0, exp_post_group_mins_total=12,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='Club Brugge CM; set-piece specialist; depth only',
         int_l5_pattern='DNP/90/DNP/DNP/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='4th CM; squad depth', tier_revised='4'),
    dict(player='Nicolas Raskin', position='MID', sub_position='CM',
         club='Rangers', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=12.0, exp_post_group_mins_total=12,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='Rangers CM; young and energetic; depth option only',
         int_l5_pattern='DNP/90/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='5th CM; squad depth', tier_revised='4'),
    # ── Forwards ───────────────────────────────────────────────────────────
    dict(player='Leandro Trossard', position='FWD', sub_position='',
         club='Arsenal', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=71.7, exp_post_group_mins_total=184,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='Arsenal winger/forward; strong 2025-26 season; '
                                   'direct and clinical; key rotation on the left flank',
         int_l5_pattern='90/90/90/90/DNP', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular starter; Arsenal form undeniable', tier_revised='2'),
    dict(player='Charles De Ketelaere', position='FWD', sub_position='',
         club='Atalanta', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=71.7, exp_post_group_mins_total=184,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='Atalanta AM/winger; outstanding 2024-25, solid 2025-26; '
                                   'creative and direct; key Belgium attacking option',
         int_l5_pattern='90/90/DNP/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular attacking rotation; Atalanta form justified', tier_revised='2'),
    dict(player='Alexis Saelemaekers', position='FWD', sub_position='',
         club='AC Milan', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=32.0, exp_post_group_mins_total=48,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='AC Milan winger; energetic and pressing; impact option on right',
         int_l5_pattern='90/DNP/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation winger; Milan form earned selection', tier_revised='3'),
    dict(player='Dodi Lukebakio', position='FWD', sub_position='',
         club='Benfica', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=32.0, exp_post_group_mins_total=48,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='Benfica winger; pace and power; impact off bench',
         int_l5_pattern='DNP/90/90/DNP/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Impact winger; Benfica form earned spot', tier_revised='3'),
    dict(player='Matias Fernández-Pardo', position='FWD', sub_position='',
         club='Lille', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=12.0, exp_post_group_mins_total=12,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='Lille winger; young French-born Belgian; squad depth',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='5th winger; youth option', tier_revised='4'),
    dict(player='Diego Moreira', position='FWD', sub_position='',
         club='Strasbourg', nationality='Belgium', group='G',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=12.0, exp_post_group_mins_total=12,
         country_p_advance_pct=92, country_p_dead_rubber_g3_pct=50,
         fitness_flag='Fit', notes='Strasbourg winger; young Portuguese-born Belgian; squad depth',
         int_l5_pattern='DNP/90/DNP/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='6th winger; depth only', tier_revised='4'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    updated = 0
    for row in rows:
        name = row['player']
        if row['nationality'] != 'Belgium':
            continue
        if name in NOT_SELECTED:
            row['wc_squad_prob_pct'] = '0'
            updated += 1
            print(f'  Set 0%:   {name}')
        elif name in CONFIRMED_IN:
            row['wc_squad_prob_pct'] = '100'
            updated += 1
            print(f'  Set 100%: {name}')
        if name in CORRECTIONS:
            for k, v in CORRECTIONS[name].items():
                row[k] = str(v)
            print(f'  Patched:  {name} ({", ".join(CORRECTIONS[name].keys())})')

    blank_pts = {'action_pts_per_90': '0', 'exp_pts_per_90': '0',
                 'total_exp_fantasy_pts': '0', 'adj_exp_fantasy_pts': '0'}
    for p in NEW_PLAYERS:
        new_row = {k: '' for k in fieldnames}
        new_row.update(blank_pts)
        new_row.update({str(k): str(v) for k, v in p.items()})
        rows.append(new_row)
        print(f'  Added:    {p["player"]}')

    with open(PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f'\nDone — {updated} rows updated, {len(NEW_PLAYERS)} rows added. Total: {len(rows)}')


if __name__ == '__main__':
    main()
