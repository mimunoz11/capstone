# Planificación Regional bajo incertidumbre de precios
Equipo 10

## Formato del Script

El problema fue escrito en `Python 3.6` y fue resuelto con Gurobi. Si bien, el archivo `plan_regional.py` está bien explicado, a continuación se presenta la estructura de este. 
Para escribirlo, se dividió el script en 5 partes. 

La primera parte se utilizó para poblar el modelo con los parámetros entregados inicialmente por el equipo docente. Aquí se definen las variaciones de los precios, las características de los cultivos, cantidades de aguas, entre otros.

La segunda parte corresponde a la definición de las variables utilizadas en el modelo. 

La tercera parte corresponde a la definición de la función objetivo. Aquí se maximiza el PBI para todos los periodos. Cabe destacar que el PBI está medido utilizando el método de gasto, lo que significa que para cada periodo se maximiza el gasto interno.

La cuarta parte corresponde a la definición de las restricciones. Existen restricciones de primer nivel y de segundo nivel. Debido a la linealización utilizada en el problema, las restricciones de segundo nivel están dualizadas y se utilizan las restricciones duales y de holguras complementarias.

La quinta parte corresponde a correr el modelo utilizando Gurobi y se exportan los resultados en arhivos `.csv`.

## Ejecución del archivo

Ya que la variación de los precios es determinística, al momento de ejecutar el archivo hay que definir el valor que estos van a tomar. Para realizar esto se debe modificar el valor del parametro `vau` (linea 29 del código), entre 0 y 1.
 
Luego, si se utilizan las variaciones de precios entregadas por enunciados, no hay que hacer ningún cambio. Por el contrario, si deciden aplicar el impuesto a las paltas hay que hacer una modificació, utilizar la matriz llamada `var_precio_impuesto_paltas`. Para esto, en la restricción 22 (linea 257 del código), hay que cambiar el uso del parámetro  `var_precio` por `var_precio_impuesto_paltas`.
