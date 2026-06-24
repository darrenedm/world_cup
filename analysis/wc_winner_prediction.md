# World Cup 2026 Winner Prediction
*Written Jun 23 2026, updated Jun 24 — after G1+G2, before G3 (Jun 24–27)*
*All 21 G2 matches complete: Colombia 1-0 DR Congo (Muñoz 76'), Croatia 1-0 Panama (Budimir 54')*

---

## Methodology

### Step 1 — Team Form Score (0–10)

Computed from G1+G2 data across five components (2 pts each):

| Component | 2.0 | 1.5 | 1.0 | 0.5 |
|-----------|-----|-----|-----|-----|
| Group points | 6 | 4 | 3 | 0–1 |
| Goals scored/game | 3+ | 2–3 | 1–2 | <1 |
| Goals conceded/game | 0 | 0–0.5 | 0.5–1 | 1.5+ |
| Star player Δ (avg top 3) | ≥+9 | +6–+9 | +3–+6 | 0–+3 |
| Consistency | 2W | 1W1D | 1W1L | 0W |

### Step 2 — Pre-Tournament Baseline (0–10)

Squad quality prior derived from FIFA rankings, squad depth, and pre-tournament Win% data from the model. France and Argentina anchored at 9.0 and 8.5 respectively based on pre-WC market consensus.

### Step 3 — Blended Rating

```
Blended Rating = 0.6 × Form Score + 0.4 × Pre-Tournament Baseline
```

60% weight to observed tournament form, 40% to prior quality. This stops an inflated G1 scoreline (e.g. Germany 7-1 Curaçao) from fully overriding squad quality.

### Step 4 — Match Win Probability

Logistic model: `P(A beats B) = 1 / (1 + exp(-0.5 × (Ra − Rb)))`

Where Ra, Rb are the Blended Ratings. At equal ratings this gives 50/50. A 2-point rating gap gives ~73/27. A 4-point gap gives ~88/12.

### Step 5 — Tournament Path

Each team's most likely bracket opponents are identified round by round. P(wins tournament) = product of P(qualify) × P(win each round) using expected opponents at each stage.

---

## Group Reference

| Group | Teams | Key tracked nations |
|-------|-------|---------------------|
| A | Mexico, South Africa, South Korea, Czech Republic | — |
| B | Canada, Bosnia, Qatar, Switzerland | Canada |
| C | **Brazil**, **Morocco**, Haiti, **Scotland** | Brazil, Morocco |
| D | **USA**, Paraguay, Australia, Turkey | USA, Turkey |
| E | **Germany**, **Ivory Coast**, Ecuador, Curaçao | Germany, CIV |
| F | **Netherlands**, Japan, **Sweden**, Tunisia | Netherlands, Sweden |
| G | **Belgium**, **Egypt**, Iran, New Zealand | Belgium, Egypt |
| H | **Spain**, Cape Verde, Saudi Arabia, **Uruguay** | Spain |
| I | **France**, **Norway**, Senegal, Iraq | France, Norway |
| J | **Argentina**, Algeria, Austria, Jordan | Argentina |
| K | **Portugal**, **Colombia**, DR Congo, Uzbekistan | Portugal, Colombia |
| L | **England**, **Croatia**, Ghana, Panama | England, Croatia |

---

## Team Form Ratings

| Team | Pts | GF/g | GA/g | Star Δ | Consistency | **Form** | Pre-WC | **Blended** |
|------|-----|------|------|--------|-------------|---------|--------|------------|
| France | 6 | 3.0 (3-1, 3-0) | 0.5 | +9.3 (Mbappé/Dembélé/Olise) | 2W | **9.5** | 9.0 | **9.30** |
| Argentina | 6 | 2.5 (3-0, 2-0) | 0.0 | +6.0 (Martínez/Romero) | 2W | **9.0** | 8.5 | **8.80** |
| Portugal | 4 | 3.0 (1-1, 5-0) | 0.5 | +7.3 (Mendes/Dias/Leão) | 1D1W | **8.0** | 7.5 | **7.80** |
| Netherlands | 6 | 2.5 (est.) | 0.5 (est.) | +4.0 (limited data) | 2W | **8.0** | 7.5 | **7.80** |
| Germany | 6 | 4.0 (7-1⚠️, 3-1) | 1.0 | +5.0 (Nmecha/Schlotterbeck) | 2W | **7.5** | 8.0 | **7.70** |
| Brazil | 4 | 2.0 (1-1, 3-0) | 0.5 | +5.0 (Vinícius/Raphinha) | 1D1W | **7.0** | 8.5 | **7.60** |
| Colombia | 6 | 2.0 | 0.5 | +4.5 (Díaz G1 +9, G2 +0) | 2W | **7.0** | 6.5 | **6.90** |
| Spain | 4 | 1.0 (0-0, 2-0) | 0.2 | +5.7 (Simón/Yamal/Cubarsí) | 1D1W | **6.7** | 8.0 | **7.22** |
| England | 4 | 2.0 (4-2, 0-0) | 1.0 | +4.3 (Kane peak/Guéhi) | 1W1D | **6.5** | 8.0 | **7.10** |
| Norway | 6 | 3.0 (4-1, 2-1) | 1.0 | +9.0 (Haaland ×2 games) | 2W | **9.0** | 4.0 | **7.00** |
| Belgium | 4 | 1.5 (1-1, 2-0) | 0.8 | +3.5 (Courtois/De Bruyne) | 1D1W | **6.4** | 7.0 | **6.64** |
| Morocco | 4 | 1.3 (1-1, 1-0) | 0.8 | +3.0 (Hakimi) | 1D1W | **6.4** | 7.0 | **6.64** |
| Egypt | 4 | 2.0 (1-1, 3-1) | 1.0 | +5.0 (Salah +9 G2) | 1D1W | **7.0** | 5.0 | **6.20** |
| USA | ~4 | 1.5 | 1.0 | +2.0 | 1W1D | **5.5** | 5.5 | **5.50** |
| Mexico | ~4 | 1.5 | 1.0 | moderate | 1W1D | **5.5** | 5.5 | **5.50** |
| Canada | 3–4† | 2.5 (David hat-trick) | 1.5 | +8.0 (David) | 1W+ | **6.5** | 4.5 | **5.70** |
| Croatia | 3 | 0.5 (0-4, 1-0) | 2.0 | +2.0 (Gvardiol +4 G2) | 1L1W | **3.8** | 6.0 | **4.68** |

*† Canada David hat-trick inflates form.*  
*⚠️ Germany's 7-1 was vs Curaçao — quality-adjusted down from raw GF score.*

---

## Bracket Structure — R32 through Final

*(From Wikipedia 2026 FIFA World Cup knockout stage; pre-set bracket locks Jun 27)*

### Round of 32 Matchups

| Match | Fixture | Key tracked teams |
|-------|---------|------------------|
| M73 | RU-A vs RU-B | — |
| M74 | **W-E (Germany)** vs 3rd best A/B/C/D/F | Germany |
| M75 | **W-F (Netherlands)** vs RU-C (**Morocco** likely) | Netherlands, Morocco |
| M76 | **W-C (Brazil)** vs RU-F (Japan/Sweden) | Brazil |
| M77 | **W-I (France** or Norway**)** vs 3rd best C/D/F/G/H | France |
| M78 | RU-E (CIV/Ecuador) vs **RU-I (Norway** or France**)** | Norway |
| M79 | Mexico vs 3rd best C/E/F/H/I | Mexico |
| M80 | **W-L (England)** vs 3rd best E/H/I/J/K | England |
| M81 | **USA** vs 3rd best B/E/F/I/J | USA |
| M82 | **W-G (Belgium)** vs 3rd best A/E/H/I/J | Belgium |
| M83 | **RU-K** (Colombia or Portugal) vs **RU-L** (Croatia or England) | Colombia/Portugal/Croatia |
| M84 | **W-H (Spain)** vs RU-J (Algeria/Jordan) | Spain |
| M85 | W-B (Canada/Switzerland) vs 3rd best E/F/G/I/J | Canada |
| M86 | **Argentina** vs RU-H (Uruguay/Cape Verde) | Argentina |
| M87 | **W-K (Portugal** or Colombia**)** vs 3rd best D/E/I/J/L | Portugal/Colombia |
| M88 | RU-D (USA/Turkey) vs **RU-G (Egypt** or Belgium**)** | Egypt |

### Round of 16 through Final

```
R32                      R16              QF              SF           Final

M74 (Germany)    ─┐
                  ├── M89 ──┐
M77 (France)     ─┘         │
                             ├── M97 ──┐
M73 (RU-A/B)     ─┐         │         │
                  ├── M90 ──┘         │
M75 (Netherlands)─┘                   ├── M101 ──┐
                                       │           │
M76 (Brazil)     ─┐                   │           │        FINAL
                  ├── M91 ──┐         │           ├──────  M104
M78 (Norway)     ─┘         │         │           │
                             ├── M99 ──┘           │
M79 (Mexico)     ─┐         │                     │
                  ├── M92 ──┘                     │
M80 (England)    ─┘                               │
                                                   │
M83 (RU-K/L)     ─┐                               │
                  ├── M93 ──┐                     │
M84 (Spain)      ─┘         │                     │
                             ├── M98 ──┐           │
M81 (USA)        ─┐         │         │           │
                  ├── M94 ──┘         ├── M102 ──┘
M82 (Belgium)    ─┘                   │
                                       │
M86 (Argentina)  ─┐                   │
                  ├── M95 ──┐         │
M88 (Egypt/USA)  ─┘         │         │
                             ├── M100 ─┘
M85 (Canada)     ─┐         │
                  ├── M96 ──┘
M87 (Portugal)   ─┘
```

---

## The Two Halves — A Stark Contrast

### SF M101 Half — "The European Gauntlet"

**Occupants:** France, Germany, Netherlands, Spain, Belgium, (USA)

This half is heavily weighted towards European sides. The key early collision is **France vs Germany in R16 (M89)** — if both win their groups and advance, the tournament's two best-form European teams eliminate each other before the quarter-finals. The Netherlands have a softer path (Morocco in R32, weak RU-A/B in R16) before potentially meeting France or Germany in QF M97. Spain can navigate to the SF without facing any of France/Germany/Netherlands until the SF itself.

**Key R16 clash:** France (9.30) vs Germany (7.70) — M89

### SF M102 Half — "The Death Bracket"

**Occupants:** Brazil, England, Norway (if France wins Group I), Argentina, Portugal, Colombia, Canada

This is the most brutally stacked half of any World Cup since 2014. Every top-10 blended-rated non-European nation ends up here:

- **Brazil vs Norway** in R16 (M91) — two teams both boasting 4+ goals/game
- **England vs Mexico** in R16 (M92) — England's most winnable path, but Mexico is the host
- **Argentina vs Egypt/Belgium RU** in R16 (M95) — Argentina's most beatable early opponent
- **Portugal vs Canada** in R16 (M96) — David's form makes Canada dangerous
- **Brazil vs England** in QF M99 — potential classic
- **Argentina vs Portugal** in QF M100 — the tie of the tournament

Then SF M102 could produce **Brazil vs Argentina** — a South American semifinal.

**Key structural note:** France and England are confirmed in opposite halves (cannot meet before the Final). Spain and Argentina are also confirmed in opposite halves.

---

## Path Analysis — Top Contenders

### France (9.30) — Favourite

| Round | Likely opponent | P(win) |
|-------|----------------|--------|
| R32 M77 | 3rd place (~6.0) | 0.84 |
| R16 M89 | **Germany (7.70)** | 0.69 |
| QF M97 | Netherlands (7.80) | 0.68 |
| SF M101 | Spain (7.22) | 0.74 |
| Final M104 | Argentina (8.80) | 0.56 |
| **P(Champion)** | | **~16%** |

France's biggest threat is a potential France vs Germany R16 match — a winnable but far-from-certain 69% proposition. If they survive Germany, Netherlands in QF is another tough assignment. The Final most likely pits them against Argentina.

**Key risk:** Germany in R16 before the quarter-finals.

---

### Argentina (8.80) — Co-favourite

| Round | Likely opponent | P(win) |
|-------|----------------|--------|
| R32 M86 | RU-H (Uruguay ~5.5) | 0.84 |
| R16 M95 | RU-G (Egypt 6.20) | 0.79 |
| QF M100 | **Portugal (7.80)** | 0.62 |
| SF M102 | Brazil (7.60) or England (7.10) | 0.65 |
| Final M104 | France (9.30) | 0.44 |
| **P(Champion)** | | **~12%** |

Argentina's path through the Death Bracket is actually easier in the early rounds than the bracket's reputation suggests. Their R32 opponent is a Group H runner-up (Uruguay or similar) and R16 is likely Egypt — both very beatable. The real tests start in QF (Portugal) and SF (Brazil/England). The Final against France is the hardest match in the tournament at 44%.

**Key risk:** Portugal in QF M100. If Nuno Mendes and Leão are in form, this is a genuine upset threat.

---

### Netherlands (7.80) — Dark Horse

| Round | Likely opponent | P(win) |
|-------|----------------|--------|
| R32 M75 | **Morocco (6.44)** | 0.66 |
| R16 M90 | RU-A/RU-B (~4.0) | 0.87 |
| QF M97 | France (9.30) or Germany (7.70) | 0.40 (vs France) / 0.53 (vs Germany) |
| SF M101 | Spain (7.22) | 0.57 |
| Final M104 | Argentina (8.80) | 0.47 |
| **P(Champion)** | | **~5%** |

Netherlands have the most navigable early bracket path in the European half — Morocco in R32, then a weak RU-A or RU-B winner in R16, before the France/Germany gauntlet in QF. Their QF match probability depends entirely on who comes through M89 (France vs Germany). If Germany knocks out France, Netherlands are a genuine SF contender.

**Key upside:** If Germany beats France in R16, Netherlands avoid their toughest matchup until the SF.

---

### Portugal (7.80) — Sleeper

| Round | Likely opponent | P(win) |
|-------|----------------|--------|
| R32 M87 | 3rd best (~4.5) | 0.84 |
| R16 M96 | Canada (5.70) | 0.79 |
| QF M100 | **Argentina (8.80)** | 0.38 |
| SF M102 | Brazil (7.60) or England (7.10) | 0.53 |
| Final M104 | France (9.30) | 0.32 |
| **P(Champion)** | | **~4%** |

Portugal's first two rounds are very manageable (3rd-place team, then Canada). The QF wall is Argentina — a 38% proposition. Portugal's biggest form signal is Nuno Mendes (12pts in G2, free-kick goal + DEF CS), making them more dangerous than a cold pre-tournament read would suggest. Rúben Dias returning from G1 absence is a huge boost. If they can topple Argentina, they're live threats to the end.

**Key risk:** Argentina in QF M100 — the most likely early elimination point.

---

### Germany (7.70) — Bracket Casualty Risk

| Round | Likely opponent | P(win) |
|-------|----------------|--------|
| R32 M74 | 3rd best A/B/C/D/F (~3.5) | 0.89 |
| R16 M89 | **France (9.30)** | 0.31 |
| QF M97 | Netherlands (7.80) | 0.47 |
| SF M101 | Spain (7.22) | 0.62 |
| Final M104 | Argentina (8.80) | 0.37 |
| **P(Champion)** | | **~3%** |

Germany's Blended Rating (7.70) is strong but they are bracket-poisoned. Their 7-1 G1 win (vs Curaçao) inflates their goal tally and their path immediately produces France in R16. The probability of Germany winning the tournament is dragged down primarily by that single 31% R16 match. If they somehow beat France, they have legitimate QF and SF paths. But at 31% probability, they're very unlikely to navigate it.

**Key upside:** If France surprisingly rotates for G3 (vs Norway) and suffers fatigue or injury, Germany's R16 draw could be a slightly diminished French side.

---

### Brazil (7.60) — Underperforming Pre-Tournament Expectations

| Round | Likely opponent | P(win) |
|-------|----------------|--------|
| R32 M76 | RU-F (Japan/Sweden ~4.5) | 0.81 |
| R16 M91 | **Norway (7.00)** | 0.58 |
| QF M99 | **England (7.10)** | 0.56 |
| SF M102 | **Argentina (8.80)** | 0.35 |
| Final M104 | France (9.30) | 0.30 |
| **P(Champion)** | | **~3%** |

Brazil's pre-tournament rating (8.5) drops in the blended model because their G1+G2 form was inconsistent (drew Morocco 1-1 in G1, needed to beat Haiti to get 4pts). Pre-tournament they were co-favourites with France and Argentina; their tournament form pushes them down to 7.60. The Death Bracket compound: Norway (R16), England (QF), Argentina (SF), France (Final) is four successive high-quality opponents.

**Key risk:** The path is demanding from Round 1. They need Vinícius and Raphinha performing consistently across 5 matches after a mixed group stage.

---

### Spain (7.22) — Reasonable Path, Wrong Half

| Round | Likely opponent | P(win) |
|-------|----------------|--------|
| R32 M84 | RU-J (Algeria ~4.0) | 0.83 |
| R16 M93 | Colombia/Portugal RU or Croatia (~6.0 avg) | 0.57 |
| QF M98 | **Belgium (6.64) or USA (5.50)** | 0.57 |
| SF M101 | France (9.30) or Germany (7.70) | 0.26 (vs France) |
| Final M104 | Argentina (8.80) | 0.34 |
| **P(Champion)** | | **~2%** |

Spain's group stage form has been uninspiring (0-0 vs Cape Verde in G1, won Saudi Arabia G2) which depresses their Form Score despite a high Pre-WC baseline. Their bracket path to the QF is manageable — RU-J is likely Jordan or Algeria, and R16 could be Colombia/Portugal RU or Croatia. The SF is where Spain meets France or Germany — and if France is alive, Spain's SF probability is just 26%. The bracket seeding confirms Spain and Argentina cannot meet before the Final, which is a slight silver lining.

---

### England (7.10) — Worst Bracket Draw

| Round | Likely opponent | P(win) |
|-------|----------------|--------|
| R32 M80 | 3rd best E/H/I/J/K (~5.5) | 0.69 |
| R16 M92 | **Mexico (5.50)** | 0.69 |
| QF M99 | **Brazil (7.60)** | 0.44 |
| SF M102 | **Argentina (8.80)** | 0.30 |
| Final M104 | France (9.30) | 0.27 |
| **P(Champion)** | | **~2%** |

England's group stage form (4-2 win, 0-0 draw) is inconsistent. Kane blanked in G2 after his G1 brace — a concern. The bracket gives England one of the toughest paths in the tournament: Mexico (R16), Brazil (QF), Argentina (SF), France (Final). Every round from QF onwards is a match England would likely lose on the pre-tournament market. The bracket seeding means England and France cannot meet before the Final — small comfort given the death bracket.

**Key upside:** Kane is the world's best penalty-taker and England could win ugly through a knockout-stage run.

---

### Norway (7.00) — Exceptional Form, Brutal Draw

| Round | Likely opponent | P(win) |
|-------|----------------|--------|
| R32 M78 | RU-E (CIV ~5.5) | 0.68 |
| R16 M91 | **Brazil (7.60)** | 0.43 |
| QF M99 | **England (7.10)** | 0.48 |
| SF M102 | **Argentina (8.80)** | 0.29 |
| Final M104 | France (9.30) | 0.26 |
| **P(Champion)** | | **~1%** |

Norway's 1% probability is the clearest example of great form meeting a brutal bracket. As RU-I (if France wins Group I in G3), Norway falls straight into the Death Bracket facing Brazil in R16 — a match played in the M102 path. Their Blended Rating (7.00) is genuinely competitive but every round from R16 onwards is against a higher-rated team. Haaland's personal scoring rate (4 goals in 2 games) is the only realistic route through — goals can decide individual matches regardless of team ratings. Norway is the tournament's biggest "great team, wrong half" story.

**Key upside:** Haaland in R16 vs Brazil, R32 vs CIV. He can personally override team-level ratings. Norway are dangerous in every individual match.

---

## Outright Winner Probability Table

| Rank | Team | Blended Rating | Half | Path Risk | **P(Champion)** |
|------|------|---------------|------|-----------|----------------|
| 1 | **France** | 9.30 | M101 | Germany R16 | **~16%** |
| 2 | **Argentina** | 8.80 | M102 | Portugal QF | **~12%** |
| 3 | **Netherlands** | 7.80 | M101 | France QF | **~5%** |
| 4 | **Portugal** | 7.80 | M102 | Argentina QF | **~4%** |
| 5 | **Germany** | 7.70 | M101 | France R16 | **~3%** |
| 6 | **Brazil** | 7.60 | M102 | Norway R16, Argentina SF | **~3%** |
| 7 | **Spain** | 7.22 | M101 | France SF | **~2%** |
| 8 | **England** | 7.10 | M102 | Brazil QF, Argentina SF | **~2%** |
| 9 | **Colombia** | 6.90 | M102 | Argentina QF (via M100) | **~2%** |
| 10 | **Norway** | 7.00 | M102 | Brazil R16 | **~1%** |
| 11 | **Belgium** | 6.64 | M101 | France SF | **~1%** |
| 12 | **Canada** | 5.70 | M102 | Portugal R16 | **~1%** |
| 13 | **Morocco** | 6.64 | M101 | Netherlands R32 | **~1%** |
| 14 | **Egypt** | 6.20 | M102 | Argentina R16 | **~0.5%** |
| 15 | **USA** | 5.50 | M101 | Belgium R16 | **~0.5%** |
| 16 | **Mexico** | 5.50 | M102 | England R16 | **~0.5%** |
| — | All others | <5.0 | — | — | **~44%** combined |

*Probabilities are estimates from the path model, not a full Monte Carlo simulation.*

---

## Key Narratives

### 1. The Draw Created Two Unequal Halves

The M101 SF (France/Germany/Netherlands/Spain/Belgium) is top-heavy with European quality but concentrated — they eliminate each other early. The M102 SF (Brazil/England/Norway/Argentina/Portugal/Colombia) is the "World Half" where the very best teams outside Europe all collide, paradoxically depressing each other's individual win probabilities. France benefits enormously from being in the European-only half.

### 2. France's Biggest Threat Is in Round of 16

France (9.30) and Germany (7.70) are locked into a potential R16 collision in M89. France are 69% favourites, but a 31% chance Germany knocks them out in round 1 of the knockouts is real. If Mbappé is fit and in the same form (4 goals in G1+G2), France advance. But this is not the "should be a QF" tie — it's Round of 16.

### 3. Argentina Has the Best Value-Adjusted Path

Despite a lower Blended Rating than France (8.80 vs 9.30), Argentina's path probability (~12%) rivals France's (~16%) because their early bracket (Uruguay/Cape Verde R32, Egypt R16) is far more benign. They don't face a team above 6.20 until QF (Portugal). France needs to beat Germany AND Netherlands before the SF; Argentina needs to beat Uruguay AND Egypt before the QF.

### 4. Norway Are the Tournament's Great Injustice

Norway's Blended Rating (7.00) is higher than Spain's (7.22) is close. They've scored the most goals of any tracked team adjusted for opponent. Haaland has 4 goals in 2 games. Yet their tournament win probability is just 1% — because as RU-I they land in the Death Bracket facing Brazil (R16), England (QF), Argentina (SF), and France (Final). If Norway were in the M101 half, they'd be 6-8% to win the tournament. The bracket is the story, not the team.

### 5. Brazil Are Underperforming Their Pre-Tournament Market Position

Pre-tournament, Brazil sat at or near the top of most markets alongside France and Argentina. Their G1+G2 results (drew Morocco 1-1, beat Haiti) were functional but not dominant. They arrive in the knockouts as 7.60 — behind France, Argentina, Portugal, Netherlands, and Germany. Combined with the Death Bracket path (Norway R16, England QF, Argentina SF), they're a 3% shot to win — far below what the market priced them at. The Morocco draw in G1 cost them dearly.

### 6. Spain's Route to the Final Requires Beating France or Germany in the SF

Spain are in the M101 SF half. To reach the Final, they must beat France OR Germany in the SF (M101). Spain vs France in SF: 26% for Spain. Spain vs Germany in SF: 38% for Spain. Even with a decent path to the SF (Jordan/Algeria R32, then a favourable R16), the SF wall is formidable. Spain's form is below their pre-tournament baseline (0-0 vs Cape Verde in G1 drags their Form Score). They're a 2% outsider.

### 7. Portugal Are the Genuine Surprise Threat

Portugal's Blended Rating (7.80) is 4th in the tournament, boosted by a 5-0 G2 win (strong form signal) and the emergence of Nuno Mendes as an attacking DEF. They have a clean path to QF (3rd place R32, Canada R16) and then a winnable but very tough QF vs Argentina. If Portugal's peak form from G2 carries through, Nuno Mendes + Leão on the left is the best wide combination in the tournament. At 4%, Portugal represent the best EV for a non-France/Argentina bet.

### 8. The Final Will Most Likely Be France vs Argentina

Following each team's most probable path through the bracket, the Final odds heavily favour a **France vs Argentina rematch** of the 2022 WC Final. France navigating M101 (Germany, Netherlands, Spain) and Argentina navigating M102 (Egypt, Portugal, Brazil/England) produces a 56% vs 44% Final prediction at current ratings. Both teams peak in high-pressure knockout environments. The narrative writes itself: the 2022 Final rematch in front of 94,000 at MetLife.

---

## Caveats and Limitations

| Factor | Impact |
|--------|--------|
| G3 results not yet played (Jun 24–27) | Could shift group standings and bracket position |
| Díaz G2 blank (Mpasi 8 saves) | Colombia 6pts qualified; star metric slightly reduced from G1 +9 baseline |
| Argentina rotation risk (G3 vs Jordan) | Key players may arrive the knockouts with rest vs form trade-off |
| Romero injury (knee vs Austria G2) | If Romero misses R32, Argentina DEF rating drops |
| France/Norway G3 match (group decider) | Will both play full strength? Key warm-up before knockouts |
| Third-place slots | The 8 best 3rd-place teams' specific bracket slots depend on which groups they come from — affects "3rd best" R32 matchups |
| Model is single-path, not Monte Carlo | Full simulation would produce wider probability distributions; these are median-path estimates |
