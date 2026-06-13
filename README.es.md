# 庖丁解牛 PaoDing JieNiu — El Arte de Despiezar el Buey

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

ES: Este es uno de los diez regalos que el linaje de sabiduría chino ofrece a la comunidad mundial del código abierto. No afirmamos que ninguna civilización sea superior; simplemente empezamos por el linaje que mejor conocemos y lo colocamos en el estante de herramientas compartido de la humanidad. Seguirán los regalos de los linajes griego, de Nalanda, hebreo y persa.

---

> **依乎天理，批大郤，导大窾** — Sigue la veta natural; hiende las grandes junturas, guía la hoja por los huecos.
> — Zhuangzi, *El secreto de cuidar la vida* (《庄子·养生主》)

**Tu IA despieza sistemas complejos con un machete de carnicero. Enséñale la hoja del cocinero.**

Ante una base de código enmarañada o una tarea ambigua del tipo «constrúyeme X», la mayoría de las IA arremeten y empiezan a tajar: editan archivos antes de comprender la estructura, atacan primero el núcleo más acoplado y golpean a la misma velocidad en todas partes. Cortan a través del hueso. La hoja se mella. Las cosas se rompen.

**庖丁解牛** (PaoDing JieNiu) codifica una respuesta de hace 2300 años, la del legendario cocinero de Zhuangzi, cuya hoja se mantuvo afilada como una navaja durante diecinueve años porque nunca cortó contra la veta: hallaba las junturas que ya estaban allí y dejaba que el cuchillo se deslizara.

## El problema

```
Tú: «Refactoriza este módulo heredado de 40 000 líneas».

IA sin PaoDing:
  - Abre 3 archivos y empieza a editar de inmediato la clase más central
  - Toca el estado global, rompe 12 cosas y no puede deshacerlas
  - La misma velocidad temeraria en la ruta de criptografía que en un archivo CSS
  - «Mejor lo reescribo todo» (新刀又卷 — hoja nueva, mellada de nuevo)

IA con PaoDing:
  - Primero LEE la estructura: grafo de dependencias, flujo de datos, fronteras de dominio (依乎天理)
  - Halla las junturas: módulos puros, interfaces limpias, capas de bajo acoplamiento (批大郤·导大窾)
  - AMINORA en los nudos duros: añade pruebas, pequeños experimentos (怵然为戒)
  - Commits pequeños y reversibles; la cadena de herramientas y la confianza siguen afiladas (刀刃若新)
```

## Lo que le enseña a la IA

### 🔪 Los cuatro fundamentos (四底层原则)

| Principio | Chino | Lo que hace la IA |
|-----------|---------|--------------|
| Sigue la veta | 依乎天理 | Lee la estructura antes de tocar nada |
| Entra por las junturas | 批大郤·导大窾 | Empieza por interfaces, módulos puros, capas de bajo acoplamiento |
| Aminora en los nudos | 怵然为戒·动刀甚微 | Desacelera en las rutas de núcleo / concurrencia / seguridad |
| Mantén la hoja afilada | 刀刃若新发于硎 | Pasos pequeños, reversibles y respaldados por pruebas: sin acumular deuda |

### 🐂 La anatomía del buey (拆解概念体系)

La skill le da a la IA un vocabulario para saber **dónde cortar**:

| Término | Chino | Significado en ingeniería |
|------|---------|---------------------|
| Veta natural | 天理 | Las líneas estructurales inherentes del sistema |
| Gran juntura | 大郤 (xì) | Una frontera amplia y evidente: el primer corte fácil |
| Hueco | 大窾 (kuǎn) | El espacio entre articulaciones: donde la hoja fluye libre |
| Hueso duro | 大軱 (gū) | Abstracción central / estado global: no lo tajes a la fuerza |
| Nudo enredado | 族 (zú) | Un cúmulo denso de acoplamiento: aminora aquí |
| Espacio para moverse | 游刃有余 | La reversibilidad y la holgura que la hoja siempre preserva |
| Encuentro por el espíritu | 以神遇 | Cuando se comprende de veras la estructura, despiezar se vuelve sin esfuerzo |

### 📏 El método de los cuatro trazos (拆解四步法)

```
1. 观 OBSERVAR  — cartografía el buey: árbol de directorios, grafo de dependencias, flujo de datos, dominios
2. 寻 BUSCAR    — halla la juntura: el primer corte reversible y comprobable
3. 慎 CUIDAR    — en el nudo, aminora: pruebas, pequeños experimentos, vía de escape
4. 养 SOSTENER  — commits pequeños, siempre en verde, sin deuda: mantén la hoja nueva
```

### 以道驭术 — Maestría, no fuerza

> 「良庖岁更刀，割也；族庖月更刀，折也。」
> Un buen cocinero cambia su cuchillo una vez al año: él *corta*.
> Un cocinero corriente lo cambia cada mes: él *taja*.
> — Zhuangzi, *El secreto de cuidar la vida*

La diferencia nunca está en el cuchillo. Está en el **modo** (道) de usarlo. PaoDing JieNiu comparte la misma raíz que **NoPUA**: *guía el trabajo con el Camino, no con el miedo; reemplaza el tajeo presa del pánico por la comprensión de la estructura.* Cortar a favor de la veta es lo que mantiene la hoja —tus herramientas, tu atención, tu presupuesto de contexto y la confianza— por siempre nueva.

## Oriente y Occidente se encuentran

PaoDing JieNiu no reemplaza tu formación en ingeniería. La **afila**.

| Práctica occidental | + 庖丁解牛 | = Completo |
|------------------|-----------|------------|
| «Hazlo funcionar, luego refactoriza» | 依乎天理 primero | Comprender antes de cortar: menos reescrituras |
| Hallar las junturas (Michael Feathers) | 批大郤·导大窾 | Una filosofía de *dónde* viven las junturas |
| «Muévete rápido y rompe cosas» | 怵然为戒 en los nudos | Rápido en los huecos, lento en el hueso |
| Regla del buen explorador | 刀刃若新发于硎 | Mantén afilados toda la cadena de herramientas y la confianza, no solo el archivo |

> **以无厚入有间，恢恢乎其于游刃必有余地矣。**
> Introduce lo-que-no-tiene-grosor en lo-que-tiene-espacio, y la hoja vaga con holgura de sobra.
> — Zhuangzi, *El secreto de cuidar la vida*

## Del mismo linaje

- [**NoPUA**](https://github.com/wuji-labs/nopua) — guía a la IA con sabiduría en lugar de miedo.
- [**TianGong** 天工](https://github.com/wuji-labs) — 5000 años de estética china para el diseño con IA.

## Instalación

```bash
# Como plugin de Claude Code (un solo clic)
/plugin marketplace add wuji-labs/paoding-jieniu
/plugin install paoding-jieniu

# O clónalo sin más en tu directorio de skills
git clone https://github.com/wuji-labs/paoding-jieniu
cp -r paoding-jieniu ~/.claude/skills/        # global
# o:  cp -r paoding-jieniu .claude/skills/    # por proyecto
```

## Invocación

| Modo | Cómo |
|------|-----|
| **Automático** | Solo describe el trabajo: «refactoriza este módulo heredado», «no sé por dónde empezar en esta base de código», «separa estas fronteras». El campo `description` dispara la carga automática. |
| **Manual** | `/paoding-jieniu <target>` — entrada explícita con un formato de salida fijo. |
| **Ejemplos** | Consulta `examples/` para ver entrada→salida en refactorización de código heredado, depuración profunda y diseño de fronteras. |
| **Benchmark** | `benchmark/` incluye una batería de 6 escenarios y un sujeto de prueba real. Los resultados NO vienen rellenados: ejecútalo tú mismo. |

## Información básica

| Campo | Valor |
|----|-----|
| Pertenencia | WUJI Labs |
| Directorio | `labs/skills/paoding-jieniu/` |
| Licencia | MIT |
| Origen (upstream) | github.com/wuji-labs/paoding-jieniu |
| Fuente clásica | 《庄子·养生主》庖丁解牛 |
| Versión | v1.1.0 · 2026-06-02 |

## Licencia

MIT — Úsalo con libertad. Corta a favor de la veta.

---

*庖丁解牛 PaoDing JieNiu — por [WUJI](https://github.com/wuji-labs)*
*依乎天理，游刃有余。Sigue la veta; la hoja vaga libre.*
