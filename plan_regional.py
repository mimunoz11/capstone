# Modelación planificación regional

from gurobipy import *
import numpy as np

# p.setObjective(quicksum(h[i, j] * (precio[j] * (100 + variaciones_precio[i][j][0])/100 * (1 - costos[j])) - inversion[j] for i in [0 + t_i, 1 + t_i, 2 + t_i, 3 + t_i, 4 + t_i] for j in range(c)), GRB.MAXIMIZE)

# constr_a = p.addConstrs((quicksum(h[i, j] for j in range(c)) <= H_total for i in [0 + t_i, 1 + t_i, 2 + t_i, 3 + t_i, 4 + t_i]), name="Capacidad hectareas")

# constr_b = 

# constr_c = p.addConstrs(h[i, j] = H_min[j] for j in range(c) for i in [0 + t_i, 1 + t_i, 2 + t_i, 3 + t_i, 4 + t_i])

# constr_d = p.addConstrs(h[i, j] = np.absolute(H_cien[j]))


# Definición de Parámetros

mujeres = [3900, 2600, 5980, 7020, 6500]
hombres = [3960, 2200, 5940, 5940, 3960]
Nac = [0, 30, 120, 40, 0] #tasa de nacimiento por rango etareo

# Agro-industria, Comercio, Gobierno, Profesionales, Desempleados, Pensionados
# ojo hay que incluir los profesionales externos que son 960 y ganan 3000
ingreso_mensual = [550, 550, 450, 2500, 200, 300]
dist_empleos_m = [0.55, 0.2, 0.07, 0.03, 0.15]
dist_empleos_h = [0.65, 0.1, 0.07, 0.02, 0.16]
Prom_i_h = 526 # ingreso promedio hombres
Prom_i_m = 549 # ingreso promedio mujeres
MOD_min =  [0.74, 2.48, 2.88, 3.35,  1.04, 1.16, 0.22] # Mano de obra minima por hectarea
Dolares_ton=[2640, 650, 230, 345, 1485, 2750, 4500] #precio venta por cada tonelada, ordenadas según excel
kg_hectarea=[10000,25000,58000,45000,7000,7800,1000,0]
# Orden Cultivos: Palta, Uva de Mesa, Manzanas, Peras, Aceitunas, Uva vino, aceites
c = 7 #cantidad de cultivos
t = 10 #cantidad de periodos
r = 9 #cantidad de variables de holgura
H_total = 16000 #cantidad de hectareas disponibles, revisar porque depende de t
variaciones_precio = [
    [
        [-3,-2,-1,0,1,2], [0,1,2,3,4,5], [-5,-4,-3,-2,-1, 0, 1, 2, 3, 4], [-5,-4,-3,-2,-1, 0], [-4,-3,-2,-1,0,1,2,3], [-2,-1,0,1,2,3,4,5], [-5,-4,-3,-2,-1,0,1,2]
    ],
    [
        [-2,-1,0,1,2,3,4,5,6,7], [0,1,2,3,4,5,6], [0,1,2,3], [-1,0,1,2,3,4,5], [-2,-1,0,1,2,3], [0,1,2,3,4,5], [0,1,2,3,4,5,6,7]
    ],
    [
        [-2,-1,0,1,2], [-1,0,1,2,3,4], [-5,-4,-3,-2,-1,0,1,2,3,4], [-2,-1,0,1,2,3], [0,1,2,3,4], [0,1,2,3], [0,1,2,3]
    ],
    [
        [-2,-1,0,1,2,3,4,5,6,7,8], [-3,-2,-1,0,1,2,3,4,5,6,7], [-1,0,1,2,3,4,5,6], [-2,-1,0,1,2], [-4,-3,-2,-1,0,1,2,3,4,5,6], [-4,-3,-2,-1,0,1,2,3,4,5,6], [-4,-3,-2,-1,0,1,2,3]
    ],
    [
        [0,1,2], [-2,-1,0,1,2,3,4,5,6,7], [-5,-4,-3,-2,-1,0,1,2], [-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7], [-3,-2,-1,0,1,2,3,4,5,6,7], [-3,-2,-1,0,1,2,3,4,5], [0,1,2,3,4,5,6]
    ],
    [
        [-2,-1,0,1,2,3,4,5], [-5,-4,-3,-2,-1,0,1,2], [-3,-2,-1,0,1,2,3,4], [0,1,2,3,4], [-3,-2,-1,0], [-3,-2,-1,0,1,2,3], [-3,-2,-1,0]
    ],
    [
        [0,1,2], [-4,-3,-2,-1,0,1,2], [-3,-2,-1,0,1,2,3], [-3,-2,-1,0,1], [-1,0,1], [-3,-2,-1,0,1,2,3], [0,1,2,3]
    ],
    [
        [-4,-3,-2,-1,0,1,2,3,4], [-4,-3,-2,-1,0,1,2,3,4,5], [-3,-2,-1,0,1,2,3,4,5], [-2,-1,0,1,2,3,4,5], [-3,-2,-1,0,1,2], [-2,-1,0,1,2,3], [0,1,2,3,4,5]
    ],
    [
        [-3,-2,-1,0,1,2,3], [-2,-1,0,1,2,3,4,5,6], [-1,0,1,2,3,4,5,6], [0,1,2,3], [-1,0,1,2,3,4,5], [-3,-2,-1,0,1,2,3,4,5], [-3,-2,-1,0,1,2,3]
    ],
    [
        [-1,0,1,2,3,4], [-3,-2,-1,0,1,2,3,4], [-2,-1,0,1,2], [-2,-1,0,1,2,3,4], [-4,-3,-2,-1,0,1,2,3,4], [-5,-4,-3,-2,-1,0,1,2,3,4], [-3,-2,-1,0,1,2]
    ]
]
costos = [0.6, 0.65, 0.8, 0.66, 0.7, 0.45, 0.65] #costos de cada cultivo, porcentaje respecto al precio
inversion = [211.200, 45.500, 4.800, 23.460, 89.100, 302.500, 315.000] #inversion para plantar cada cultivo
precio = [2640.00, 650.00, 120.00, 345.00, 1485.00, 2750.00, 4500.00]
A_c = [1981, 422, 822, 922, 900, 869, 14431] # Agua que consume cada cultivo

H_min = [10, 4, 1.724137931, 2.222222222, 14.28571429, 12.82051282, 100]
M = 10000

t_i = 0 #Se define el problema para el tiempo inicial, variable auxiliar
CBS = 10 #capacidad bocas subterraneas


p = Model("planificacion") # Se define el modelo

# VARIABLES

## Variables para calcular PBI
# PBI
PBI = p.addVars(t, lb = 0.0, name="PBI", vtype=GRB.CONTINUOUS)
# Gastos en empleo para el año t
Emp = p.addVars(t, lb = 0.0, name="Empleo", vtype=GRB.CONTINUOUS)
# Gasto de Gobierno para el año t
GG = p.addVars(t, lb = 0.0, name="Gasto Gobierno", vtype=GRB.CONTINUOUS)
# Inversión público para el año t
Inv_pub = p.addVars(t, lb = 0.0, name="Inv_pub", vtype=GRB.CONTINUOUS)
# Inversión privada para el año t
Inv_priv = p.addVars(t, lb = 0.0, name="Inv_priv", vtype=GRB.CONTINUOUS)
# Gasto realizado por la importación de bienes para el año t
Imp = p.addVars(t, lb = 0.0, name="Importaciones", vtype=GRB.CONTINUOUS)
# Ganancia de los exportaciones para el año t
Exp = p.addVars(t, lb = 0.0, name="Exportaciones", vtype=GRB.CONTINUOUS)

## Variables para calcular la cantidad de gente y casas
# # Población total para el periodo t
Pob = p.addVars(t, lb= 0.0, name="Poblacion", vtype=GRB.INTEGER)
# Cantidad de mujeres para el periodo t
QM = p.addVars(t, c, lb= 0.0, name="Cantidad Mujeres", vtype=GRB.INTEGER)
# Cantidad de hombres para el periodo t
QH = p.addVars(t,c, lb= 0.0, name="Cantidad Hombres", vtype=GRB.INTEGER)
# Cantidad de casas para el periodo t
QC = p.addVars(t, lb = 0.0, name="Cantidad Casas", vtype=GRB.INTEGER)
# Cantidad de profesionales para el periodo t
Prof = p.addVars(t, lb = 0.0, name="Cantidad Profesionales", vtype=GRB.INTEGER)

# ## Variables de plantas de recuperacion/potabilizacion aguas
# Cantidad de conexiones a alcantarillas que hay que hacer el periodo t
QCA = p.addVars(t, lb = 0.0, name="Cantidad Alcantarillas", vtype=GRB.INTEGER)
# Cantidad de bocas subterraneas en el periodo t
QBS = p.addVars(t, lb = 0.0, name="Cantidad Bocas Subterraneas", vtype=GRB.INTEGER)
# Cantidad de plantas potabilizadoras en el periodo t
QPP = p.addVars(t, lb = 0.0, name="Cantidad Plantas Potabilizadoras", vtype=GRB.INTEGER)
# Cantidad de plantas de afluentes en el periodo t
QPA = p.addVars(t, lb = 0.0, name="Cantidad Plantas Afluentes", vtype=GRB.INTEGER)
# Capacidad de planta potable para el periodo t
CPP = p.addVars(t, lb = 0.0, name="Capacidad Planta Potable", vtype=GRB.INTEGER)
# Capacidad de planta afluentes para el periodo t
CPA = p.addVars(t, lb = 0.0, name="Capacidad Planta Afluentes", vtype=GRB.INTEGER)

## Variables para calcular el Agua
# Agua potable que consumen las casa en el periodo t
WP = p.addVars(t, lb = 0.0, name="Agua Potable", vtype=GRB.CONTINUOUS)
# Agua recuperada por la planta de afluentes en el periodo t
WR = p.addVars(t, lb = 0.0, name="Agua Recuperada Alcantarillado", vtype=GRB.CONTINUOUS)
# Agua subterranea disponible en el periodo t, ES PARAMETRO
WS = 3942000
# Agua disponible para la agricultura que se consume el periodo t
WA = p.addVars(t, lb = 0.0, name="Agua Agricultura", vtype=GRB.CONTINUOUS)
# Agua que se consume en el sector de la industria ES PARAMETRO
WI = 3942000
# Agua de lluvia disponible para el periodo t, SON PARAMETROS, CAMBIAR A LITROS
WL = [780, 800, 850, 830, 750, 650, 750, 725, 600, 550]
# Agua total disponible para el periodo t
W = p.addVars(t, lb = 0.0, name="Agua Total", vtype=GRB.CONTINUOUS)

## Variables de decision
#Cantidad de plantas potabilizadoras que se construyen en el periodo t
X = p.addVars(t, lb = 0.0, name="Plantas Potabilizadoras", vtype=GRB.BINARY)
#Cantidad de plantas afluentes que se construyen en el periodo t
Y = p.addVars(t, lb = 0.0, name="Plantas Afluentes", vtype= GRB.BINARY)

## Variables de los productores
# cantidad de hect a plantar en periodo t del cultuvo c
H = p.addVars(t, c, lb = 0.0, name="Hectareas a producir", vtype=GRB.CONTINUOUS)

# Variables Duales

# Variable dual pi
pi = p.addVar(lb = 0.0, name="pi", vtype=GRB.CONTINUOUS)
# Variables duales beta, una para cada cultivo
beta = p.addVars(c, lb = 0.0, name="beta", vtype=GRB.CONTINUOUS)
# Variable dual alpha
alpha = p.addVar(lb = 0.0, name="alpha", vtype=GRB.CONTINUOUS)
# Variables z
zeta = p.addVars(r, lb =0.0, name="zeta", vtype= GRB.BINARY)


# FUNCION OBJETIVO

p.setObjective(quicksum(PBI[i] for i in range(t)), GRB.MAXIMIZE)


# Restriccion 1 Definición de PBI
restr_1_0 = p.addConstr(PBI[0] == 5500 * 48000)
restr_1 = p.addConstrs(PBI[i] <= Emp[i] + GG[i] + Inv_priv[i] + Imp[i]  for i in range(1, t)) # Sacamos la variable Exp

# Restriccion 2 Gastos en empleo para el año t
restr_2 = p.addConstrs(Emp[i] <= 0.75 * quicksum(QM[i, e] * Prom_i_m + QH[i, e] * Prom_i_h for e in range(2, 4)) + 300 * (QM[i, 4] + QH[i, 4]) for i in range(t))

# Restriccion 3 Gasto del Gobierno para el periodo t
restr_3 = p.addConstrs(GG[i] <= 200 * quicksum(QM[i, e] + QH[i, e] for e in range(5)) + Inv_pub[i] for i in range(1,t))

# Restriccion 4 Inversión pública realizada el año t
# Se supone que el gasto se reparte en 3 años, pero esta como si se repartiera solo en uno
restr_4 = p.addConstrs(Inv_pub[i] <= 660000 * (X[i] + Y[i]) + 2000 * (QCA[i] - QCA[i-1]) for i in range(1, t))

# Restriccion 5 Inversión privada realizada el año t
restr_5 = p.addConstrs(Inv_priv[i] <= 0.05 * PBI[i-1] for i in range(1, t))

# Restriccion 6 Gasto realizado por la importación de bienes en el periodo t
restr_6 = p.addConstrs(Imp[i] <= 1680 * quicksum(QM[i, e] + QH[i, e] for e in range(5)) for i in range(1, t))
#
# # # Restriccion 7 Total de población para el periodo t
restr_7_m = p.addConstrs(QM[0, e] == mujeres[e] for e in range(5))
restr_7_h = p.addConstrs(QH[0, e] == hombres[e] for e in range(5))
restr_7 = p.addConstrs(Pob[i] <= quicksum(QM[i, e] + QH[i, e] for e in range(5)) for i in range(t))

# Restriccion 8 Total de profesionales para el periodo t
restr_8 = p.addConstrs(Prof[i] >=  quicksum(0.03 * QM[i, e] + 0.02 * QH[i, e] for e in range(3,5)) for i in range(t))

# Restriccion 9 Inmigración
# ni idea como esribirla

# Restriccion 10 Población para el próximo periodo
restr_10_H = p.addConstrs(quicksum(QH[i, e] for e in range(5)) <= quicksum(QH[i - 1, e] for e in range(5)) - quicksum(QH[i - 1, e] * 0.00505 for e in range(5)) + quicksum(QM[i - 1 ,e]  * 0.0005 * Nac[e] for e in range(5)) for i in range(1, t))
restr_10_M = p.addConstrs(quicksum(QM[i, e] for e in range(5)) <= quicksum(QM[i - 1, e] for e in range(5)) - quicksum(QM[i - 1, e] * 0.00505 for e in range(5)) + quicksum(QM[i - 1 , e] * 0.0005 * Nac[e] for e in range(5)) for i in range(1, t))

# # # Restriccion 11 La inversión pública no puede superar el 2% del PBI del año anterior
restr_11 = p.addConstrs(Inv_pub[i] <= 0.02 * PBI[i-1] for i in range(1,t))

# Restriccion 12 Cantidad de casas que hay en la comuna
restr_12 = p.addConstrs(QC[i] == 0.25 * quicksum(QM[i, e] + QH[i, e] for e in range(5))  for i in range(t))

# Restriccion 13 Respetar cantidad total de agua disponible para todos los periodos
restr_13_0 = p.addConstr(W[0] == WL[0] + WS)
restr_13 = p.addConstrs(W[i] == W[i-1] + WL[i] + WS + WR[i] - WA[i] - WI - WP[i] for i in range(1, t))

# Restriccion 14 Respetar producción de agua potable (120 ltpersona * dia  y debe cubrir como mínimo al 60% de la población)
restr_14_arriba = p.addConstrs(quicksum(QM[i, e] + QH[i, e] for e in range(5)) >= 0.6 * WP[i] for i in range(t))
restr_14_abajo = p.addConstrs(quicksum(QM[i, e] + QH[i, e] for e in range(5)) <= WP[i] for i in range(t))
restr_14_prod = p.addConstrs(WP[i] == QPP[i] for i in range(t)) # FALTA MULTIPLICARLO POR LA CAPACIDAD DE LA PLANTA

# Restriccion 15 Respetar conexión a alcantarillas (Mínimo 60% de las casas)
restr_15_abajo = p.addConstrs(QCA[i] >=  0.25 * 0.6 * quicksum(QM[i, e] + QH[i, e] for e in range(5)) for i in range(t))
restr_15_arriba = p.addConstrs(QCA[i] <= 0.25 * quicksum(QM[i, e] + QH[i, e] for e in range(5)) for i in range(t))

# Restriccion 16 Agua total recuperada por la planta de afluentes
restr_16 = p.addConstrs(WR[i] == 0.8 * WP[i] for i in range(t))

# Restriccion 17 no va porque el agua subterranea es un parametro
#
# Restriccion 18 Cantidad de plantas de potabilizacion
# rest_18 = p.addConstrs(QPP[i] == QPP[i-1] + X[i] for i in range(1, t))

# Restriccion 19 Aumento de capacidad al crear planta de potabilizacion
rest_19 = p.addConstrs(CPP[i] == CPP[i-1] + 60 * X[i] for i in range(1, t))

# Restricción 20 Cantidad de plantas de afluentes
rest_20 = p.addConstrs(QPA[i] == QPA[i-1] + Y[i] for i in range(1, t))

# Restricción 21 Aumento de capacidad al crear planta de afluentes
rest_21 = p.addConstrs(CPA[i] == CPA[i-1] + 60 * Y[i] for i in range(1, t))

# # Restricciones duales productor

# Restriccion a Cantidad a producir en hectáreas para cada cultivo para el año t debe ser menor al total de hectáreas
restr_22 = p.addConstr(quicksum(H[0,j] for j in range(c)) >= H_total)

# Restriccion b Agua disponible para la agricultura no debe ser sobrepasada
restr_23 = p.addConstr(quicksum(A_c[j] * H[1,j] for j in range(c)) <= WA[1])

# Restriccion c Producción mínima de un cultivo
restr_24 = p.addConstrs(H[1,j] >= H_min[j] for j in range(c))

# Restriccion d minimo para cultivar
restr_25 = p.addConstrs(pi + alpha * A_c[j] + beta[j] >= variaciones_precio[1][j][0] * (1 - costos[j]) for j in range(c))

# Restriccion z1
restr_26 = p.addConstr(pi <= M * zeta[0])

# Restriccion z2
restr_27 = p.addConstr(alpha <= M * zeta[1])

# Restriccion zr
restr_28 = p.addConstrs(beta[k-2] <= M * zeta[k] for k in range(2, r))

# Restriccion Holguras
#restr_29 = p.addConstr(H_total - quicksum(H[1, j] for j in range(c)) <= M * (1 - zeta[0]))

#restr_30 = p.addConstr( WA[1] * alpha - quicksum(A_c[j] * H[1, j] for j in range(c)) <= M * (1 - zeta[1]))

restr_31 = p.addConstrs( H[1, k - 2] - H_min[k - 2] <= M * (1 - zeta[k]) for k in range(2, r))

# Restriccion Exportaciones
# restr_32 = p.addConstrs(Exp[u] == (quicksum(precio[j] * (1 - costos[j]) for j in range(c)) * H[1, i] - inversion[i] for i in range(c)) for u in range(1, t)) # revisar range para u

p.update()
p.optimize()

#p.feasibility()
#p.display()
