# -*- coding: utf-8 -*-
"""
Created on Sat May 11 17:34:01 2019

@author: Alf
"""

# Programa para calcular precios de impresiones en 3d

def obtener_datos():
    precio_rollo                = input("[*] Introduce el precio del rollo (euros) > ")
    precio_rollo                = float(precio_rollo)
    
    peso_del_rollo              = input("[*] Introduce el peso del rollo (kg) > ")
    peso_del_rollo              = float(peso_del_rollo)
    
    precio_kwatio_hora          = input("[*] Introduce el precio del kwatio hora (euros) > ")
    precio_kwatio_hora          = float(precio_kwatio_hora)
    
    consumo_impresora           = input("[*] Introduce el consumo por hora que gasta tu impresora (watios) > ")
    consumo_impresora           = float(consumo_impresora) / 1000
    
    peso_de_la_impresion        = input("[*] Introduce el peso de la impresión a realizar (gramos) > ")
    peso_de_la_impresion        = float(peso_de_la_impresion) / 1000
    
    duracion_de_la_impresion    = input("[*] Introduce el tiempo aproximado de la impresión (minutos) > ")
    duracion_de_la_impresion    = float(duracion_de_la_impresion) / 60
    
    return precio_rollo, peso_del_rollo, precio_kwatio_hora, peso_de_la_impresion, duracion_de_la_impresion, consumo_impresora

def calcular_costes(precio_rollo, peso_del_rollo, precio_kwatio_hora, peso_de_la_impresion, duracion_de_la_impresion, consumo_impresora):
    coste_impresion         = (precio_rollo * peso_de_la_impresion) / peso_del_rollo
    coste_de_electricidad   = (consumo_impresora * duracion_de_la_impresion * precio_kwatio_hora)
    
    return coste_impresion, coste_de_electricidad, coste_impresion + coste_de_electricidad 

def imprimir_costes(coste_impresion, coste_electricidad, coste_total, peso_de_la_impresion, duracion_de_la_impresion):
    print("######################################################################")
    
    print("# Material gastado = {} Kilogramos \t\t\t\t#".format(peso_de_la_impresion))
    print("# Minutos de consumo = {} Horas \t\t\t\t#".format(duracion_de_la_impresion))
    
    print("# Impresion = {} € | Consumo Impresora = {} € #".format(coste_impresion, coste_electricidad))
    print("# Total     = {} € \t\t\t\t#".format(coste_total))
    print("######################################################################")

if __name__ == '__main__':
    precio_rollo, peso_del_rollo, precio_kwatio_hora, peso_de_la_impresion, duracion_de_la_impresion, consumo_impresora = obtener_datos()
    
    coste_impresion, coste_de_electricidad, coste_total = calcular_costes(precio_rollo, peso_del_rollo, 
                                                                          precio_kwatio_hora, peso_de_la_impresion, 
                                                                          duracion_de_la_impresion, consumo_impresora)
    imprimir_costes(coste_impresion, coste_de_electricidad, coste_total, peso_de_la_impresion, duracion_de_la_impresion)