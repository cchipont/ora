import argparse, os, json, sys
import constant as constants
from helpers import parseIntSet

from pprint import pprint
from mpmath import mp
from collections import Counter, OrderedDict

import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib
from scipy.stats import randint

# Parseo de parametros
parser = argparse.ArgumentParser(description='Procesmianto de riesgo.')
parser.add_argument('archivo', type=str, help='archivo a procesar')
args = parser.parse_args()

# Auxiliares


# Configuraciones del sistema
mp.dps = constants.PRECISION

def distribution(name=''):
    d = {
        "uniforme_discreta" : 1,
        "otra" : 100
    }
    return d[name]

class parameter():
    _id = 0
    _nombre = 'param'
    _rango = ''
    _intervalo = 1.0
    _distribucion = 1
    _iteraciones = 100
    _cantidad = 1
    _operacion = 'suma'
    
    def __init__(self, id, arr = {}):
        self._id = id
        self._nombre = arr['nombre']
        self._rango = arr['rango']
        self._intervalo = arr['intervalo']
        self._distribucion = distribution(arr['distribucion'])
        self._iteraciones = arr['iteraciones']
        self._cantidad = arr['cantidad']
        self._operacion = arr['operacion']
        pass
        
    def __str__(self):
        return 'id: {} nombre: {}'.format(str(self._id), self._nombre)

    def __unicode__(self):
        return 
    
    def processParameter(self):
        print('Procesando : (' + str(self._id) + ') ' + self._nombre)
        if self._distribucion == 1 :
            print('Distribución : Uniforme Discreta')
            ar = []
            # Obtengo el rango
            rango = parseIntSet(str(self._rango))
            lrango = list(rango)
            # Creo una lista con la cantidad de iteraciones deseada
            for c in range(0,self._cantidad):
                ar.append(np.array(random.choices(lrango, k=self._iteraciones)))
            # Ahora proceso la operacion
            if self._operacion == 'suma' : 
                r = sum(ar)
            else:
                print('La operacion "{}" no se encuentra definida'.format(self._operacion))
                sys.exit()
            return r
        else:
            print(u'Distribución : desconocida')
        return
        pass

class run() :
    _file = ''
    _parameter_list = []
    
    def __init__(self, file = ''):
        
        self._file = file
        basePath = os.path.dirname(os.path.abspath(__file__))
        
        with open(basePath + '/' + file, 'r') as f:
            value = None; name = None; contador = None
            data = json.load(f)
            for d in data:
                
                # iteramos los terminos
                p = parameter(d, data[d])
                self._parameter_list.append([p._nombre, p.processParameter()])
                value = self._parameter_list[0][1]
                name = self._parameter_list[0][0]
                unique_values = list(set(value))
                contador = dict(Counter(value))
                contador = OrderedDict(sorted(contador.items()))
            
            # graficamos
            bins = unique_values
            bins.append(max(value)+1)
            bins_pos = [x+n for n in range(min(bins), max(bins)) for x in [0.5]]

            pprint('Min.:{} / Max.: {}'.format(min(value), max(value)))
            pprint('Set: {}'.format(bins[:-1]))
            pprint('Frecuencia: {}'.format(str(contador)))
            
            plt.hist(value,bins)
            plt.xticks(bins_pos,bins[:-1])
            plt.xlabel('Rango')
            plt.ylabel('Frecuencia')
            plt.title(name)
            plt.grid()
            
            # for label in plt.xaxis.get_xticklabels():
            #     label.set_horizontalalignment('right')
                
            plt.show()            

        

mc = run(file=args.archivo)