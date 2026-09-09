#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# O GATE DO GATE — que o que NÃO foi conferido seja DITO (ADR-0123 §3).
#
# ========================= POR QUE ISTO EXISTE =========================
# 🔴 Desde que os registos deixaram de morar ao lado do código, um `confirmed-by: engine:app/js/x.ts` só se
# confere quando alguém passa a raiz da engine. Sem ela, o validador não pode abrir o ficheiro — e a única
# coisa que separa isso de um carimbo é a linha que diz «24 caminhos NÃO conferidos».
#
# ⚠️ UMA DEFESA SEM TESTE É UM COMENTÁRIO. Apagar aquele `print` deixa o validador a imprimir «123 sãos, 0
# problemas» sem ter aberto um único artefacto, e nada em lado nenhum reprova. É a forma exacta do falso
# relatório que este projecto já apanhou três vezes: uma varredura vazia lida como ausência.
#
# 📌 SEM DEPENDÊNCIAS E SEM RUNNER: este repositório guarda registos, não uma aplicação. `python
# scripts/test-validate-adr.py` corre, sai 0 ou 1, e a CI lê o código de saída — que é o mesmo contrato do
# validador ao lado.
#
# MUTAÇÕES CONFERIDAS (no fim do ficheiro).
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
VALIDADOR = os.path.join(AQUI, "validate-adr.py")

REGISTO = """---
metadata:
  shape: bundle
  status: "accepted"
  date: 2026-09-09
  decision-makers: [Dev]
  consulted: []
  informed: []
{confirmed}
title: {titulo}
context-and-problem-statement: |
  Um registo de fixture. Existe para o validador ter o que ler.
decision-outcome:
  justification: |
    Nada a decidir: este registo existe para exercitar o crivo.
more-information: |
  Nada.
"""


def escreve(pasta, numero, titulo, confirmed=""):
    caminho = os.path.join(pasta, f"ADR-{numero:04d}-fixture.yaml")
    with open(caminho, "w", encoding="utf-8") as fh:
        fh.write(REGISTO.format(titulo=titulo, confirmed=confirmed))
    return caminho


def corre(*args):
    # ⚠️ `encoding="utf-8"` E NÃO O PADRÃO: o validador imprime ⚠️ e 📌, e em Windows o `text=True` decodifica
    # com o cp1252 da consola — o que rebenta com `UnicodeDecodeError` antes de qualquer asserção correr.
    # Apanhado a correr, na primeira tentativa. `errors="replace"` para o caso nunca morrer por um byte.
    r = subprocess.run(
        [sys.executable, VALIDADOR, *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return r.returncode, (r.stdout or "") + (r.stderr or "")


falhas = []


def exige(condicao, porque):
    if not condicao:
        falhas.append(porque)


with tempfile.TemporaryDirectory() as base:
    adr = os.path.join(base, "adr")
    engine = os.path.join(base, "engine-de-mentira")
    os.makedirs(adr)
    os.makedirs(engine)
    with open(os.path.join(engine, "existe.ts"), "w", encoding="utf-8") as fh:
        fh.write("// o artefacto que confirma o registo\n")

    escreve(adr, 1, "com confirmação noutro repositório",
            "  confirmed-by:\n    - engine:existe.ts")
    escreve(adr, 2, "sem confirmação nenhuma")

    # [Vácuo] — antes de tudo: o crivo ACHA a fixture. Sem isto, um validador que não lesse nada passaria
    # todos os casos abaixo por não ter o que reprovar.
    codigo, saida = corre(adr)
    exige("2 records" in saida, f"o validador não leu a fixture — mediria o nada. Saída:\n{saida}")

    # 🎯 [Zero] SEM a raiz da engine: são sãos, E a linha do que não foi conferido aparece.
    exige(codigo == 0, f"a fixture devia ser sã sem `--repo`; saiu {codigo}. Saída:\n{saida}")
    exige("NOT checked" in saida,
          "o validador CALOU-SE sobre o que não conferiu — é um carimbo, não um crivo. "
          f"Saída:\n{saida}")
    exige("`engine`" in saida, f"a linha não nomeia o repositório que falta. Saída:\n{saida}")

    # [Right] COM a raiz certa: confere de verdade, e deixa de avisar.
    codigo, saida = corre(adr, "--repo", f"engine={engine}")
    exige(codigo == 0, f"com a raiz certa devia sair 0; saiu {codigo}. Saída:\n{saida}")
    exige("NOT checked" not in saida,
          f"avisou que não conferiu, com a raiz na mão. Saída:\n{saida}")

    # 🔴 [Boundary] UM PREFIXO QUE NINGUÉM DECLAROU é problema, e não «não conferido». Era o caso que o
    # ADR-0123 dizia não poder pagar, e a frase estava mal posta: o risco não é o repositório mudar de nome, é
    # o rótulo nunca ter existido — e um erro de escrita ficava a viver dentro da mensagem do dia a dia.
    escreve(adr, 3, "com um prefixo que não existe",
            "  confirmed-by:\n    - enigne:existe.ts")
    codigo, saida = corre(adr)
    exige(codigo != 0, f"prefixo desconhecido devia reprovar; saiu {codigo}. Saída:\n{saida}")
    exige("not a declared repository" in saida,
          f"reprovou, mas não pela razão certa. Saída:\n{saida}")
    os.remove(os.path.join(adr, "ADR-0003-fixture.yaml"))

    # 🔴 [Inverse] COM a raiz errada: reprova, e a mensagem diz contra o que mediu.
    codigo, saida = corre(adr, "--repo", f"engine={os.path.join(base, 'nao-existe')}")
    exige(codigo != 0, f"raiz errada devia reprovar; saiu {codigo}. Saída:\n{saida}")
    exige("existe.ts" in saida, f"a reprovação não nomeia o caminho. Saída:\n{saida}")
    exige("nao-existe" in saida,
          f"a reprovação não diz contra QUE raiz mediu — parece um registo mentiroso. Saída:\n{saida}")

    # ======================= o ÍNDICE, que drenou sete registos em silêncio =======================
    indice = os.path.join(adr, "README.md")

    # [Vácuo] PRIMEIRO, e é o caso que importa mais: sem `README.md` o crivo SALTA, e tem de saltar —
    # uma árvore de registos sem índice não é uma árvore partida. ⚠️ Mas um salto que ninguém afirma é
    # como um crivo desligado: se o `os.path.exists` virasse `True` constante, nada abaixo notava.
    codigo, saida = corre(adr)
    exige(codigo == 0, f"sem índice nenhum devia saltar e sair 0; saiu {codigo}. Saída:\n{saida}")
    exige("no row in the index" not in saida,
          f"acusou índice em falta numa árvore que não tem índice nenhum. Saída:\n{saida}")

    # [Right] com um índice que nomeia UM dos dois, o outro é acusado — e o acusado é o que falta.
    with open(indice, "w", encoding="utf-8") as fh:
        fh.write("| ADR | Decision | Status |\n|---|---|---|\n"
                 "| [ADR-0001](ADR-0001-fixture.yaml) | a que está | accepted |\n")
    codigo, saida = corre(adr)
    exige(codigo != 0, f"registo fora do índice devia reprovar; saiu {codigo}. Saída:\n{saida}")
    exige("ADR-0002" in saida, f"reprovou sem nomear QUAL registo falta. Saída:\n{saida}")
    exige("ADR-0001" not in saida.replace("ADR-0001-fixture.yaml", ""),
          f"acusou também o registo que TEM linha. Saída:\n{saida}")

    # 🎯 [Boundary] SER MENCIONADO NÃO É TER LINHA, e é exactamente assim que os sete se esconderam:
    # um registo citado dentro da prosa de outra linha aparece a um `grep` e continua sem entrada.
    with open(indice, "w", encoding="utf-8") as fh:
        fh.write("| ADR | Decision | Status |\n|---|---|---|\n"
                 "| [ADR-0001](ADR-0001-fixture.yaml) | supersede em parte o ADR-0002 | accepted |\n")
    codigo, saida = corre(adr)
    exige(codigo != 0,
          f"o ADR-0002 só é MENCIONADO na prosa de outra linha e mesmo assim passou; saiu {codigo}. "
          f"Saída:\n{saida}")

    # [Inverse] com os dois indexados, verde outra vez — senão seria um gate que nunca pode ficar verde.
    with open(indice, "w", encoding="utf-8") as fh:
        fh.write("| ADR | Decision | Status |\n|---|---|---|\n"
                 "| [ADR-0001](ADR-0001-fixture.yaml) | a primeira | accepted |\n"
                 "| [ADR-0002](ADR-0002-fixture.yaml) | a segunda | accepted |\n")
    codigo, saida = corre(adr)
    exige(codigo == 0, f"com os dois no índice devia sair 0; saiu {codigo}. Saída:\n{saida}")

if falhas:
    for f in falhas:
        print(f"FAIL {f}")
    print(f"\n{len(falhas)} problema(s)")
    raise SystemExit(1)
print("validador: o que não é conferido é dito, e o que é conferido reprova quando falta")

# ================================ MUTAÇÕES CONFERIDAS ================================
# 1. apagar o laço que imprime `NOT checked` no `main()` → o caso [Zero] reprova. É a mutação inteira: sem
#    ela, o validador diz «tudo são» sem ter aberto um artefacto, e nenhum outro caso nota.
# 2. contar o não-conferido como PROBLEMA em vez de o saltar → o caso [Zero] reprova pelo código de saída.
#    Seria a outra maneira de errar: um repositório que só tem registos ficaria vermelho para sempre, e um
#    gate que nunca pode ficar verde é um gate que alguém desliga.
# 3. tirar o `--repo` do parser (voltar a resolver tudo contra o `cwd`) → o [Right] reprova: os caminhos
#    qualificados deixariam de ser encontrados mesmo com a raiz correcta.
# 4. o crivo do índice a procurar `ADR-\d{4}` em qualquer posição da linha em vez de `^\| \[ADR-\d{4}\]`
#    → o [Boundary] reprova. É a mutação que mais importa deste bloco, porque é a forma REAL do defeito:
#    os sete registos que faltavam apareciam todos a um `grep` por número, citados na prosa de outras
#    linhas, e um crivo assim teria dito «está tudo indexado» durante os sete.
# 5. trocar o `os.path.exists(indice)` por `True` → o [Vácuo] reprova com um traceback em vez de saltar.
#    Ao contrário, fixá-lo em `False` deixa o bloco inteiro verde para sempre — e é o [Right] que a apanha.
