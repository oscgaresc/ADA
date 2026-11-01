import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import tkinter.filedialog as tfd
import tkinter.messagebox as tmb
import xml.etree.ElementTree as ET  # librería para XML
from bs4 import BeautifulSoup       # librería para HTML
import csv                          # librería para CSV
import io                           # io.StringIO(texto) para CSV -> OBJ permite tratar el texto como archivo
import json                         # librería para JSON
import pickle                       # librería para pickle

from functools import partial       # para poder pasar parámetros a las funciones de callback
from dataclasses import dataclass   # almacenamiento de datos en objetos Python


# clase para guardar los datos
@dataclass
class Producto():
    genero: str
    titulo: str
    autor: str
    precio: float
    disponible: bool

    def __post_init__(self):
        self.genero = self.genero.strip()
        self.titulo = self.titulo.strip()
        self.autor = self.autor.strip()
        self.precio = float(self.precio)


#
# DEFINICIÓN DE FUNCIONES
#
def seleccionar_fichero(editor):
    '''Diálogo para seleccionar un fichero y mostrarlo en el editor
    Args:
        editor(ScrolledText): zona para visualizar/editar datos
    '''
    dlg_selec = tfd.askopenfilename(
        title='Seleccionar un fichero',
        initialdir='/',
        filetypes= (('Fichero de texto', '*.txt'),
                    ('Todos los ficheros', '*.*')))
    
    # leemos todo el fichero
    with open(dlg_selec, 'r') as fr:
        contenido = fr.read()
    
    # guardamos en el editor
    editor.delete(1.0,'end')
    editor.insert('1.0', contenido)
    
    
def guardar_fichero(editor):
    '''Diálogo para guardar el contenido del editor en un fichero
    Args:
        editor(ScrolledText): zona para visualizar/editar datos
    ''' 
    dlg_save = tfd.asksaveasfilename(
        title="Guardar un fichero", defaultextension=".txt")
    
    # escribimos el fichero con el contenido del editor
    with open(dlg_save, 'w') as fw:        
        fw.write(editor.get('1.0','end'))
    
def extraer_producto_de_xml(producto_xml):
    genero = producto_xml.attrib['genero']
    titulo = producto_xml.find('titulo').text
    autor = producto_xml.find('autor').text
    precio = producto_xml.find('precio').text
    disponible = producto_xml.find('disponible').text
    disponible = True if disponible == 'si' else False
    return Producto(genero, titulo, autor, precio, disponible)


def xml_a_objetos(editor):
    '''Parsea el texto XML y lo convierte en objetos Producto.
    Args:
        editor(ScrolledText): zona para visualizar/editar datos
    '''
    try:
        productos = []
        str_xml_editor = editor.get('1.0', 'end')

        if str_xml_editor =='\n':
            raise Exception('No hay libros o se ha cargado un xml no compatible.')
        
        xml = ET.fromstring(str_xml_editor)
        productos_xml = xml.findall('libro') # retorna una lista de productos
        for producto_xml in productos_xml:
            productos.append(extraer_producto_de_xml(producto_xml))
        if not productos:
            raise Exception("No hay libros o se ha cargado un xml no compatible.")

    except SyntaxError:
        tmb.showerror("Error", "Parece que la sintaxis no es XML.")

    except Exception as e:
        tmb.showerror("Error", f'{e}')
    else:
        # mostramos en el editor
        editor.delete('1.0','end')
        texto_a_insertar = ''
        for producto in productos:
            texto_a_insertar += str(producto) + '\n'
        editor.insert(f'1.0',texto_a_insertar)


def objetos_a_xml(editor):
    '''genera un texto xml a partir de los objetos (en texto) que hay en el editor
    Args:
        editor(ScrolledText): zona para editar/visualizar datos
    '''
    try:
        # creamos el elemento raíz
        raiz_xml = ET.Element('libreria')

        # leemos los objetos del editor
        texto_objetos = editor.get('1.0','end')
        lista_objetos = texto_objetos.split(sep='\n')

        # quito basura 
        while True:
            try:
                lista_objetos.remove('')
            except ValueError:
                break
    
        if not lista_objetos:
            raise Exception("No hay objetos.")
        
    except Exception as e:
        tmb.showerror("Error", f'{e}')

    else:
        # creamos elementos libro
        for libro in lista_objetos:
            try:
                objeto_producto = eval(libro)
            except Exception as e:
                tmb.showerror("Error", f'{e}')
            else:
                libro_xml = ET.Element('libro', attrib=dict(genero=objeto_producto.genero))
                # creamos subelementos libro y los enganchamos
                titulo_xml = ET.Element('titulo')
                titulo_xml.text = objeto_producto.titulo
                autor_xml = ET.Element('autor')
                autor_xml.text = objeto_producto.autor
                precio_xml = ET.Element('precio')
                precio_xml.text = str(objeto_producto.precio)
                disponible_xml = ET.Element('disponible')
                disponible_xml.text = "si" if objeto_producto.disponible else "no"

                libro_xml.extend([titulo_xml, autor_xml, precio_xml, disponible_xml])

                # enganchamos el libro a la raiz
                raiz_xml.append(libro_xml)

        # generamos la cadena con la raiz
        ET.indent(raiz_xml, space="\t", level=0) # prettify
        str_xml = ET.tostring(raiz_xml, encoding="unicode", xml_declaration=True)

        # mostramos en el editor
        editor.delete(1.0,'end')
        editor.insert('1.0', str_xml)    


def html_a_objetos(editor):
    '''Parsea un texto html del editor a objetos
    Args:
        editor(ScrolledText): zona para editar/visualizar datos
    '''
    pass


def objetos_a_html(editor):
    '''genera un texto html a partir de los objetos (en texto) que hay en el editor
    Args:
        editor(ScrolledText): zona para editar/visualizar datos
    '''
    pass


def csv_a_objetos(editor):
    '''Parsea un texto csv del editor a objetos
    Args:
        editor(ScrolledText): zona para editar/visualizar datos
    '''
    pass


def objetos_a_csv(editor):
    '''genera un texto csv a partir de los objetos (en texto) que hay en el editor
    Args:
        editor(ScrolledText): zona para editar/visualizar datos
    '''
    pass


def como_productos(dct):
    '''Retorna un objeto Producto a partir de un diccionario
    Args:
        dct(dict): diccionario con la información necesaria para crear un objeto Producto
    '''
    return Producto(dct['genero'], dct['titulo'], dct['autor'], dct['precio'], dct['disponible'])

class ProductoEncoder(json.JSONEncoder):
    '''Si el objeto es de tipo Producto lo pasa a dict para que json.JSONEncoder pueda codificarlo.
    En otro caso, json.JOSNEncoder lo codifica directamente
    '''
    def default(self, o):
        if isinstance(o, Producto):
            return dict(genero=o.genero, titulo=o.titulo, autor=o.autor, precio=float(o.precio), disponible=o.disponible)
        return json.JSONEncoder.default(self, o)


def json_a_objetos(editor):
    '''Parsea un texto json del editor a objetos
    Args:
        editor(ScrolledText): zona para editar/visualizar datos
    '''
    pass


def objetos_a_json(editor):
    '''genera un texto json a partir de los objetos (en texto) que hay en el editor
    Args:
        editor(ScrolledText): zona para editar/visualizar datos
    '''
    pass

# VARIABLE GLOBAL
lista_objetos_pickle = []

def pickle_a_objetos(editor):
    '''deserializa los objetos pickle del editor a objetos Python (muestra el resultado en el editor).
    En la variable global lista_objetos_pickle está el resultado de la serialización anterior.

    Args:
        editor(ScrolledText): zona para editar/visualizar datos
    '''
    pass

def objetos_a_pickle(editor):
    '''serializa los objetos del editor a pickle (muestra el resultado en el editor)
    Al mismo tiempo se guarda una variable global lista_objetos_pickle con todas las serializaciones.
    Esto es porque pickle solo serializa un objeto cada vez
    Args:
        editor(ScrolledText): zona para editar/visualizar datos
    '''
    pass

#
# INTERFAZ GRÁFICA
#

# Configuración de la raíz
root = tk.Tk()
root.geometry("800x600+50+50")
root.title('Files')

# Marco para el texto
marco_texto = tk.Frame(root, height='400')
marco_texto.config(background='white')
marco_texto['borderwidth'] = 5  #Ancho del borde
marco_texto['relief'] = 'sunken' #Relieve, otros: flat, groove, raised, ridge, sunken.
marco_texto.pack(fill='x')

etiqueta_texto = ttk.Label(marco_texto, text="VISOR/EDITOR DE CONTENIDO")
etiqueta_texto.config(background='white')
etiqueta_texto.pack()

# Text + scroll
texto = ScrolledText(marco_texto)
texto.config(state='normal')
texto.pack(fill='both')

# Marco para la botonera
marco_botones = tk.Frame(root, height='150')
marco_botones.config(background='white')
marco_botones['borderwidth'] = 5
marco_botones['relief'] = 'sunken'
marco_botones.pack(fill='x',side='bottom')

# botones
boton_xml_objetos = ttk.Button(marco_botones, text="xml->obj", command=partial(xml_a_objetos, texto))
boton_xml_objetos.config(padding=10, width=15)
boton_xml_objetos.grid(row=0, column=0, padx=5, pady=5)

# Aquí van los botones que faltan de la fila 0

boton_objetos_xml = ttk.Button(marco_botones, text="obj->xml", command=partial(objetos_a_xml, texto))
boton_objetos_xml.config(padding=10, width=15)
boton_objetos_xml.grid(row=1, column=0, padx=5, pady=5)

# Aquí van los botones que faltan de la fila 1

# Creamos el menú principal
menubar = tk.Menu(root)   #Creamos el objeto Menu
root.config(menu=menubar) #Indicamos que es el menú principal

# Creamos los submenús
archivo_menu = tk.Menu(menubar, tearoff=False)

# Añadimos opciones al submenú "Archivo"
# cada opción tendrá una función o método que ejecutará
archivo_menu.add_command(label="Abrir", command=partial(seleccionar_fichero, texto)) # label es el texto que mostrará
archivo_menu.add_command(label="Guardar", command=partial(guardar_fichero, texto))
archivo_menu.add_separator() # línea separadora
archivo_menu.add_command(label="Salir", command=root.destroy) # command es el comando que se ejecutará

# Asignamos los submenús al menú principal
menubar.add_cascade(label="Archivo", menu=archivo_menu) # label es el texto que se mostrará

# Bucle de la aplicación
root.mainloop()
