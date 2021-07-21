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
    return analyzer

# Funciones para agregar informacion al catalogo

def addEvent(analyzer, event):

    lt.addLast(analyzer['events'], event)
    addArtistId(analyzer, event)
    addTrackId(analyzer, event)


def addArtistId(analyzer, event):
    try:
        artists = analyzer['artist_id']
        artist_id = event['artist_id']

        existArtist = om.contains(artists, artist_id)

        if existArtist:
            entry = om.get(artists, artist_id)
            artistEntry = me.getValue(entry)
        else:
            artistEntry = newArtistEntry(artist_id)
            om.put(artists, artist_id, artistEntry)
        lt.addLast(artistEntry['artist_id'], event)
    except Exception:
        return None

def addTrackId(analyzer, event):
    try:
        track = analyzer['track_id']
        track_id = event['track_id']

        existTrack = om.contains(track, track_id)

        if existTrack:
            entry = om.get(track, track_id)
            trackEntry = me.getValue(entry)
        else:
            trackEntry = newArtistEntry(track_id)
            om.put(track, track_id, trackEntry)
        lt.addLast(trackEntry['track_id'], event)
    except Exception:
        return None

    
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

# Funciones de consulta
def eventSize(analyzer):

    return lt.size(analyzer['events'])


def artistSize(analyzer):

    return om.size(analyzer['artist_id'])

def trackSize(analyzer):

    return om.size(analyzer['track_id'])

# Funciones utilizadas para comparar elementos dentro de una lista

def compareEvents(event1, event2):
    """
    Compara dos crimenes
    """
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

# Funciones de ordenamiento
