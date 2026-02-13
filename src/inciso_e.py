import numpy as np
import matplotlib.pyplot as plt

# --- 1. Constantes y Parámetros ---
k = 8.98755e9         # N·m^2/C^2
e_charge = 1.6022e-19 # C
Z = 79                # Oro
Q = Z * e_charge
q = 2 * e_charge      # Partícula alfa

# Radios de los modelos (en metros)
R_thomson = 5e-10      # 5 Angstroms
R_rutherford = 5e-15   # 5 Fermis

# Energía de la partícula incidente (para dibujar la línea de referencia)
K_alpha_MeV = 7.7
K_alpha_Joules = K_alpha_MeV * 1e6 * e_charge

# --- 2. Funciones de Potencial ---
def calculate_potential(r, R_model):
    """Calcula V(r) para un modelo dado con radio R_model"""
    V = np.zeros_like(r)
    
    # Dentro de la esfera (r <= R)
    mask_inside = r <= R_model
    term_const = (k * Q * q) / (2 * R_model)
    V[mask_inside] = term_const * (3 - (r[mask_inside]**2 / R_model**2))
    
    # Fuera de la esfera (r > R)
    mask_outside = r > R_model
    V[mask_outside] = (k * Q * q) / r[mask_outside]
    
    return V

# --- 3. Generación de Datos ---
# Usamos escala logarítmica para r para poder ver ambos modelos
# Desde 10^-16 m (dentro del núcleo) hasta 10^-9 m (fuera del átomo)
r = np.logspace(-16, -9, 1000)

V_thomson = calculate_potential(r, R_thomson)
V_rutherford = calculate_potential(r, R_rutherford)

# Convertir a eV para la gráfica
V_thomson_eV = V_thomson / e_charge
V_rutherford_eV = V_rutherford / e_charge

# --- 4. Graficar ---
plt.figure(figsize=(10, 7))

# Graficar Potenciales
plt.plot(r, V_rutherford_eV, label='Modelo Rutherford (Núcleo pequeño)', color='darkred', linewidth=2)
plt.plot(r, V_thomson_eV, label='Modelo Thomson (Átomo grande)', color='blue', linewidth=2, linestyle='--')

# Graficar la Energía de la Partícula Alfa (Línea horizontal)
plt.axhline(y=K_alpha_MeV * 1e6, color='green', linestyle='-', linewidth=2, label=f'Energía Partícula $\\alpha$ ({K_alpha_MeV} MeV)')

# Escalas Logarítmicas (Crucial para ver la diferencia)
plt.xscale('log')
plt.yscale('log')

# Etiquetas y Títulos
plt.xlabel('Distancia radial $r$ (metros)', fontsize=12)
plt.ylabel('Energía Potencial $V(r)$ (eV)', fontsize=12)
plt.title(f'Comparación: Barrera de Potencial Thomson vs Rutherford\nIncidente: $\\alpha$ de {K_alpha_MeV} MeV', fontsize=14)

# Límites para visualizar mejor
plt.ylim(1e2, 1e9) # De 100 eV a 1 Giga-eV
plt.xlim(1e-16, 1e-9)

plt.grid(True, which="both", ls="-", alpha=0.2)
plt.legend(loc='upper right', fontsize=11)

plt.tight_layout()
plt.show()

# --- 5. Imprimir comparación numérica ---
print(f"Barrera Máxima Thomson: {np.max(V_thomson_eV):.2f} eV")
print(f"Barrera Máxima Rutherford: {np.max(V_rutherford_eV)/1e6:.2f} MeV")
print(f"Energía Partícula Alfa: {K_alpha_MeV} MeV")
