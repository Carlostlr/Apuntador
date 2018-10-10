#importamos la libreria de tkinter
from tkinter import *
import sqlite3

#creamos la clase para crear los botones
class botones():

#los valores se pasan desde la creacion del objeto
    def __init__(self,nombre,row,column,valor,frame):
        self.nombre=nombre
        self.row=row
        self.column=column
        self.valor=valor
        self.frame=frame

#con esto creamos los botones cada uno con su posicion y ademas con la llamada a su funcion para cambiar de frame
    def boton(self):
        self.nombre=Button(self.frame, text=self.nombre,width=8, height=2,bg="#545856",fg="white",command=self.valor)
        self.nombre.grid(row=self.row,column=self.column,sticky="w",pady=30,padx=15)
        self.nombre.config(cursor="hand2")

#creamos el titulo de bienvenidos, con columnspan podemos unir celdas
    def saludo(self):
        self.nombre=Label(self.frame, text=self.nombre,bg="#3c3c3c",fg="white", font=(18))
        self.nombre.grid(row=self.row,columnspan=self.column,pady=25,padx=50)

#con esto creamos  el label con el nombre del autor abajo a la izquierda
    def creador(self):
        self.nombre=Label(self.frame,text="Creado por Carlos",bg="#3c3c3c",fg="white",font=("Comic sans MS", 8))
        self.nombre.grid(row=self.row,columnspan=self.column,sticky="w")


    def atras(self):
        self.nombre=Button(self.frame, text=self.nombre,width=9, height=2,bg="#545856",fg="white",command=self.valor)
        self.nombre.grid(row=self.row,column=self.column,sticky="w",pady=10,padx=20)
        self.nombre.config(cursor="hand2")

    def agrandar(self):
        foto=PhotoImage(file='grande.png')
        boton=Button(self.frame,image=foto)
        boton.grid(row=self.row,column=self.column)


#creamos la clase para manipular la base de datos
class bbdd():

#los valores se pasan desde la creacion del objeto
    def __init__(self,tabla,nombre,valor1,valor2,valor3):
        self.tabla=tabla
        self.nombre=nombre
        self.valor1=valor1
        self.valor2=valor2
        self.valor3=valor3

    def conectar(self):
        # creamos la base de datos con el cursor
        miconexion=sqlite3.connect("apuntes")
        micursor=miconexion.cursor()

        # creamos la consulta que creara las tablas
        #micursor.execute("CREATE TABLE "+tabla+" (NOMBRE VARCHAR(10) UNIQUE,EXPLICACION VARCHAR(2000),EJEMPLO VARCHAR(2000))")
        micursor.execute("CREATE TABLE "+self.tabla+" (NOMBRE VARCHAR(10) UNIQUE,EXPLICACION VARCHAR(2000),EJEMPLO VARCHAR(2000))")

        datos=[('Bienvenido','Aquí puedes escibir tus apuntes','Aquí puedes escibir tus ejemplos')]

        micursor.executemany("INSERT INTO "+self.tabla+" VALUES(?,?,?)",datos)
        miconexion.commit()

        miconexion.close()


    def create(self):
        # creamos la base de datos con el cursor
        miconexion=sqlite3.connect("apuntes")
        micursor=miconexion.cursor()

        datos=[(self.valor1,self.valor2,self.valor3)]

        micursor.executemany("INSERT INTO "+self.tabla+" VALUES(?,?,?)",datos)

        miconexion.commit()

        miconexion.close()


    def titul(self):
        miconexion=sqlite3.connect("apuntes")

        micursor=miconexion.cursor()

        micursor.execute("SELECT NOMBRE FROM "+self.tabla)

        datos=micursor.fetchall()

        #creamos un bucle porque la consulta se devuelve en una lista con tuplas, creamos la lista y vamos añadiendo con append los elementos que estan en la
        # posicion 0 de las tuplas dentro de la lista
        valores=[]
        for i in datos:
            valores.append(i[0])

        return valores

        miconexion.commit()

        miconexion.close()

    def read(self):

        miconexion=sqlite3.connect("apuntes")

        micursor=miconexion.cursor()

        micursor.execute("SELECT * FROM "+self.tabla+" WHERE NOMBRE='"+self.nombre+"'")

        datos=micursor.fetchall()

        #creamos un bucle porque la consulta se devuelve en una lista con tuplas, creamos la lista y vamos añadiendo con append los elementos que estan en la
        # posicion 0 de las tuplas dentro de la lista
        valores=[]
        for i in datos:
            valores.append(i[0])
            valores.append(i[1])
            valores.append(i[2])
        return valores

        miconexion.commit()

        miconexion.close()

    def update(self):
        # creamos la base de datos con el cursor
        miconexion=sqlite3.connect("apuntes")
        micursor=miconexion.cursor()

        micursor.execute("UPDATE "+ self.tabla + " SET NOMBRE='"+self.valor1+"', EXPLICACION='"+self.valor2+"', EJEMPLO='"+self.valor3+"' WHERE NOMBRE='"+ self.valor1+"'")

        miconexion.commit()

        miconexion.close()


    def delete(self):

        miconexion=sqlite3.connect("apuntes")

        micursor=miconexion.cursor()

        micursor.execute("DELETE FROM "+self.tabla+" WHERE NOMBRE='"+self.nombre+"'")

        miconexion.commit()

        miconexion.close()

    def delete_table(self):

        miconexion=sqlite3.connect("apuntes")

        micursor=miconexion.cursor()

        micursor.execute("DROP TABLE "+self.tabla)

        miconexion.commit()

        miconexion.close()
