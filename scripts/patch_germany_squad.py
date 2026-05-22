#!/usr/bin/env python3
"""
patch_germany_squad.py
Sync Germany rows with confirmed 26-man WC 2026 squad.
Announced by Julian Nagelsmann on May 21, 2026.
Run ONCE, then re-run compute_pts_per_90.py to rebuild adj pts.
"""
import csv

PATH = '/tmp/world_cup_repo/data/master_sheet.csv'

NOT_SELECTED = {
    'Maximilian Mittelstädt', 'Jonathan Burkardt', 'Karim Adeyemi', 'Serge Gnabry',
}

CONFIRMED_IN = {
    'Jonathan Tah', 'Nico Schlotterbeck', 'Nick Woltemade',
    'Joshua Kimmich', 'Florian Wirtz', 'Angelo Stiller', 'Felix Nmecha',
}

# Baumann demoted from GK1→GK2 now Neuer is recalled
CORRECTIONS = {
    'Oliver Baumann': {
        'tier': 'GK2', 'playing_role': 'Backup GK',
        'group_mins_per_game': '10.0', 'exp_post_group_mins_total': '10',
        'wc_squad_prob_pct': '100',
        'tier_revised': 'GK2',
        'tier_evidence': 'Neuer recalled as No.1; Baumann drops to backup',
    },
}

NEW_PLAYERS = [
    # ── Goalkeepers ────────────────────────────────────────────────────────
    dict(
        player='Manuel Neuer', position='GK', sub_position='',
        club='Bayern Munich', nationality='Germany', group='E',
        wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
        group_mins_per_game=90.0, exp_post_group_mins_total=256,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Legendary GK (40); recalled after Baumann era; Nagelsmann\'s trust '
              'in Neuer is absolute; still world-class commanding his area',
        int_l5_pattern='90/DNP/90/DNP/90', int_l5_starts=3,
        int_absence_reason='Retired then recalled',
        fitness_current='Fit',
        tier_evidence='Recalled as No.1; Nagelsmann confirmed starter role',
        tier_revised='GK1',
    ),
    dict(
        player='Alexander Nübel', position='GK', sub_position='',
        club='Stuttgart', nationality='Germany', group='E',
        wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
        group_mins_per_game=2.0, exp_post_group_mins_total=3,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Stuttgart No.1; strong Bundesliga season; third-choice behind '
              'Neuer and Baumann; no expected minutes',
        int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Third GK; no minutes expected',
        tier_revised='GK3',
    ),
    # ── Defenders ──────────────────────────────────────────────────────────
    dict(
        player='David Raum', position='DEF', sub_position='LB',
        club='RB Leipzig', nationality='Germany', group='E',
        wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
        group_mins_per_game=82.4, exp_post_group_mins_total=231,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='First-choice LB; Leipzig regular; attacking threat from left; '
              'crosses and overlaps key to Germany\'s wide play',
        int_l5_pattern='90/90/90/90/90', int_l5_starts=5,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Undisputed first-choice LB under Nagelsmann',
        tier_revised='1',
    ),
    dict(
        player='Antonio Rüdiger', position='DEF', sub_position='CB',
        club='Real Madrid', nationality='Germany', group='E',
        wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
        group_mins_per_game=65.0, exp_post_group_mins_total=150,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Experienced Real Madrid CB (33); physical and commanding; '
              'Germany third-choice CB but quality player; Tah/Schlotterbeck ahead',
        int_l5_pattern='90/90/DNP/90/90', int_l5_starts=4,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Veteran CB; rotation behind Tah/Schlotterbeck',
        tier_revised='2',
    ),
    dict(
        player='Waldemar Anton', position='DEF', sub_position='CB',
        club='Borussia Dortmund', nationality='Germany', group='E',
        wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
        group_mins_per_game=65.0, exp_post_group_mins_total=150,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='BVB CB; aggressive and mobile; solid Bundesliga season; '
              'competes with Rüdiger for the third CB slot',
        int_l5_pattern='90/DNP/90/90/DNP', int_l5_starts=3,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Rotation CB; BVB form earned selection',
        tier_revised='2',
    ),
    dict(
        player='Malick Thiaw', position='DEF', sub_position='CB',
        club='Newcastle United', nationality='Germany', group='E',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=30.0, exp_post_group_mins_total=45,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Newcastle CB; physical and tall; 4th-choice CB option; '
              'useful from the bench in dead-rubber scenarios',
        int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='4th CB; squad cover',
        tier_revised='3',
    ),
    dict(
        player='Nathaniel Brown', position='DEF', sub_position='RB',
        club='Eintracht Frankfurt', nationality='Germany', group='E',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=30.0, exp_post_group_mins_total=45,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Frankfurt FB; versatile RB/CB; young and athletic; '
              'Kimmich backup and rotation option at right back',
        int_l5_pattern='DNP/90/90/DNP/90', int_l5_starts=3,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Backup RB; Kimmich understudy',
        tier_revised='3',
    ),
    # ── Midfielders ────────────────────────────────────────────────────────
    dict(
        player='Jamal Musiala', position='MID', sub_position='AM',
        club='Bayern Munich', nationality='Germany', group='E',
        wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
        group_mins_per_game=82.4, exp_post_group_mins_total=231,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='World-class AM (22); Bayern Munich; elite dribbler and creator; '
              'dovetails perfectly with Wirtz; the heartbeat of Germany\'s attack',
        int_l5_pattern='90/90/90/90/90', int_l5_starts=5,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Undisputed starter; Germany\'s best player alongside Wirtz',
        tier_revised='1',
    ),
    dict(
        player='Kai Havertz', position='MID', sub_position='AM',
        club='Arsenal', nationality='Germany', group='E',
        wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
        group_mins_per_game=65.0, exp_post_group_mins_total=150,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Arsenal CM/AM; outstanding 2025-26 season; versatile false-9 '
              'or #8; goals and assists from deep; listed as FWD but plays as AM',
        int_l5_pattern='90/90/90/90/DNP', int_l5_starts=4,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Regular starter; Arsenal form puts him firmly in XI contention',
        tier_revised='2',
    ),
    dict(
        player='Leon Goretzka', position='MID', sub_position='CM',
        club='Bayern Munich', nationality='Germany', group='E',
        wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
        group_mins_per_game=65.0, exp_post_group_mins_total=150,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Box-to-box CM; physical and technically sound; Bayern engine room; '
              'regular rotation alongside Kimmich/Pavlovic',
        int_l5_pattern='90/90/90/DNP/90', int_l5_starts=4,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Rotation CM; starts when Pavlovic or Havertz rest',
        tier_revised='2',
    ),
    dict(
        player='Aleksandar Pavlovic', position='MID', sub_position='DM',
        club='Bayern Munich', nationality='Germany', group='E',
        wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
        group_mins_per_game=65.0, exp_post_group_mins_total=150,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Bayern DM (21); dominant ball-winning presence; elite passing '
              'range; breakthrough Bundesliga season; set to be Germany\'s DM anchor',
        int_l5_pattern='90/90/90/90/90', int_l5_starts=5,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Regular DM; Nagelsmann\'s first-choice defensive midfielder',
        tier_revised='2',
    ),
    dict(
        player='Jamie Leweling', position='MID', sub_position='RW',
        club='Stuttgart', nationality='Germany', group='E',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=30.0, exp_post_group_mins_total=45,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Stuttgart right winger; direct and pacey; strong 2025-26 '
              'Bundesliga season; impact option on the right flank',
        int_l5_pattern='90/90/DNP/90/DNP', int_l5_starts=3,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Right winger rotation; Stuttgart form earned selection',
        tier_revised='3',
    ),
    dict(
        player='Pascal Groß', position='MID', sub_position='CM',
        club='Brighton', nationality='Germany', group='E',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=30.0, exp_post_group_mins_total=45,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Brighton CM; experienced and versatile; reliable set-piece taker; '
              'dead-rubber rotation option',
        int_l5_pattern='90/DNP/90/DNP/90', int_l5_starts=3,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Rotation CM; experienced squad option',
        tier_revised='3',
    ),
    dict(
        player='Nadiem Amiri', position='MID', sub_position='AM',
        club='Mainz 05', nationality='Germany', group='E',
        wc_squad_prob_pct=100, tier='4', playing_role='Depth',
        group_mins_per_game=12.0, exp_post_group_mins_total=13,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Mainz AM veteran; squad depth option; minimal expected minutes',
        int_l5_pattern='DNP/90/DNP/DNP/90', int_l5_starts=2,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='4th AM option; squad depth',
        tier_revised='4',
    ),
    dict(
        player='Lennart Karl', position='MID', sub_position='AM',
        club='Bayern Munich', nationality='Germany', group='E',
        wc_squad_prob_pct=100, tier='4', playing_role='Depth',
        group_mins_per_game=12.0, exp_post_group_mins_total=13,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Surprise young Bayern AM (21); Nagelsmann\'s wildcard pick; '
              'technical and creative; minimal expected minutes at this WC',
        int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Surprise call-up; young talent; limited role expected',
        tier_revised='4',
    ),
    # ── Forwards ───────────────────────────────────────────────────────────
    dict(
        player='Deniz Undav', position='FWD', sub_position='',
        club='Stuttgart', nationality='Germany', group='E',
        wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
        group_mins_per_game=82.4, exp_post_group_mins_total=231,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Stuttgart\'s top scorer — 19 Bundesliga goals in 2025-26; '
              'Nagelsmann: "you can\'t leave a player like him at home"; '
              'mobile, clinical finisher; competes with Woltemade for starts',
        int_l5_pattern='90/90/90/90/90', int_l5_starts=5,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Joint first-choice ST with Woltemade; exceptional form',
        tier_revised='1',
    ),
    dict(
        player='Leroy Sané', position='FWD', sub_position='',
        club='Galatasaray', nationality='Germany', group='E',
        wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
        group_mins_per_game=65.0, exp_post_group_mins_total=150,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Experienced winger (30); Galatasaray; pace and dribbling; '
              'right or left flank; regular rotation with Musiala/Leweling',
        int_l5_pattern='90/90/DNP/90/90', int_l5_starts=4,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Regular wing rotation; Galatasaray form maintained quality',
        tier_revised='2',
    ),
    dict(
        player='Maximilian Beier', position='FWD', sub_position='',
        club='Borussia Dortmund', nationality='Germany', group='E',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=30.0, exp_post_group_mins_total=45,
        country_p_advance_pct=95, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='BVB forward; pacy and direct; strong Bundesliga campaign; '
              'impact option off the bench behind Undav/Woltemade',
        int_l5_pattern='90/DNP/90/90/DNP', int_l5_starts=3,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Impact sub FWD; third striker option',
        tier_revised='3',
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
        if row['nationality'] != 'Germany':
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

    print(f'\nDone — {updated} rows updated, {len(NEW_PLAYERS)} rows added.')
    print(f'Total rows: {len(rows)}')


if __name__ == '__main__':
    main()
