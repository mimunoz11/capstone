# Modelación planificación regional

from gurobipy import *
import csv


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

# Orden Cultivos: Palta, Uva de Mesa, Manzanas, Peras, Aceitunas, Uva vino, aceites
c = 7 #cantidad de cultivos
t = 11 #cantidad de periodos
r = 187 #Cantidad de variables de holgura
H_total = 34749.49 #cantidad de hectareas disponibles, revisar porque depende de t
H_inicial = [2000, 600, 775.86, 666.67, 2142.86, 2564.10, 10000.00, 16000.00]
var_precio = [
    [[-3, -3], [0, 5], [-5, 4], [-5, 0], [-4, 3], [-2, 5], [-5, 2]],
    [[-2, -2], [0, 6], [0, 3], [-1, 5], [-2, 3], [0, 5], [0, 7]],
    [[-2, -2], [-1, 4], [-5, 4], [-2, 3], [0, 4], [0, 3], [0, 3]],
    [[-2, -2], [-3, 7], [-1, 6], [-2, 2], [-4, 6], [-4, 6], [-4, 3]],
    [[0, 0], [-2, 7], [-5, 2], [-5, 7], [-3, 7], [-3, 5], [0, 6] ],
    [[-2, -2], [-5, 2], [-3, 4], [0, 4], [-3, 0], [-3, 3], [-3, 0]],
    [[0, 0], [-4, 2], [-3, 3], [-3, 1], [-1, 1], [-3, 3], [0, 3]],
    [[-4, -4], [-4, 5], [-3, 5], [-2, 5], [-3, 2], [-2, 3], [0, 5]],
    [[-3, -3], [-2, 6], [-1, 6], [0, 3], [-1, 5], [-3, 5], [-3, 3]],
    [[-1, -1], [-3, 4], [-2, 2], [-2, 4], [-4, 4], [-5, 4], [-3, 2]]
]

vau = 1

costos = [0.6, 0.65, 0.8, 0.66, 0.7, 0.45, 0.65] #costos de cada cultivo, porcentaje respecto al precio
inversion = [2112, 455, 48, 234.6, 891, 3025, 3150] #inversion para tener 1 ton de cada cultivo
MOD_min =  [0.74, 2.48, 2.88, 3.35,  1.04, 1.16, 0.22] # Mano de obra minima por hectarea
precio_kg = [2.64, 0.65, 0.120, 0.345, 1.485, 2.75, 4.5]
precio_ton=[2640, 650, 230, 345, 1485, 2750, 4500] #precio venta por cada tonelada, ordenadas según excel
kg_hectarea=[10000,25000,58000,45000,7000,7800,1000,0]
ton_hectarea=[10, 25, 58, 45, 7, 7.8, 1, 0]
A_c = [1981, 422, 822, 922, 900, 869, 14431] # Agua que consume cada cultivo
H_min = [10, 4, 1.724137931, 2.222222222, 14.28571429, 12.82051282, 100]

M = 10000000
CBS = 10 #capacidad bocas subterraneas

p = Model("planificacion") # Se define el modelo

# VARIABLES

## Variables para calcular PBI
# PBI
PBI = p.addVars(t, lb = 0.0, name="PBI", vtype=GRB.CONTINUOUS)
# Consumo familias para el año t
Cons = p.addVars(t, lb = 0.0, name="Consumo_familias", vtype=GRB.CONTINUOUS)
# Gasto de Gobierno para el año t
GG = p.addVars(t, lb = 0.0, name="Gasto_Gobierno", vtype=GRB.CONTINUOUS)
# Gasto en Inversión público para el año t
Inv_pub = p.addVars(t, lb = 0.0, name="Inv_pub", vtype=GRB.CONTINUOUS)
# Gasto en Inversión privada para el año t
Inv_priv = p.addVars(t, lb = 0.0, name="Inv_priv", vtype=GRB.CONTINUOUS)
# Gasto realizado por la importación de bienes para el año t
Imp = p.addVars(t, lb = 0.0, name="Importaciones", vtype=GRB.CONTINUOUS)
# Gasto de los productores para el año t
Exp = p.addVars(t, lb = 0.0, name="Exportaciones", vtype=GRB.CONTINUOUS)
# Gastos totales realizado fuera de la comuna para el periodo t
Gastos = p.addVars(t, lb = 0.0, name="Gastos", vtype=GRB.CONTINUOUS)

## Variables para calcular la cantidad de gente y casas
# # Población total para el periodo t
Pob = p.addVars(t, lb= 0.0, name="Poblacion", vtype=GRB.INTEGER)
# Cantidad de mujeres para el periodo t
QM = p.addVars(t, 5, lb= 0.0, name="Cantidad_Mujeres", vtype=GRB.INTEGER)
# Cantidad de hombres para el periodo t
QH = p.addVars(t, 5, lb= 0.0, name="Cantidad_Hombres", vtype=GRB.INTEGER)
# Cantidad de casas para el periodo t
QC = p.addVars(t, lb = 0.0, name="Cantidad_Casas", vtype=GRB.INTEGER)
# Cantidad de profesionales para el periodo t
Prof = p.addVars(t, lb = 0.0, name="Cantidad_Profesionales", vtype=GRB.INTEGER)
# Mano de obra agricultura
MDOA = p.addVars(t, lb=0.0, name="Mano_de_obra_en_agricultura", vtype=GRB.INTEGER)

# ## Variables de plantas de recuperacion/potabilizacion aguas
# Cantidad de conexiones a alcantarillas que hay que hacer el periodo t
QCA = p.addVars(t, lb = 7200.0 , name="Cantidad_Alcantarillas", vtype=GRB.INTEGER)
# Cantidad de bocas subterraneas en el periodo t
CPP = p.addVars(t, obj = 5760.0, name="Capacidad_diaria_Planta_Potable", vtype=GRB.INTEGER)
# Capacidad de planta Aguas Servidas para el periodo t
CPA = p.addVars(t, obj = 2765.0, name="Capacidad_diaria_Planta_Aguas_Servidas", vtype=GRB.INTEGER)

## Variables para calcular el Agua, estan en m3
# Agua potable que consumen las casa en el periodo t
WP = p.addVars(t, lb = 0.0, name="Agua_Potable", vtype=GRB.CONTINUOUS)
# Agua recuperada por la planta de Aguas Servidas en el periodo t
WR = p.addVars(t, lb = 0.0, name="Agua_Recuperada_Alcantarillado", vtype=GRB.CONTINUOUS)
# Agua subterranea disponible en el periodo t
WS = p.addVars(t, lb = 0.0, name="Agua_Subterranea", vtype=GRB.CONTINUOUS) # 3942000
# Agua disponible para la agricultura que se consume el periodo t
WA = p.addVars(t, lb = 0.0, name="Agua_Agricultura", vtype=GRB.CONTINUOUS)
# Agua que se consume en el sector de la industria ES PARAMETRO
WI = 1296000
# Agua de lluvia disponible para el periodo t, SON PARAMETROS, CAMBIAR A LITROS
WL = [750, 780, 800, 850, 830, 750, 650, 750, 725, 600, 550]
# Agua total disponible para el periodo t
W = p.addVars(t, lb = 0.0, name="Agua_Total", vtype=GRB.CONTINUOUS)

## Variables de decision
#Cantidad de plantas potabilizadoras que se construyen en el periodo t AUMENTO CAPACIDAD PLANTA
X = p.addVars(t, lb = 0.0, name="Aumento_capacidad_Plantas_Potabilizadoras", vtype=GRB.BINARY)
#Cantidad de plantas Aguas Servidas que se construyen en el periodo t AUMENTO CAPACIDAD PLANTA
Y = p.addVars(t, lb = 0.0, name="Aumento_capacidad_Plantas_Aguas_Servidas", vtype= GRB.BINARY)

## Variables de los productores
# cantidad de hect a plantar en periodo t del cultuvo c
H = p.addVars(t, c, lb = 0.0, name="Hectareas_nuevas_plantadas", vtype=GRB.CONTINUOUS)
# precio de una tonelada del cultivo c en el periodo t
Precio = p.addVars(t,c, lb=0.0, name="Precio", vtype=GRB.CONTINUOUS)


# Variables Duales

# Variable dual pi
pi = p.addVars(t, lb = 0.0, name="pi", vtype=GRB.CONTINUOUS)
# Variables duales beta, una para cada cultivo
beta = p.addVars(t, c, lb = 0.0, name="beta", vtype=GRB.CONTINUOUS)
# Variable dual alpha
alpha = p.addVars(t, lb = 0.0, name="alpha", vtype=GRB.CONTINUOUS)
# Variables gamma
gamma = p.addVars(t, c, lb =0.0, name="gamma", vtype= GRB.BINARY)
# Variables delta
delta = p.addVars(t, lb=0.0, name="delta", vtype=GRB.CONTINUOUS)
# Variables z
zeta = p.addVars(r, lb=0.0, name="zeta", vtype=GRB.BINARY)

# FUNCION OBJETIVO


p.setObjective(quicksum(PBI[i] for i in range(t)), GRB.MAXIMIZE)


# Restriccion 1 Definición de PBI
restr_1_0 = p.addConstr(PBI[0] == 5500 * Pob[0])
restr_1 = p.addConstrs(PBI[i] ==  Exp[i] - Gastos[i] for i in range(1, t))

# Restricción 2 Gastos totales
restr_2 = p.addConstrs(Gastos[i] == - Cons[i] - GG[i] - Inv_priv[i] + Imp[i]  for i in range(1, t))

# Restriccion 3 Gastos en empleo para el año t
restr_3 = p.addConstrs(Cons[i] == 0.75 * quicksum(QM[i, e] * Prom_i_m + QH[i, e] * Prom_i_h for e in range(2, 4)) + 0.75 * 300 * (QM[i, 4] + QH[i, 4]) for i in range(1, t))

# Restriccion 4 Gasto del Gobierno para el periodo t
restr_4 = p.addConstrs(GG[i] == 200 * Pob[i] + Inv_pub[i]  for i in range(1, t))

# Restriccion 5 Inversión pública realizada el año t
# Se supone que el gasto se reparte en 3 años, pero esta como si se repartiera solo en uno
# WS NO SE SI ES UN GASTO QUE NOS CONVIENE O NO PERO COMO AUMENTA EL PIB SIEMPRE, SE USA AUNQUE NO SEA NECESARIO
# SIEMPRE SE HACE UN AUMENTO A LAS PLANTAS PORQUE INFLUYE EN EL PIB, AUN CUANDO NO ES NECESARIO
restr_5 = p.addConstrs(Inv_pub[i] == 660000 * (X[i] + Y[i]) + 2000 * (QCA[i] - QCA[i-1]) + 2.5 * WS[i] for i in range(1, t))

# Restriccion 6 Inversión privada realizada el año t
restr_6 = p.addConstrs(Inv_priv[i] == 0.05 * PBI[i-1] for i in range(1, t))

# Restriccion 7 Gasto realizado por la importación de bienes en el periodo t
restr_7 = p.addConstrs(Imp[i] == 1680 * Pob[i] for i in range(1, t))

# Restriccion 8 Total de población para el periodo t
restr_8_m = p.addConstrs(QM[0, e] == mujeres[e] for e in range(5))
restr_8_h = p.addConstrs(QH[0, e] == hombres[e] for e in range(5))
restr_8 = p.addConstrs(Pob[i] == quicksum(QM[i, e] + QH[i, e] for e in range(5)) for i in range(t))

# Restriccion 9 Total de profesionales para el periodo t
restr_9 = p.addConstrs(Prof[i] >=  quicksum(0.03 * QM[i, e] + 0.02 * QH[i, e] for e in range(2,4)) for i in range(t))

# Restriccion 10 Inmigración
# SE LIMITA POR ARRIBA PARA QUE MDOA NO SUPERE LA CANTIDAD DE POBLACION DE LA COMUNA
restr_10 = p.addConstrs(MDOA[i] <= 0.55 * quicksum(QH[i, e] for e in range(2,4)) + 0.65 * quicksum(QM[i, e] for e in range(2,4)) for i in range(1, t))



# Restriccion 11 Población para el próximo periodo
# LOS RANGOS 0, 1 Y 4 CAMBIO EL SIGNO PORQUE DE LO CONTRARIO SE HACEN CERO DEBIDO A QUE NO APORTAN INGRESOS A LA COMUNA Y LA OPTIMIZACION LOS ELIMINA
restr_11_1 = p.addConstrs(QH[i, 0] >= QH[i-1, 0] * 0.99495 + quicksum(QM[i - 1 ,e]  * 0.0005 * Nac[e] for e in range(5)) for i in range(1,t)) # + quicksum(QM[i, e] * Nac[e] for e in range(re))
restr_11_2 = p.addConstrs(QH[i, 1] >= QH[i-1, 1] * 0.99495 + QH[i-1, 0] * 0.03 for i in range(1,t))
restr_11_3 = p.addConstrs(QH[i, 2] <= QH[i-1, 2] * 0.99495 + QH[i-1, 1] * 0.02 for i in range(1,t))
restr_11_4 = p.addConstrs(QH[i, 3] <= QH[i-1, 3] * 0.99495 + QH[i-1, 2] * 0.02 for i in range(1,t))
restr_11_5 = p.addConstrs(QH[i, 4] >= QH[i-1, 4] * 0.99495 + QH[i-1, 3] * 0.015 for i in range(1,t))

restr_11_6 = p.addConstrs(QM[i, 0] >= QM[i-1, 0] * 0.99495 + quicksum(QM[i - 1 ,e]  * 0.0005 * Nac[e] for e in range(5))for i in range(1,t))
restr_11_7 = p.addConstrs(QM[i, 1] >= QM[i-1, 1] * 0.99495 + QM[i-1, 0] * 0.03 for i in range(1,t))
restr_11_8 = p.addConstrs(QM[i, 2] <= QM[i-1, 2] * 0.99495 + QM[i-1, 1] * 0.02 for i in range(1,t))
restr_11_9 = p.addConstrs(QM[i, 3] <= QM[i-1, 3] * 0.99495 + QM[i-1, 2] * 0.02 for i in range(1,t))
restr_11_10 = p.addConstrs(QM[i, 4] >= QM[i-1, 4] * 0.99495 + QM[i-1, 3] * 0.015 for i in range(1,t))

# Restriccion 12 La inversión pública no puede superar el 2% del PBI del año anterior
restr_12 = p.addConstrs(Inv_pub[i] <= 0.02 * PBI[i-1] for i in range(1,t))

# Restriccion 13 Cantidad de casas que hay en la comuna
restr_13 = p.addConstrs(QC[i] == 0.25 * Pob[i]  for i in range(t))


## Las cantidades de aguas estan en m3


# Restriccion 14 Respetar cantidad total de agua disponible para todos los periodos
    # m3 de agua en toda la comuna - las 16000 sin plantar
restr_14_0 = p.addConstr(W[0] == WL[0] * 24000 * 10 * 0.5  + WS[0])
    # agua de lluvia considera los terrenos agricoals utilizados mas el terreno urbano
restr_14 = p.addConstrs(W[i] == W[i-1] + WL[i] * 10 * (quicksum(H[i, j] for j in range(c)) + 5250.51) + WS[i] + WR[i] - WA[i] - WI - WP[i] for i in range(1, t))

# Restriccion 15 Respetar producción de agua potable, min 120 lts/dia, max 150 lts/dia, produccion de agua potable < capacidad plantas potables + agua recuperada
restr_15_arriba = p.addConstrs(0.12 * Pob[i] * 365 <= WP[i] for i in range(t))
restr_15_abajo = p.addConstrs(0.15 * Pob[i] * 365 >= WP[i] for i in range(t))
restr_15_prod = p.addConstrs(WP[i] <= 365 * CPP[i] + WR[i] for i in range(t))

# Restriccion 16 Respetar conexión a alcantarillas (Mínimo 60% de las casas y si se construyeron no se pueden sacar)
# CAMBIO EN LA DEFINICION DE QCA Y EN EL LIMITE SUPERIOR
restr_16 = p.addConstr(QCA[0] == 0.6 * QC[0])
restr_16_abajo = p.addConstrs(QCA[i] >=  0.6 * QC[i]  for i in range(1, t))
restr_16_arriba = p.addConstrs(QCA[i] <=  QC[i] for i in range(1, t))

restr_16_1 = p.addConstrs(QCA[i] >= QCA[i - 1] for i in range(1, t))

# Restriccion 17 Agua total recuperada por la planta de Aguas Servidas
# CAMBIA LA RELACION ENTRE QCA/QC POR LO QUE EL 0.6 DEBERIA CAMBIAR
restr_17_abajo = p.addConstrs(WR[i] >= 0.8 * WP[i] * 0.6 for i in range(1, t))
restr_17_prod = p.addConstrs(WR[i] <= 365 * CPA[i]  for i in range(t))

# Restriccion 18 Aumento de capacidad al crear planta de potabilizacion
restr_18_0 = p.addConstr(CPP[0] == 0.12 * Pob[0])
restr_18 = p.addConstrs(CPP[i] == CPP[i-1] + 60 * X[i] * 24 for i in range(1, t))

# Restricción 19 Aumento de capacidad al crear planta de Aguas Servidas
restr_19_0 = p.addConstr(CPA[0] == 2765)
restr_19 = p.addConstrs(CPA[i] == CPA[i-1] + 60 * Y[i] * 24 for i in range(1, t))

# Restriccion 20 Aporte de aguas subterraneas
restr_20 = p.addConstrs(WS[i] <= 450 * 8640 for i in range(1, t))

# Restriccion 21 Asegurar agua potable para prox año
# NO NECESARIA
# restr_21_a = p.addConstrs(W[i] >= WP[i-1] for i in range(1, t))

# Restriccion 22 Limitar consumo agua en agricultura
restr_21_b = p.addConstrs(WA[i] <= 190000000 for i in range(1, t))

# Restriccion 22 Precio del cultivo c el periodo t
restr_22_0 = p.addConstrs(Precio[0,j] == precio_ton[j] for j in range(c))
restrr_22 = p.addConstrs(Precio[i,j] == Precio[i-1, j] * (round(1 + ((var_precio[i-1][j][1] - var_precio[i-1][j][0]) * vau + var_precio[i-1][j][0])/100,2)) for j in range(c) for i in range(1, t))


# # Restricciones duales productor para todos los periodos


# Restriccion Definicion Exportaciones
restr_23 = p.addConstrs(Exp[i] == quicksum(H[i,j] * ton_hectarea[j] * Precio[i, j] * costos[j] + inversion[j] * H[i,j] * ton_hectarea[j] for j in range(c)) for i in range(1, t))

# Restriccion 24 Respetar cantidad de hectareas disponibles
restr_24_0 = p.addConstrs(H[0,j] == H_inicial[j] for j in range(c))
restr_24 = p.addConstrs(quicksum(H[i,j] for j in range(c)) + quicksum(H[i-1, j] for j in range(c)) <= H_total for i in range(1,t))

# Restriccion 25 Agua disponible para la agricultura no debe ser sobrepasada
restr_25 = p.addConstrs(quicksum(A_c[j] * H[i,j] for j in range(c)) <= WA[i] for i in range(1, t))

# Restriccion 26 Mano de obra para la agricultura
restr_26 = p.addConstrs(quicksum(MOD_min[j] * H[i,j] for j in range(c)) <= MDOA[i] for i in range(1, t))

# Restriccion 27 Restringir el crecimiento maximo de los cultivos en un 25%
restr_27 = p.addConstrs(H[i, j] <= 1.25 * H[i-1, j] for j in range(c) for i in range(1, t))

# Restriccion 28 Restringir disminucion maxima de los cultivos en un 30%
restr_28 = p.addConstrs(H[i, j] >= 0.7 * H[i-1, j] for j in range(c) for i in range(1, t))

# Restriccion 29 Restricción del dual
restr_29 = p.addConstrs(quicksum(pi[i] for i in range(1, t)) + quicksum(pi[i-1] for i in range(1, t)) + A_c[j] * quicksum(alpha[i] for i in range(1, t))
+ MOD_min[j] * quicksum(delta[i] for i in range(1, t)) - 1.25 * quicksum(gamma[i, j] for i in range(1, t))
+ quicksum(gamma[i-1, j] for i in range(1, t)) - 0.7 * quicksum(beta[i, j] for i in range(1, t))
+ quicksum(beta[i-1, j] for i in range(1, t)) >= quicksum(ton_hectarea[j] * Precio[i, j] * costos[j] + inversion[j] * ton_hectarea[j] for i in range(1, t)) for j in range(c))

# Restriccion 30 Holguras complementarias
restr_30_1 = p.addConstrs(H_total - quicksum(H[i, j] for j in range(c)) - quicksum(H[i-1, j] for j in range(c)) <= M * (1 - zeta[i]) for i in range(1, t))
restr_30_2 = p.addConstrs(WA[i-t] - quicksum(A_c[j] * H[i-t-1, j] for j in range(c)) <= M * (1 - zeta[i]) for i in range(1 + t, 2 * t))
restr_30_3 = p.addConstrs(MDOA[i-2*t] - quicksum(MOD_min[j] * H[i-2*t-1, j] for j in range(c)) <= M *(1- zeta[i]) for i in range(1 + 2*t, 3 * t))

restr_30_4_1 = p.addConstrs(0 - H[i-3*t, 0] + 1.25 * H[i-3*t-1, 0] <= M * (1-zeta[i]) for i in range(1+3*t,4 *t))
restr_30_4_2 = p.addConstrs(0 - H[i-4*t, 1] + 1.25 * H[i-4*t-1, 1] <= M * (1-zeta[i]) for i in range(1+4*t,5 * t))
restr_30_4_3 = p.addConstrs(0 - H[i-5*t, 2] + 1.25 * H[i-5*t-1, 2] <= M * (1-zeta[i]) for i in range(1+5*t,6 * t))
restr_30_4_4 = p.addConstrs(0 - H[i-6*t, 3] + 1.25 * H[i-6*t-1, 3] <= M * (1-zeta[i]) for i in range(1+6*t,7 * t))
restr_30_4_5 = p.addConstrs(0 - H[i-7*t, 4] + 1.25 * H[i-7*t-1, 4] <= M * (1-zeta[i]) for i in range(1+7*t,8 * t))
restr_30_4_6 = p.addConstrs(0 - H[i-8*t, 5] + 1.25 * H[i-8*t-1, 5] <= M * (1-zeta[i]) for i in range(1+8*t,9 * t))
restr_30_4_7 = p.addConstrs(0 - H[i-9*t, 6] + 1.25 * H[i-9*t-1, 6] <= M * (1-zeta[i]) for i in range(1+9*t,10 * t))

restr_30_5_1 = p.addConstrs(0 - H[i-10*t, 0] + 0.7 * H[i-10*t-1, 0] <= M * (1-zeta[i]) for i in range(1+10*t,11 * t))
restr_30_5_2 = p.addConstrs(0 - H[i-11*t, 1] + 0.7 * H[i-11*t-1, 1] <= M * (1-zeta[i]) for i in range(1+11*t,12 * t))
restr_30_5_3 = p.addConstrs(0 - H[i-12*t, 2] + 0.7 * H[i-12*t-1, 2] <= M * (1-zeta[i]) for i in range(1+12*t,13 * t))
restr_30_5_4 = p.addConstrs(0 - H[i-13*t, 3] + 0.7 * H[i-13*t-1, 3] <= M * (1-zeta[i]) for i in range(1+13*t,14 * t))
restr_30_5_5 = p.addConstrs(0 - H[i-14*t, 4] + 0.7 * H[i-14*t-1, 4] <= M * (1-zeta[i]) for i in range(1+14*t,15 * t))
restr_30_5_6 = p.addConstrs(0 - H[i-15*t, 5] + 0.7 * H[i-15*t-1, 5] <= M * (1-zeta[i]) for i in range(1+15*t,16 * t))
restr_30_5_7 = p.addConstrs(0 - H[i-16*t, 6] + 0.7 * H[i-16*t-1, 6] <= M * (1-zeta[i]) for i in range(1+16*t,17 * t))

p.update()
p.optimize()
p.printAttr('X')



with open('resultados.txt', 'w', encoding='utf-8') as file:
    for v in p.getVars():
        file.write('%s %g \n' % (v.varName, v.x))

lista = []
for i in range(27):
    lista.append([])
with open('resultados.txt', 'r', encoding='utf-8') as file:
    actual = "PBI"
    cont = 0
    for linea in file:
        if cont < 26:
            fila = linea.strip().split(']')
            datos = [fila[0].split('[')[0], fila[0].split('[')[1], fila[1]]
            if datos[0] == actual:
                lista[cont].append(datos)
            else:
                cont += 1
                actual = datos[0]
                lista[cont].append(datos)
conta = 0
for i in lista:
    conta += 1
    with open(f"Var_{conta}.txt", 'w', encoding='utf-8') as file_1:
        for elem in i:
            linea = f"{elem[0]} {elem[1]} {elem[2]}\n"
            file_1.write(linea)