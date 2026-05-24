#!/usr/bin/env python3
"""
patch_japan_squad.py
Sync Japan rows with confirmed 26-man WC 2026 squad.
Announced by Hajime Moriyasu on May 15, 2026.
Key absences: Mitoma (hamstring), Minamino (ACL), Morita (fitness).
Run ONCE, then re-run compute_pts_per_90.py to rebuild adj pts.
"""
import csv

PATH = '/tmp/world_cup_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

# Group F: Netherlands(8.2), Japan(6.8), Tunisia(4.5), Sweden(4.4)
# Advance ~62%, dead rubber G3 ~22%
ADV = 62
DR  = 22

NEW_PLAYERS = [
    # ── Goalkeepers ──────────────────────────────────────────────────────
    dict(player='Zion Suzuki', position='GK', sub_position='',
         club='Parma', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=162,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Japan No.1 (23); Parma Serie A; excellent shot-stopper; '
               'clean sheet run in qualifiers; commanding in box',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed No.1; Parma regular', tier_revised='GK1'),
    dict(player='Keisuke Osako', position='GK', sub_position='',
         club='Sanfrecce Hiroshima', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=8,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Japan No.2; Sanfrecce Hiroshima J-League; backup only',
         int_l5_pattern='90/DNP/90/DNP/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; domestic league', tier_revised='GK2'),
    dict(player='Tomoki Hayakawa', position='GK', sub_position='',
         club='Kashima Antlers', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Japan No.3; Kashima Antlers; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; squad depth only', tier_revised='GK3'),
    # ── Defenders ────────────────────────────────────────────────────────
    dict(player='Hiroki Ito', position='DEF', sub_position='CB',
         club='Bayern Munich', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=80.0, exp_post_group_mins_total=158,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Bayern Munich CB/LB (27); Japan defensive linchpin; '
               'composed in possession; dominant in the air; Bundesliga quality',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed first-choice CB/LB; Bayern regular', tier_revised='1'),
    dict(player='Ko Itakura', position='DEF', sub_position='CB',
         club='Ajax', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=80.0, exp_post_group_mins_total=158,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Ajax CB (29); Japan captain contender; commanding defender; '
               'strong in the air and comfortable on the ball',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB pairing; Ajax pedigree', tier_revised='1'),
    dict(player='Yukinari Sugawara', position='DEF', sub_position='RB',
         club='Werder Bremen', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=60.0, exp_post_group_mins_total=100,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Werder Bremen RB (25); attack-minded; overlapping runs; '
               'regular right-back option for Moriyasu',
         int_l5_pattern='90/90/90/DNP/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular RB starter; Werder form solid', tier_revised='2'),
    dict(player='Takehiro Tomiyasu', position='DEF', sub_position='RB',
         club='Ajax', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=58.0, exp_post_group_mins_total=94,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Managed',
         notes='Ajax RB/CB (27); injury concerns (shoulder/knee history at Arsenal); '
               'included on fitness; can play RB and CB; quality when fit',
         int_l5_pattern='90/sub/90/DNP(inj)/90', int_l5_starts=3, int_absence_reason='Prior shoulder/knee issues',
         fitness_current='Managed: cleared to play; monitored load',
         tier_evidence='Rotation RB/CB; fitness must be managed', tier_revised='2'),
    dict(player='Tsuyoshi Watanabe', position='DEF', sub_position='CB',
         club='Feyenoord', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=58.0, exp_post_group_mins_total=94,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Feyenoord CB (29); physical and commanding; third-choice CB option',
         int_l5_pattern='90/90/DNP/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB rotation; Feyenoord quality', tier_revised='2'),
    dict(player='Ayumu Seko', position='DEF', sub_position='LB',
         club='Le Havre', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=38.0, exp_post_group_mins_total=42,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Le Havre LB (26); backup left-back option; limited WC starts expected',
         int_l5_pattern='90/DNP/sub/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup LB; Ligue 1 squad level', tier_revised='3'),
    dict(player='Shogo Taniguchi', position='DEF', sub_position='CB',
         club='Sint-Truiden', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=38.0, exp_post_group_mins_total=40,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Sint-Truiden CB (34); veteran; squad depth; limited WC starts expected',
         int_l5_pattern='90/sub/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran CB cover; Belgian Pro League', tier_revised='3'),
    dict(player='Junnosuke Suzuki', position='DEF', sub_position='RB',
         club='FC Copenhagen', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=36.0, exp_post_group_mins_total=38,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='FC Copenhagen RB (22); young; squad depth behind Sugawara/Tomiyasu',
         int_l5_pattern='sub/DNP/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young backup RB; Copenhagen level', tier_revised='3'),
    dict(player='Yuto Nagatomo', position='DEF', sub_position='LB',
         club='FC Tokyo', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=16.0, exp_post_group_mins_total=10,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='FC Tokyo LB (39); historic 5th World Cup; sentimental selection; '
               'squad depth — minimal competitive minutes expected',
         int_l5_pattern='sub/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran 5th-WC selection; symbolic', tier_revised='4'),
    # ── Midfielders ──────────────────────────────────────────────────────
    dict(player='Wataru Endo', position='MID', sub_position='DM',
         club='Liverpool', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=80.0, exp_post_group_mins_total=158,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Managed',
         notes='Liverpool DM captain (33); ankle ligament injury Feb 2026; '
               'returned to training; quality anchor; key to Japan\'s defensive structure',
         int_l5_pattern='90/90/DNP(inj)/90/90', int_l5_starts=4, int_absence_reason='Ankle Feb 2026',
         fitness_current='Managed: returned from ankle; fit to play June',
         tier_evidence='Captain and DM anchor; Liverpool quality; monitored', tier_revised='1'),
    dict(player='Takefusa Kubo', position='MID', sub_position='AM',
         club='Real Sociedad', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=80.0, exp_post_group_mins_total=158,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Real Sociedad AM (25); Japan\'s most creative attacker; '
               'elite dribbler, chance creator; expected to be Japan\'s standout player',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Japan\'s best player; Real Sociedad form', tier_revised='1'),
    dict(player='Ao Tanaka', position='MID', sub_position='CM',
         club='Leeds United', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=62.0, exp_post_group_mins_total=100,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Leeds CM (27); promoted to Premier League with Leeds; '
               'box-to-box energy and work rate; key rotation in Moriyasu system',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM starter; Leeds PL promotion', tier_revised='2'),
    dict(player='Ritsu Doan', position='MID', sub_position='AM',
         club='Eintracht Frankfurt', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=62.0, exp_post_group_mins_total=100,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Frankfurt winger/AM (27); direct and dangerous; key right-wing option; '
               'WC 2022 scorer; regular in Moriyasu system',
         int_l5_pattern='90/90/90/DNP/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular winger/AM; Frankfurt form solid', tier_revised='2'),
    dict(player='Daichi Kamada', position='MID', sub_position='AM',
         club='Crystal Palace', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=60.0, exp_post_group_mins_total=96,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Crystal Palace AM (29); creative and technical; '
               'eye for goal; rotation in Moriyasu attacking midfield',
         int_l5_pattern='90/sub/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular AM rotation; Palace form', tier_revised='2'),
    dict(player='Kaishu Sano', position='MID', sub_position='CM',
         club='Mainz 05', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=38.0, exp_post_group_mins_total=42,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Mainz CM (25); progressive passer; squad depth option',
         int_l5_pattern='90/sub/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM rotation; Mainz Bundesliga', tier_revised='3'),
    dict(player='Junya Ito', position='MID', sub_position='AM',
         club='KRC Genk', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=38.0, exp_post_group_mins_total=40,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Genk winger (33); experienced Japan international; pace on right wing; '
               'squad cover behind Kubo/Doan',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran winger rotation; Genk level', tier_revised='3'),
    dict(player='Keito Nakamura', position='MID', sub_position='AM',
         club='Stade de Reims', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=36.0, exp_post_group_mins_total=38,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Reims AM (25); technical and creative; squad depth attacking option',
         int_l5_pattern='90/sub/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Attacking rotation; Reims Ligue 1', tier_revised='3'),
    # ── Forwards ─────────────────────────────────────────────────────────
    dict(player='Ayase Ueda', position='FWD', sub_position='',
         club='Feyenoord', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=80.0, exp_post_group_mins_total=158,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Feyenoord striker (27); Japan No.1 CF; clinical finisher; '
               'strong aerial presence; regular Moriyasu first-choice',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed first-choice striker; Feyenoord form', tier_revised='1'),
    dict(player='Daizen Maeda', position='FWD', sub_position='',
         club='Celtic', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=60.0, exp_post_group_mins_total=96,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Celtic striker (28); high pressing and direct; regular Japan option; '
               'scored in WC 2022; excellent work rate',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular forward rotation; Celtic form', tier_revised='2'),
    dict(player='Koki Ogawa', position='FWD', sub_position='',
         club='NEC Nijmegen', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=58.0, exp_post_group_mins_total=92,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='NEC Nijmegen striker (28); physical CF; rotation behind Ueda',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup striker; Eredivisie form', tier_revised='2'),
    dict(player='Yuito Suzuki', position='FWD', sub_position='',
         club='SC Freiburg', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=38.0, exp_post_group_mins_total=42,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='SC Freiburg winger/forward (24); Bundesliga talent; '
               'joined Freiburg from Brøndby July 2025; pace and direct play',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Impact winger; Bundesliga potential', tier_revised='3'),
    dict(player='Keisuke Goto', position='FWD', sub_position='',
         club='Sint-Truiden', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=36.0, exp_post_group_mins_total=38,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Sint-Truiden forward (21); young attacker; squad depth; '
               'minimal WC starts expected',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young depth forward; Belgian Pro League', tier_revised='3'),
    dict(player='Kento Shiogai', position='FWD', sub_position='',
         club='VfL Wolfsburg', nationality='Japan', group='F',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=34.0, exp_post_group_mins_total=36,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Wolfsburg forward (21); young Bundesliga talent; squad depth option',
         int_l5_pattern='DNP/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young depth forward; Wolfsburg', tier_revised='3'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    updated = 0
    for row in rows:
        if row['nationality'] != 'Japan':
            continue
        name = row['player']
        if name in NOT_SELECTED:
            row['wc_squad_prob_pct'] = '0'
            updated += 1
        elif name in CONFIRMED_IN:
            row['wc_squad_prob_pct'] = '100'
            updated += 1
        if name in CORRECTIONS:
            for k, v in CORRECTIONS[name].items():
                row[k] = str(v)

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
