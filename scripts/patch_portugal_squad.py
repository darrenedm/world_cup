#!/usr/bin/env python3
"""
patch_portugal_squad.py
Sync Portugal rows with confirmed 26-man WC 2026 squad.
Announced by Roberto Martínez on May 19, 2026.
Run ONCE, then re-run compute_pts_per_90.py to rebuild adj pts.
"""
import csv

PATH = '/tmp/world_cup_repo/data/master_sheet.csv'

NOT_SELECTED = set()   # all existing Portugal rows are confirmed in squad

CONFIRMED_IN = {
    'Bruno Fernandes', 'Vitinha', 'João Neves',
    'Nuno Mendes', 'Rúben Dias', 'Rafael Leão', 'Pedro Neto',
}

NEW_PLAYERS = [
    # ── Goalkeepers ────────────────────────────────────────────────────────
    dict(
        player='Diogo Costa', position='GK', sub_position='',
        club='Porto', nationality='Portugal', group='K',
        wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
        group_mins_per_game=90.0, exp_post_group_mins_total=256,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=45,
        fitness_flag='Fit',
        notes='Portugal No.1; hero of WC 2022 penalty shootout vs Slovenia; '
              'exceptional distribution and shot-stopping',
        int_l5_pattern='90/90/90/90/90', int_l5_starts=5,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Undisputed No.1; WC 2022 penalty-save hero',
        tier_revised='GK1',
    ),
    dict(
        player='José Sá', position='GK', sub_position='',
        club='Wolverhampton', nationality='Portugal', group='K',
        wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
        group_mins_per_game=10.0, exp_post_group_mins_total=10,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=45,
        fitness_flag='Fit',
        notes='Wolves No.1; reliable backup; limited international role behind Costa',
        int_l5_pattern='DNP/90/DNP/DNP/DNP', int_l5_starts=1,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='No.2 GK; no realistic starts expected',
        tier_revised='GK2',
    ),
    dict(
        player='Rui Silva', position='GK', sub_position='',
        club='Sporting CP', nationality='Portugal', group='K',
        wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
        group_mins_per_game=2.0, exp_post_group_mins_total=3,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=45,
        fitness_flag='Fit',
        notes='Third-choice GK; Sporting CP first team regular; no expected minutes',
        int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Third GK; squad depth only',
        tier_revised='GK3',
    ),
    # ── Defenders ──────────────────────────────────────────────────────────
    dict(
        player='João Cancelo', position='DEF', sub_position='RB',
        club='Al-Hilal', nationality='Portugal', group='K',
        wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
        group_mins_per_game=83.8, exp_post_group_mins_total=256,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=45,
        fitness_flag='Fit',
        notes='Elite attacking FB; can play either side; key creative outlet '
              'from deep; excellent cross and dribble numbers',
        int_l5_pattern='90/90/90/90/90', int_l5_starts=5,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='First-choice RB; one of Portugal\'s key creative outlets',
        tier_revised='1',
    ),
    dict(
        player='Gonçalo Inácio', position='DEF', sub_position='CB',
        club='Sporting CP', nationality='Portugal', group='K',
        wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
        group_mins_per_game=65.0, exp_post_group_mins_total=150,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=45,
        fitness_flag='Fit',
        notes='Left-footed CB; Sporting CP captain; strong in possession; '
              'Rúben Dias\' regular partner',
        int_l5_pattern='90/90/90/90/DNP', int_l5_starts=4,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Regular CB starter; Dias partner; likely starter most games',
        tier_revised='2',
    ),
    dict(
        player='Diogo Dalot', position='DEF', sub_position='RB',
        club='Manchester United', nationality='Portugal', group='K',
        wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
        group_mins_per_game=65.0, exp_post_group_mins_total=150,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=45,
        fitness_flag='Fit',
        notes='Man Utd RB; strong 2025-26 season; Cancelo backup and rotation option; '
              'can also play LB',
        int_l5_pattern='90/DNP/90/90/90', int_l5_starts=4,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Regular rotation RB; Cancelo\'s understudy',
        tier_revised='2',
    ),
    dict(
        player='Nelson Semedo', position='DEF', sub_position='RB',
        club='Fenerbahçe', nationality='Portugal', group='K',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=32.0, exp_post_group_mins_total=50,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=45,
        fitness_flag='Fit',
        notes='Experienced RB/WB; Fenerbahçe; third RB option; pace and energy '
              'off the bench',
        int_l5_pattern='90/DNP/90/DNP/90', int_l5_starts=3,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Third RB; impact option behind Cancelo/Dalot',
        tier_revised='3',
    ),
    dict(
        player='Renato Veiga', position='DEF', sub_position='CB',
        club='Villarreal', nationality='Portugal', group='K',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=32.0, exp_post_group_mins_total=50,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=45,
        fitness_flag='Fit',
        notes='Utility CB/LB; can also cover LB; Villarreal; strong aerial; '
              'flexible defensive cover option',
        int_l5_pattern='90/DNP/90/DNP/DNP', int_l5_starts=2,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Versatile utility defender; 4th CB or LB option',
        tier_revised='3',
    ),
    dict(
        player='Tomás Araújo', position='DEF', sub_position='CB',
        club='Benfica', nationality='Portugal', group='K',
        wc_squad_prob_pct=100, tier='4', playing_role='Depth',
        group_mins_per_game=12.0, exp_post_group_mins_total=15,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=45,
        fitness_flag='Fit',
        notes='Young Benfica CB; squad depth; unlikely to start unless injuries',
        int_l5_pattern='DNP/90/DNP/DNP/DNP', int_l5_starts=1,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='4th-choice CB; squad cover',
        tier_revised='4',
    ),
    # ── Midfielders ────────────────────────────────────────────────────────
    dict(
        player='Bernardo Silva', position='MID', sub_position='CM',
        club='Manchester City', nationality='Portugal', group='K',
        wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
        group_mins_per_game=83.8, exp_post_group_mins_total=256,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=45,
        fitness_flag='Fit',
        notes='World-class CM/winger hybrid; Man City stalwart; '
              'elite technical ability, high work rate, key playmaker role alongside '
              'Vitinha and João Neves',
        int_l5_pattern='90/90/90/90/90', int_l5_starts=5,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='First-choice CM; integral to Portugal\'s shape',
        tier_revised='1',
    ),
    dict(
        player='Rúben Neves', position='MID', sub_position='DM',
        club='Al-Hilal', nationality='Portugal', group='K',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=32.0, exp_post_group_mins_total=50,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=45,
        fitness_flag='Fit',
        notes='Veteran DM (29); Al-Hilal; experienced ball-winner; '
              'depth behind Neves/Vitinha; long-range shooting threat',
        int_l5_pattern='90/DNP/90/90/DNP', int_l5_starts=3,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Rotation DM; third choice behind João Neves/Vitinha',
        tier_revised='3',
    ),
    dict(
        player='Matheus Nunes', position='MID', sub_position='CM',
        club='Manchester City', nationality='Portugal', group='K',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=32.0, exp_post_group_mins_total=50,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=45,
        fitness_flag='Fit',
        notes='Athletic CM; Man City squad player; listed as DF in official squad '
              'sheet but plays CM; versatile pressing option off bench',
        int_l5_pattern='90/DNP/DNP/90/90', int_l5_starts=3,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Utility CM; rotation option; plays deeper than his role suggests',
        tier_revised='3',
    ),
    dict(
        player='Samu Costa', position='MID', sub_position='DM',
        club='Mallorca', nationality='Portugal', group='K',
        wc_squad_prob_pct=100, tier='4', playing_role='Depth',
        group_mins_per_game=12.0, exp_post_group_mins_total=15,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=45,
        fitness_flag='Fit',
        notes='Mallorca DM; solid La Liga season; squad depth only; '
              'unlikely to feature barring multiple injuries',
        int_l5_pattern='DNP/90/DNP/DNP/90', int_l5_starts=2,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='4th midfielder; squad depth',
        tier_revised='4',
    ),
    # ── Forwards ───────────────────────────────────────────────────────────
    dict(
        player='Cristiano Ronaldo', position='FWD', sub_position='',
        club='Al-Nassr', nationality='Portugal', group='K',
        wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
        group_mins_per_game=83.8, exp_post_group_mins_total=256,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=45,
        fitness_flag='Fit',
        notes='Record WC goal-scorer at his 6th tournament (41); Al-Nassr captain; '
              'still lethal in the box; pace declined but positioning elite; '
              'Martínez builds around him',
        int_l5_pattern='90/90/90/90/90', int_l5_starts=5,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Automatic starter; Portugal captain; Martínez trusts fully',
        tier_revised='1',
    ),
    dict(
        player='Gonçalo Ramos', position='FWD', sub_position='',
        club='Paris Saint-Germain', nationality='Portugal', group='K',
        wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
        group_mins_per_game=65.0, exp_post_group_mins_total=150,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=45,
        fitness_flag='Fit',
        notes='PSG striker; hat-trick vs Switzerland at WC 2022; mobile, clinical; '
              'strong alternative No.9 to Ronaldo; expected significant minutes',
        int_l5_pattern='90/90/90/DNP/90', int_l5_starts=4,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Key rotation/starter ST; hat-trick sub at WC 2022',
        tier_revised='2',
    ),
    dict(
        player='Francisco Conceição', position='FWD', sub_position='',
        club='Juventus', nationality='Portugal', group='K',
        wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
        group_mins_per_game=65.0, exp_post_group_mins_total=150,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=45,
        fitness_flag='Fit',
        notes='Direct RW; explosive pace; Juventus regular; scored winner vs France '
              'at Euro 2024; clinical in 1v1s; competes for Pedro Neto\'s spot',
        int_l5_pattern='90/90/DNP/90/90', int_l5_starts=4,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Regular winger; Euro 2024 match-winner; Martínez trusts him',
        tier_revised='2',
    ),
    dict(
        player='João Félix', position='FWD', sub_position='',
        club='Al-Nassr', nationality='Portugal', group='K',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=32.0, exp_post_group_mins_total=50,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=45,
        fitness_flag='Fit',
        notes='Talented AM/FW; Al-Nassr teammate of Ronaldo; creative in tight '
              'spaces; excellent dribbler; inconsistent but a difference-maker '
              'off the bench',
        int_l5_pattern='90/DNP/90/90/DNP', int_l5_starts=3,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Impact sub; creative alternate No.10 option',
        tier_revised='3',
    ),
    dict(
        player='Francisco Trincão', position='FWD', sub_position='',
        club='Sporting CP', nationality='Portugal', group='K',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=32.0, exp_post_group_mins_total=50,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=45,
        fitness_flag='Fit',
        notes='Sporting CP winger; strong Primeira Liga season; direct and pacey; '
              'depth winger behind Leão/Neto/Conceição',
        int_l5_pattern='DNP/90/90/DNP/90', int_l5_starts=3,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Fourth winger option; Sporting form earned call-up',
        tier_revised='3',
    ),
    dict(
        player='Gonçalo Guedes', position='FWD', sub_position='',
        club='Real Sociedad', nationality='Portugal', group='K',
        wc_squad_prob_pct=100, tier='4', playing_role='Depth',
        group_mins_per_game=12.0, exp_post_group_mins_total=15,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=45,
        fitness_flag='Fit',
        notes='Veteran winger (29); Real Sociedad; La Liga experience; '
              'squad depth with minimal expected minutes',
        int_l5_pattern='DNP/90/DNP/DNP/90', int_l5_starts=2,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='5th winger; squad cover only',
        tier_revised='4',
    ),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    updated = 0
    for row in rows:
        name = row['player']
        if row['nationality'] != 'Portugal':
            continue
        if name in NOT_SELECTED:
            row['wc_squad_prob_pct'] = '0'
            updated += 1
            print(f'  Set 0%:   {name}')
        elif name in CONFIRMED_IN:
            row['wc_squad_prob_pct'] = '100'
            updated += 1
            print(f'  Set 100%: {name}')

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

    print(f'\nDone — {updated} rows updated, {len(NEW_PLAYERS)} rows added.')
    print(f'Total rows: {len(rows)}')


if __name__ == '__main__':
    main()
