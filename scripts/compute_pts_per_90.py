#!/usr/bin/env python3
"""
compute_pts_per_90.py
Compute expected fantasy points for each player in master_sheet.csv.
Adds columns: action_pts_per_90, exp_pts_per_90, total_exp_fantasy_pts
"""
import csv

# ──────────────────────────────────────────────
# TEAM PARAMETERS
# (group_win_draw_bonus, group_cs_pct, group_gc_per_game,
#  ko_win_pct, ko_cs_pct, ko_gc_per_game)
# group_win_draw_bonus = P(win)*30 + P(draw)*15
# ko stage: no draws, so bonus = ko_win_pct * 30
# ──────────────────────────────────────────────
TEAM = {
    'France':      (21.6, 0.45, 0.70, 0.59, 0.35, 0.60),
    'Argentina':   (21.6, 0.42, 0.70, 0.59, 0.35, 0.60),
    'Spain':       (21.9, 0.42, 0.70, 0.59, 0.35, 0.60),
    'England':     (20.9, 0.38, 0.80, 0.54, 0.30, 0.70),
    'Portugal':    (20.5, 0.35, 0.80, 0.54, 0.30, 0.70),
    'Morocco':     (20.1, 0.33, 1.10, 0.49, 0.25, 0.90),
    'Netherlands': (20.0, 0.38, 0.80, 0.49, 0.28, 0.80),
    'Germany':     (21.5, 0.40, 0.70, 0.49, 0.28, 0.80),
    'Brazil':      (19.9, 0.30, 1.10, 0.49, 0.25, 0.90),
    'Belgium':     (20.8, 0.38, 0.80, 0.46, 0.25, 0.90),
    'Croatia':     (18.1, 0.30, 1.10, 0.40, 0.22, 1.00),
    'Colombia':    (18.4, 0.32, 0.90, 0.40, 0.22, 1.00),
    'Switzerland': (19.8, 0.30, 1.00, 0.38, 0.20, 1.00),
    'USA':         (18.0, 0.30, 1.00, 0.38, 0.20, 1.00),
    'Canada':      (18.9, 0.25, 1.10, 0.33, 0.18, 1.10),
    'Ecuador':     (18.1, 0.22, 1.20, 0.33, 0.18, 1.10),
    'Uruguay':     (19.4, 0.32, 0.90, 0.44, 0.25, 0.90),
    'Turkey':      (15.1, 0.22, 1.30, 0.30, 0.15, 1.20),
    'Norway':      (13.5, 0.18, 1.60, 0.22, 0.15, 1.30),
    'Sweden':      (11.4, 0.15, 1.70, 0.22, 0.15, 1.30),
    'Scotland':    (15.2, 0.18, 1.60, 0.22, 0.15, 1.30),
    'Egypt':       (17.1, 0.22, 1.40, 0.22, 0.15, 1.30),
    'Ivory Coast': (15.2, 0.18, 1.50, 0.26, 0.15, 1.20),
    'Ghana':       ( 6.3, 0.08, 2.50, 0.08, 0.05, 2.00),
}

CS_BONUS = {'GK': 40, 'DEF': 30, 'MID': 10, 'FWD': 0}
GC_PEN   = {'GK':  5, 'DEF':  5, 'MID':  3, 'FWD': 0}

# ──────────────────────────────────────────────
# POSITIONAL BASELINES (per 90, pre-WC calibration)
# ──────────────────────────────────────────────
BASELINE = {
    'GK1': dict(saves_ib=3.0, saves_ob=0.8, saves_pen=0.04, pickups=6.0, catches=1.5,
                punches=0.8, sweeper=0.3, cross_nc=0.25, six_sec=0.010,
                yellow=0.06, disposs=0.5, miscont=0.20,
                duels_won=0.5, duels_lost=0.5, fouls_comm=0.1,
                pen_giveaway=0.010, err_goal=0.020, err_shot=0.050),
    'CB':  dict(goals=0.03, assists=0.05, SoT=0.20, shots_off=0.10,
                bcc=0.06, key2=0.10, passes_own=45, passes_opp=12, pass_pct=0.88,
                tackles=1.5, last_tack=0.040, intercepts=2.0, intercepts_box=0.15,
                duels_won=3.5, duels_lost=2.5,
                blocks=0.5, blocks_6yd=0.12, crosses_blocked=0.15, clearance_line=0.012,
                recoveries=3.5, clear=5.0, head_clear=3.0,
                dribbles=0.2, disposs=0.5, miscont=0.60,
                fouls_won=0.3, pen_won=0.020, offsides=0,
                yellow=0.12, red=0.0, fouls_comm=1.2,
                own_goals=0.010, pen_giveaway=0.040, err_goal=0.025, err_shot=0.060),
    'FB':  dict(goals=0.05, assists=0.12, SoT=0.40, shots_off=0.40,
                bcc=0.30, key2=0.20, passes_own=25, passes_opp=30, pass_pct=0.87,
                tackles=1.8, last_tack=0.030, intercepts=1.5, intercepts_box=0.08,
                duels_won=3.0, duels_lost=2.5,
                blocks=0.3, blocks_6yd=0.06, crosses_blocked=0.30, clearance_line=0.006,
                recoveries=3.0, clear=2.0, head_clear=1.0,
                dribbles=1.2, disposs=0.8, miscont=0.85,
                fouls_won=1.0, pen_won=0.060, offsides=0,
                yellow=0.10, red=0.0, fouls_comm=1.0,
                own_goals=0.008, pen_giveaway=0.050, err_goal=0.020, err_shot=0.050),
    'DM':  dict(goals=0.06, assists=0.08, SoT=0.40, shots_off=0.50,
                bcm=0.05, bcc=0.20, key2=0.20, passes_own=35, passes_opp=25, pass_pct=0.90,
                tackles=2.5, last_tack=0.040, intercepts=2.0, intercepts_box=0.10,
                duels_won=4.0, duels_lost=3.0,
                blocks=0.4, blocks_6yd=0.08, crosses_blocked=0.10, clearance_line=0.003,
                recoveries=5.0, clear=0.8, head_clear=0.3,
                dribbles=0.8, disposs=0.7, miscont=1.00,
                fouls_won=0.8, pen_won=0.050, offsides=0,
                yellow=0.14, red=0.0, fouls_comm=1.5,
                own_goals=0.002, pen_giveaway=0.040, err_goal=0.015, err_shot=0.040),
    'CM':  dict(goals=0.10, assists=0.12, SoT=0.60, shots_off=0.80,
                bcm=0.08, bcc=0.40, key2=0.30, passes_own=28, passes_opp=28, pass_pct=0.87,
                tackles=1.8, last_tack=0.020, intercepts=1.5, intercepts_box=0.06,
                duels_won=3.0, duels_lost=2.5,
                blocks=0.3, blocks_6yd=0.04, crosses_blocked=0.08, clearance_line=0.002,
                recoveries=3.5, clear=0.5, head_clear=0.2,
                dribbles=1.0, disposs=0.8, miscont=1.20,
                fouls_won=1.0, pen_won=0.080, offsides=0,
                yellow=0.12, red=0.0, fouls_comm=1.2,
                own_goals=0.001, pen_giveaway=0.020, err_goal=0.010, err_shot=0.030),
    'AM':  dict(goals=0.20, assists=0.20, SoT=1.00, shots_off=0.80,
                bcm=0.15, bcc=0.70, key2=0.40, passes_own=10, passes_opp=22, pass_pct=0.84,
                tackles=1.0, last_tack=0.010, intercepts=0.8, intercepts_box=0.04,
                duels_won=2.5, duels_lost=2.5,
                blocks=0.1, blocks_6yd=0.01, crosses_blocked=0.04, clearance_line=0.001,
                recoveries=2.0, clear=0.2, head_clear=0.1,
                dribbles=2.0, disposs=1.5, miscont=1.50,
                fouls_won=1.5, pen_won=0.120, offsides=0.2,
                yellow=0.10, red=0.0, fouls_comm=0.8,
                own_goals=0.001, pen_giveaway=0.020, err_goal=0.008, err_shot=0.020),
    'CF':  dict(goals=0.40, assists=0.12, SoT=2.00, shots_off=1.50,
                bcm=0.50, bcc=0.20, key2=0.10, passes_own=2, passes_opp=10, pass_pct=0.78,
                tackles=0.3, last_tack=0.000, intercepts=0.3, intercepts_box=0.02,
                duels_won=2.0, duels_lost=2.0,
                blocks=0.0, blocks_6yd=0.00, crosses_blocked=0.01, clearance_line=0.000,
                recoveries=1.5, clear=0.0, head_clear=0.3,
                dribbles=1.5, disposs=1.5, miscont=1.80,
                fouls_won=2.5, pen_won=0.150, offsides=1.5,
                yellow=0.10, red=0.0, fouls_comm=1.5,
                own_goals=0.001, pen_giveaway=0.030, err_goal=0.005, err_shot=0.015),
    'WNG': dict(goals=0.25, assists=0.25, SoT=1.50, shots_off=1.00,
                bcm=0.30, bcc=0.80, key2=0.35, passes_own=5, passes_opp=18, pass_pct=0.78,
                tackles=0.8, last_tack=0.000, intercepts=0.7, intercepts_box=0.02,
                duels_won=2.5, duels_lost=2.5,
                blocks=0.0, blocks_6yd=0.00, crosses_blocked=0.02, clearance_line=0.000,
                recoveries=2.0, clear=0.0, head_clear=0.1,
                dribbles=3.0, disposs=2.0, miscont=2.00,
                fouls_won=2.0, pen_won=0.150, offsides=0.5,
                yellow=0.10, red=0.0, fouls_comm=1.0,
                own_goals=0.001, pen_giveaway=0.040, err_goal=0.005, err_shot=0.015),
}
BASELINE['GK2'] = dict(BASELINE['GK1'])
BASELINE['GK3'] = dict(BASELINE['GK1'])

# WC calibration multipliers (applied to per-90 rates)
WC = dict(
    goals=0.82, assists=0.82, SoT=0.85, shots_off=0.85, bcm=0.85, bcc=0.85,
    key2=1.00, passes_own=1.05, passes_opp=1.05, pass_pct=1.00,
    tackles=1.10, last_tack=1.10, intercepts=1.10, intercepts_box=1.10,
    duels_won=1.10, duels_lost=1.10,
    blocks=1.10, blocks_6yd=1.10, crosses_blocked=1.10, clearance_line=1.05,
    recoveries=1.10, clear=1.10, head_clear=1.10,
    dribbles=0.90, disposs=0.90, miscont=0.88,
    fouls_won=1.00, pen_won=0.90, offsides=0.90,
    yellow=1.20, red=1.20, fouls_comm=1.10,
    own_goals=0.80, pen_giveaway=0.85, err_goal=0.80, err_shot=0.85,
    saves_ib=1.05, saves_ob=1.05, saves_pen=1.00, pickups=1.05, catches=1.05,
    punches=1.05, sweeper=1.05, cross_nc=0.85, six_sec=0.85,
)

# Individual stat overrides (pre-WC calibration club rates)
OVR = {
    'Erling Haaland':    dict(goals=0.82, assists=0.25, SoT=1.76, shots_off=2.13, bcm=0.60, yellow=0.04),
    'Harry Kane':        dict(goals=1.30, assists=0.20, SoT=2.51, shots_off=1.96, bcm=0.80, yellow=0.04),
    'Kylian Mbappé':     dict(goals=0.90, assists=0.15, SoT=2.00, shots_off=1.50, dribbles=3.5, yellow=0.05,
                              pen_won=0.18, miscont=1.80),
    'Lamine Yamal':      dict(goals=0.63, assists=0.43, SoT=2.50, shots_off=2.00, bcc=1.20, dribbles=4.0, yellow=0.05,
                              pen_won=0.18, miscont=2.50),
    'Mohamed Salah':     dict(goals=0.31, assists=0.26, SoT=1.30, shots_off=1.00, dribbles=2.5, yellow=0.04),
    'Vinícius Júnior':   dict(goals=0.51, assists=0.17, SoT=1.80, shots_off=1.50, dribbles=2.4, yellow=0.27,
                              pen_won=0.22, miscont=2.50),
    'Bukayo Saka':       dict(goals=0.33, assists=0.20, SoT=1.50, shots_off=1.50, bcc=0.80, dribbles=3.0, yellow=0.08,
                              pen_won=0.16, miscont=1.80),
    'Amad Diallo':       dict(goals=0.18, assists=0.09, SoT=1.00, shots_off=1.20, dribbles=3.5, yellow=0.04),
    'Viktor Gyökeres':   dict(goals=0.57, assists=0.04, SoT=1.80, shots_off=1.50, bcm=0.55, yellow=0.20),
    'Kenan Yıldız':      dict(goals=0.33, assists=0.20, SoT=1.50, shots_off=1.20, yellow=0.07),
    'Mohammed Kudus':    dict(goals=0.12, assists=0.35, SoT=0.52, shots_off=0.90, bcc=0.70, dribbles=4.0, yellow=0.17,
                              pen_won=0.14, miscont=2.20),
    'Christian Pulisic': dict(goals=0.56, assists=0.21, SoT=1.80, shots_off=1.20, yellow=0.08),
    'Jonathan David':    dict(goals=0.31, assists=0.23, SoT=1.40, shots_off=1.50, yellow=0.05),
    'Alexander Isak':    dict(goals=0.25, assists=0.15, SoT=1.50, shots_off=1.20, yellow=0.08),
    'Ousmane Dembélé':   dict(goals=0.22, assists=0.25, SoT=1.40, shots_off=1.20, dribbles=3.0, yellow=0.12),
    'Julián Álvarez':    dict(goals=0.38, assists=0.19, SoT=1.23, shots_off=1.20, yellow=0.09),
    'Luis Díaz':         dict(goals=0.50, assists=0.43, SoT=1.80, shots_off=1.20, bcc=0.90, dribbles=2.5, yellow=0.08),
    'Raphinha':          dict(goals=0.75, assists=0.20, SoT=1.29, shots_off=1.20, bcc=0.80, dribbles=2.8, yellow=0.27),
    'Omar Marmoush':     dict(goals=0.20, assists=0.15, SoT=1.20, shots_off=1.00, yellow=0.08),
    'Scott McTominay':   dict(goals=0.17, assists=0.12, SoT=1.14, shots_off=1.80, yellow=0.04),
    'Martin Ødegaard':   dict(goals=0.08, assists=0.42, SoT=0.80, bcc=1.00, key2=0.50, yellow=0.05),
    'Bruno Fernandes':   dict(goals=0.26, assists=0.61, SoT=0.77, shots_off=1.80, bcc=1.00, key2=0.50, yellow=0.07),
    'Joshua Kimmich':    dict(goals=0.07, assists=0.24, SoT=0.60, passes_own=52, passes_opp=52,
                              pass_pct=0.925, tackles=1.27, intercepts=0.92, recoveries=4.2,
                              bcc=0.54, key2=0.40, yellow=0.04),
    'Jude Bellingham':   dict(goals=0.21, assists=0.21, SoT=1.25, yellow=0.04),
    'Declan Rice':       dict(goals=0.12, assists=0.15, SoT=0.50, passes_own=45, passes_opp=25,
                              pass_pct=0.90, tackles=1.97, intercepts=1.08, recoveries=5.24, yellow=0.09),
    'Florian Wirtz':     dict(goals=0.22, assists=0.15, SoT=1.00, yellow=0.04),
    'Federico Valverde': dict(goals=0.17, assists=0.27, SoT=1.00, tackles=1.80, intercepts=1.20, yellow=0.06),
    'Pedri':             dict(goals=0.09, assists=0.38, SoT=0.60, passes_own=30, passes_opp=50,
                              pass_pct=0.90, bcc=0.60, yellow=0.11),
    'Moisés Caicedo':    dict(goals=0.10, assists=0.03, SoT=0.30, passes_own=40, passes_opp=25,
                              pass_pct=0.88, tackles=4.0, intercepts=2.6, recoveries=5.5,
                              yellow=0.38, red=0.034, pen_giveaway=0.07),
    'Michael Olise':     dict(goals=0.59, assists=0.75, SoT=1.89, shots_off=1.20, bcc=1.20, dribbles=3.0, yellow=0.31),
    'Dani Olmo':         dict(goals=0.33, assists=0.38, SoT=0.99, bcc=0.70, yellow=0.05),
    'Ryan Gravenberch':  dict(goals=0.13, assists=0.10, SoT=0.36, passes_own=40, passes_opp=30,
                              pass_pct=0.91, tackles=2.0, intercepts=1.5, recoveries=4.5, yellow=0.16),
    'Arda Güler':        dict(goals=0.16, assists=0.31, SoT=1.20, yellow=0.08),
    'Hakan Çalhanoğlu':  dict(goals=0.49, assists=0.22, SoT=0.93, passes_own=38, passes_opp=28,
                              pass_pct=0.91, tackles=2.0, intercepts=1.8, yellow=0.38, pen_giveaway=0.06),
    'Kevin De Bruyne':   dict(goals=0.43, assists=0.09, SoT=0.94, bcc=0.80, key2=0.45, yellow=0.09),
    'Vitinha':           dict(goals=0.08, assists=0.20, SoT=0.60, passes_own=35, passes_opp=35,
                              pass_pct=0.92, yellow=0.06),
    'João Neves':        dict(goals=0.06, assists=0.15, SoT=0.40, passes_own=32, passes_opp=32,
                              pass_pct=0.91, tackles=2.5, intercepts=1.8, yellow=0.08),
    'Joško Gvardiol':    dict(goals=0.14, assists=0.14, SoT=0.40, yellow=0.14),
    'Nuno Mendes':       dict(goals=0.06, assists=0.15, SoT=0.40, dribbles=1.5, yellow=0.08),
    'Nick Woltemade':    dict(goals=0.45, assists=0.15, SoT=1.80, shots_off=1.20, yellow=0.12),
    'Rafael Leão':       dict(goals=0.46, assists=0.18, SoT=1.70, shots_off=1.00, dribbles=3.5, yellow=0.10),
    'Jérémy Doku':       dict(goals=0.12, assists=0.22, SoT=0.90, shots_off=0.80, dribbles=5.2, bcc=0.90, yellow=0.14,
                              pen_won=0.16, miscont=3.00),
    'Emiliano Martínez': dict(saves_pen=0.10),
    'Thibaut Courtois':  dict(saves_pen=0.09),
    'Gregor Kobel':      dict(saves_pen=0.08),
    'Jordan Pickford':   dict(saves_pen=0.06),
    'Achraf Hakimi':     dict(goals=0.13, assists=0.13, SoT=0.59, dribbles=2.0, yellow=0.20, red=0.066,
                              pen_won=0.10, miscont=1.50, pen_giveaway=0.06),
    'Reece James':       dict(goals=0.08, assists=0.15, SoT=0.45, dribbles=1.8, yellow=0.12,
                              pen_won=0.05, miscont=0.70),
    'John Stones':       dict(goals=0.05, assists=0.06, SoT=0.18,
                              passes_own=50, passes_opp=14, pass_pct=0.91,
                              tackles=1.2, intercepts=1.8, yellow=0.09),
    'Kobbie Mainoo':     dict(goals=0.08, assists=0.10, SoT=0.45,
                              passes_own=28, passes_opp=25, pass_pct=0.88,
                              tackles=2.2, intercepts=1.5, yellow=0.10),
    'Anthony Gordon':    dict(goals=0.18, assists=0.18, SoT=1.20, shots_off=0.90,
                              dribbles=2.5, yellow=0.10, pen_won=0.08, miscont=1.80),
    'Noni Madueke':      dict(goals=0.22, assists=0.16, SoT=1.30, shots_off=0.90,
                              dribbles=2.5, yellow=0.09, pen_won=0.09, miscont=1.70),
    'Ivan Toney':        dict(goals=0.40, assists=0.08, SoT=1.50, shots_off=1.20,
                              bcm=0.40, yellow=0.15),
    # France
    'Marcus Thuram':     dict(goals=0.55, assists=0.25, SoT=2.00, shots_off=1.00,
                              bcm=0.45, yellow=0.12),
    'Theo Hernandez':    dict(goals=0.18, assists=0.22, SoT=0.70, dribbles=2.0,
                              tackles=1.5, yellow=0.22, pen_won=0.06),
    'Aurélien Tchouaméni': dict(goals=0.06, assists=0.06, SoT=0.30,
                              passes_own=45, passes_opp=8, pass_pct=0.90,
                              tackles=3.5, intercepts=2.0, yellow=0.15),
    'Bradley Barcola':   dict(goals=0.35, assists=0.22, SoT=1.60, shots_off=1.00,
                              dribbles=3.5, yellow=0.08, pen_won=0.07, miscont=1.60),
    'Warren Zaïre-Emery': dict(goals=0.10, assists=0.14, SoT=0.60,
                              passes_own=30, passes_opp=22, pass_pct=0.87,
                              tackles=2.0, intercepts=1.2, yellow=0.12),
    'Adrien Rabiot':     dict(goals=0.12, assists=0.14, SoT=0.65,
                              passes_own=28, passes_opp=20, pass_pct=0.85,
                              tackles=2.2, intercepts=1.0, yellow=0.18),
    'Ibrahima Konaté':   dict(goals=0.08, assists=0.04, SoT=0.22,
                              passes_own=48, passes_opp=12, pass_pct=0.91,
                              tackles=1.2, intercepts=1.8, yellow=0.10),
    # Portugal
    'Diogo Costa':       dict(saves_pen=0.12),
    'Cristiano Ronaldo': dict(goals=0.48, assists=0.12, SoT=1.80, shots_off=1.40,
                              bcm=0.35, yellow=0.10),
    'Bernardo Silva':    dict(goals=0.14, assists=0.22, SoT=0.80,
                              passes_own=32, passes_opp=32, pass_pct=0.88,
                              dribbles=2.5, bcc=0.8, yellow=0.12),
    'Gonçalo Ramos':     dict(goals=0.55, assists=0.12, SoT=1.80, shots_off=0.90,
                              bcm=0.30, dribbles=1.2, yellow=0.10),
    'João Cancelo':      dict(goals=0.12, assists=0.18, SoT=0.55, dribbles=2.5,
                              yellow=0.18, pen_won=0.05),
    'Francisco Conceição': dict(goals=0.22, assists=0.18, SoT=1.20, shots_off=0.80,
                              dribbles=3.0, yellow=0.10, pen_won=0.08, miscont=1.60),
    'João Félix':        dict(goals=0.25, assists=0.22, SoT=1.10, dribbles=2.5,
                              bcc=0.3, yellow=0.12, pen_won=0.08),
    # Germany
    'Manuel Neuer':      dict(saves_pen=0.07),
    'Jamal Musiala':     dict(goals=0.30, assists=0.25, SoT=1.50, shots_off=0.80,
                              dribbles=3.5, bcc=0.8, yellow=0.10, pen_won=0.08),
    'Kai Havertz':       dict(goals=0.25, assists=0.15, SoT=1.20, shots_off=0.70,
                              bcm=0.20, passes_own=28, passes_opp=22, pass_pct=0.87,
                              yellow=0.12),
    'Deniz Undav':       dict(goals=0.55, assists=0.14, SoT=1.80, shots_off=1.00,
                              bcm=0.30, yellow=0.12),
    'Leroy Sané':        dict(goals=0.28, assists=0.22, SoT=1.40, shots_off=0.90,
                              dribbles=3.0, yellow=0.14, pen_won=0.06, miscont=1.80),
    'Leon Goretzka':     dict(goals=0.14, assists=0.18, SoT=0.70,
                              passes_own=30, passes_opp=25, pass_pct=0.87,
                              tackles=2.0, intercepts=1.2, yellow=0.16),
    'Aleksandar Pavlovic': dict(goals=0.06, assists=0.10, SoT=0.35,
                              passes_own=40, passes_opp=20, pass_pct=0.89,
                              tackles=3.0, intercepts=1.8, yellow=0.12),
    # Belgium
    'Romelu Lukaku':     dict(goals=0.55, assists=0.12, SoT=1.80, shots_off=1.20,
                              bcm=0.55, yellow=0.18),
    'Amadou Onana':      dict(goals=0.06, assists=0.10, SoT=0.40,
                              passes_own=38, passes_opp=22, pass_pct=0.87,
                              tackles=3.8, intercepts=2.0, yellow=0.20),
    'Leandro Trossard':  dict(goals=0.28, assists=0.22, SoT=1.40, shots_off=0.80,
                              dribbles=2.5, yellow=0.10, pen_won=0.06),
    'Charles De Ketelaere': dict(goals=0.22, assists=0.20, SoT=1.10, shots_off=0.70,
                              dribbles=2.8, bcc=0.6, yellow=0.14),
    # Brazil
    'Alisson Becker':    dict(saves_pen=0.08),
    'Bruno Guimarães':   dict(goals=0.12, assists=0.18, SoT=0.60,
                              passes_own=35, passes_opp=28, pass_pct=0.88,
                              tackles=3.2, intercepts=1.8, yellow=0.18),
    'Marquinhos':        dict(goals=0.08, assists=0.06, SoT=0.25,
                              passes_own=52, passes_opp=12, pass_pct=0.92,
                              tackles=1.5, intercepts=2.0, yellow=0.10),
    'Casemiro':          dict(goals=0.08, assists=0.08, SoT=0.35,
                              passes_own=40, passes_opp=18, pass_pct=0.88,
                              tackles=3.5, intercepts=1.8, yellow=0.22),
    'Lucas Paquetá':     dict(goals=0.18, assists=0.22, SoT=0.90, shots_off=0.60,
                              dribbles=2.2, bcc=0.5, yellow=0.16),
    'Neymar':            dict(goals=0.35, assists=0.30, SoT=1.40, shots_off=0.90,
                              dribbles=3.8, bcc=0.7, yellow=0.22, pen_won=0.10),
    'Endrick':           dict(goals=0.52, assists=0.14, SoT=1.90, shots_off=1.00,
                              dribbles=2.0, yellow=0.10),
    'Gabriel Martinelli': dict(goals=0.28, assists=0.18, SoT=1.30, shots_off=0.90,
                              dribbles=2.8, yellow=0.12, pen_won=0.07, miscont=1.70),
    # Croatia
    'Dominik Livaković': dict(saves_pen=0.13),
    'Luka Modrić':       dict(goals=0.08, assists=0.20, SoT=0.55,
                              passes_own=35, passes_opp=35, pass_pct=0.90,
                              tackles=1.5, intercepts=1.2, bcc=0.6, yellow=0.12),
    'Andrej Kramarić':   dict(goals=0.55, assists=0.18, SoT=1.80, shots_off=1.20,
                              bcm=0.40, yellow=0.12),
    'Ivan Perišić':      dict(goals=0.22, assists=0.28, SoT=1.20, shots_off=0.80,
                              dribbles=2.2, yellow=0.10, pen_won=0.06),
    'Mario Pašalić':     dict(goals=0.22, assists=0.16, SoT=1.00, shots_off=0.60,
                              bcc=0.5, yellow=0.12),
    'Mateo Kovačić':     dict(goals=0.10, assists=0.14, SoT=0.60,
                              passes_own=32, passes_opp=30, pass_pct=0.90,
                              tackles=2.2, intercepts=1.5, yellow=0.12),
    'Nikola Vlašić':     dict(goals=0.18, assists=0.14, SoT=0.90, shots_off=0.50,
                              yellow=0.10),
    # Senegal
    'Sadio Mané':        dict(goals=0.35, assists=0.22, SoT=1.50, shots_off=0.80,
                              dribbles=2.8, yellow=0.12, pen_won=0.08),
    'Nicolas Jackson':   dict(goals=0.35, assists=0.12, SoT=1.50, shots_off=0.90,
                              bcm=0.30, yellow=0.16),
    'Pape Matar Sarr':   dict(goals=0.10, assists=0.18, SoT=0.70,
                              passes_own=25, passes_opp=28, pass_pct=0.87,
                              tackles=2.5, intercepts=1.8, yellow=0.12),
    'Lamine Camara':     dict(goals=0.15, assists=0.20, SoT=0.80,
                              passes_own=18, passes_opp=25, pass_pct=0.85,
                              dribbles=2.0, bcc=0.5, yellow=0.12),
    'Kalidou Koulibaly': dict(goals=0.06, assists=0.06, SoT=0.25,
                              passes_own=50, passes_opp=12, pass_pct=0.91,
                              tackles=1.5, intercepts=2.2, yellow=0.14),
    # Japan
    'Takefusa Kubo':     dict(goals=0.20, assists=0.25, SoT=1.20, shots_off=0.80,
                              dribbles=3.5, bcc=0.8, yellow=0.10, pen_won=0.07),
    'Wataru Endo':       dict(goals=0.08, assists=0.10, SoT=0.35,
                              passes_own=38, passes_opp=20, pass_pct=0.90,
                              tackles=4.0, intercepts=2.5, yellow=0.16),
    'Ayase Ueda':        dict(goals=0.50, assists=0.12, SoT=1.60, shots_off=0.90,
                              bcm=0.35, yellow=0.10),
    'Ritsu Doan':        dict(goals=0.18, assists=0.18, SoT=1.00, shots_off=0.60,
                              dribbles=2.5, yellow=0.10, pen_won=0.06),
    # Switzerland
    'Granit Xhaka':      dict(goals=0.10, assists=0.20, SoT=0.65,
                              passes_own=42, passes_opp=28, pass_pct=0.90,
                              tackles=2.5, intercepts=1.8, yellow=0.20),
    'Manuel Akanji':     dict(goals=0.05, assists=0.08, SoT=0.25,
                              passes_own=52, passes_opp=12, pass_pct=0.92,
                              tackles=1.5, intercepts=2.2, yellow=0.10),
    'Dan Ndoye':         dict(goals=0.18, assists=0.20, SoT=1.10, shots_off=0.70,
                              dribbles=3.0, yellow=0.12, pen_won=0.06),
    'Breel Embolo':      dict(goals=0.45, assists=0.18, SoT=1.60, shots_off=1.00,
                              bcm=0.30, yellow=0.14),
    'Ardon Jashari':     dict(goals=0.08, assists=0.16, SoT=0.50,
                              passes_own=32, passes_opp=28, pass_pct=0.88,
                              tackles=2.2, intercepts=1.5, yellow=0.14),
    # South Korea
    'Son Heung-min':     dict(goals=0.40, assists=0.25, SoT=1.50, shots_off=1.00,
                              dribbles=2.5, yellow=0.06, pen_won=0.08),
    'Kim Min-jae':       dict(goals=0.06, assists=0.05, SoT=0.22,
                              passes_own=50, passes_opp=12, pass_pct=0.91,
                              tackles=1.8, intercepts=2.2, yellow=0.16),
    'Lee Kang-in':       dict(goals=0.18, assists=0.28, SoT=1.00, shots_off=0.60,
                              passes_own=20, passes_opp=28, pass_pct=0.87,
                              dribbles=2.5, bcc=0.7, yellow=0.14),
    # Austria
    'Marcel Sabitzer':   dict(goals=0.15, assists=0.18, SoT=0.80,
                              passes_own=30, passes_opp=28, pass_pct=0.88,
                              tackles=2.0, intercepts=1.5, yellow=0.14),
    'David Alaba':       dict(goals=0.06, assists=0.10, SoT=0.30,
                              passes_own=48, passes_opp=12, pass_pct=0.92,
                              tackles=1.5, intercepts=2.0, yellow=0.08),
    'Marko Arnautovic':  dict(goals=0.40, assists=0.14, SoT=1.40, shots_off=1.00,
                              bcm=0.35, yellow=0.20),
    'Christoph Baumgartner': dict(goals=0.18, assists=0.22, SoT=0.90, shots_off=0.50,
                              passes_own=20, passes_opp=25, pass_pct=0.87,
                              yellow=0.10),
    # Norway
    'Fredrik Aursnes':      dict(goals=0.08, assists=0.10, SoT=0.35,
                              passes_own=35, passes_opp=22, pass_pct=0.88,
                              tackles=3.5, intercepts=2.5, yellow=0.14),
    'Alexander Sørloth':    dict(goals=0.45, assists=0.12, SoT=1.50, shots_off=0.90,
                              bcm=0.40, yellow=0.18),
    'Jørgen Strand Larsen': dict(goals=0.38, assists=0.14, SoT=1.40, shots_off=0.90,
                              bcm=0.30, yellow=0.14),
    'Oscar Bobb':           dict(goals=0.14, assists=0.20, SoT=0.80,
                              dribbles=2.5, bcc=0.6, yellow=0.10, pen_won=0.05),
    'Antonio Nusa':         dict(goals=0.14, assists=0.18, SoT=0.85, shots_off=0.60,
                              dribbles=3.0, bcc=0.7, yellow=0.10),
    # Scotland
    'Andrew Robertson':     dict(goals=0.04, assists=0.14, SoT=0.22,
                              passes_own=38, passes_opp=18, pass_pct=0.87,
                              tackles=1.5, intercepts=1.5, yellow=0.10),
    'John McGinn':          dict(goals=0.16, assists=0.14, SoT=0.80,
                              passes_own=22, passes_opp=25, pass_pct=0.85,
                              tackles=2.5, intercepts=1.5, bcc=0.5, yellow=0.18),
    'Billy Gilmour':        dict(goals=0.06, assists=0.12, SoT=0.35,
                              passes_own=35, passes_opp=22, pass_pct=0.91,
                              tackles=2.8, intercepts=2.2, yellow=0.12),
    'Che Adams':            dict(goals=0.45, assists=0.14, SoT=1.50, shots_off=0.90,
                              bcm=0.30, yellow=0.14),
    'Ryan Christie':        dict(goals=0.12, assists=0.18, SoT=0.70,
                              dribbles=2.0, bcc=0.5, yellow=0.12, pen_won=0.05),
    # Sweden
    'Viktor Lindelöf':      dict(goals=0.04, assists=0.06, SoT=0.20,
                              passes_own=52, passes_opp=12, pass_pct=0.90,
                              tackles=1.5, intercepts=2.2, yellow=0.10),
    'Lucas Bergvall':       dict(goals=0.10, assists=0.18, SoT=0.55,
                              passes_own=28, passes_opp=25, pass_pct=0.88,
                              dribbles=2.0, bcc=0.5, yellow=0.10),
    'Anthony Elanga':       dict(goals=0.20, assists=0.18, SoT=1.10, shots_off=0.70,
                              dribbles=3.0, bcc=0.5, yellow=0.10, pen_won=0.05),
    'Mattias Svanberg':     dict(goals=0.10, assists=0.14, SoT=0.55,
                              passes_own=30, passes_opp=22, pass_pct=0.89,
                              tackles=2.0, intercepts=1.5, yellow=0.14),
    'Isak Hien':            dict(goals=0.05, assists=0.06, SoT=0.22,
                              passes_own=48, passes_opp=12, pass_pct=0.90,
                              tackles=1.8, intercepts=2.2, yellow=0.14),
    # Ivory Coast
    'Odilon Kossounou':     dict(goals=0.05, assists=0.06, SoT=0.22,
                              passes_own=48, passes_opp=12, pass_pct=0.90,
                              tackles=1.8, intercepts=2.2, yellow=0.14),
    'Wilfried Singo':       dict(goals=0.06, assists=0.14, SoT=0.35,
                              passes_own=30, passes_opp=20, pass_pct=0.86,
                              dribbles=1.8, yellow=0.12),
    'Ibrahim Sangaré':      dict(goals=0.08, assists=0.10, SoT=0.40,
                              passes_own=30, passes_opp=20, pass_pct=0.87,
                              tackles=3.5, intercepts=2.8, yellow=0.18),
    'Seko Fofana':          dict(goals=0.12, assists=0.16, SoT=0.65,
                              passes_own=28, passes_opp=25, pass_pct=0.87,
                              tackles=2.0, intercepts=1.8, bcc=0.5, yellow=0.16),
    'Simon Adingra':        dict(goals=0.22, assists=0.22, SoT=1.10, shots_off=0.70,
                              dribbles=3.2, bcc=0.6, yellow=0.10, pen_won=0.06),
    'Evann Guessand':       dict(goals=0.35, assists=0.14, SoT=1.30, shots_off=0.90,
                              bcm=0.30, yellow=0.14),
    # DR Congo
    'Yoane Wissa':          dict(goals=0.38, assists=0.18, SoT=1.50, shots_off=0.90,
                              dribbles=2.5, bcc=0.4, yellow=0.12),
    'Gaël Kakuta':          dict(goals=0.14, assists=0.20, SoT=0.75,
                              passes_own=18, passes_opp=22, pass_pct=0.85,
                              dribbles=2.5, bcc=0.6, yellow=0.14),
    'Aaron Wan-Bissaka':    dict(goals=0.02, assists=0.08, SoT=0.10,
                              passes_own=25, passes_opp=18, pass_pct=0.84,
                              tackles=2.5, intercepts=1.8, dribbles=1.5, yellow=0.12),
    'Cédric Bakambu':       dict(goals=0.35, assists=0.12, SoT=1.30, shots_off=0.90,
                              bcm=0.30, yellow=0.16),
    'Simon Banza':          dict(goals=0.42, assists=0.12, SoT=1.50, shots_off=0.90,
                              bcm=0.35, yellow=0.14),
    # Turkey (extra — Güler, Çalhanoğlu, Yıldız already above)
    'Zeki Çelik':           dict(goals=0.03, assists=0.10, SoT=0.15,
                              passes_own=25, passes_opp=18, pass_pct=0.83,
                              tackles=1.5, intercepts=1.0, dribbles=1.5, yellow=0.14),
    'Ferdi Kadıoğlu':       dict(goals=0.04, assists=0.15, SoT=0.20,
                              passes_own=28, passes_opp=20, pass_pct=0.84,
                              tackles=1.8, intercepts=1.2, dribbles=2.0, yellow=0.12),
    'Merih Demiral':        dict(goals=0.08, assists=0.05, SoT=0.30,
                              passes_own=40, passes_opp=15, pass_pct=0.87,
                              tackles=1.5, intercepts=1.2, yellow=0.18),
    'Kerem Aktürkoğlu':     dict(goals=0.30, assists=0.25, SoT=1.40, shots_off=1.00,
                              dribbles=3.0, bcc=0.7, yellow=0.14),
    'Barış Alper Yılmaz':   dict(goals=0.22, assists=0.20, SoT=1.10, shots_off=0.90,
                              dribbles=2.5, bcc=0.5, yellow=0.12),
    'Can Uzun':             dict(goals=0.25, assists=0.18, SoT=1.20, shots_off=1.00,
                              yellow=0.10),
    # Ecuador (Caicedo already above)
    'Willian Pacho':        dict(goals=0.06, assists=0.04, SoT=0.25,
                              passes_own=55, passes_opp=20, pass_pct=0.92,
                              tackles=1.5, intercepts=1.0, yellow=0.18),
    'Piero Hincapié':       dict(goals=0.05, assists=0.06, SoT=0.20,
                              passes_own=52, passes_opp=18, pass_pct=0.90,
                              tackles=1.8, intercepts=1.2, dribbles=1.0, yellow=0.14),
    'Kendry Páez':          dict(goals=0.12, assists=0.25, SoT=0.90,
                              passes_own=22, passes_opp=30, pass_pct=0.87,
                              bcc=0.60, dribbles=2.5, yellow=0.10),
    'Enner Valencia':       dict(goals=0.32, assists=0.12, SoT=1.40, shots_off=1.00,
                              bcm=0.25, yellow=0.14),
    'Gonzalo Plata':        dict(goals=0.22, assists=0.20, SoT=1.10, shots_off=0.90,
                              dribbles=3.0, bcc=0.6, yellow=0.12),
    'Nilson Angulo':        dict(goals=0.18, assists=0.22, SoT=1.00, shots_off=0.80,
                              dribbles=2.5, bcc=0.5, yellow=0.10),
    # Canada (Jonathan David already above)
    'Alphonso Davies':      dict(goals=0.08, assists=0.18, SoT=0.30,
                              passes_own=30, passes_opp=22, pass_pct=0.86,
                              tackles=1.8, intercepts=1.2, dribbles=3.0, bcc=0.8, yellow=0.18),
    'Tajon Buchanan':       dict(goals=0.22, assists=0.18, SoT=1.10, shots_off=0.80,
                              dribbles=3.0, bcc=0.6, yellow=0.12),
    'Stephen Eustáquio':    dict(goals=0.08, assists=0.12, SoT=0.35,
                              passes_own=32, passes_opp=22, pass_pct=0.87,
                              tackles=2.5, intercepts=1.8, recoveries=4.0, yellow=0.22),
    'Cyle Larin':           dict(goals=0.38, assists=0.10, SoT=1.50, shots_off=1.20,
                              bcm=0.30, yellow=0.20),
    'Ismaël Koné':          dict(goals=0.08, assists=0.10, SoT=0.40,
                              passes_own=28, passes_opp=22, pass_pct=0.87,
                              tackles=2.0, intercepts=1.5, yellow=0.18),
    # Australia
    'Jackson Irvine':       dict(goals=0.12, assists=0.14, SoT=0.50,
                              passes_own=25, passes_opp=20, pass_pct=0.85,
                              tackles=2.5, intercepts=1.5, yellow=0.18),
    'Ajdin Hrustic':        dict(goals=0.08, assists=0.18, SoT=0.50,
                              passes_own=22, passes_opp=28, pass_pct=0.86,
                              bcc=0.50, key2=0.25, yellow=0.12),
    'Nestory Irankunda':    dict(goals=0.18, assists=0.22, SoT=0.90, shots_off=0.70,
                              dribbles=3.5, bcc=0.6, yellow=0.10),
    'Martin Boyle':         dict(goals=0.20, assists=0.18, SoT=1.00, shots_off=0.70,
                              dribbles=3.0, bcc=0.5, yellow=0.12),
    'Harry Souttar':        dict(goals=0.06, assists=0.04, SoT=0.30,
                              passes_own=42, passes_opp=12, pass_pct=0.88,
                              tackles=1.2, intercepts=0.8, yellow=0.14),
    'Mohamed Toure':        dict(goals=0.28, assists=0.12, SoT=1.30, shots_off=1.00,
                              bcm=0.30, yellow=0.18),
    # Iran
    'Mehdi Taremi':         dict(goals=0.50, assists=0.20, SoT=1.80, shots_off=1.20,
                              bcm=0.35, yellow=0.16, pen_won=0.08),
    'Saeid Ezatolahi':      dict(goals=0.05, assists=0.06, SoT=0.20,
                              passes_own=32, passes_opp=22, pass_pct=0.85,
                              tackles=3.0, intercepts=2.0, yellow=0.20),
    'Alireza Jahanbakhsh':  dict(goals=0.16, assists=0.22, SoT=0.90, shots_off=0.70,
                              dribbles=2.0, bcc=0.5, yellow=0.12),
    'Saman Ghoddos':        dict(goals=0.12, assists=0.18, SoT=0.70,
                              passes_own=18, passes_opp=22, pass_pct=0.85,
                              dribbles=1.5, bcc=0.4, yellow=0.10),
    # Panama
    'Aníbal Godoy':         dict(goals=0.04, assists=0.06, SoT=0.15,
                              passes_own=35, passes_opp=18, pass_pct=0.84,
                              tackles=3.5, intercepts=2.0, yellow=0.22),
    'Adalberto Carrasquilla': dict(goals=0.10, assists=0.18, SoT=0.50,
                              passes_own=20, passes_opp=25, pass_pct=0.85,
                              bcc=0.40, yellow=0.16),
    'Michael Murillo':      dict(goals=0.03, assists=0.10, SoT=0.15,
                              passes_own=22, passes_opp=18, pass_pct=0.82,
                              tackles=2.0, intercepts=1.2, dribbles=1.5, yellow=0.16),
    'Ismael Díaz':          dict(goals=0.28, assists=0.14, SoT=1.30, shots_off=0.90,
                              bcm=0.25, dribbles=1.5, yellow=0.14),
    'Cecilio Waterman':     dict(goals=0.22, assists=0.14, SoT=1.10, shots_off=0.80,
                              dribbles=2.0, bcc=0.4, yellow=0.16),
    'José Fajardo':         dict(goals=0.30, assists=0.10, SoT=1.30, shots_off=1.00,
                              bcm=0.25, yellow=0.14),
    # Argentina
    'Lionel Messi':          dict(goals=1.10, assists=0.45, SoT=2.20, shots_off=1.50,
                              bcc=1.50, dribbles=4.5, yellow=0.06, pen_won=0.20, miscont=2.20),
    'Lautaro Martínez':      dict(goals=0.72, assists=0.22, SoT=2.10, shots_off=1.50,
                              bcm=0.45, yellow=0.12),
    'Alexis Mac Allister':   dict(goals=0.10, assists=0.18, SoT=0.60,
                              passes_own=32, passes_opp=28, pass_pct=0.88,
                              tackles=2.0, intercepts=1.5, yellow=0.14),
    'Rodrigo De Paul':       dict(goals=0.10, assists=0.18, SoT=0.55,
                              passes_own=28, passes_opp=25, pass_pct=0.85,
                              tackles=2.5, intercepts=1.5, yellow=0.22),
    'Enzo Fernández':        dict(goals=0.09, assists=0.14, SoT=0.50,
                              passes_own=30, passes_opp=25, pass_pct=0.88,
                              tackles=2.5, intercepts=1.8, yellow=0.18),
    # Spain
    'Rodri':                 dict(goals=0.08, assists=0.12, SoT=0.45,
                              passes_own=55, passes_opp=25, pass_pct=0.925,
                              tackles=2.5, intercepts=1.8, recoveries=5.5, yellow=0.08),
    'Nico Williams':         dict(goals=0.35, assists=0.30, SoT=1.60, shots_off=1.00,
                              dribbles=4.5, bcc=0.80, yellow=0.10, pen_won=0.15, miscont=2.00),
    'Mikel Oyarzabal':       dict(goals=0.50, assists=0.20, SoT=1.80, shots_off=1.20,
                              bcm=0.30, yellow=0.08),
    'Fabián Ruiz':           dict(goals=0.14, assists=0.24, SoT=0.80,
                              passes_own=30, passes_opp=28, pass_pct=0.88,
                              bcc=0.55, yellow=0.10),
    'Martín Zubimendi':      dict(goals=0.06, assists=0.08, SoT=0.30,
                              passes_own=45, passes_opp=22, pass_pct=0.92,
                              tackles=2.8, intercepts=2.0, yellow=0.10),
    'Mikel Merino':          dict(goals=0.14, assists=0.16, SoT=0.70,
                              passes_own=28, passes_opp=20, pass_pct=0.87,
                              tackles=2.5, intercepts=1.5, yellow=0.14),
    # Morocco
    'Ayoub El Kaabi':        dict(goals=0.52, assists=0.14, SoT=1.80, shots_off=1.20,
                              bcm=0.35, yellow=0.12),
    'Brahim Díaz':           dict(goals=0.20, assists=0.28, SoT=1.00, shots_off=0.70,
                              dribbles=3.5, bcc=0.70, yellow=0.10),
    'Sofyan Amrabat':        dict(goals=0.04, assists=0.08, SoT=0.20,
                              passes_own=38, passes_opp=22, pass_pct=0.88,
                              tackles=4.5, intercepts=2.5, recoveries=6.0, yellow=0.30),
    'Azzedine Ounahi':       dict(goals=0.08, assists=0.14, SoT=0.45,
                              passes_own=30, passes_opp=25, pass_pct=0.87,
                              tackles=2.0, intercepts=1.5, dribbles=1.5, yellow=0.16),
    'Abdessamad Ezzalzouli': dict(goals=0.18, assists=0.22, SoT=1.00, shots_off=0.80,
                              dribbles=3.0, bcc=0.60, yellow=0.12),
    # Netherlands
    'Virgil van Dijk':       dict(goals=0.08, assists=0.06, SoT=0.30,
                              passes_own=52, passes_opp=12, pass_pct=0.92,
                              tackles=1.5, intercepts=2.0, yellow=0.10),
    'Tijjani Reijnders':     dict(goals=0.22, assists=0.26, SoT=1.10, shots_off=0.70,
                              passes_own=28, passes_opp=30, pass_pct=0.87,
                              bcc=0.70, yellow=0.12),
    'Cody Gakpo':            dict(goals=0.52, assists=0.22, SoT=1.85, shots_off=1.20,
                              dribbles=2.5, bcc=0.50, yellow=0.12),
    'Memphis Depay':         dict(goals=0.50, assists=0.20, SoT=1.70, shots_off=1.20,
                              bcm=0.35, dribbles=2.5, yellow=0.14),
    'Denzel Dumfries':       dict(goals=0.06, assists=0.14, SoT=0.30,
                              passes_own=22, passes_opp=20, pass_pct=0.83,
                              tackles=2.0, intercepts=1.2, dribbles=1.8, yellow=0.18),
    # Colombia
    'James Rodríguez':       dict(goals=0.18, assists=0.42, SoT=0.80, shots_off=0.60,
                              bcc=1.00, key2=0.50, passes_own=20, passes_opp=30, pass_pct=0.87,
                              yellow=0.10),
    'Richard Ríos':          dict(goals=0.10, assists=0.16, SoT=0.50,
                              passes_own=30, passes_opp=25, pass_pct=0.88,
                              tackles=3.0, intercepts=2.0, yellow=0.22),
    'Cucho Hernández':       dict(goals=0.45, assists=0.18, SoT=1.60, shots_off=1.00,
                              dribbles=2.5, bcm=0.30, yellow=0.14),
    # USA
    'Tyler Adams':           dict(goals=0.04, assists=0.08, SoT=0.20,
                              passes_own=38, passes_opp=20, pass_pct=0.88,
                              tackles=4.5, intercepts=2.5, recoveries=5.5, yellow=0.30),
    'Malik Tillman':         dict(goals=0.20, assists=0.26, SoT=1.00, shots_off=0.70,
                              bcc=0.60, dribbles=2.0, yellow=0.12),
    'Folarin Balogun':       dict(goals=0.45, assists=0.14, SoT=1.60, shots_off=0.90,
                              bcm=0.30, yellow=0.10),
    'Tim Weah':              dict(goals=0.18, assists=0.16, SoT=0.90, shots_off=0.70,
                              dribbles=2.5, bcc=0.40, yellow=0.14),
}

WINGERS = {
    'Kylian Mbappé', 'Lamine Yamal', 'Mohamed Salah', 'Vinícius Júnior',
    'Bukayo Saka', 'Amad Diallo', 'Kenan Yıldız', 'Mohammed Kudus',
    'Christian Pulisic', 'Ousmane Dembélé', 'Luis Díaz', 'Raphinha',
    'Jérémy Doku', 'Pedro Neto', 'Rafael Leão', 'Marcus Rashford',
    'Karim Adeyemi', 'Serge Gnabry', 'Nick Woltemade', 'Antony',
    'Mason Greenwood', 'Hugo Ekitiké', 'Désiré Doué',
    'Anthony Gordon', 'Noni Madueke',
    'Bradley Barcola', 'Michael Olise', 'Rayan Cherki', 'Maghnes Akliouche',
    'Francisco Conceição', 'Francisco Trincão', 'João Félix',
    'Jamal Musiala', 'Leroy Sané', 'Jamie Leweling',
    'Leandro Trossard', 'Charles De Ketelaere', 'Alexis Saelemaekers', 'Dodi Lukebakio',
    'Neymar', 'Gabriel Martinelli',
    'Ivan Perišić',
    # Senegal
    'Sadio Mané', 'Ismaïla Sarr', 'Iliman Ndiaye',
    # Japan
    'Ritsu Doan', 'Junya Ito',
    # Switzerland
    'Dan Ndoye', 'Ruben Vargas', 'Noah Okafor',
    # South Korea
    'Son Heung-min', 'Hwang Hee-chan', 'Yang Hyun-jun',
    # Norway
    'Antonio Nusa', 'Oscar Bobb',
    # Scotland
    'Ryan Christie', 'Ben Doak',
    # Sweden
    'Anthony Elanga', 'Ken Sema',
    # Ivory Coast
    'Simon Adingra', 'Nicolas Pépé', 'Dango Ouattara',
    # DR Congo
    'Yoane Wissa', 'Nathanaël Mbuku', 'Théo Bongonda',
    # Turkey
    'Kerem Aktürkoğlu', 'Barış Alper Yılmaz', 'Yunus Akgün', 'İrfan Can Kahveci',
    # Ecuador
    'Gonzalo Plata', 'Nilson Angulo',
    # Canada
    'Tajon Buchanan', 'Liam Millar', 'Tani Oluwaseyi', 'Promise David',
    # Australia
    'Martin Boyle', 'Nestory Irankunda', 'Mathew Leckie', 'Brandon Borrello', 'Nishan Velupillay',
    # Iran
    'Amirhossein Hosseinzadeh',
    # Panama
    'Cecilio Waterman', 'Tomás Rodríguez',
    # Argentina
    'Lionel Messi', 'Nicolás González', 'Giuliano Simeone', 'Nico Paz',
    # Spain
    'Nico Williams', 'Ferran Torres', 'Yeremy Pino',
    # Morocco
    'Brahim Díaz', 'Abdessamad Ezzalzouli', 'Soufiane Rahimi',
    'Ilias Talbi', 'Bilal Amaimouni', 'Nassim Gessime',
    # Netherlands
    'Cody Gakpo', 'Donyell Malen', 'Crysencio Summerville',
    'Noa Lang', 'Memphis Depay', 'Patrick Kluivert',
    # Colombia
    'Daniel Campaz', 'Yaser Asprilla', 'Brayan Rodríguez',
    # USA
    'Tim Weah', 'Brenden Aaronson', 'Alan Zendejas', 'Caden Clark',
}

# Scoring matrix point values (per event, per 90 min)
# Positional totals (base + additional) for key asymmetric actions:
BCM_PTS   = {'GK': -10, 'DEF': -13, 'MID': -10, 'FWD': -15}
SOT_OFF   = {'GK':   0, 'DEF':  -1, 'MID':   0, 'FWD':  -3}
DRIB_PTS  = {'GK':   0, 'DEF':   1, 'MID':   2, 'FWD':   3}
DISP_PTS  = {'GK':  -5, 'DEF':  -5, 'MID':  -3, 'FWD':  -1}
MCTR_PTS  = {'GK':  -5, 'DEF':  -5, 'MID':  -3, 'FWD':  -1}
DL_PTS    = {'GK':  -3, 'DEF':  -3, 'MID':  -2, 'FWD':  -1}
OFF_PTS   = {'GK':   0, 'DEF':   0, 'MID':  -3, 'FWD':  -3}
ELG_PTS   = {'GK': -20, 'DEF': -20, 'MID': -10, 'FWD': -10}
ELS_PTS   = {'GK': -10, 'DEF': -10, 'MID':  -5, 'FWD':  -5}


def get_archetype(row):
    pos, sub, tier, name = row['position'], row['sub_position'], row['tier'], row['player']
    if pos == 'GK':
        return tier          # GK1, GK2, GK3
    if pos == 'DEF':
        return 'FB' if sub in ('LB', 'RB', 'RWB', 'FB') else 'CB'
    if pos == 'MID':
        return sub if sub in ('DM', 'CM', 'AM') else 'AM'   # RW/LW → AM
    # FWD (sub_position is empty for all forwards)
    return 'WNG' if name in WINGERS else 'CF'


def pos_cat(archetype):
    if archetype in ('GK1', 'GK2', 'GK3'):
        return 'GK'
    if archetype in ('CB', 'FB'):
        return 'DEF'
    if archetype in ('DM', 'CM'):
        return 'MID'
    return 'FWD'   # AM, CF, WNG


def get_stats(row, archetype):
    """Return WC-calibrated per-90 stats (baseline + overrides × WC factors)."""
    stats = dict(BASELINE[archetype])
    name = row['player']
    if name in OVR:
        stats.update(OVR[name])
    for k in list(stats.keys()):
        if k in WC:
            stats[k] *= WC[k]
    return stats


def action_pts_90(stats, archetype):
    """Action points per 90 min from per-90 event rates."""
    pc = pos_cat(archetype)
    p = 0.0

    p += 50   * stats.get('goals', 0)
    sot = stats.get('SoT', 0)
    p += 10   * sot                          # shots on target
    p += 3    * 0.6 * sot                    # shots blocked by opponent (~60% of SoT)
    p += BCM_PTS[pc] * stats.get('bcm', 0)
    p += SOT_OFF[pc] * stats.get('shots_off', 0)
    p += 30   * stats.get('assists', 0)
    p += 10   * stats.get('key2', 0)         # assists the assister
    p += 10   * stats.get('bcc', 0)          # big chances created
    p += 0.25 * stats.get('passes_own', 0) * stats.get('pass_pct', 0)
    p += 0.75 * stats.get('passes_opp', 0) * stats.get('pass_pct', 0)
    p += DISP_PTS[pc] * stats.get('disposs', 0)
    p += MCTR_PTS[pc] * stats.get('miscont', 0)
    p += DRIB_PTS[pc] * stats.get('dribbles', 0)
    p += 2    * stats.get('fouls_won', 0)
    p += 10   * stats.get('pen_won', 0)
    p += OFF_PTS[pc]  * stats.get('offsides', 0)
    p += 3    * stats.get('duels_won', 0)
    p += DL_PTS[pc]   * stats.get('duels_lost', 0)
    p += 5    * stats.get('blocks', 0)
    p += 8    * stats.get('blocks_6yd', 0)
    p += 3    * stats.get('tackles', 0)
    p += 10   * stats.get('last_tack', 0)
    p += 2    * stats.get('recoveries', 0)
    p += 1    * stats.get('clear', 0)
    p += 1    * stats.get('head_clear', 0)
    p += 2    * stats.get('crosses_blocked', 0)
    p += 20   * stats.get('clearance_line', 0)
    p += 3    * stats.get('intercepts', 0)
    p += 2    * stats.get('intercepts_box', 0)   # extra +2 on top of base +3 for box interceptions
    p += -10  * stats.get('yellow', 0)
    p += -20  * stats.get('red', 0)
    p += -3   * stats.get('fouls_comm', 0)
    p += -20  * stats.get('own_goals', 0)
    p += -20  * stats.get('pen_giveaway', 0)
    p += ELG_PTS[pc]  * stats.get('err_goal', 0)
    p += ELS_PTS[pc]  * stats.get('err_shot', 0)

    if pc == 'GK':
        p += 5  * stats.get('saves_ib', 0)
        p += 3  * stats.get('saves_ob', 0)
        p += 30 * stats.get('saves_pen', 0)
        p += 1  * stats.get('pickups', 0)
        p += 3  * stats.get('catches', 0)
        p += 3  * stats.get('punches', 0)
        p += 3  * stats.get('sweeper', 0)
        p += -5 * stats.get('six_sec', 0)
        p += -5 * stats.get('cross_nc', 0)

    return p


def compute_player_pts(row):
    """Returns (action_pts_per_90, exp_pts_per_90, total_exp_fantasy_pts)."""
    archetype = get_archetype(row)
    pc        = pos_cat(archetype)
    tier      = row['tier']
    nation    = row['nationality']

    gmins   = float(row['group_mins_per_game'])
    ko_mins = float(row['exp_post_group_mins_total'])

    total_mins = gmins * 3 + ko_mins
    if total_mins == 0:
        return 0.0, 0.0, 0.0

    stats   = get_stats(row, archetype)
    a90     = action_pts_90(stats, archetype)

    if nation not in TEAM:
        total = round(a90 * total_mins / 90, 1)
        return round(a90, 1), round(a90, 1), total

    g_wd, g_cs_pct, g_gc, ko_win, ko_cs_pct, ko_gc = TEAM[nation]

    is_starter = gmins >= 45
    wd_factor  = 1.0 if is_starter else 0.5
    cs_factor  = 1.0 if is_starter else 0.0
    app_pts    = 10.0 if is_starter else 5.0
    gc_frac_g  = gmins / 90          # fraction of group game played

    # Expected group-stage appearances (how many of 3 games does player appear)
    if tier in ('GK1', 'GK2', 'GK3'):
        g_apps = min(3.0, gmins * 3 / 90)
    elif tier in ('1', '2', '3'):
        g_apps = 3.0
    elif tier == '4':
        g_apps = 2.0
    else:   # tier 5
        g_apps = 1.0

    g_bonus_per_app = (
        app_pts
        + wd_factor  * g_wd
        + cs_factor  * g_cs_pct   * CS_BONUS[pc]
        - gc_frac_g  * g_gc       * GC_PEN[pc]
    )
    total_g_bonus = g_apps * g_bonus_per_app

    # Expected KO appearances
    mins_per_ko = {'GK1': 90, 'GK2': 90, 'GK3': 90,
                   '1': 90, '2': 80, '3': 25, '4': 10, '5': 5}
    mpg = mins_per_ko.get(tier, 90)
    ko_apps = ko_mins / mpg if mpg > 0 else 0.0
    gc_frac_ko = mpg / 90

    ko_bonus_per_app = (
        app_pts
        + wd_factor  * ko_win   * 30   # no draws in KO
        + cs_factor  * ko_cs_pct * CS_BONUS[pc]
        - gc_frac_ko * ko_gc    * GC_PEN[pc]
    )
    total_ko_bonus = ko_apps * ko_bonus_per_app

    total_action  = a90 * total_mins / 90
    total_pts     = total_action + total_g_bonus + total_ko_bonus
    exp_pts_per90 = total_pts / (total_mins / 90)

    return round(a90, 1), round(exp_pts_per90, 1), round(total_pts, 1)


def main():
    path = '/tmp/wc_repo/data/master_sheet.csv'

    with open(path, newline='', encoding='utf-8') as f:
        reader    = csv.DictReader(f)
        rows      = list(reader)
        fieldnames = list(reader.fieldnames)

    new_cols = ['action_pts_per_90', 'exp_pts_per_90', 'total_exp_fantasy_pts', 'adj_exp_fantasy_pts']
    out_fields = fieldnames + [c for c in new_cols if c not in fieldnames]

    for row in rows:
        a90, e90, tot = compute_player_pts(row)
        squad_prob = float(row.get('wc_squad_prob_pct', 100)) / 100.0
        row['action_pts_per_90']     = a90
        row['exp_pts_per_90']        = e90
        row['total_exp_fantasy_pts'] = tot
        row['adj_exp_fantasy_pts']   = round(tot * squad_prob, 1)

    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        writer.writerows(rows)

    ranked = sorted(rows, key=lambda r: float(r['adj_exp_fantasy_pts']), reverse=True)
    hdr = f"{'#':<4} {'Player':<28} {'Nat':<13} {'Pos':<4} {'Tier':<5} {'Sq%':>4} {'act/90':>7} {'Raw Pts':>8} {'Adj Pts':>8}"
    print(hdr)
    print('-' * len(hdr))
    for i, r in enumerate(ranked[:35], 1):
        print(f"{i:<4} {r['player']:<28} {r['nationality']:<13} {r['position']:<4} "
              f"{r['tier']:<5} {r['wc_squad_prob_pct']:>3}% {r['action_pts_per_90']:>7} "
              f"{r['total_exp_fantasy_pts']:>8} {r['adj_exp_fantasy_pts']:>8}")

    print(f"\nTotal players processed: {len(rows)}")


if __name__ == '__main__':
    main()
