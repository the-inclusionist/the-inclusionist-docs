# the-inclusionist-docs

**The decisions of the whole project live here.** One tree, one supersession graph, one place a reader goes to
find out what was decided — for the engine, the games, Bússola Escolar, the site, the knowledge tree and
whatever comes next (ADR-0123, which decides this and declares this address).

## What is here today

```
docs/2-Architecture/adr/     123 records (YADR) + README.md, the index
scripts/validate-adr.py      the validator: form, supersession pairs, and `confirmed-by`
.github/workflows/ci.yml     the gate that runs it on every push
```

⚠️ **The path is deliberate.** The records keep `docs/2-Architecture/adr/` — the address they had in the
engine — so that every link written inside a hundred and twenty-three records keeps working, and so the other
SDD phases can follow later without a second reorganisation. This repository is named for DOCUMENTS: the ADR
tree is its first tenant, not its only one.

## Running the validator

```bash
python scripts/validate-adr.py                       # form, pairs, and local paths
python scripts/validate-adr.py --repo engine=../SP-the-inclusionist-tracer
```

🔴 **The second line is not optional rigour — it is the only way the `confirmed-by` paths get opened.** A
record that says it was BUILT names the artefacts that prove it, and 24 of those live in the engine. Without
`--repo`, the validator says so, out loud, on every run:

```
123 records · 123 sound · 0 with problems
⚠️  24 `confirmed-by` paths in `engine` NOT checked — pass `--repo engine=<path>` to check them
```

A sieve that checks nothing and prints «all sound» is worse than no sieve. That line is the difference.

## Where the gates are

📌 **The tree is concentrated; the validators and the gates are not** (ADR-0123 §4, the Dev's rule). Every
repository keeps an `adr` job of its own, checks this tree out, and runs the validator against it — the
engine's job passes `--repo engine=.`, because it is the only one holding the code those 24 paths name.

⚠️ **And this repository's CI does NOT check out the engine.** A record pointing at an engine artefact that
disappeared is the engine's breakage, and it has to redden where somebody can fix it.

## The rules a record follows

- **A record changes by SUPERSESSION; errata is the only edit in place** (ADR-0057). The validator enforces
  the pair in both directions — a `supersedes-in-part` with no back-pointer fails.
- **A record says what it decided, and `confirmed-by` says whether it was BUILT.** The prose of `confirmation`
  is historical and is not rewritten; `confirmed-by` is today's fact and lives in the metadata.
- **`confirmed-by` entries carry their repository**: `engine:app/js/x.ts`. An unqualified path resolves
  against this repository.

## Licence

The records are documentation of a project whose code is AGPL-3.0-or-later. See the engine's `docs/LICENSES.md`
for the full picture — art is not FOSS and is governed separately.
