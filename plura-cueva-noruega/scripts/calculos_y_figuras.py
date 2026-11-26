#!/usr/bin/env python3
"""Cálculos y figuras del estudio de la cueva de Plura (Noruega, 2014).
Calculations and figures for the Plura cave study (Norway, 2014).

Uso / usage:  python3 scripts/calculos_y_figuras.py
Genera / writes: figs/*_es.png, figs/*_en.png y calculos.txt

ATENCIÓN: cálculos divulgativos. No sirven para planificar inmersiones reales.
WARNING: educational only. Do not use to plan real dives.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGS = os.path.join(BASE, "figs")
os.makedirs(FIGS, exist_ok=True)

# ---------------------------------------------------------------- física
RHO_AIR_2C = 1.293 * 273.15 / (273.15 + 2)   # g/L del aire a 1 bar y 2 °C
M_AIR = 28.96                                  # g/mol

def p_abs(d):            # bar, agua dulce ~ 10,3 m por bar; usamos 10 m (redondeo habitual)
    return 1 + d / 10.0

def molar_mass(fo2, fhe):
    fn2 = 1 - fo2 - fhe
    return fo2 * 32 + fhe * 4 + fn2 * 28

def density(d, fo2, fhe):
    return RHO_AIR_2C * p_abs(d) * molar_mass(fo2, fhe) / M_AIR

def end_n2(d, fo2, fhe):  # profundidad narcótica equivalente (solo N2)
    fn2 = 1 - fo2 - fhe
    return max(0.0, (p_abs(d) * fn2 / 0.79 - 1) * 10)

def mod(fo2, ppo2):
    return (ppo2 / fo2 - 1) * 10

lines = []
def out(s=""):
    lines.append(s)

out("CÁLCULOS · PLURA 2014  (divulgativos / educational only)")
out("=" * 60)
out(f"Densidad del aire a 1 bar y 2 °C: {RHO_AIR_2C:.3f} g/L")
for d in (30, 100, 110, 125, 130, 135):
    out(f"\nProfundidad {d} m -> presión absoluta {p_abs(d):.1f} bar")
    out(f"  AIRE   ppO2={0.21*p_abs(d):.2f} bar  ppN2={0.79*p_abs(d):.2f} bar  densidad={density(d,0.21,0):.1f} g/L")
    for name, o2, he in (("TX 10/70", .10, .70), ("TX 8/80", .08, .80)):
        out(f"  {name} ppO2={o2*p_abs(d):.2f} bar  END={end_n2(d,o2,he):.0f} m  densidad={density(d,o2,he):.1f} g/L")
out("\nMOD del aire: 1,4 bar -> %.1f m · 1,6 bar -> %.1f m" % (mod(.21, 1.4), mod(.21, 1.6)))
out("MOD trimix 10/70: 1,4 bar -> %.0f m · 1,6 bar -> %.0f m" % (mod(.10, 1.4), mod(.10, 1.6)))

# Profundidad a la que el aire alcanza los límites de densidad
for lim in (5.2, 6.2):
    d = (lim / RHO_AIR_2C - 1) * 10
    out(f"El aire alcanza {lim} g/L a ~{d:.0f} m")

# Autonomía de una botella de bailout de 11 L a 200 bar (2.200 L) a 130 m
out("\nBotella de rescate (bailout) de 11 L a 200 bar = 2.200 L a 130 m (14 bar):")
for sac, lbl in ((15, "relajado"), (20, "normal"), (30, "esfuerzo"), (45, "estrés"), (60, "pánico")):
    lpm = sac * p_abs(130)
    out(f"  SAC {sac:>2} L/min ({lbl:<8}) -> {lpm:>4.0f} L/min -> {2200/lpm:4.1f} min")

out("\nDuraciones (fuentes: Helsingin Sanomat, X-Ray Mag):")
out("  Plan: ~5 h · Grönqvist: ~8,5 h · Känkänen: ~11,5 h · Rescate: 101 h de buceo en total")

with open(os.path.join(BASE, "calculos.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("\n".join(lines))

# ---------------------------------------------------------------- textos
T = {
 "es": dict(
   prof_t="Perfil esquemático de la travesía Plura → Steinugleflåget (no a escala)",
   dist="Distancia desde la entrada de Plura (m, aprox.)", depth="Profundidad (m)",
   s1="Sifón 1 (≤30 m)\nzona del buceo «normal»", ac="Cámara de aire\n(«Wedding Chamber»)",
   deep="Sección profunda\n~125–135 m", r125="Paso bajo ~125 m\n(Rantanen se atasca)",
   r110="Estrechamiento ~110 m\n(muere Huotarinen)", u="Zona donde\nmuere Jari U.",
   plura="Entrada: estanque\nde Plura (hielo)", stein="Salida: cueva seca\nSteinugleflåget",
   note="Reconstrucción aproximada a partir de HS, X-Ray Mag, Wikipedia y el informe finlandés. Las distancias son orientativas.",
   gas_t="Qué le pasa al gas respirado hasta 140 m",
   ppo2="ppO₂ (bar)", dens="Densidad del gas (g/L)", air="Aire", tx="Trimix 10/70 (ejemplo)",
   lim_o="Límite 1,4 / máx. 1,6", lim_d="Recomendado 5,2 / máx. 6,2", cave="Zona profunda de Plura",
   dur_t="Horas dentro del agua a 2–4 °C",
   dur_lbl=["Plan previsto", "Grönqvist\n(sale por Steinugleflåget)", "Känkänen\n(vuelve a Plura solo)"],
   hours="Horas", unk="≈ (sin cifra exacta)"),
 "en": dict(
   prof_t="Schematic profile of the Plura → Steinugleflåget traverse (not to scale)",
   dist="Distance from the Plura entrance (m, approx.)", depth="Depth (m)",
   s1="Sump 1 (≤30 m)\n'normal' diving zone", ac="Air chamber\n('Wedding Chamber')",
   deep="Deep section\n~125–135 m", r125="Low passage ~125 m\n(Rantanen gets stuck)",
   r110="Restriction ~110 m\n(Huotarinen dies)", u="Area where\nJari U. dies",
   plura="Entry: Plura pond\n(ice)", stein="Exit: dry cave\nSteinugleflåget",
   note="Approximate reconstruction from HS, X-Ray Mag, Wikipedia and the Finnish report. Distances are indicative.",
   gas_t="What happens to the breathing gas down to 140 m",
   ppo2="ppO₂ (bar)", dens="Gas density (g/L)", air="Air", tx="Trimix 10/70 (example)",
   lim_o="Limit 1.4 / max 1.6", lim_d="Recommended 5.2 / max 6.2", cave="Deep zone of Plura",
   dur_t="Hours in 2–4 °C water",
   dur_lbl=["Planned", "Grönqvist\n(exits at Steinugleflåget)", "Känkänen\n(returns to Plura alone)"],
   hours="Hours", unk="≈ (no exact figure)"),
}

plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
INK, ROCK, WATER, RED, AMBER, BLUE = "#1f2a36", "#8c7b6b", "#cfe3f1", "#c0392b", "#d68910", "#1f6fb2"

for lang, t in T.items():
    # 1 ─ perfil
    x = [0, 80, 250, 450, 520, 560, 600, 680, 800, 950, 1050, 1200, 1350, 1430, 1500, 1650, 1800, 1950, 2036]
    y = [0, 12, 25, 30, 8, 0, 0, 20, 60, 100, 125, 132, 130, 118, 110, 95, 70, 30, 0]
    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.fill_between(x, y, 0, color=WATER, alpha=.7)
    ax.plot(x, y, color=BLUE, lw=2.5)
    ax.fill_between(x, [v + 12 for v in y], 150, color=ROCK, alpha=.35)
    ax.set_ylim(150, -15); ax.set_xlim(-30, 2100)
    ax.set_xlabel(t["dist"]); ax.set_ylabel(t["depth"]); ax.set_title(t["prof_t"], fontweight="bold")
    ax.annotate(t["plura"], (0, 0), (60, -10), fontsize=8.5, color=INK)
    ax.annotate(t["stein"], (2036, 0), (1720, -8), fontsize=8.5, color=INK)
    ax.text(160, 45, t["s1"], fontsize=8.5, color=INK)
    ax.text(470, 60, t["ac"], fontsize=8.5, color=INK)
    ax.text(1080, 147, t["deep"], fontsize=8.5, color=INK)
    for xx, yy, lbl, c, dx, dy in ((1050, 125, t["r125"], AMBER, -330, 20),
                                   (1500, 110, t["r110"], RED, 90, -25),
                                   (1430, 118, t["u"], RED, -260, 45)):
        ax.plot(xx, yy, "o", color=c, ms=9, mec="white", zorder=5)
        ax.annotate(lbl, (xx, yy), (xx + dx, yy - dy), fontsize=8.5, color=c,
                    arrowprops=dict(arrowstyle="-", color=c, lw=1))
    fig.text(.01, .01, t["note"], fontsize=7.5, color="#555")
    fig.tight_layout(rect=(0, .03, 1, 1))
    fig.savefig(os.path.join(FIGS, f"perfil_{lang}.png"), dpi=150); plt.close(fig)

    # 2 ─ gases
    d = np.linspace(0, 140, 281)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6))
    a1.plot(d, .21 * p_abs(d), color=RED, lw=2.4, label=t["air"])
    a1.plot(d, .10 * p_abs(d), color=BLUE, lw=2.4, label=t["tx"])
    a1.axhline(1.4, color=AMBER, ls="--"); a1.axhline(1.6, color=RED, ls=":")
    a1.text(2, 1.47, t["lim_o"], fontsize=8, color=AMBER)
    a1.set_xlabel(t["depth"]); a1.set_ylabel(t["ppo2"]); a1.legend(frameon=False)
    a2.plot(d, density(d, .21, 0), color=RED, lw=2.4, label=t["air"])
    a2.plot(d, density(d, .10, .70), color=BLUE, lw=2.4, label=t["tx"])
    a2.axhline(5.2, color=AMBER, ls="--"); a2.axhline(6.2, color=RED, ls=":")
    a2.text(2, 6.5, t["lim_d"], fontsize=8, color=AMBER)
    a2.set_xlabel(t["depth"]); a2.set_ylabel(t["dens"]); a2.legend(frameon=False)
    for a in (a1, a2):
        a.axvspan(110, 135, color="#222", alpha=.12)
        a.text(108, a.get_ylim()[1] * .55, t["cave"], fontsize=7.5, color="#333", rotation=90, ha="right")
    fig.suptitle(t["gas_t"], fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, f"gases_{lang}.png"), dpi=150); plt.close(fig)

    # 3 ─ duraciones
    vals = [5, 8.5, 11.5]
    fig, ax = plt.subplots(figsize=(9, 3.8))
    cols = ["#95a5a6", BLUE, RED]
    bars = ax.barh(t["dur_lbl"], vals, color=cols)
    for b, v in zip(bars, vals):
        ax.text(v + .15, b.get_y() + b.get_height() / 2, (f"{v:g} h".replace(".", ",") if lang == "es" else f"{v:g} h"), va="center", fontsize=9)
    ax.invert_yaxis(); ax.set_xlabel(t["hours"]); ax.set_xlim(0, 13.5)
    ax.set_title(t["dur_t"], fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, f"duraciones_{lang}.png"), dpi=150); plt.close(fig)

print("Figuras en", FIGS)
