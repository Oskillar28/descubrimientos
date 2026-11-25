"""Cálculos del estudio del SS Thistlegorm (Óscar Ramírez Martín, 2026).

Fórmulas estándar de buceo recreativo en agua de mar (1,025 kg/L).
"""

P_SUP = 1.013          # bar, presión atmosférica
K = 0.1006             # bar por metro de agua de mar


def presion(prof_m):
    return P_SUP + K * prof_m


def ppo2(fo2, prof_m):
    return fo2 * presion(prof_m)


def mod(fo2, ppo2_max=1.4):
    return (ppo2_max / fo2 - P_SUP) / K


def end(fo2, prof_m):
    """Profundidad equivalente narcótica (nitrógeno = narcótico)."""
    fn2 = 1 - fo2
    return (presion(prof_m) * fn2 / 0.79 - P_SUP) / K


print("== Presión y ppO2 en el Thistlegorm ==")
print("Prof (m) | P (bar) | ppO2 aire | ppO2 EAN32 | END aire (m) | Consumo x sup.")
for p in (12, 17, 24, 30, 32):
    print(f"{p:8} | {presion(p):7.2f} | {ppo2(0.21, p):9.2f} | {ppo2(0.32, p):10.2f} | "
          f"{end(0.21, p):12.1f} | {presion(p) / P_SUP:5.1f}")

print("\n== Profundidad máxima operativa (MOD, ppO2 1,4 bar) ==")
for nombre, f in (("Aire", 0.21), ("EAN28", 0.28), ("EAN32", 0.32), ("EAN36", 0.36)):
    print(f"{nombre}: {mod(f):.1f} m   (con 1,6 bar: {mod(f, 1.6):.1f} m)")

print("\n== Gas: botella de 12 L a 200 bar, consumo 20 L/min en superficie ==")
litros = 12 * 200
reserva = 12 * 50
for p in (24, 30):
    c = 20 * presion(p) / P_SUP
    print(f"A {p} m: {c:.0f} L/min -> {(litros - reserva) / c:.0f} min hasta reserva (sin contar subida)")

print("\n== Estimación de inmersiones acumuladas (1992-2026) ==")
anios = 2026 - 1992
escenarios = {
    "Bajo (30.000/año)": 30_000,
    "Medio (~200 al día, PADI)": 200 * 365,
    "Alto (175.000/año, cifra máxima citada)": 175_000,
}
for n, v in escenarios.items():
    print(f"{n}: {v:,} al año -> {v * anios / 1e6:.1f} millones en {anios} años")

print("\n== Corrosión del eje de la hélice (Brown y Henderson 2025) ==")
d_ori, d_act = 317, 203
area = 1 - (d_act / d_ori) ** 2
print(f"Diámetro {d_ori} -> {d_act} mm: pérdida de sección {area * 100:.0f} %")

print("\n== Campo de restos ==")
print(f"10,9 ha -> 21,9 ha: x{21.9 / 10.9:.1f}")
