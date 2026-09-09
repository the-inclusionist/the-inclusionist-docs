#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""A DIVIDA DOS REGISTOS — um registo que deve trabalho tem de dizer QUEM o faz (ADR-0126).

=========================== POR QUE ISTO EXISTE, MEDIDO E NAO SUPOSTO ===========================
O ADR-0126 fechou com uma clausula: «EVERY RECORD THAT OWES WORK NAMES THE ISSUE THAT DOES IT», e a razao
escrita era manter «a decisao e um registo» de virar o sitio onde trabalho e arquivado sem ninguem o agendar.

MEDIDO em 2026-09-09, e a medicao mudou a forma do gate: dos 126 registos, DOZE declaram divida na
confirmacao e DEZ nao nomeiam issue nenhuma. Mas ao abrir tres deles, a divida era TEXTO VELHO — o ADR-0110,
o 0111 e o 0115 abriam com «NOT YET BUILT» sobre trabalho que ja estava construido.

E O PIOR DE TUDO: o validador dava «126 sound, 0 problems» — porque esses registos nao tinham `confirmed-by`
NENHUM. Um registo que declara divida e nunca a confirma fica SAO PARA SEMPRE. A divida e invisivel a maquina
exactamente enquanto ninguem a paga, que e o oposto do que se quer.

Entao o crivo pergunta duas coisas, nao uma:
  1. o registo declara divida?  (texto: NOT YET BUILT / NOT YET EXECUTED / gates this owes / caixa vazia)
  2. se sim, ha por onde a seguir? — uma ISSUE nomeada, OU um `confirmed-by` (que o validador ABRE).

REPORTA E NAO REPROVA. Corrigir doze registos historicos nao e trabalho de um commit, e um gate que nasce
vermelho e fica vermelho e um gate que alguem desliga — a licao que o `check-annual-report` ja carrega. O
numero e um TECTO QUE SO DESCE, e sai 0 sempre.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "docs/2-Architecture/adr"

DEVE = re.compile(r"NOT YET BUILT|NOT YET EXECUTED|gates this owes|⬜", re.I)
ISSUE = re.compile(r"(?:issue\s+)?#\d+|[a-z][a-z0-9-]*#\d+", re.I)


def confirmacao(texto: str) -> str:
    """O bloco `confirmation`, ate ao `more-information` seguinte. Vazio se nao houver."""
    i = texto.find("confirmation:")
    if i < 0:
        return ""
    j = texto.find("\nmore-information:", i)
    return texto[i:j if j > 0 else len(texto)]


def main() -> int:
    ficheiros = sorted(p for p in RAIZ.glob("ADR-*.yaml"))
    if not ficheiros:
        # DORMENTE E EM VOZ ALTA: zero ficheiros nao e zero dividas, e dizer «tudo bem» aqui seria o falso
        # relatorio que este projecto ja apanhou tres vezes.
        print(f"divida dos registos: DORMENTE — nenhum ADR-*.yaml em {RAIZ}")
        print("  ⚠️ isto NAO e «zero dividas»: e zero medicoes.")
        return 0

    devedores, sem_rastro = [], []
    for p in ficheiros:
        texto = p.read_text(encoding="utf-8")
        conf = confirmacao(texto)
        if not conf or not DEVE.search(conf):
            continue
        devedores.append(p.name)
        tem_issue = bool(ISSUE.search(conf))
        tem_confirmacao = "confirmed-by:" in texto
        if not tem_issue and not tem_confirmacao:
            sem_rastro.append(p.name)

    # ⏳ E AS DECISOES A ESPERA DO DEV, que sao a outra forma de uma coisa ficar quieta. Um registo
    # `proposed` nao deve gates — nao ha decisao para os dever — entao os contadores acima nao o veem. Sem esta
    # linha, uma proposta medida e escrita fica no mesmo silencio de que uma issue fechada a tiraria.
    propostas = [
        p.name for p in ficheiros
        if re.search(r'^\s*status:\s*"?proposed', p.read_text(encoding="utf-8")[:400], re.M)
    ]

    print(f"divida dos registos · {len(ficheiros)} registos")
    if propostas:
        print(f"  ⏳ A ESPERA DE DECISAO ({len(propostas)}): " + ", ".join(n[:12] for n in propostas))
    print(f"  declaram divida na confirmacao: {len(devedores)}")
    print(f"  🔴 SEM RASTRO — nem issue nomeada, nem `confirmed-by`: {len(sem_rastro)}")
    for n in sem_rastro:
        print(f"     {n[:16]}")
    print()
    print("  ⚠️ «sem rastro» nao quer dizer «por fazer»: quer dizer que ninguem consegue SABER, daqui, se")
    print("     esta feito. Tres deles em 2026-09-09 estavam FEITOS e o texto continuava a dizer que nao —")
    print("     e o validador aprovava-os, porque um registo sem `confirmed-by` nao tem o que conferir.")
    print("  (relatorio: nunca reprova — ver o cabecalho e o ADR-0126)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
