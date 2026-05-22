#!/usr/bin/env python3
"""
patch_france_squad.py
Sync France dataset rows with the confirmed 26-man WC 2026 squad.
Announced by Deschamps on May 14, 2026.
Run ONCE, then re-run compute_pts_per_90.py to rebuild adj pts.
"""
import csv, os

PATH = '/tmp/world_cup_repo/data/master_sheet.csv'

# Players confirmed NOT in the France squad (already in CSV at 0% or need zeroing)
NOT_SELECTED = {
    'Lucas Chevalier', 'Leny Yoro', 'Hugo Ekitiké',
}

# Players confirmed IN the squad already in CSV — set to 100%
CONFIRMED_IN = {
    'Mike Maignan', 'William Saliba', 'Dayot Upamecano', 'Jules Koundé',
    'Kylian Mbappé', 'Ousmane Dembélé', 'Michael Olise',
    'Rayan Cherki', 'Désiré Doué', 'Maghnes Akliouche',
}

# Club/role corrections for existing players
CORRECTIONS = {
    'Ousmane Dembélé':  {'club': 'Barcelona'},
    'Rayan Cherki':     {'club': 'Olympique Lyonnais'},
    'Maghnes Akliouche': {
        'tier': '3', 'playing_role': 'Impact Sub',
        'group_mins_per_game': '30.0', 'exp_post_group_mins_total': '50',
        'tier_revised': '3',
        'tier_evidence': 'Confirmed squad; Monaco breakout season; impact sub',
    },
}

# 16 new players to add
NEW_PLAYERS = [
    # ── Goalkeepers ────────────────────────────────────────────────────────
    dict(
        player='Brice Samba', position='GK', sub_position='',
        club='Lens', nationality='France', group='I',
        wc_squad_prob_pct=100, tier='GK2', playing_role='Backup GK',
        group_mins_per_game=10.0, exp_post_group_mins_total=10,
        country_p_advance_pct=97, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Reliable Lens No.1; proven Ligue 1 penalty stopper; Maignan backup',
        int_l5_pattern='DNP/90/DNP/DNP/DNP', int_l5_starts=1,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Clear No.2 behind Maignan; no realistic route to starts',
        tier_revised='GK2',
    ),
    dict(
        player='Robin Risser', position='GK', sub_position='',
        club='Lens', nationality='France', group='I',
        wc_squad_prob_pct=100, tier='GK3', playing_role='Third GK',
        group_mins_per_game=2.0, exp_post_group_mins_total=3,
        country_p_advance_pct=97, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Young Lens keeper; first senior WC call-up; third choice',
        int_l5_pattern='DNP/DNP/DNP/90/DNP', int_l5_starts=1,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Third GK; no expected minutes',
        tier_revised='GK3',
    ),
    # ── Defenders ──────────────────────────────────────────────────────────
    dict(
        player='Theo Hernandez', position='DEF', sub_position='LB',
        club='AC Milan', nationality='France', group='I',
        wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
        group_mins_per_game=82.4, exp_post_group_mins_total=288,
        country_p_advance_pct=97, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='France first-choice LB; among the best attacking FBs in the world; '
              'goal threat from left; AC Milan captain',
        int_l5_pattern='90/90/90/90/90', int_l5_starts=5,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Undisputed first-choice LB; outstanding 2025-26 with Milan',
        tier_revised='1',
    ),
    dict(
        player='Ibrahima Konaté', position='DEF', sub_position='CB',
        club='Liverpool', nationality='France', group='I',
        wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
        group_mins_per_game=65.0, exp_post_group_mins_total=160,
        country_p_advance_pct=97, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Liverpool CB; powerful and quick; Saliba/Upamecano first-choice pair '
              'but Konaté partners either in rotation; excellent aerial presence',
        int_l5_pattern='90/90/90/DNP/90', int_l5_starts=4,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Third CB option but high quality; regular squad minutes',
        tier_revised='2',
    ),
    dict(
        player='Lucas Hernandez', position='DEF', sub_position='LB',
        club='Athletic Bilbao', nationality='France', group='I',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=30.0, exp_post_group_mins_total=50,
        country_p_advance_pct=97, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Theo\'s brother; versatile LB/CB; strong campaign with Bilbao; '
              'backup to Theo but more than capable of starting',
        int_l5_pattern='90/DNP/90/90/DNP', int_l5_starts=3,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='LB backup; Theo\'s understudy; 3rd CB option too',
        tier_revised='3',
    ),
    dict(
        player='Malo Gusto', position='DEF', sub_position='RB',
        club='Chelsea', nationality='France', group='I',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=30.0, exp_post_group_mins_total=50,
        country_p_advance_pct=97, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Chelsea RB; quick and technical; Koundé backup; good in transition',
        int_l5_pattern='DNP/90/90/DNP/90', int_l5_starts=3,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Backup RB behind Koundé; rotation option',
        tier_revised='3',
    ),
    dict(
        player='Lucas Digne', position='DEF', sub_position='LB',
        club='Aston Villa', nationality='France', group='I',
        wc_squad_prob_pct=100, tier='4', playing_role='Depth',
        group_mins_per_game=12.0, exp_post_group_mins_total=15,
        country_p_advance_pct=97, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Veteran LB (32); Villa regular; squad depth behind the Hernandez brothers',
        int_l5_pattern='DNP/90/DNP/90/DNP', int_l5_starts=2,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='4th LB option; squad cover only',
        tier_revised='4',
    ),
    dict(
        player='Maxence Lacroix', position='DEF', sub_position='CB',
        club='Crystal Palace', nationality='France', group='I',
        wc_squad_prob_pct=100, tier='4', playing_role='Depth',
        group_mins_per_game=12.0, exp_post_group_mins_total=15,
        country_p_advance_pct=97, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Surprise call-up after strong Crystal Palace season; 4th CB option',
        int_l5_pattern='DNP/DNP/90/DNP/DNP', int_l5_starts=1,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='4th CB; squad cover; strong club form earned call-up',
        tier_revised='4',
    ),
    # ── Midfielders ────────────────────────────────────────────────────────
    dict(
        player='Aurélien Tchouaméni', position='MID', sub_position='DM',
        club='Real Madrid', nationality='France', group='I',
        wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
        group_mins_per_game=82.4, exp_post_group_mins_total=288,
        country_p_advance_pct=97, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='France\'s first-choice DM; Real Madrid regular; elite ball-winner '
              'and distributor; screens the defence and launches attacks',
        int_l5_pattern='90/90/90/90/90', int_l5_starts=5,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Undisputed DM starter; key to France\'s defensive structure',
        tier_revised='1',
    ),
    dict(
        player='Warren Zaïre-Emery', position='MID', sub_position='CM',
        club='AS Roma', nationality='France', group='I',
        wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
        group_mins_per_game=65.0, exp_post_group_mins_total=160,
        country_p_advance_pct=97, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Young dynamic CM (20); outstanding box-to-box energy; '
              'pressing and carrying; expected to start most games',
        int_l5_pattern='90/90/90/90/90', int_l5_starts=5,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Regular starter at 20; Deschamps trusts him fully',
        tier_revised='2',
    ),
    dict(
        player='Adrien Rabiot', position='MID', sub_position='CM',
        club='Marseille', nationality='France', group='I',
        wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
        group_mins_per_game=65.0, exp_post_group_mins_total=160,
        country_p_advance_pct=97, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Experienced CM; Marseille resurgence; physical and creative; '
              'box-to-box presence and occasional goals',
        int_l5_pattern='90/90/90/90/DNP', int_l5_starts=4,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Regular France CM; competes with ZE for starts',
        tier_revised='2',
    ),
    dict(
        player='Manu Koné', position='MID', sub_position='CM',
        club='Real Madrid', nationality='France', group='I',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=30.0, exp_post_group_mins_total=50,
        country_p_advance_pct=97, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Powerful CM; Real Madrid squad member; strong pressing and carrying; '
              'impact option from the bench',
        int_l5_pattern='90/DNP/90/90/DNP', int_l5_starts=3,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Impact sub CM; competes with Rabiot for minutes',
        tier_revised='3',
    ),
    dict(
        player="N'Golo Kanté", position='MID', sub_position='DM',
        club='Al-Ittihad', nationality='France', group='I',
        wc_squad_prob_pct=100, tier='4', playing_role='Depth',
        group_mins_per_game=12.0, exp_post_group_mins_total=15,
        country_p_advance_pct=97, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Legendary veteran (35); recalled on form; limited role expected '
              'but still elite in short bursts; Saudi League pace concerns',
        int_l5_pattern='45/DNP/45/90/DNP', int_l5_starts=2,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Veteran squad option; Tchouaméni/ZE ahead of him',
        tier_revised='4',
    ),
    # ── Forwards ───────────────────────────────────────────────────────────
    dict(
        player='Marcus Thuram', position='FWD', sub_position='',
        club='Inter Milan', nationality='France', group='I',
        wc_squad_prob_pct=100, tier='1', playing_role='Automatic Starter',
        group_mins_per_game=82.4, exp_post_group_mins_total=288,
        country_p_advance_pct=97, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='France\'s first-choice CF; outstanding 2025-26 Inter season; '
              'powerful, technical, links play brilliantly; Serie A top scorer',
        int_l5_pattern='90/90/90/90/90', int_l5_starts=5,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Undisputed No.9 for France; world-class 2025-26 form',
        tier_revised='1',
    ),
    dict(
        player='Bradley Barcola', position='FWD', sub_position='',
        club='Paris Saint-Germain', nationality='France', group='I',
        wc_squad_prob_pct=100, tier='2', playing_role='Regular Starter',
        group_mins_per_game=65.0, exp_post_group_mins_total=160,
        country_p_advance_pct=97, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='PSG flyer; rapid left-footed winger; outstanding 2025-26 '
              'Ligue 1 season; direct and explosive; key rotation with Mbappé/Dembélé',
        int_l5_pattern='90/90/90/90/90', int_l5_starts=5,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Regular France starter; elite pace and directness',
        tier_revised='2',
    ),
    dict(
        player='Jean-Philippe Mateta', position='FWD', sub_position='',
        club='Crystal Palace', nationality='France', group='I',
        wc_squad_prob_pct=100, tier='3', playing_role='Impact Sub',
        group_mins_per_game=30.0, exp_post_group_mins_total=50,
        country_p_advance_pct=97, country_p_dead_rubber_g3_pct=60,
        fitness_flag='Fit',
        notes='Physical CF; strong Palace campaign; powerful target man alternative '
              'to Thuram; selected over Kolo Muani for physical presence',
        int_l5_pattern='DNP/90/DNP/90/DNP', int_l5_starts=2,
        int_absence_reason='',
        fitness_current='Fit',
        tier_evidence='Impact sub CF; Thuram backup; physical option off bench',
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
        if row['nationality'] != 'France':
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
