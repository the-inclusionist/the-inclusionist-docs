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

## 2026-09-13 · «Voz» sits after the narration volume

⚠️ The row is the Dev's (ADR-0185); its PLACE was chosen while building and NOT YET SEEN by the Dev. «Voz» follows «Volume da narração» and precedes «Índice falado dos menus», so the voice block reads switch, volume, voice. Names shown are the middle of the provider's id («Faber», «Ryan», «Amy», «Claude»). `engine:9d0f5e5`, issue #180.

## 2026-09-13 · Rates read «125 PPM», and a menu is not a manual

«Em acessibilidade visual, o ritmo das legendas está com a explicação no lugar errado. E você deve abreviar palavras por minuto para PPM. Menu não é manual de instruções.» A rate's value is «125 PPM» (WPM in English), and a row's explanation is one short sentence, in the footer. `engine:` the commit after `e61d571`, issue #179.

## 2026-09-13 · A settings panel wears the pause card, and every menu card has one height

«Ao clicar em configurações de inclusão, o menu mantem a mesma altura e identidade visual. Para além disso, todos os submenus
estão com outra identidade visual, com alturas menores, título maior e cores diferentes. Corrija.» A panel takes the pause card as
it is — the whole height, the dark card with the gold border, the gold title at the text size, rows in the pause items' fill,
border and radius with 2 px gaps — and is at least the pause card's width, wider only when a steps row needs it (the visual
panel, 602 px at 640×360, because of the BDA spacing). The root card, whose six items had shrunk it 46 px, holds the whole height
too. The panel runs under the explanation band, and its last row scrolls above it. `engine:d5b4c10`, `engine:36ca8d6`.

## 2026-09-13 · The help is a slide show

«Ao clicar em ajuda a tela se assemelha a um menu e inclusive tem um botão "restaurar padrões deste menu" quando na verdade deveria
conter uma "apresentação de slides" (textos, figuras e no máximo animações).» One slide per position the game names: the child's
key drawn as a key cap that presses itself now and then (off under reduced motion), the game's word and its sentence, dots for
the place; left and right turn the page, the ends are walls. No reset, no footer band. ⚠️ The slide's LAYOUT was chosen while
building and is NOT YET SEEN by the Dev; it shows what the engine knows (key, word, sentence) — a game's own «how to play» slides
would be a contract field, not drawn here. `engine:e9a24d1`.

## 2026-09-14 · A game's «how to play» slide: figure above, text below

⚠️ The slide's LAYOUT was chosen while building ADR-0195 and is NOT YET SEEN by the Dev. A cartridge's slide shows its figure on
top (up to 16 em wide, 7 em tall) and its text under it, with the same arrows and dots as the button slides; the game's slides
come first. The house quiz tells how to play in two slides, the second animating the marked option down. `engine:a85bfee`.

## 2026-09-14 · «Ritmo da fala» sits after the narration volume, and starts at 150 PPM

⚠️ The rate is the Dev's (ADR-0183 §1); its PLACE and its DEFAULT were chosen while building and are NOT YET SEEN by the Dev. The
row is a list («150 PPM» … «500 PPM», eleven steps) after «Volume da narração», before «Voz». It starts at 150, the slowest step,
as the caption rate starts at its slowest; at 150 the Faber voice (255 PPM of speech, measured) plays at about 0.59×.
`engine:c3a0097`, issue #179.

## 2026-09-14 · The speech rate starts at the voice's normal speed

The entry above chose 150 PPM as the default. The Dev: «Nada disso, velocidade normal é a mínima (254?, e deve poder aumentar de 50
em 50 até ~500ppm, isto é, 504ppm)». The steps become 254–504 by 50, starting at 254, and no voice plays under 1× — a record
(ADR-0196), since it changes ADR-0183's steps. The row keeps its place after the narration volume.
## 2026-09-16 · The eye control's regions: where they sit, their size, and the colours of a look

⚠️ Chosen in the lab while building the Dev's presentation (ADR-0213 §6) and seen by the Dev only through the lab, not in the engine. The
four regions sit at the edges of the game region and the middle at its centre, as fractions of it: north and south 26% × 18% at 10% from
the top and bottom edge, east and west 24% × 24% at 13% from the side edge, the middle 24% × 26%. A region nobody looks at is outlined and
hatched faintly; a look that prepares draws it amber (#ffd23f), an armed look green (#3ddc84), with a 3 px outline. The face button's two
circles sit side by side. Lab `apresentacao.js`; engine issue #194.

## 2026-09-16 · The eye control in the engine: the eye lines and no dark wash

⚠️ Chosen while porting the lab to `engine:ui/gaze-overlay` and not yet seen by the Dev in the engine. The eyes, irises and brows are drawn
as white lines 2 px wide (growing with the text) with a soft black shadow, both eyes the same colour — the lab drew the left eye green and
the right one red, which reads as a state colour beside the amber and green of a look. The lab's dark wash under each region (35% navy) is
left out: over a game it would darken the game itself at every level; the outline, and at the hatched level the hatching, mark the
regions instead. Engine issue #194.

## 2026-09-16 · The quick bar's hand icons: 🤟 is gestures, 🦻 is the deaf person

The Dev: «O ícone para jogar por gestos é 🤟, a partir de agora o ícone da pessoa surda deve ser 🦻». The Libras / deaf-mode icon changed
its glyph from 🤟 to 🦻 (`engine:ui/pause-icons`); its key, name and behaviour did not. 🤟 is kept for the hand-gestures toggle, which the
bar does not have yet (issue #191). Seen by the Dev only as this decision, not yet in the engine.
