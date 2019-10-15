# -*- encoding: 850 -*-
########### El programa que se presenta a continuación esconde un texto dentro de una imagen de manera que 
########### este no pueda ser visto por terceros a simple vista.
############### IDENTIFICACIÓN
######### Versión: 1.6
######### Fecha: 28-02-2016
############### BLOQUE DE DEFINICIÓN
############### DEFINICIÓN DE CONSTANTES
############### IMPORTACIÓN DE FUNCIONES
from PIL import Image                      #### Con esta librería se podrá abrir imágenes para luego editarlas 
                                           #### internamente y posterior a eso guardarla, lo cual es esencial 
                                           #### para este programa.

from Tkinter import Tk                     #### Tkinter ayudará al programa a dar una mejor interfaz al usuario 
                                           #### y que sea más "didáctico" con éste.

from tkFileDialog import askopenfilename   #### Función de Tkinter que pedirá a través de una ventana al usuario, 
                                           #### la imagen que desea ingresar. Pero lo que realmente hace la función
                                           #### es que cuando se ingrese la imagen, retornará la ubicación de dicho
                                           #### archivo. (Se complementará con la función importada PIL).
from tkFileDialog import askdirectory      #### Función de Tkinter que pedirá a través de una ventana al usuario, 
                                           #### la ubicación de donde desea guardar su imagen nueva ya con el texto oculto.

############### DEFINICIÓN DE FUNCIONES

####### Función para transformar un texto ingresado por el usuario en formato string a otro string que 
####### contiene el mismo texto pero en sistema binario, cabe destacar que se le agrega el binario de 
####### 255 para efectos reversos del programa; al inicio para verificar que posee un texto la imagen; 
####### y el binario de 255 al final para ver hasta donde el programa tiene que leer.
#### Entrada: Texto en formato string.
#### Salida: String del texto ingresado por el usuario en sistema binario más el binario de 255 por delante y atrás.
## Ejemplo: "Texto: python ---->  codigoBinarioDelTexto = 1111111101110000011110010111010001101000011011110110111011111111" 
## (Cabe destacar que el código binario de "python" es 011100000111100101110100011010000110111101101110, pero para efectos 
## del programa se le agregan el binario de 255 al principio y al final del texto).
def transformarTextoABinario(textoIngresado):
    codigoAsciiDelTexto=[]
    for letra in textoIngresado:
        codigoAsciiDelTexto.append(ord(letra)) ### ord() es una función de Python para entregar el código ASCII de una 
                                               ### letra, valor, símbolo, etc.
    listaBinarioDelTexto = []
    for valor in codigoAsciiDelTexto:
        if valor<=63:
            listaBinarioDelTexto.append(bin(valor).replace("b","0")) ### Cuando se aplica la función bin(valor) retorna 
                                                                     ### el binario con una "b", por ejemplo: 0b0100, por 
                                                                     ### lo tanto se le cambia la "b" por un "0" o un 
                                                                     ### string vacio "" dependiendo de la cantidad de bit 
                                                                     ### que posee, ya que este no influye en su resultado, 
                                                                     ### y en una función más adelante se agregarán "0" a 
                                                                     ### la izquierda si el binario no posee 8 bit, puesto 
                                                                     ### que eso es lo que se necesita para este programa.
        elif valor>=128:
            listaBinarioDelTexto.append(bin(valor).lstrip("0").replace("b","")) ### La función lstrip("x") elimina un valor 
                                                                                ### x a una string temporalmente.
        else:
             listaBinarioDelTexto.append(bin(valor).replace("b",""))
        codigoBinarioDelTexto="".join(listaBinarioDelTexto)
    return "11111111" + codigoBinarioDelTexto + "11111111" ### Se le agrega el binario de 255 para efectos reversos del 
                                                           ### programa; al inicio para verificar que posee un texto la 
                                                           ### imagen; y el binario de 255 al final para ver hasta donde 
                                                           ### el programa tiene que leer.

####### Función para ingresar una imagen al programa utilizando la librería PIL.
#### Entrada: Ubicación de la imagen, nombre y su formato.
#### Salida: Imagen abierta en el programa para ser procesada, obteniendo de ellas información como cantidad de pixeles, 
#### formato, etc.
## Ejemplo: "ubicacionArchivo = C:/Users/User/Desktop/ImagenAProcesar.bmp"
def ingresarImagen(ubicacionArchivo):
    archivoImagen = Image.open(ubicacionArchivo)  ### Aquí se utiliza la función importada "from PIL import Image".
    return archivoImagen

####### Función para descomponer la imagen ingresada por el usuario y obtener una lista de pixeles de RGB en binario.
#### Entrada: Información de la imagen abierta ya ingresada por el usuario.
#### Salida: Descomposición de la imagen en formato de lista de pixeles de RGB en binario.
## Ejemplo: "-----> [['1', '1', '1', '1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1', '1', '1', '1']]"
def descomponerImagenPorPixelesEnRgb(imagenAbierta):
    pixeles = list(imagenAbierta.getdata())                     ### De la información de la imagen ingresada a través 
                                                                ### de esta función se obtienen los pixeles en formato 
                                                                ### de lista de RGB en decimal.
    binario = []
    for rgb in pixeles:
        for color in rgb:
            binario.append(bin(color).replace("b",""))          ### De la lista de pixeles en decimal se transforma a una 
                                                                ### lista de binario.
    listaBinarioArreglada=[]
    for contador in range(len(binario)):
        listaBinarioArreglada.append(list(binario[contador]))   
    for valor in listaBinarioArreglada:
        if len(valor)== 2:
            for contador1 in range(6):
                valor.insert(0,"0")
        elif len(valor) == 3:
            for contador2 in range(5):
                valor.insert(0,"0")
        elif len(valor) == 4:
            for contador3 in range(4):
                valor.insert(0,"0")
        elif len(valor) == 5:
            for contador4 in range(3):
                valor.insert(0,"0")
        elif len(valor) == 6:
            valor.insert(0,"0")
            valor.insert(0,"0")
        elif len(valor) == 7:
            valor.insert(0,"0")
        elif len(valor) == 9:
            valor.remove("0")
        elif len(valor) == 10:
            valor.remove("0")
            valor.remove("0")
    return listaBinarioArreglada                                ### Se arregla la lista de binarios ya que algunos binarios 
                                                                ### poseen cantidad de bit que varían entre 2 y 9, por lo 
                                                                ### que se arregla para que todas posean 8 bit.

####### Funciónn para utilizar la técnica del bit menos significativo.
###### La técnica del bit menos significativo consiste en intercambiar el valor numérico del último número de cada byte 
###### en binario por otro valor que forme una palabra, esta función será la más importante dentro del programa ya que
###### con esta función se podrá esconder el texto en la imagen.
#### Entrada: Lista con cada valor numérico en binario de los colores de cada pixel en la imagen, además el texto que 
#### se quiere esconder en la imagen en binario.
#### Salida: La misma lista pero con el texto dentro de la imagen.
## Ejemplo: "Texto = "01" -- [['1', '1', '1', '1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1', '1', '1', '1']] 
## -----> [['1', '1', '1', '1', '1', '1', '1', '0 #se cambia# '], ['1', '1', '1', '1', '1', '1', '1', '1 #se cambia# ']]"
def utilizarTecnicaBitMenosSignificativo(texto, descomposicionImagen):
    for cnt in range(len(texto)):
        descomposicionImagen[cnt][7] = texto[cnt]
    return descomposicionImagen

####### Función para transformar la lista  que contiene dentro de ella listas de RGB de los pixeles a una lista de los 
####### RGB de los pixeles en decimal.
#### Entrada: Lista de listas de RGB.
#### Salida: Lista de RGB en decimal, agrupadas por pixeles.
## Ejemplo: "[['1', '1', '1', '1', '1', '1', '1', '1'],['1', '1', '1', '1', '1', '1', '1', '1'],
## ['1', '1', '1', '1', '1', '1', '1', '1'],['1', '1', '1', '1', '1', '1', '1', '1'],
## ['1', '1', '1', '1', '1', '1', '1', '1'],['1', '1', '1', '1', '1', '1', '1', '1']] -----> [(255,255,255), (255,255,255)]"
def transformarListadeListaRgbaListadeListasAsciiAgrupada(lista):
    listaBinario=[]
    for rgb in lista:
        rgbBinario =""
        for cnt in range(len(rgb)):
            rgbBinario = rgbBinario + str(rgb[cnt])
        listaBinario.append(rgbBinario)
    listaDecimal=[]
    for binario in listaBinario:
        listaDecimal.append(int(str(binario),2))                        ### int(str(binario),2) se utiliza para transformar 
                                                                        ### de binario a decimal, en este caso a código ASCII.
    listaAgrupada=[]
    contador=0
    while contador < len(listaDecimal):
        listaTemporal=[]
        for cntAux in range(3):
            listaTemporal.append(listaDecimal[contador])
            contador = contador + 1
        listaAgrupada.append(tuple(listaTemporal))                      ### La Función tuple() lo que hace es transformar una lista 
                                                                        ### en formato [1,2,3] a una lista (1,2,3), se realiza esta 
                                                                        ### función para posteriormente guardarla como imagen.
    return listaAgrupada

####### Función para crear una imagen a partir de la lista y de la imagen ingresada.
#### Entrada: Lista de tuplas para intercambiar cada pixel de la imagen original, la imagen original, y el nombre de la imagen nueva.
#### Salida: Guardar una imagen en formato 'bmp'.
## Ejemplo: "[(255,255,255), (255,255,255)] -- Imagen -----> imagenNueva = [(255,255,255), (255,255,255)]"
def crearImagenAPartirDeLista(lista, imagen, nombreArchivoGuardado):
    coordenadaX =imagen.size[0]                 ### Se obtiene las coordenadas de la imagen, en cuanto a pixeles.
    coordenadaY=imagen.size[1]
    pix = imagen.load()
    cnt=0
    while cnt<len(lista):
        for cnt2 in range(coordenadaY):
            for cnt1 in range(coordenadaX):
                pix[cnt1, cnt2] = lista[cnt]    ### Se van intercambiando cada valor de las coordenadas en la imagen ingresada 
                                                ### con los de la lista de imagen que posee el texto.
                cnt = cnt + 1
            cnt1 = 0
    return imagen.save(nombreArchivoGuardado)

####### Función para obtener una lista de listas con un supuesto texto escrito en binario agrupados por byte.
#### Entrada: Lista que contiene los RGB de una imagen en binario.
#### Salida: Lista que contiene agrupados por cada 8 elementos el último bit de cada supuesto texto.
## Ejemplo: "lista: [['1', '1', '1', '1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1', '1', '1', '1'], 
## ['1', '1', '1', '1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1', '1', '1', '1']] ----->
## ['11111111', '11111111', '11111111', '11111111']" 
def listaAgrupadaSupuestoTexto(lista):
    bitSupuestoTexto = []
    for cnt in range(len(lista)):
        bitSupuestoTexto.append(lista[cnt][7])
    while len(bitSupuestoTexto)%8!=0:
        bitSupuestoTexto.pop(-1)
    byteSupuestoTexto=[] 
    cnt1=0
    while cnt1 < len(bitSupuestoTexto):
        listaTemporal=[]
        for cntAux in range(8):
            listaTemporal.append(bitSupuestoTexto[cnt1])
            cnt1 = cnt1 + 1
        byteSupuestoTexto.append(listaTemporal)
    listaStringBin = []
    for bit in byteSupuestoTexto:
        listaStringBin.append("".join(bit))
    return listaStringBin

####### Función para transformar la lista de binario en una lista de decimales (supuesto código ASCII).
#### Entrada: Lista que contiene supuesto código en binario separados por letra.
#### Salida: Lista que contiene los decimales de los binarios, es decir supuesto código ASCII separados por letras.
## Ejemplo: "['11111111', '11111111', '11111111', '11111111', '11111111', '11111111', '11111111'] --> 
## [255, 255, 255, 255, 255, 255, 255]"
def transformarBinarioADecimal(lista):
    listaDecimales=[]
    for binario in lista:
        listaDecimales.append(int(binario, 2))
    return listaDecimales

####### Función para transformar la lista de supuesto texto en código ASCII a una lista de caracteres.
#### Entrada: Supuesto texto en código ASCII separados por letras en formato de lista.
#### Salida: Supuesto texto en caracteres por letras en una lista.
## Ejemplo: "[104, 111, 108, 97] ---->  "hola""
def transformarAsciiCaracter(lista):
    listaCaracteres=[]
    if lista[0] == 255:
        for ascii in lista[1:len(lista)]:  ### Se inicia desde el 1 para darle la condición si posee texto o no la imagen.
            if ascii==255:
                return "".join(listaCaracteres)    
            else:
                listaCaracteres.append(chr(ascii))
    else:
        return ""
    return "".join(listaCaracteres)

####### Función para mostrar al usuario cuantos caracteres puede escribir como máximo.
#### Entrada: La ubicación de la imagen.
#### Salida: Cantidad de caracteres disponibles por la imagen.
def cantidadMaximaDeCaracteres(ubicacionImagen):
    archivoImagen = Image.open(ubicacionImagen)
    pixeles= list(archivoImagen.getdata())
    return int((len(pixeles))*3/8) - 16   ### A la cantidad de pixeles se le multiplica por 3 por el hecho de que un pixel 
                                          ### tiene la capacidad de almacenar 3 byte, de un carácter (1byte)
                                          ### que posee 8 bit de acuerdo a la técnica que se está utilizando, se divide por 8, 
                                          ### por lo anteriormente indicado, y se le resta 16 ya que se 
                                          ### agregaron 8 bit antes y después del texto para verificar si una imagen posee un texto.

####### Función de la opción 1 (opcion1) para guardar un texto en una imagen en formato BMP.
#### Entrada: Texto dado por el usuario y el archivo de imagen donde se desea guardar el texto.
#### Salida: Archivo de imagen en formato BMP con el texto oculto.
def opcion1(texto, imagen, nombreArchivoGuardado):
    textoAOcultar = transformarTextoABinario(texto)
    imagen1 = ingresarImagen(imagen)
    lista = descomponerImagenPorPixelesEnRgb(imagen1)
    lsb = utilizarTecnicaBitMenosSignificativo(textoAOcultar,lista)
    agrupada = transformarListadeListaRgbaListadeListasAsciiAgrupada(lsb)
    imagenCreada = crearImagenAPartirDeLista(agrupada,imagen1,nombreArchivoGuardado)
    return imagenCreada

####### Función de la opción 2 (opcion2) para encontrar un texto oculto dentro de una imagen.
#### Entrada: Archivo de imagen en formato BMP.
#### Salida: Texto encontrado en la imagen.
def opcion2(archivo):
    imagen = ingresarImagen(archivo)
    pixeles = descomponerImagenPorPixelesEnRgb(imagen)
    supuestoTexto = listaAgrupadaSupuestoTexto(pixeles)
    supuestoTextoAscii = transformarBinarioADecimal(supuestoTexto)
    caracteres = transformarAsciiCaracter(supuestoTextoAscii)
    return caracteres

####### Función para dar a elegir al usuario que camino desea seguir, si guardar un texto dentro de una imagen o encontrar 
####### el texto escondido en una imagen.
#### Entrada: Opción 1 u opción 2.
#### Salida: Si es opción 1, imagen guardada con texto dentro, si es opción 2 retornará un texto.
def menu(opcion):
    if opcion == "1":
        print "------------------------------------------------ \nUsted ha seleccionado la opción de esteganografía para ocultar texto en una imagen...\n"
        iforelse = raw_input("-------------- INGRESANDO IMAGEN --------------- \n\nPresione 'ENTER' para ingresar la imagen en donde desea ocultar el texto. \nNOTA: El programa sólo acepta imágenes en formato 'bmp'.\n")
        Tk().withdraw()
        imagen = askopenfilename()
        while imagen[-3:len(imagen)]!= "bmp" and imagen[-3:len(imagen)]!= "BMP":
            iforelse = raw_input("Se ingresó un archivo incorrecto, recuerde que el programa sólo acepta formato 'bmp', para ingresar nuevamente presione 'ENTER'.\n")
            Tk().withdraw()
            imagen = askopenfilename()
        print "ARCHIVO: ", imagen, "\n"
        print "---------- INGRESANDO TEXTO A OCULTAR ----------\n\nPor favor ingrese el texto que desea ocultar...\nNOTA: Usted tiene un máximo de ",cantidadMaximaDeCaracteres(imagen)," caracteres disponibles."
        texto = raw_input("Texto: ")
        if len(texto)<=cantidadMaximaDeCaracteres(imagen):
            ""
        else:
            texto = texto[0:cantidadMaximaDeCaracteres(imagen)]
            print "La cantidad de caracteres del texto se excedió del máximo, su texto se acortará a ",cantidadMaximaDeCaracteres(imagen), " caracteres, su nuevo texto quedara como: ",texto,"..."
        print "\n------------ GUARDANDO IMAGEN NUEVA ------------ \n"    
        ifforelse = raw_input("a) Presione 'ENTER' para ingresar la ubicación en donde desea guardar su imagen nueva. \n")
        Tk().withdraw()
        dirSelected = askdirectory()
        while dirSelected == "":
            ifforelse=raw_input("Ingresar ubicación valida, presione 'ENTER' para intentarlo nuevamente.\n")
            Tk().withdraw()
            dirSelected = askdirectory()
        nombre = raw_input("b) Ingresar nombre de la imagen nueva: ")
        if len(nombre)>222:
            print "\nSe ingresó un nombre muy largo para el archivo, el nombre de la imagen nueva se acortará a nombre de archivo: \n", nombre[0:222]
        nombreArchivoGuardado = dirSelected + "/" + nombre[0:221] + ".bmp"
        print "\nCargando... \n\n------------------------------------------------"
        opcion1(texto,imagen,nombreArchivoGuardado)
        print "\nLa imagen se ingresó correctamente y el texto ingresado ya se ocultó dentro de ést, su archivo nuevo se encuentra en: \n",nombreArchivoGuardado
    elif opcion == "2":
        print "------------------------------------------------ \nUsted ha seleccionado la opción de esteganografía para encontrar el texto oculto en una imagen... \n\n-------------- INGRESANDO IMAGEN ---------------"
        iffforelse = raw_input("Por favor ingrese 'ENTER' para obtener la ubicación del archivo imagen BMP en donde desea verificar texto oculto. \nNOTA: El programa sólo acepta imágenes en formato 'bmp'.\n")
        Tk().withdraw()
        archivo = askopenfilename()
        while archivo[-3:len(archivo)] != "bmp":
            iffforelse = raw_input("Se ingresó un archivo incorrecto, recuerde que el programa sólo acepta formato .bmp, para ingresar nuevamente presione 'ENTER'.\n")
            Tk().withdraw()
            archivo = askopenfilename()
        print "ARCHIVO: ", archivo, "\n\nCargando... \n\n------------------------------------------------\n"
        if opcion2(archivo) == "":
            print "La imagen ingresada no posee un texto oculto."
        else:
            print "El texto oculto en la imagen es: \n", opcion2(archivo)
    else:
        print "\n-------------------------------------------------------------------------------------------------------\nInformación del programa.\n\nEl proyecto de esteganografía es un proyecto realizado por un grupo de estudiantes de la clase\nFundamentos de Computación y Programación de la Universidad de Santiago de Chile, con el fin de\naprender a elaborar programas computacinales para la resolución de problemas de ingeniería\naplicada a distintos contextos, usando lenguaje de programación Python, mostrando preocupación\npor la generalidad y las buenas prácticas de programación, de forma crítica, pertinente y creativa,\nresguardando criterios de innovación y emprendimiento(Según programa del curso Fundamentos de\ncomputación y programación). \n\n-------------------------------------------------------------------------------------------------------\nFuncionamiento del programa. \n\nEl programa de esteganografía oculta un texto en una imagen (las dos ingresadas por el\nusuario), con la idea de que la imagen que salga del programa sea casi idéntica a la ingresada\nanteriormente, y así darle diferentes usos.\nPor otro lado también se da la opción al usuario  para ingresar una imagen y verificar si tiene\nun texto oculto en la imagen; si lo tiene mostrar el texto, y si no indicar al usuario que la\nimagen ingresada no posee un texto oculto."
    return opcion

############### BLOQUE PRINCIPAL
########## ENTRADA
opcion = raw_input("---------------------------------------------------\nBIENVENIDO AL PROGRAMA DE ESTEGANOGRAFÍA (versión 1.6) \n\nPor favor escoja una opción:\na) Para ocultar texto en una imagen:             Ingrese número 1\n\nb) Para obtener texto oculto en una imagen:      Ingrese número 2 \n\nPara conocer la información de este programa: 	 Presione ENTER \n\nOpción: ")
########## PROCESAMIENTO
while opcion != "1" and opcion != "2" and opcion != "":
    opcion = raw_input("\nSe ingresó una opción incorrecta, por favor ingresar nuevamente: \na) Para ocultar texto en una imagen:             Ingrese número 1 \n\nb) Para obtener texto oculto en una imagen:      Ingrese número 2 \n\nOpción: ")
mostrarMenu = menu(opcion)
########## SALIDA
mostrarMenu
print "\nGracias por utilizar este programa..."""
auxiliar = raw_input("") ### Se utiliza esta entrada auxiliar para que cuando se ejecute el programa en la consola de Python, 
                         ### no se cierre al termino de su proceso.
