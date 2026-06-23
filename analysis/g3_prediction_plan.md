# G3 Standout Prediction Plan — World Cup 2026
*Methodology for identifying high-probability fantasy scoring picks in Group Stage Round 3*
*Written Jun 23 2026 — Colombia/Croatia G2 results pending at time of writing*

---

## Inputs

All data sourced from `price_value_table.txt` (post-G2 update) and `g2_report.md`:

| Column | Use |
|--------|-----|
| `G3 Win%` | Proxy for team strength vs G3 opponent → drives CS and attack expectation |
| `G2 Pts` | Actual G2 output → G3 appearance baseline + form signal |
| `G2 Δ` | Over/underperformance vs G2 expectation → FORM_ADJ |
| `F.St / F.Ap` | Cumulative appearances → informs rotation context |
| `Fitness` | Current physical status entering G3 |
| `Adj Pts` | Pre-tournament model quality baseline |

---

## G3 Fixture List (All Tracked Nations)

All matches played simultaneously within each date. Final group stage round.

| Date | Match | Tracked side Win% | Key tracked players | Notes |
|------|-------|-------------------|--------------------|----|
| Jun 24 | Scotland vs Brazil | BRA 80% | Alisson, Gabriel Magalhães, Vinícius, Raphinha, Cunha, McTominay | Brazil likely rotates fringe |
| Jun 24 | Morocco vs Haiti | MAR 91% | Hakimi | Haiti eliminated |
| Jun 24 | Switzerland vs Canada | SUI 53% | Kobel, Jonathan David | Canada reversed standing after David hat-trick |
| Jun 25 | Japan vs Sweden | JPN 55% | Gyökeres, Isak, Svensson | Sweden eliminated or fighting 3rd |
| Jun 25 | Tunisia vs Netherlands | NED 93% | Timber, van Dijk, Dumfries, Gravenberch, Flekken | Dead rubber risk NED |
| Jun 25 | Germany vs Ecuador | GER 65% | Neuer, Schlotterbeck, Kimmich, Tah, Wirtz, Nmecha, Woltemade | Germany through, semi-dead rubber |
| Jun 25 | CIV vs Curaçao | CIV 72% | Diallo, Singo | CIV needs points |
| Jun 25 | Turkey vs USA | USA 67% | Çalhanoğlu, Güler, Yildiz, Tillman, Pulisic (fitness) | Turkey must win to advance |
| Jun 26 | France vs Norway | FRA 65% | Mbappé, Maignan, Koundé, Saliba, Upamecano, Olise, Dembélé, Doué, Cherki | Group 1st-vs-2nd decider; BOTH play full XI |
| Jun 26 | Spain vs Uruguay | SPA 58% | Simón, Cubarsí, Cucurella, Pedri, Rodri, Yamal, Olmo, Grimaldo | Spain needs win for top spot |
| Jun 26 | Belgium vs New Zealand | BEL 88% | Courtois, De Bruyne, Lukaku, Doku (fitness) | NZL eliminated; Belgium CS banker |
| Jun 26 | Egypt vs Iran | EGY 60% | Salah, Marmoush | Group decider; both need result |
| Jun 27 | Argentina vs Jordan | ARG 95% | Martínez, Romero (inj), Fernández, Lautaro, Álvarez, Palacios | DEAD RUBBER — Argentina rotate |
| Jun 27 | Colombia vs Portugal | COL 52% | Díaz, Nuno Mendes, Rúben Dias, João Neves, Vitinha, Bruno Fernandes, Pedro Neto, Leão | Huge match; Colombia G2 result pending |
| Jun 27 | Panama vs England | ENG 83% | Pickford, Konsa, Guéhi, Bellingham, Rice, Anderson, Kane, Saka, Rashford | England CS candidate vs weak Panama |
| Jun 27 | Croatia vs Ghana | CRO 60% | Gvardiol | Croatia G2 result pending |

---

## G3_OUTLOOK Score Formula

```
G3_OUTLOOK = APP_EXP + CS_EXP + ATTACK_EXP + FORM_ADJ
```

### 1. APP_EXP — Appearance expectation

Based on **G2 actual** appearance status:

| G2 role | P(plays) | APP_EXP |
|---------|----------|---------|
| G2 starter (G2 Pts ≥ 2, started) | 0.93 | 1.85 |
| G2 substitute (G2 Pts = 1 sub app) | 0.50 | 0.90 |
| G2 bench/DNP (G2 Pts = 0, not injury) | 0.10 | 0.15 |
| Injured G2 DNP (fitness = not/mostly + flagged) | 0.10–0.20 | 0.10–0.25 |

**Dead-rubber rotation adjustment** — applies to Argentina vs Jordan, Netherlands vs Tunisia, and partly Germany vs Ecuador where qualifying teams face eliminated opponents:

| Nation | Rotation factor | Rationale |
|--------|----------------|-----------|
| Argentina | 0.75 × P(plays) | 6pts, through; Jordan has 0pts; Scaloni rotates |
| Netherlands | 0.82 × P(plays) | Likely through 6pts; may rest key men vs Tunisia |
| Germany | 0.88 × P(plays) | 6pts, through; Ecuador competitive so partial rotation |

These reduce APP_EXP for starters in those groups (e.g. Argentina starters get P=0.70 not 0.93).

### 2. CS_EXP — Clean sheet expectation

```
CS_EXP = P(plays) × P(CS | G3 Win%) × CS_pts
```

**CS_pts by position:** GK=6, DEF=4, MID=1, FWD=0

**P(CS) calibration from G3 Win%:**

| G3 Win% | P(CS) |
|---------|-------|
| 95%+ | 0.55 |
| 90–94% | 0.50 |
| 85–89% | 0.45 |
| 80–84% | 0.43 |
| 75–79% | 0.38 |
| 70–74% | 0.32 |
| 65–69% | 0.27 |
| 60–64% | 0.23 |
| 55–59% | 0.19 |
| 50–54% | 0.16 |
| 45–49% | 0.13 |
| 20–39% | 0.08 |

**G3 Win% for tracked nations:**

| Match | Win% |
|-------|------|
| Argentina vs Jordan | ARG 95% |
| Netherlands vs Tunisia | NED 93% |
| Morocco vs Haiti | MAR 91% |
| Belgium vs New Zealand | BEL 88% |
| Panama vs England | ENG 83% |
| Brazil vs Scotland | BRA 80% |
| Scotland vs Brazil | SCO 20% |
| CIV vs Curaçao | CIV 72% |
| Turkey vs USA | USA 67% |
| France vs Norway | FRA 65% |
| Germany vs Ecuador | GER 65% |
| Colombia vs Portugal | COL 52% |
| Spain vs Uruguay | SPA 58% |
| Croatia vs Ghana | CRO 60% |
| Egypt vs Iran | EGY 60% |
| Switzerland vs Canada | SUI 53% |
| Japan vs Sweden | JPN 55% |
| Norway vs France | NOR 25% |

### 3. ATTACK_EXP — Expected offensive contribution

```
ATTACK_EXP = P(plays) × BASE_ATTACK × (G3 Win% / 0.50)
```

**BASE_ATTACK:** FWD=1.50, MID=0.93, DEF=0.39, GK=0

### 4. FORM_ADJ — G2 momentum signal

| G2 Δ | Adjustment |
|------|-----------|
| ≥ +9 | +1.5 |
| +6 to +8 | +1.0 |
| +3 to +5 | +0.5 |
| 0 to +2 | 0 |
| −1 | −0.2 |
| −2 | −0.5 |

---

## Dead Rubber / Rotation Risk Flags

The following nations have already qualified heading into G3 and face opponents with nothing to play for or low threat levels. **High rotation risk**:

1. **Argentina** vs Jordan — Argentina 6pts, through regardless. Jordan likely at 0pts. Scaloni will rest Messi, Di María equivalents and give fringe players time. **Specific impact**: Romero may be rested due to injury; Lautaro may rest; Palacios and Álvarez likely to FINALLY start. Only Emiliano Martínez GK rotation is unlikely.

2. **Netherlands** vs Tunisia — Netherlands likely already qualified (6pts). Tunisia likely eliminated. May rotate van Dijk, Dumfries, Gravenberch. **Specific opportunity**: Timber (G2 bench → G3 possible start) is the key rotation play.

3. **Germany** vs Ecuador — Germany 6pts, but Ecuador has 4pts and could get through in 3rd place. Germany won't fully rest but may make 2-3 changes. Medium risk.

4. **France** vs Norway — Both at 6pts fighting for 1st place. **DO NOT** apply rotation discount — both managers will play full strength for group positioning ahead of R32.

5. **Brazil** vs Scotland — Brazil at 4pts, Scotland at 3pts (both still fighting). Brazil plays full strength. No rotation discount.

---

## Standout Categories

### Category A — CS Bankers (highest floor)

Target profile: `G2 Pts ≥ 2` (G2 starter) + `G3 Win% ≥ 80%` + `Pos = GK or DEF`

Priority matches: Belgium vs NZL, Brazil vs Scotland, Panama vs England, Morocco vs Haiti, Argentina vs Jordan (rotation caveat)

### Category B — Premium Goal Threats

Target profile: `G2 Δ ≥ +6` (elite form) OR high-quality FWD + `G3 Win% ≥ 55%` + starter

### Category C — Value Midfielders

Target profile: `G2 starter + MID + G3 Win% ≥ 60%` + `Pts/$ > 30,000`

### Category D — Rotation Gambles

Players who were G2 bench/sub but face weak G3 opponents and may finally get starts:
- Palacios, Álvarez (ARG vs JOR — dead rubber start candidates)
- Timber (NED vs TUN — rotation opportunity)
- Doué (FRA vs NOR — Dembélé may rest → Doué starts?)
- Grimaldo (SPA vs URU — will Cucurella or Grimaldo sit?)
- Doku (if fit for BEL vs NZL)

---

## Top G3 Predicted Standouts

*G3_OUTLOOK scores computed per formula above. Dead rubber adjustments applied to Argentina/Netherlands/Germany.*

| Rank | Player | Nat | Pos | G3 Win% | G2 Δ | G3_OUTLOOK | Category | Note |
|------|--------|-----|-----|---------|------|-----------|---------|------|
| 1 | Courtois | BEL | GK | 88% | +6 | **5.53** | A | GK CS banker; NZL eliminated; Belgium dominant |
| 2 | Alisson Becker | BRA | GK | 80% | +6 | **5.36** | A | GK CS vs Scotland; Brazil through and focused |
| 3 | Pickford | ENG | GK | 83% | +6 | **5.36** | A | GK CS vs Panama; ENG 83% clean sheet probability |
| 4 | Guéhi | ENG | DEF | 83% | +6 | **5.11** | A | G2 starter (G1 bench reversal confirmed), DEF CS vs Panama |
| 5 | Mbappé | FRA | FWD | 65% | +12 | **5.16** | B | Top ceiling pick; FRA vs NOR is the match of G3 |
| 6 | Dembélé | FRA | FWD | 65% | +9 | **5.16** | B | Same formula as Mbappé; one of two will lead France attack |
| 7 | Vinícius Júnior | BRA | FWD | 80% | +6 | **5.08** | B | 2 goals across G1+G2; Brazil vs Scotland is winnable |
| 8 | Hakimi | MAR | DEF | 91% | +4 | **4.79** | A | DEF CS vs Haiti; Morocco dominant; highest DEF floor |
| 9 | Emiliano Martínez | ARG | GK | 95% | +6 | **4.71** | A⚠️ | Highest CS expectation but DEAD RUBBER rotation risk |
| 10 | Konsa | ENG | DEF | 83% | +4 | **4.61** | A | DEF CS vs Panama; confirmed G2 starter |
| 11 | Salah | EGY | MID | 60% | +9 | **4.61** | B | 1G+1A in G2; Egypt vs Iran is a group decider |
| 12 | Gabriel Magalhães | BRA | DEF | 80% | +4 | **4.60** | A | DEF CS vs Scotland; Brazil back four reliable |
| 13 | Maignan | FRA | GK | 65% | +6 | **4.41** | A | GK CS chance against Norway; France 65% CS probability |
| 14 | Olise | FRA | MID | 65% | +7 | **4.23** | C | 2 assists in G2; MID CS bonus if France keep CS vs NOR |
| 15 | Nuno Mendes | POR | DEF | 52% | +10 | **4.22** | A | G2 free-kick goal hero; Colombia is tough but Mendes delivers |
| 16 | Kane | ENG | FWD | 83% | 0 | **4.14** | B | 82% win% carries his ATTACK_EXP despite 0pt G2; vs Panama |
| 17 | Haaland | NOR | FWD | 25% | +12 | **4.05** | B | NOR underdog vs France but personal form rate anomaly again |
| 18 | Romero | ARG | DEF | 95% | +4 | **3.40** | A⚠️ | CS probability high but injury (knee vs Austria) reduces P(plays) to ~0.55 |
| 19 | De Bruyne | BEL | MID | 88% | +1 | **3.82** | C | MID CS + attack upside vs NZL; reliable Belgium starter |
| 20 | Koundé | FRA | DEF | 65% | +4 | **3.86** | A | DEF CS vs Norway; France back four starting again |
| 21 | Saliba | FRA | DEF | 65% | +4 | **3.86** | A | Same profile as Koundé |
| 22 | Upamecano | FRA | DEF | 65% | +4 | **3.86** | A | Same profile |
| 23 | Rúben Dias | POR | DEF | 52% | +6 | **3.72** | A | G2 comeback story; Portugal vs Colombia is even but Dias should start |
| 24 | Bellingham | ENG | MID | 83% | +1 | **3.69** | C | MID CS + attack upside vs Panama; England's creative force |
| 25 | Rice | ENG | MID | 83% | +1 | **3.69** | C | Same as Bellingham vs Panama |
| 26 | Anderson | ENG | MID | 83% | +1 | **3.69** | C | Same |
| 27 | Marmoush | EGY | FWD | 60% | 0 | **3.53** | B | Egypt vs Iran; FWD attack upside vs quality opponent |
| 28 | Bruno Fernandes | POR | MID | 52% | +4 | **3.31** | C | OG corner assist G2; vs Colombia; MID CS + attack |
| 29 | Ødegaard | NOR | MID | 25% | +3 | **2.86** | C | Assist G2; low win% drags score; Norway underdog vs France |
| 30 | Díaz | COL | FWD | 52% | G2 TBD | **~3.4** | B | G1 +9; G3 vs Portugal; G3_OUTLOOK depends on G2 result |
| 31 | Yamal | SPA | FWD | 58% | +7 | **3.41** | B | Scored G2; Spain vs Uruguay is competitive; no CS for FWD |
| 32 | Cubarsí | SPA | DEF | 58% | +4 | **3.40** | A | DEF CS if Spain keeps sheet vs Uruguay |
| 33 | Simón | SPA | GK | 58% | +6 | **3.65** | A | GK CS if Spain keeps sheet vs Uruguay |
| 34 | Gvardiol | CRO | DEF | 60% | G2 TBD | **~3.0** | A | Croatia G2 result pending; G3 vs Ghana |
| 35 | Jonathan David | CAN | FWD | 47% | +19 | **3.32** | B | Hat-trick G2; form anomaly; Canada vs Switzerland is even |

---

## Rotation Gamble — "If Starts" Picks

| Player | G3 Opponent | Base G3_OUTLOOK | If Starts | Rationale |
|--------|-------------|-----------------|-----------|-----------|
| Palacios | JOR (ARG 95%) | 0.55 | **4.01** | ARG dead rubber; Scaloni has incentive to finally give Palacios minutes |
| Álvarez | JOR (ARG 95%) | 1.45 | **3.73** | G2 sub appearance; likely starts G3 rest-rotation |
| Timber | TUN (NED 93%) | 1.21 | **4.52** | G2 bench DNP (rotation); NED dead rubber = prime Timber opportunity |
| Grimaldo | URU (SPA 58%) | 0.68 | **2.87** | Hasn't started either group game; Spain may give him G3 |
| Doué | NOR (FRA 65%) | 0.96 | **4.07** | G1 starter, G2 sub; if Dembélé rested vs Norway, Doué steps in |
| Doku | NZL (BEL 88%) | 0.40 | **4.47** | Illness G2 DNP; could be fit for NZL |
| Leão | COL (POR 48%) | 2.22 | **4.19** | G2 sub scorer; could start G3 vs Colombia |

---

## Key G3 Narratives

1. **France vs Norway — The tournament's best G3 match.** Two unbeaten sides fighting for group top spot. Mbappé (brace x2 in G1+G2) vs Haaland (brace x2 in G1+G2). Neither manager rotates. This is a ~5pt ceiling match for either team's FWDs, and a 4.4pt CS banker matchup for GKs. The biggest fantasy exposure is Mbappé/Dembélé (FRA 65% win%) vs Haaland (NOR 25% win% but anomaly score 4.05). Model favours the French attackers.

2. **England vs Panama — The safest CS triple.** England 83% win vs a Panama side that is likely eliminated. Pickford (5.36), Guéhi (5.11), and Konsa (4.61) are the three cleanest structural picks in all of G3. The only risk: England are already through if Ghana/Croatia result goes their way — they may ease off. But England's setup vs Panama should produce a clean sheet.

3. **Argentina dead rubber — The Palacios moment.** Argentina 6pts vs Jordan 0pts. Scaloni HAS to rotate. The three-game Palacios ($0.0041/pt, Pts/$=122,530) bench watch finally ends here. If he starts, his 4.01 "if starts" outlook comes with the highest Pts/$ in the tournament. Same logic for Álvarez and reducing Romero's risk (injured knee).

4. **Belgium vs New Zealand — Courtois is the pick.** Belgium 88% vs an eliminated NZL side. Courtois (5.53) is the highest G3_OUTLOOK score of any GK and the top floor pick in the round. De Bruyne's MID CS + attack gives 3.82. Doku's return from illness is the wildcard — if fit, Category D gamble.

5. **Colombia vs Portugal — The group decider.** Both strong teams, ~52/48 split. Colombia's standing depends on their G2 result (pending). If Colombia won G2, they arrive with 6pts and might rest players. If Colombia drew/lost G2, this is a must-win. Díaz (~3.4 G3_OUTLOOK) vs Nuno Mendes (4.22) is the value headliner. Bruno Fernandes (3.31) has demonstrated he delivers on corners. Watch for Leão start (if starts: 4.19).

6. **Netherlands vs Tunisia — Timber's window.** Netherlands 93% win%, likely already qualified, facing eliminated Tunisia. Timber was G2 bench-DNP despite being a G1 starter. With near-zero competitive pressure for Netherlands in G3, Timber (DEF, "if starts" = 4.52) is the highest upside rotation pick in the round. If he's in the XI, he gets DEF CS + start = 6pts with very high probability.

7. **Egypt vs Iran — Salah as G3 anchor.** Both teams likely level on points; this is a group decider. Salah's G2 1G+1A (11pts) makes him the form player for the G3 matchup. Egypt 60% win%, which places Salah at 4.61 — solidly in the top 10. Marmoush (3.53) is the value alternative but ceiling is lower. No CS expected (Iran will push).

8. **Spain vs Uruguay — Grimaldo's last chance.** Spain needs a win vs Uruguay (both likely ~4pts entering G3). This is meaningful for both teams. But Grimaldo's rotation risk applies even in meaningful games — he hasn't started G1 or G2 despite being fit. Cubarsí (3.40), Simón (3.65), and Pedri/Rodri are more reliable Spain picks here.

---

## Key Risks vs G2 Prediction Model

| Risk | Player | Concern |
|------|--------|---------|
| Dead rubber rotation | Emiliano Martínez, Romero, Fernández (ARG) | Argentina may rest players vs Jordan |
| Injury | Romero (Argentina, knee) | Might not feature at all |
| Dead rubber rotation | van Dijk, Dumfries, Gravenberch (NED) | Netherlands likely through; Tunisia is trivial |
| Match intensity | Kane (England) | Blanked in G2; Panama is exploitable but form is flat |
| Fitness | Doku (Belgium) | Recovery from illness illness uncertain |
| Pending G2 | Díaz (Colombia), Gvardiol (Croatia) | G3 context changes based on G2 result |
| France rotation | Doué, Cherki | Might not play vs Norway; Dembélé/Olise will get priority |

---

## How to Produce the G3 Report

After G3 results are confirmed (Jun 24–27):

1. Collect: match scores, goalscorers, assisters, starting XIs, substitution times for all G3 fixtures
2. Apply same scoring system (Goal=+6, Assist=+3, GK CS=+6, DEF CS=+4, MID CS=+1, Start=+2, Sub=+1, Yellow=-1, Red=-3)
3. G3 Δ baseline = **G2 actual starter status**: G2 starter → expected 2, G2 sub → expected 1, G2 bench → expected 0
4. Add `G3_ACTUAL` dict to `price_value_lookup.py` with same structure as `G2_ACTUAL`
5. Update `price_value_table.txt`: add G3 Pts and G3 Δ columns; update F.St/F.Ap (max 3 each); update Win% column to reflect knockouts context
6. Write `analysis/g3_report.md` following same section structure as `g2_report.md`
