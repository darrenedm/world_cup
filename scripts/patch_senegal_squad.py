#!/usr/bin/env python3
"""
patch_senegal_squad.py
Sync Senegal rows with WC 2026 squad.
28-man provisional announced May 21, 2026 by coach Pape Thiaw.
Final 26 confirmed by FIFA deadline June 2. 4 marginal players at 80%.
Run ONCE, then re-run compute_pts_per_90.py to rebuild adj pts.
"""
import csv

PATH = '/tmp/world_cup_repo/data/master_sheet.csv'

NOT_SELECTED = set()

CONFIRMED_IN = set()

CORRECTIONS = {}

# Group I: France(10.0), Senegal(7.1), Norway(5.3), Iraq(3.2)
# Advance ~65%, dead rubber G3 ~28%
ADV = 65
DR  = 28

NEW_PLAYERS = [
    # ── Goalkeepers ──────────────────────────────────────────────────────
    dict(player='Édouard Mendy', position='GK', sub_position='',
         club='Al-Ahli', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=168,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Senegal No.1 (34); Al-Ahli Saudi Pro League; experienced shot-stopper; '
               'ex-Chelsea; solid WC pedigree',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed No.1', tier_revised='GK1'),
    dict(player='Yehvann Diouf', position='GK', sub_position='',
         club='OGC Nice', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=10,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Senegal No.2; OGC Nice; no WC starts expected',
         int_l5_pattern='90/DNP/90/DNP/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; no mins expected', tier_revised='GK2'),
    dict(player='Mory Diaw', position='GK', sub_position='',
         club='Le Havre', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Senegal No.3; Le Havre Ligue 1; third-choice only',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; no minutes', tier_revised='GK3'),
    # ── Defenders ────────────────────────────────────────────────────────
    dict(player='Kalidou Koulibaly', position='DEF', sub_position='CB',
         club='Al-Hilal', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=80.0, exp_post_group_mins_total=162,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Senegal captain (34); Al-Hilal; still elite CB; towering and commanding; '
               'defensive rock and set-piece threat',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed captain and first-choice CB', tier_revised='1'),
    dict(player='Ismaïl Jakobs', position='DEF', sub_position='LB',
         club='Galatasaray', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=80.0, exp_post_group_mins_total=162,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='First-choice Senegal LB; Galatasaray; attack-minded and energetic; '
               'strong dribbler for a left back',
         int_l5_pattern='90/90/90/90/DNP', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; Galatasaray form solid', tier_revised='1'),
    dict(player='Moussa Niakhaté', position='DEF', sub_position='CB',
         club='Lyon', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=62.0, exp_post_group_mins_total=104,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Lyon CB; powerful and aerial; regular Senegal CB alongside Koulibaly',
         int_l5_pattern='90/90/90/DNP/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB partner to Koulibaly', tier_revised='2'),
    dict(player='El Hadji Malick Diouf', position='DEF', sub_position='RB',
         club='West Ham United', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=62.0, exp_post_group_mins_total=104,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='West Ham full-back; can play RB and LB; energetic; solid attacking contributions',
         int_l5_pattern='90/90/DNP/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular full-back rotation', tier_revised='2'),
    dict(player='Mamadou Sarr', position='DEF', sub_position='CB',
         club='Chelsea', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=60.0, exp_post_group_mins_total=98,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Young Chelsea CB; impressive technically; gaining international experience',
         int_l5_pattern='90/sub/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young regular CB rotation', tier_revised='2'),
    dict(player='Krépin Diatta', position='DEF', sub_position='RB',
         club='AS Monaco', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=60.0, exp_post_group_mins_total=98,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Monaco; versatile RB/winger; direct and attacking; regular Senegal option',
         int_l5_pattern='90/90/sub/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Versatile RB option; Monaco form', tier_revised='2'),
    dict(player='Ilay Camara', position='DEF', sub_position='LB',
         club='Anderlecht', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=40.0, exp_post_group_mins_total=46,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Anderlecht LB; squad depth behind Jakobs; young option',
         int_l5_pattern='90/DNP/sub/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup LB; Anderlecht squad level', tier_revised='3'),
    dict(player='Antoine Mendy', position='DEF', sub_position='RB',
         club='OGC Nice', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=40.0, exp_post_group_mins_total=46,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Nice RB; Senegal defensive rotation; limited WC starts expected',
         int_l5_pattern='90/DNP/90/DNP/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation RB; Nice squad level', tier_revised='3'),
    dict(player='Abdoulaye Seck', position='DEF', sub_position='CB',
         club='Maccabi Haifa', nationality='Senegal', group='I',
         wc_squad_prob_pct=80, tier='3', playing_role='Squad Player',
         group_mins_per_game=38.0, exp_post_group_mins_total=42,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Provisional 28-man squad (June 2 cut to 26 TBC); Maccabi Haifa CB; '
               'marginal selection; may be cut before tournament',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit',
         tier_evidence='Marginal CB; provisional squad inclusion', tier_revised='3'),
    dict(player='Moustapha Mbow', position='DEF', sub_position='RB',
         club='Paris FC', nationality='Senegal', group='I',
         wc_squad_prob_pct=80, tier='4', playing_role='Depth',
         group_mins_per_game=16.0, exp_post_group_mins_total=10,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Provisional; Paris FC Ligue 2; most likely to be cut before June 2',
         int_l5_pattern='90/DNP/DNP/DNP/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit',
         tier_evidence='Fringe provisional; Ligue 2 level; likely cut', tier_revised='4'),
    # ── Midfielders ──────────────────────────────────────────────────────
    dict(player='Pape Matar Sarr', position='MID', sub_position='CM',
         club='Tottenham Hotspur', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=80.0, exp_post_group_mins_total=162,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Tottenham CM (23); key creative force; returning from injury; '
               'dynamic box-to-box; key to Senegal\'s midfield engine',
         int_l5_pattern='90/sub/90/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key starter; Spurs form excellent', tier_revised='1'),
    dict(player='Lamine Camara', position='MID', sub_position='AM',
         club='AS Monaco', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=80.0, exp_post_group_mins_total=162,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Monaco AM; creative and progressive; key attacking midfielder; '
               'rapid development into Senegal\'s most creative player',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Creative starter; Monaco quality', tier_revised='1'),
    dict(player='Idrissa Gana Gueye', position='MID', sub_position='DM',
         club='Everton', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=62.0, exp_post_group_mins_total=100,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Managed',
         notes='Everton DM (36); experienced; late-season injury concern; '
               'managed load; defensive anchor; WC experience',
         int_l5_pattern='90/DNP(inj)/90/sub/90', int_l5_starts=3, int_absence_reason='Late-season injury',
         fitness_current='Managed: missed some late Everton games; cleared to play',
         tier_evidence='Veteran DM starter; managed load', tier_revised='2'),
    dict(player='Pape Gueye', position='MID', sub_position='CM',
         club='Villarreal', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=60.0, exp_post_group_mins_total=96,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Villarreal CM; physical and energetic; box-to-box rotation option',
         int_l5_pattern='90/90/DNP/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM rotation; Villarreal form', tier_revised='2'),
    dict(player='Pathé Ciss', position='MID', sub_position='DM',
         club='Rayo Vallecano', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=40.0, exp_post_group_mins_total=44,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Rayo Vallecano DM; defensive cover; squad rotation behind Gueye',
         int_l5_pattern='90/sub/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup DM; Rayo Vallecano level', tier_revised='3'),
    dict(player='Habib Diarra', position='MID', sub_position='CM',
         club='Sunderland', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=38.0, exp_post_group_mins_total=42,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Sunderland Championship CM; young developing talent; squad depth',
         int_l5_pattern='sub/90/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young squad depth CM', tier_revised='3'),
    dict(player='Bara Sapoko Ndiaye', position='MID', sub_position='CM',
         club='Bayern Munich', nationality='Senegal', group='I',
         wc_squad_prob_pct=80, tier='3', playing_role='Squad Player',
         group_mins_per_game=36.0, exp_post_group_mins_total=38,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Provisional; Bayern Munich (18); surprise call-up; youth talent; '
               'may be cut before June 2 deadline',
         int_l5_pattern='DNP/sub/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Provisional youth inclusion; minimal intl mins', tier_revised='3'),
    # ── Forwards ─────────────────────────────────────────────────────────
    dict(player='Sadio Mané', position='FWD', sub_position='',
         club='Al-Nassr', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=80.0, exp_post_group_mins_total=162,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Senegal all-time top scorer (51+ goals); Al-Nassr; came out of '
               'intl retirement; expected final WC; winger/CF; still decisive',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Star player; international retirement reversed for this WC', tier_revised='1'),
    dict(player='Nicolas Jackson', position='FWD', sub_position='',
         club='Chelsea', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=80.0, exp_post_group_mins_total=162,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Chelsea striker (Bayern loan 25-26); registered as Chelsea for WC; '
               'powerful and fast CF; strong finisher; key alongside Mané',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CF; Chelsea quality', tier_revised='1'),
    dict(player='Ismaïla Sarr', position='FWD', sub_position='',
         club='Crystal Palace', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=64.0, exp_post_group_mins_total=104,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Crystal Palace winger (26); pace and power; regular right-wing option; '
               'direct and dangerous in transition',
         int_l5_pattern='90/90/90/DNP/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular winger rotation', tier_revised='2'),
    dict(player='Iliman Ndiaye', position='FWD', sub_position='',
         club='Everton', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=62.0, exp_post_group_mins_total=100,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Everton forward; creative and direct; can play multiple forward positions; '
               'important squad member',
         int_l5_pattern='90/sub/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular attacking rotation', tier_revised='2'),
    dict(player='Assane Diao', position='FWD', sub_position='',
         club='Como', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=40.0, exp_post_group_mins_total=44,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Como Serie A forward; young and explosive; impact option off bench',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young impact option; Como form', tier_revised='3'),
    dict(player='Chérif Ndiaye', position='FWD', sub_position='',
         club='Samsunspor', nationality='Senegal', group='I',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=38.0, exp_post_group_mins_total=40,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Samsunspor forward; squad depth striker; limited WC minutes expected',
         int_l5_pattern='90/DNP/sub/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth forward; Turkish Süper Lig level', tier_revised='3'),
    dict(player='Bamba Dieng', position='FWD', sub_position='',
         club='Lorient', nationality='Senegal', group='I',
         wc_squad_prob_pct=80, tier='4', playing_role='Depth',
         group_mins_per_game=16.0, exp_post_group_mins_total=10,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Provisional; Lorient Ligue 2; may be cut before June 2 deadline; '
               'pace option but limited mins expected',
         int_l5_pattern='90/DNP/sub/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Provisional fringe; Ligue 2 level', tier_revised='4'),
    dict(player='Ibrahim Mbaye', position='FWD', sub_position='',
         club='Paris Saint-Germain', nationality='Senegal', group='I',
         wc_squad_prob_pct=80, tier='4', playing_role='Depth',
         group_mins_per_game=16.0, exp_post_group_mins_total=10,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Provisional; PSG youth forward; uncapped or minimal caps; '
               'may be cut before June 2 deadline',
         int_l5_pattern='DNP/sub/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Provisional youth forward; PSG system', tier_revised='4'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    updated = 0
    for row in rows:
        if row['nationality'] != 'Senegal':
            continue
        name = row['player']
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
