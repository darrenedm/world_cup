# World Cup 2026 — Master Player Sheet
*115 players across GK / DEF / MID / FWD | Data as of May 14, 2026*

---

## How to read this sheet

**WC Prob %** — probability of making the national squad (from position-specific analysis files).

**Playing Role** — conditional on making the squad, the expected role in the team:
| Tier | Role | Competitive Game | Dead Rubber G3 | Knockout |
|------|------|-----------------|----------------|---------|
| GK1 | Starting GK | 90 min | 90 min | 90 min |
| GK2 | Backup GK | ~5 min | ~5 min | ~10 min total |
| GK3 | Third GK | ~2 min | ~2 min | ~3 min total |
| 1 | Automatic Starter | 88 min | 60 min | 90 min |
| 2 | Regular Starter | 75 min | 55 min | 80 min |
| 3 | Impact Sub | 30 min | 75 min | 20 min |
| 4 | Fringe | 12 min | 30 min | 5 min |
| 5 | Depth | ~3 min | ~8 min | ~5 min total |

**Group Mins/Game** — blended average per game across all 3 group games, incorporating each country's P(Dead Rubber Game 3). Game 1 and Game 2 always use competitive mins; Game 3 is weighted by P(DR G3). Managers never rest GKs even in dead rubbers.

**Exp Post-Group Mins** — *total* expected minutes across all knockout rounds, conditional on making the squad. Formula: `P(country advances) × KO mins/game × E[knockout games if advance]`. E[KO games] estimated from country strength and advance-path composition (3rd-place advances face stronger R32 opponents): France/Argentina/Spain ~3.3 games; England/Portugal ~3.0; Netherlands/Germany/Morocco/Brazil ~2.7; Belgium ~2.5; Uruguay ~2.4; Colombia/Croatia ~2.2; Switzerland/USA ~2.1; Canada/Ecuador ~1.8; Turkey ~1.7; Ivory Coast ~1.5; Egypt/Scotland/Norway/Sweden ~1.4; Ghana ~1.1.

**Fitness flag** — `[INJ]` = active injury concern entering WC; `[MGD]` = managed/monitored; blank = fully fit.

**act/90** — action points per 90 minutes: pure on-pitch event scoring (goals, assists, passes, tackles, saves, disciplinary) from WC-calibrated per-90 rates. Does not include win/draw/CS/GC bonuses.

**exp/90** — expected total points per 90 minutes played (action pts + per-game bonuses amortised over total expected mins). Comparable across players; higher = better value per minute.

**Total Pts** — expected total fantasy points across the full tournament (conditional on squad inclusion). Accounts for expected minutes, team strength (P(win)/P(CS)/E[GC]), and stage bonuses (top-tier win=30, draw=15, CS: GK=40/DEF=30/MID=10).

---

## Country Parameters (quick reference)

| Country | Group | P(Advance) | P(Dead Rubber G3) | E[KO Games] |
|---------|-------|-----------|------------------|-------------|
| France | I | 97% | 60% | 3.3 |
| Argentina | J | 98% | 70% | 3.3 |
| Spain | H | 97% | 60% | 3.3 |
| England | L | 95% | 55% | 3.0 |
| Portugal | K | 95% | 45% | 3.0 |
| Netherlands | F | 94% | 55% | 2.7 |
| Uruguay | H | 94% | 50% | 2.4 |
| Belgium | G | 92% | 50% | 2.5 |
| Germany | E | 95% | 60% | 2.7 |
| Morocco | C | 84% | 20% | 2.7 |
| Brazil | C | 83% | 20% | 2.7 |
| Colombia | K | 89% | 35% | 2.2 |
| Croatia | L | 82% | 30% | 2.2 |
| Switzerland | B | 87% | 20% | 2.1 |
| USA | D | 87% | 45% | 2.1 |
| Canada | B | 83% | 20% | 1.8 |
| Ecuador | E | 66% | 20% | 1.8 |
| Turkey | D | 79% | 15% | 1.7 |
| Egypt | G | 58% | 10% | 1.4 |
| Ivory Coast | E | 44% | 10% | 1.5 |
| Scotland | C | 40% | 10% | 1.4 |
| Norway | I | 58% | 10% | 1.4 |
| Sweden | F | 28% | 10% | 1.4 |
| Ghana | L | 5% | 5% | 1.1 |

---

## Goalkeepers

| Player | Club | Country | WC Prob | Playing Role | Group Mins/Game | Exp Post-Group Mins | Notes | act/90 | exp/90 | Total Pts |
|--------|------|---------|---------|-------------|----------------|--------------------|----|-------|-------|----------|
| Emiliano Martínez | Aston Villa | Argentina | 97% | Starting GK | 90 | 291 | 3× WC/Copa Golden Glove | 29.5 | 71.1 | 443.5 |
| Mike Maignan | AC Milan | France | 97% | Starting GK | 90 | 288 | Undisputed No.1; Euro 2024 ToT | 29.5 | 71.7 | 444.8 |
| Unai Simón | Athletic Club | Spain | 95% | Starting GK | 90 | 288 | First choice despite domestic dip | 29.5 | 71.3 | 442.1 |
| Gregor Kobel | B. Dortmund | Switzerland | 95% | Starting GK | 90 | 164 | Record clean sheet run in qualifying | 29.5 | 61.6 | 296.9 |
| Jordan Pickford | Everton | England | 96% | Starting GK | 90 | 256 | England settled No.1; 5th major tournament | 29.5 | 68.0 | 397.2 |
| Alisson Becker | Liverpool | Brazil | 80% | Starting GK | 90 | 202 | **[INJ]** Hamstring since Mar 18; race for Jun 11 | 29.5 | 63.2 | 331.5 |
| Thibaut Courtois | Real Madrid | Belgium | 88% | Starting GK | 90 | 207 | **[INJ]** Quad Mar 2026; targeting return ~May 10 | 29.5 | 65.9 | 349.5 |
| Gerónimo Rulli | Marseille | Argentina | 88% | Backup GK | 5 | 10 | Confirmed No.2; guaranteed squad | 29.5 | 43.2 | 12.0 |
| David Raya | Arsenal | Spain | 82% | Backup GK | 5 | 10 | Plays if Simón struggles | 29.5 | 43.3 | 12.0 |
| Joan García | Barcelona | Spain | 80% | Third GK | 2 | 3 | Confirmed in squad per May 9 reports | 29.5 | 43.7 | 4.4 |
| Matz Sels | Nottingham Forest | Belgium | 75% | Backup GK | 5 | 10 | Becomes key No.1 if Courtois misses | 29.5 | 41.5 | 11.5 |
| Lucas Chevalier | PSG | France | 75% | Third GK | 2 | 3 | France future No.1; bench only now | 29.5 | 43.6 | 4.4 |
| James Trafford | Manchester City | England | 65% | Third GK | 2 | 3 | Strong contender; Tuchel backing | 29.5 | 42.9 | 4.3 |
| Mark Flekken | Bayer Leverkusen | Netherlands | 45% | Third GK | 2 | 3 | Below Verbruggen and Bijlow | 29.5 | 42.2 | 4.2 |
| Dean Henderson | Crystal Palace | England | 55% | Third GK | 2 | 3 | +5.0 PSxG-GA but 0 recent caps | 29.5 | 42.9 | 4.3 |
| Nick Pope | Newcastle | England | 30% | Third GK | 2 | 3 | **[MGD]** 4th option; crowded race | 29.5 | 42.9 | 4.3 |
| Robert Sánchez | Chelsea | Spain | 25% | Third GK | 2 | 3 | 4th option; 3 ahead of him | 29.5 | 43.7 | 4.4 |

---

## Defenders

| Player | Club | Country | WC Prob | Sub-Pos | Playing Role | Group Mins/Game | Exp Post-Group Mins | Notes | act/90 | exp/90 | Total Pts |
|--------|------|---------|---------|---------|-------------|----------------|--------------------|----|-------|-------|----------|
| Gabriel Magalhães | Arsenal | Brazil | 95% | CB | Automatic Starter | 86.1 | 202 | Brazil CB1 with Militão ruled out | 51.8 | 83.7 | 428.2 |
| William Saliba | Arsenal | France | 95% | CB | Automatic Starter | 82.4 | 288 | France CB1; Euro 2024 ToT | 51.8 | 91.9 | 546.6 |
| Jules Koundé | Barcelona | France | 95% | RB | Automatic Starter | 82.4 | 288 | Undisputed France first-choice RB | 58.6 | 98.6 | 586.5 |
| Virgil van Dijk | Liverpool | Netherlands | 97% | CB | Automatic Starter | 82.9 | 228 | Netherlands captain; elite at 34 | 51.8 | 87.1 | 461.4 |
| Denzel Dumfries | Inter Milan | Netherlands | 85% | RWB | Automatic Starter | 82.9 | 228 | Netherlands automatic RWB; 11 intl goals | 58.6 | 93.8 | 497.0 |
| Marc Cucurella | Chelsea | Spain | 90% | LB | Automatic Starter | 82.4 | 288 | Euro 2024 ToT; Spain first-choice LB | 58.6 | 98.3 | 584.7 |
| Dayot Upamecano | Bayern Munich | France | 90% | CB | Automatic Starter | 82.4 | 288 | Saliba's established partner; 35 caps | 51.8 | 91.9 | 546.6 |
| Nico Schlotterbeck | B. Dortmund | Germany | 85% | CB | Automatic Starter | 82.4 | 231 | Germany best-rated CB (FotMob 7.58) | 51.8 | 88.6 | 471.0 |
| Maximilian Mittelstädt | Stuttgart | Germany | 82% | LB | Automatic Starter | 82.4 | 231 | Germany established LB; 5G/4A from LB | 58.6 | 95.4 | 506.7 |
| Nuno Mendes | PSG | Portugal | 85% | LB | Automatic Starter | 83.8 | 256 | **[MGD]** Nations League best player; minor thigh | 60.2 | 96.0 | 541.5 |
| Rúben Dias | Manchester City | Portugal | 80% | CB | Automatic Starter | 83.8 | 256 | **[INJ]** Ankle; near return; Portugal linchpin | 51.8 | 87.7 | 494.2 |
| Pau Cubarsí | Barcelona | Spain | 88% | CB | Automatic Starter | 82.4 | 288 | 17-yr-old Spain CB1; elite metrics | 51.8 | 91.6 | 544.8 |
| Marc Guéhi | Manchester City | England | 82% | CB | Automatic Starter | 82.9 | 256 | England CB1; first intl goal Sep 2025 | 51.8 | 88.6 | 496.7 |
| Cristian Romero | Tottenham | Argentina | 82% | CB | Automatic Starter | 81.5 | 291 | **[INJ]** Grade 2 MCL Apr 12; on track Jun 16 | 51.8 | 91.6 | 545.3 |
| Achraf Hakimi | PSG | Morocco | 75% | RWB | Automatic Starter | 86.1 | 204 | **[INJ]** Hamstring tear May 8; race for Jun 14 | 61.9 | 94.4 | 485.1 |
| Joško Gvardiol | Manchester City | Croatia | 68% | LB | Automatic Starter | 85.2 | 162 | **[INJ]** Tibial fracture Jan; back in training May | 62.3 | 92.0 | 427.0 |
| Jonathan Tah | Bayern Munich | Germany | 82% | CB | Regular Starter | 71.0 | 205 | Competing for CB2 with Schlotterbeck | 51.8 | 94.4 | 438.7 |
| Robin Le Normand | Atlético Madrid | Spain | 82% | CB | Regular Starter | 71.0 | 256 | Returned from knee injury Jan 2026 | 51.8 | 97.7 | 509.0 |
| Ezri Konsa | Aston Villa | England | 72% | CB | Regular Starter | 71.3 | 228 | Competing for England CB2 | 51.8 | 94.4 | 463.3 |
| Trent Alexander-Arnold | Real Madrid | England | 82% | RB | Regular Starter | 71.3 | 228 | Hybrid RB-mid; England need his quality | 58.6 | 101.1 | 496.4 |
| Jurriën Timber | Arsenal | Netherlands | 72% | RB | Regular Starter | 71.3 | 203 | **[INJ]** Groin Mar 2026; slow recovery | 58.6 | 99.5 | 460.9 |
| Dean Huijsen | Real Madrid | Spain | 78% | CB | Impact Sub | 39.0 | 64 | 5 caps; gets dead rubber starts; 20 yrs old | 51.8 | 89.9 | 180.9 |
| Alejandro Grimaldo | Bayer Leverkusen | Spain | 72% | LB | Impact Sub | 39.0 | 64 | 8G/7A from LB; backup to Cucurella | 58.6 | 96.7 | 194.4 |
| Pedro Porro | Tottenham | Spain | 72% | RB | Impact Sub | 39.0 | 64 | ~12 Spain caps; cover for Carvajal role | 58.6 | 96.7 | 194.4 |
| Daniel Svensson | B. Dortmund | Sweden | 55% | LB | Impact Sub | 31.5 | 8 | 2 Sweden caps; competing for squad spot | 58.6 | 80.7 | 91.9 |
| Jarell Quansah | Bayer Leverkusen | England | 52% | CB | Fringe | 15.3 | 14 | 1 senior cap; dead rubber minutes only | 51.8 | 123.0 | 81.8 |
| Leny Yoro | Manchester United | France | 22% | CB | Depth | 3 | 6 | No senior France caps yet | 51.8 | 244.5 | 40.7 |
| Álvaro Carreras | Real Madrid | Spain | 22% | LB | Depth | 3 | 6 | Zero senior Spain caps | 58.6 | 252.1 | 42.0 |

---

## Midfielders

| Player | Club | Country | WC Prob | Sub-Pos | Playing Role | Group Mins/Game | Exp Post-Group Mins | Notes | act/90 | exp/90 | Total Pts |
|--------|------|---------|---------|---------|-------------|----------------|--------------------|----|-------|-------|----------|
| Declan Rice | Arsenal | England | 99% | DM | Automatic Starter | 82.9 | 256 | England's most important midfielder | 72.0 | 103.1 | 578.2 |
| Michael Olise | Bayern Munich | France | 96% | AM | Automatic Starter | 82.4 | 288 | 15G/18A — Europe's best MF this season | 107.2 | 138.0 | 820.6 |
| Joshua Kimmich | Bayern Munich | Germany | 97% | DM | Automatic Starter | 82.4 | 231 | Germany anchor; 103.7 passes/game | 95.7 | 126.7 | 673.4 |
| Florian Wirtz | Liverpool | Germany | 96% | AM | Automatic Starter | 82.4 | 231 | Germany creative hub; now delivering | 65.6 | 95.3 | 506.5 |
| Bruno Fernandes | Manchester United | Portugal | 98% | AM | Automatic Starter | 83.8 | 256 | Portugal captain; record PL assists | 76.9 | 106.3 | 599.5 |
| Vitinha | PSG | Portugal | 93% | DM | Automatic Starter | 83.8 | 256 | Portugal best pure midfielder | 82.6 | 113.2 | 638.3 |
| João Neves | PSG | Portugal | 87% | DM | Automatic Starter | 83.8 | 256 | 21 yrs; already PSG's pivotal figure | 74.5 | 105.0 | 592.1 |
| Federico Valverde | Real Madrid | Uruguay | 98% | CM | Automatic Starter | 83.3 | 203 | Uruguay most complete MF; first name on sheet | 76.3 | 104.6 | 526.2 |
| Ryan Gravenberch | Liverpool | Netherlands | 88% | DM | Automatic Starter | 82.9 | 228 | PL Young Player of Season; NED anchor | 71.5 | 101.4 | 536.9 |
| Pedri | Barcelona | Spain | 91% | CM | Automatic Starter | 82.4 | 288 | Spain's most elegant CM; returned from injury | 90.8 | 123.8 | 736.4 |
| Rodri | Manchester City | Spain | 75% | DM | Automatic Starter | 82.4 | 288 | **[INJ]** Groin May 2026; Spain's biggest WC concern | 68.1 | 101.1 | 601.5 |
| Enzo Fernández | Chelsea | Argentina | 90% | CM | Automatic Starter | 81.5 | 291 | Justified record fee; 9 yellows a concern | 66.0 | 99.1 | 589.6 |
| Moisés Caicedo | Chelsea | Ecuador | 95% | DM | Automatic Starter | 86.1 | 107 | Ecuador's best; discipline concern (11Y 1R) | 72.4 | 97.6 | 396.3 |
| Christian Pulisic | AC Milan | USA | 99% | AM | Automatic Starter | 83.8 | 164 | USMNT captain and best player; 84 caps | 87.5 | 114.2 | 527.1 |
| Scott McTominay | Napoli | Scotland | 98% | CM | Automatic Starter | 87.1 | 50 | Scotland WC hero; bicycle kick vs Denmark | 81.4 | 103.1 | 356.6 |
| Martin Ødegaard | Arsenal | Norway | 82% | AM | Automatic Starter | 87.1 | 73 | **[INJ]** Knee + shoulder all season; Norway captain | 67.9 | 90.5 | 336.3 |
| Mohammed Kudus | Tottenham | Ghana | 88% | AM | Automatic Starter | 87.5 | 5 | Ghana's best player; limited by Spurs' poor season | 65.2 | 81.9 | 243.4 |
| Jude Bellingham | Real Madrid | England | 85% | CM | Automatic Starter | 82.9 | 256 | **[INJ]** Hamstring Feb-Apr; Tuchel wants him regardless | 80.2 | 111.3 | 624.4 |
| Dani Olmo | Barcelona | Spain | 88% | AM | Regular Starter | 71.0 | 256 | Euro 2024 Golden Boot; rotates in attack | 75.6 | 110.9 | 578.1 |
| Malik Tillman | Bayer Leverkusen | USA | 95% | AM | Regular Starter | 71.9 | 146 | USMNT key creative force; starts most games | 65.3 | 95.9 | 385.5 |
| Kevin De Bruyne | Napoli | Belgium | 72% | CM | Regular Starter | 71.7 | 184 | **[MGD]** Age 34; hamstring Oct-Mar; managed carefully | 87.5 | 122.0 | 541.0 |
| Arda Güler | Real Madrid | Turkey | 78% | AM | Regular Starter | 74.0 | 107 | **[INJ]** Thigh tear Apr 21; targeting Jun 13 opener | 68.6 | 96.2 | 351.5 |
| Hakan Çalhanoğlu | Inter Milan | Turkey | 71% | DM | Regular Starter | 74.0 | 107 | **[INJ]** Soleus May 2026; fitness race for Jun 13 | 92.4 | 118.5 | 433.3 |
| Cole Palmer | Chelsea | England | 74% | AM | Impact Sub | 38.3 | 57 | **[INJ]** Chronic pubalgia; impact sub role | 65.3 | 105.2 | 200.9 |
| Eberechi Eze | Arsenal | England | 72% | AM | Impact Sub | 38.3 | 57 | Different option for England; ~10 caps | 65.3 | 105.2 | 200.9 |
| Angelo Stiller | Stuttgart | Germany | 62% | DM | Impact Sub | 39.0 | 51 | Germany backup DM; won't start over Kimmich | 68.1 | 104.7 | 195.4 |
| Felix Nmecha | B. Dortmund | Germany | 58% | CM | Impact Sub | 39.0 | 51 | Germany 4th/5th CM; squad depth | 66.0 | 102.6 | 191.6 |
| Rayan Cherki | Manchester City | France | 52% | AM | Fringe | 15.6 | 16 | 6 France caps; France depth means dead rubber only | 65.3 | 142.3 | 99.3 |
| Phil Foden | Manchester City | England | 58% | AM | Fringe | 15.3 | 14 | **[INJ]** Ankle Apr; form drop-off; Tuchel doubts | 65.3 | 139.3 | 92.7 |
| Morgan Gibbs-White | Nottingham Forest | England | 68% | AM | Fringe | 15.3 | 14 | 13 PL goals but Tuchel trust barrier | 65.3 | 139.3 | 92.7 |
| Fabián Ruiz | PSG | Spain | 73% | CM | Fringe | 15.6 | 16 | **[INJ]** Knee Jan; limited to 13 L1 apps | 66.0 | 142.0 | 99.1 |
| Exequiel Palacios | Bayer Leverkusen | Argentina | 65% | CM | Fringe | 16.2 | 16 | **[MGD]** Returning from adductor; Argentina depth | 66.0 | 139.4 | 100.1 |
| Maghnes Akliouche | AS Monaco | France | 55% | AM | Depth | 3 | 6 | France AM depth too deep to get minutes | 65.3 | 259.8 | 43.3 |
| Elliot Anderson | Nottingham Forest | England | 35% | CM | Depth | 3 | 6 | England CM crowded; squad bubble only | 66.0 | 251.7 | 42.0 |
| Jobe Bellingham | B. Dortmund | England | 5% | DM | Depth | 3 | 6 | Zero senior caps; emergency only | 68.1 | 253.8 | 42.3 |

---

## Forwards

| Player | Club | Country | WC Prob | Playing Role | Group Mins/Game | Exp Post-Group Mins | Notes | act/90 | exp/90 | Total Pts |
|--------|------|---------|---------|-------------|----------------|--------------------|----|-------|-------|----------|
| Erling Haaland | Manchester City | Norway | 99% | Automatic Starter | 87.1 | 73 | Broke PL record (35 PL goals); Norway's everything | 61.8 | 84.4 | 313.6 |
| Harry Kane | Bayern Munich | England | 99% | Automatic Starter | 82.9 | 256 | England captain; 33 BL goals; automatic | 85.7 | 115.5 | 647.7 |
| Kylian Mbappé | Real Madrid | France | 99% | Automatic Starter | 82.4 | 288 | France captain; 41 goals all comps; irreplaceable | 96.7 | 127.6 | 758.7 |
| Lamine Yamal | Barcelona | Spain | 99% | Automatic Starter | 82.4 | 288 | Spain talisman; 17G/13A La Liga; non-negotiable | 101.0 | 132.0 | 785.2 |
| Christian Pulisic | AC Milan | USA | 99% | Automatic Starter | 83.8 | 164 | *(see Midfielders)* | 87.5 | 114.2 | 527.1 |
| Lautaro Martínez | Inter Milan | Argentina | 95% | Automatic Starter | 81.5 | 291 | Argentina captain; automatic striker | 46.0 | 77.0 | 457.9 |
| Mohamed Salah | Liverpool | Egypt | 95% | Automatic Starter | 87.1 | 73 | Egypt's greatest player; final Liverpool season | 66.9 | 92.4 | 343.4 |
| Vinícius Júnior | Real Madrid | Brazil | 95% | Automatic Starter | 86.1 | 202 | Brazil key winger; 20G/13A all comps | 73.6 | 102.0 | 521.7 |
| Bukayo Saka | Arsenal | England | 92% | Automatic Starter | 82.9 | 256 | England first-choice right winger | 67.9 | 97.7 | 547.9 |
| Luis Díaz | Bayern Munich | Colombia | 92% | Automatic Starter | 84.7 | 176 | Colombia's best; 15G/13A — BL's best output | 83.8 | 110.6 | 528.6 |
| Jonathan David | Juventus | Canada | 90% | Automatic Starter | 86.1 | 134 | Canada all-time top scorer; hosts nation | 39.6 | 66.3 | 288.8 |
| Raphinha | Barcelona | Brazil | 82% | Automatic Starter | 86.1 | 202 | Brazil captain; first choice right winger | 80.9 | 109.3 | 559.1 |
| Viktor Gyökeres | Arsenal | Sweden | 82% | Automatic Starter | 87.1 | 35 | Sweden's standout striker; 14 PL goals | 47.1 | 68.6 | 225.8 |
| Julián Álvarez | Atlético Madrid | Argentina | 85% | Regular Starter | 70.3 | 259 | Often starts alongside Lautaro; 2022 WC winner | 40.0 | 75.4 | 393.5 |
| Kenan Yıldız | Juventus | Turkey | 85% | Automatic Starter | 86.6 | 121 | Turkey's defining player | 68.8 | 92.6 | 391.8 |
| Amad Diallo | Manchester United | Ivory Coast | 80% | Automatic Starter | 87.1 | 59 | WC qualifying hero; Ivory Coast's talisman | 56.6 | 81.1 | 288.7 |
| Ousmane Dembélé | PSG | France | 75% | Regular Starter | 71.0 | 256 | Established France starter; trusted by Deschamps | 63.9 | 99.1 | 516.3 |
| Alexander Isak | Liverpool | Sweden | 72% | Regular Starter | 74.3 | 31 | **[INJ]** Injury-ravaged season; starts if fit | 36.6 | 61.6 | 173.7 |
| Jérémy Doku | Manchester City | Belgium | 72% | Impact Sub | 37.5 | 46 | Regular Belgium squad; rotation at City | 66.9 | 105.5 | 185.8 |
| Pedro Neto | Chelsea | Portugal | 68% | Impact Sub | 36.8 | 57 | Nations League winner; regular squad member | 66.9 | 107.5 | 200.0 |
| Omar Marmoush | Manchester City | Egypt | 68% | Impact Sub | 31.5 | 16 | **[INJ]** Knee Sep 2025; wrecked season; limited role | 32.0 | 69.4 | 85.3 |
| Désiré Doué | PSG | France | 72% | Impact Sub | 39.0 | 64 | 26G across 5 comps; 8 caps; France depth limits starts | 66.9 | 108.1 | 217.3 |
| Ollie Watkins | Aston Villa | England | 65% | Impact Sub | 38.3 | 57 | Kane backup; 16G all comps; likely squad pick | 46.0 | 85.9 | 164.0 |
| Rafael Leão | AC Milan | Portugal | 65% | Impact Sub | 36.8 | 57 | Quality but inconsistent; depth forward | 66.9 | 107.5 | 200.0 |
| Jonathan Burkardt | Eintracht Frankfurt | Germany | 55% | Impact Sub | 39.0 | 51 | 5 caps; emerging Germany option | 46.0 | 84.8 | 158.3 |
| Karim Adeyemi | B. Dortmund | Germany | 50% | Impact Sub | 39.0 | 51 | Inconsistent but in Germany plans | 66.9 | 105.7 | 197.2 |
| Nick Woltemade | Newcastle | Germany | 45% | Impact Sub | 39.0 | 51 | 10 caps; squad bubble; scored in qualifying | 66.9 | 105.7 | 197.2 |
| Marcus Rashford | Barcelona | England | 45% | Impact Sub | 38.3 | 57 | Revitalised (12G/10A); re-entering England picture | 66.9 | 106.8 | 203.9 |
| Hugo Ekitiké | Liverpool | France | 48% | Fringe | 15.6 | 16 | 7 France caps; France forward depth extraordinary | 66.9 | 143.9 | 100.4 |
| Romelu Lukaku | Napoli | Belgium | 50% | Fringe | 15.0 | 12 | **[INJ]** High-grade thigh injury; fitness is everything | 46.0 | 117.2 | 74.2 |
| Serge Gnabry | Bayern Munich | Germany | 40% | Fringe | 15.6 | 13 | **[INJ]** Late-season groin; Germany have options ahead | 66.9 | 138.4 | 92.0 |
| João Pedro | Chelsea | Brazil | 42% | Fringe | 13.2 | 11 | Brazil forward depth makes squad very hard | 46.0 | 123.3 | 69.3 |
| Matheus Cunha | Manchester United | Brazil | 52% | Fringe | 13.2 | 11 | Fringe role even if he makes squad | 46.0 | 123.3 | 69.3 |
| Matías Soulé | Roma | Argentina | 22% | Depth | 3 | 6 | 2 senior caps; Argentina depth too deep | 46.0 | 240.5 | 40.1 |
| Antony | Real Betis | Brazil | 38% | Depth | 3 | 4 | Not featuring for Brazil; squad unlikely | 66.9 | 238.8 | 34.5 |
| Mason Greenwood | Marseille | England | 5% | Depth | 3 | 6 | 18G/7A but effectively excluded by FA | 66.9 | 253.9 | 42.3 |

---

## Notable patterns

**Highest total expected minutes (assuming squad inclusion):**
Lautaro Martínez, Enzo Fernández, Emiliano Martínez (Argentina ~82+291), Mbappé, Olise, Saliba, Koundé, Upamecano, Yamal (France/Spain ~82+288) dominate because their countries have the highest P(advance) × E[KO games].

**The Haaland paradox revised:** 87 group mins/game for Norway, and now 73 expected post-group minutes — not as bleak as originally modelled. Norway's P(Advance) rises to 58% once the 3rd-place route is included (they beat Iraq most of the time, and a GD of ~−1 makes them strong best-8 candidates), and their E[KO] edges up to 1.4 because ~71% of their advances come as 3rd-place (facing tougher R32 opponents, but Norway are competitive enough to win at least one). Haaland likely goes home after 3 games in 42% of scenarios, but in 58% he has real knockout exposure. Still a far cry from the 288 expected post-group minutes for Mbappé.

**Argentina's dead rubber effect:** All Argentina players take a ~6-min/game hit in group stage average vs equivalent tier on Brazil/Morocco (70% vs 20% P(DR G3)). Lautaro and Enzo likely rest in game 3 against Jordan.

**The backup GK reality:** 10 of the 17 GKs on this list will play zero minutes. Courtois's fitness is the single biggest binary event — if he's out, Sels goes from 0 to ~90 mins/game, and Belgium's entire dynamic changes.

**France's depth problem:** Akliouche (55%), Cherki (52%), Yoro (22%), Ekitiké (48%) are all talented players who may make the squad but will barely feature. France could field two entirely different competitive XIs.

**Fantasy point leaders (Total Pts):** Olise (820), Yamal (785), Mbappé (759), Pedri (736), Kimmich (673), Kane (648), Vitinha (638), Bellingham (624), Rodri (601), B.Fernandes (599). France and Spain dominate the top 10 due to elite team parameters (CS%, GC, win probability) combined with individual quality. Olise tops on the back of his 15G/18A club season plus AM archetype pass-volume scoring.

**Best value (exp/90):** Olise (138), Yamal (132), Mbappé (128), Kimmich (127), De Bruyne (122) — high exp/90 signals players who deliver both per-minute action AND play for strong teams. De Bruyne at 122 exp/90 is the best-value T2 pick given Belgium's team quality.

**Team-quality drag on elite players:** Haaland (84 act/90, only 313 total) and Ødegaard (90 exp/90, 336 total) are penalised heavily by Norway's weak win/CS probability (g_wd=13.5, g_cs=18%). Salah (Egypt) earns 82 act/90 but only 295 total for the same reason. These are elite players bottlenecked by their national teams.
