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
import shutil
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

    # ============ CITAÇÕES ENTRE ÁRVORES (ADR-0229): um registo mudou-se para um jogo ============
    # A árvore de casa (`adr`) cita o 0005, que mora no jogo; a árvore do jogo cita o 0001, que ficou em casa.
    jogo = os.path.join(base, "jogo")
    arvore_do_jogo = os.path.join(jogo, "docs", "2-Architecture", "adr")
    os.makedirs(arvore_do_jogo)
    escreve(arvore_do_jogo, 5, "o registo do jogo, que cita o ADR-0001 que ficou em casa")
    escreve(adr, 4, "cita o ADR-0005, que se mudou para o jogo")
    casa_sem_linha = ("| ADR | Decision | Status |\n|---|---|---|\n"
                      "| [ADR-0001](ADR-0001-fixture.yaml) | a primeira | accepted |\n"
                      "| [ADR-0002](ADR-0002-fixture.yaml) | a segunda | accepted |\n"
                      "| [ADR-0004](ADR-0004-fixture.yaml) | a quarta | accepted |\n")
    linha_movida = ("| [ADR-0005](game-platformer:docs/2-Architecture/adr/ADR-0005-fixture.yaml) "
                    "| mudou-se | accepted |\n")
    with open(indice, "w", encoding="utf-8") as fh:
        fh.write(casa_sem_linha)

    # 🔴 [Boundary] sem linha nem `--repo`, a citação ao 0005 REPROVA — nunca vira «não conferido», senão o
    # erro de um dígito do ADR-0010 passaria a viver dentro da mensagem de que está tudo bem.
    codigo, saida = corre(adr)
    exige(codigo != 0 and "cites ADR-0005" in saida,
          f"uma citação que nenhuma árvore responde passou; saiu {codigo}. Saída:\n{saida}")

    # 🎯 [Zero] com a linha «mudou-se» e SEM a raiz do jogo: verde, e a linha é CONTADA e dita.
    with open(indice, "w", encoding="utf-8") as fh:
        fh.write(casa_sem_linha + linha_movida)
    codigo, saida = corre(adr)
    exige(codigo == 0, f"a linha «mudou-se» devia responder pela citação; saiu {codigo}. Saída:\n{saida}")
    exige("index rows moved to `game-platformer` NOT checked" in saida,
          f"a linha movida não foi conferida e o validador calou-se. Saída:\n{saida}")

    # [Right] COM a raiz do jogo: confere o ficheiro do outro lado, e deixa de avisar.
    codigo, saida = corre(adr, "--repo", f"game-platformer={jogo}")
    exige(codigo == 0 and "index rows moved" not in saida,
          f"com a raiz do jogo devia conferir e calar; saiu {codigo}. Saída:\n{saida}")

    # 🔴 [Inverse] a linha aponta para um ficheiro que não está lá: reprova o ÍNDICE.
    os.rename(os.path.join(arvore_do_jogo, "ADR-0005-fixture.yaml"), os.path.join(arvore_do_jogo, "fora.yaml"))
    codigo, saida = corre(adr, "--repo", f"game-platformer={jogo}")
    exige(codigo != 0 and "FAIL README.md" in saida,
          f"a linha «mudou-se» aponta para nada e passou; saiu {codigo}. Saída:\n{saida}")
    os.rename(os.path.join(arvore_do_jogo, "fora.yaml"), os.path.join(arvore_do_jogo, "ADR-0005-fixture.yaml"))

    # 🔴 [Boundary] um rótulo que ninguém declarou na linha «mudou-se» reprova, pela mesma razão do
    # `confirmed-by`: contá-lo como «não conferido» esconderia o erro de escrita na mensagem do dia a dia.
    with open(indice, "w", encoding="utf-8") as fh:
        fh.write(casa_sem_linha + linha_movida.replace("game-platformer:", "game-platfromer:"))
    codigo, saida = corre(adr)
    exige(codigo != 0 and "not a declared repository" in saida,
          f"uma linha com rótulo errado passou; saiu {codigo}. Saída:\n{saida}")
    with open(indice, "w", encoding="utf-8") as fh:
        fh.write(casa_sem_linha + linha_movida)

    # 🔴 [Inverse] o ficheiro ficou em casa E a linha diz que se mudou: uma das duas está velha.
    escreve(adr, 5, "a cópia que ficou para trás")
    codigo, saida = corre(adr, "--repo", f"game-platformer={jogo}")
    exige(codigo != 0 and "one of the two is stale" in saida,
          f"um registo em duas casas passou; saiu {codigo}. Saída:\n{saida}")
    os.remove(os.path.join(adr, "ADR-0005-fixture.yaml"))

    # O outro lado: a árvore do JOGO cita o 0001. Sem a casa declarada reprova; com ela, é são.
    codigo, saida = corre(arvore_do_jogo)
    exige(codigo != 0 and "cites ADR-0001" in saida,
          f"a árvore do jogo citou o que não tem e passou sem `--repo`; saiu {codigo}. Saída:\n{saida}")
    # A árvore de casa é copiada para a forma de um repositório (`<raiz>/docs/2-Architecture/adr`), que é
    # onde o validador procura — a fixture `adr` solta não tem essa forma.
    casa = os.path.join(base, "casa")
    shutil.copytree(adr, os.path.join(casa, "docs", "2-Architecture", "adr"))
    codigo, saida = corre(arvore_do_jogo, "--repo", f"docs={casa}")
    exige(codigo == 0, f"com a casa declarada a árvore do jogo devia ser sã; saiu {codigo}. Saída:\n{saida}")

    # 🔴 [Boundary] declarar a PRÓPRIA árvore não a deixa responder por si: o índice dela tem uma linha para o
    # 0009 sem ficheiro nenhum, e essa linha não pode passar a valer como prova só porque o `--repo` a aponta.
    escreve(arvore_do_jogo, 6, "cita o ADR-0009, que não existe em lado nenhum")
    with open(os.path.join(arvore_do_jogo, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("| ADR | Decision | Status |\n|---|---|---|\n"
                 "| [ADR-0005](ADR-0005-fixture.yaml) | a quinta | accepted |\n"
                 "| [ADR-0006](ADR-0006-fixture.yaml) | a sexta | accepted |\n"
                 "| [ADR-0009](ADR-0009-fixture.yaml) | uma linha sem ficheiro | accepted |\n")
    codigo, saida = corre(arvore_do_jogo, "--repo", f"docs={casa}", "--repo", f"game-platformer={jogo}")
    exige(codigo != 0 and "cites ADR-0009" in saida,
          f"um número que nenhuma árvore tem passou; saiu {codigo}. Saída:\n{saida}")

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
#
# CITAÇÕES ENTRE ÁRVORES (ADR-0229), 9 de 9 vermelhas em 2026-09-23:
# 6. a outra árvore declarada deixar de responder → a árvore do jogo, com a casa declarada, reprova.
# 7. a linha «mudou-se» deixar de responder → o [Zero] da casa reprova.
# 8. a árvore que se valida responder por si quando o `--repo` a aponta → o [Boundary] do 0009 fica verde.
# 9. um registo com ficheiro em casa E linha «mudou-se» passar → o [Inverse] das duas casas reprova.
# 10. um rótulo errado na linha «mudou-se» ser CONTADO em vez de reprovar → o [Boundary] do rótulo reprova.
# 11. o ficheiro do outro lado não ser conferido → o [Inverse] do ficheiro em falta reprova.
# 12. calar a contagem das linhas movidas → o [Zero] reprova. É a mutação 1, um andar abaixo.
# 13. a reprovação do índice sair 0, e 14. deixar de a imprimir → o [Inverse] do ficheiro em falta reprova.
#    O índice não é um registo e não entra na conta «N records», mas uma linha que aponta para nada é a
#    mesma mentira que um `confirmed-by` a apontar para nada.
