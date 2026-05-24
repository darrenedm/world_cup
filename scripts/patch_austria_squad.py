#!/usr/bin/env python3
"""
patch_austria_squad.py
Sync Austria rows with confirmed 26-man WC 2026 squad.
Announced by Ralf Rangnick on May 18, 2026.
Austria's first World Cup since 1998 — 28-year absence.
Run ONCE, then re-run compute_pts_per_90.py to rebuild adj pts.
"""
import csv

PATH = '/tmp/world_cup_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = set()
CORRECTIONS  = {}

# Group J: Argentina(10.0), Austria(5.9), Algeria(4.9), Jordan(2.5)
# Advance ~62%, dead rubber G3 ~22%
ADV = 62
DR  = 22

NEW_PLAYERS = [
    # ── Goalkeepers ──────────────────────────────────────────────────────
    dict(player='Alexander Schlager', position='GK', sub_position='',
         club='Red Bull Salzburg', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=158,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Austria No.1; Salzburg; 25 caps; reliable shot-stopper; '
               'commanding in the air; first WC for Austria in 28 years',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed No.1; Salzburg regular', tier_revised='GK1'),
    dict(player='Florian Wiegele', position='GK', sub_position='',
         club='Viktoria Plzen', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=8,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Viktoria Plzen GK; Austria No.2; no WC starts expected',
         int_l5_pattern='90/DNP/90/DNP/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK', tier_revised='GK2'),
    dict(player='Patrick Pentz', position='GK', sub_position='',
         club='Brondby', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Brondby GK; Austria No.3; no WC minutes expected',
         int_l5_pattern='DNP/90/DNP/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Scandinavian league', tier_revised='GK3'),
    # ── Defenders ────────────────────────────────────────────────────────
    dict(player='David Alaba', position='DEF', sub_position='CB',
         club='Real Madrid', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=62.0, exp_post_group_mins_total=100,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Managed',
         notes='Real Madrid captain; 13-month ACL recovery (Dec 2023 injury); '
               'limited 2025-26 minutes; announced Real Madrid departure May 22; '
               'free agent after tournament; included on form/experience not fitness',
         int_l5_pattern='sub/sub/90/DNP(inj)/sub', int_l5_starts=1, int_absence_reason='ACL Dec 2023',
         fitness_current='Managed: returning from ACL; Rangnick says he feels himself again',
         tier_evidence='T2: elite when fit but ACL limits guarantee; managed load', tier_revised='2'),
    dict(player='Kevin Danso', position='DEF', sub_position='CB',
         club='Tottenham Hotspur', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=80.0, exp_post_group_mins_total=158,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Tottenham CB; Austria\'s most dominant CB; powerful in the air; '
               'excellent reading of the game; PL quality; key defensive anchor',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Tottenham PL quality', tier_revised='1'),
    dict(player='Stefan Posch', position='DEF', sub_position='RB',
         club='Mainz 05', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=80.0, exp_post_group_mins_total=158,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Mainz RB; Austria first-choice right-back; solid and reliable; '
               'experienced Bundesliga presence; consistent performer',
         int_l5_pattern='90/90/90/90/DNP', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; Mainz Bundesliga', tier_revised='1'),
    dict(player='Philipp Lienhart', position='DEF', sub_position='CB',
         club='SC Freiburg', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=62.0, exp_post_group_mins_total=100,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Freiburg CB; regular Austria CB alongside Danso; '
               'composed on the ball; good recovery pace',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB; Freiburg Bundesliga', tier_revised='2'),
    dict(player='Marco Friedl', position='DEF', sub_position='LB',
         club='Werder Bremen', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=62.0, exp_post_group_mins_total=100,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Werder Bremen LB; Austria regular left-back; good in transition; '
               'overlapping and creative from deep',
         int_l5_pattern='90/90/DNP/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular LB starter; Werder form solid', tier_revised='2'),
    dict(player='Alexander Prass', position='DEF', sub_position='LB',
         club='TSG Hoffenheim', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=40.0, exp_post_group_mins_total=44,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Hoffenheim LB; Austria rotation; can play left-back and wide midfield; '
               'young and energetic',
         int_l5_pattern='90/sub/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation LB; Hoffenheim Bundesliga', tier_revised='3'),
    dict(player='Philipp Mwene', position='DEF', sub_position='RB',
         club='Mainz 05', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=36.0, exp_post_group_mins_total=38,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Mainz RB; Austria squad cover; backup for Posch',
         int_l5_pattern='sub/90/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup RB; Mainz Bundesliga', tier_revised='3'),
    dict(player='Michael Svoboda', position='DEF', sub_position='CB',
         club='Venezia', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=34.0, exp_post_group_mins_total=36,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Venezia CB; Austria 4th/5th CB option; Serie A squad level',
         int_l5_pattern='sub/DNP/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CB; Italian league', tier_revised='3'),
    dict(player='David Affengruber', position='DEF', sub_position='CB',
         club='SK Rapid Wien', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=14.0, exp_post_group_mins_total=8,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Rapid Wien CB; domestic selection; squad depth only',
         int_l5_pattern='DNP/sub/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Domestic depth CB; Austrian Bundesliga', tier_revised='4'),
    # ── Midfielders ──────────────────────────────────────────────────────
    dict(player='Marcel Sabitzer', position='MID', sub_position='CM',
         club='Borussia Dortmund', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=80.0, exp_post_group_mins_total=158,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Dortmund CM; Austria\'s best midfielder; dynamic box-to-box; '
               'goals and assists from deep; key to Rangnick\'s pressing system',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed key CM; Dortmund CL quality', tier_revised='1'),
    dict(player='Christoph Baumgartner', position='MID', sub_position='AM',
         club='RB Leipzig', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=78.0, exp_post_group_mins_total=152,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Leipzig AM; Austria\'s creative hub; excellent chance creation; '
               'technical and intelligent; key attacking option in Rangnick system',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Creative AM starter; Leipzig quality', tier_revised='1'),
    dict(player='Konrad Laimer', position='MID', sub_position='CM',
         club='Bayern Munich', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=64.0, exp_post_group_mins_total=104,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Bayern Munich CM; versatile — plays CM and can cover full-back; '
               'Rangnick uses him as a high-intensity runner; tireless pressing',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular starter; Bayern versatility', tier_revised='2'),
    dict(player='Xaver Schlager', position='MID', sub_position='CM',
         club='RB Leipzig', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=62.0, exp_post_group_mins_total=100,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Leipzig CM; technical and progressive; excellent passer; '
               'key midfield engine alongside Sabitzer',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM; Leipzig quality', tier_revised='2'),
    dict(player='Nicolas Seiwald', position='MID', sub_position='DM',
         club='RB Leipzig', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=60.0, exp_post_group_mins_total=96,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Leipzig DM; Austria\'s defensive midfield anchor; '
               'shields defence and distributes cleanly; key Rangnick selection',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular DM; Leipzig defensive anchor', tier_revised='2'),
    dict(player='Romano Schmid', position='MID', sub_position='AM',
         club='Werder Bremen', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=40.0, exp_post_group_mins_total=44,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Werder Bremen AM; energetic and creative; rotation AM option',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Impact AM; Werder Bundesliga', tier_revised='3'),
    dict(player='Patrick Wimmer', position='MID', sub_position='AM',
         club='VfL Wolfsburg', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=38.0, exp_post_group_mins_total=42,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Wolfsburg AM/winger; Austrian international; squad rotation',
         int_l5_pattern='90/sub/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation AM; Wolfsburg Bundesliga', tier_revised='3'),
    dict(player='Paul Wanner', position='MID', sub_position='AM',
         club='PSV Eindhoven', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=36.0, exp_post_group_mins_total=38,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='PSV AM (20); German-born newly naturalised Austrian; '
               'creative and technically gifted; youth talent with potential',
         int_l5_pattern='sub/90/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young squad AM; PSV quality', tier_revised='3'),
    dict(player='Carney Chukwuemeka', position='MID', sub_position='CM',
         club='Borussia Dortmund', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=34.0, exp_post_group_mins_total=36,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Dortmund CM (23); English-born Nigerian-heritage; newly naturalised Austrian; '
               'box-to-box energy; Dortmund squad rotation',
         int_l5_pattern='sub/90/DNP/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Naturalised rotation CM; Dortmund quality', tier_revised='3'),
    dict(player='Florian Grillitsch', position='MID', sub_position='DM',
         club='SC Braga', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=16.0, exp_post_group_mins_total=10,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Braga DM; veteran Austria international; squad depth; '
               'minimal WC minutes expected',
         int_l5_pattern='sub/DNP/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran depth DM; Portuguese league', tier_revised='4'),
    dict(player='Alessandro Schopf', position='MID', sub_position='CM',
         club='Wolfsberger AC', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=14.0, exp_post_group_mins_total=8,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Wolfsberger AC CM; domestic Austrian league; squad depth only',
         int_l5_pattern='DNP/sub/DNP/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Domestic depth CM; minimal mins', tier_revised='4'),
    # ── Forwards ─────────────────────────────────────────────────────────
    dict(player='Marko Arnautovic', position='FWD', sub_position='',
         club='FK Crvena Zvezda', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=75.0, exp_post_group_mins_total=148,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Red Star Belgrade striker; Austria record scorer (47 goals, 132 caps, age 37); '
               'physical CF; clinical and powerful; key aerial threat; '
               'iconic captain for Austria\'s historic return',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Record scorer; key starter; managed due to age 37', tier_revised='1'),
    dict(player='Michael Gregoritsch', position='FWD', sub_position='',
         club='FC Augsburg', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=62.0, exp_post_group_mins_total=100,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Augsburg striker (6\'4"); scored key qualifier equaliser vs Bosnia; '
               'aerial power and clinical finishing; important rotation behind Arnautovic',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Second striker; Augsburg form solid', tier_revised='2'),
    dict(player='Sasa Kalajdzic', position='FWD', sub_position='',
         club='LASK', nationality='Austria', group='J',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=60.0, exp_post_group_mins_total=96,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Wolves loanee at LASK; 7 goals 9 assists on loan; helped LASK domestic double; '
               'powerful physical presence; key part of Austrian domestic success',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third striker option; LASK loan form excellent', tier_revised='2'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    updated = 0
    for row in rows:
        if row['nationality'] != 'Austria':
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
