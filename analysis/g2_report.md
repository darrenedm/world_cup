# G2 Performance Report — World Cup 2026
*Covers completed Group Stage Round 2 matches as of Jun 21 2026*  
*Pending (Jun 22–23): France, England, Argentina, Colombia, Norway, Portugal, Croatia*  
*Only covers the 93 priced players tracked in price_value_table.txt*

---

## Methodology — How to reproduce this report for G3

### Scoring system
Every player's G2 fantasy score is computed from the raw match result using this rule set:

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

A "clean sheet" counts only if the player's team conceded 0 goals **and** the player appeared in the match.

### What G2 Pts measures
`G2 Pts` = the sum of the above for that player in their Group 2 match only. Players who were not selected (bench, injury DNP) score 0.

### What G2 Δ means
`G2 Δ = G2 Pts − G2 appearance expectation`

G2 appearance expectation derives from **G1 actual** appearances (not pre-tournament LIVE_STATUS):

| G1 role | G2 expected pts |
|---------|----------------|
| G1 starter (F.St=1) | 2 |
| G1 substitute (F.Ap=1, F.St=0) | 1 |
| G1 bench/DNP (F.Ap=0) | 0 |

G2 Δ > 0: delivered goals/assists/CS on top of appearing  
G2 Δ = 0: appeared and matched G2 appearance expectation  
G2 Δ < 0: expected to appear but didn't (benched, injured, or rotated)

### How to reproduce this for G3

1. **Collect match data** for all G3 fixtures — scorers, assisters, starting XIs, substitution times, clean sheets.
2. **Add a `G3_ACTUAL` dict** to `price_value_lookup.py` with the same structure as `G2_ACTUAL`.
3. **G3 Δ baseline** = G2 actual appearance status (G2 starter → expected 2, G2 sub → expected 1, G2 bench → expected 0).
4. **Update `price_value_table.txt`**: add G3 Pts and G3 Δ columns; update Starter/Fitness/Win% from G2 actuals.
5. **Write `analysis/g3_report.md`** following this structure.

---

## The G2 Headline — Jonathan David's Hat-Trick

Canada's Jonathan David delivered the highest individual G2 score among all tracked players with a **hat-trick against Qatar**.

| Player | Match | Goals | G2 Pts | G1 Role | G2 Δ |
|--------|-------|-------|-------:|---------|-----:|
| **Jonathan David** | CAN vs QAT | 3 | 20 | G1 sub | +19 |

David came off the bench in G1 (1pt appearance; G2 expected baseline = 1pt), then **started and scored three times** in G2. The G2_OUTLOOK model assigned him a "sometimes" APP_EXP — a predicted ceiling of roughly 3pts. This was the model's largest individual miss of G2, surpassing even the Nmecha surprise of G1.

---

## Top Overperformers (Δ ≥ +4)

| # | Player | Nat | Pos | G2 Pts | G2 Δ | G1 Role | Notes |
|---|--------|-----|-----|-------:|-----:|---------|-------|
| 1 | Jonathan David | Canada | FWD | 20 | +19 | G1 starter | Hat-trick vs Qatar; biggest G2 surprise |
| 2 | Matheus Cunha | Brazil | FWD | 14 | +12 | G1 starter | 2 goals vs Haiti; not in prediction top 20 |
| 3 | Mohamed Salah | Egypt | MID | 11 | +9 | G1 starter | 1G+1A vs New Zealand; Egypt's historic first WC win |
| 4 | Lamine Yamal | Spain | FWD | 8 | +7 | G1 sub | First WC start; scored vs Saudi Arabia |
| 5 | Pedro Porro | Spain | DEF | 6 | +6 | G1 bench | Reversed G1 DNP; started and earned full DEF CS |
| 6 | Unai Simón | Spain | GK | 8 | +6 | G1 starter | GK CS vs Saudi Arabia; Category A top pick delivered |
| 7 | Alisson Becker | Brazil | GK | 8 | +6 | G1 starter | GK CS vs Haiti; Category A banker |
| 8 | Vinícius Júnior | Brazil | FWD | 8 | +6 | G1 starter | Goal vs Haiti; G1 form carried forward |
| 9 | Thibaut Courtois | Belgium | GK | 8 | +6 | G1 starter | GK CS vs Iran despite Doku illness absence |
| 10 | Pau Cubarsí | Spain | DEF | 6 | +4 | G1 starter | DEF CS vs Saudi Arabia; confirmed every-game starter |
| 11 | Marc Cucurella | Spain | DEF | 6 | +4 | G1 starter | DEF CS vs Saudi Arabia |
| 12 | Gabriel Magalhães | Brazil | DEF | 6 | +4 | G1 starter | DEF CS vs Haiti |
| 13 | Achraf Hakimi | Morocco | DEF | 6 | +4 | G1 starter | DEF CS vs Scotland |

**Notable Δ = +3:** Felix Nmecha (Germany MID, 5pts, assist vs Ivory Coast — G1 form carry), Dani Olmo (Spain FWD, 5pts, assisted Yamal's goal).

---

## Underperformers — Expected starters who blanked (Δ ≤ −2)

| Player | Nat | Pos | G2 Pts | G2 Δ | Reason |
|--------|-----|-----|-------:|-----:|--------|
| Christian Pulisic | USA | FWD | 0 | −2 | Calf injury — missed G2 vs Australia |
| Romelu Doku | Belgium | FWD | 0 | −2 | Respiratory infection — ruled out vs Iran |
| Jurriën Timber | Netherlands | DEF | 0 | −2 | Benched for G2 vs Sweden; Verbruggen XI used |

**Rotation flags (Δ = −1):** Alejandro Grimaldo (Spain, DEF) — bench DNP again vs Saudi Arabia. Pre-G2 model correctly flagged him as Category D rotation risk after G1 bench appearance. Grimaldo has not started either group game despite fitness.

---

## CS Cleaners — Defensive clean sheet hauls

Six of the eleven completed G2 matches produced clean sheets for tracked nations:

| Match | CS Team | Tracked beneficiaries |
|-------|---------|----------------------|
| Spain vs Saudi Arabia | Spain | Simón 8pts, Porro 6pts, Cubarsí 6pts, Cucurella 6pts, Pedri 3pts, Rodri 3pts |
| Brazil vs Haiti | Brazil | Alisson 8pts, Gabriel Magalhães 6pts |
| Belgium vs Iran | Belgium | Courtois 8pts, De Bruyne 3pts |
| Morocco vs Scotland | Morocco | Hakimi 6pts |
| USA vs Australia | USA | Tillman 3pts (MID CS) |
| Ecuador vs Curaçao | Ecuador | Caicedo 3pts (MID CS) |

**No CS in completed G2 matches:** Germany vs Ivory Coast, Netherlands vs Sweden, Turkey vs Paraguay, Uruguay vs Cape Verde, Switzerland, Canada vs Qatar, Egypt vs New Zealand (NZL scored 15').

Spain's G2 vs Saudi Arabia was the richest single defensive game for tracked players — six players collected CS bonus points across GK (8pts), DEF (6pts each) and MID (3pts each). The prediction model's "Spain CS wall" narrative from the G2 plan was the round's clearest structural call.

**Correction vs G2 prediction plan:** Porro started G2 (predicted as bench risk / Category D) and delivered the DEF CS bonus. The prediction plan correctly identified Cubarsí and Cucurella as the reliable Spain CS picks but undervalued Porro's chances of returning to the XI.

---

## G2 Reality vs G2 Prediction Model

| Prediction | Verdict |
|------------|---------|
| Spain CS vs Saudi Arabia (Simón, Cubarsí, Cucurella) | ✅ Correct — all three Category A picks delivered 6–8pts |
| Brazil CS vs Haiti (Alisson, Gabriel Magalhães) | ✅ Correct — BRA dominant, both CS bankers delivered |
| Vinícius Júnior form carry | ✅ Correct — goal, 8pts +6 |
| Alisson GK CS banker | ✅ Correct — 8pts +6 |
| Gabriel Magalhães DEF CS | ✅ Correct — 6pts +4 |
| Nmecha G1 form carry | 🟡 Partial — assist (+3) but not a goal; still above baseline |
| Schlotterbeck DEF with attack upside | ❌ Faded — 2pts +0; no CS, no goal |
| Raphinha BRA attack depth | ❌ Blanked offensively — 2pts +0 |
| Grimaldo rotation risk (Category D) | ✅ Correct — bench DNP again; risk flag justified |
| Porro bench risk (Category D) | ❌ Model flagged correctly as risk, but he STARTED and delivered +6 (reversal) |
| Doku Belgium injury risk | ✅ Correct — respiratory infection ruled him out |
| Jonathan David (sometimes APP_EXP) | ❌ Model miss — predicted ~3pts, delivered 20pts hat-trick |
| Matheus Cunha (unranked) | ❌ Model miss — 14pts, 2 goals; not in top 20 |
| Salah Egypt (Category C, ~4pt OUTLOOK) | 🟡 Direction correct, magnitude undersold — 11pts (1G+1A vs NZL); model had him as a good pick but ceiling was higher |
| Marmoush Egypt (Category B FWD) | ✅ Correct baseline — started, 2pts +0; no goals but delivered appearance value |
| France vs Iraq CS (pending) | ⏳ Mbappé, Maignan, Koundé, Saliba, Olise all pending Jun 22–23 |
| Kane England form carry (pending) | ⏳ ENG vs GHA Jun 23 |
| Díaz momentum (pending) | ⏳ COL vs DRC Jun 22 |
| Haaland anomaly (pending) | ⏳ NOR vs SEN Jun 22 |

---

## Key G2 Narratives (Completed Matches)

1. **Spain's CS wall delivered** — The pre-G2 plan's clearest structural call. Spain vs Saudi Arabia (91% win%) produced 6 tracked players earning CS bonus. Simón (8pts), Porro/Cubarsí/Cucurella (6pts each), Pedri/Rodri (3pts). Olmo assisted Yamal's goal (+3). The only disappointment: Grimaldo bench DNP again.

2. **Yamal's first WC start** — After being managed carefully in G1 (sub 71'), Yamal started G2 and scored. His 8pts (Δ=+7 from G1 sub baseline) was one of the cleaner predictions — the model had him in the Spain CS core with scoring upside.

3. **Matheus Cunha brace — the unranked 14pt bomb** — Brazil's Cunha (Adj Pts 148.6, not in top 20 predicted standouts) scored twice vs Haiti for 14pts. With Alisson's CS and Gabriel Magalhães's DEF CS also delivering, Brazil's G2 was the most productive single match for tracked players after Spain.

4. **Jonathan David's hat-trick defies the model** — The G2_OUTLOOK framework couldn't account for a "G1 sub becomes G2 starter and scores 3" scenario. David's 20pts (+19) is the G2 story. Canada's 62% G2 win probability should have been a green flag, but the APP_EXP model significantly underweighted his starting probability.

5. **Porro starts after G1 bench — Grimaldo doesn't** — The two Spain DEFs who were bench in G1 diverged sharply. Porro returned to the XI and earned a full CS (6pts, Δ=+6). Grimaldo remained on the bench (0pts, Δ=−1). In hindsight, Porro's 2024–25 club form at Tottenham should have been weighted higher.

6. **Belgium CS without Doku** — Courtois kept a clean sheet vs Iran (8pts) and De Bruyne contributed as normal (3pts, MID CS). Lukaku started (2pts, FWD no CS) but didn't score. The illness removal of Doku (rated as G1 starter, Δ=−2) was absorbed cleanly — Belgium's structure held.

7. **Morocco CS vs Scotland** — Hakimi delivered DEF CS (6pts, Δ=+4) as Scotland managed only a started-but-blanked performance from McTominay (2pts). The 65% Morocco win probability CS expectation was correct.

8. **Salah leads Egypt to historic first WC win** — Egypt 3-1 New Zealand (Jun 21). Salah started, scored at 67' (combination with Zico) and delivered the corner assist for Trezeguet's 82' header. 11pts, Δ=+9 — third-highest G2 score among all tracked players. Marmoush started but didn't feature on the scoresheet (2pts, Δ=0). New Zealand's Surman header at 15' broke Egyptian CS hopes early, so no defensive bonus for Egyptian players. The G2_OUTLOOK model had Salah at ~4.21 (Category C); he exceeded that significantly.

---

## Summary Stats (completed G2 matches only)

| Metric | Value |
|--------|-------|
| Highest G2 score | 20 pts (Jonathan David, hat-trick vs Qatar) |
| Biggest G2 Δ | +19 (Jonathan David) |
| CS matches among completed | 6 of 13 (Spain, Brazil, Belgium, Morocco, USA, Ecuador) |
| Richest single CS game | Spain vs Saudi Arabia — 6 tracked players, CS bonus across GK/DEF/MID |
| Biggest model miss | Jonathan David — predicted ~3pts, delivered 20pts |
| Biggest unranked overperformer | Matheus Cunha — 14pts, 2 goals, not in prediction top 20 |
| G1 form that carried | Vinícius Jr (+6→+6), Nmecha (+8→+3), Simón (+6→+6), Salah (+3→+9) |
| G1 form that faded | Schlotterbeck (8pts G1 → 2pts G2), Raphinha (blank offensively) |
| Injury/illness blanks | Pulisic (Δ=−2), Doku (Δ=−2) |
| Rotation surprises | Porro returned to XI (+6); Grimaldo DNP again (−1) |
| Prediction model hit rate (completed) | 7 clear ✅, 3 ❌, 3 🟡 partial out of 13 assessed |

---

## Pending G2 Fixtures (Jun 22–23)

| Match | Key tracked players | G2 Win% | Notes |
|-------|---------------------|---------|-------|
| France vs Iraq | Mbappé, Maignan, Koundé, Saliba, Upamecano, Olise, Dembélé, Doué | 93% | Rank #1 CS banker; Mbappé G1 brace form carry |
| England vs Ghana | Kane, Bellingham, Rice, Anderson, Saka, Pickford | 75% | Kane 14pt G1 form; ENG CS possible |
| Argentina vs Austria | Romero, Martínez, Fernández, Álvarez, Palacios | 63% | Rotation risk; Palacios may finally start |
| Colombia vs DR Congo | Díaz | 78% | G1 +9 momentum carry; COL should dominate |
| Norway vs Senegal | Haaland, Ødegaard | 29% | Haaland individual rate above team; high-variance |
| Portugal vs Uzbekistan | Leão, Vitinha, Bruno Fernandes, Rúben Dias, João Neves | 84% | POR attack overdue after G1 1-1 draw |
| Croatia vs Panama | Gvardiol | 57% | Near-even; modest CS expectation |

*Update this file once all G2 fixtures complete (by Jun 23).*
