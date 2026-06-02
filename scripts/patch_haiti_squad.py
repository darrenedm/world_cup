#!/usr/bin/env python3
"""
patch_haiti_squad.py — official 26-man squad (Sébastien Migné, announced May 15 2026).
Group C: Morocco(8.3), Brazil(7.9), Scotland(5.0), Haiti(1.2).
Advance 2%, dead rubber G3 10%.
HISTORIC RETURN — Haiti's first WC appearance in 52 years (last appeared 1974).
All players except one (Woodensky Pierre, Violette AC) developed abroad.
Diaspora-heavy squad: primarily France, Belgium, England, Portugal, USA and Canada.
Captain: Johny Placide (GK, 38yo). Stars: Jean-Ricner Bellegarde (Wolves), Wilson Isidor (Sunderland).
Both Bellegarde and Isidor switched allegiance from France in 2025.
Duckens Nazon: Haiti all-time leading scorer; scored hat-trick vs Costa Rica in qualifying.
Average age 24; only 5 players older than 30.
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
    dict(player='Johny Placide', position='GK', sub_position='', club='Unattached', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='GK1', playing_role='Starting GK',
         group_mins_per_game=90.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Haiti captain and veteran GK (38yo); undisputed No.1 for historic WC return; experienced campaigner '
               'who has been Haiti\'s backbone for years; leads the team in their first WC since 1974',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Captain and undisputed GK1; veteran 38yo', tier_revised='GK1'),
    dict(player='Alexandre Pierre', position='GK', sub_position='', club='Unattached', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
         group_mins_per_game=5.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Haiti No.2 keeper; backup behind Placide; no starts expected in group stage',
         int_l5_pattern='90/DNP/DNP/90/DNP', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Backup GK; Haiti squad', tier_revised='GK2'),
    dict(player='Josue Duverger', position='GK', sub_position='', club='Unattached', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
         group_mins_per_game=0.0, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Haiti third-choice keeper; no WC minutes expected',
         int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Third GK; Haiti squad', tier_revised='GK3'),
    # Defenders
    dict(player='Jean-Kévin Duverne', position='DEF', sub_position='CB', club='Unattached', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Haiti first-choice centre-back; commanding and experienced; one of Haiti\'s most reliable defenders; '
               'diaspora-based defender; key in Group C defensive organisation',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CB; Haiti defence leader', tier_revised='1'),
    dict(player='Hannes Delcroix', position='DEF', sub_position='CB', club='Unattached', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Haiti regular centre-back; Belgium-developed; physical and combative CB; strong aerial presence; '
               'part of Haiti\'s central defensive partnership',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Regular CB; Belgium-based development', tier_revised='1'),
    dict(player='Ricardo Adé', position='DEF', sub_position='RB', club='Unattached', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Haiti first-choice right-back; France-developed; athletic and disciplined; key in right flank for Haiti',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice RB; France-developed', tier_revised='1'),
    dict(player='Wilguens Paugain', position='DEF', sub_position='LB', club='Unattached', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Haiti first-choice left-back; energetic and attacking-minded fullback; key in Haiti\'s left flank',
         int_l5_pattern='90/sub/90/90/sub', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice LB; Haiti squad', tier_revised='1'),
    dict(player='Duke Lacroix', position='DEF', sub_position='CB', club='Unattached', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Haiti defensive rotation; CB/LB versatility; squad depth option across the back line',
         int_l5_pattern='90/sub/sub/90/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation DEF; Haiti squad', tier_revised='2'),
    dict(player='Martin Expérience', position='DEF', sub_position='CB', club='Unattached', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Haiti defensive rotation; experienced CB option; squad depth in central defence',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CB; Haiti squad', tier_revised='2'),
    dict(player='Carlens Arcus', position='DEF', sub_position='RB', club='Unattached', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Haiti fullback depth option; limited WC minutes expected',
         int_l5_pattern='sub/DNP/90/sub/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='FB depth; Haiti squad', tier_revised='3'),
    dict(player='Keeto Thermoncy', position='DEF', sub_position='CB', club='Unattached', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Haiti CB squad depth; limited WC minutes expected',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CB depth; Haiti squad', tier_revised='3'),
    # Midfielders
    dict(player='Jean-Ricner Bellegarde', position='MID', sub_position='CM', club='Wolverhampton Wanderers', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Wolverhampton Wanderers CM (Premier League); Haiti key midfielder; switched allegiance from France in Aug 2025; '
               'combative and technically proficient; Premier League quality is massive boost for Haiti\'s midfield; '
               'one of the two headline signings for Haiti\'s WC campaign',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Haiti star CM; switched from France; Wolves Premier League', tier_revised='1'),
    dict(player='Carl-Fred Sainthe', position='MID', sub_position='CM', club='El Paso Locomotive FC', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='El Paso Locomotive FC CM (USL); Haiti midfield starter; energetic and hardworking; '
               'key figure in Haiti\'s qualifying campaign',
         int_l5_pattern='90/90/90/sub/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CM; El Paso Locomotive USL Championship', tier_revised='1'),
    dict(player='Jean-Jacques Danley', position='MID', sub_position='CM', club='Philadelphia Union', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Philadelphia Union CM (MLS); Haiti regular midfielder; MLS quality; energetic and versatile; '
               'part of Haiti\'s midfield core for Group C',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice CM; Philadelphia Union MLS', tier_revised='1'),
    dict(player='Dominique Simon', position='MID', sub_position='CM', club='FC Tatran Prešov', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FC Tatran Prešov CM (Slovakia); Haiti midfield rotation; Slovak league; squad depth in midfield',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; FC Tatran Prešov Slovak Super Liga', tier_revised='2'),
    dict(player='Leverton Pierre', position='MID', sub_position='CM', club='FC Vizela', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FC Vizela CM (Portugal Liga Portugal 2); Haiti midfield rotation; Portuguese second-tier experience; '
               'technically capable squad option',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CM; FC Vizela Liga Portugal 2', tier_revised='2'),
    dict(player='Woodensky Pierre', position='MID', sub_position='CM', club='Violette AC', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Violette AC CM (Haiti); only domestic-based player in entire 26-man squad; symbolic selection; '
               'limited WC minutes expected',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CM depth; Violette AC Haitian Championnat National; sole domestic pick', tier_revised='3'),
    # Forwards
    dict(player='Wilson Isidor', position='FWD', sub_position='CF', club='Sunderland', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Sunderland CF (Championship); Haiti headline striker; switched allegiance from France early 2026; '
               'pace, power and finishing; Championship quality; made debut for Haiti in March 2026 warm-up; '
               'the new face of Haiti\'s attack for historic WC campaign',
         int_l5_pattern='90/90/90/90/90', int_l5_starts=5, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Haiti star CF; switched from France; Sunderland Championship', tier_revised='1'),
    dict(player='Duckens Nazon', position='FWD', sub_position='CF', club='Esteghlal FC', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Esteghlal FC CF (Iran); Haiti all-time leading goalscorer; scored 6 qualifying goals including a hat-trick '
               'vs Costa Rica; the veteran talisman of Haiti\'s resurgence; clinical finisher; '
               'indispensable to Haiti\'s attack',
         int_l5_pattern='90/90/90/90/sub', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Haiti all-time top scorer; first-choice CF; Esteghlal FC Iran Pro League', tier_revised='1'),
    dict(player='Derrick Etienne', position='FWD', sub_position='WNG', club='Toronto FC', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
         group_mins_per_game=T1G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Toronto FC WNG (MLS); Haiti experienced attacker; direct wide forward; MLS quality; '
               'key in Haiti\'s wide attack alongside Isidor and Nazon',
         int_l5_pattern='90/90/sub/90/90', int_l5_starts=4, int_absence_reason='',
         fitness_current='Fit', tier_evidence='First-choice WNG; Toronto FC MLS', tier_revised='1'),
    dict(player='Frantzdy Pierrot', position='FWD', sub_position='CF', club='Çaykur Rizespor', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Çaykur Rizespor CF (Turkey Süper Lig); Haiti rotation striker; Süper Lig experience; '
               'physical CF option providing rotation behind Isidor/Nazon',
         int_l5_pattern='90/sub/90/sub/90', int_l5_starts=3, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation CF; Çaykur Rizespor Süper Lig', tier_revised='2'),
    dict(player='Josué Casimir', position='FWD', sub_position='WNG', club='AJ Auxerre', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
         group_mins_per_game=T2G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='AJ Auxerre WNG (Ligue 1); Haiti wide attacker; Ligue 1 quality; direct and pacy from the flank; '
               'rotation option in wide areas',
         int_l5_pattern='sub/90/sub/90/sub', int_l5_starts=2, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Rotation WNG; AJ Auxerre Ligue 1', tier_revised='2'),
    dict(player='Lenny Joseph', position='FWD', sub_position='CF', club='Ferencváros TC', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Ferencváros TC CF (Hungary); Haiti striker depth; Hungarian OTP Bank Liga; Champions League preliminary experience; '
               'limited WC minutes expected',
         int_l5_pattern='sub/DNP/sub/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='CF depth; Ferencváros TC Hungarian OTP Bank Liga', tier_revised='3'),
    dict(player='Ruben Providence', position='FWD', sub_position='WNG', club='Almere City FC', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='Almere City FC WNG (Netherlands Eerste Divisie); Haiti wide forward depth; Dutch football; '
               'limited WC minutes expected',
         int_l5_pattern='DNP/sub/sub/DNP/90', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='WNG depth; Almere City FC Dutch Eerste Divisie', tier_revised='3'),
    dict(player='Yassin Fortune', position='FWD', sub_position='WNG', club='FC Vizela', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='3', playing_role='Squad Player',
         group_mins_per_game=T3G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FC Vizela WNG (Portugal Liga Portugal 2); Haiti forward depth; Portuguese second-tier; limited WC minutes expected',
         int_l5_pattern='sub/sub/DNP/90/DNP', int_l5_starts=1, int_absence_reason='',
         fitness_current='Fit', tier_evidence='WNG depth; FC Vizela Liga Portugal 2', tier_revised='3'),
    dict(player='Louicius Deedson', position='FWD', sub_position='CF', club='FC Dallas', nationality='Haiti', group='C',
         wc_squad_prob_pct=100, tier='4', playing_role='Fringe Player',
         group_mins_per_game=T4G, exp_post_group_mins_total=0,
         country_p_advance_pct=ADV, country_p_dead_rubber_g3_pct=DR, fitness_flag='Fit',
         notes='FC Dallas CF (MLS); Haiti fringe striker; MLS-based; minimal WC minutes expected; squad depth only',
         int_l5_pattern='DNP/DNP/sub/sub/DNP', int_l5_starts=0, int_absence_reason='',
         fitness_current='Fit', tier_evidence='Fringe CF; FC Dallas MLS', tier_revised='4'),
]


def main():
    with open(PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    updated = 0
    for row in rows:
        if row['nationality'] != 'Haiti': continue
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
