#Modelación planificación regional
from gurobipy import *
import numpy as np

# p.setObjective(quicksum(h[i, j] * (precio[j] * (100 + variaciones_precio[i][j][0])/100 * (1 - costos[j])) - inversion[j] for i in [0 + t_i, 1 + t_i, 2 + t_i, 3 + t_i, 4 + t_i] for j in range(c)), GRB.MAXIMIZE)

# constr_a = p.addConstrs((quicksum(h[i, j] for j in range(c)) <= h_total for i in [0 + t_i, 1 + t_i, 2 + t_i, 3 + t_i, 4 + t_i]), name="Capacidad hectareas")

# constr_b = 

# constr_c = p.addConstrs(h[i, j] = H_min[j] for j in range(c) for i in [0 + t_i, 1 + t_i, 2 + t_i, 3 + t_i, 4 + t_i])

# constr_d = p.addConstrs(h[i, j] = np.absolute(H_cien[j]))


# Definición de Parámetros
c = 7 #cantidad de cultivos
t = 10 #cantidad de periodos
h_total = 16000 #cantidad de hectareas disponibles, revisar porque depende de t
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
precio = [2640.00, 650.00, 120.00,345.00,1485.00,2750.00,4500.00]
H_min = [

]

H_cien = [

]
p = Model("planificacion") # Se define el modelo
t_i = 0 #Se define el problema para el tiempo inicial, variable auxiliar

# Parametros que estan en el informe
Prom_i_h = 0 # ingreso promedio hombres
Prom_i_m = 0 # ingreso promedio mujeres 
CBS = 0 #capacidad bocas subterraneas

# VARIABLES

## Variables para calcular PBI
# PBI
PBI = p.addVars(t, name="PBI", vtype=GRB.CONTINUOUS)
# Gastos en empleo para el año t
Emp = p.addVars(t, name="Empleo", vtype=GRB.CONTINUOUS)
# Gasto de Gobierno para el año t
GG = p.addVars(t, name="Gasto Gobierno", vtype=GRB.CONTINUOUS)
# Inversión público para el año t
Inv_pub = p.addVars(t, name="Inv_pub", vtype=GRB.CONTINUOUS)
# Inversión privada para el año t
Inv_priv = p.addVars(t, name="Inv_priv", vtype=GRB.CONTINUOUS)
# Gasto realizado por la importación de bienes para el año t
Imp = p.addVars(t, name="Importaciones", vtype=GRB.CONTINUOUS)
# Ganancia de los exportaciones para el año t
Exp = p.addVars(t, name="Exportaciones", vtype=GRB.CONTINUOUS)

## Variables para calcular la cantidad de gente y casas
# Población total para el periodo t
Pob = p.addVars(t, name="Poblacion", vtype=GRB.INTEGER)
# Cantidad de mujeres para el periodo t
QM = p.addVars(t,e, name="Cantidad Mujeres", vtype=GRB.INTEGER)
# Cantidad de hombres para el periodo t
QH = p.addVars(t,e, name="Cantidad Hombres", vtype=GRB.INTEGER)
# Cantidad de casas para el periodo t
QC = p.addVars(t, name="Cantidad Casas", vtype=GRB.INTEGER)
# Cantidad de profesionales para el periodo t
Prof = p.addVars(t, name="Cantidad Profesionales", vtype=GRB.INTEGER)

## Variables de plantas de recuperacion/potabilizacion aguas
# Cantidad de conexiones a alcantarillas que hay que hacer el periodo t
QCA = p.addVars(t, name="Cantidad Alcantarillas", vtype=GRB.INTEGER)
# Cantidad de bocas subterraneas en el periodo t
QBS = p.addVars(t, name="Cantidad Bocas Subterraneas", vtype=GRB.INTEGER)
# Cantidad de plantas potabilizadoras en el periodo t
QPP = p.addVars(t, name="Cantidad Plantas Potabilizadoras", vtype=GRB.INTEGER)
# Cantidad de plantas de afluentes en el periodo t
QPA = p.addVars(t, name="Cantidad Plantas Afluentes", vtype=GRB.INTEGER)
# Capacidad de planta potable para el periodo t
CPP = p.addVars(t, name="Capacidad Planta Potable", vtype=GRB.INTEGER)
# Capacidad de planta afluentes para el periodo t
CPA = p.addVars(t, name="Capacidad Planta Afluentes", vtype=GRB.INTEGER)

## Variables para calcular el Agua
# Agua potable que consumen las casa en el periodo t
WP = p.addVars(t, name="Agua Potable", vtype=GRB.CONTINUOUS)
# Agua recuperada por la planta de afluentes en el periodo t
WR = p.addVars(t, name="Agua Recuperada Alcantarillado", vtype=GRB.CONTINUOUS)
# Agua disponible para la agricultura que se consume el periodo t
WA = p.addVars(t, name="Agua Agricultura", vtype=GRB.CONTINUOUS)
# Agua que se consume en el sector de la industria el periodo t
WI = p.addVars(t, name="Agua Industria", vtype=GRB.CONTINUOUS)
# Agua de lluvia disponible para el periodo t
WL = p.addVars(t, name="Agua Lluvia", vtype=GRB.CONTINUOUS)
# Agua total disponible para el periodo t
W = p.addVars(t, name="Agua Total", vtype=GRB.CONTINUOUS)

## Variables de decision
#Cantidad de plantas potabilizadoras que se construyen en el periodo t
X = pa.addConstrs(t, name="Plantas Potabilizadoras", vtype= GRB.INTEGER)
#Cantidad de plantas afluentes que se construyen en el periodo t
Y = pa.addConstrs(t, name="Plantas Afluentes", vtype= GRB.INTEGER)

## Variables de los productores
# cantidad de hect a plantar en periodo t del cultuvo c
h = p.addVars(t, c, name="h", vtype=GRB.CONTINUOUS) 





# FUNCION OBJETIVO

p.setObjective(quicksum(PBI[i] for i in range(t)))

#Restriccion 1 Definición de PBI
restr_1 = p.addConstrs(PBI[i] = Emp[i] + GG[t] +  Inv_priv[i] + Imp[i] + Exp[i] for i in range(t))

#Restriccion 2 Gastos en empleo para el año t  
restr_2 = p.addConstrs(Emp[i] = 0.75*(quicksum(QM[i, e] * Prom_i_m) + QH[i, e] * Prom_i_h + 300* (QM[i, 4] + QH[i, 4] for e in range(2, 4)) for i in range(t)))

#Restriccion 3 Gasto del Gobierno para el periodo t
restr_3 = p.addConstrs(GG[i] = quicksum(200 * (QM[i, e] + QH[i, e]) + Inv_pub[t] for e in range(5)) for i in range(t))

#Restriccion 4 Inversión pública realizada el año t
restr_4 = p.addConstrs(Inv_pub[i] = quicksum(220000 * (X[i] + Y[i]) + QCA[i] * 2000 for i in range(t)))

#Restriccion 5 Inversión privada realizada el año t
restr_5 = p.addConstrs(Inv_priv[i] = 0.05 * PBI[i-1 for i in range(t-1)])

#Restriccion 6 Gasto realizado por la importación de bienes en el periodo t 
restr_6 = p.addConstrs(Imp[i] = quicksum((QM[i, e] + QH[i, e]) * 1680 for e in range(5)) for i in range(t))

#Restriccion 7 Total de población para el periodo t
restr_7 = p.addConstrs(Pob[i] = quicksum(QM[i, e] + QH[i, e] for e in range(5)) for i in range(t))

#Restriccion 8 Total de profesionales para el periodo t
restr_8 = p.addConstrs(Prof[i] = quicksum((QM[i, e] * 0.03 + QH[i, e] * 0.02 for e in range(3,5)) for i in range(t))

#Restriccion 9 Inmigración

#Restriccion 10 Población para el próximo periodo
restr_10_H = p.addConstrs(quicksum(QM[i, e] for e range(5)) = quicksum(QM[i - 1, e] for e in range(5)) - quicksum(QM[i - 1, e] * 0.00505 for e in range(5)) + quicksum(QM[i - 1 ,e] * 0.0005 * Nac[i]) for i in range(1, t))
restr_10_M = p.addConstrs(quicksum(QH[i, e] for e range(5)) = quicksum(QH[i - 1, e] for e in range(5)) - quicksum(QM[i - 1, e] * 0.00505 for e in range(5)) + quicksum(QM[i - 1 ,e] * 0.0005 * Nac[i]) for i in range(1, t))

#Restriccion 11 La inversión pública no puede superar el 2% del PBI del año anterior
restr_11 = p.addConstrs(Inv_priv[i] <= 0.02 * PIB[i-1] for i in range(1,t))

#Restriccion 12 Cantidad de casas que hay en la comuna 
restr_12 = p.addConstrs(QC[i] = quicksum(QM[i, e] + QH[i, e] for e in range(5)) * 0.25 for i in range(t))

#Restriccion 13 Respetar cantidad total de agua disponible para todos los periodos
restr_13 = p.addConstrs(W[i] = W[i-1] + Wl[i] + WS[i] + WR[i] - WA[i] - Wi[i] - WP[i] for i in range(t))

#Restriccion 14 Respetar producción de agua potable (120 ltpersona * dia  y debe cubrir como mínimo al 60% de la población)
# restr_14_arriba = p.addConstrs(QPP[i] * CPP[i] * quicksum(QM[i, e] + QH[i, e] for e in range(5)) >= 0.6 * WP[i] for i in range(t))
# restr_14_abajo = p.addConstrs(QPP[i] * CPP[i] * )

#Restriccion 15 Respetar conexión a alcantarillas (Mínimo 60% de las casas)
restr_15_arriba = p.addConstrs(QCA[i] >= 0.6 * quicksum(QM[i, e] + QH[i, e] for e in range(5)) * 0.25 for i in range(t))
restr_15_abajo = p.addConstrs(QCA[i] <= quicksum(QM[i, e] + QH[i, e] for e in range(5)) * 0.25 for i in range(t))

# #Restriccion 16 Agua total recuperada por la planta de afluentes
# restr_16 = p.addConstrs(WR[i] = 0.8 * Y[i] * WP[i] * 4 for i in range(t))
 
#  #Restriccion 17 Agua total obtenida de las bocas de agua subterránea
# restr_17 = p.addConstrs(WS[i] = QPP[i] * CBS) for i in range(t)

# Restriccion 18 Cantidad de plantas de potabilizacion
rest_18 = p.addConstrs(QPP[i] = QPP[i-1 + X[i]] for i in range(t))

# Restriccion 19 Aumento de capacidad al crear planta de potabilizacion
rest_19 = p.addConstrs(CPP[i] = CPP[i-1] + 60*X[i] for i in range(t))

# Restricción 20 Cantidad de plantas de afluentes
rest_20 = p.addConstrs(QPA[i] = QPA[i-1] + Y[i] for i in range(t))

# Restricción 21 Aumento de capacidad al crear planta de afluentes
rest_21 = p.addConstr(CPA[i] = CPA[i-1] + 60 *X[i] for i in range(t))