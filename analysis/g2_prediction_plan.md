# G2 Standout Prediction Plan — World Cup 2026
*Methodology for identifying high-probability fantasy scoring picks in Group Stage Round 2*

---

## Inputs

All data sourced from `price_value_table.txt` (post-G1 update) and `g1_report.md`:

| Column | Use |
|--------|-----|
| `G2 Win%` | Proxy for team strength vs G2 opponent → drives CS and attack expectation |
| `Starter` | G1-actual starting status → appearance probability |
| `Fitness` | Current physical status entering G2 |
| `G1 Pts` | Actual G1 output |
| `Δ` | Over/underperformance vs expectation → form signal |
| `Adj Pts` | Pre-tournament model expectation → player quality baseline |
| `Pos` | Determines CS eligibility and attack rate |

---

## G2 Outlook Score Formula

```
G2_OUTLOOK = APP_EXP + CS_EXP + ATTACK_EXP + FORM_ADJ
```

### 1. APP_EXP — Appearance expectation

Based on updated G1-actual Starter status (accounts for ~7% rotation/injury buffer on "yes"):

| Starter | P(plays) | APP_EXP |
|---------|----------|---------|
| yes     | 0.93     | 1.85    |
| sometimes | 0.50   | 0.90    |
| no      | 0.10     | 0.15    |

Fitness modifier: if `fitness = not`, multiply P(plays) by 0.15 (near-zero). If `mostly`, no change (already reflected in Starter status).

### 2. CS_EXP — Clean sheet expectation

```
CS_EXP = P(plays) × P(CS | G2 Win%) × CS_pts
```

**CS points by position:**
| Pos | CS_pts |
|-----|--------|
| GK  | 6      |
| DEF | 4      |
| MID | 1      |
| FWD | 0      |

**P(CS) calibration from G2 Win%:**

| G2 Win% | P(CS) | Rationale |
|---------|-------|-----------|
| 90%+    | 0.52  | Dominant mismatch (FRA/BRA vs bottom-tier) |
| 80–89%  | 0.45  | Strong favourite, opponent very limited |
| 70–79%  | 0.33  | Clear favourite but opponent can score |
| 60–69%  | 0.24  | Comfortable favourite, CS real but not likely |
| 50–59%  | 0.18  | Slight favourite, CS a bonus not a base |
| 40–49%  | 0.14  | Near-even; CS unlikely |
| 20–39%  | 0.09  | Underdog; CS very unlikely |
| <20%    | 0.04  | Heavy underdog; near-zero CS expectation |

**G2 matchup CS buckets for tracked nations:**

| G2 Win% | Nations (G2 opponent) |
|---------|----------------------|
| 93%     | France (Iraq), Brazil (Haiti) |
| 91%     | Spain (Saudi Arabia) |
| 87%     | Uruguay (Cape Verde) |
| 83%     | Egypt (New Zealand) |
| 81%     | Ecuador (Curaçao) |
| 78%     | Colombia (DR Congo) |
| 75%     | England (Ghana) |
| 71%     | Belgium (Iran) |
| 68%     | Germany (Ivory Coast) |
| 65%     | Morocco (Scotland) |
| 63%     | Argentina (Austria) |
| 62%     | Netherlands (Sweden), Canada (Qatar) |
| 60%     | USA (Australia) |
| 57%     | Croatia (Panama) |
| 48%     | Turkey (Paraguay) |
| 29%     | Norway (Senegal) |
| 23%     | Scotland (Morocco) |
| 21%     | Sweden (Netherlands) |
| 13%     | Ivory Coast (Germany) |

### 3. ATTACK_EXP — Expected offensive contribution

```
ATTACK_EXP = P(plays) × BASE_ATTACK × (G2 Win% / 0.50)
```

**BASE_ATTACK (pts/game at 50% win prob):**

| Pos | Goals/game | Assists/game | BASE_ATTACK |
|-----|-----------|-------------|-------------|
| FWD | 0.20      | 0.10        | 1.50        |
| MID | 0.08      | 0.15        | 0.93        |
| DEF | 0.04      | 0.05        | 0.39        |
| GK  | 0         | 0           | 0           |

The (G2 Win% / 0.50) multiplier scales attack expectation by opponent quality — a team 93% likely to win is generating ~1.86× the attacking threat of an even contest.

**Note:** High-profile individual attackers (Kane, Mbappé, Haaland, Díaz) with large pre-tournament Adj Pts have a personal quality premium above the positional base. These are flagged separately in the Top Picks section.

### 4. FORM_ADJ — G1 momentum signal

| G1 Δ     | Adjustment | Rationale |
|----------|-----------|-----------|
| ≥ +9     | +1.5      | Exceptional form; likely in scorer/assist groove |
| +6 to +8 | +1.0      | Strong G1; confidence/minutes high |
| +3 to +5 | +0.5      | Delivered above baseline; modest carry-forward |
| 0 to +2  | 0         | On expectation; neutral signal |
| −1       | −0.2      | Benched "sometimes" pick; mild rotation concern |
| −2       | −0.5      | Expected starter who sat out G1; real rotation/fitness risk |

---

## Rotation Risk Flags

These factors increase the chance a player unexpectedly doesn't start G2:

1. **Starter = sometimes** after G1 — already confirmed non-starter once; manager's trust unclear
2. **Dead rubber G2 risk** — teams with near-certain G2 qualification may rest stars (check standings post-G1)
3. **Fitness = mostly** combined with Δ = −2 — missed G1, no confirmed recovery
4. **High-squad-depth nations** (France, Spain, Argentina) — rotation more likely even in meaningful games

---

## Standout Categories

### Category A — CS Bankers (GK/DEF, G2 Win% ≥ 80%)

These players have the highest floor: appearance pts + high CS probability. Best for budget-efficient DEF/GK slots.

Target profile: `fitness = full/mostly` + `starter = yes` + `G2 Win% ≥ 80%` + `Pos = GK or DEF`

Priority nations: **France, Brazil, Spain**

### Category B — Premium Goal Threats (FWD, G1 Δ ≥ +6, G2 Win% ≥ 60%)

Players who demonstrated form in G1 AND face beatable opposition in G2. Highest ceiling picks.

Target profile: `G1 Δ ≥ +6` + `G2 Win% ≥ 60%` + `Pos = FWD` + `starter = yes`

### Category C — Value MID Starters (MID, high Pts/$, starter = yes, G2 Win% ≥ 60%)

Midfielders with top Pts/$ from price_value_table who started G1 and face winnable G2 ties. Best coverage picks (CS+1 bonus if team keeps CS, plus attack upside).

Target profile: `Pts/$ > 50000` + `starter = yes` + `G2 Win% ≥ 60%` + `Pos = MID`

### Category D — Rotation/Avoid List

Players to flag as high-uncertainty despite good model scores:
- Starter = sometimes + Δ = −2 (benched in G1)
- Fitness = not
- "Premium bench" players on nations likely to manage workloads

---

## Top G2 Predicted Standouts

*G2_OUTLOOK scores computed per formula above. Ranked by score.*

| Rank | Player | Nat | Pos | G2 Win% | Starter | G1 Δ | G2_OUTLOOK | Category | Note |
|------|--------|-----|-----|---------|---------|------|-----------|---------|------|
| 1  | Mbappé          | FRA | FWD | 93%  | yes       | +12 | 6.1 | B | Premium goal threat vs Iraq |
| 2  | Simón           | SPA | GK  | 91%  | yes       | +6  | 5.5 | A | GK CS banker + form; Spain structured vs Saudi |
| 3  | Díaz            | COL | FWD | 78%  | yes       | +9  | 5.5 | B | Exceptional G1; COL vs weak DRC |
| 4  | Vinícius Júnior | BRA | FWD | 93%  | yes       | +6  | 5.4 | B | Form + massive BRA attack vs Haiti |
| 5  | Kane            | ENG | FWD | 75%  | yes       | +12 | 5.4 | B | Best in world form; ENG dominant vs Ghana |
| 6  | Cubarsí         | SPA | DEF | 91%  | yes       | +4  | 4.8 | A | Confirmed starter; Spain defence dominant |
| 7  | Cucurella       | SPA | DEF | 91%  | yes       | +4  | 4.8 | A | Confirmed Spain G1 starter; CS candidate |
| 8  | Grimaldo        | SPA | DEF | 91%  | sometimes | +3  | 2.7 | A | Sub 71' in G1 (not starter); lower APP_EXP for G2 |
| 9  | Porro           | SPA | DEF | 91%  | sometimes | −1  | 2.0 | D | Bench DNP in G1; rotation risk for G2 |
| 10 | Maignan         | FRA | GK  | 93%  | yes       | +0  | 4.8 | A | GK CS banker vs Iraq; top floor pick |
| 11 | Alisson Becker  | BRA | GK  | 93%  | yes       | +0  | 4.8 | A | BRA dominant vs Haiti; high CS probability |
| 12 | Schlotterbeck   | GER | DEF | 68%  | yes       | +6  | 4.2 | B/A | Scored G1; DEF with attack upside vs CIV |
| 13 | Nmecha          | GER | MID | 68%  | yes       | +8  | 4.3 | C | Surprise G1 starter who scored; form carry |
| 14 | Rafael Leão     | POR | FWD | 84%  | yes       | +0  | 4.2 | B | Quality FWD vs Uzbekistan; high ceiling |
| 15 | Raphinha        | BRA | FWD | 93%  | yes       | +0  | 4.5 | B | BRA attacking depth vs Haiti; CS upside |
| 16 | Haaland         | NOR | FWD | 29%  | yes       | +12 | 4.2 | B | Low G2 Win% but personal scoring rate overrides |
| 17 | Gabriel Magalhães| BRA | DEF | 93%  | yes      | +0  | 4.5 | A | DEF CS + BRA dominant |
| 18 | Olise           | FRA | MID | 93%  | yes       | +3  | 4.6 | C | MID + CS bonus vs Iraq; France's creative engine |
| 19 | Koundé          | FRA | DEF | 93%  | yes       | +0  | 4.5 | A | Reliable France DEF; high CS probability |
| 20 | Upamecano       | FRA | DEF | 93%  | yes       | +0  | 4.5 | A | Same profile as Koundé |
| 21 | Saliba          | FRA | DEF | 93%  | yes       | +0  | 4.5 | A | Confirmed G1 starter (corrected from bench); France CS banker vs Iraq |

---

## Key G2 Narratives to Watch

1. **Spain's CS wall** — Spain kept a 0-0 in G1. Facing Saudi Arabia (G2 Win% 91%) they are the clearest CS opportunity of the round. **Corrected**: Spain's G1 back four was Llorente/Laporte/Cubarsí/Cucurella — Grimaldo and Porro were both bench. Reliable CS picks: Cubarsí and Cucurella (confirmed G1 starters), Simón (GK CS ceiling). Grimaldo/Porro are "sometimes" starter risk for G2.

2. **France/Brazil vs minnows** — France vs Iraq (93%) and Brazil vs Haiti (93%) are the two highest-probability mismatches. Expect high-scoring games with multiple CS-eligible players delivering. Risk: France may rotate for G3 rest.

3. **Mbappé & Kane form carry** — Both scored braces in G1. Facing weaker G2 opponents (Iraq and Ghana), the probability of repeat goal involvement is high. At their current platform prices they represent the premium ceiling.

4. **Haaland anomaly** — Despite Norway's low G2 Win% (29% vs Senegal), Haaland's personal scoring rate (2 goals vs Iraq from minimal chances) means his individual output may decouple from team context. High-risk, high-ceiling pick.

5. **Díaz momentum** — Colombia's 11-pt G1 performer has the best G1 Δ among forwards paired with a winnable G2 opponent. Under-owned relative to his G1 output.

6. **German DEF/MID value** — Schlotterbeck (DEF, scored G1) and Nmecha (MID, started and scored despite pre-WC "no" rating) are strong G2 picks at very low prices vs a weakened Ivory Coast side.

7. **Rotation risks** — Argentina's G2 vs Austria may see partial rotation (Palacios/Álvarez already benched in G1). France's squad depth means Saliba could again miss out. Monitor pre-match line-up news.

---

## How to Produce the G2 Report

After G2 results are confirmed (Jun 18–23):

1. Collect: match scores, goalscorers, assisters, starting XIs, substitution times for all 23 G2 fixtures
2. Apply the same scoring system as G1 (see `g1_report.md` methodology section)
3. Compute G2 Pts and G2 Δ for each player using **G1-actual Starter status** as the new appearance baseline (i.e. if a player started G1, expected pts = 2; if sub in G1, expected pts = 1; if benched in G1, expected pts = 0)
4. Update `price_value_table.txt`: G3 Win%, Starter status, Fitness, F.St/F.Ap → G2 data
5. Write `g2_report.md` following the same section structure as `g1_report.md`
