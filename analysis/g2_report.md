# G2 Performance Report — World Cup 2026
*Covers all 21 Group Stage Round 2 matches (Jun 18–23 2026)*  
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
| 1 | Jonathan David | Canada | FWD | 20 | +19 | G1 sub | Hat-trick vs Qatar; biggest G2 surprise |
| 2 | Matheus Cunha | Brazil | FWD | 14 | +12 | G1 starter | 2 goals vs Haiti; not in prediction top 20 |
| 3 | Erling Haaland | Norway | FWD | 14 | +12 | G1 starter | 2 goals vs Senegal (48', 58'); model anomaly call vindicated despite 29% win% |
| 4 | Kylian Mbappé | France | FWD | 14 | +12 | G1 starter | 2 goals vs Iraq; G1 brace form carry; 100th France cap |
| 5 | Mohamed Salah | Egypt | MID | 11 | +9 | G1 starter | 1G+1A vs New Zealand; Egypt's historic first WC win |
| 6 | Ousmane Dembélé | France | FWD | 11 | +9 | G1 starter | 1G+1A vs Iraq (off 66'); scored and assisted before subbed |
| 7 | Nuno Mendes | Portugal | DEF | 12 | +10 | G1 starter | Free-kick goal + DEF CS vs Uzbekistan; highest DEF score of G2 |
| 8 | Michael Olise | France | MID | 9 | +7 | G1 starter | 2 assists vs Iraq + MID CS; best MID output of G2 |
| 9 | Lamine Yamal | Spain | FWD | 8 | +7 | G1 sub | First WC start; scored vs Saudi Arabia |
| 10 | Emiliano Martínez | Argentina | GK | 8 | +6 | G1 starter | GK CS vs Austria 2-0 |
| 11 | Mike Maignan | France | GK | 8 | +6 | G1 starter | GK CS vs Iraq; Category A banker delivered |
| 12 | Jordan Pickford | England | GK | 8 | +6 | G1 starter | GK CS vs Ghana 0-0 |
| 13 | Pedro Porro | Spain | DEF | 6 | +6 | G1 bench | Reversed G1 DNP; started and earned full DEF CS |
| 14 | Unai Simón | Spain | GK | 8 | +6 | G1 starter | GK CS vs Saudi Arabia; Category A top pick delivered |
| 15 | Alisson Becker | Brazil | GK | 8 | +6 | G1 starter | GK CS vs Haiti; Category A banker |
| 16 | Vinícius Júnior | Brazil | FWD | 8 | +6 | G1 starter | Goal vs Haiti; G1 form carried forward |
| 17 | Thibaut Courtois | Belgium | GK | 8 | +6 | G1 starter | GK CS vs Iran despite Doku illness absence |
| 18 | Rúben Dias | Portugal | DEF | 6 | +6 | G1 bench | G1 fitness DNP reversed — started G2 and earned DEF CS |
| 19 | Marc Guéhi | England | DEF | 6 | +6 | G1 bench | G1 bench → G2 starter alongside Konsa; full DEF CS |
| 20 | Rafael Leão | Portugal | FWD | 7 | +6 | G1 sub | Sub ~86'; scored vs Uzbekistan; Neto/Leão swap confirmed |
| 21 | Koundé | France | DEF | 6 | +4 | G1 starter | DEF CS vs Iraq |
| 22 | Saliba | France | DEF | 6 | +4 | G1 starter | DEF CS vs Iraq |
| 23 | Upamecano | France | DEF | 6 | +4 | G1 starter | DEF CS vs Iraq |
| 24 | Ezri Konsa | England | DEF | 6 | +4 | G1 starter | DEF CS vs Ghana |
| 25 | Cristian Romero | Argentina | DEF | 6 | +4 | G1 starter | DEF CS vs Austria; injury concern late in match |
| 26 | Pau Cubarsí | Spain | DEF | 6 | +4 | G1 starter | DEF CS vs Saudi Arabia; confirmed every-game starter |
| 27 | Marc Cucurella | Spain | DEF | 6 | +4 | G1 starter | DEF CS vs Saudi Arabia |
| 28 | Gabriel Magalhães | Brazil | DEF | 6 | +4 | G1 starter | DEF CS vs Haiti |
| 29 | Achraf Hakimi | Morocco | DEF | 6 | +4 | G1 starter | DEF CS vs Scotland |
| 30 | Joško Gvardiol | Croatia | DEF | 6 | +4 | G1 starter | Started, subbed HT; DEF CS vs Panama 1-0 |

**Notable Δ = +3:** Ødegaard (NOR MID, 5pts, assist for Haaland 48'), Enzo Fernández (ARG MID, 3pts, MID CS), Bruno Fernandes (POR MID, 6pts +4, OG corner assist + MID CS), Felix Nmecha (GER MID, 5pts, assist vs Ivory Coast — G1 form carry), Dani Olmo (Spain FWD, 5pts, assisted Yamal's goal).

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

Twelve of the twenty-one G2 matches produced clean sheets for tracked nations:

| Match | CS Team | Tracked beneficiaries |
|-------|---------|----------------------|
| Spain vs Saudi Arabia | Spain | Simón 8pts, Porro 6pts, Cubarsí 6pts, Cucurella 6pts, Pedri 3pts, Rodri 3pts |
| Brazil vs Haiti | Brazil | Alisson 8pts, Gabriel Magalhães 6pts |
| Belgium vs Iran | Belgium | Courtois 8pts, De Bruyne 3pts |
| Morocco vs Scotland | Morocco | Hakimi 6pts |
| USA vs Australia | USA | Tillman 3pts (MID CS) |
| Ecuador vs Curaçao | Ecuador | Caicedo 3pts (MID CS) |
| France vs Iraq (3-0) | France | Maignan 8pts, Koundé/Saliba/Upamecano 6pts each, Olise 9pts (2A+MID CS), Cherki 2pts (sub+MID CS) |
| England vs Ghana (0-0) | England | Pickford 8pts, Konsa/Guéhi 6pts each, Bellingham/Rice/Anderson 3pts each |
| Argentina vs Austria (2-0) | Argentina | Martínez 8pts, Romero 6pts, Fernández 3pts |
| Portugal vs Uzbekistan (5-0) | Portugal | Nuno Mendes 12pts, Rúben Dias 6pts, Bruno Fernandes 6pts, João Neves/Vitinha 3pts each |
| Croatia vs Panama (1-0) | Croatia | Gvardiol 6pts (start + DEF CS; subbed HT) |
| Colombia vs DR Congo (1-0) | Colombia | No tracked CS earners (Díaz=FWD, no CS bonus) |

**No CS in completed G2 matches:** Germany vs Ivory Coast, Netherlands vs Sweden, Turkey vs Paraguay, Uruguay vs Cape Verde, Switzerland, Canada vs Qatar, Egypt vs New Zealand, Norway vs Senegal (Senegal scored twice).

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
| France CS vs Iraq (Maignan, Koundé, Saliba, Upamecano) | ✅ Correct — all four Category A picks delivered 6–8pts; CS bankers vindicated |
| Mbappé FRA form carry (Category B) | ✅ Correct — 14pts, 2 goals; G1 brace followed by G2 brace |
| Dembélé FRA attack depth | ✅ Correct — 11pts (1G+1A); Category B ceiling delivered |
| Olise FRA MID (Category C) | ✅ Exceeded — 9pts (2A+CS); model had ~4.44, exceeded significantly |
| Doué FRA (G1 starter → G2 sub) | 🟡 Partial — came on 66' (sub, 1pt); rotation risk wasn't flagged clearly enough |
| Kane England form carry (Category B) | ❌ Faded — 2pts +0; 0-0 draw, no goal or assist in G2 despite 14pt G1 |
| England CS vs Ghana (Pickford, Konsa, Guéhi) | ✅ CS materialised — Pickford/Konsa 6–8pts; Guéhi bonus (G1 bench → G2 starter, +6) |
| Haaland anomaly (Category B, 29% win%) | ✅ Correct call — 14pts, 2 goals vs Senegal; personal scoring rate decoupled from team win% exactly as modelled |
| Argentina CS vs Austria (Martínez, Romero) | ✅ Correct — GK CS (8pts) and DEF CS (6pts) both delivered |
| Palacios ARG (highest Pts/$, bench risk) | ✅ Correct — bench DNP again; rotation flag was justified |
| Portugal CS vs Uzbekistan (Nuno Mendes) | ✅ Exceeded — Mendes scored a free-kick (12pts, +10); Category A floor became Category B ceiling |
| Rúben Dias POR (G1 fitness DNP) | ❌ Wrong direction — model gave near-zero APP_EXP; he started and earned DEF CS (6pts, +6) |
| Leão vs Neto POR (rotation gamble) | 🟡 Correct swap predicted — Neto started (2pts), Leão sub scored (7pts); if-starts scenario played out |
| Díaz COL G1 momentum carry | ❌ Started but blanked — 2pts +0; DRC GK Mpasi made 8 saves; disallowed goal ruled out offside |
| Gvardiol CRO CS (57% win%) | ✅ Correct — started, DEF CS (6pts, +4); Croatia 1-0 Panama; Budimir sub winner |

---

## Key G2 Narratives (Completed Matches)

1. **Spain's CS wall delivered** — The pre-G2 plan's clearest structural call. Spain vs Saudi Arabia (91% win%) produced 6 tracked players earning CS bonus. Simón (8pts), Porro/Cubarsí/Cucurella (6pts each), Pedri/Rodri (3pts). Olmo assisted Yamal's goal (+3). The only disappointment: Grimaldo bench DNP again.

2. **Yamal's first WC start** — After being managed carefully in G1 (sub 71'), Yamal started G2 and scored. His 8pts (Δ=+7 from G1 sub baseline) was one of the cleaner predictions — the model had him in the Spain CS core with scoring upside.

3. **Matheus Cunha brace — the unranked 14pt bomb** — Brazil's Cunha (Adj Pts 148.6, not in top 20 predicted standouts) scored twice vs Haiti for 14pts. With Alisson's CS and Gabriel Magalhães's DEF CS also delivering, Brazil's G2 was the most productive single match for tracked players after Spain.

4. **Jonathan David's hat-trick defies the model** — The G2_OUTLOOK framework couldn't account for a "G1 sub becomes G2 starter and scores 3" scenario. David's 20pts (+19) is the G2 story. Canada's 62% G2 win probability should have been a green flag, but the APP_EXP model significantly underweighted his starting probability.

5. **Porro starts after G1 bench — Grimaldo doesn't** — The two Spain DEFs who were bench in G1 diverged sharply. Porro returned to the XI and earned a full CS (6pts, Δ=+6). Grimaldo remained on the bench (0pts, Δ=−1). In hindsight, Porro's 2024–25 club form at Tottenham should have been weighted higher.

6. **Belgium CS without Doku** — Courtois kept a clean sheet vs Iran (8pts) and De Bruyne contributed as normal (3pts, MID CS). Lukaku started (2pts, FWD no CS) but didn't score. The illness removal of Doku (rated as G1 starter, Δ=−2) was absorbed cleanly — Belgium's structure held.

7. **Morocco CS vs Scotland** — Hakimi delivered DEF CS (6pts, Δ=+4) as Scotland managed only a started-but-blanked performance from McTominay (2pts). The 65% Morocco win probability CS expectation was correct.

8. **Salah leads Egypt to historic first WC win** — Egypt 3-1 NZL (Jun 21). Salah 1G+1A (11pts, +9). Marmoush started, 2pts, Δ=0. No Egyptian CS (Surman 15').

9. **France dismantle Iraq, CS bankers deliver** — France 3-0 Iraq (Jun 22). Mbappé brace (14pts, +12); Dembélé 1G+1A (11pts, +9); Olise double-assist + MID CS (9pts, +7). All four France defenders earned DEF CS (6pts each). Cherki sub-on at 68' and got MID CS (2pts, +2). Doué sub-on at 66' but FWD CS=0 (1pt, -1). The France machine was exactly as predicted.

10. **England 0-0 Ghana — Kane silenced, CS carries the team** — The prediction on Kane's form carry was wrong (0 goals, 0 assists, Δ=0). But England's CS was the story: Pickford (8pts), Konsa (6pts), and surprise Guéhi — G1 bench → G2 starter → full DEF CS (6pts, +6). England's defensive unit overdelivered where the attack fell flat.

11. **Haaland vs Senegal — anomaly model validated** — Norway 3-2 Senegal (Jun 22). Haaland brace (14pts, +12). Ødegaard assisted the 48' goal (5pts, +3). Norway's 29% win% was irrelevant to Haaland's personal output — exactly the "personal rate decouples from team" scenario flagged in the prediction plan.

12. **Argentina CS vs Austria — defensive structure holds, Messi breaks record** — Argentina 2-0 Austria (Jun 22). Messi scored both goals (not tracked). Emiliano Martínez GK CS (8pts, +6), Romero DEF CS before injury (6pts, +4), Enzo Fernández MID CS (3pts, +1). Palacios bench DNP again — the highest Pts/$ player still has no G2 pts. Álvarez came on late (1pt, +1).

13. **Portugal explode for 5 — Nuno Mendes the standout** — Portugal 5-0 Uzbekistan (Jun 23). Rúben Dias returned from G1 fitness DNP to start and earn DEF CS (6pts, +6). Nuno Mendes scored a free-kick + DEF CS = 12pts (+10), highest DEF score of G2. Bruno Fernandes OG corner assist + MID CS (6pts, +4). Leão sub-on scored at 86' (7pts, +6). Neto started (2pts, Δ=0).

14. **Croatia grind past Panama — Gvardiol's CS on Modrić's 200th cap** — Croatia 1-0 Panama (Jun 23). Ante Budimir came off the bench at HT and scored from Stanišić's cross (54'). Gvardiol started but was the player replaced at HT by Budimir — he still collected DEF CS (played any min, +4) + start (+2) = 6pts (+4). Livaković made crucial late saves to preserve the shutout. Croatia's first WC 2026 points; Panama eliminated.

15. **Colombia 1-0 DR Congo — Muñoz beats Mpasi, Díaz goes scoreless** — Muñoz (76', deflected) was the difference after a thoroughly dominant Colombia display that DRC goalkeeper Mpasi single-handedly contained: 8 saves including Díaz twice denied (one disallowed for offside at 81'). Lucumí booked (55'). Colombia qualified on 6pts; Díaz: 2pts (+0) — strong underlying performance that produced no trackable stats, confirming the model's pattern of his form not always converting to scoreline.

---

## Summary Stats — G2 Complete (all 21 matches)

| Metric | Value |
|--------|-------|
| Highest G2 score | 20 pts (Jonathan David, hat-trick vs Qatar) |
| Joint second highest | 14 pts (Haaland, Mbappé, Matheus Cunha) |
| Biggest G2 Δ | +19 (Jonathan David) |
| Best DEF/GK single game | Nuno Mendes 12pts (goal + DEF CS vs Uzbekistan) |
| CS matches | 12 of 21 (Spain, Brazil, Belgium, Morocco, USA, Ecuador, France, England, Argentina, Portugal, Croatia, Colombia) |
| Richest single CS game | France vs Iraq — GK (8), 3×DEF (6 each), Olise MID (9), Cherki MID sub (2) |
| Biggest model miss | Jonathan David — predicted ~3pts, delivered 20pts |
| Biggest positive surprise | Nuno Mendes — predicted ~4.1pt OUTLOOK, delivered 12pts |
| Biggest G1-form carry | Haaland (+12→+12), Mbappé (+12→+12), Salah (+3→+9) |
| G1 form that faded | Kane (14pts G1 → 2pts G2), Schlotterbeck (8pts → 2pts) |
| G1 bench → G2 CS bonus | Guéhi (+6), Rúben Dias (+6), Porro (+6) |
| Injury/illness blanks | Pulisic (Δ=−2), Doku (Δ=−2) |
| Rotation surprises | Porro returned to XI; Grimaldo DNP twice; Palacios bench both games |
| Prediction model hit rate | 13 ✅, 5 ❌, 3 🟡 partial out of 21 assessed |

---

## G2 Final Results — Colombia and Croatia

| Match | Result | Key tracked player | G2 Pts | G2 Δ |
|-------|--------|-------------------|-------:|-----:|
| Colombia vs DR Congo | **1-0** (Muñoz 76') | Díaz (FWD, started) | 2 | +0 |
| Croatia vs Panama | **1-0** (Budimir 54' sub) | Gvardiol (DEF, started/HT off) | 6 | +4 |

Colombia qualified with 6pts. Croatia earned their first WC 2026 points (3pts total). Both advance with G3 still to come.
