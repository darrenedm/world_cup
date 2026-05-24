#!/usr/bin/env python3
"""
patch_switzerland_squad.py
Sync Switzerland rows with confirmed 26-man WC 2026 squad.
Announced by Murat Yakin on May 20, 2026.
Note: Gregor Kobel already in CSV — update to 100%, add 25 new.
Run ONCE, then re-run compute_pts_per_90.py to rebuild adj pts.
"""
import csv

PATH = '/tmp/world_cup_repo/data/master_sheet.csv'

NOT_SELECTED = set()
CONFIRMED_IN = {'Gregor Kobel'}

CORRECTIONS = {
    'Gregor Kobel': {
        'wc_squad_prob_pct': '100',
        'club': 'Borussia Dortmund',
        'country_p_advance_pct': '87',
        'country_p_dead_rubber_g3_pct': '20',
    },
}

# Group B: Switzerland(6.5), Canada(5.7), Qatar(3.7), Bosnia(2.2)
# Advance ~87%, dead rubber G3 ~20%
ADV = 87
DR  = 20

NEW_PLAYERS = [
    # ── Goalkeepers ──────────────────────────────────────────────────────
    dict(player='Marvin Keller', position='GK', sub_position='',
         club='BSC Young Boys', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=10,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Young Boys GK; Switzerland No.2 behind Kobel; no WC starts expected',
         int_l5_pattern='90/DNP/90/DNP/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; domestic league', tier_revised='GK2'),
    dict(player='Yvon Mvogo', position='GK', sub_position='',
         club='Lorient', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Lorient GK; Switzerland No.3; no WC minutes expected',
         int_l5_pattern='DNP/90/DNP/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Ligue 1 squad level', tier_revised='GK3'),
    # ── Defenders ────────────────────────────────────────────────────────
    dict(player='Manuel Akanji', position='DEF', sub_position='CB',
         club='Inter Milan', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=82.0, exp_post_group_mins_total=200,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Inter Milan CB (29); Switzerland No.1 CB; elite in possession and defending; '
               'Champions League quality; key to Yakin\'s build-out',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed first-choice CB; Inter CL quality', tier_revised='1'),
    dict(player='Silvan Widmer', position='DEF', sub_position='RB',
         club='Mainz 05', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=82.0, exp_post_group_mins_total=200,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Mainz RB; Switzerland first-choice right-back; solid defensively; '
               'contributes in attack with crosses and overlaps',
         int_l5_pattern='90/90/90/90/DNP', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; Mainz Bundesliga regular', tier_revised='1'),
    dict(player='Nico Elvedi', position='DEF', sub_position='CB',
         club='Borussia Mönchengladbach', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=66.0, exp_post_group_mins_total=160,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Gladbach CB (28); regular partner to Akanji; physical and aggressive; '
               'aerial strength; consistent Switzerland presence',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB starter; Gladbach consistent', tier_revised='2'),
    dict(player='Ricardo Rodriguez', position='DEF', sub_position='LB',
         club='Real Betis', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=64.0, exp_post_group_mins_total=152,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Veteran Switzerland LB (32); Real Betis; 4th World Cup; '
               'experienced and reliable; left-back anchor',
         int_l5_pattern='90/90/DNP/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Veteran LB; 4th WC; Real Betis LaLiga', tier_revised='2'),
    dict(player='Aurele Amenda', position='DEF', sub_position='CB',
         club='Eintracht Frankfurt', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=62.0, exp_post_group_mins_total=148,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Frankfurt CB; solid and technical; rotation CB option for Yakin',
         int_l5_pattern='90/90/DNP/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB rotation; Frankfurt quality', tier_revised='2'),
    dict(player='Eray Comert', position='DEF', sub_position='CB',
         club='Valencia', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=40.0, exp_post_group_mins_total=52,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Valencia CB; 4th CB option; squad depth cover',
         int_l5_pattern='90/DNP/sub/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup CB; Valencia LaLiga', tier_revised='3'),
    dict(player='Miro Muheim', position='DEF', sub_position='LB',
         club='Hamburger SV', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=38.0, exp_post_group_mins_total=48,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Hamburg LB; backup behind Rodriguez; squad depth only',
         int_l5_pattern='sub/DNP/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup LB; Bundesliga 2', tier_revised='3'),
    dict(player='Luca Jaquez', position='DEF', sub_position='CB',
         club='VfB Stuttgart', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=36.0, exp_post_group_mins_total=44,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Stuttgart CB; 5th CB option; minimal WC minutes expected',
         int_l5_pattern='DNP/sub/90/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Depth CB; Stuttgart Bundesliga', tier_revised='3'),
    # ── Midfielders ──────────────────────────────────────────────────────
    dict(player='Granit Xhaka', position='MID', sub_position='CM',
         club='Sunderland', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=82.0, exp_post_group_mins_total=200,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Sunderland CM captain (33); 144 caps; 4th World Cup; '
               'Switzerland heartbeat; tenacious tackler and excellent passer; '
               'now in Championship but quality undimmed',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain; undisputed starter; 4th WC', tier_revised='1'),
    dict(player='Dan Ndoye', position='MID', sub_position='AM',
         club='Nottingham Forest', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=80.0, exp_post_group_mins_total=196,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Nottingham Forest winger (24); direct and explosive; '
               'Switzerland\'s most dangerous attacking threat on the right; '
               'Premier League quality earning him T1 status',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Key wide attacker; Forest PL form strong', tier_revised='1'),
    dict(player='Remo Freuler', position='MID', sub_position='CM',
         club='Bologna', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=66.0, exp_post_group_mins_total=160,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Bologna CM; experienced and reliable; key Xhaka partnership in midfield; '
               'excellent work rate and distribution',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CM partner to Xhaka; Bologna form', tier_revised='2'),
    dict(player='Ruben Vargas', position='MID', sub_position='AM',
         club='Sevilla', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=64.0, exp_post_group_mins_total=152,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Sevilla winger (26); left-wing option; direct and pacy; '
               'key attacking rotation for Yakin',
         int_l5_pattern='90/90/DNP/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular left winger; Sevilla LaLiga', tier_revised='2'),
    dict(player='Noah Okafor', position='MID', sub_position='AM',
         club='Leeds United', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=60.0, exp_post_group_mins_total=144,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Leeds forward/winger; pace and power; versatile attacker; '
               'regular Switzerland option; PL promotion with Leeds',
         int_l5_pattern='90/sub/90/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular wide forward; Leeds PL', tier_revised='2'),
    dict(player='Ardon Jashari', position='MID', sub_position='CM',
         club='AC Milan', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=60.0, exp_post_group_mins_total=140,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='AC Milan CM (22); Switzerland\'s most exciting midfield talent; '
               'technical, progressive, and dynamic; Serie A quality',
         int_l5_pattern='90/90/sub/90/DNP', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young key CM; Milan quality', tier_revised='2'),
    dict(player='Denis Zakaria', position='MID', sub_position='DM',
         club='AS Monaco', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=40.0, exp_post_group_mins_total=52,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Monaco DM; powerful and athletic; rotation option behind Freuler/Xhaka',
         int_l5_pattern='sub/90/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation DM; Monaco Ligue 1', tier_revised='3'),
    dict(player='Djibril Sow', position='MID', sub_position='CM',
         club='Sevilla', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=38.0, exp_post_group_mins_total=48,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Sevilla CM; versatile in midfield; squad depth option',
         int_l5_pattern='90/sub/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; Sevilla squad level', tier_revised='3'),
    dict(player='Michel Aebischer', position='MID', sub_position='CM',
         club='Pisa', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=36.0, exp_post_group_mins_total=44,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Pisa CM (Italian league); squad depth midfielder',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Squad CM; lower-tier European league', tier_revised='3'),
    dict(player='Fabian Rieder', position='MID', sub_position='AM',
         club='FC Augsburg', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=36.0, exp_post_group_mins_total=42,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Augsburg AM; young talent; squad depth attacking option',
         int_l5_pattern='sub/90/DNP/DNP/sub', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Young AM rotation; Augsburg Bundesliga', tier_revised='3'),
    dict(player='Joan Manzambi', position='MID', sub_position='CM',
         club='SC Freiburg', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=18.0, exp_post_group_mins_total=14,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Freiburg CM; 5th/6th midfield option; depth only',
         int_l5_pattern='sub/DNP/DNP/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Deep squad CM; minimal mins expected', tier_revised='4'),
    dict(player='Christian Fassnacht', position='MID', sub_position='AM',
         club='BSC Young Boys', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='4', playing_role='Depth',
         group_mins_per_game=16.0, exp_post_group_mins_total=12,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Young Boys AM; surprise recall; domestic league option; depth',
         int_l5_pattern='90/DNP/sub/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Surprise recall; domestic league depth', tier_revised='4'),
    # ── Forwards ─────────────────────────────────────────────────────────
    dict(player='Breel Embolo', position='FWD', sub_position='',
         club='Rennes', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=80.0, exp_post_group_mins_total=196,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Rennes striker (27); Switzerland No.1 CF; physical power and clinical; '
               'dangerous from set pieces; key WC 2022 scorer',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Undisputed first-choice striker; Rennes form', tier_revised='1'),
    dict(player='Zeki Amdouni', position='FWD', sub_position='',
         club='Burnley', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=60.0, exp_post_group_mins_total=140,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Managed',
         notes='Burnley striker; ACL rupture Jul 2025; returned late-season with <60 min all 2025-26; '
               'selected on 11-goal intl record; match fitness a concern',
         int_l5_pattern='sub/DNP(inj)/DNP(inj)/sub/sub', int_l5_starts=0, int_absence_reason='ACL Jul 2025',
         fitness_current='Managed: returning from ACL; limited minutes; Yakin optimistic',
         tier_evidence='T2 potential; quality if fit — ACL recovery limits starts', tier_revised='2'),
    dict(player='Cedric Itten', position='FWD', sub_position='',
         club='Fortuna Düsseldorf', nationality='Switzerland', group='B',
         wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
         group_mins_per_game=38.0, exp_post_group_mins_total=48,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR,
         fitness_flag='Fit',
         notes='Düsseldorf striker; surprise inclusion; target man option; '
               'impact sub cover for Embolo',
         int_l5_pattern='90/sub/DNP/sub/90', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third-choice striker; Bundesliga 2', tier_revised='3'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    updated = 0
    for row in rows:
        if row['nationality'] != 'Switzerland':
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
