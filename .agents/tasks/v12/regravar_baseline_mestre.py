# -*- coding: utf-8 -*-
"""Regrava .agents/tasks/mestre/baseline-hashes.json com os SHA-256 atuais.

A suíte `protegidos` da Planilha do Mestre confere, por SHA-256, se os arquivos DA FICHA
continuam idênticos ao que esta linha de base gravou. É o guarda que prova que o trabalho
da Mestre nunca escreve em arquivo da ficha.

Quando a ficha muda legitimamente — aqui, o redesenho das Raças da v1.2 —, a linha de base
precisa ser regravada. O procedimento é o mesmo das vezes anteriores: backup primeiro, e a
lista do que mudou impressa, para que nenhum arquivo entre no novo baseline sem explicação.

A estrutura do arquivo (chaves de caminho absoluto, uma por arquivo) é preservada: só os
valores de hash dos arquivos existentes são recalculados. Arquivo ausente mantém o hash
antigo, porque a suíte trata ausência com a lista AUSENTES_CONHECIDOS dela.
"""
import hashlib
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
BASELINE = RAIZ / ".agents" / "tasks" / "mestre" / "baseline-hashes.json"

# Os arquivos que o redesenho das Raças toca, com a razão de cada um. Qualquer arquivo
# alterado FORA desta lista é interrompido: seria mudança que eu não sei explicar.
ESPERADOS = {
    "build/gerar_ficha.py": "EJ_VANTAGENS_CURTAS: texto curto por Raça na aba Em Jogo (entrou o Haloviano)",
    "build/testar_ficha.py": "caso de bônus inválido do Vidyadhara (Poder virou válido) e LIVRO_V12 (E20/E25)",
    "build/oraculo_ficha.py": "RACAS: pares de atributo redistribuídos; VANTAGEM_TR_CONDICIONAL esvaziado",
    "build/ficha_dados.py": "TRANSCRITO['vantagens_raciais']: traços novos e âncoras do capítulo 05",
    "build/ficha_funcoes_ok.json": "regravado pela própria suíte da ficha",
    "build/ficha_protegidos.json": "regravado: hashes do livro e dos entregáveis V1.2",
    "build/ficha_mapa.json": "regerado por gerar_ficha.py",
    "ficha-automatizada/Ficha Exemplo - Nadir.xlsx": "regerado por gerar_ficha.py",
}


def sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def rel(caminho):
    try:
        return Path(caminho).resolve().relative_to(RAIZ.resolve()).as_posix()
    except ValueError:
        return str(caminho).replace("\\", "/")


base = json.loads(BASELINE.read_text(encoding="utf-8"))
hashes = base.get("sha256") if isinstance(base, dict) and "sha256" in base else base
if not isinstance(hashes, dict):
    raise SystemExit("ERRO: formato inesperado do baseline")

alterados, ausentes, iguais, inesperados = [], [], [], []
novo = {}
for chave, antigo in hashes.items():
    p = Path(chave)
    if not p.is_absolute():
        p = RAIZ / chave
    r = rel(chave)
    if not p.exists():
        ausentes.append(r)
        novo[chave] = antigo
        continue
    atual = sha256(p)
    novo[chave] = atual
    if atual == antigo:
        iguais.append(r)
    elif r in ESPERADOS:
        alterados.append((r, ESPERADOS[r]))
    else:
        inesperados.append(r)

print(f"iguais        : {len(iguais)}")
print(f"ausentes      : {len(ausentes)}" + (f" -> {ausentes}" if ausentes else ""))
print(f"alterados     : {len(alterados)}")
for r, motivo in alterados:
    print(f"  - {r}\n      {motivo}")
if inesperados:
    print(f"\nINESPERADOS ({len(inesperados)}) — NADA FOI GRAVADO:")
    for r in inesperados:
        print(f"  - {r}")
    raise SystemExit("abortado: arquivo alterado sem explicação na lista ESPERADOS")

if isinstance(base, dict) and "sha256" in base:
    base["sha256"] = novo
    saida = base
else:
    saida = novo
BASELINE.write_text(json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\ngravado: {BASELINE}")
