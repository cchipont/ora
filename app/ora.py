import argparse, os, json
import constant as constants
from helpers import parseIntSet

from pprint import pprint
from mpmath import mp

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
    
    def __init__(self, id, arr = {}):
        self._id = id
        self._nombre = arr['nombre']
        self._rango = arr['rango']
        self._intervalo = arr['intervalo']
        self._distribucion = distribution(arr['distribucion'])
        self._iteraciones = arr['iteraciones']
        pass
        
    def __str__(self):
        return 'id: {} nombre: {}'.format(str(self._id), self._nombre)

    def __unicode__(self):
        return 
    
    def processParameter(self):
        print('Procesando : (' + str(self._id) + ') ' + self._nombre)
        if self._distribucion == 1 :
            print('Distribución : Uniforme Discreta')
            rango = parseIntSet(str(self._rango))
            lrango = list(rango)
            r = randint.rvs(lrango[0], lrango[-1], size = self._iteraciones)
            return r
        else:
            print('Distribuación : desconocida')
        return
        pass

class run() :
    _file = ''
    _parameter_list = []
    
    def __init__(self, file = ''):
        self._file = file
        basePath = os.path.dirname(os.path.abspath(__file__))
        with open(basePath + '/' + file, 'r') as f:
            data = json.load(f)
            for d in data:
                # creamos los parametros
                self._parameter_list.append(parameter(d, data[d]).processParameter())
            res = sum(self._parameter_list)
            df = pd.DataFrame(res)
            df.hist(bins = 18)
            plt.xlabel('Rango')
            plt.ylabel('Frecuencia')
            plt.grid(b=None)
            
            # for label in plt.xaxis.get_xticklabels():
            #     label.set_horizontalalignment('right')
                
            plt.show()            

        

mc = run(file=args.archivo)