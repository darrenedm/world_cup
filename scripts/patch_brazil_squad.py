#!/usr/bin/env python3
"""
patch_brazil_squad.py
Sync Brazil rows with confirmed 26-man WC 2026 squad.
Announced by Carlo Ancelotti (replaced Dorival Júnior).
Run ONCE, then re-run compute_pts_per_90.py to rebuild adj pts.
"""
import csv

PATH = '/tmp/world_cup_repo/data/master_sheet.csv'

NOT_SELECTED = {'João Pedro', 'Antony'}

CONFIRMED_IN = {
    'Alisson Becker', 'Gabriel Magalhães', 'Vinícius Júnior',
    'Raphinha', 'Matheus Cunha',
}

NEW_PLAYERS = [
    # ── Goalkeepers ────────────────────────────────────────────────────────
    dict(player='Ederson', position='GK', sub_position='',
         club='Fenerbahçe', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=10.0, exp_post_group_mins_total=10,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit', notes='Former Man City GK; now Fenerbahçe; reliable No.2 behind Alisson',
         int_l5_pattern='DNP/90/DNP/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='No.2 GK; no starts expected', tier_revised='GK2'),
    dict(player='Weverton', position='GK', sub_position='',
         club='Grêmio', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=2.0, exp_post_group_mins_total=3,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit', notes='Grêmio veteran; third choice; no minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; experience only', tier_revised='GK3'),
    # ── Defenders ──────────────────────────────────────────────────────────
    dict(player='Marquinhos', position='DEF', sub_position='CB',
         club='Paris Saint-Germain', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=86.1, exp_post_group_mins_total=202,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit', notes='PSG captain; Brazil captain; elite CB (30); '
                                   'commanding in the air, superb reading of the game; '
                                   'partners Gabriel Magalhães at the heart of Brazil\'s defence',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Co-captain; undisputed first-choice CB', tier_revised='1'),
    dict(player='Bremer', position='DEF', sub_position='CB',
         club='Juventus', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=68.0, exp_post_group_mins_total=160,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit', notes='Juventus CB; powerful and aggressive; '
                                   'third CB option rotating with Marquinhos/Gabriel',
         int_l5_pattern='90/90/90/DNP/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB rotation; Juventus quality', tier_revised='2'),
    dict(player='Danilo', position='DEF', sub_position='RB',
         club='Flamengo', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=68.0, exp_post_group_mins_total=160,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit', notes='Flamengo RB; Brazil captain/veteran (34); '
                                   'experienced in Europe; competes with Wesley for starts',
         int_l5_pattern='90/90/DNP/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran RB; Ancelotti may rotate with Wesley', tier_revised='2'),
    dict(player='Wesley', position='DEF', sub_position='RB',
         club='Roma', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=68.0, exp_post_group_mins_total=160,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit', notes='Roma RB; young and attacking (22); overlapping runs '
                                   'and crossing; competes with Danilo for RB starts',
         int_l5_pattern='90/90/90/DNP/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young RB option; Ancelotti trusts him', tier_revised='2'),
    dict(player='Alex Sandro', position='DEF', sub_position='LB',
         club='Flamengo', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=35.0, exp_post_group_mins_total=46,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit', notes='Veteran LB (35); Flamengo; familiar to Ancelotti from Juventus; '
                                   'squad depth at left back',
         int_l5_pattern='90/DNP/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran LB rotation; Ancelotti connection', tier_revised='3'),
    dict(player='Léo Pereira', position='DEF', sub_position='CB',
         club='Flamengo', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=12.0, exp_post_group_mins_total=11,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit', notes='Flamengo CB; strong and physical; 4th CB option',
         int_l5_pattern='DNP/90/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='4th CB; squad depth', tier_revised='4'),
    dict(player='Roger Ibañez', position='DEF', sub_position='CB',
         club='Al-Ahli', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=12.0, exp_post_group_mins_total=11,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit', notes='Al-Ahli CB; experienced in Italy (Roma, Atalanta); depth cover',
         int_l5_pattern='DNP/90/DNP/DNP/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='5th CB; squad cover', tier_revised='4'),
    dict(player='Douglas Santos', position='DEF', sub_position='LB',
         club='Zenit Saint Petersburg', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=12.0, exp_post_group_mins_total=11,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit', notes='Zenit LB; solid left back cover; minimal expected minutes',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup LB; squad cover', tier_revised='4'),
    # ── Midfielders ────────────────────────────────────────────────────────
    dict(player='Bruno Guimarães', position='MID', sub_position='CM',
         club='Newcastle United', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=86.1, exp_post_group_mins_total=202,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit', notes='Newcastle CM; Brazil\'s midfield heartbeat — box-to-box, '
                                   'ball-winning and creative; one of the best CMs in the world',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed first-choice CM; world-class form', tier_revised='1'),
    dict(player='Lucas Paquetá', position='MID', sub_position='AM',
         club='Flamengo', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=68.0, exp_post_group_mins_total=160,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit', notes='Flamengo AM; Brazil\'s creative No.10; '
                                   'goals and assists; technical and direct',
         int_l5_pattern='90/90/90/90/DNP', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular AM starter; key creative outlet', tier_revised='2'),
    dict(player='Casemiro', position='MID', sub_position='DM',
         club='Manchester United', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=68.0, exp_post_group_mins_total=160,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit', notes='Man Utd DM (34); Brazil co-captain; experienced '
                                   'ball-winner and shield; competes with Guimarães/Paquetá '
                                   'for starts; may be slightly rotated',
         int_l5_pattern='90/90/90/DNP/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Co-captain; rotation DM alongside Guimarães', tier_revised='2'),
    dict(player='Fabinho', position='MID', sub_position='DM',
         club='Al-Ittihad', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=12.0, exp_post_group_mins_total=11,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit', notes='Al-Ittihad DM veteran (32); squad depth behind Casemiro/Guimarães',
         int_l5_pattern='DNP/90/DNP/DNP/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran DM depth; Saudi league minutes', tier_revised='4'),
    dict(player='Danilo Santos', position='MID', sub_position='CM',
         club='Botafogo', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=12.0, exp_post_group_mins_total=11,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit', notes='Botafogo CM; emerging Brazilian midfielder; squad depth',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CM; Botafogo form earned call-up', tier_revised='4'),
    # ── Forwards ───────────────────────────────────────────────────────────
    dict(player='Neymar', position='FWD', sub_position='',
         club='Santos', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=68.0, exp_post_group_mins_total=160,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit',
         notes='Record Brazil goalscorer (79 goals); returned to Santos; '
               'ACL recovery completed; Ancelotti believed in his fitness; '
               'if fit, still one of the most creative players on the planet',
         int_l5_pattern='90/90/DNP/90/90', int_l5_starts=4,
         int_absence_reason='ACL recovery 2024-25',
         fitness_current='Fit — returned to Santos; declared fit for WC camp',
         tier_evidence='T2 given injury history; when fit, absolute starter quality',
         tier_revised='2'),
    dict(player='Endrick', position='FWD', sub_position='',
         club='Lyon', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=68.0, exp_post_group_mins_total=160,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit', notes='Lyon CF (19); explosive pace and finishing; '
                                   'outstanding 2025-26 Ligue 1 season; '
                                   'Brazil\'s next superstar; Ancelotti\'s first-choice striker',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CF; unstoppable form at 19', tier_revised='2'),
    dict(player='Gabriel Martinelli', position='FWD', sub_position='',
         club='Arsenal', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=35.0, exp_post_group_mins_total=46,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit', notes='Arsenal LW; direct and energetic; competes with '
                                   'Vinícius/Neymar for left flank; excellent pressing',
         int_l5_pattern='90/90/DNP/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation winger; Arsenal regular', tier_revised='3'),
    dict(player='Igor Thiago', position='FWD', sub_position='',
         club='Brentford', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=35.0, exp_post_group_mins_total=46,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit', notes='Brentford CF; powerful target man; strong PL season; '
                                   'backup to Endrick; aerially dominant',
         int_l5_pattern='90/DNP/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup CF; Brentford form earned selection', tier_revised='3'),
    dict(player='Luiz Henrique', position='FWD', sub_position='',
         club='Zenit Saint Petersburg', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=12.0, exp_post_group_mins_total=11,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit', notes='Zenit winger; pace and directness; squad depth option',
         int_l5_pattern='DNP/90/DNP/DNP/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth winger; squad cover', tier_revised='4'),
    dict(player='Rayan', position='FWD', sub_position='',
         club='Bournemouth', nationality='Brazil', group='C',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=12.0, exp_post_group_mins_total=11,
         country_p_advance_pct=83, country_p_dead_rubber_g3_pct=20,
         fitness_flag='Fit', notes='Bournemouth winger (19); exciting young talent; '
                                   'surprise call-up; squad depth',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young squad option; depth only', tier_revised='4'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    updated = 0
    for row in rows:
        name = row['player']
        if row['nationality'] != 'Brazil':
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

    print(f'\nDone — {updated} rows updated, {len(NEW_PLAYERS)} rows added. Total: {len(rows)}')


if __name__ == '__main__':
    main()
