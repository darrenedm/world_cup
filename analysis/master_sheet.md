# World Cup 2026 — Master Player Sheet
*115 players across GK / DEF / MID / FWD | Data as of May 12, 2026*

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

**Exp Post-Group Mins** — *total* expected minutes across all knockout rounds, conditional on making the squad. Formula: `P(country advances) × KO mins/game × E[knockout games if advance]`. E[KO games] estimated from country strength: top-tier nations (France, Argentina, Spain, England) ~3.5 games; strong nations (Portugal, Germany, Netherlands, Belgium) ~2.5–3.0; mid-tier ~2.0; underdogs ~1.5.

**Fitness flag** — `[INJ]` = active injury concern entering WC; `[MGD]` = managed/monitored; blank = fully fit.

---

## Country Parameters (quick reference)

| Country | Group | P(Advance) | P(Dead Rubber G3) | E[KO Games] |
|---------|-------|-----------|------------------|-------------|
| France | I | 97% | 60% | 3.5 |
| Argentina | J | 98% | 70% | 3.5 |
| Spain | H | 97% | 60% | 3.5 |
| England | L | 95% | 55% | 3.0 |
| Portugal | K | 95% | 45% | 3.0 |
| Netherlands | F | 94% | 55% | 3.0 |
| Uruguay | H | 94% | 50% | 2.5 |
| Belgium | G | 92% | 50% | 2.5 |
| Germany | E | 95% | 60% | 2.5 |
| Morocco | C | 84% | 20% | 2.5 |
| Brazil | C | 83% | 20% | 2.5 |
| Colombia | K | 89% | 35% | 2.0 |
| Croatia | L | 82% | 30% | 2.0 |
| Switzerland | B | 87% | 20% | 2.0 |
| USA | D | 87% | 45% | 2.0 |
| Canada | B | 83% | 20% | 1.5 |
| Ecuador | E | 66% | 20% | 1.5 |
| Turkey | D | 56% | 15% | 1.5 |
| Egypt | G | 43% | 10% | 1.0 |
| Ivory Coast | E | 34% | 10% | 1.0 |
| Scotland | C | 30% | 10% | 1.0 |
| Norway | I | 17% | 10% | 1.0 |
| Sweden | F | 14% | 10% | 1.0 |
| Ghana | L | 3% | 5% | 1.0 |

---

## Goalkeepers

| Player | Club | Country | WC Prob | Playing Role | Group Mins/Game | Exp Post-Group Mins | Notes |
|--------|------|---------|---------|-------------|----------------|--------------------|----|
| Emiliano Martínez | Aston Villa | Argentina | 97% | Starting GK | 90 | 309 | 3× WC/Copa Golden Glove |
| Mike Maignan | AC Milan | France | 97% | Starting GK | 90 | 305 | Undisputed No.1; Euro 2024 ToT |
| Unai Simón | Athletic Club | Spain | 95% | Starting GK | 90 | 305 | First choice despite domestic dip |
| Gregor Kobel | B. Dortmund | Switzerland | 95% | Starting GK | 90 | 157 | Record clean sheet run in qualifying |
| Jordan Pickford | Everton | England | 96% | Starting GK | 90 | 257 | England settled No.1; 5th major tournament |
| Alisson Becker | Liverpool | Brazil | 80% | Starting GK | 90 | 187 | **[INJ]** Hamstring since Mar 18; race for Jun 11 |
| Thibaut Courtois | Real Madrid | Belgium | 88% | Starting GK | 90 | 207 | **[INJ]** Quad Mar 2026; targeting return ~May 10 |
| Gerónimo Rulli | Marseille | Argentina | 88% | Backup GK | 5 | 10 | Confirmed No.2; guaranteed squad |
| David Raya | Arsenal | Spain | 82% | Backup GK | 5 | 10 | Plays if Simón struggles |
| Joan García | Barcelona | Spain | 80% | Third GK | 2 | 3 | Confirmed in squad per May 9 reports |
| Matz Sels | Nottingham Forest | Belgium | 75% | Backup GK | 5 | 10 | Becomes key No.1 if Courtois misses |
| Lucas Chevalier | PSG | France | 75% | Third GK | 2 | 3 | France future No.1; bench only now |
| James Trafford | Manchester City | England | 65% | Third GK | 2 | 3 | Strong contender; Tuchel backing |
| Mark Flekken | Bayer Leverkusen | Netherlands | 45% | Third GK | 2 | 3 | Below Verbruggen and Bijlow |
| Dean Henderson | Crystal Palace | England | 55% | Third GK | 2 | 3 | +5.0 PSxG-GA but 0 recent caps |
| Nick Pope | Newcastle | England | 30% | Third GK | 2 | 3 | **[MGD]** 4th option; crowded race |
| Robert Sánchez | Chelsea | Spain | 25% | Third GK | 2 | 3 | 4th option; 3 ahead of him |

---

## Defenders

| Player | Club | Country | WC Prob | Sub-Pos | Playing Role | Group Mins/Game | Exp Post-Group Mins | Notes |
|--------|------|---------|---------|---------|-------------|----------------|--------------------|----|
| Gabriel Magalhães | Arsenal | Brazil | 95% | CB | Automatic Starter | 86.1 | 187 | Brazil CB1 with Militão ruled out |
| William Saliba | Arsenal | France | 95% | CB | Automatic Starter | 82.4 | 305 | France CB1; Euro 2024 ToT |
| Jules Koundé | Barcelona | France | 95% | RB | Automatic Starter | 82.4 | 305 | Undisputed France first-choice RB |
| Virgil van Dijk | Liverpool | Netherlands | 97% | CB | Automatic Starter | 82.9 | 254 | Netherlands captain; elite at 34 |
| Denzel Dumfries | Inter Milan | Netherlands | 85% | RWB | Automatic Starter | 82.9 | 254 | Netherlands automatic RWB; 11 intl goals |
| Marc Cucurella | Chelsea | Spain | 90% | LB | Automatic Starter | 82.4 | 305 | Euro 2024 ToT; Spain first-choice LB |
| Dayot Upamecano | Bayern Munich | France | 90% | CB | Automatic Starter | 82.4 | 305 | Saliba's established partner; 35 caps |
| Nico Schlotterbeck | B. Dortmund | Germany | 85% | CB | Automatic Starter | 82.4 | 214 | Germany best-rated CB (FotMob 7.58) |
| Maximilian Mittelstädt | Stuttgart | Germany | 82% | LB | Automatic Starter | 82.4 | 214 | Germany established LB; 5G/4A from LB |
| Nuno Mendes | PSG | Portugal | 85% | LB | Automatic Starter | 83.8 | 257 | **[MGD]** Nations League best player; minor thigh |
| Rúben Dias | Manchester City | Portugal | 80% | CB | Automatic Starter | 83.8 | 257 | **[INJ]** Ankle; near return; Portugal linchpin |
| Pau Cubarsí | Barcelona | Spain | 88% | CB | Automatic Starter | 82.4 | 305 | 17-yr-old Spain CB1; elite metrics |
| Marc Guéhi | Manchester City | England | 82% | CB | Automatic Starter | 82.9 | 257 | England CB1; first intl goal Sep 2025 |
| Cristian Romero | Tottenham | Argentina | 82% | CB | Automatic Starter | 81.5 | 309 | **[INJ]** Grade 2 MCL Apr 12; on track Jun 16 |
| Achraf Hakimi | PSG | Morocco | 75% | RWB | Automatic Starter | 86.1 | 189 | **[INJ]** Hamstring tear May 8; race for Jun 14 |
| Joško Gvardiol | Manchester City | Croatia | 68% | LB | Automatic Starter | 85.2 | 148 | **[INJ]** Tibial fracture Jan; back in training May |
| Jonathan Tah | Bayern Munich | Germany | 82% | CB | Regular Starter | 71.0 | 190 | Competing for CB2 with Schlotterbeck |
| Robin Le Normand | Atlético Madrid | Spain | 82% | CB | Regular Starter | 71.0 | 272 | Returned from knee injury Jan 2026 |
| Ezri Konsa | Aston Villa | England | 72% | CB | Regular Starter | 71.3 | 228 | Competing for England CB2 |
| Trent Alexander-Arnold | Real Madrid | England | 82% | RB | Regular Starter | 71.3 | 228 | Hybrid RB-mid; England need his quality |
| Jurriën Timber | Arsenal | Netherlands | 72% | RB | Regular Starter | 71.3 | 226 | **[INJ]** Groin Mar 2026; slow recovery |
| Dean Huijsen | Real Madrid | Spain | 78% | CB | Impact Sub | 39.0 | 68 | 5 caps; gets dead rubber starts; 20 yrs old |
| Alejandro Grimaldo | Bayer Leverkusen | Spain | 72% | LB | Impact Sub | 39.0 | 68 | 8G/7A from LB; backup to Cucurella |
| Pedro Porro | Tottenham | Spain | 72% | RB | Impact Sub | 39.0 | 68 | ~12 Spain caps; cover for Carvajal role |
| Daniel Svensson | B. Dortmund | Sweden | 55% | LB | Impact Sub | 31.5 | 3 | 2 Sweden caps; competing for squad spot |
| Jarell Quansah | Bayer Leverkusen | England | 52% | CB | Fringe | 15.3 | 14 | 1 senior cap; dead rubber minutes only |
| Leny Yoro | Manchester United | France | 22% | CB | Depth | 3 | 5 | No senior France caps yet |
| Álvaro Carreras | Real Madrid | Spain | 22% | LB | Depth | 3 | 5 | Zero senior Spain caps |

---

## Midfielders

| Player | Club | Country | WC Prob | Sub-Pos | Playing Role | Group Mins/Game | Exp Post-Group Mins | Notes |
|--------|------|---------|---------|---------|-------------|----------------|--------------------|----|
| Declan Rice | Arsenal | England | 99% | DM | Automatic Starter | 82.9 | 257 | England's most important midfielder |
| Michael Olise | Bayern Munich | France | 96% | AM | Automatic Starter | 82.4 | 305 | 15G/18A — Europe's best MF this season |
| Joshua Kimmich | Bayern Munich | Germany | 97% | DM | Automatic Starter | 82.4 | 214 | Germany anchor; 103.7 passes/game |
| Florian Wirtz | Liverpool | Germany | 96% | AM | Automatic Starter | 82.4 | 214 | Germany creative hub; now delivering |
| Bruno Fernandes | Manchester United | Portugal | 98% | AM | Automatic Starter | 83.8 | 257 | Portugal captain; record PL assists |
| Vitinha | PSG | Portugal | 93% | DM | Automatic Starter | 83.8 | 257 | Portugal best pure midfielder |
| João Neves | PSG | Portugal | 87% | DM | Automatic Starter | 83.8 | 257 | 21 yrs; already PSG's pivotal figure |
| Federico Valverde | Real Madrid | Uruguay | 98% | CM | Automatic Starter | 83.3 | 212 | Uruguay most complete MF; first name on sheet |
| Ryan Gravenberch | Liverpool | Netherlands | 88% | DM | Automatic Starter | 82.9 | 254 | PL Young Player of Season; NED anchor |
| Pedri | Barcelona | Spain | 91% | CM | Automatic Starter | 82.4 | 305 | Spain's most elegant CM; returned from injury |
| Rodri | Manchester City | Spain | 75% | DM | Automatic Starter | 82.4 | 305 | **[INJ]** Groin May 2026; Spain's biggest WC concern |
| Enzo Fernández | Chelsea | Argentina | 90% | CM | Automatic Starter | 81.5 | 309 | Justified record fee; 9 yellows a concern |
| Moisés Caicedo | Chelsea | Ecuador | 95% | DM | Automatic Starter | 86.1 | 89 | Ecuador's best; discipline concern (11Y 1R) |
| Christian Pulisic | AC Milan | USA | 99% | AM | Automatic Starter | 83.8 | 157 | USMNT captain and best player; 84 caps |
| Scott McTominay | Napoli | Scotland | 98% | CM | Automatic Starter | 87.1 | 27 | Scotland WC hero; bicycle kick vs Denmark |
| Martin Ødegaard | Arsenal | Norway | 82% | AM | Automatic Starter | 87.1 | 15 | **[INJ]** Knee + shoulder all season; Norway captain |
| Mohammed Kudus | Tottenham | Ghana | 88% | AM | Automatic Starter | 87.5 | 3 | Ghana's best player; limited by Spurs' poor season |
| Jude Bellingham | Real Madrid | England | 85% | CM | Automatic Starter | 82.9 | 257 | **[INJ]** Hamstring Feb-Apr; Tuchel wants him regardless |
| Dani Olmo | Barcelona | Spain | 88% | AM | Regular Starter | 71.0 | 272 | Euro 2024 Golden Boot; rotates in attack |
| Malik Tillman | Bayer Leverkusen | USA | 95% | AM | Regular Starter | 71.9 | 139 | USMNT key creative force; starts most games |
| Kevin De Bruyne | Napoli | Belgium | 72% | CM | Regular Starter | 71.7 | 184 | **[MGD]** Age 34; hamstring Oct-Mar; managed carefully |
| Arda Güler | Real Madrid | Turkey | 78% | AM | Regular Starter | 74.0 | 67 | **[INJ]** Thigh tear Apr 21; targeting Jun 13 opener |
| Hakan Çalhanoğlu | Inter Milan | Turkey | 71% | DM | Regular Starter | 74.0 | 67 | **[INJ]** Soleus May 2026; fitness race for Jun 13 |
| Cole Palmer | Chelsea | England | 74% | AM | Impact Sub | 38.3 | 57 | **[INJ]** Chronic pubalgia; impact sub role |
| Eberechi Eze | Arsenal | England | 72% | AM | Impact Sub | 38.3 | 57 | Different option for England; ~10 caps |
| Angelo Stiller | Stuttgart | Germany | 62% | DM | Impact Sub | 39.0 | 48 | Germany backup DM; won't start over Kimmich |
| Felix Nmecha | B. Dortmund | Germany | 58% | CM | Impact Sub | 39.0 | 48 | Germany 4th/5th CM; squad depth |
| Rayan Cherki | Manchester City | France | 52% | AM | Fringe | 15.6 | 17 | 6 France caps; France depth means dead rubber only |
| Phil Foden | Manchester City | England | 58% | AM | Fringe | 15.3 | 14 | **[INJ]** Ankle Apr; form drop-off; Tuchel doubts |
| Morgan Gibbs-White | Nottingham Forest | England | 68% | AM | Fringe | 15.3 | 14 | 13 PL goals but Tuchel trust barrier |
| Fabián Ruiz | PSG | Spain | 73% | CM | Fringe | 15.6 | 17 | **[INJ]** Knee Jan; limited to 13 L1 apps |
| Exequiel Palacios | Bayer Leverkusen | Argentina | 65% | CM | Fringe | 16.2 | 17 | **[MGD]** Returning from adductor; Argentina depth |
| Maghnes Akliouche | AS Monaco | France | 55% | AM | Depth | 3 | 5 | France AM depth too deep to get minutes |
| Elliot Anderson | Nottingham Forest | England | 35% | CM | Depth | 3 | 5 | England CM crowded; squad bubble only |
| Jobe Bellingham | B. Dortmund | England | 5% | DM | Depth | 3 | 5 | Zero senior caps; emergency only |

---

## Forwards

| Player | Club | Country | WC Prob | Playing Role | Group Mins/Game | Exp Post-Group Mins | Notes |
|--------|------|---------|---------|-------------|----------------|--------------------|----|
| Erling Haaland | Manchester City | Norway | 99% | Automatic Starter | 87.1 | 15 | Broke PL record (35 PL goals); Norway's everything |
| Harry Kane | Bayern Munich | England | 99% | Automatic Starter | 82.9 | 257 | England captain; 33 BL goals; automatic |
| Kylian Mbappé | Real Madrid | France | 99% | Automatic Starter | 82.4 | 305 | France captain; 41 goals all comps; irreplaceable |
| Lamine Yamal | Barcelona | Spain | 99% | Automatic Starter | 82.4 | 305 | Spain talisman; 17G/13A La Liga; non-negotiable |
| Christian Pulisic | AC Milan | USA | 99% | Automatic Starter | 83.8 | 157 | *(see Midfielders)* |
| Lautaro Martínez | Inter Milan | Argentina | 95% | Automatic Starter | 81.5 | 309 | Argentina captain; automatic striker |
| Mohamed Salah | Liverpool | Egypt | 95% | Automatic Starter | 87.1 | 39 | Egypt's greatest player; final Liverpool season |
| Vinícius Júnior | Real Madrid | Brazil | 95% | Automatic Starter | 86.1 | 187 | Brazil key winger; 20G/13A all comps |
| Bukayo Saka | Arsenal | England | 92% | Automatic Starter | 82.9 | 257 | England first-choice right winger |
| Luis Díaz | Bayern Munich | Colombia | 92% | Automatic Starter | 84.7 | 160 | Colombia's best; 15G/13A — BL's best output |
| Jonathan David | Juventus | Canada | 90% | Automatic Starter | 86.1 | 112 | Canada all-time top scorer; hosts nation |
| Raphinha | Barcelona | Brazil | 82% | Automatic Starter | 86.1 | 187 | Brazil captain; first choice right winger |
| Viktor Gyökeres | Arsenal | Sweden | 82% | Automatic Starter | 87.1 | 13 | Sweden's standout striker; 14 PL goals |
| Julián Álvarez | Atlético Madrid | Argentina | 85% | Regular Starter | 70.3 | 274 | Often starts alongside Lautaro; 2022 WC winner |
| Kenan Yıldız | Juventus | Turkey | 85% | Automatic Starter | 86.6 | 76 | Turkey's defining player |
| Amad Diallo | Manchester United | Ivory Coast | 80% | Automatic Starter | 87.1 | 31 | WC qualifying hero; Ivory Coast's talisman |
| Ousmane Dembélé | PSG | France | 75% | Regular Starter | 71.0 | 272 | Established France starter; trusted by Deschamps |
| Alexander Isak | Liverpool | Sweden | 72% | Regular Starter | 74.3 | 11 | **[INJ]** Injury-ravaged season; starts if fit |
| Jérémy Doku | Manchester City | Belgium | 72% | Impact Sub | 37.5 | 46 | Regular Belgium squad; rotation at City |
| Pedro Neto | Chelsea | Portugal | 68% | Impact Sub | 36.8 | 57 | Nations League winner; regular squad member |
| Omar Marmoush | Manchester City | Egypt | 68% | Impact Sub | 31.5 | 9 | **[INJ]** Knee Sep 2025; wrecked season; limited role |
| Désiré Doué | PSG | France | 72% | Impact Sub | 39.0 | 68 | 26G across 5 comps; 8 caps; France depth limits starts |
| Ollie Watkins | Aston Villa | England | 65% | Impact Sub | 38.3 | 57 | Kane backup; 16G all comps; likely squad pick |
| Rafael Leão | AC Milan | Portugal | 65% | Impact Sub | 36.8 | 57 | Quality but inconsistent; depth forward |
| Jonathan Burkardt | Eintracht Frankfurt | Germany | 55% | Impact Sub | 39.0 | 48 | 5 caps; emerging Germany option |
| Karim Adeyemi | B. Dortmund | Germany | 50% | Impact Sub | 39.0 | 48 | Inconsistent but in Germany plans |
| Nick Woltemade | Newcastle | Germany | 45% | Impact Sub | 39.0 | 48 | 10 caps; squad bubble; scored in qualifying |
| Marcus Rashford | Barcelona | England | 45% | Impact Sub | 38.3 | 57 | Revitalised (12G/10A); re-entering England picture |
| Hugo Ekitiké | Liverpool | France | 48% | Fringe | 15.6 | 17 | 7 France caps; France forward depth extraordinary |
| Romelu Lukaku | Napoli | Belgium | 50% | Fringe | 15.0 | 12 | **[INJ]** High-grade thigh injury; fitness is everything |
| Serge Gnabry | Bayern Munich | Germany | 40% | Fringe | 15.6 | 12 | **[INJ]** Late-season groin; Germany have options ahead |
| João Pedro | Chelsea | Brazil | 42% | Fringe | 13.2 | 10 | Brazil forward depth makes squad very hard |
| Matheus Cunha | Manchester United | Brazil | 52% | Fringe | 13.2 | 10 | Fringe role even if he makes squad |
| Matías Soulé | Roma | Argentina | 22% | Depth | 3 | 5 | 2 senior caps; Argentina depth too deep |
| Antony | Real Betis | Brazil | 38% | Depth | 3 | 5 | Not featuring for Brazil; squad unlikely |
| Mason Greenwood | Marseille | England | 5% | Depth | 3 | 5 | 18G/7A but effectively excluded by FA |

---

## Notable patterns

**Highest total expected minutes (assuming squad inclusion):**
Lautaro Martínez, Enzo Fernández, Emiliano Martínez (Argentina ~81+309), Mbappé, Olise, Saliba, Koundé, Upamecano, Yamal (France/Spain ~82+272–305) dominate because their countries have the highest P(advance) × E[KO games].

**The Haaland paradox:** 87 group mins/game (plays every minute for Norway) but only 15 expected post-group minutes. Norway's 17% P(advance) means he almost certainly goes home after 3 games despite being the tournament's most dangerous individual threat.

**Argentina's dead rubber effect:** All Argentina players take a ~6-min/game hit in group stage average vs equivalent tier on Brazil/Morocco (70% vs 20% P(DR G3)). Lautaro and Enzo likely rest in game 3 against Jordan.

**The backup GK reality:** 10 of the 17 GKs on this list will play zero minutes. Courtois's fitness is the single biggest binary event — if he's out, Sels goes from 0 to ~90 mins/game, and Belgium's entire dynamic changes.

**France's depth problem:** Akliouche (55%), Cherki (52%), Yoro (22%), Ekitiké (48%) are all talented players who may make the squad but will barely feature. France could field two entirely different competitive XIs.
