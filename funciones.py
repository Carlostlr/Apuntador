#importamos la libreria tkinter y las ventanas emergentes y creamos la raiz
from tkinter import *
from tkinter import messagebox
#from io import open
import pickle
import sqlite3

#----------------------------------------------------------------------------------------------------------------------------
root=Tk()

#le damos un titulo, que no se pueda redimensionar con 0,0 y le asignamos un icono
root.title("Apuntes")
root.resizable(0,0)
root.geometry("+290+70")

#importamos el modulo para crear botones
from objetos import *

#----------------------------------------FRAME PANTALLA PRINCIPAL---------------------------------------------------------------

#definimos la funcion de la pantalla principal
def principal():

    #creamos el Frame
    inicio=Frame(root,bg="#3c3c3c")
    inicio.pack()

    #----------------------------------------FUNCIONES MANIPULACION DEL MENU--------------------------------------------------------------------------

    #creamos la funcion para añadir elementos al listbox
    def add():
        tit=titulo.get()

        # creamos una condicion para que si no ponemos nada salte una ventana de emergencia y no haga nada
        if tit=="":
            messagebox.showwarning("Alerta","No has insertado nada, por favor, intentalo de nuevo")

        else:
            #comprobamos que el valor introducio no está ya en la lista
            if tit in str1:
                messagebox.showwarning("Alerta","Ese nombre ya existe, por favor, intentalo de nuevo con otro nombre distinto")

            else:
                #añadimos el elemento a la lista
                str1.append(tit)

                #reescribimos el archivo con la lista con el elemento nuevo
                fin=open("nombres", "wb")
                pickle.dump(str1,fin)
                fin.close()

                #insertamos el valor introducido al final del listbox
                listbox.insert(END,titulo.get())

                #borramos el entry para dejarlo vacio
                titulo.set("")

    #--------------------------------------------------------------------

    #creamos la funcion para añadir elementos al listbox
    def delete():
        #borra el elemento de la posicion señalado en la lista
        index=listbox.curselection()[0]
        listbox.delete(index)

        #borra el elemento que esta en la posicion indicada con el index de arriba
        num=str1[index]
        str1.remove(num)

        #reescribimos el archivo con la lista con el elemento borrado
        fin=open("nombres", "wb")
        pickle.dump(str1,fin)
        fin.close()

        try:
            borra=bbdd(num,"","","","")
            borra.delete_table()

            #borramos el entry para dejarlo vacio
            titulo.set("")
        except:
            #borramos el entry para dejarlo vacio
            titulo.set("")


    #--------------------------------------------------------------------

    #creamos la funcion para entrar en el frame de consultas
    def enter():
        tit=titulo.get()
        #comprobamos que el valor introducio no está ya en la lista
        if tit in str1:
            inicio.destroy()
            consult(tit)
        else:
            messagebox.showwarning("Alerta","Ese nombre no existe, se añadira automaticamente a su lista")

            #añadimos el elemento a la lista
            str1.append(tit)

            #reescribimos el archivo con la lista con el elemento nuevo
            fin=open("nombres", "wb")
            pickle.dump(str1,fin)
            fin.close()

            #insertamos el valor introducido al final del listbox
            listbox.insert(END,titulo.get())

            #borramos el entry para dejarlo vacio
            titulo.set("")


    #---------------------------------------------VARIABLES PARA LOS ENTRY----------------------------------------------------------

    #creamos las variables para los entry
    titulo=StringVar()

    #----------------------------------------CREA Y LEE EL ARCHIVO DE TEXTO-----------------------------------------------

    # creamos/abrimos el archivo nombres donde se guardarna todos los nombres del listbox, lo leemos y cerramos el archivo
    try:
        # leemos los datos del archivo nombres.txt
        fin=open("nombres","rb")
        list=pickle.load(fin)
        fin.close()

        # pendiente de investigar
        str1=[i.rstrip() for i in list]

    except:
        # si al leer no existe el archivo con la excepcion creara el archivo y la lista vacia
        lst=['']
        fin=open("nombres","wb")
        pickle.dump(lst,fin)
        fin.close()

        str1=[]


    #----------------------------------------listbox------------------------------------------------------------------------------------

    # creamos la funcion para que obtenga el valor al hacer click sobre un elemento
    def obtiene_valor(event):
        try:
            index=listbox.curselection()[0]
            # obtiene la linea de texto
            seltext=listbox.get(index)
            num=str1[index]
            titulo.set(num)
        except:
            print("No hay nada")


    # creamos el listbox y le damos el tamaño
    listbox=Listbox(inicio, width=18, height=6)
    listbox.grid(row=1, columnspan=2)
    listbox.config(bg="#545856",fg="white")

    # creamos el scrollbar del listbox
    scrollexplica=Scrollbar(inicio,command=listbox.yview)
    scrollexplica.grid(row=1,columnspan=7,sticky="ns")
    listbox.config(yscrollcommand=scrollexplica.set)


    # creamos un bucle para insertar los parametros de los datos uno por uno en la listbox
    for item in str1:
        listbox.insert(END, item)

    # al hacer click sobre un valor llamara a la funcion obtiene_valor
    listbox.bind('<ButtonRelease-1>', obtiene_valor)

    #------------------------------------------------ CREACION DEL MENÚ ----------------------------------------------------------------------------

    nombre=Label(inicio, text="Nombre de la tabla",bg="#3c3c3c",fg="white",font=("Arial", 9))
    nombre.grid(row=1,column=2,sticky="n")

    #creamos el titulo
    saludo1=botones("Seleccione la opción que desee ver",0,20,"",inicio)
    saludo1.saludo()

    #boton para añadir
    botcreate=botones("Añadir",2,0,add,inicio)
    botcreate.boton()

    #boton para borrar
    botborra=botones("Borrar",2,1,delete,inicio)
    botborra.boton()

    titul=Entry(inicio,textvariable=titulo)
    titul.config(bg="#545856",fg="white")
    titul.grid(row=1,column=2,sticky="w")

    #boton para Entrar
    botentrar=botones("Entrar",2,2,enter,inicio)
    botentrar.boton()

    #creamos el objeto para crear el label del creador
    botcreadopy=botones("creador",8,3,"",inicio)
    botcreadopy.creador()

#-----------------------------------------------------------------------------------------------------------------------------------------
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#----------------------------------------FRAME DE CONSULTAS-------------------------------------------------------------------------------


#creamos el menu de consultas
def consult(tabla):
    ver=Frame(root,bg="#3c3c3c")
    ver.pack()

    #----------------------------------------BOTON ATRAS------------------------------------------------------------------------------------

    #definimos la funcion para cuando el boton sea pulsado destruya el frame ver y llame a la funcion anterior
    def atras():
        ver.destroy()
        principal()

    #-----------------------------------------FUNCION DE BOTON CREAR --------------------------------------------------------------------------

    #definimos la funcion para cuando el boton crear sea pulsado suba los datos a la base de datos y deje los campos en blanco
    def botcrea():
        #obtenemos los valores que ha introducido el usuario y lo metemos en variables
        expl=textexplica.get("1.0", END)
        ejem=ejemplo.get("1.0", END)
        tit=titulo.get()


        #llamamos a la funcion pasandole los valores para subirlos a la base de datos, si no existe el nombre se creara y mostrara el mensaje
        #de creado, si falla porque ya existe dira que existe y saldra en rojo
        try:
            crea=bbdd(tabla,"",tit,expl,ejem)
            crea.create()

            bbddestado.set("CREADO CORRECTO")
            cuadroestado.config(fg='#98ed4d')

        except:
            bbddestado.set("EXISTE, NO CREADO")
            cuadroestado.config(fg='red')

        #llamamos a la funcion del menu desplegable para que lo actualice
        despliega()

        #borramos los campos dejandolos en blanco
        titulo.set("")
        textexplica.delete("1.0", END)
        ejemplo.delete("1.0", END)

    #---------------------------------------------FUNCION DE BOTON MODIFICAR ---------------------------------------------------------------------

    def botmodifica():
        #obtenemos los valores que ha introducido el usuario y lo metemos en variables
        expl=textexplica.get("1.0", END)
        ejem=ejemplo.get("1.0", END)
        tit=titulo.get()

        #llamamos a la funcion pasandole los valores para modificarlos en la base de datos, si falla saldra en rojo
        try:
            crea=bbdd(tabla,"",tit,expl,ejem)
            crea.update()

            bbddestado.set("MODIFICADO OK")
            cuadroestado.config(fg='#98ed4d')

        except:
            bbddestado.set("NO MODIFICADO")
            cuadroestado.config(fg='red')

        #borramos los campos dejandolos en blanco
        titulo.set("")
        textexplica.delete("1.0", END)
        ejemplo.delete("1.0", END)


    #-----------------------------------------------FUNCION DE BOTON BORRAR --------------------------------------------------------------

    #definimos la funcion para cuando el boton borrar sea pulsado, borre los datos a la base de datos y deje los campos en blanco
    def dell():
        #obtenemos los valores que ha introducido el usuario y lo metemos en variables
        tit=titulo.get()

        #creamos una condicion para que si el campo está en blanco no haga la consulta
        if tit=="":
            bbddestado.set("SELECCIONA VALOR")
            cuadroestado.config(fg='red')
        else:
            try:
                borra=bbdd(tabla,tit,"","","")
                borra.delete()

                bbddestado.set("BORRADO CORRECTO")
                cuadroestado.config(fg='#98ed4d')

            except:
                bbddestado.set("NO EXISTE EL VALOR")
                cuadroestado.config(fg='red')

        #llamamos a la funcion del menu desplegable para que lo actualice
        despliega()

        #borramos los campos dejandolos en blanco
        titulo.set("")
        textexplica.delete("1.0", END)
        ejemplo.delete("1.0", END)

    #---------------------------------------------VARIABLES PARA LOS ENTRY Y TEXT ----------------------------------------------------------

    #creamos las variables
    bbddestado=StringVar()
    titulo=StringVar()
    value=StringVar(root)

    #---------------------------------------------- CREACION DE LA BASE DE DATOS------------------------------------------------------------------------------

    #conectamos a la base de datos e introducimos el estado en la variable anterior
    try:
        conex=bbdd(tabla,"","","","")
        conex.conectar()

        estadobd="BBDD CREADA"
        color='#60eef7'
    except:
        estadobd="CONECTADO"
        color="#98ed4d"

    #------------------------------------------------- MENU DESPLEGABLE ---------------------------------------------------------------------------

    def despliega():
        #llamamos a la funcion para hacer la consulta SQL devolviendonos los titulos de los valores de la base de datos pasandole la vaiable tabla
        dato=bbdd(tabla,"","","","")
        datos=dato.titul()

        #Definimos el nombre por defecto del menu desplegable
        value.set("Opciones")

        #Creamos el combobox con OptionMenu y pasamos por parámetro el frame, la variable la cual utilizara para guardar los valores y la biblioteca
        popupMenu=OptionMenu(ver, value,*datos)

        #creamos el menu desplegable con OptionMenu indicandole la posicion
        popupMenu.grid(row=1,columnspan=2,sticky="w")
        popupMenu.config(background="#545856",foreground="white",activebackground="#85878c")

        # se crea una funcion para que obtenga el valor pulsado y lo introduca en una variable, acontinuacion mostramos en el label de titulo la opcion elegida
        def cambia_opcion(*args):
            #borramos los campos dejandolos en blanco
            titulo.set("")
            textexplica.delete("1.0", END)
            ejemplo.delete("1.0", END)

            #obtenemos el valor elegido en el menu desplegable
            opconsulta=value.get()
            titulo.set(opconsulta)

            try:
                #creamos el objeto para recuperar los datos de la base de datos seleccionado en el menu desplegable
                leer=bbdd(tabla,opconsulta,"","","")
                listadevuelta=leer.read()

                #insertamos los valores recuperados de la consulta
                textexplica.insert(INSERT, listadevuelta[1])
                ejemplo.insert(INSERT, listadevuelta[2])
            except:
                print("")

        # llama a la funcion anterior
        value.trace('w', cambia_opcion)


    despliega()

    #----------------------------------------------------------------------------------------------------------------------------

    #introduce el valor adecuado despues de conectar con al base de datos
    bbddestado.set(estadobd)

    #----------------------------------------- CREACION DE LOS WIDGET -----------------------------------------------------------------------------------

    #creamos el texto y el campo entry para el estado de la base de datos
    textoestado=Label(ver,text="Estado de BBDD")
    textoestado.config(bg="#3c3c3c",fg="white")
    textoestado.grid(row=0,column=3,padx=1,pady=10,sticky="e")

    cuadroestado=Entry(ver,textvariable=bbddestado,bg="black",fg=color)
    cuadroestado.grid(row=0,column=4,padx=1,pady=10)


    #creamos el texto y el entry para el titulo de la opcion elegida
    textotitulo=Label(ver,text="Título")
    textotitulo.config(bg="#3c3c3c",fg="white")
    textotitulo.grid(row=1,column=1,padx=1,pady=10,sticky="e")

    cuadrotitulo=Entry(ver,textvariable=titulo)
    cuadrotitulo.config(bg="#545856",fg="white")
    cuadrotitulo.grid(row=1,column=2,padx=1,pady=10)


    # creamos el text para mostrar la explicacion de la opcion elegida anteriormente
    textoexpl=Label(ver,text="Explicacion:")
    textoexpl.config(bg="#3c3c3c",fg="white")
    textoexpl.grid(row=2,column=0,padx=1,pady=5)


    textexplica=Text(ver,width=70,height=19, font=("Arial", 11))
    textexplica.grid(row=3,columnspan=5,padx=5,pady=5)
    textexplica.config(bg="#545856",fg="white")

    scrollexplica=Scrollbar(ver,command=textexplica.yview)
    scrollexplica.grid(row=3,column=5,sticky="nsew")

    textexplica.config(yscrollcommand=scrollexplica.set)


    # creamos el text para mostrar el ejemplo de la opcion elegida anteriormente
    textoejem=Label(ver,text="Anotaciones:")
    textoejem.config(bg="#3c3c3c",fg="white")
    textoejem.grid(row=4,column=0,padx=1,pady=5)

    ejemplo=Text(ver,width=70,height=5,bg="#e0db8c",fg="black", font=("Arial", 11))
    ejemplo.grid(row=5,columnspan=5,padx=5,pady=5)

    scrollejem=Scrollbar(ver,command=ejemplo.yview)
    scrollejem.grid(row=5,column=5,sticky="nsew")

    ejemplo.config(yscrollcommand=scrollejem.set)


    #------------------------------------------------ CREACION DE LOS BOTONES ----------------------------------------------------------------------------
    #boton para añadir
    botcreate=botones("Añadir",6,1,botcrea,ver)
    botcreate.atras()

    #boton para modificar
    botupdate=botones("Modificar",6,2,botmodifica,ver)
    botupdate.atras()

    #boton para Borrar
    botdelete=botones("Borrar",6,3,dell,ver)
    botdelete.atras()


    #boton para atras
    botbotatras=botones("Atras",7,4,atras,ver)
    botbotatras.atras()

    #creamos el objeto para crear el label del creador, el orden es el mismo que antes
    botcreadopy=botones("creador",8,3,"",ver)
    botcreadopy.creador()


def exit():
    exi=messagebox.askokcancel("Salir","¿Realmente desea salir de la aplicación?")

    if exi==True:
        root.destroy()

def acerca():
    messagebox.showinfo("Acerca de ...","Este programa sirve para tomar apuntes, está creado por Carlos Lorente")


#----------------------------------------------------------------------------------------------------------------------------
