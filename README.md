# the-inclusionist-docs

**The decisions that belong to the whole project live here** — the ones no single repository owns: the pillars,
privacy and compliance, the organisation and its repositories, licences and art, the catalogue, and the project's
governance. The engine's records live in the engine, and a game's own in that game (ADR-0242, which decides this;
ADR-0226 §1 for the games).

## What is here today

```
docs/2-Architecture/adr/     the project-wide records (YADR) + README.md, the index — with a row for EVERY record
                             of the project, local or pointing at the repository that holds it
scripts/validate-adr.py      the validator: form, supersession pairs (across repositories too), `confirmed-by`
scripts/test-validate-adr.py the validator's own gate
scripts/tempo-dos-registos.py    a record with `confirmed-by` does not say it is still to be built (ADR-0128)
scripts/divida-dos-registos.py   the records that owe work nobody can find (ADR-0126), and its test
.github/workflows/ci.yml     the gate that runs them on every push
```

📌 **The five scripts exist, identical, in the engine too**, because both repositories keep records and «cada
repositório precisa ter seus validadores e gates para ADRs». The engine's drift gate compares them file by file; a
change to one is made in both, in the same change.

## Which tree a record goes to

**Whose repository breaks or must change if this decision changes?** Every repository, or none in particular → here.
The engine's code, the contract it publishes, the UI it draws, delivery, accessibility → the engine. One game → that
game. The reading of every record that lived here on 2026-09-26 is in the engine's
`docs/2-Architecture/record-ownership-triage.md`. Numbers are one sequence for the whole project.

⚠️ Three records here read as `game-platformer`'s — ADR-0045, ADR-0060, ADR-0237 — and wait for a move made in that
repository. Six more belong to systems with no records tree of their own yet: the labs (ADR-0023) and the pixel-data
pipeline (ADR-0134 to 0138).

## Running the validator

```bash
python scripts/validate-adr.py docs/2-Architecture/adr --repo docs=.          # what crosses is counted
python scripts/validate-adr.py docs/2-Architecture/adr --repo docs=. \
    --repo engine=../the-inclusionist-engine --repo game-platformer=../game-platformer   # and opened
```

🔴 **Without `--repo engine=…` the validator says, on every run, what it did not open**: the `engine:` confirmations,
the index rows that point at the engine, and the supersession pointers whose other half lives there. A sieve that
checks nothing and prints «all sound» is worse than no sieve. That line is the difference.

## Where the gates are

This repository's CI validates what it keeps and **does not check out the engine** (ADR-0123 §5): a record naming an
engine artefact that disappeared is the engine's breakage, and it must redden where somebody can fix it. The engine's
own `adr` job is what opens those confirmations, with `--repo engine=.`, against a checkout of this repository.

## The rules a record follows

- **A record changes by SUPERSESSION; errata is the only edit in place** (ADR-0057). The validator enforces the pair in
  both directions — also when the other half lives in another repository and its root is declared.
- **A record says what it decided, and `confirmed-by` says whether it was BUILT.** The prose of `confirmation` is
  historical and is not rewritten; `confirmed-by` is today's fact and lives in the metadata.
- **`confirmed-by` entries carry their repository**: `engine:app/js/x.ts`. An unqualified path resolves against this
  repository.

## Licence

The records are documentation of a project whose code is AGPL-3.0-or-later. See the engine's `docs/LICENSES.md` for
the full picture — art is not FOSS and is governed separately.
