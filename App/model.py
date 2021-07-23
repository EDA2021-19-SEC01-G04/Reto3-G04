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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import shellsort as sa
import random
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'events': None,
                'artist_id': None,
                'track_id': None
                }

    analyzer['events'] = lt.newList('SINGLE_LINKED', compareEvents)

    analyzer['artist_id'] = om.newMap(omaptype='BST',
                                      comparefunction=compareArtist)

    analyzer['track_id'] = om.newMap(omaptype='BST',
                                      comparefunction=compareTrack)
    
    # Características de contenido

    analyzer['instrumentalness'] = om.newMap(omaptype='BST',
                                      comparefunction=compareFeatures)
    analyzer['acousticness'] = om.newMap(omaptype='BST',
                                      comparefunction=compareFeatures)
    analyzer['liveness'] = om.newMap(omaptype='BST',
                                      comparefunction=compareFeatures)
    analyzer['speechiness'] = om.newMap(omaptype='BST',
                                      comparefunction=compareFeatures)
    analyzer['energy'] = om.newMap(omaptype='BST',
                                      comparefunction=compareFeatures)
    analyzer['danceability'] = om.newMap(omaptype='BST',
                                      comparefunction=compareFeatures)
    analyzer['valence'] = om.newMap(omaptype='BST',
                                      comparefunction=compareFeatures)
    analyzer['tempo'] = om.newMap(omaptype='BST',
                                      comparefunction=compareFeatures)
    return analyzer

# Funciones para agregar informacion al catalogo

def addEvent(analyzer, event):

    lt.addLast(analyzer['events'], event)

    addArtistId(analyzer['artist_id'], event)
    addTrackId(analyzer['track_id'], event)
    actualizarArbol(analyzer['instrumentalness'], event, 'instrumentalness', False)
    actualizarArbol(analyzer['acousticness'], event, 'acousticness', False)
    actualizarArbol(analyzer['liveness'], event, 'liveness', False)
    actualizarArbol(analyzer['speechiness'], event, 'speechiness', False)
    actualizarArbol(analyzer['energy'], event, 'energy', False)
    actualizarArbol(analyzer['danceability'], event, 'danceability', False)
    actualizarArbol(analyzer['valence'], event, 'valence', False)
    actualizarArbol(analyzer['tempo'], event, 'tempo', False)

    return analyzer

def addArtistId(map, event):
    try:
        artists = map
        artist_id = event['artist_id']

        existArtist = om.contains(artists, artist_id)

        if existArtist:
            entry = om.get(artists, artist_id)
            artistEntry = me.getValue(entry)
        else:
            artistEntry = newArtistEntry(artist_id)
            om.put(artists, artist_id, artistEntry)
        lt.addLast(artistEntry['events'], event)
    except Exception:
        return None

def addTrackId(map, event):
    try:
        track = map
        track_id = event['track_id']

        existTrack = om.contains(track, track_id)

        if existTrack:
            entry = om.get(track, track_id)
            trackEntry = me.getValue(entry)
        else:
            trackEntry = newArtistEntry(track_id)
            om.put(track, track_id, trackEntry)
        lt.addLast(trackEntry['events'], event)
    except Exception:
        return None

def actualizarArbol(map, event, featureName, arbol_hijo): # agrega un evento(event) al arbol(map) del feature(feature) que tenga el nombre que pase por param

    featureValue = event[featureName] # ejemplo con liveness: event['liveness'] que sería un número: 0.01
    
    entry = om.get(map, featureValue) 
    if entry is None: # si no existe el nodo se crea un nuevo nodo con esa llave, en este caso 0.1 
        datentry = creadorDeNodos(arbol_hijo) # datentry es el nodo creado

        om.put(map, featureValue, datentry) # y guarda dentro del arbol(map) el nuevo nodo(datentry)
    else: # si ya existe el nodo solo lo va a traer
        datentry = me.getValue(entry) # dataentry es el nodo conseguido

    # ya cuando tengo un datentry (nodo):
    # después de eso, ya tengo entonces un dataentry (un nodo), ya sea creado o conseguido 
    agregarEventoAListaYArboles(datentry, event, arbol_hijo) # y ahora lo único que hago es guardar mi evento nuevo en ese nodo
    return map

def agregarEventoAListaYArboles(datentry, event, deboParar): # agrega un evento(event) a la lista de events dataentry['lstevents'] 
    # y tambien ahora, para mas placer, a cada arbol del dataentry en cuestion

    lstEventos = datentry['lstevents'] # saca la lista del nodo (la lista en la llave 'lstevents')
    lstArtistas = datentry['lstartists'] 
    lstTracks = datentry['lsttracks'] 
    lt.addLast(lstEventos, event) # luego agrega el nuevo evento a la lista
    lt.addLast(lstArtistas, event['artist_id'])
    lt.addLast(lstTracks, event["track_id"])

    # si todavia no deboparar (porque en teoria estoy en el arbol papa), saco tambien los árboles hijos y hago lo mismo de arriba (actualizarArbol)
    if deboParar == False: # si me llega false también significa que quien me llamó fue el arbol padre, asi que solo queda hacer lo mismo con los arboles en sus nodos hijos
        
        livenessTree = datentry['liveness'] 
        actualizarArbol(livenessTree, event, 'liveness', True)

        instrumentalnessTree = datentry['instrumentalness'] 
        actualizarArbol(instrumentalnessTree, event, 'instrumentalness', True) 

        acousticnessTree = datentry['acousticness'] 
        actualizarArbol(acousticnessTree, event, 'acousticness', True) 

        speechinessTree = datentry['speechiness'] 
        actualizarArbol(speechinessTree, event, 'speechiness', True) 

        energyTree = datentry['energy'] 
        actualizarArbol(energyTree, event, 'energy', True) 

        danceabilityTree = datentry['danceability'] 
        actualizarArbol(danceabilityTree, event, 'danceability', True) 

        valenceTree = datentry['valence'] 
        actualizarArbol(valenceTree, event, 'valence', True) 

        tempoTree = datentry['tempo'] 
        actualizarArbol(tempoTree, event, 'tempo', True) 



    return datentry # y ya puedo retornar en paz mi nodo, sabiendo que quedó actualizado

# Funciones para creacion de datos

def newArtistEntry(artist_id):
    entry = {'artist': "", "events": None}
    entry['artist'] = artist_id
    entry['events'] = lt.newList('ARRAY_LIST', compareArtist)
    return entry

def newTracksEntry(track_id):
    entry = {'artist': "", "events": None}
    entry['track'] = track_id
    entry['events'] = lt.newList('ARRAY_LIST', compareTrack)
    return entry

def creadorDeNodos(esHijo = False):
    entry = {} # Fijate que el "entry" es un nodo... se complican la vida; en lugar de llamarlo nodo y ya
    entry['lstevents'] = lt.newList('SINGLE_LINKED', compareFeatures)
    entry['lstartists'] = lt.newList('SINGLE_LINKED', compareArtist)
    entry['lsttracks'] = lt.newList('SINGLE_LINKED', compareArtist)

    if not esHijo: # si no es hijo (por ende es padre) que cree los arboles internos 
        # Aqui creo los arboles dentro del nodo del arbol papá
        entry['instrumentalness'] = om.newMap(omaptype='BST',
                                        comparefunction=compareFeatures)
        entry['acousticness'] = om.newMap(omaptype='BST',
                                        comparefunction=compareFeatures)
        entry['liveness'] = om.newMap(omaptype='BST',
                                        comparefunction=compareFeatures)
        entry['speechiness'] = om.newMap(omaptype='BST',
                                        comparefunction=compareFeatures)
        entry['energy'] = om.newMap(omaptype='BST',
                                        comparefunction=compareFeatures)
        entry['danceability'] = om.newMap(omaptype='BST',
                                        comparefunction=compareFeatures)
        entry['valence'] = om.newMap(omaptype='BST',
                                        comparefunction=compareFeatures)
        entry['tempo'] = om.newMap(omaptype='BST',
                                        comparefunction=compareFeatures)
    return entry


# Funciones de consulta

def eventSize(analyzer):

    return lt.size(analyzer['events'])


def artistSize(analyzer):
    return om.size(analyzer['artist_id'])

def artistSize2(analyzer):
    return lt.size(analyzer['artist_id'])

def trackSize(analyzer):

    return om.size(analyzer['track_id'])

def firstFiveEvents(analyzer):
    subList = lt.subList(analyzer["events"], 0, 5)
    return subList

def LastFiveEvents(analyzer):
    subList = lt.subList(analyzer["events"], -5, 5)
    return subList


def getEventsByRange(analyzer, c1, vmin1, vmax1, c2, vmin2, vmax2):

    nodos = om.values(analyzer[c1], vmin1, vmax1) # obtener los nodos del arbol padre que cumplan con el rango

    eventosFinal = []

    for nodoArbolPadre in lt.iterator(nodos): # esos nodos que cumplan ese rango, tienen adentro otros arboles hijos
        arbolC2 = nodoArbolPadre[c2] # sacando el arbol de la caracteristica 2
        nodosHijos = om.values(arbolC2, vmin2, vmax2) # obtener los nodos del arbol hijo que cumplan con el rango
        
        for nodoArbolHijo in lt.iterator(nodosHijos):
            listaEventosHijos = nodoArbolHijo['lstevents']
            eventosFinal = eventosFinal+list(lt.iterator(listaEventosHijos))
        
    return eventosFinal


def getArtistsByRange(analyzer, c1, vmin1, vmax1, c2, vmin2, vmax2):

    nodos = om.values(analyzer[c1], vmin1, vmax1) # obtener los nodos del arbol padre que cumplan con el rango

    artistasFinal = []
    for nodoArbolPadre in lt.iterator(nodos): # esos nodos que cumplan ese rango, tienen adentro otros arboles hijos
        if c2:
            arbolC2 = nodoArbolPadre[c2] # sacando el arbol de la caracteristica 2
            nodosHijos = om.values(arbolC2, vmin2, vmax2) # obtener los nodos del arbol hijo que cumplan con el rango
            
            for nodoArbolHijo in lt.iterator(nodosHijos):
                listaArtitasHijos = nodoArbolHijo['lstartists']
                artistasFinal = artistasFinal+list(lt.iterator(listaArtitasHijos))
        else:
            listaArtitasPadre = nodoArbolPadre['lstartists']
            artistasFinal = artistasFinal+list(lt.iterator(listaArtitasPadre))
        
    return artistasFinal


def getTracksByRange(analyzer, c1, vmin1, vmax1, c2, vmin2, vmax2):

    nodos = om.values(analyzer[c1], vmin1, vmax1) # obtener los nodos del arbol padre que cumplan con el rango

    artistasFinal = []
    for nodoArbolPadre in lt.iterator(nodos): # esos nodos que cumplan ese rango, tienen adentro otros arboles hijos
        if c2:
            arbolC2 = nodoArbolPadre[c2] # sacando el arbol de la caracteristica 2
            nodosHijos = om.values(arbolC2, vmin2, vmax2) # obtener los nodos del arbol hijo que cumplan con el rango
            
            for nodoArbolHijo in lt.iterator(nodosHijos):
                listaArtitasHijos = nodoArbolHijo['lsttracks']
                artistasFinal = artistasFinal+list(lt.iterator(listaArtitasHijos))
        else:
            listaArtitasPadre = nodoArbolPadre['lsttracks']
            artistasFinal = artistasFinal+list(lt.iterator(listaArtitasPadre))
        
    return artistasFinal

def getUnicos(lst):
    list_set = set(lst)
    unique_list = list(list_set)
    return unique_list


def aleatoria(lista): 
    ale = []
    indicesQueYaSalieron = []
    if len(lista) < 8:
        return lista
        
    while len(ale) < 8:
        randIndex = random.randint(0, len(lista) - 1)
        eventoAleatorio = lista[randIndex]

        if randIndex not in indicesQueYaSalieron:
            ale.append(eventoAleatorio)
            indicesQueYaSalieron.append(randIndex)
    return ale

        
        


# Funciones utilizadas para comparar elementos dentro de una lista

def compareEvents(event1, event2):

    if (event1 == event2):
        return 0
    elif event1 > event2:
        return 1
    else:
        return -1

def compareArtist(artist1, artist2):

    if (artist1 == artist2):
        return 0
    elif (artist1 > artist2):
        return 1
    else:
        return -1

def compareTrack(track1, track2):

    if (track1 == track2):
        return 0
    elif (track1 > track2):
        return 1
    else:
        return -1

def compareFeatures(feature1, feature2):

    if (feature1 == feature2):
        return 0
    elif (feature1 > feature2):
        return 1
    else:
        return -1


# Funciones de ordenamiento

 