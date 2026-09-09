#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""O CENSO DA DIVIDA CONTINUA VIVO — um relatorio que morre em silencio imprime «0» para sempre.

O `divida-dos-registos.py` REPORTA e nunca reprova, de proposito (ADR-0126). E precisamente por isso precisa
deste ficheiro: um gate que reprova e lido no dia em que fica vermelho; um relatorio cujo detector morreu
continua a imprimir numeros — zeros — e ninguem volta a olhar. Este repositorio ja pagou isso: uma varredura
devolveu ZERO e quase virou «nao ha CDN nenhum».

Os casos correm sobre uma arvore TEMPORARIA, escrita aqui, com o VACUO primeiro.
MUTACOES CONFERIDAS no fim do ficheiro.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
CENSO = AQUI / "divida-dos-registos.py"

REGISTO = """---
metadata:
  status: "accepted"
{confirmado}  date: 2026-01-01
  decision-makers: [Dev]
title: {titulo}
decision-outcome:
  chosen-option:
    link: "x"
  confirmation: |
    {conf}
more-information: |
  nada
"""


def escrever(dir_: Path, nome: str, conf: str, confirmado: bool = False) -> None:
    bloco = "  confirmed-by:\n    - engine:tests/x.test.js\n" if confirmado else ""
    (dir_ / nome).write_text(
        REGISTO.format(titulo=nome, conf=conf, confirmado=bloco), encoding="utf-8"
    )


def correr(dir_: Path) -> tuple[int, str]:
    p = subprocess.run(
        [sys.executable, str(CENSO), str(dir_)], capture_output=True, text=True, encoding="utf-8"
    )
    return p.returncode, p.stdout


def main() -> int:
    falhas = []

    with tempfile.TemporaryDirectory() as td:
        vazio = Path(td)

        # 🎯 O VACUO PRIMEIRO: uma arvore sem registos nao pode ser lida como «sem dividas». Este e o caso
        # que apanha o detector morto, e e a razao de ele ser o primeiro e nao o ultimo.
        cod, saida = correr(vazio)
        if "DORMENTE" not in saida:
            falhas.append("[Vacuo] arvore vazia nao anunciou DORMENTE — leria zero como «tudo bem»")
        if cod != 0:
            falhas.append(f"[Vacuo] o censo reprovou (codigo {cod}); ele nunca pode reprovar")

        # Um registo que DEVE e nao tem por onde ser seguido: tem de aparecer.
        escrever(vazio, "ADR-9001-deve-sem-rastro.yaml", "⚠️ NOT YET BUILT. The gates this owes: uma coisa.")
        cod, saida = correr(vazio)
        if "SEM RASTRO — nem issue nomeada, nem `confirmed-by`: 1" not in saida:
            falhas.append("[Zero] divida sem rastro nao foi contada")
        if "ADR-9001" not in saida:
            falhas.append("[Zero] o registo devedor nao foi NOMEADO — um numero sozinho nao se persegue")

        # ⚠️ O PAR: uma divida COM issue nomeada nao e «sem rastro». Sem este caso, o crivo podia contar
        # todos os devedores e a distincao que o ADR-0126 pede desaparecia.
        escrever(vazio, "ADR-9002-deve-com-issue.yaml", "⚠️ NOT YET BUILT. Ver a issue #42, que faz o trabalho.")
        cod, saida = correr(vazio)
        if "`confirmed-by`: 1" not in saida:
            falhas.append("[Boundary] a issue nomeada nao tirou o registo de «sem rastro»")

        # E o outro par: `confirmed-by` tambem e rastro — e o mais forte, porque o validador ABRE os caminhos.
        escrever(vazio, "ADR-9003-deve-confirmado.yaml", "⚠️ NOT YET BUILT. Nada mais.", confirmado=True)
        cod, saida = correr(vazio)
        if "`confirmed-by`: 1" not in saida:
            falhas.append("[Boundary] `confirmed-by` nao contou como rastro")

        # Um registo que NAO deve nada nao pode ser acusado — um crivo que acusa tudo e desligado.
        escrever(vazio, "ADR-9004-nao-deve.yaml", "O gate E a confirmacao: corre na CI todos os dias.")
        cod, saida = correr(vazio)
        if "declaram divida na confirmacao: 3" not in saida:
            falhas.append("[Zero] um registo sem divida foi contado como devedor")

    for f in falhas:
        print(f"FALHA {f}")
    print(f"\ncenso da divida: {'OK' if not falhas else str(len(falhas)) + ' falha(s)'}")
    return 1 if falhas else 0


if __name__ == "__main__":
    raise SystemExit(main())

# ================================ MUTACOES CONFERIDAS ================================
# 1. 🎯 o `DEVE` a deixar de casar «NOT YET BUILT» -> reprovam TRES casos. E a mutacao inteira: o censo
#    passaria a dizer «0 devedores» sobre 126 registos, que e o zero falso que este ficheiro existe para
#    impedir.
# 2. o ramo do DORMENTE removido (arvore vazia a imprimir «0 dividas») -> o [Vacuo] reprova, e o defeito e o
#    pior de todos: um caminho errado passa a ser lido como saude.
# 3. `tem_issue or tem_confirmacao` -> so `tem_issue` -> o [Boundary] do `confirmed-by` reprova. Sem ele, a
#    forma MAIS forte de rastro — a que o validador abre de verdade — contaria como ausencia.
