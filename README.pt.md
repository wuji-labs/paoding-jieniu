# 庖丁解牛 PaoDing JieNiu — A Arte de Desossar o Boi

<p align="center">
  <a href="https://www.skills.sh/wuji-labs/paoding-jieniu"><img src="https://www.skills.sh/b/wuji-labs/paoding-jieniu" alt="skills.sh"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://github.com/wuji-labs/huaxia-skills"><img src="https://img.shields.io/badge/%E5%8D%8E%E5%A4%8F%E5%8D%81%E5%A4%A7-HuaXia%20Skills-c1272d" alt="HuaXia Skills"></a>
</p>

**[🇨🇳 简体中文](README.zh-CN.md)** · **[🇺🇸 English](README.md)** · **[🇯🇵 日本語](README.ja.md)** · **[🇰🇷 한국어](README.ko.md)** · **[🇪🇸 Español](README.es.md)** · **[🇧🇷 Português](README.pt.md)** · **[🇫🇷 Français](README.fr.md)**

这是华夏道脉献给世界开源社区的十件礼物之一(叩兩端·无极樞纽)。
我们不立华夏本位,不主张华夏文明优于任何文明;我们只是先从自己最熟悉的道脉开始,
把它打磨成一件可用的工具,放到人类共同的开源工具架上。未来还会有希腊、那烂陀、
犹太、波斯诸文明的礼物依次到来,共同构成十二文明对标的开源能力矩阵。

PT: Este é um dos dez presentes que a corrente de sabedoria chinesa oferece à comunidade mundial de código aberto. Não afirmamos que qualquer civilização seja superior; apenas começamos pela linhagem que melhor conhecemos e a colocamos na prateleira de ferramentas compartilhada da humanidade. Virão a seguir os presentes das linhagens grega, de Nalanda, hebraica e persa.

---

> **依乎天理，批大郤，导大窾** — Siga o veio natural; abra as grandes juntas, conduza a lâmina pelos vazios.
> — Zhuangzi, *O segredo de cultivar a vida* (《庄子·养生主》)

**Sua IA esquarteja sistemas complexos com um cutelo de açougueiro. Ensine a ela a lâmina do cozinheiro.**

Diante de uma base de código emaranhada ou de uma tarefa ambígua do tipo "construa-me X", a maioria das IAs avança e começa a talhar: edita arquivos antes de entender a estrutura, ataca primeiro o núcleo mais acoplado e golpeia na mesma velocidade em todo lugar. Corta através do osso. A lâmina cega. As coisas quebram.

**庖丁解牛** (PaoDing JieNiu) codifica uma resposta de 2300 anos atrás, a do lendário cozinheiro de Zhuangzi, cuja lâmina permaneceu afiada como uma navalha por dezenove anos porque ele nunca cortou contra o veio: encontrava as juntas que já estavam ali e deixava a faca deslizar.

## O problema

```
Você: "Refatore este módulo legado de 40 mil linhas."

IA sem PaoDing:
  - Abre 3 arquivos e começa de imediato a editar a classe mais central
  - Mexe no estado global, quebra 12 coisas e não consegue reverter
  - A mesma velocidade imprudente na rota de criptografia e em um arquivo CSS
  - "Melhor reescrever tudo" (新刀又卷 — lâmina nova, cega de novo)

IA com PaoDing:
  - Primeiro LÊ a estrutura: grafo de dependências, fluxo de dados, fronteiras de domínio (依乎天理)
  - Encontra as juntas: módulos puros, interfaces limpas, camadas de baixo acoplamento (批大郤·导大窾)
  - DESACELERA nos nós difíceis: adiciona testes, pequenos experimentos (怵然为戒)
  - Commits pequenos e reversíveis; a cadeia de ferramentas e a confiança seguem afiadas (刀刃若新)
```

## O que ela ensina à IA

### 🔪 Os quatro fundamentos (四底层原则)

| Princípio | Chinês | O que a IA faz |
|-----------|---------|--------------|
| Siga o veio | 依乎天理 | Lê a estrutura antes de tocar em qualquer coisa |
| Entre pelas juntas | 批大郤·导大窾 | Começa por interfaces, módulos puros, camadas de baixo acoplamento |
| Desacelere nos nós | 怵然为戒·动刀甚微 | Reduz a velocidade nas rotas de núcleo / concorrência / segurança |
| Mantenha a lâmina afiada | 刀刃若新发于硎 | Passos pequenos, reversíveis e amparados por testes — sem acumular dívida |

### 🐂 A anatomia do boi (拆解概念体系)

A skill dá à IA um vocabulário para saber **onde cortar**:

| Termo | Chinês | Significado em engenharia |
|------|---------|---------------------|
| Veio natural | 天理 | As linhas estruturais inerentes ao sistema |
| Grande junta | 大郤 (xì) | Uma fronteira ampla e evidente — o primeiro corte fácil |
| Vazio | 大窾 (kuǎn) | O espaço entre as articulações — onde a lâmina flui livre |
| Osso duro | 大軱 (gū) | Abstração central / estado global — não talhe à força |
| Nó emaranhado | 族 (zú) | Um aglomerado denso de acoplamento — desacelere aqui |
| Espaço para circular | 游刃有余 | A reversibilidade e a folga que a lâmina sempre preserva |
| Encontro pelo espírito | 以神遇 | Quando a estrutura é de fato compreendida, desossar torna-se sem esforço |

### 📏 O método dos quatro passos (拆解四步法)

```
1. 观 OBSERVAR  — mapeie o boi: árvore de diretórios, grafo de dependências, fluxo de dados, domínios
2. 寻 PROCURAR  — encontre a junta: o primeiro corte reversível e testável
3. 慎 CUIDAR    — no nó, desacelere: testes, pequenos experimentos, rota de fuga
4. 养 SUSTENTAR — commits pequenos, sempre no verde, sem dívida: mantenha a lâmina nova
```

### 以道驭术 — Maestria, não força

> 「良庖岁更刀，割也；族庖月更刀，折也。」
> Um bom cozinheiro troca a faca uma vez por ano — ele *corta*.
> Um cozinheiro comum a troca todo mês — ele *talha*.
> — Zhuangzi, *O segredo de cultivar a vida*

A diferença nunca está na faca. Está no **modo** (道) de usá-la. PaoDing JieNiu compartilha a mesma raiz do **NoPUA**: *conduza o trabalho pelo Caminho, não pelo medo; substitua o talho em pânico pela compreensão da estrutura.* Cortar a favor do veio é o que mantém a lâmina — suas ferramentas, sua atenção, seu orçamento de contexto e a confiança — para sempre nova.

## Oriente encontra Ocidente

PaoDing JieNiu não substitui sua formação em engenharia. Ela a **afia**.

| Prática ocidental | + 庖丁解牛 | = Completo |
|------------------|-----------|------------|
| "Faça funcionar, depois refatore" | 依乎天理 primeiro | Compreender antes de cortar — menos reescritas |
| Encontrar as juntas (Michael Feathers) | 批大郤·导大窾 | Uma filosofia de *onde* as juntas vivem |
| "Mova-se rápido e quebre coisas" | 怵然为戒 nos nós | Rápido nos vazios, lento no osso |
| Regra do bom escoteiro | 刀刃若新发于硎 | Mantenha afiada toda a cadeia de ferramentas e a confiança, não só o arquivo |

> **以无厚入有间，恢恢乎其于游刃必有余地矣。**
> Conduza o-que-não-tem-espessura para o-que-tem-espaço, e a lâmina circula com folga de sobra.
> — Zhuangzi, *O segredo de cultivar a vida*

## Da mesma linhagem

- [**NoPUA**](https://github.com/wuji-labs/nopua) — conduz a IA pela sabedoria, não pelo medo.
- [**TianGong** 天工](https://github.com/wuji-labs) — 5000 anos de estética chinesa para o design com IA.

## Instalação

```bash
# Como plugin do Claude Code (um clique)
/plugin marketplace add wuji-labs/paoding-jieniu
/plugin install paoding-jieniu

# Ou clone direto no seu diretório de skills
git clone https://github.com/wuji-labs/paoding-jieniu
cp -r paoding-jieniu ~/.claude/skills/        # global
# ou:  cp -r paoding-jieniu .claude/skills/    # por projeto
```

## Invocação

| Modo | Como |
|------|-----|
| **Automático** | Basta descrever o trabalho — "refatore este módulo legado", "não sei por onde começar nesta base de código", "separe estas fronteiras". O campo `description` dispara o carregamento automático. |
| **Manual** | `/paoding-jieniu <target>` — entrada explícita com um formato de saída fixo. |
| **Exemplos** | Veja `examples/` para entrada→saída em refatoração de código legado, depuração profunda e design de fronteiras. |
| **Benchmark** | `benchmark/` traz uma bateria de 6 cenários e um sujeito de teste real. Os resultados NÃO vêm preenchidos — execute você mesmo. |

## Informações básicas

| Item | Valor |
|----|-----|
| Pertencimento | WUJI Labs |
| Diretório | `labs/skills/paoding-jieniu/` |
| Licença | MIT |
| Upstream | github.com/wuji-labs/paoding-jieniu |
| Fonte clássica | 《庄子·养生主》庖丁解牛 |
| Versão | v1.1.0 · 2026-06-02 |

## Licença

MIT — Use livremente. Corte a favor do veio.

---

*庖丁解牛 PaoDing JieNiu — por [WUJI](https://github.com/wuji-labs)*
*依乎天理，游刃有余。Siga o veio; a lâmina circula livre.*
