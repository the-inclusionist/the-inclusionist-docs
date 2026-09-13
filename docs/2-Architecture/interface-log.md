# Interface log

The two-way doors of the interface (ADR-0172): choices a commit can reverse — layout, order, wording, which items show,
spacing. One-way doors — the contract, the public surface, stored keys, packages, licences, privacy — are records in
`adr/`.

**Form of an entry.** A dated heading, the Dev's words quoted, what was decided in one or two sentences, and the commit or
issue. A changed decision gets a new entry below; the old one stays. Newest last.

<!-- entries start below -->

## 2026-09-13 · The quiz's options at 640×360: 4 px apart, 2 px above the footer

Asked whether the quiz may keep its options 4 px apart with 2 px to spare above the footer (the cost of reserving the
icon-name line under the quick bar, issue #160): «Ficou bom». The spacing of `engine:4f111ec` stays.

## 2026-09-13 · The HUD's look: dark chips, and the learning bar's cues besides colour

⚠️ Chosen while building issue #162 and NOT YET SEEN by the Dev — no Dev words to quote. Identity and round numbers are
text on the same dark chip as the icon's name; the learning bar's segments are Okabe-Ito (blue #0072B2, green #009E73,
red #D55E00; a purple #CC79A7 or orange #E69F00 bar covers them), with a second cue each so no state is told by colour
alone (WCAG 1.4.1): green a dot, red stripes, an empty slot only its outline, a purple bar ▲ and an orange one ▼.
`engine:2e83917`, `engine:a998e33`.

## 2026-09-13 · The learning bars: position and size approved

Shown the demo page of the HUD (three ten-segment bars centred in the footer, Okabe-Ito with a cue besides colour): «As barras
de ganho na parte de baixo estão bem posicionadas e num tamanho bom, aprovo.» The bars of `engine:a998e33` stay. The rest of
that demo's layout changed by a record (ADR-0175).
