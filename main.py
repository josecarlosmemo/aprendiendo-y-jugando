'''
Autores: José Carlos Martínez y Fabricio Blanco.
'''

### NOTAS IMPORTANTES ###
'''
- Para instalar los modulos que no vienen preinstalados con python3 y 
son necesarios para el funcionamiento del programa basta con abrir cmd/Terminal y escribir:

pip3 install pyfiglet requests beautifulsoup4 unidecode

- El juego de ahorcado necesita una conexión a internet para ser jugado.

- Para el correcto funcionamiento del programa este debe ser abierto desde cmd/Terminal.

'''

### MODULOS IMPORTADOS ###

# Generales
from pyfiglet import figlet_format as banner
from time import sleep
from os import system, name

# Ahorcado
from requests import get
from bs4 import BeautifulSoup
from unidecode import unidecode

# Memorama
from random import randint, choice
from copy import deepcopy

'''
GENERALES
- Importamos la función figlet_format como banner, 
esto nos permite pasarle un string y crea un banner.

- Imporamos sleep del modulo tiempo, para hacer pequeños delays.

- Del modulo os importamos system y name.
Se utilizan para la función clear.

AHORCADO
- Importamos requests y beautifulsoup para poder hacer web scraping. 
 (Se utiliza en el ahorcado para obtener palabras.)
 
- Tambien importamos unidecode, para normalizar la palabra obtenida y eliminar acentos.

MEMORAMA
- Importamos randint y choice para generar números aletorios y llenar listas de manera aleatoria.

- Importamos deepcopy para poder crear copias de listas 

(Las listas son guardadas en memoria, entonces
si queremos guardar una copia de la lista sin editar la original es necesario).
'''

### FUNCIONES GENERALES ###

''' clear: Función que limpia la pantalla del usuario '''


def clear():
    if name == "posix":
        system("clear")
    else:
        system("cls")


''' format: Función que agrega colores y formatos 

Opciones de colores y formatos:
- Red
- Light Red
- Green
- Light Green
- Yellow
- Light Yellow
- Blue
- Magenta
- Light Magenta
- Cyan
- Light Cyan
- Bold
- Underline
'''


def format(text, color="default", format="default"):
    if format == "bold":
        format = "[1m"
    elif format == "underline":
        format = "[4m"
    else:
        format = ""

    if color == "red":
        color = "[31m"
    elif color == "green":
        color = "[32m"
    elif color == "yellow":
        color = "[33m"
    elif color == "blue":
        color = "[34m"
    elif color == "magenta":
        color = "[35m"
    elif color == "cyan":
        color = "[36m"
    elif color == "light-red":
        color = "[91m"
    elif color == "light-green":
        color = "[92m"
    elif color == "light-yellow":
        color = "[93m"
    elif color == "light-magenta":
        color = "[95m"
    elif color == "light-cyan":
        color = "[96m"
    else:
        color = ""

    if color != "" and format != "":
        return "\u001b" + color + "\u001b" + format + text + "\u001b[0m"
    elif color != "" and format == "":
        return "\u001b" + color + text + "\u001b[0m"
    elif color == "" and format != "":
        return "\u001b" + format + text + "\u001b[0m"
    else:
        return text


''' imagen: Esta función nos regresa la imagen que le pedimos. (trofeo o calabera)'''


def imagen(nombre):
    if nombre == "trofeo":
        image = '''
              .-=========-.
              \\'-=======-'/
              _|   .=.   |_
             ((|  {{1}}  |))
              \|   /|\   |/
               \__ '`' __/
                 _`) (`_
               _/_______\_
              /___________\\'''
    elif nombre == "skull":
        image = '''
             ..ooo@@@XXX%%%xx..
          .oo@@XXX%x%xxx..     ` .
        .o@XX%%xx..               ` .
      o@X%..                  ..ooooooo
    .@X%x.                 ..o@@^^   ^^@@o
  .ooo@@@@@@ooo..      ..o@@^          @X%
  o@@^^^     ^^^@@@ooo.oo@@^             %
 xzI    -*--      ^^^o^^        --*-     %
 @@@o     ooooooo^@@^o^@X^@oooooo     .X%x
I@@@@@@@@@XX%%xx  ( o@o )X%x@ROMBASED@@@X%x
I@@@@XX%%xx  oo@@@@X% @@X%x   ^^^@@@@@@@X%x
 @X%xx     o@@@@@@@X% @@XX%%x  )    ^^@X%x
  ^   xx o@@@@@@@@Xx  ^ @XX%%x    xxx
        o@@^^^ooo I^^ I^o ooo   .  x
        oo @^ IX      I   ^X  @^ oo
        IX     U  .        V     IX
         V     .           .     V'''
    return image


### FUNCIONES DE MENUS ###
# Menu Principal
menu_options = f'''
{format("¡Escoge!", "red", "bold")}
{format("1 - Ahorcado", "cyan", "bold")}
{format("2 - Memorama", "yellow", "bold")}
{format("0 - Salir", "magenta", "bold")}
{format("Respuesta: ", "green", "bold")}'''


def main_menu():
    clear()
    print(format(banner("Aprendiendo y Jugando"), "blue", "bold"))
    option = input(menu_options)
    if option == "1":
        ahorcado()
    elif option == "2":
        memorama()
    elif option == "0":
        print()
        print(format("¡Muchas Gracias por Jugar!", "yellow", "bold"))
        sleep(2)
        exit()
    else:
        print()
        print(format("Respuesta Invalida", "red"))
        sleep(2)
        clear()
        main_menu()


# Menu de Volver a Jugar
def play_again(juego):
    volver_a_jugar = f'''
        {format(f"¿Quieres volver a jugar {juego}?", "green", "bold")}
        {format("        SI (0) NO (1)", "yellow", "bold")}
        {format("Respuesta: ", "red", "bold")}'''
    clear()
    print(format(banner("Volver a Jugar"), "green", "bold"))
    respuesta = input(volver_a_jugar)
    if respuesta == "0" and juego == "Ahorcado":
        ahorcado()
    elif respuesta == "0" and juego == "Memorama":
        memorama()
    elif respuesta == "1":
        main_menu()
    else:
        print(format("Respuesta Invalida", "red", "bold"))
        sleep(2)
        play_again(juego)


### FUNCIONES DE AHORCADO ###
''' palabra: Hace web scraping a palabrasaleatorias.com y regresa una palabra en mayusculas y sin acentos. '''


def palabra():
    page = get("https://www.palabrasaleatorias.com/")
    word = BeautifulSoup(page.content, "html.parser").find(style="font-size:3em; color:#6200C5;").text.strip().upper()
    return unidecode(word)


''' espacios: Crea una lista con guiones representando cada letra de la palabra. '''


def espacios(word):
    spaces = []
    for i in range(len(word)):
        spaces.append("_")
    return spaces


'''imprime_ahorcado: Imprime la lista de characteres tapados o destapados'''


def imprime_ahorcado(lst):
    for i in lst:
        print(i, end=" ")


### FUNCIONES DE MEMORAMA ###

''' crea_tablero: Crea una martiz de 3x4 llena de "*". '''


def crea_tablero():
    matrix = []
    for r in range(4):
        row = []
        for c in range(3):
            row.append("*")
        matrix.append(row)
    return matrix


''' hidden: Crea una matriz 3x4 con los elementos a utilizar en el memorama. '''


def hidden():
    options = ["A", "B", "C", "D", "E", "F", "A", "B", "C", "D", "E", "F"]
    matrix = []
    for r in range(4):
        row = []
        for c in range(3):
            x = choice(options)
            row.append(x)
            options.pop(options.index(x))
        matrix.append(row)
    return matrix


''' imprime_tablero: Recibe una matriz y la imprime con formato de tarjeta. '''


def imprime_tablero(matrix):
    for i in matrix:
        row = f"        ".join(i)
        print(format(banner(row, "bubble"), "green", "bold"))


''' crea_operaciones: En base a la operacion regresa los elementos de la operación y su resultado en un array, 
se utiliza en conjunto con evalua_expresion().'''


def crea_operaciones(operacion):
    x = randint(1, 10)
    y = randint(1, 10)
    if operacion == "+":
        resultado = x + y
    elif operacion == "-":
        resultado = max(x, y) - min(x, y)
    elif operacion == "*":
        resultado = x * y
    return operacion, max(x, y), min(x, y), resultado


''' evalua_expresion: Recibe una lista de elementos (x,y,operador,resultado) y 
regresa True or False dependiendo de la respuesta del usuario'''


def evalua_expresion(array):
    print(format(f"{array[1]} {array[0]} {array[2]} = ?", "yellow", "bold"))
    while True:
        respuesta = input(format("Respuesta: ", "red", "bold"))
        if respuesta.isdigit() == False:
            print(format("Ingresa un número.", "red", "bold"))
            sleep(2)
            print("\033[A                             \033[A")
            print("\033[A                             \033[A")
            continue
        break

    if int(respuesta) == array[-1]:
        print(format("¡Muy bien! Puedes destapar una tarjeta.", "green", "bold"))
        sleep(2)
        return True
    else:
        print(format("Vuelve a intentarlo.", "red", "bold"))
        sleep(2)
        return False


''' input_destapa: Pide al usuario las coordenadas de la tarjeta y valida si estan 
correctas o si fueron utilizadas anteriormente. Regresa las coordenadas -1.'''


def input_destapa(tablero_temporal):
    while True:
        clear()
        print(format(banner("Memorama"), "yellow", "bold"))
        imprime_tablero(tablero_temporal)
        r = input(format("Renglón: ", "magenta", "bold"))
        if r.isdigit() == False:
            print(format("Ingresa un número", "red", "bold"))
            sleep(2)
            clear()
            continue
        r = int(r)
        if r < 1 or r > 4:
            print(format("Respuesta invalida", "red", "bold"))
            sleep(2)
            clear()
            continue

        c = input(format("Columna: ", "magenta", "bold"))
        if c.isdigit() == False:
            print(format("Ingresa un número", "red", "bold"))
            sleep(2)
            clear()
            continue

        c = int(c)
        if c < 1 or c > 3:
            print(format("Respuesta invalida", "red", "bold"))
            sleep(2)
            clear()
            continue

        if tablero_temporal[r - 1][c - 1] != "*":
            print(format("¡Esa carta ya fue destapada!", "red", "bold"))
            sleep(2)
            clear()
            continue
        break
    return r - 1, c - 1


''' destapa: Recibe las coordenadas el tablero actual y el tablero con las respuestas, 
regresa el tablero actual modificado.'''


def destapa(r, c, tablero_actual, tablero_oculto):
    tablero_actual[r][c] = tablero_oculto[r][c]
    return tablero_actual


''' evalua_memorama: Contiene la logica repetitiva del juego, 
Regresa el numero de pares obtenidos y el tablero más actualizado.'''


def evalua_memorama(tablero_temporal, tablero_oculto):
    count_pares = 0
    while True:
        tablero_original = deepcopy(tablero_temporal)
        if tablero_original == tablero_oculto:
            break
        destapadas = []
        for i in range(2):
            coordenadas = input_destapa(tablero_temporal)
            destapadas.append(coordenadas)
            tablero_temporal = destapa(coordenadas[0], coordenadas[1], tablero_temporal, tablero_oculto)
            clear()
            print(format(banner("Memorama"), "yellow", "bold"))
            imprime_tablero(tablero_temporal)
            sleep(2)
        if tablero_oculto[destapadas[0][0]][destapadas[0][1]] == tablero_oculto[destapadas[1][0]][
            destapadas[1][1]]:
            tablero = tablero_temporal.copy()
            print(format("¡Encontraste un par!", "green", "bold"))
            count_pares += 1
            sleep(2)
            continue

        else:
            tablero = tablero_original
            print(format("No son pares", "red", "bold"))
            sleep(5)
            break
    return count_pares, tablero


### JUEGOS ###
def ahorcado():
    ahorcado_imagen = ['''
      +---+
      |   |
          |
          |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
          |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|\  |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|\  |
     /    |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|\  |
     / \  |
          |
    =========''']
    juego = "Ahorcado"
    puntos = 0
    tries = 7
    guesses = 0
    wrongs = 0
    word_as_string = palabra()
    word_as_list = list(word_as_string)
    status = word_as_list.copy()
    display = espacios(word_as_list)
    used = []
    while tries > 0:
        clear()
        print(format(banner("Ahorcado"), "cyan", "bold"))
        print(format(f"                                     Puntos: {puntos}", "magenta", "bold"))
        print(format(ahorcado_imagen[wrongs], "green", "bold"))

        if display == word_as_list:  # Validamos si la palabra ya fue encontrada
            break

        imprime_ahorcado(display)
        if guesses != 0:  # Despliega las letras ya utilizadas
            usadas = ", "
            print(format(f"\n\nLetras usadas: {usadas.join(used)}", "yellow", "bold"))

        current_guess = input(format("\nIngresa una letra: ", "red", "bold")).upper()

        if current_guess in used:  # Validamos si la letra ya fue usada antes
            print(format(f"\nYa usaste la letra {current_guess}.", "yellow", "bold"))
            sleep(2)
            continue

        if not current_guess.isalpha():  # Validamos si se ingreso una letra. (No números o caracteres especiales)
            print(format("\nEl valor ingresado, no es una letra.", "red", "bold"))
            sleep(2)
            continue

        if len(current_guess) > 1:  # Validamos si se ingreso más de una letra
            print(format("\nIngresa solamente una letra.", "red", "bold"))
            sleep(2)
            continue

        if current_guess in status:  # Si la letra se encuentra en la palabra
            print(format("\n¡Correcto!", "green", "bold"))
            sleep(2)
            for i in range(word_as_list.count(current_guess)):
                display[status.index(current_guess)] = current_guess
                status[(status.index(current_guess))] = "*"
                puntos += 10
        else:  # Si la letra no esta en la palabra
            print(format("\nIntentalo de nuevo", "red", "bold"))
            sleep(2)
            tries -= 1
            wrongs += 1
        guesses += 1
        used.append(current_guess)
    clear()
    if wrongs == 7:
        print(format(imagen("skull"), "red", "bold"))
        print(format(banner("Perdiste"), "red", "bold"))
    else:
        print(format(imagen("trofeo"), "yellow", "bold"))
        print(format(banner("Ganaste"), "yellow", "bold"))
    print(format(f"La palabra correcta era: {word_as_string}. Obtuviste {puntos} puntos.", "yellow", "bold"))
    sleep(5)
    play_again(juego)


def memorama():
    juego = "Memorama"
    count_pares = 1
    tablero = crea_tablero()  # Crea tablero en blanco.
    tablero_oculto = hidden()  # Crea tablero con respuestas.
    while count_pares != 7:
        clear()
        print(format(banner("Memorama"), "yellow", "bold"))
        imprime_tablero(tablero)
        print(format("¡Responde operaciones matemáticas para destapar una tarjeta!", "cyan", "bold"))
        if count_pares <= 2:  # Si el número de pares abiertos es menor o igual a dos. (SUMAS)
            if evalua_expresion(
                    crea_operaciones("+")):  # Pregunta la operación y si la saco bien prosigue, sino genera otra.
                tablero_temporal = deepcopy(tablero)  # Hacemos una copia del tablero actual.
                evaluado = evalua_memorama(tablero_temporal,
                                           tablero_oculto)  # Pregunta las coordenadas y las valida. (Regresa: Tablero Acutualizado y número de pares abiertos.
                count_pares += evaluado[0]  # Sumamos los pares que abrio el usuario. (Si no hay le suma 0)
                tablero = evaluado[1]  # Actualizamos el tablero

        elif count_pares > 2 and count_pares <= 4:  # Si el número de pares abiertos esta entre 2 y 4. (RESTAS)
            if evalua_expresion(crea_operaciones("-")):
                tablero_temporal = deepcopy(tablero)
                evaluado = evalua_memorama(tablero_temporal, tablero_oculto)
                count_pares += evaluado[0]
                tablero = evaluado[1]

        else:  # Si el número de pares abiertos esta entre 4 y 6. (MULTIPLICACIONES)
            if evalua_expresion(crea_operaciones("*")):
                tablero_temporal = deepcopy(tablero)
                evaluado = evalua_memorama(tablero_temporal, tablero_oculto)
                count_pares += evaluado[0]
                tablero = evaluado[1]
    clear()
    print(format(imagen("trofeo"), "yellow", "bold"))
    print(format(banner("Ganaste"), "yellow", "bold"))
    sleep(5)
    play_again(juego)


### PROGRAMA PRINCIPAL ###
main_menu()
