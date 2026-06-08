# Dashboard Plan: "Breakout Stars of World Cup 2026"

*Interactive HTML dashboard — implementation plan*  
*Drafted: June 8, 2026*

---

## 1. Goal & Story

**Core narrative**: Most World Cup coverage focuses on Mbappé, Haaland, Bellingham. This dashboard asks a different question — *who are the players that could emerge from relative obscurity to define this tournament?* Players who are first-choice starters for their countries, potentially undervalued by global audiences, and who could rack up massive fantasy-relevant output if their nation goes deep.

**Secondary narrative layer**: Since WC 2026 is a 48-team tournament with group→R32→R16→QF→SF→Final, the compounding upside of a dark-horse run is massive. A player like Woltemade (Germany, price 0.006) playing 8 games is worth more than Mbappé playing 3.

**User experience arc**:
1. Land on the dashboard → immediately see 4–5 "featured breakout candidates" with a punchy headline
2. Scroll to the interactive advancement selector → pick which teams advance
3. Watch the ranked player list re-sort in real time
4. Explore the scatter plot, drill into country views

---

## 2. Data Model

### Source files
- `data/master_sheet.csv` — all 1,216+ confirmed WC 2026 players
- `scripts/price_value_lookup.py` — `FRIENDLY`, `LIVE_STATUS`, `G1_WIN`, `CONFIRMED_OUT` dicts
- `analysis/country_rankings.md` — 48-nation strength scores

### Python data-prep script (`scripts/build_dashboard_data.py`)
Generates a single `dashboard_data.json` embedded in the HTML. Fields per player:

```json
{
  "name": "Nick Woltemade",
  "country": "Germany",
  "group": "E",
  "position": "FWD",
  "sub_pos": "CF",
  "club": "Stuttgart",
  "tier": "T2",
  "playing_role": "Starter",
  "pts_per_game": 42.1,
  "adj_pts": 549.7,
  "price": 0.00621,
  "fitness": "full",
  "starter": "yes",
  "g1_win_pct": 95,
  "country_p_advance": 97,
  "f_starts": 0,
  "f_apps": 1,
  "breakout_score": 87.4,
  "breakout_tier": "sleeper"
}
```

### Key computed fields

**`pts_per_game`** (the universal currency):
```
pts_per_game = action_pts_per_90 × group_mins_per_game / 90
```
This is position- and role-adjusted. A starter CF has ~65 mins/game × high action rate. A fringe GK gets 2 mins × low rate.

**`conditional_pts(n_games)`** — used for all interactive calculations:
```
conditional_pts = pts_per_game × n_games
```
WC 2026 game counts by advancement stage:
- Group stage only: 3 games
- Reach R32: 4 games  
- Reach R16: 5 games
- Reach QF: 6 games
- Reach SF: 7 games
- Reach Final: 8 games

**`breakout_score`** — determines featured/highlighted status:
```
breakout_score = (pts_per_game × 8 / price) 
                × fitness_weight 
                × form_weight
                × (1 − established_penalty)
```
- `fitness_weight`: full=1.0, mostly=0.85, not=0.2
- `form_weight`: (1 + f_apps × 0.15) — recent friendly appearances boost score
- `established_penalty`: 0.4 if price > 0.020 (already a global superstar), else 0

**`breakout_tier`** (categorical label, drives visual badges):
- `"star"` — top-30 global price, deep-run country (the known names for context)
- `"rising"` — breakout_score top-30 but price < 0.012
- `"sleeper"` — breakout_score top-60 but price < 0.008 (the real discoveries)
- `"wildcard"` — high pts_per_game but country p_advance < 40%

---

## 3. Dashboard Structure

### Layout (single-page HTML, ~1,600 lines)

```
┌──────────────────────────────────────────────────────┐
│  HERO  "Who will light up World Cup 2026?"           │
│  Animated featured player cards (4 rotating picks)  │
└──────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────┐
│  ADVANCEMENT BUILDER                                 │
│  12 groups × 4 teams — click to advance/eliminate   │
│  [ Probability-weighted ] [ Your picks ]  toggles   │
└──────────────────────────────────────────────────────┘
┌────────────────────┐  ┌───────────────────────────────┐
│  SCATTER PLOT      │  │  RANKED PLAYER LIST           │
│  X: price          │  │  Sorted by conditional pts    │
│  Y: conditional    │  │  Filters: pos / tier / ctry   │
│     pts            │  │  Each row: mini-card with     │
│  Color: position   │  │  badge (rising/sleeper/etc.)  │
│  Size: g1_win_pct  │  │                               │
│                    │  │                               │
└────────────────────┘  └───────────────────────────────┘
┌──────────────────────────────────────────────────────┐
│  FEATURED STORYLINES  (4 editorial cards)            │
│  "The German depth machine"  "Scotland's McTominay"  │
│  "Egypt's Marmoush problem"  "The Canadian surge"    │
└──────────────────────────────────────────────────────┘
```

---

## 4. Sections in Detail

### 4.1 Hero Section
- Full-width dark navy background with animated gold particle field
- Rotating headline: *"Breakout Stars of World Cup 2026"*
- 4 featured player cards auto-cycling through top `breakout_tier: sleeper` picks:
  - Woltemade (Germany), Palacios (Argentina), Svensson (Sweden), McTominay (Scotland), Tillman (USA)
- Each card shows: name, country flag emoji, pts_per_game, price, breakout tier badge
- "Build your bracket →" CTA button

### 4.2 Advancement Builder
- 12 groups in a 4×3 grid (4 teams per group)
- Default state: probability-weighted (teams displayed with their `g1_win_pct` and `country_p_advance`)
- Each team button shows: flag, name, P(advance) percentage
- Two modes:
  - **"By probability"** (default): advancement multiplied by each team's actual probability — no clicking needed, just shows expected value
  - **"Your picks"**: user clicks exactly 2 teams per group to advance; wildcard slots auto-fill the 8 best 3rd-place teams using a simple points-ranking heuristic
- "Reset" button returns to probability mode
- Live counter: "X teams advancing from your bracket"

### 4.3 Scatter Plot (D3.js)
- X-axis: log-scale price (0.002 → 0.07), labelled in tenero units
- Y-axis: conditional pts (recalculated on every bracket change)
- Each dot = one player from the 93 tracked (our price-list universe)
- Color by position: GK=grey, DEF=blue, MID=green, FWD=orange
- Dot size proportional to `g1_win_pct` (bigger = more likely to win G1)
- Hover tooltip: player card pop-up (name, country, pts, price, fitness, friendly form)
- **Breakout zone**: shaded quadrant — low price (left half) + high cond. pts (upper half) — labelled *"Breakout Zone"*
- Stars (⭐) mark `breakout_tier: sleeper` players

### 4.4 Ranked Player List
- Sorted by `conditional_pts` descending, updating live with bracket changes
- Each row:
  ```
  [Tier badge]  Name          Country  Pos  Price    Cond.Pts  Pts/$ | Fit  Starter  F.St F.Ap
  [SLEEPER 🔥]  Woltemade     GER     FWD  0.00621   337.0    54.3K | ✅  yes       0    1
  ```
- Filters (pills): All / GK / DEF / MID / FWD | All / star / rising / sleeper / wildcard
- Country filter: searchable dropdown
- Each name is clickable → expands an inline player detail card with notes from `master_sheet.notes` and `LIVE_STATUS`

### 4.5 Featured Storylines
4 editorial cards, hand-curated, each with a 2-sentence narrative and 3 key players:

| Card | Theme | Players |
|------|-------|---------|
| "Germany's depth machine" | Germany's 2nd-tier attackers are priced like squad players but could see huge minutes if top-9 favoured run plays out | Woltemade, Nmecha, Stiller |
| "The underdog who got here on vibes" | Scotland's McTominay has been heroic in qualifying — can he replicate in the big show? | McTominay + squad context |
| "Egypt's Marmoush problem" | Egypt face Belgium G1 and draw on paper is tough — but if Marmoush fires, the pts/$ ratio is extraordinary | Omar Marmoush, Salah |
| "The co-host wildcard" | USA and Canada are home nations with boosted crowds and tournament experience. Pulisic/Tillman/Jonathan David all priced at breakout value | Pulisic, Tillman, J.David |

---

## 5. Visual Design

### Colour palette
```
Background (deep navy):   #0A1628
Card surface:             #112240
Accent gold:              #F5A623
Gold highlight:           #FFD700
Text primary:             #E8EDF5
Text secondary:           #8FA3BF
Position DEF:             #4A90D9
Position MID:             #27AE60
Position FWD:             #E8632A
Position GK:              #7B68EE
Breakout badge:           #FF6B35 (orange-red)
Rising badge:             #F5A623 (gold)
Star badge:               #A0A0A0 (grey — established, not the story)
```

### Typography
- Headings: `'Inter', system-ui` — bold, tight letter-spacing
- Stats: monospace (`'JetBrains Mono', monospace`) for numbers
- Body: `system-ui`

### Component styles
- Cards: `border-radius: 12px`, subtle `box-shadow`, `backdrop-filter: blur(8px)` for glass effect
- Player rows: alternating subtle row tints, smooth highlight on hover
- Scatter dots: `cursor: pointer`, scale to 1.4× on hover with drop-shadow
- Tier badges: pill-shaped, colour-coded, uppercase
- Animated stat counters when bracket changes (numbers count up/down over 400ms)

---

## 6. Technology Stack

| Concern | Choice | Reason |
|---------|--------|--------|
| Markup | Vanilla HTML5 | No build step; single-file deliverable |
| Styling | Vanilla CSS (custom properties) | Full control; no framework bloat |
| Interactions | Vanilla JS (ES2020) | Simple enough; no React needed |
| Scatter plot | D3.js v7 (CDN) | Industry standard for this chart type |
| Flags | Unicode country flag emoji | Zero dependency |
| Data | Embedded JSON blob | Self-contained HTML; no CORS issues |
| Fonts | Google Fonts (Inter, JetBrains Mono) | CDN import in `<head>` |

**Single output file**: `analysis/breakout_stars_dashboard.html` (~2,000 lines)  
The data-prep Python script (`scripts/build_dashboard_data.py`) regenerates the embedded JSON and re-writes the HTML.

---

## 7. File Structure

```
wc_repo/
├── scripts/
│   ├── price_value_lookup.py         ← existing
│   ├── build_combined_sheet.py       ← existing
│   └── build_dashboard_data.py       ← NEW: generates JSON, writes HTML
├── analysis/
│   ├── price_value_table.txt         ← existing
│   ├── all_players_by_position.md    ← existing
│   └── breakout_stars_dashboard.html ← NEW: the deliverable
├── data/
│   └── master_sheet.csv              ← existing
├── countries/                        ← existing
├── dashboard_plan.md                 ← THIS FILE
└── ...
```

---

## 8. Implementation Phases

### Phase 1 — Data prep script (`build_dashboard_data.py`)
- Import master_sheet.csv + dicts from price_value_lookup.py
- Compute `pts_per_game`, `breakout_score`, `breakout_tier` for all confirmed players
- Output validated JSON (check for missing prices, zero pts, etc.)
- Target: ~100 lines of Python

### Phase 2 — HTML shell + hero section
- Page structure, CSS variables, typography
- Hero section with static featured players (no JS yet)
- Verify design feels right before adding interactivity

### Phase 3 — Advancement builder
- 12-group grid with click-to-advance
- Probability mode as default
- State management: `advancingTeams = Set<string>`
- Trigger `updateConditionalPts()` on any change

### Phase 4 — Scatter plot (D3)
- Static first, then wired to bracket state
- Tooltip system
- Breakout zone shading

### Phase 5 — Ranked player list
- Reactive sort on bracket change
- Filters/search
- Inline player card expand

### Phase 6 — Storylines + polish
- Editorial cards (static content, dynamic player stats)
- Animated number transitions
- Mobile layout pass
- Cross-browser smoke test

---

## 9. Open Questions / Decisions Needed

1. **Scope of player data**: Show all 1,216 tracked WC players (full dataset) or just the 93 in the priced universe? Recommendation: show all in scatter/list, but only 93 have price data so pts/$ only available for priced players.

2. **WC 2026 wildcard slots**: The 8 best 3rd-place teams qualifying for R32 adds complexity to the bracket builder. Simplest implementation: show group stage advancement only (2 per group = 24), then add a "3rd place wildcard" toggle that auto-advances the 8 highest-ranked 3rd-place finishers.

3. **Conditional pts formula**: The plan uses a linear `pts_per_game × n_games` model. The existing `adj_pts` already bakes in dead-rubber G3 adjustments. Decision needed: use the simple linear model for interactivity (cleaner UX) and note it's an approximation, or try to reconstruct the exact formula.

4. **Mobile layout**: The side-by-side scatter + list layout likely needs to stack on mobile. The advancement builder needs to be scrollable on small screens. Confirm mobile is in scope.
