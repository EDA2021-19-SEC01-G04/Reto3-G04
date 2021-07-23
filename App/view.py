"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 * along withthis program.  If not, see <http://www.gnu.org/license.s/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


file = 'subsamples-small/context_content_features-small.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información")
    print("3- Consultar número de reproducciones según características de contenido")
    print("4- Consultar pistas recomendaddaas para Karaoke")
    print("5- Consultar pistas segun tempo y valencia")
    print("6- Consultar información según un género musical")


def printInfo1(events, inicio, eventsLstNormal = None):

    indice = inicio
    if eventsLstNormal: 
        iterador = eventsLstNormal
    else:
        iterador = lt.iterator(events)

    for event in iterador:

        print("Evento #", indice)

        print("--> Instrumentalidad: ", event["instrumentalness"] )
        print("--> Viveza: " +str((event["liveness"])))
        print("--> Habla: " +str(event["speechiness"]))
        print("--> Capacidad de baile: " +str(event["danceability"]))
        print("--> Valencia: " +str(event["valence"]))
        print("--> Sonoridad: " +str(event["loudness"]))
        print("--> Tempo: " +str(event["tempo"]))
        print("--> Acústica: " +str(event["acousticness"]))
        print("--> Energía: " +str(event["energy"]))
        print("--> Modo: " +str(event["mode"]))
        print("--> Clave: " +str(event["key"]))
        print("--> idiomma del tweet: " +str(event["tweet_lang"]))
        print("--> Fecha de creación: " +str(event["created_at"]))
        print("--> Idioma del usuario: " +str(event["lang"]))
        print("--> Zona horaria: " +str(event["time_zone"]))

        indice += 1

def printInfo2(events, inicio, eventsLstNormal = None):

    indice = inicio
    if eventsLstNormal: 
        iterador = eventsLstNormal
    else:
        iterador = lt.iterator(events)

    for event in iterador:

        print("Evento #", indice)

        print("--> Track ID: ", event["track_id"], "Con una viveza de: ", event["liveness"], " y Habla de: ", event["speechiness"])

        indice += 1

def printInfo3(events, inicio, eventsLstNormal = None):

    indice = inicio
    if eventsLstNormal: 
        iterador = eventsLstNormal
    else:
        iterador = lt.iterator(events)

    for event in iterador:

        print("Evento #", indice)

        print("--> Track ID: ", event["track_id"], "Con una valencia de: ", event["valence"], " y Tempo de: ", event["tempo"])

        indice += 1
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init() 


    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ...")
        controller.loadData(cont, file)
        print('Eventos de escucha cargados: ' + str(controller.eventSize(cont))) 
        print('Artistas cargados: ' + str(controller.artistSize(cont)))
        print('Pistas de audio cargadas: ' + str(controller.trackSize(cont))) 

        firstElements = controller.firstFiveEvents(cont)
        lastElements = controller.lastFiveEvents(cont)

        print("Información de contenido y contexto de los primeros 5 eventos: ")

        printInfo1(firstElements, 1)

        print("Información de contenido y contexto de los últimos 5 eventos: ")

        printInfo1(lastElements, controller.eventSize(cont) - 5)

    elif int(inputs[0]) == 3:
        c1 = input("Característica 1: ")
        vmin1 = input("Valor mínimo: ")
        vmax1 = input("Valor máximo: ")
        c2 = input("Característica 2: ")
        vmin2 = input("Valor mínimo: ")
        vmax2 = input("Valor máximo: ")
        print("Consultando...")

        result = controller.getEventsByRange(cont, c1, vmin1, vmax1, c2, vmin2, vmax2)
        resultArtistas = controller.getArtistsByRange(cont, c1, vmin1, vmax1, c2, vmin2, vmax2)

        artistasUnicas = controller.getUnicos(resultArtistas)

        print("El total de reproducciones encontradas para las características y el rango dado son: ", len(result))
        print("El total de artistas únicos son: ", len(artistasUnicas))
        

    elif int(inputs[0]) == 4:
        vmin1 = input("Valor mínimo para liveness: ")
        vmax1 = input("Valor máximo para liveness: ")
        vmin2 = input("Valor mínimo para speechiness: ")
        vmax2 = input("Valor máximo para speechiness: ")
        print("Consultando...")

        result = controller.getEventsByRange(cont, "liveness", vmin1, vmax1, "speechiness", vmin2, vmax2)
        aleatorias = controller.aleatorias(result)

        print("8 canciones aleatorias son: ",)
        printInfo2(None, inicio=1, eventsLstNormal=aleatorias)

    elif int(inputs[0]) == 5:
        vmin1 = input("Valor mínimo para tempo: ")
        vmax1 = input("Valor máximo para tempo: ")
        vmin2 = input("Valor mínimo para valence: ")
        vmax2 = input("Valor máximo para valence: ")
        print("Consultando...")

        result = controller.getEventsByRange(cont, "tempo", vmin1, vmax1, "valence", vmin2, vmax2)
        aleatorias = controller.aleatorias(result)

        print("8 canciones aleatorias son: ",)
        printInfo3(None, inicio=1, eventsLstNormal=aleatorias)

    elif int(inputs[0]) == 6:
        genero = input("Ingrese genero musical que desea consultar: ")

        if genero.lower() == "Reggae".lower():
            vmin1 = "60"
            vmax1 = "90"
            artis = controller.getArtistsByRange(cont, "tempo", vmin1, vmax1, None, None, None)
            tracks = controller.getTracksByRange(cont, "tempo", vmin1, vmax1, None, None, None)
        
        elif genero.lower() == "Down-tempo".lower():
            vmin1 = 70
            vmax1 = 100
            artis = controller.getArtistsByRange(cont, "tempo", vmin1, vmax1, None, None, None)
            tracks = controller.getTracksByRange(cont, "tempo", vmin1, vmax1, None, None, None)

        elif genero.lower() == "Chill-out".lower():
            vmin1 = 90
            vmax1 = 120
            artis = controller.getArtistsByRange(cont, "tempo", vmin1, vmax1, None, None, None)
            tracks = controller.getTracksByRange(cont, "tempo", vmin1, vmax1, None, None, None)

        elif genero.lower() == "Hip-hop".lower():
            vmin1 = 85
            vmax1 = 115
            artis = controller.getArtistsByRange(cont, "tempo", vmin1, vmax1, None, None, None)
            tracks = controller.getTracksByRange(cont, "tempo", vmin1, vmax1, None, None, None)

        elif genero.lower() == "Jazz and Funk".lower():
            vmin1 = 120
            vmax1 = 125
            artis = controller.getArtistsByRange(cont, "tempo", vmin1, vmax1, None, None, None)
            tracks = controller.getTracksByRange(cont, "tempo", vmin1, vmax1, None, None, None)

        elif genero.lower() == "Pop".lower():
            vmin1 = 100
            vmax1 = 130
            artis = controller.getArtistsByRange(cont, "tempo", vmin1, vmax1, None, None, None)
            tracks = controller.getTracksByRange(cont, "tempo", vmin1, vmax1, None, None, None)

        elif genero.lower() == "R&B".lower():
            vmin1 = 60
            vmax1 = 80
            artis = controller.getArtistsByRange(cont, "tempo", vmin1, vmax1, None, None, None)
            tracks = controller.getTracksByRange(cont, "tempo", vmin1, vmax1, None, None, None)

        elif genero.lower() == "Rock".lower():
            vmin1 = 110
            vmax1 = 140
            artis = controller.getArtistsByRange(cont, "tempo", vmin1, vmax1, None, None, None)
            tracks = controller.getTracksByRange(cont, "tempo", vmin1, vmax1, None, None, None)

        elif genero.lower() == "Metal".lower():
            vmin1 = 100
            vmax1 = 160
            artis = controller.getArtistsByRange(cont, "tempo", vmin1, vmax1, None, None, None)
            tracks = controller.getTracksByRange(cont, "tempo", vmin1, vmax1, None, None, None)
        
        unicosArtis = controller.getUnicos(artis)
        unicosTracks = controller.getUnicos(artis)
        print("El total de artistas únicos son: ", len(unicosArtis))
        print("El total de tracks únicos son: ", len(unicosTracks))

    else: 
        sys.exit(0)
sys.exit(0)
 