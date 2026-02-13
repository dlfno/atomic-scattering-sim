import numpy as np
import matplotlib.pyplot as plt

# --- 1. Constantes ---
k = 8.98755e9         # N·m^2/C^2
e_charge = 1.6022e-19 # C

# Parámetros del problema (Modelo de Rutherford)
Z_gold = 79           
Q = Z_gold * e_charge 
q = 2 * e_charge      

# Radio del NÚCLEO (Ojo con la conversión)
# R = 5e-13 cm = 5e-15 m
R = 5e-15 

# --- 2. Función de Potencial (Misma lógica, distinta escala) ---
def potential_energy(r, R, k, Q, q):
    V = np.zeros_like(r)
    
    # r <= R (Dentro del núcleo)
    mask_inside = r <= R
    term_constant = (k * Q * q) / (2 * R)
    V[mask_inside] = term_constant * (3 - (r[mask_inside]**2 / R**2))
    
    # r > R (Fuera del núcleo - Repulsión Coulombiana)
    mask_outside = r > R
    V[mask_outside] = (k * Q * q) / r[mask_outside]
    
    return V

# --- 3. Generar datos ---
# Usamos un rango muy pequeño: de 0 a 30 femtómetros (3*R aproximadamente)
r_values = np.linspace(0, 4*R, 500) 

# Manejo del cero para evitar división
if r_values[0] == 0:
    r_values = r_values[1:]
    r_values = np.insert(r_values, 0, 0)

# Calcular Energía en Joules y convertir a eV
V_joules = potential_energy(r_values, R, k, Q, q)
V_eV = V_joules / e_charge

# Para facilitar la lectura en la gráfica, usaremos Mega-electronvoltios (MeV)
# aunque el cálculo interno respeta tu petición de eV.
V_MeV = V_eV / 1e6 

# --- 4. Graficar ---
plt.figure(figsize=(10, 6))

# Eje X en femtómetros (1 fm = 10^-15 m)
r_fm = r_values * 1e15 
R_fm = R * 1e15

plt.plot(r_fm, V_eV, label=r'$V(r)$ Rutherford', color='darkred', linewidth=2)

# Línea vertical para el radio nuclear
plt.axvline(x=R_fm, color='black', linestyle='--', label=r'Radio Nuclear $R$')

# Formato
plt.title(r'Energía Potencial $V(r)$ Partícula $\alpha$ - Núcleo de Au (Rutherford)', fontsize=14)
plt.xlabel(r'Distancia radial $r$ (Femtómetros $10^{-15}$m)', fontsize=12)
plt.ylabel(r'Energía Potencial (eV)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)

# Notación científica en el eje Y porque los valores son enormes
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

plt.tight_layout()
plt.show()

# --- 5. Resultados Numéricos ---
V_max_eV = (k * Q * q) / (2 * R) / e_charge * 3
V_surf_eV = (k * Q * q) / R / e_charge

print(f"--- Resultados Modelo de Rutherford ---")
print(f"Radio del núcleo: {R} m")
print(f"Energía en la superficie del núcleo (Barrera de Coulomb): {V_surf_eV:.2e} eV ({V_surf_eV/1e6:.2f} MeV)")
print(f"Energía máxima en el centro (r=0): {V_max_eV:.2e} eV ({V_max_eV/1e6:.2f} MeV)")
