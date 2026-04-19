# Ads Budget Research — Tandartspraktijk Zuyderhoven

**Datum:** 2026-04-19
**Doel:** Realistisch Google Ads budget bepalen voor 3 stads-keywords over 3 maanden.

---

## CPC-benchmarks (public bronnen)

| Markt | Gemiddeld CPC tandarts | Range |
|---|---|---|
| US algemeen | $7,85 | $2–12 |
| US grote stad (Manhattan) | $7,85+ | — |
| US kleine plaats | $2–3 | — |
| US implantaat/specialistisch | — | $12–25 |
| EU algemeen | — | $0,20–$5+ |
| **NL tandarts geschat** (60–70% van US) | **€3–5** | **€1,50–7** |

Bronnen: Dentx, Causal Funnel, UpROAS, Searchlab NL.

> Exact NL CPC per keyword ontbreekt in publieke data — Google Keyword
> Planner (via onze Google Ads MCP na setup) geeft de definitieve cijfers.

## Geschatte CPC per keyword (NL, April 2026)

| Keyword | Markt | Geschat CPC | Redenering |
|---|---|---|---|
| tandarts Amstelveen | 37 praktijken concurrent, 90k inw | €3–5 | Hoge competitie, mid-size stad |
| tandarts Amstelveen inschrijven | Long-tail, hoge intentie | €2–4 | Minder bids op long-tail |
| tandarts Aalsmeer | 33k inw, weinig concurrentie | €1,50–3 | Kleine markt |
| tandarts Uithoorn | 30k inw, weinig concurrentie | €1,50–3 | Kleine markt |
| tandarts spoed Amstelveen | Hoge intentie, spoed-premium | €4–7 | Spoed-keywords duurder |
| implantaat tandarts Amstelveen | Specialistisch | €8–15 | Implantaat sector-premium |
| tanden bleken Amstelveen | Cosmetisch | €3–6 | Mid-range |

## Geschatte zoekvolumes (maandelijks, ruwe schatting op bevolking × intent-ratio)

| Keyword | Zoekopdrachten/mnd (geschat) |
|---|---|
| tandarts Amstelveen | 500–1.500 |
| tandarts Aalsmeer | 150–400 |
| tandarts Uithoorn | 150–400 |
| tandarts Kudelstaart | 50–100 |
| tandarts De Kwakel | 10–30 |

> Pas verifiëren na Google Keyword Planner access (via MCP).

## Budget-advies

**Startup fase (maand 1–2):** conservatief beginnen, data verzamelen.

| Stad | Dagbudget | Weekbudget | Verwachte clicks/week |
|---|---|---|---|
| Amstelveen | €3,50 | €25 | 5–8 |
| Aalsmeer | €1,50 | €10 | 3–6 |
| Uithoorn | €1,50 | €10 | 3–6 |
| **Totaal** | **€6,50** | **€45** | **11–20** |

Maand-budget fase 1: **€180–195**.

**Groei-fase (maand 3+):** opschalen op de keywords die converteren.

| Stad | Weekbudget | Verwachte clicks/week |
|---|---|---|
| Amstelveen | €40 | 8–13 |
| Aalsmeer | €15 | 5–10 |
| Uithoorn | €15 | 5–10 |
| **Totaal** | **€70** | **18–33** |

Maand-budget fase 2: **€280–300**.

## ROI-sanity check

Aannames (branche-gemiddelden):
- Landing page → inschrijving conversie: 2–5% (bij goede landing)
- Lifetime waarde nieuwe tandarts patiënt: €500–2.500
- Benodigd voor break-even: 1 nieuwe patiënt per €500 ad-spend

**Fase 1 berekening:**
- €45/week × 4 = €180/maand
- 15 clicks/week × 3% conv = ~2 leads/week = ~8/maand
- Van leads naar afspraken: ~40% = **3 nieuwe patiënten/maand**
- 3 × €500 LTV = €1.500 waarde vs €180 spend = **ROI ~8×** (conservatief gerekend)

**Fase 2 berekening:**
- €70/week × 4 = €280/maand
- 25 clicks/week × 3% conv = ~3 leads/week = ~12/maand
- 40% show-up rate = **~5 nieuwe patiënten/maand**
- 5 × €500 LTV = €2.500 vs €280 spend = **ROI ~9×**

## Aanbeveling

1. **Start met Fase 1 (€45/week = €180/maand) gedurende 4–6 weken.**
2. Meet: clicks, CTR, conversions, kosten-per-lead, kosten-per-nieuwe-patiënt.
3. Schakel naar Fase 2 (€70/week) pas na bewezen ROI.
4. Herinvestering-regel: zodra 1 patiënt/maand uit ads komt met LTV ≥€500, budget mag 50% omhoog.
5. Blijf conservatief op "implantaat" keywords (CPC €8–15) tot we weten dat de landingspagina converteert.

## Niet-verifieerbaar zonder credentials

Deze schattingen zijn gebaseerd op publieke benchmarks + marktlogica.
Voor exacte cijfers heb ik nodig:
- Google Ads Keyword Planner toegang (via MCC of eigen account)
- Of iemand met Ahrefs / SEMrush die NL search volume data heeft

Na setup van de `google-ads-tpzuyderhoven` MCP server kan ik
`generate_keyword_ideas` draaien voor exacte CPC + volume data.

## Bronnen

- https://dentx.ca/blog/google-ads-for-dentists/
- https://www.causalfunnel.com/blog/google-ads-for-dentists-in-2026-the-complete-guide-to-maximize-roi-and-new-patients/
- https://www.uproas.io/blog/google-ads-benchmarks
- https://searchlab.nl/en/statistics/google-ads-statistics-2026
- https://www.digitalapplied.com/blog/google-ads-benchmarks-2026-cpc-ctr-cvr-industry
- https://clickpatrol.com/ppc-costs-in-europe-2025-how-to-budget-optimize/

Lokale referentie-data:
- https://tandartsregister.nl/tandarts/amstelveen (37 praktijken in Amstelveen)
