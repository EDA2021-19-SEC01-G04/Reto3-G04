"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
# catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos


def loadData(analyzer, file): 

    file = cf.data_dir + file
    print("file", file)
    input_file = csv.DictReader(open(file, encoding="utf-8"),
                                delimiter=",")
    for event in input_file:
        model.addEvent(analyzer, event)
    
    return analyzer


# Funciones de ordenamiento

def getEventsByCharacteristics(cont, c1, vmin1, vmax1, c2, vmin2, vmax2):
    algo = 0
# Funciones de consulta sobre el catálogo

def eventSize(cont):

    return model.eventSize(cont)  

def artistSize(cont):

    return model.artistSize(cont)

def artistSize2(cont):
    return model.artistSize2(cont)

def trackSize (cont):

    return model.trackSize(cont)

def firstFiveEvents(cont):
    result = model.firstFiveEvents(cont)
    return result

def lastFiveEvents(cont):
    result = model.LastFiveEvents(cont)
    return result

def getEventsByRange(analyzer, c1, vmin1, vmax1, c2, vmin2, vmax2):
    result =  model.getEventsByRange(analyzer, c1, vmin1, vmax1, c2, vmin2, vmax2)
    return result

def getArtistsByRange(analyzer, c1, vmin1, vmax1, c2, vmin2, vmax2):
    result =  model.getArtistsByRange(analyzer, c1, vmin1, vmax1, c2, vmin2, vmax2)
    return result

def getTracksByRange(analyzer, c1, vmin1, vmax1, c2, vmin2, vmax2):
    result =  model.getTracksByRange(analyzer, c1, vmin1, vmax1, c2, vmin2, vmax2)
    return result

def getUnicos(lst):
    return model.getUnicos(lst)

def aleatorias(lista):
    return model.aleatoria(lista) 
 