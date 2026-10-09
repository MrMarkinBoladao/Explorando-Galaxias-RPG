# -*- coding: utf-8 -*-
"""
testar_mestre.py — Bateria de testes da Planilha do Mestre (Explorando Galáxias v1.2).

COMO USAR
    $env:PYTHONUTF8="1"; python "build\\testar_mestre.py" --suite <nome|fase1|fase2|fase3|tudo> [--saida "<arquivo.txt>"]

    --saida duplica tudo o que é impresso num arquivo UTF-8 (plano P11: não usar Tee-Object/'>'
    do PowerShell 5.1, que gravam UTF-16).

    oraculo e extremos rodam em até 8 processos (build\\mestre\\paralelo.py; plano §10 item 8). O número
    de processos vem de $env:MESTRE_PROCESSOS (padrão 8). --trabalhador é uso interno do processo filho.

SUÍTES DA FASE 1 (plano, seção 8; design §12.1)
    spike        padrões novos de fórmula × Python (grava build\\mestre_spike.json)
    protegidos   livro e ficha intocados (só leitura; plano P4/P5)
    dados        parser próprio do teste × aba Dados e listas "Livro" da aba Tabelas
    bestiario    32 fichas criatura por criatura, fases, ações renderizadas na faixa original
    ouro         números impressos no livro calculados NA planilha
    oraculo      build\\oraculo_mestre.py × planilha, 0 divergência (cobertura medida, P10)
    determinismo propriedades (a)–(g) do sorteio (§5) + planilha = oráculo em u/y/x
    extremos     recálculo sem célula de erro (branco, Exemplo, ~200 sementes, estados extremos)
    lint         compatibilidade Google (P3), D3, D11, entradas vazias, auxiliares ocultas
    texto        ortografia PT-BR, glossário 30.1, 30.2, rótulo das Sugestões
    preview      recortes ≤ 1800 px em .agents\\tasks\\mestre\\preview (P6), 0 texto cortado
    visual       régua da ficha: cabe na célula, listas com seta, contraste, 1360 px, 15 linhas

SUÍTE DA FASE 2 (fase2 = as da fase 1 + sabor; oraculo/determinismo/dados/ouro/extremos cobrem NPCs, Aventuras e
Recompensas — G = 200, 300, 400, 410, 420 —, e preview/visual as 12 abas prontas)
    sabor        tabelas de sabor: mínimos, vazio, repetido, 200 caracteres, nomes ≥ 30 por cultura, nenhum nome de
                 personagem do jogo (lista do teste), entradas do livro no início das listas

FASE 3 (fase3 = as mesmas suítes, sobre as 18 abas; casos e conferências da Fase 3 em mestre\\testes_fase3.py)
    dados        + blocos novos (27.3, 27.9, 17.2, 19.4, 19.7, 20.2, 20.3, 23.3–23.6, 26.1, 27.10, 27.16, 27.17, 28.2,
                   29.12), trechos de regra na seção citada, loja de 24.1–24.3 e cada célula do Escudo × aba Dados
    ouro         + 27.9 nível a nível, 23.3, 23.6, 27.2 (30 casos), 26.1, 26.7, preços da loja, H16, H17, H23
    oraculo      + G = 510…650 e 701…710 (900 casos), 60 estados de campanha, H10, H15, H25, (d) toda entrada alcançável
    determinismo + (a)–(g) e u/y/x dos geradores novos; parâmetros de §5 dos geradores novos
    extremos     + Campanha/Sessões/Missões cheias, Minhas Tabelas cheias e vazias, sementes com os geradores novos
    lint / texto + Escudo em A4 paisagem com as quebras e a altura das páginas, nenhum "Em construção" nem
                   "próxima fase"; H24
    origem       (revisão da Fase 3) no início e no fim da fase3: os dois .xlsx são os do gerador, não uma
                 regravação do Google Planilhas pelo Drive

FASE 4 (tudo = origem, entregaveis, as da fase 2, exemplo, guia, origem; mestre\\testes_fase4.py)
    exemplo      o Exemplo é o do gerador; 4 PJs = oraculo_ficha; encontro A; Fila do Ciclo 1 e 2 = oráculo; o
                 critério de aceitação do Memoespírito e das condições; 0 célula de erro; geradores no modelo em branco
    guia         cada `Aba!A1` mostra **valor** do COMO-USAR conferido na planilha calculada
    entregaveis  os 3 entregáveis com os nomes exatos e nada mais em Mestre\\
    (Memoespírito e condições, pedido do usuário: oraculo, ouro, extremos, determinismo, lint, texto, preview e visual
    cobrem G7/G8, C2b, a Fila com 22 combatentes, a C7 com 4 condições por combatente e o painel C9b)

Os testes ficam em build\\mestre\\testes_*.py; este arquivo é a CLI e o registro.
Código de saída 1 em qualquer falha.
"""

import argparse
import io
import sys
import time
from pathlib import Path

BUILD = Path(__file__).resolve().parent
sys.path.insert(0, str(BUILD))

import testar_ficha  # noqa: E402  (Resultado, Modelo, _checar_formula, … — reuso por import)
from mestre import testes_base, testes_dados, testes_regras, testes_estados, testes_hist, testes_fase4  # noqa: E402

Resultado = testar_ficha.Resultado

SUITES = {
    "spike": testes_base.suite_spike,
    "protegidos": testes_base.suite_protegidos,
    "dados": testes_dados.suite_dados,
    "bestiario": testes_dados.suite_bestiario,
    "ouro": testes_regras.suite_ouro,
    "oraculo": testes_regras.suite_oraculo,
    "determinismo": testes_regras.suite_determinismo,
    "extremos": testes_estados.suite_extremos,
    "lint": testes_base.suite_lint,
    "texto": testes_base.suite_texto,
    "preview": testes_estados.suite_preview,
    "visual": testes_estados.suite_visual,
    "sabor": testes_hist.suite_sabor,
    "origem": testes_base.suite_origem,
    "exemplo": testes_fase4.suite_exemplo,
    "guia": testes_fase4.suite_guia,
    "entregaveis": testes_fase4.suite_entregaveis,
}

FASES = {
    "fase1": ["spike", "protegidos", "dados", "bestiario", "ouro", "oraculo", "determinismo",
              "extremos", "lint", "texto", "preview", "visual"],
}
FASES["fase2"] = FASES["fase1"] + ["sabor"]
# Fase 3 (plano 3.5): todas as suítes menos exemplo e entregaveis (Fase 4), sobre as 18 abas; dados, ouro, oraculo,
# determinismo, extremos, lint, texto, preview e visual cobrem também Campanha, Grupo, Sessões, Missões, Mundos,
# Improviso, Escudo do Mestre e Minhas Tabelas (mestre\\testes_fase3.py)
# origem no início e no fim (revisão da Fase 3, F2): as suítes medem os .xlsx do gerador do começo ao fim da bateria
FASES["fase3"] = ["origem"] + FASES["fase2"] + ["origem"]
# Fase 4 (plano 4.3): tudo = todas as suítes de §12.1 + exemplo, guia (o COMO-USAR conferido contra a planilha) e
# entregaveis (os 3 arquivos com os nomes exatos e nada mais em Mestre\\), com a origem no começo e no fim
FASES["tudo"] = ["origem", "entregaveis"] + FASES["fase2"] + ["exemplo", "guia", "origem"]


class _Duplicador(io.TextIOBase):
    def __init__(self, *destinos):
        self.destinos = destinos

    def write(self, s):
        for d in self.destinos:
            d.write(s)
            d.flush()
        return len(s)

    def flush(self):
        for d in self.destinos:
            if not d.closed:      # o arquivo de --saida já fechado quando o objeto é finalizado
                d.flush()


def main():
    ap = argparse.ArgumentParser(description="Bateria de testes da Planilha do Mestre.")
    ap.add_argument("--suite", choices=list(SUITES) + list(FASES))
    ap.add_argument("--saida", default=None, help="arquivo UTF-8 que recebe uma cópia da saída")
    ap.add_argument("--trabalhador", default=None, help=argparse.SUPPRESS)   # processo filho (mestre\\paralelo.py)
    args = ap.parse_args()
    if args.trabalhador:
        from mestre import paralelo
        paralelo.trabalhador(args.trabalhador)
        return
    if not args.suite:
        ap.error("informe --suite")
    arq = None
    if args.saida:
        arq = open(args.saida, "w", encoding="utf-8", newline="\n")
        sys.stdout = _Duplicador(sys.__stdout__, arq)
    nomes = FASES.get(args.suite, [args.suite])
    print(f"Bateria da Planilha do Mestre — suítes: {', '.join(nomes)}")
    print(f"Início: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    resultados = []
    t_total = time.time()
    for n in nomes:
        t0 = time.time()
        try:
            res = SUITES[n](args)
        except Exception as e:  # noqa: BLE001 — erro inesperado vira falha da suíte
            import traceback
            res = Resultado(n)
            res.falha(f"exceção: {e!r}\n{traceback.format_exc()}")
        res.info(f"tempo: {time.time() - t0:.1f} s")
        res.imprimir()
        resultados.append(res)
    print("\n=== RESUMO ===")
    for res in resultados:
        print(f"  {res.nome:<13} {'OK' if not res.falhas else 'FALHOU':<7} {res.checagens:>8} checagens, "
              f"{len(res.falhas)} falha(s)")
    total_f = sum(len(x.falhas) for x in resultados)
    print(f"  total: {sum(x.checagens for x in resultados)} checagens, {total_f} falha(s), "
          f"{time.time() - t_total:.0f} s")
    if arq:
        sys.stdout = sys.__stdout__
        arq.close()
    sys.exit(1 if total_f else 0)


if __name__ == "__main__":
    main()
