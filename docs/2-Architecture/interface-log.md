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

## 2026-09-13 · A face with a 20 px floor enlarges its own text, not the whole document

Shown that at 640×360 the quiz's last option drops into the footer when a face with a 20 px floor (text 25% larger) is
chosen, with three things that could yield — the gap between options, the footer band while no explanation shows, or the
face enlarging only its own text: «Apertando ctrl + - até o zoom chegar a 25% a fonte não diminuiu de tamanho mais uma série
de espaços sim, mantendo o design muito bom. Quais espaços diminuiram? Seja quais forem, estes é que devem ser atacados. Por
isso minha intuição diz que a face de piso 20 deve aumentar só o próprio texto, sem aumentar o documento inteiro.» The floor
scale applies to text, not to spacing; and the spaces that shrink under browser zoom-out while text holds its floor are
measured and named, since those are the ones to reduce. Issue #172.

## 2026-09-13 · A sound caption stays for its words

⚠️ Chosen while building plan phase 5c and NOT YET SEEN by the Dev — no Dev words to quote. The sound caption left after a
fixed 2600 ms; it now stays 500 ms a word (120 words a minute, the low end of the BBC subtitle guidelines' rate for children's
programmes), never under 2600 ms. `engine:2bd2826`. A reading-pace preference for early readers would be a stored setting,
and is a question, not this entry.

## 2026-09-13 · The quick bar sits on the screen's top edge; speed and toggle keys are two buttons

Asked where the game speed goes: «No painel de acessibilidade rápida (ícone de dedo, já existe no Platformer inclusive). Importante: eleve este painel para que compartilhe a borda com a tela e ceda mais pixels para o restante do jogo.» And, on reading that the finger icon's panel would hold the speed: «De forma alguma. Um botão para alternância e outro para velocidade.» The quick bar loses its 10 px from the top and sits on the edge, giving that room to the game; the game speed is its own ⏳ button (ADR-0180), beside ☝️ toggle keys. Issue #176.
