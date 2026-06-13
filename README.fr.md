# 庖丁解牛 PaoDing JieNiu — L'Art de Découper le Bœuf

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

FR : Voici l'un des dix présents que le courant de sagesse chinois offre à la communauté mondiale de l'open source. Nous ne prétendons qu'aucune civilisation ne soit supérieure ; nous commençons simplement par la lignée que nous connaissons le mieux, pour la déposer sur l'étagère à outils partagée de l'humanité. Suivront les présents des lignées grecque, de Nalanda, hébraïque et perse.

---

> **依乎天理，批大郤，导大窾** — Suis le fil naturel ; fends les grandes jointures, guide la lame dans les creux.
> — Zhuangzi, *Le secret de l'entretien de la vie* (《庄子·养生主》)

**Votre IA découpe des systèmes complexes au couperet de boucher. Apprenez-lui la lame du cuisinier.**

Face à une base de code enchevêtrée ou à une tâche floue du type « construis-moi X », la plupart des IA foncent et se mettent à tailler : elles modifient des fichiers avant d'en comprendre la structure, attaquent d'abord le cœur le plus couplé et frappent partout à la même vitesse. Elles tranchent dans l'os. La lame s'émousse. Tout casse.

**庖丁解牛** (PaoDing JieNiu) encode une réponse vieille de 2300 ans, celle du légendaire cuisinier de Zhuangzi, dont la lame est restée tranchante comme un rasoir pendant dix-neuf ans parce qu'il n'a jamais coupé à contre-fil : il trouvait les jointures déjà présentes et laissait le couteau glisser.

## Le problème

```
Vous : « Refactorise ce module hérité de 40 000 lignes. »

IA sans PaoDing :
  - Ouvre 3 fichiers et se met aussitôt à modifier la classe la plus centrale
  - Touche à l'état global, casse 12 choses et ne peut rien annuler
  - La même vitesse téméraire sur le chemin cryptographique que sur un fichier CSS
  - « Autant tout réécrire » (新刀又卷 — lame neuve, déjà émoussée)

IA avec PaoDing :
  - LIT d'abord la structure : graphe de dépendances, flux de données, frontières de domaine (依乎天理)
  - Trouve les jointures : modules purs, interfaces nettes, couches faiblement couplées (批大郤·导大窾)
  - RALENTIT aux nœuds durs : ajoute des tests, de petites expériences (怵然为戒)
  - Commits petits et réversibles ; la chaîne d'outils et la confiance restent affûtées (刀刃若新)
```

## Ce qu'elle enseigne à l'IA

### 🔪 Les quatre fondements (四底层原则)

| Principe | Chinois | Ce que fait l'IA |
|-----------|---------|--------------|
| Suivre le fil | 依乎天理 | Lire la structure avant de toucher à quoi que ce soit |
| Entrer par les jointures | 批大郤·导大窾 | Commencer par les interfaces, les modules purs, les couches faiblement couplées |
| Ralentir aux nœuds | 怵然为戒·动刀甚微 | Décélérer sur les chemins cœur / concurrence / sécurité |
| Garder la lame affûtée | 刀刃若新发于硎 | Des pas petits, réversibles et adossés à des tests — sans accumuler de dette |

### 🐂 L'anatomie du bœuf (拆解概念体系)

La compétence donne à l'IA un vocabulaire pour savoir **où couper** :

| Terme | Chinois | Sens en ingénierie |
|------|---------|---------------------|
| Fil naturel | 天理 | Les lignes de structure inhérentes au système |
| Grande jointure | 大郤 (xì) | Une frontière large et évidente — la première entaille facile |
| Creux | 大窾 (kuǎn) | L'espace entre les articulations — là où la lame coule librement |
| Os dur | 大軱 (gū) | Abstraction centrale / état global — ne pas tailler en force |
| Nœud emmêlé | 族 (zú) | Un amas dense de couplage — ralentir ici |
| Marge de manœuvre | 游刃有余 | La réversibilité et le jeu que la lame préserve toujours |
| Rencontre par l'esprit | 以神遇 | Quand la structure est vraiment comprise, la découpe se fait sans effort |

### 📏 La méthode en quatre temps (拆解四步法)

```
1. 观 OBSERVER  — cartographier le bœuf : arborescence, graphe de dépendances, flux de données, domaines
2. 寻 CHERCHER  — trouver la jointure : la première entaille réversible et testable
3. 慎 PRENDRE GARDE — au nœud, ralentir : tests, petites expériences, issue de secours
4. 养 ENTRETENIR — petits commits, toujours au vert, sans dette : garder la lame neuve
```

### 以道驭术 — La maîtrise, non la force

> 「良庖岁更刀，割也；族庖月更刀，折也。」
> Un bon cuisinier change de couteau une fois l'an — il *tranche*.
> Un cuisinier ordinaire en change chaque mois — il *taille*.
> — Zhuangzi, *Le secret de l'entretien de la vie*

La différence ne tient jamais au couteau. Elle tient à la **manière** (道) de s'en servir. PaoDing JieNiu partage la même racine que **NoPUA** : *mener le travail par la Voie, et non par la peur ; remplacer la taille paniquée par la compréhension de la structure.* Couper dans le sens du fil, voilà ce qui garde la lame — vos outils, votre attention, votre budget de contexte et la confiance — à jamais neuve.

## L'Orient rencontre l'Occident

PaoDing JieNiu ne remplace pas votre formation d'ingénieur. Elle l'**affûte**.

| Pratique occidentale | + 庖丁解牛 | = Complet |
|------------------|-----------|------------|
| « Fais-le marcher, puis refactorise » | 依乎天理 d'abord | Comprendre avant de couper — moins de réécritures |
| Trouver les jointures (Michael Feathers) | 批大郤·导大窾 | Une philosophie de l'endroit *où* vivent les jointures |
| « Avance vite et casse des choses » | 怵然为戒 aux nœuds | Vite dans les creux, lentement dans l'os |
| Règle du bon scout | 刀刃若新发于硎 | Garder affûtées toute la chaîne d'outils et la confiance, pas seulement le fichier |

> **以无厚入有间，恢恢乎其于游刃必有余地矣。**
> Engage ce-qui-n'a-pas-d'épaisseur dans ce-qui-a-de-l'espace, et la lame se meut avec de la marge à revendre.
> — Zhuangzi, *Le secret de l'entretien de la vie*

## De la même lignée

- [**NoPUA**](https://github.com/wuji-labs/nopua) — mène l'IA par la sagesse plutôt que par la peur.
- [**TianGong** 天工](https://github.com/wuji-labs) — 5000 ans d'esthétique chinoise au service du design par l'IA.

## Installation

```bash
# En tant que plugin Claude Code (en un clic)
/plugin marketplace add wuji-labs/paoding-jieniu
/plugin install paoding-jieniu

# Ou clone simple dans votre répertoire de skills
git clone https://github.com/wuji-labs/paoding-jieniu
cp -r paoding-jieniu ~/.claude/skills/        # global
# ou :  cp -r paoding-jieniu .claude/skills/    # à l'échelle du projet
```

## Invocation

| Mode | Comment |
|------|-----|
| **Automatique** | Décrivez simplement le travail — « refactorise ce module hérité », « je ne sais pas par où commencer dans cette base de code », « sépare ces frontières ». Le champ `description` déclenche le chargement automatique. |
| **Manuel** | `/paoding-jieniu <target>` — entrée explicite avec un format de sortie fixe. |
| **Exemples** | Voir `examples/` pour les entrées→sorties sur la refactorisation de code hérité, le débogage en profondeur et la conception de frontières. |
| **Benchmark** | `benchmark/` fournit une batterie de 6 scénarios et un sujet de test réel. Les résultats ne sont PAS pré-remplis — exécutez-la vous-même. |

## Informations de base

| Élément | Valeur |
|----|-----|
| Rattachement | WUJI Labs |
| Répertoire | `labs/skills/paoding-jieniu/` |
| Licence | MIT |
| Amont | github.com/wuji-labs/paoding-jieniu |
| Source classique | 《庄子·养生主》庖丁解牛 |
| Version | v1.1.0 · 2026-06-02 |

## Licence

MIT — Utilisez-la librement. Coupez dans le sens du fil.

---

*庖丁解牛 PaoDing JieNiu — par [WUJI](https://github.com/wuji-labs)*
*依乎天理，游刃有余。Suis le fil ; la lame se meut librement.*
