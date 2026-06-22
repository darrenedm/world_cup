# G1 Performance Report — World Cup 2026
*Covers all 23 matchdays of Group Stage Round 1 (Jun 12–17 2026)*  
*Only covers the 93 priced players tracked in price_value_table.txt*

---

## Methodology — How to reproduce this report for G2

### Scoring system
Every player's G1 fantasy score is computed from the raw match result using this rule set:

| Event | Points |
|-------|--------|
| Goal scored | +6 |
| Assist | +3 |
| GK clean sheet (90 min) | +6 |
| DEF clean sheet (played any min) | +4 |
| MID clean sheet (played any min) | +1 |
| FWD clean sheet | 0 |
| Started (in XI from kick-off) | +2 |
| Came on as substitute | +1 |
| Yellow card | −1 |
| Red card | −3 |

A "clean sheet" counts only if the player's team conceded 0 goals **and** the player appeared in the match. A 90+4' equaliser breaks a clean sheet (see Switzerland–Qatar).

### What G1 Pts measures
`G1 Pts` = the sum of the above for that player in their Group 1 match only. Players who were not selected (bench, injury DNP) score 0.

### What Δ means
`Δ = G1 Pts − appearance expectation`

Appearance expectation is derived from that player's **pre-tournament** `LIVE_STATUS` starter rating in `price_value_lookup.py`:
- `"yes"` → expected 2 pts (starter appearance value)
- `"sometimes"` → expected 1 pt (sub-role appearance value)
- `"no"` → expected 0 pts

Δ > 0: delivered goals/assists/CS bonus on top of appearing  
Δ = 0: appeared and scored exactly the baseline (or wasn't expected to play and didn't)  
Δ < 0: expected to play but didn't (benched, injured, or rotated)

### How to reproduce this for G2

1. **Collect match data** for all G2 fixtures (Jun 18–22) — scorers, assisters, starting XIs, substitution times, clean sheets.
2. **Add a `G2_ACTUAL` dict** to `price_value_lookup.py` with the same structure as `G1_ACTUAL`:
   ```python
   G2_ACTUAL = {
       "Player display name": (g2_pts, goals, assists, cs_bonus, "notes"),
       ...
   }
   ```
   One entry per priced player. Players not in the squad or whose team hasn't played yet get `None` (omit from dict).
3. **Update `main()`** to look up `G2_ACTUAL.get(display)` and compute `g2_delta` using the same appearance-expectation logic. Use the **actual** G2 starting XI (not pre-tournament `LIVE_STATUS`) as the baseline — i.e. update `LIVE_STATUS` starters from G2 observed lineups before computing Δ, or pass actual starter status from the dict's notes field.
4. **Add `G2 Pts` and `G2 Δ` columns** to the print format (extend the tuple in `results.append`).
5. **Run the script** → regenerates `analysis/price_value_table.txt`.
6. **Write `analysis/g2_report.md`** following the same section structure as this file.

---

## The Headliners — Tri-way tie at the top

Three of the tournament's biggest names all scored **14 pts** in G1, matching perfectly on a brace-and-start:

| Player | Match | Goals | G1 Pts | Pre-WC Rank | Δ |
|--------|-------|-------|-------:|------------:|--:|
| **Harry Kane** | ENG 4-2 CRO | 2 (12', 42' pen) | 14 | #79 | +12 |
| **Kylian Mbappé** | FRA 3-1 SEN | 2 (53', 66') | 14 | #81 | +12 |
| **Erling Haaland** | NOR 4-1 IRQ | 2 (29', 43') | 14 | #86 | +12 |

Mbappé's G1 broke France's all-time scoring record. All three were started despite pre-tournament fitness concerns (Mbappé's hamstring, Kane's price premium, Haaland's rested-for-friendly status). The "expensive = justified" tier.

---

## Top Overperformers (Δ ≥ +4)

| # | Player | Nat | Pos | G1 Pts | Δ | Pre-WC Rank | Notes |
|---|--------|-----|-----|-------:|--:|------------:|-------|
| 1 | Kylian Mbappé | France | FWD | 14 | +12 | #81 | 2 goals; broke France record |
| 2 | Harry Kane | England | FWD | 14 | +12 | #79 | 2 goals inc. pen; England captain |
| 3 | Erling Haaland | Norway | FWD | 14 | +12 | #86 | 2 goals; rested both pre-WC friendlies |
| 4 | Luis Díaz | Colombia | FWD | 11 | +9 | #55 | 1G+1A vs Uzbekistan; Bayern form carries over |
| 5 | Felix Nmecha | Germany | MID | 8 | +8 | #87 | Started; 1 goal in 7-1 demolition; was listed "no" for starter |
| 6 | Jude Bellingham | England | MID | 8 | +6 | #26 | 1 goal (47'); started, subbed off later |
| 7 | Nico Schlotterbeck | Germany | DEF | 8 | +6 | #56 | 1 goal; defender scoring in 7-1 rout |
| 8 | Viktor Gyökeres | Sweden | FWD | 8 | +6 | #71 | 1 goal vs Tunisia; 5-1 win |
| 9 | Unai Simón | Spain | GK | 8 | +6 | #72 | GK CS in 0-0 vs Cape Verde; clean sheet banker |
| 10 | Alexander Isak | Sweden | FWD | 8 | +6 | #73 | 1 goal vs Tunisia; fibula scare forgotten |
| 11 | Marcus Rashford | England | FWD | 7 | +6 | #57 | Sub 2nd half; 1 goal (85'); impact role vindicated |
| 12 | Amad Diallo | Ivory Coast | FWD | 7 | +6 | #18 | Sub 56'; 1 goal (90'); CIV won 1-0; strong G1 for cheap pick |
| 13 | Alejandro Grimaldo | Spain | DEF | 5 | +3 | #5 | Sub 71'; DEF CS (5 pts = 1 sub + 4 CS) |
| 14 | Cristian Romero | Argentina | DEF | 6 | +4 | #17 | DEF CS; ARG 3-0 Algeria |
| 15 | Marc Cucurella | Spain | DEF | 6 | +4 | #41 | DEF CS; started in Spain's 0-0 |

**Notable: Bukayo Saka (+3, sub assist)**, **Christian Pulisic (+3, assist)**, **Kevin De Bruyne (+3, assist for OG)**, **Mohamed Salah (+3, assist)**, **Martin Ødegaard (+3, assist)** — all delivered above appearance value.

---

## Underperformers — Expected starters who blanked (Δ = −2)

These players were rated "yes" for starter pre-tournament but scored 0 or underperformed (bench or limited role):

| Player | Nat | Pos | Pre-WC Rank | G1 Pts | Δ | Reason |
|--------|-----|-----|------------:|-------:|--:|--------|
| Exequiel Palacios | Argentina | MID | #1 | 0 | −2 | Bench — Almada started; ARG 3-0 Algeria |
| Lamine Yamal | Spain | FWD | #85 | 1 | −1 | Sub 71' (19 mins); hamstring management; 1 pt appearance only |
| Marc Guéhi | England | DEF | #39 | 0 | −2 | Bench — Konsa started ahead of him |
| Julián Álvarez | Argentina | FWD | #61 | 0 | −2 | Bench |
| Daniel Svensson | Sweden | DEF | #16 | 0 | −2 | Not in Sweden XI vs Tunisia |

**Key finding**: Palacios (#1 by value/price ratio) was benched in G1. The model's top value pick delivered nothing.

**Correction vs pre-report assumptions**: William Saliba (France DEF) actually started alongside Upamecano — Konaté was the one who was benched. Manuel Neuer (Germany GK) started vs Curaçao; Baumann was not used. Both scored 2 pts (start, no CS).

---

## The Underdogs — Surprise big scorers

Players who weren't expected to contribute heavily but delivered:

- **Felix Nmecha** (Germany MID, #87): 8 pts, 1 goal. Listed as a bench option pre-WC, Nmecha started and scored in Germany's 7-1 rout. Best surprise of G1.
- **Amad Diallo** (Ivory Coast FWD, #18): 7 pts, 1 goal (sub 56', scored 90'). CIV's 1-0 win over Ecuador was unexpected; Diallo came off the bench and scored the winner. Cheap at 0.00730.
- **Marcus Rashford** (England FWD, #57): 7 pts as sub. Was "sometimes" starter but his 85' goal was England's 4th. Sub-role delivery.
- **Nico Schlotterbeck** (Germany DEF, #56): 8 pts in a 7-1 blowout. Defenders scoring is bonus territory.

---

## CS Cleaners — Defensive clean sheet value

Spain's 0-0 vs Cape Verde was the only true defensive CS across all 23 G1 matches among tracked players. Spain's back four was Llorente (RB), Laporte, Cubarsí, Cucurella — Grimaldo and Porro were both on the bench:

| Player | Pos | G1 Pts | Δ | Note |
|--------|-----|-------:|--:|------|
| Unai Simón (GK) | GK | 8 | +6 | Started |
| Pau Cubarsí (DEF) | DEF | 6 | +4 | Started |
| Marc Cucurella (DEF) | DEF | 6 | +4 | Started |
| Pedri (MID) | MID | 3 | +1 | Started |
| Fabián Ruiz (MID) | MID | 3 | +1 | Started |
| Rodri (MID) | MID | 3 | +1 | Started |
| Alejandro Grimaldo (DEF) | DEF | 5 | +3 | Sub 71' (DEF CS: 1+4) |
| Lamine Yamal (FWD) | FWD | 1 | −1 | Sub 71' (no FWD CS bonus) |
| Pedro Porro (DEF) | DEF | 0 | −1 | Bench DNP |

Scotland also kept a CS (1-0 vs Haiti): **Scott McTominay** 3 pts (+1).  
Argentina kept a CS (3-0 Algeria): **Emiliano Martínez** 8 pts (+6), **Cristian Romero** 6 pts (+4), **Enzo Fernández** 3 pts (+1).

---

## G1 Reality vs Pre-Tournament Narrative

| Narrative | Verdict |
|-----------|---------|
| "Turkey are overpriced" (Çalhanoğlu/Güler/Yildiz) | ✅ Correct — all 2 pts; lost 0-2 to Australia |
| "Portugal value picks" | ❌ All drew 1-1 vs DR Congo; every POR player scored just 2 pts |
| "Spain CS candidates" | ✅ Correct — 0-0 vs Cape Verde; all Spain defenders delivered |
| "Haaland rested both friendlies → risk" | ✅ Risk was worth it — 14 pts G1 brace |
| "Germany value (7-1 win)" | ✅ Schlotterbeck, Nmecha both 8 pts; cheap German defenders delivered |
| "Belgium disappointment" | Partial — drew 1-1 with Egypt; De Bruyne assist (+3) but Lukaku only sub (1 pt) |
| "Brazil will dominate Morocco" | ❌ Drew 1-1; Vinícius 8 pts but Raphinha/Alisson just 2 each |
| "Switzerland safe CS pick vs Qatar" | ❌ Late equaliser; Kobel GK = 2 pts only |

---

## Summary Stats

| Metric | Value |
|--------|-------|
| Highest G1 score | 14 pts (Kane, Mbappé, Haaland) |
| Most assists in G1 | 1 each (Rice, Anderson, Olise, Salah, Ødegaard, Díaz, Pulisic, De Bruyne, Saka) |
| Players who scored 0 G1 pts | 19 (mostly bench/DNP; Neuer and Saliba corrected to 2 pts starters) |
| Players who matched expectation (Δ=0) | 19 (including Saliba and Neuer, now confirmed starters) |
| Biggest surprise overperformer | Nmecha (starter="no", 8 pts) |
| Biggest selection miss | Palacios (#1 value pick, benched, 0 pts) |
| CS matches yielding DEF/GK bonus | 3: Spain (0-0 vs Cape Verde), Argentina (3-0 Algeria), Scotland (1-0 Haiti) |
