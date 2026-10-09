# Site: ficha online e livro de consulta

Uma página só, sem instalação, com três abas:

- **Jogar** — a ficha na mesa: PV com dano e cura (já desconta RD e PV temporários), Energia, PH do grupo, ataques e Testes prontos para rolar (clique no valor), Bênçãos com usos, condições, Morrendo, Memoespírito e inventário.
- **Editar ficha** — os doze passos do capítulo 03, mais progressão, equipamento e Memoespírito. Tudo é recalculado na hora, e o que fere uma regra aparece em vermelho na seção.
- **Regras** — o livro inteiro (v1.2) com pesquisa instantânea, sem acento e sem maiúscula.

As fichas ficam salvas **no navegador** de cada jogador. Para backup ou para mandar ao Mestre: **Mais → Exportar** (gera um arquivo `.json`) e **Mais → Importar**.

## Como abrir

- **Pela internet:** o GitHub publica o site sozinho a cada envio para a `main` (`.github/workflows/site.yml`), em `https://mrmarkinboladao.github.io/Explorando-Galaxias-RPG/`.
- **No computador:** abra `site/index.html` no navegador. Funciona sem internet.

## Quando o livro mudar

Os textos e as tabelas saem de `livro-v1.0/`. Depois de mudar um capítulo:

```
python site/gerar_site.py
```

Isso refaz `site/dados/livro.js` e `site/dados/catalogo.js`. No GitHub não precisa: o site publicado roda o script sozinho.

Os **números das fórmulas** (PV, Defesa, dano, tetos...) moram em `site/js/motor.js`, que é a tradução de `build/oraculo_ficha.py` para JavaScript. Se uma regra numérica mudar, mude nos dois.

## Arquivos

| Arquivo | Para quê |
|---|---|
| `index.html`, `estilo.css` | A página e o visual |
| `js/motor.js` | As regras de personagem (cópia fiel do oráculo Python) |
| `js/ficha-base.js` | Modelo da ficha, salvar, exportar e importar |
| `js/ficha-editar.js` | A aba Editar ficha |
| `js/ficha-jogar.js` | A aba Jogar |
| `js/regras.js` | A aba Regras (pesquisa e leitura) |
| `js/app.js` | Rolador de dados, avisos e navegação |
| `js/vendor/marked.umd.js` | Biblioteca que transforma o texto do livro em página (licença MIT) |
| `dados/*.js`, `img/` | Gerados por `gerar_site.py`. Não edite à mão |
