#!/usr/bin/env python3
"""
patch_croatia_squad.py
Sync Croatia rows with confirmed 26-man WC 2026 squad.
Announced by Zlatko Dalić on May 18, 2026.
Run ONCE, then re-run compute_pts_per_90.py to rebuild adj pts.
"""
import csv

PATH = '/tmp/world_cup_repo/data/master_sheet.csv'

NOT_SELECTED = set()  # Gvardiol only existing row — confirmed in squad

CONFIRMED_IN = {'Joško Gvardiol'}

CORRECTIONS = {
    'Joško Gvardiol': {
        'wc_squad_prob_pct': '100',
        'notes': 'Broken right leg Jan 4; surgery; back in group training May 8; '
                 'confirmed in squad May 18; no competitive mins since; match fitness concern Jun 17',
        'fitness_current': 'Injury: group training May 8; confirmed selection; match fitness TBC',
    },
}

# Croatia group L: advance 82%, dead rubber G3 30%
ADV = 82
DR  = 30

NEW_PLAYERS = [
    # ── Goalkeepers ──────────────────────────────────────────────────────
    dict(player='Dominik Livaković', position='GK', sub_position='',
         club='Dinamo Zagreb', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=198,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Croatia No.1; WC 2022 penalty hero (saved 3 in KO rounds); '
               'returned to Dinamo Zagreb; commanding shot-stopper',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed No.1; WC pedigree', tier_revised='GK1'),
    dict(player='Ivan Kotarski', position='GK', sub_position='',
         club='FC Copenhagen', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=10,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Croatia No.2; FC Copenhagen regular; no WC starts expected',
         int_l5_pattern='90/DNP/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; no minutes expected', tier_revised='GK2'),
    dict(player='Marko Pandur', position='GK', sub_position='',
         club='Hull City', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Croatia No.3; Hull City; third-choice only; no minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; squad depth only', tier_revised='GK3'),
    # ── Defenders ────────────────────────────────────────────────────────
    dict(player='Josip Stanišić', position='DEF', sub_position='RB',
         club='Bayern Munich', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=84.0, exp_post_group_mins_total=196,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Croatia first-choice RB; Bayern Munich regular; strong in possession '
               'and defensively reliable; covers at CB when needed',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed RB starter; Bayern quality', tier_revised='1'),
    dict(player='Duje Ćaleta-Car', position='DEF', sub_position='CB',
         club='Real Sociedad', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=84.0, exp_post_group_mins_total=196,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Experienced Croatia CB (28); Real Sociedad regular; '
               'dominant aerially and composed in possession',
         int_l5_pattern='90/90/90/90/DNP', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB pairing with Šutalo', tier_revised='1'),
    dict(player='Martin Erlić', position='DEF', sub_position='CB',
         club='Midtjylland', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=42.0, exp_post_group_mins_total=48,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Croatia squad CB; Midtjylland; rotation depth behind Ćaleta-Car/Šutalo/Gvardiol',
         int_l5_pattern='90/DNP/90/DNP/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third CB; rotation cover', tier_revised='3'),
    dict(player='Šime Vušković', position='DEF', sub_position='CB',
         club='Hamburger SV', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=18.0, exp_post_group_mins_total=14,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Young Croatia CB (22); Hamburg; fifth CB option; minimal minutes expected',
         int_l5_pattern='DNP/90/DNP/DNP/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='4th/5th CB; youth depth', tier_revised='4'),
    dict(player='Marin Pongračić', position='DEF', sub_position='CB',
         club='Fiorentina', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=68.0, exp_post_group_mins_total=130,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Croatia CB; Fiorentina; key rotation CB when Gvardiol managed; '
               'physical and aggressive; competes with Erlić for 4th CB spot',
         int_l5_pattern='90/90/DNP/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular rotation CB with Gvardiol managed', tier_revised='2'),
    dict(player='Domagoj Šutalo', position='DEF', sub_position='CB',
         club='Ajax', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=84.0, exp_post_group_mins_total=196,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Croatia first-choice CB alongside Ćaleta-Car; Ajax regular; '
               'composed on the ball; 25 years old; developing into a top CB',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed CB starter; Ajax pedigree', tier_revised='1'),
    # ── Midfielders ──────────────────────────────────────────────────────
    dict(player='Luka Modrić', position='MID', sub_position='CM',
         club='AC Milan', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=70.0, exp_post_group_mins_total=140,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Croatia legend (40); AC Milan; still a key starter under Dalić; '
               'managed with careful load; elite passing range and reading of the game',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key starter; managed at 40; sub around 70 min', tier_revised='2'),
    dict(player='Mateo Kovačić', position='MID', sub_position='CM',
         club='Manchester City', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=38.0, exp_post_group_mins_total=42,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Injury',
         notes='Achilles injury; missed most of 2025-26 season; '
               'included on fitness optimism; match readiness very uncertain by Jun 17',
         int_l5_pattern='DNP(inj)/DNP(inj)/DNP(inj)/sub/sub', int_l5_starts=0, int_absence_reason='Achilles tear',
         fitness_current='Injury: Achilles; returning late May; no competitive mins since Dec 2025',
         tier_evidence='T3: quality player but fitness huge doubt; bench at best if available',
         tier_revised='3'),
    dict(player='Mario Pašalić', position='MID', sub_position='AM',
         club='Atalanta', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=70.0, exp_post_group_mins_total=140,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Creative attacking MF; Atalanta Serie A regular; '
               'goals and assists from midfield; key to Croatia\'s attacking system',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular starter; Atalanta goal contributions', tier_revised='2'),
    dict(player='Nikola Vlašić', position='MID', sub_position='AM',
         club='Torino', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=65.0, exp_post_group_mins_total=120,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Croatia AM; Torino regular; energetic box-to-box player; '
               'regular Croatia starter; competes with Mario Pašalić for advanced MID role',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular rotation in Dalić system', tier_revised='2'),
    dict(player='Luka Sučić', position='MID', sub_position='CM',
         club='Real Sociedad', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=68.0, exp_post_group_mins_total=130,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Young Croatia CM (22); Real Sociedad; technical and progressive; '
               'established himself as key starter post-Modrić transition',
         int_l5_pattern='90/90/90/90/DNP', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Emerging key starter; Real Sociedad form excellent', tier_revised='2'),
    dict(player='Martin Baturina', position='MID', sub_position='AM',
         club='Como', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=42.0, exp_post_group_mins_total=48,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Young attacking MF (22); Como; creative dribbler and chance creator; '
               'impact sub option in Dalić\'s attacking system',
         int_l5_pattern='90/sub/90/DNP/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Impact AM sub; developing Croatia talent', tier_revised='3'),
    dict(player='Kristijan Jakić', position='MID', sub_position='DM',
         club='Augsburg', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=42.0, exp_post_group_mins_total=48,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Defensive MF; Augsburg; squad depth behind Modrić/Kovačić/L.Sučić; '
               'reliable holding option when needed',
         int_l5_pattern='90/DNP/sub/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='DM rotation; defensive cover', tier_revised='3'),
    dict(player='Petar Sučić', position='MID', sub_position='CM',
         club='Inter Milan', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=38.0, exp_post_group_mins_total=42,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Inter Milan youth product; Croatia CM (20); minimal first-team experience; '
               'squad depth with potential',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young depth option; Inter pedigree but limited mins', tier_revised='3'),
    dict(player='Nikola Moro', position='MID', sub_position='CM',
         club='Bologna', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=35.0, exp_post_group_mins_total=38,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Bologna CM; defensive-minded; squad cover; typically behind main starters',
         int_l5_pattern='90/sub/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation cover CM; Bologna squad level', tier_revised='3'),
    dict(player='Josip Fruk', position='MID', sub_position='CM',
         club='HNK Rijeka', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=18.0, exp_post_group_mins_total=14,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Domestic league product; Rijeka CM; squad depth selection; '
               'minimal WC minutes expected',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='4th/5th CM; domestic-league depth', tier_revised='4'),
    # ── Forwards ─────────────────────────────────────────────────────────
    dict(player='Andrej Kramarić', position='FWD', sub_position='',
         club='Hoffenheim', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=84.0, exp_post_group_mins_total=196,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Croatia\'s first-choice CF (33); Hoffenheim top scorer; '
               'prolific and clinical; national record scorer; lethal from set pieces',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed No.1 striker; national record holder', tier_revised='1'),
    dict(player='Ivan Perišić', position='FWD', sub_position='',
         club='PSV Eindhoven', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=68.0, exp_post_group_mins_total=130,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Veteran Croatia winger (35); PSV Eindhoven; experienced WC contributor; '
               'key left flank option; managed due to age but still influential',
         int_l5_pattern='90/90/sub/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Starting winger; veteran managed minutes', tier_revised='2'),
    dict(player='Ante Budimir', position='FWD', sub_position='',
         club='Osasuna', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=65.0, exp_post_group_mins_total=120,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Croatia back-up striker; Osasuna consistent scorer; '
               'strong aerial presence; rotation option behind Kramarić',
         int_l5_pattern='sub/90/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Second striker; Osasuna form solid', tier_revised='2'),
    dict(player='Marko Pašalić', position='FWD', sub_position='',
         club='Orlando City', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=42.0, exp_post_group_mins_total=48,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Croatia FWD; Orlando City MLS; impact option from the bench; '
               'useful rotation and set-piece threat',
         int_l5_pattern='90/sub/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Impact sub FWD; MLS form', tier_revised='3'),
    dict(player='Ivan Muša', position='FWD', sub_position='',
         club='FC Dallas', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=38.0, exp_post_group_mins_total=40,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Croatia FWD; FC Dallas MLS; squad depth striker; '
               'minimal WC starts expected; depth cover for Kramarić',
         int_l5_pattern='sub/90/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='MLS striker; squad depth only', tier_revised='3'),
    dict(player='Oliver Matanović', position='FWD', sub_position='',
         club='SC Freiburg', nationality='Croatia', group='L',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=35.0, exp_post_group_mins_total=38,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Young Croatia striker (21); SC Freiburg; emerging Bundesliga talent; '
               'pace and clinical finishing; depth option behind Kramarić/Budimir',
         int_l5_pattern='90/sub/90/DNP/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young depth striker; Freiburg development', tier_revised='3'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    updated = 0
    for row in rows:
        name = row['player']
        if row['nationality'] != 'Croatia':
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
