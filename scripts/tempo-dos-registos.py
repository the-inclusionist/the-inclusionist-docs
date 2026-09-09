#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""OS DOIS TEMPOS DE UM REGISTO — a decisao antes, a confirmacao depois (ADR-0128).

=========================== O DEFEITO QUE ISTO APANHA, E ELE ACONTECEU OITO VEZES ===========================
Em 2026-09-09 OITO registos aceites abriam com «⚠️ NOT YET BUILT» sobre trabalho que estava construido —
0108, 0109, 0110, 0111, 0113, 0114, 0115 e 0124. Cada um foi escrito antes do codigo, e cada um continuou a
descrever um futuro que ja tinha acontecido.

E A MAQUINA CONCORDAVA COM ELES: o validador dizia «126 sound, 0 problems», porque um registo sem
`confirmed-by` nao tem o que conferir. Um registo que declara divida e nunca a confirma fica sao PARA SEMPRE.

Este crivo fecha a contradicao que resta depois de a divida ser paga: **um registo que carrega `confirmed-by`
nao pode continuar a dizer que o trabalho esta por fazer.** Ou o texto foi corrigido — e uma `errata` diz o que
mudou, como o ADR-0057 manda — ou o registo contradiz-se, e quem o ler a seguir herda a mentira.

REPROVA, ao contrario do censo da divida, e a diferenca e deliberada: isto e mecanico e conserta-se num
commit (escrever a errata que ja devia la estar). O censo conta uma divida que so o TRABALHO paga, e por isso
so reporta.

MEDIDO ANTES DE SER ESCRITO: 127 registos, 18 com `confirmed-by`, ZERO contraditorios. Nasce verde e pode
ficar vermelho — que e a unica forma de uma regra ser mantida.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "docs/2-Architecture/adr"

POR_CONSTRUIR = re.compile(r"NOT YET BUILT|NOT YET EXECUTED|gates this owes|⬜", re.I)
TEM_CONFIRMADO = re.compile(r"^\s*confirmed-by:", re.M)
TEM_ERRATA = re.compile(r"^\s*errata:", re.M)


def confirmacao(texto: str) -> str:
    i = texto.find("confirmation:")
    if i < 0:
        return ""
    j = texto.find("\nmore-information:", i)
    return texto[i:j if j > 0 else len(texto)]


def main() -> int:
    ficheiros = sorted(p for p in RAIZ.glob("ADR-*.yaml"))
    if not ficheiros:
        # DORMENTE E EM VOZ ALTA: zero ficheiros nao e zero contradicoes. Dizer «tudo bem» aqui seria o falso
        # relatorio que este repositorio ja apanhou tres vezes — e um crivo que aprova o vazio aprova tudo.
        print(f"tempos dos registos: DORMENTE — nenhum ADR-*.yaml em {RAIZ}")
        print("  ⚠️ isto NAO e «zero contradicoes»: e zero medicoes.")
        return 0

    com_confirmado, maus = 0, []
    for p in ficheiros:
        texto = p.read_text(encoding="utf-8")
        if not TEM_CONFIRMADO.search(texto):
            continue
        com_confirmado += 1
        if POR_CONSTRUIR.search(confirmacao(texto)) and not TEM_ERRATA.search(texto):
            maus.append(p.name)

    print(f"tempos dos registos · {len(ficheiros)} registos · {com_confirmado} com `confirmed-by`")
    if not maus:
        print("  ✅ nenhum registo se contradiz: quem tem `confirmed-by` nao diz que o trabalho esta por fazer.")
        return 0

    print(f"\n🔴 {len(maus)} registo(s) CONTRADIZEM-SE — carregam `confirmed-by` e continuam a dizer que o")
    print("   trabalho esta por construir, sem uma `errata` a dizer o que mudou:\n")
    for n in maus:
        print(f"     {n}")
    print("\n  A confirmacao e o SEGUNDO tempo do registo (ADR-0128): quando o gate aterra, o texto deixa de")
    print("  falar no futuro e uma `errata` diz o que mudou (ADR-0057). Um registo que aponta para o gate e")
    print("  ao mesmo tempo diz que ele nao existe ensina o proximo leitor a nao acreditar em nenhum dos dois.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
