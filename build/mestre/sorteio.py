# -*- coding: utf-8 -*-
"""
sorteio.py — o ÚNICO construtor de fórmulas de sorteio da Planilha do Mestre (design §5, D5).

Modelo (sem RAND): para o gerador G, o campo C, a semente S (aba Início) e a Rolagem nº R:
    h  = MOD(S + 7919*G + 104729*R + 1299709*C, 2147483646) + 1
    L3(z) = MOD(MOD(MOD(z*16807,M)*16807,M)*16807,M)               (3 rodadas de Lehmer, M = 2^31-1)
    Q(z)  = MOD(MOD(INT(z/65536)*z,M)*65536 + MOD(z,65536)*z, M)   (z² mod M partido em 16 bits)
    X(z)  = MOD(z + INT(z/65536)*MOD(z,65536), 2147483646) + 1     (mistura não polinomial)
    u = L3(h)   y = L3(Q(u))   x = L3(X(y))      — três células auxiliares ocultas por campo.
Aritmética: todo intermediário < 2,8·10^14 < 2^53 (inteiro exato em ponto flutuante).
A mesma conta, em Python puro, está em build\\oraculo_mestre.py (independente deste arquivo).
"""

M = 2147483647
A = 16807


def _l3(z):
    return f"MOD(MOD(MOD(({z})*16807,2147483647)*16807,2147483647)*16807,2147483647)"


def _q(z):
    return f"MOD(MOD(INT({z}/65536)*{z},2147483647)*65536+MOD({z},65536)*{z},2147483647)"


def _x(z):
    return f"MOD({z}+INT({z}/65536)*MOD({z},65536),2147483646)+1"


def formula_u(semente, rolagem, g, c):
    """Fórmula da célula u (h escrito dentro dela). `semente`/`rolagem` são referências de células
    que já contêm a semente e a rolagem EFETIVAS; g e c são inteiros fixos."""
    k = 7919 * int(g) + 1299709 * int(c)
    h = f"MOD({semente}+104729*{rolagem}+{k},2147483646)+1"
    return "=" + _l3(h)


def formula_y(u):
    return "=" + _l3(_q(u))


def formula_x(y):
    return "=" + _l3(_x(y))


def semente_efetiva(cel):
    """Semente vazia, não numérica, não inteira ou fora de 1..2147483646 = 12345 (design §5)."""
    return (f"=IF(ISNUMBER({cel}),IF(AND({cel}>=1,{cel}<=2147483646,INT({cel})={cel}),{cel},12345),12345)")


def aviso_semente(cel):
    # LEN(x)=0, não ISBLANK: a entrada chega pela camada de leitura protegida, que devolve "" (ISBLANK("") = FALSE)
    return (f'=IF(LEN({cel})=0,"",IF(ISNUMBER({cel}),IF(AND({cel}>=1,{cel}<=2147483646,INT({cel})={cel}),"",'
            f'"Semente fora de 1 a 2.147.483.646: usando 12345"),"Semente fora de 1 a 2.147.483.646: usando 12345"))')


def rolagem_efetiva(cel):
    return f"=IF(ISNUMBER({cel}),IF(AND({cel}>=1,{cel}<=1000000,INT({cel})={cel}),{cel},1),1)"


def aviso_rolagem(cel):
    return (f'=IF(LEN({cel})=0,"",IF(ISNUMBER({cel}),IF(AND({cel}>=1,{cel}<=1000000,INT({cel})={cel}),"",'
            f'"Rolagem nº fora de 1 a 1.000.000: usando 1"),"Rolagem nº fora de 1 a 1.000.000: usando 1"))')


def escolha(x, n):
    """Índice de 1 a n numa lista de tamanho n (0 quando a lista está vazia)."""
    return f"IF({n}<=0,0,INT({x}*{n}/2147483647)+1)"


def inteiro(x, a, b):
    """Inteiro uniforme em [a, b]."""
    return f"({a}+INT({x}*(({b})-({a})+1)/2147483647))"


def dado(x, faces):
    return f"(INT({x}*{faces}/2147483647)+1)"


PRIMOS_PASSO = (7, 11, 13, 17, 19, 23)


def passo(n):
    """O primeiro de 7, 11, 13, 17, 19, 23 que não divide n (design §6.17; com n ≤ 100 sempre existe, 7·11·13 > 100)."""
    s = str(PRIMOS_PASSO[-1])
    for p in reversed(PRIMOS_PASSO[:-1]):
        s = f"IF(MOD({n},{p})<>0,{p},{s})"
    return s


def kesimo_sem_repetir(i0, k, n, passo_ref):
    """O k-ésimo resultado (k = 0, 1, …) da sequência sem repetição: MOD(i₀ − 1 + k·passo, n) + 1 (1 a n; 0 com a
    lista vazia). Os k < n primeiros são distintos porque o passo é primo e não divide n."""
    return f"IF({n}<=0,0,MOD({i0}-1+{k}*{passo_ref},{n})+1)"


def segundo_sem_repetir(x2, n, i1):
    """Segundo índice na mesma lista sem repetir i1 (n = 1 repete)."""
    return f"IF({n}<=1,{i1},MOD({i1}-1+1+INT({x2}*({n}-1)/2147483647),{n})+1)"


class Campo:
    """Um campo sorteado: as três células auxiliares (u, y, x) numa linha de colunas ocultas."""

    def __init__(self, ws, linha, col_u, semente, rolagem, g, c, nome, registrar):
        from openpyxl.utils import get_column_letter as L
        cu, cy, cx = L(col_u), L(col_u + 1), L(col_u + 2)
        self.u, self.y, self.x = f"{cu}{linha}", f"{cy}{linha}", f"{cx}{linha}"
        registrar(ws, self.u, formula_u(semente, rolagem, g, c), f"{nome}.u")
        registrar(ws, self.y, formula_y(f"${cu}${linha}"), f"{nome}.y")
        registrar(ws, self.x, formula_x(f"${cy}${linha}"), f"{nome}.x")
        self.g, self.c = g, c
        self.xref = f"${cx}${linha}"
