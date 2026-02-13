import numpy as np
import matplotlib.pyplot as plt

# --- 1. Definición de Constantes ---
k = 8.98755e9        # Constante de Coulomb (N·m^2/C^2)
e_charge = 1.6022e-19 # Magnitud de la carga elemental (C)

# Parámetros del problema
Z_gold = 79          # Número atómico del Oro
Q = Z_gold * e_charge # Carga del átomo (Positiva)
q = 2 * e_charge     # Carga de la partícula alfa (Positiva)

# Radio del átomo (convertido de cm a metros)
# R = 5e-8 cm = 5e-10 m
R = 5e-10 

# --- 2. Definición de la Función de Potencial V(r) ---
def potential_energy(r, R, k, Q, q):
    """
    Calcula V(r) en Joules.
    r: distancia desde el centro (array o escalar)
    """
    # Preparamos un array del mismo tamaño que r lleno de ceros
    V = np.zeros_like(r)
    
    # Caso 1: r <= R (Dentro de la esfera - Potencial de oscilador)
    mask_inside = r <= R
    # Fórmula: (kQq / 2R) * (3 - (r/R)^2)
    term_constant = (k * Q * q) / (2 * R)
    V[mask_inside] = term_constant * (3 - (r[mask_inside]**2 / R**2))
    
    # Caso 2: r > R (Fuera de la esfera - Potencial de Coulomb)
    mask_outside = r > R
    # Fórmula: kQq / r
    V[mask_outside] = (k * Q * q) / r[mask_outside]
    
    return V

# --- 3. Generación de datos para la gráfica ---
# Creamos un rango de distancias r.
# Desde 0 hasta 3 veces el radio para ver bien el comportamiento fuera.
r_values = np.linspace(0, 3*R, 500) 

# Evitamos la división por cero en el primer punto si r=0 empieza el array
# (aunque nuestra fórmula interna maneja r=0 bien, es buena práctica)
if r_values[0] == 0:
    r_values = r_values[1:] 
    # Reinsertamos 0 al inicio manualmente para la gráfica completa
    r_values = np.insert(r_values, 0, 0)

# Calculamos V en Joules
V_joules = potential_energy(r_values, R, k, Q, q)

# Convertimos a Electronvoltios (eV)
# 1 eV = 1.6022e-19 J
V_eV = V_joules / e_charge

# --- 4. Graficar ---
plt.figure(figsize=(10, 6))

# Trazar la curva
plt.plot(r_values * 1e10, V_eV, label=r'$V(r)$ Interaction', color='b', linewidth=2)

# Línea vertical para marcar el Radio R (convertido a Angstroms para el eje X)
plt.axvline(x=R * 1e10, color='r', linestyle='--', label=r'Radio $R$ (Superficie)')

# Estilizado
plt.title(r'Energía Potencial $V(r)$ de partícula $\alpha$ en átomo de Au (Modelo Thomson)', fontsize=14)
plt.xlabel(r'Distancia radial $r$ ($\AA$ngstroms)', fontsize=12)
plt.ylabel(r'Energía Potencial (eV)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)

# Anotación de las fórmulas en el gráfico
plt.text(0.5 * R * 1e10, max(V_eV)*0.9, r'$r \leq R: V \propto (3 - r^2/R^2)$', fontsize=10, color='blue')
plt.text(1.5 * R * 1e10, max(V_eV)*0.4, r'$r > R: V \propto 1/r$', fontsize=10, color='blue')

plt.tight_layout()
plt.show()

# Imprimir el valor máximo (en el centro)
V_max = (k * Q * q) / (2 * R) / e_charge * 3
print(f"Energía potencial máxima en el centro (r=0): {V_max:.2f} eV")
print(f"Energía potencial en la superficie (r=R): {V_max/1.5:.2f} eV")
