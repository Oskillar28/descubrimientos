"""Cálculos del estudio Britannic / Carl Spencer (agua de mar)."""
R = 0.083145  # L·bar/(mol·K)
T = 273.15 + 18   # agua del Egeo a 120 m, aprox. 18 °C (supuesto)
M = {"O2": 32.0, "He": 4.003, "N2": 28.01}
def P(d):  # bar, agua de mar ~1,025 kg/L
    return 1.013 + 0.10055 * d
def dens(fo2, fhe, d):
    fn2 = 1 - fo2 - fhe
    m = fo2*M["O2"] + fhe*M["He"] + fn2*M["N2"]
    return P(d) * m / (R * T)
print("Profundidad -> presión")
for d in [0, 6, 21, 30, 36.6, 60, 90, 120]:
    print(f"{d:6.1f} m  {P(d):5.2f} bar")
print("\nppO2 de una botella 'aire' que era nitrox 50 %")
for d in [6, 12, 21, 30, 36.6]:
    print(f"{d:5.1f} m  EAN50 ppO2={0.5*P(d):.2f} bar   aire ppO2={0.21*P(d):.2f} bar")
for lim in (1.4, 1.6):
    print(f"MOD EAN50 a {lim}: {(lim/0.5-1.013)/0.10055:.1f} m")
print(f"\nAire a 120 m: ppO2={0.21*P(120):.2f} bar, densidad={dens(0.21,0,120):.1f} g/L")
print(f"Diluyente trimix 9/73 a 120 m: ppO2={0.09*P(120):.2f}, densidad={dens(0.09,0.73,120):.1f} g/L")
print(f"Bailout 13/60 a 120 m: ppO2={0.13*P(120):.2f}, densidad={dens(0.13,0.60,120):.1f} g/L")
print(f"Bailout 20/30 MOD a 1,6: {(1.6/0.2-1.013)/0.10055:.0f} m")
print(f"O2 puro bajo campana a 90 m? ppO2 aire en campana a 90 m={0.21*P(90):.2f} bar")
