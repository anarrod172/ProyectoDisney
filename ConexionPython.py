#Clase conexión
#Propósito: conectar Pycharm con Mongo y hacer un CRUD
#Autor: Asunción Naranjo Rodríguez
#Fecha:2024-05-17
import datetime

import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017") #Se conecta MongoDB a nuestro localhost.
db = client.peliculas_disney  #Se muestra el nombre de la bbdd  que vamos a usar
print(db.name) #Se muestra el nombre de la bbdd


#Definimos funciones para cada opción elegida en el menú.
#Opcion 1
def registrar_peliculas():
    while True:
        titulo = input("Introduce el titulo: ");
        añoLanzamiento = input("Introduce el año de lanzamiento de la película: ");
        decada = input("Introduce la década: ");
        genero = input("Introduce el género: ");
        duracion = input("Introduce la duración de la película: ");
        director = input("Introduce el autor o autores del libro separados por /: ");
        descripcion = input("Introduce una breve descripción del argumento de la película: ");
        valoracion = input("Introduce un número del 1 al cinco que indique si te ha gustado la película, siendo 1 no me ha gustado y 5 me ha encantado: ")

        db.peliculas.insert_one({
            "titulo": titulo,
            "añoLanzamiento": int(añoLanzamiento),
            "decada": decada,
            "genero":genero,
            "duracion":duracion,
            "director":director.split("/"),
            "descripcion":descripcion,
            "valoracion": int(valoracion)
        });

        salida = input("Introduce el símbolo + si quieres seguir registrando películas: ");
        if salida != "+":
            break;
    print("Se han registrado las películas correctamente.")

#Opcion 2
def actualizar_valoracion_peliculas():
    opcion = input("¿Cuántas películas desea actualizar?, si quiere actualizar una pulse 1, si quiere actualizar varias pulse 2: ");
    if opcion == "1":
        peliculas = input("¿A qué película deseas cambiarle la valoración? ");
        nuevaValoracion = int(input("Introduce la nueva valoración que tendrá la película: "));

        db.peliculas.update_one(
            {"titulo": peliculas},
            {"$set": {"valoracion": nuevaValoracion}}
        )
        print("Se ha actualizado la valoración de la película " + peliculas)
    else:
        opcion1 = input("¿Quieres buscar por titulo(t) o por director(d)? ");
        if opcion1 == "t":
            titulo = input("Introduce el título de la película que quieres actualizar: ");
            nuevaValoracion = input("Introduce la nueva valoración que tendrá la película: ");

            db.peliculas.update_many(
                {"titulo": titulo},
                {"$set": {"valoracion":nuevaValoracion}}
            )
        else:
            director = input("Introduce el nombre del director que quieres actualizar: ");
            valoracion = input("Introduce la nueva valoracion que tendrá la película: ");

            db.libros.update_many(
                {"director": director},
                {"$set": {"valoracion": valoracion}}
            )

#Opcion 3
def eliminar_solo_una_pelicula():
    peliculaEliminar = input("Introduce el título de la película que deseas eliminar: ")
    respuestaUs = input("¿Quieres eliminar la película " + peliculaEliminar + "? En caso afirmativo, pulse s y en caso negativo pulsa n. ");
    if respuestaUs == "s":
        db.peliculas.delete_one(
            {"titulo": peliculaEliminar}
        )
        print("Se ha eliminado la película " + peliculaEliminar);


#Opcion 4
def ver_peliculas_disponibles():
    peliculasDisponibles = db.peliculas.find()
    for peliculas in peliculasDisponibles:
        print(peliculas)


#Opcion 5
def buscar_peliculas():
    print("Selecciona una de las siguientes opciones de búsqueda: ");
    print("1.Búsqueda por titulo o director");
    print("2.Búsqueda por género y número de valoración");
    print("3.Búsqueda por título y década")
    opcionBuscar = input("Marque con un número del 1 al 3 la opción que desea: ")

    if opcionBuscar == "1":
        tituloDirector= input("Introduce el título o el director de la película que deseas buscar: ");

        busqueda = db.peliculas.find(
            {"$or": [{"titulo": tituloDirector}, {"director": tituloDirector}]}
        )
    elif opcionBuscar == "2":
        genero = input("Introduce el género de la película que deseas buscar: ");
        numeroValoracion = int(input("Introduce el número de valoración por el que deseas filtrar: "));
        comparacion = input("¿Quiere que la busqueda filtre por películas mayores(+) o menores(-) de la valoración insertada?: ");

        if comparacion == "+":
            busqueda = db.peliculas.find(
                {"$and": [{"genero": genero}, {"valoracion": {"$gte": numeroValoracion}}]}
            );
        else:
            busqueda = db.peliculas.find(
                {"$and": [{"genero": genero}, {"valoracion": {"$lte": numeroValoracion}}]}
            );
    elif opcionBuscar == "3":
        titulo = input("Introduce el título de la película que deseas buscar: ");
        decada = input("Introduce la década de la película que deseas buscar: ");

        busqueda = db.peliculas.find(
            {"$and": [{"titulo": titulo}, {"decada": decada}]}
        )
    else:
        busqueda = [];
        print("Elige bien");

    if opcionBuscar >= "1" and opcionBuscar <= "3":
        for peliculas in busqueda:
            print(peliculas)


#Opcion 6
def eliminar_peliculas():
     respuestaUs = input("¿Quieres eliminar todas los películas? En caso afirmativo, pulse s y en caso negativo pulsa n. ");

     if respuestaUs == "s":
         db.peliculas.delete_many({});
         print("Se han borrado los películas")
     else:
         print("Elija otro acción que desee realizar");


#Opcion 7
def eliminar_peliculas_disney():
    respuesta = input("¿Quieres eliminar peliculas_disney? En caso afirmativo, pulse s y en caso negativo pulsa n. ");

    if respuesta == "s":
        db.peliculas.drop();
    else :
        print("Elija otro acción que desee realizar");

#Opcion 9
def ver_años_peliculas():
    respuestaAnyo = int(input("Introduce el año a partir del cual desea buscar la película: "));
    comparacion = input("¿Quiere que la busqueda filtre por películas mayores(+) o menores(-) del año que ha seleccionado? ");

    if comparacion == "+":
        respuesta = db.peliculas.aggregate([
            {"$match": {"añoLanzamiento": {"$gte": respuestaAnyo}}},
            {"$sort": {"titulo": 1}},
            {"$project": {"_id": 1, "titulo": 1, "añoLanzamiento": 1, "decada": 1}}
        ]);
    else:
        respuesta = db.peliculas.aggregate([
            {"$match": {"añoLanzamiento": {"$lte": respuestaAnyo}}},
            {"$sort": {"titulo": 1}},
            {"$project": {"_id": 1, "titulo": 1, "añoLanzamiento": 1, "decada": 1}}
        ]);

    for peliculas in respuesta:
        print(peliculas)

#Menú de la aplicación
opcion = 0;
print("Bienvenido a la aplicación Disney Cinema.")
while opcion != "8":

    print("¿qué es lo que desea hacer?");

    print("1: Registrar una o varias películas nuevas en el catálogo");
    print("2: Actualizar la valoración de una película que hayas visto");
    print("3: Eliminar una película");
    print("4: Ver todas las películas del catálogo");
    print("5: Buscar por...");
    print("6: Eliminar todos las películas que haya registradas");
    print("7: Eliminar peliculas_disney");
    print("8: Salir");
    print("9: Ver los años de las películas");


    opcion = input("Marque con un número del 1 al 9 la opción que desea: ")

    if opcion == "1":
        registrar_peliculas();
    elif opcion == "2":
        actualizar_valoracion_peliculas();
    elif opcion == "3":
        eliminar_solo_una_pelicula();
    elif opcion == "4":
        ver_peliculas_disponibles();
    elif opcion == "5":
        buscar_peliculas();
    elif opcion == "6":
        eliminar_peliculas();
    elif opcion == "7":
        eliminar_peliculas_disney();
    elif opcion == "8":
        print("Salir");
    elif opcion == "9":
        ver_años_peliculas();
    else:
        print("Vuelve a introducir un valor válido entre 1 y 8");



