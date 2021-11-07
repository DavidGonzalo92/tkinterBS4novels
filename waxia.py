


import requests
import os
from bs4 import BeautifulSoup
import codecs
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium.webdriver.chrome.service import Service
import warnings
import json
from pathlib import Path
from tkinter import ttk  
from tkinter import * 
import sqlite3
import subprocess


#we connect to chrome or firefox(chromedriver or geckodriver)
driver = webdriver.Chrome('C:\\Users\\david\\chromedriver.exe')
driver.set_window_position(0, 0)
driver.set_window_size(10, 10)

# we obtain the content of the page in this case genre of the novel
def genero():
    browser=driver.get('https://readnovelfull.com/')
    content = driver.page_source
    soup = BeautifulSoup(content)
    generol=[]
    for a in soup.findAll("div", class_="col-xs-6"):
        añadir=a.text
        generol.append(añadir)
    return generol
  
# we obtain the content of the page in this case the novels by genre    
def novelas(genero):
    i=1
    unique = []
    while i<=7:
        if i==1:
            browser=driver.get("https://readnovelfull.com/genre/"+ genero.replace(" ", "+"))
            content = driver.page_source
            soup = BeautifulSoup(content)
            lista=[]
            for a in soup.findAll("h3", class_="novel-title"):
                añadir=a.text
                lista.append(añadir)
        #'Else' its cause you change the url when you move to other page 
        else:
            browser=driver.get("https://readnovelfull.com/genre/"+ genero.replace(" ", "+")+'?page='+str(i))
            content = driver.page_source
            soup = BeautifulSoup(content)
            for a in soup.findAll("h3", class_="novel-title"):
                añadir=a.text
                lista.append(añadir)
        i+=1
    lista1=[unique.append(x) for x in lista if x not in unique]#lambda function unique novels
    lista=unique
    return lista


# we need this function beacuse when you select in tkinter, the program should know where it is
def seleccionar():
    global lista_novela,numero_inicio
    numero_inicio=0  # restart  when you change novel
    lista_novela.clear()
    capitulos(listaop[opcion.get()])
    return
    


# we obtain the list of novel that we select in the menu
def capitulos(novela):
    
    global lista_novela,numero_inicio
    print(novela)
    warnings.filterwarnings("ignore")
    novela=novela.replace("'s","s")
    novela=novela.replace(": ","-")
    novela=novela.replace(" ","-")
    novela="https://readnovelfull.com/"+ novela +'.html#tab-chapters-title'       
    driver.get(novela)
    elem = driver.find_element_by_css_selector('#tab-chapters')
    html = driver.execute_script("return arguments[0].innerHTML;", elem)
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.findAll('a'):
      lista_novela.append(a['href'])
    print(lista_novela[0])
    escribir_novela(lista_novela[0])

    return lista_novela

# we obtain the text of the novel
def escribir_novela(urlpagina):
    T.delete('1.0', END)
    browser=driver.get("https://readnovelfull.com"+urlpagina)
    content = driver.page_source
    soup = BeautifulSoup(content)
    for a in  soup.findAll("div", class_="chr-c"):
        T.insert(END,a.text) 
   

# we obtain the url of the next chapter
def capitulos_siguiente():
    global numero_inicio
    numero_inicio+=1
    T.delete('1.0', END)
    urlpagina=lista_novela[numero_inicio]
    browser=driver.get("https://readnovelfull.com"+urlpagina)
    content = driver.page_source
    soup = BeautifulSoup(content)
    for a in  soup.findAll("div", class_="chr-c"):
        T.insert(END,a.text)
    return numero_inicio


# we obtain the url of the previous chapter
def capitulos_anterior():
    global numero_inicio
    numero_inicio-=1
    T.delete('1.0', END)
    urlpagina=lista_novela[numero_inicio]
    browser=driver.get("https://readnovelfull.com"+urlpagina)
    content = driver.page_source
    soup = BeautifulSoup(content)
    for a in  soup.findAll("div", class_="chr-c"):
        T.insert(END,a.text)
    return  numero_inicio   


# we obtain the url of the  chapter  that we choose
def elegir_capitulo():
        def show_entry_fields():
            global numero_inicio
            numero_inicio=int(e1.get())-1
            T.delete('1.0', END)
            urlpagina=lista_novela[numero_inicio]
            browser=driver.get("https://readnovelfull.com"+urlpagina)
            content = driver.page_source
            soup = BeautifulSoup(content)
            for a in  soup.findAll("div", class_="chr-c"):
                T.insert(END,a.text)
            return  

        master =Tk()
        Label(master, 
                text="capitulo").grid(row=0)
        

        e1 =Entry(master)
        e1.grid(row=0, column=1)
        Button(master, text='acepta', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=4)   

# if we press this, it will send you to the page
def traducir_novela():  
    

    subprocess.Popen("start chrome /new-tab https://dictionary.cambridge.org/dictionary/english", shell=True)
    

    

    
 
    
   
    
#tkinter  

root = Tk()
opcion = IntVar()
root.title("novelas")
  
generol=genero()
lista_novela=[]
numero_inicio=0
# Superior menu

top = Menu(root)
edit=Menu(top, tearoff=0)
top.add_cascade(label='genero',menu=edit, underline=0)
i=0
listaop=[]

'''

submenu = Menu(edit, tearoff=0)
lista=novelas('sci-fi')
for a in lista:
    listaop.append(a)
    submenu.add_radiobutton(label=a,variable=opcion,value=i,command=seleccionar)
    i+=1
edit.add_cascade(label='sci-fi', menu=submenu, underline=0)
'''
for b in generol:
    submenu = Menu(edit, tearoff=0)
    lista=novelas(b)
    for a in lista:
        listaop.append(a)
        submenu.add_radiobutton(label=a,variable=opcion,value=i,command=seleccionar)
        i+=1
    edit.add_cascade(label=b, menu=submenu, underline=0)

# Central text box
texto = Text(root)
root.config(menu=top)


S = Scrollbar(root)
T = Text(root, height=40, width=80)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
T.grid(column=0, row=0)
S.grid(column=1, row=0, sticky='NS')


#buttons

boton_eliminar =Button(text = 'traducir', command =traducir_novela)
boton_eliminar.grid(row = 31, column = 0, sticky = 'S')
boton_eliminar =Button(text = 'siguiente', command =capitulos_siguiente)
boton_eliminar.grid(row = 30, column = 0, sticky = 'SE')
boton_editar = Button(text='elegir_Capitulo',command =elegir_capitulo)
boton_editar.grid(row = 30, column = 0, sticky ='S')
boton_editar = Button(text='anterior',command = capitulos_anterior)
boton_editar.grid(row = 30, column = 0, sticky = 'SW')



# Finally loop the app
root.mainloop()

