# World Cup 2026 — Country Group Stage Odds
*Analysis as of May 12, 2026 | Groups drawn December 5, 2025 (Kennedy Center, Washington D.C.)*
*Sources: FIFA Rankings (April 2026 official points, November 2025 seeding ranks), Wikipedia group pages*

---

## Methodology

### Strength Score (1–10 scale)
Base score derived from **April 2026 FIFA points** (top 20 teams sourced directly; remaining teams interpolated from November 2025 ordinal rankings using the points curve). Normalised to 1–10 scale:

`score = ((FIFA_points − 1290) / (1877 − 1290)) × 9 + 1`

A **form modifier (±0.5 max)** is applied based on:
- World Cup qualifying campaign dominance / struggle
- Nations League / recent competitive results (Sep 2024–May 2026)
- Key squad injury concerns going into the tournament

### Pairwise Match Probability
Bradley-Terry model on strength scores. Draw probability increases as teams approach equal strength.

| Strength ratio (stronger/weaker) | P(strong wins) | P(draw) | P(weak wins) |
|----------------------------------|---------------|---------|-------------|
| < 1.15 (near-equal) | 0.37 | 0.28 | 0.35 |
| 1.15 – 1.40 | 0.45 | 0.26 | 0.29 |
| 1.40 – 1.70 | 0.52 | 0.24 | 0.24 |
| 1.70 – 2.20 | 0.60 | 0.22 | 0.18 |
| 2.20 – 3.00 | 0.67 | 0.18 | 0.15 |
| 3.00 – 4.50 | 0.73 | 0.15 | 0.12 |
| 4.50+ | 0.80 | 0.12 | 0.08 |

Expected points per team = Σ over 3 opponents of `3 × P(win) + 1 × P(draw)`

### Finishing Probability Conversion
Expected points gaps converted to finishing probabilities using a sigmoid-style heuristic calibrated on historical WC group stage outcomes. **P(Dead Rubber G3)** = probability the team's group outcome (advance/eliminate AND final position) is already determined before game 3, meaning the manager can rotate freely.

---

## All Team Strength Scores

| Team | FIFA Rank (Nov 2025) | April 2026 Points | Base Score | Form Adj | **Final Score** | Form Notes |
|------|---------------------|------------------|-----------|---------|----------------|-----------|
| France | 3 | 1877.32 | 10.0 | +0.0 | **10.0** | Dominant Nations League; full squad depth |
| Argentina | 2 | 1874.81 | 9.97 | +0.0 | **10.0** | Defending WC holders; CONMEBOL qualifying won comfortably |
| Spain | 1 | 1876.40 | 9.98 | −0.3 | **9.7** | Rodri groin injury (May 2026) — Spain's biggest WC concern |
| England | 4 | 1825.97 | 9.22 | +0.1 | **9.3** | Tuchel era solid; Bellingham fitness resolved |
| Portugal | 6 | 1763.83 | 8.27 | +0.3 | **8.6** | Won Nations League Jun 2025; Bruno + Vitinha in form |
| Morocco | 8 | 1755.87 | 8.15 | +0.2 | **8.3** | Strong CAF qualifying; defensively elite; Hakimi fitness TBC |
| Netherlands | 7 | 1757.87 | 8.17 | +0.0 | **8.2** | Steady but no standout recent form signal |
| Germany | 10 | 1730.37 | 7.75 | +0.15 | **7.9** | Qualified as UEFA Group A winners; strong squad depth |
| Brazil | 5 | 1761.16 | 8.23 | −0.3 | **7.9** | CONMEBOL qualifying struggles (finished 5th); recent tournament exits |
| Belgium | 9 | 1734.71 | 7.83 | −0.2 | **7.6** | Aging core; Courtois injury concern; De Bruyne at 34 |
| Croatia | 11 | 1717.07 | 7.55 | −0.2 | **7.4** | Modric at 40; transitional generation; past their peak |
| Colombia | 13 | 1693.09 | 7.18 | +0.1 | **7.3** | Caicedo-led CONMEBOL campaign solid; Luis Díaz in best-ever form |
| Senegal | 14 | 1688.99 | 7.11 | +0.0 | **7.1** | AFCON 2023 holders; strong squad |
| Mexico | 15 | 1681.03 | 7.00 | +0.1 | **7.1** | Home advantage (co-host); CONCACAF form solid |
| USA | 16 | 1673.13 | 6.87 | +0.2 | **7.1** | Co-host home boost; Pulisic captain; improved squad depth |
| Uruguay | 17 | 1673.07 | 6.87 | +0.1 | **7.0** | Valverde generation emerging; CONMEBOL decent |
| Japan | 18 | 1660.43 | 6.67 | +0.1 | **6.8** | AFC qualifiers dominant; tactically excellent |
| Switzerland | 19 | 1649.40 | 6.51 | +0.0 | **6.5** | Kobel-led qualifying; solid ceiling |
| South Korea | 22 | ~1610 | 5.90 | +0.0 | **5.9** | Consistent AFC performer |
| Austria | 24 | ~1600 | 5.75 | +0.1 | **5.9** | UEFA qualifier; decent recent form |
| Ecuador | 23 | ~1605 | 5.83 | +0.0 | **5.8** | Caicedo anchored CONMEBOL run |
| Turkey | 25 | ~1595 | 5.68 | +0.1 | **5.8** | UEFA playoff winners; Güler & Çalhanoğlu fitness concerns offset |
| Australia | 26 | ~1590 | 5.60 | +0.0 | **5.6** | AFC qualifier; steady |
| Canada | 27 | ~1585 | 5.53 | +0.15 | **5.7** | Co-host home boost; Jonathan David-led attack |
| Iran | 20 | ~1580 | 5.38 | +0.1 | **5.5** | AFC Group A winners; well-organised defensively |
| Norway | 29 | ~1575 | 5.38 | −0.1 | **5.3** | Haaland-dependent; inconsistent without him in form |
| Panama | 30 | ~1570 | 5.30 | +0.0 | **5.3** | CONCACAF qualifier; limited ceiling |
| Scotland | 36 | ~1540 | 4.84 | +0.2 | **5.0** | McTominay heroics; surprising qualification; punching above ranking |
| Egypt | 34 | ~1550 | 5.00 | +0.0 | **5.0** | Salah-dependent; CAF qualifier |
| Algeria | 35 | ~1545 | 4.92 | +0.0 | **4.9** | CAF qualifier; decent squad |
| Paraguay | 39 | ~1525 | 4.61 | +0.0 | **4.6** | CONMEBOL survivor |
| Tunisia | 40 | ~1520 | 4.53 | +0.0 | **4.5** | CAF qualifier |
| Ivory Coast | 42 | ~1510 | 4.38 | +0.0 | **4.4** | CAF qualifier; Amad Diallo key player |
| Sweden | 43 | ~1505 | 4.30 | +0.1 | **4.4** | UEFA playoff winners; Gyökeres + Isak dangerous |
| Czech Republic | 44 | ~1500 | 4.23 | +0.1 | **4.3** | Beat Denmark in playoff; some recent form |
| Uzbekistan | 50 | ~1470 | 3.77 | +0.1 | **3.9** | First WC; AFC qualifier |
| Qatar | 51 | ~1465 | 3.69 | +0.0 | **3.7** | Host nation 2022; limited quality |
| DR Congo | 56 | ~1440 | 3.31 | +0.0 | **3.3** | Inter-confederation playoff winners |
| Iraq | 58 | ~1430 | 3.16 | +0.0 | **3.2** | AFC qualifier |
| Saudi Arabia | 60 | ~1420 | 3.00 | +0.0 | **3.0** | AFC qualifier; limited WC pedigree |
| South Africa | 61 | ~1415 | 2.93 | +0.0 | **2.9** | CAF qualifier |
| Jordan | 66 | ~1390 | 2.54 | +0.0 | **2.5** | AFC qualifier |
| Cape Verde | 68 | ~1380 | 2.38 | +0.1 | **2.5** | First WC appearance |
| Bosnia | 71 | ~1365 | 2.15 | +0.0 | **2.2** | UEFA playoff qualifier |
| Ghana | 72 | ~1360 | 2.08 | +0.0 | **2.1** | CAF qualifier; Kudus key |
| Curaçao | 82 | ~1310 | 1.31 | +0.0 | **1.3** | CONCACAF qualifier; first major WC appearance |
| Haiti | 84 | ~1300 | 1.15 | +0.0 | **1.2** | CONCACAF qualifier |
| New Zealand | 86 | ~1290 | 1.00 | +0.0 | **1.0** | OFC qualifier |

---

## Group-by-Group Analysis

---

### GROUP A — Mexico, South Korea, Czech Republic, South Africa

| Team | FIFA Rank | Strength | E[Pts] | P(1st) | P(2nd) | P(Advance) | P(Eliminated) | P(Dead Rubber G3) |
|------|-----------|---------|--------|--------|--------|------------|--------------|------------------|
| **Mexico** | 15 | 7.1 | 5.60 | **55%** | 32% | **87%** | 13% | ~40% |
| **South Korea** | 22 | 5.9 | 4.76 | 30% | **45%** | **75%** | 25% | ~20% |
| Czech Republic | 44 | 4.3 | 3.89 | 13% | 20% | 33% | **67%** | ~10% |
| South Africa | 61 | 2.9 | 2.35 | 2% | 3% | 5% | **95%** | ~5% |

**Read:** Mexico is the clear group favorite but S.Korea (0.84 pts behind in expected) makes this a real contest. Czech could sneak 2nd if both Mexico and S.Korea stumble. S.Africa has almost no path.

**Key watchlist players:** Mexico (none on our list) — *note: this group has no players from our 139-player watchlist*

---

### GROUP B — Switzerland, Canada, Qatar, Bosnia

| Team | FIFA Rank | Strength | E[Pts] | P(1st) | P(2nd) | P(Advance) | P(Eliminated) | P(Dead Rubber G3) |
|------|-----------|---------|--------|--------|--------|------------|--------------|------------------|
| **Switzerland** | 17 | 6.5 | 5.63 | **47%** | 40% | **87%** | 13% | ~20% |
| **Canada** | 27 | 5.7 | 5.29 | 43% | **40%** | **83%** | 17% | ~20% |
| Qatar | 51 | 3.7 | 3.52 | 9% | 16% | 25% | **75%** | ~10% |
| Bosnia | 71 | 2.2 | 2.22 | 1% | 4% | 5% | **95%** | ~5% |

**Read:** This is the tightest group for the top-2 battle — Switzerland (6.5) vs Canada (5.7) is very close, gap of only 0.34 expected points. Either team could win the group. Qatar has an outside shot at 2nd if both collapse. No dead rubbers here; every game matters for Switzerland and Canada.

**Key watchlist players:** Switzerland (Kobel, Gregor), Canada (Jonathan David)

---

### GROUP C — Brazil, Morocco, Haiti, Scotland

| Team | FIFA Rank | Strength | E[Pts] | P(1st) | P(2nd) | P(Advance) | P(Eliminated) | P(Dead Rubber G3) |
|------|-----------|---------|--------|--------|--------|------------|--------------|------------------|
| **Morocco** | 11 | 8.3 | 5.71 | **43%** | 41% | **84%** | 16% | ~20% |
| **Brazil** | 5 | 7.9 | 5.65 | 42% | **41%** | **83%** | 17% | ~20% |
| **Scotland** | 36 | 5.0 | 4.26 | 14% | 16% | **40%** | **60%** | ~10% |
| Haiti | 84 | 1.2 | 1.23 | 1% | 2% | 3% | **97%** | ~5% |

**Read:** The standout group of the tournament. Morocco's form boost (8.3) edges past Brazil's adjusted score (7.9 after −0.3 for qualifying struggles), making this a coin-flip for 1st — effectively 43%/42%. Scotland are genuine dark-horse for 2nd (McTominay generation, 14% to win the group). Haiti are makeweights. No dead rubbers in this group at all — Brazil and Morocco will be fighting to the wire. Scotland's overall P(advance) rises to 40% with the third-place route factored in.

**Key watchlist players:** Brazil (Gabriel, Alisson, Vinícius, Raphinha, Rodrygo, Endrick candidates), Morocco (Hakimi, En-Nesyri candidates), Scotland (McTominay)

---

### GROUP D — United States, Turkey, Australia, Paraguay

| Team | FIFA Rank | Strength | E[Pts] | P(1st) | P(2nd) | P(Advance) | P(Eliminated) | P(Dead Rubber G3) |
|------|-----------|---------|--------|--------|--------|------------|--------------|------------------|
| **USA** | 14 | 7.1 | 5.02 | **62%** | 25% | **87%** | 13% | ~45% |
| **Turkey** | 25 | 5.8 | 4.10 | 19% | **37%** | 56% | **44%** | ~15% |
| **Australia** | 26 | 5.6 | 4.10 | 17% | 36% | 53% | **47%** | ~15% |
| Paraguay | 39 | 4.6 | 3.22 | 2% | 2% | 4% | **96%** | ~5% |

**Read:** USA's home advantage pushes them to clear group favorites. Turkey and Australia are near-identical in strength (5.8 vs 5.6) making 2nd place a coin-flip between them. Paraguay have almost no path. USA likely have a dead rubber game 3 — high probability (~45%) they've already clinched 1st by then.

**Key watchlist players:** USA (Pulisic, Tillman, Weah), Turkey (Güler, Çalhanoğlu, Yıldız)

---

### GROUP E — Germany, Ecuador, Ivory Coast, Curaçao

| Team | FIFA Rank | Strength | E[Pts] | P(1st) | P(2nd) | P(Advance) | P(Eliminated) | P(Dead Rubber G3) |
|------|-----------|---------|--------|--------|--------|------------|--------------|------------------|
| **Germany** | 9 | 7.9 | 6.15 | **78%** | 17% | **95%** | 5% | ~60% |
| **Ecuador** | 23 | 5.8 | 5.08 | 16% | **50%** | 66% | **34%** | ~20% |
| **Ivory Coast** | 42 | 4.4 | 4.23 | 5% | 29% | **44%** | **56%** | ~10% |
| Curaçao | 82 | 1.3 | 1.38 | 1% | 4% | 5% | **95%** | ~5% |

**Read:** Germany has the highest expected points of any team across all groups (6.15). They are near-certain to advance and very likely to win the group. Curaçao are outclassed. The interesting battle is Ecuador vs Ivory Coast for 2nd — Ecuador (50% to finish 2nd) are modest favorites, but Ivory Coast (Amad Diallo) make it competitive. Germany's game 3 is likely a dead rubber with ~60% probability. Ivory Coast's overall P(advance) rises to 44% once the third-place route is factored in.

**Key watchlist players:** Germany (Kimmich, Wirtz, Tah, Schlotterbeck, Mittelstädt, Burkardt, Woltemade), Ecuador (Caicedo), Ivory Coast (Amad Diallo)

---

### GROUP F — Netherlands, Japan, Tunisia, Sweden

| Team | FIFA Rank | Strength | E[Pts] | P(1st) | P(2nd) | P(Advance) | P(Eliminated) | P(Dead Rubber G3) |
|------|-----------|---------|--------|--------|--------|------------|--------------|------------------|
| **Netherlands** | 7 | 8.2 | 5.65 | **72%** | 22% | **94%** | 6% | ~55% |
| **Japan** | 18 | 6.8 | 4.73 | 22% | **55%** | 77% | **23%** | ~20% |
| Tunisia | 40 | 4.5 | 3.08 | 3% | 12% | 15% | **85%** | ~10% |
| **Sweden** | 43 | 4.4 | 3.08 | 3% | 11% | **20%** | **80%** | ~10% |

**Read:** Netherlands are heavy group favorites (94% P(advance)). Japan are comfortable 2nd most likely. Tunisia and Sweden are near-identical (both 4.4–4.5) and face an uphill battle. For Sweden, Gyökeres and Isak need a near-perfect campaign just to reach the knockouts. Netherlands' game 3 is very likely a dead rubber. Sweden's overall P(advance) rises to 20% once the third-place route is included.

**Key watchlist players:** Netherlands (Van Dijk, Dumfries, Gravenberch, Timber), Sweden (Gyökeres, Isak, Svensson)

---

### GROUP G — Belgium, Iran, Egypt, New Zealand

| Team | FIFA Rank | Strength | E[Pts] | P(1st) | P(2nd) | P(Advance) | P(Eliminated) | P(Dead Rubber G3) |
|------|-----------|---------|--------|--------|--------|------------|--------------|------------------|
| **Belgium** | 8 | 7.6 | 5.93 | **70%** | 22% | **92%** | 8% | ~50% |
| **Iran** | 20 | 5.5 | 5.07 | 19% | **44%** | 63% | **37%** | ~15% |
| **Egypt** | 34 | 5.0 | 4.78 | 10% | 33% | **58%** | **42%** | ~10% |
| New Zealand | 86 | 1.0 | 1.08 | 1% | 1% | 2% | **98%** | ~5% |

**Read:** Belgium are clear favorites but this group is trickier than it looks — Iran (ranked 20th) are a genuine 2nd-place threat, and Egypt (Salah) are not far behind. The Iran vs Egypt match will be a real contest for 2nd. Belgium likely have a dead rubber game 3. Egypt's P(advance) bumped to 58% once the 8-of-12 third-place route is included.

**Key watchlist players:** Belgium (Courtois, Thibaut, De Bruyne, Doku, Lukaku?), Egypt (Salah, Marmoush)

---

### GROUP H — Spain, Uruguay, Saudi Arabia, Cape Verde

| Team | FIFA Rank | Strength | E[Pts] | P(1st) | P(2nd) | P(Advance) | P(Eliminated) | P(Dead Rubber G3) |
|------|-----------|---------|--------|--------|--------|------------|--------------|------------------|
| **Spain** | 1 | 9.7 | 6.29 | **80%** | 17% | **97%** | 3% | ~60% |
| **Uruguay** | 16 | 7.0 | 5.51 | 18% | **76%** | 94% | **6%** | ~50% |
| Saudi Arabia | 60 | 3.0 | 2.75 | 1% | 5% | 6% | **94%** | ~5% |
| Cape Verde | 68 | 2.5 | 2.27 | 1% | 2% | 3% | **97%** | ~5% |

**Read:** Spain and Uruguay are near-certain to both advance (97% and 94% respectively). Saudi Arabia and Cape Verde are makeweights. The key game is Spain vs Uruguay — that determines who finishes 1st and therefore gets an easier R32 path. **Both teams likely have dead rubber game 3s** (high probability both qualify before the final round). Valverde/Fernández minutes will be managed carefully. Spain playing without Rodri makes the group slightly more interesting.

**Key watchlist players:** Spain (Simón, Raya, Cubarsí, Saliba's France isn't here — Spain's: Cucurella, Le Normand, Huijsen, Olmo, Pedri, Yamal, etc.), Uruguay (Valverde, Fernández)

---

### GROUP I — France, Senegal, Norway, Iraq

| Team | FIFA Rank | Strength | E[Pts] | P(1st) | P(2nd) | P(Advance) | P(Eliminated) | P(Dead Rubber G3) |
|------|-----------|---------|--------|--------|--------|------------|--------------|------------------|
| **France** | 3 | 10.0 | 6.16 | **82%** | 15% | **97%** | 3% | ~60% |
| **Senegal** | 19 | 7.1 | 4.76 | 14% | **70%** | 84% | **16%** | ~30% |
| **Norway** | 29 | 5.3 | 3.69 | 3% | 14% | 17% | **83%** | ~10% |
| Iraq | 58 | 3.2 | 2.10 | 1% | 1% | 2% | **98%** | ~5% |

**Read:** France are the group's dominant force (82% to win it). Senegal are comfortable 2nd favorites. Norway (Haaland + Ødegaard) have only a 17% chance of advancing — Haaland will likely play all 3 group games but go home early. France's game 3 (likely vs Iraq or Senegal) is a probable dead rubber. Olise and Mbappé likely rested.

**Key watchlist players:** France (Maignan, Saliba, Upamecano, Koundé, Mbappé, Dembélé, Doué, Olise, Ekitiké, Cherki), Norway (Haaland, Ødegaard)

---

### GROUP J — Argentina, Austria, Algeria, Jordan

| Team | FIFA Rank | Strength | E[Pts] | P(1st) | P(2nd) | P(Advance) | P(Eliminated) | P(Dead Rubber G3) |
|------|-----------|---------|--------|--------|--------|------------|--------------|------------------|
| **Argentina** | 2 | 10.0 | 6.38 | **88%** | 10% | **98%** | 2% | ~70% |
| Austria | 24 | 5.9 | 4.56 | 9% | **53%** | 62% | **38%** | ~15% |
| Algeria | 35 | 4.9 | 3.91 | 3% | 34% | 37% | **63%** | ~10% |
| Jordan | 66 | 2.5 | 1.90 | 0% | 3% | 3% | **97%** | ~5% |

**Read:** Argentina have the highest expected points across all 48 teams (6.38). They are near-certain to advance (98%) and overwhelmingly likely to win the group (88%). Argentina's game 3 is the strongest dead rubber candidate in the entire tournament (~70%). Expect Lautaro, Enzo, and potentially Álvarez to be rested. Austria vs Algeria is a real 2nd-place contest.

**Key watchlist players:** Argentina (Martínez, Romero, Enzo Fernández, Julián Álvarez, Lautaro, Soulé)

---

### GROUP K — Portugal, Colombia, Uzbekistan, DR Congo

| Team | FIFA Rank | Strength | E[Pts] | P(1st) | P(2nd) | P(Advance) | P(Eliminated) | P(Dead Rubber G3) |
|------|-----------|---------|--------|--------|--------|------------|--------------|------------------|
| **Portugal** | 6 | 8.6 | 5.99 | **68%** | 27% | **95%** | 5% | ~45% |
| **Colombia** | 13 | 7.3 | 5.34 | 28% | **61%** | 89% | **11%** | ~35% |
| Uzbekistan | 50 | 3.9 | 3.00 | 3% | 9% | 12% | **88%** | ~10% |
| DR Congo | 56 | 3.3 | 2.39 | 1% | 3% | 4% | **96%** | ~5% |

**Read:** Portugal and Colombia are both very likely to advance (95% and 89%). The group winner race is a real contest (68% vs 28%). Their head-to-head (Bruno Fernandes vs Caicedo/Lucho Díaz) is the marquee group game. Both managers may rotate for game 3 if both qualified. Uzbekistan and DR Congo are outmatched.

**Key watchlist players:** Portugal (Rúben Dias, Nuno Mendes, Vitinha, Bruno Fernandes, João Neves, Neto, Leão), Colombia (Caicedo, Luis Díaz)

---

### GROUP L — England, Croatia, Panama, Ghana

| Team | FIFA Rank | Strength | E[Pts] | P(1st) | P(2nd) | P(Advance) | P(Eliminated) | P(Dead Rubber G3) |
|------|-----------|---------|--------|--------|--------|------------|--------------|------------------|
| **England** | 4 | 9.3 | 5.97 | **72%** | 23% | **95%** | 5% | ~55% |
| **Croatia** | 10 | 7.4 | 5.08 | 22% | **60%** | 82% | **18%** | ~30% |
| **Panama** | 30 | 5.3 | 4.08 | 5% | 15% | 20% | **80%** | ~10% |
| **Ghana** | 72 | 2.1 | 1.65 | 1% | 2% | **5%** | **95%** | ~5% |

**Read:** England are clear group favorites. Croatia (Modric generation's final WC — likely) are comfortable 2nd favorites at 60%. Panama is the only team that could disrupt — a 20% chance of advancing is not negligible. Ghana (Kudus) have almost no path — P(advance) rises to only 5% even with the third-place route included. England likely have a dead rubber game 3 (~55%). Expect Pickford, Rice, Kane to be rested.

**Key watchlist players:** England (Pickford, Guéhi, Alexander-Arnold, Konsa, Quansah, Rice, Bellingham, Saka, Kane, Watkins, Rashford?), Croatia (Gvardiol), Ghana (Kudus)

---

## Watchlist Country Summary

| Country | Group | Opponents | Strength | P(Win Group) | P(Advance) | P(Eliminated) | P(Dead Rubber G3) | Key Risk |
|---------|-------|-----------|---------|-------------|------------|--------------|------------------|---------|
| **France** | I | Senegal, Norway, Iraq | 10.0 | **82%** | **97%** | 3% | **~60%** | None — heavy favourite |
| **Argentina** | J | Austria, Algeria, Jordan | 10.0 | **88%** | **98%** | 2% | **~70%** | None — tournament's dominant group |
| **Spain** | H | Uruguay, Saudi Arabia, Cape Verde | 9.7 | **80%** | **97%** | 3% | **~60%** | Rodri injury the only concern |
| **England** | L | Croatia, Panama, Ghana | 9.3 | **72%** | **95%** | 5% | **~55%** | Croatia could push them to 2nd |
| **Portugal** | K | Colombia, Uzbekistan, DR Congo | 8.6 | **68%** | **95%** | 5% | **~45%** | Colombia direct competition for 1st |
| **Morocco** | C | Brazil, Haiti, Scotland | 8.3 | **43%** | **84%** | 16% | **~20%** | Brazil coin-flip; no dead rubber |
| **Netherlands** | F | Japan, Tunisia, Sweden | 8.2 | **72%** | **94%** | 6% | **~55%** | Japan could push them |
| **Germany** | E | Ecuador, Ivory Coast, Curaçao | 7.9 | **78%** | **95%** | 5% | **~60%** | Most dominant expected group |
| **Brazil** | C | Morocco, Haiti, Scotland | 7.9 | **42%** | **83%** | 17% | **~20%** | Morocco; CONMEBOL form concern |
| **Belgium** | G | Iran, Egypt, New Zealand | 7.6 | **70%** | **92%** | 8% | **~50%** | Iran 20th ranked; trickier than it looks |
| **Croatia** | L | England, Panama, Ghana | 7.4 | 22% | **82%** | 18% | **~30%** | England will win group; Panama a threat |
| **Colombia** | K | Portugal, Uzbekistan, DR Congo | 7.3 | 28% | **89%** | 11% | **~35%** | Portugal head-to-head is decisive |
| **Uruguay** | H | Spain, Saudi Arabia, Cape Verde | 7.0 | 18% | **94%** | 6% | **~50%** | Spain head-to-head determines 1st/2nd |
| **Switzerland** | B | Canada, Qatar, Bosnia | 6.5 | **47%** | **87%** | 13% | **~20%** | Canada neck-and-neck; no dead rubber |
| **Canada** | B | Switzerland, Qatar, Bosnia | 5.7 | 43% | **83%** | 17% | **~20%** | Switzerland the primary obstacle |
| **Ecuador** | E | Germany, Ivory Coast, Curaçao | 5.8 | 16% | 66% | **34%** | **~20%** | Germany dominant; Ivory Coast danger |
| **Turkey** | D | USA, Australia, Paraguay | 5.8 | 19% | 56% | **44%** | **~15%** | Australia near-equal strength |
| **Sweden** | F | Netherlands, Japan, Tunisia | 4.4 | 3% | **20%** | **80%** | ~10% | Facing Netherlands + Japan; very tough |
| **Scotland** | C | Brazil, Morocco, Haiti | 5.0 | 14% | **40%** | **60%** | ~10% | Two top-10 teams; miracle needed |
| **Norway** | I | France, Senegal, Iraq | 5.3 | 3% | 17% | **83%** | ~10% | France dominant; Senegal dangerous |
| **Egypt** | G | Belgium, Iran, New Zealand | 5.0 | 10% | **58%** | **42%** | ~10% | Iran close in strength; tough for 2nd |
| **Ivory Coast** | E | Germany, Ecuador, Curaçao | 4.4 | 5% | **44%** | **56%** | ~10% | Germany dominant; Ecuador ahead |
| **Ghana** | L | England, Croatia, Panama | 2.1 | 1% | **5%** | **95%** | ~5% | Massive quality gap to top 2 |
| **USA** | D | Turkey, Australia, Paraguay | 7.1 | **62%** | **87%** | 13% | **~45%** | Turkey/Australia fight for 2nd |
| **Mexico** | A | South Korea, Czech Republic, South Africa | 7.1 | **55%** | **87%** | 13% | **~40%** | South Korea real challenge for 1st |

---

## Key Findings for Minutes Model

### Groups with likely dead rubbers (high rotation in game 3)
These countries should have reduced starter minutes in at least one game:

| Country | P(Dead Rubber G3) | Implication for player minutes |
|---------|------------------|-------------------------------|
| Argentina | ~70% | Lautaro/Álvarez/Enzo likely rested game 3 |
| Spain | ~60% | Yamal/Olmo/Cucurella probable rest game 3 |
| France | ~60% | Mbappé/Olise/Maignan probable rest game 3 |
| Germany | ~60% | Kimmich/Wirtz may rotate game 3 |
| England | ~55% | Kane/Rice/Saka probable rest game 3 |
| Netherlands | ~55% | Van Dijk/Gravenberch likely rotation game 3 |
| Belgium | ~50% | De Bruyne likely managed game 3 |
| Uruguay | ~50% | Valverde/Fernández may rotate with Spain already through |
| Portugal | ~45% | Bruno/Vitinha likely rested game 3 |
| USA | ~45% | Pulisic/Tillman probable rest game 3 |

### Groups with NO dead rubbers (every game full intensity)
| Country | Why | Implication |
|---------|-----|------------|
| Brazil | Morocco coin-flip | All 3 games likely full-strength |
| Morocco | Brazil coin-flip | All 3 games likely full-strength |
| Switzerland | Canada neck-and-neck | All 3 games full-strength |
| Canada | Switzerland neck-and-neck | All 3 games full-strength |
| Turkey | Australia near-identical | Fighting every minute |
| Colombia | Portugal fights for 1st | High-intensity all 3 games |
| Ecuador | Ivory Coast competition | No room for error |

### Countries likely not advancing (affects knockout minutes to 0)
Norway (83%), Ghana (95%), Scotland (60%), Sweden (80%), Ivory Coast (56%), Ecuador (34% eliminated), Turkey (44% eliminated)

*P(eliminated) after accounting for the 8-of-12 best third-place route. These players will have 3 group games of minutes at most, then near-zero knockout minutes in expectation.*
