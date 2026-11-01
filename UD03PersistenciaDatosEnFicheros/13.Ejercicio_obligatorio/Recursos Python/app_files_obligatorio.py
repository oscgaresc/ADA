# --------------------------------------------------------------------    
try:
    import Tkinter as tk  #  Es lo que indica el documento, parece ser algo antiguo
    from Tkinter import ttk #  Es lo que indica el documento
except ImportError:
    import tkinter as tk
    from tkinter import ttk
# --------------------------------------------------------------------    
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


@dataclass
class Producto():
    '''clase para guardar los datos de unos productos libro
    '''
    genero: str
    titulo: str
    autor: str
    precio: float
    disponible: bool

    def __post_init__(self):
        self.genero = self.genero.strip() # elimina los espacios laterales
        self.titulo = self.titulo.strip() # elimina los espacios laterales
        self.autor = self.autor.strip() # elimina los espacios laterales
        self.precio = float(self.precio) # pasa de str a float
        # ¿?¿? No hace falta pasar disponible a bool ya que lo hacen las funciones
        # self.disponible = bool(self.disponible) # para que tenga todos los atributos



#
# DEFINICIÓN DE FUNCIONES
#
def seleccionar_fichero(editor):
    '''Diálogo para seleccionar un fichero y mostrarlo en el editor
    Args:
        editor(ScrolledText): zona para visualizar/editar datos
    '''
    dlg_selec = tfd.askopenfilename( # ventana para localizar ficheros
        title='Seleccionar un fichero',
        initialdir='/', # se podría añadir la carpeta ficheros de muestra
        filetypes= (('Todos los ficheros', '*.*'), # lo añado primero para que aparezcan todos por defecto
                    ('Fichero de texto', '*.txt'),
                    ('Fichero de xml', '*.xml'),
                    ('Fichero de html', '*.html'),
                    ('Fichero de csv', '*.csv'),
                    ('Fichero de json', '*.json')))
    
    # leemos todo el fichero y se añade encoding='utf-8' al utilizar windows
    with open(dlg_selec, 'r', encoding='utf-8') as fr:
        contenido = fr.read()
    
    # guardamos en el editor
    editor.delete(1.0,'end')
    editor.insert('1.0', contenido)
    
    
def guardar_fichero(editor):
    '''Diálogo para guardar el contenido del editor en un fichero
    Args:
        editor(ScrolledText): zona para visualizar/editar datos
    ''' 
    dlg_save = tfd.asksaveasfilename( # ventana para guardar ficheros
        title="Guardar un fichero", defaultextension=".txt")
    
    # escribimos el fichero con el contenido del editor y se añade
    # encoding='utf-8' al utilizar windows
    with open(dlg_save, 'w', encoding='utf-8') as fw:        
        fw.write(editor.get('1.0','end'))
    
def extraer_producto_de_xml(producto_xml):
    '''Extrae la información del xml de cada producto libro y lo transforma en un objeto Producto
    Args:
        producto_xml(List): lista con el contenido xml de cada producto libro
    
    Returns:
        Out(Producto): Objeto Producto que almacena la información del producto
    ''' 
    genero = producto_xml.attrib['genero']
    titulo = producto_xml.find('titulo').text
    autor = producto_xml.find('autor').text
    precio = producto_xml.find('precio').text
    disponible = producto_xml.find('disponible').text
    disponible = True if disponible == 'si' else False
    return Producto(genero, titulo, autor, precio, disponible)

def extraer_producto_de_html(producto_html):
    '''Extrae la información del html de cada producto libro y lo transforma en un objeto Producto
    Args:
        producto_html(List): lista con el contenido html de cada producto libro
    
    Returns:
        Out(Producto): Objeto Producto que almacena la información del producto
    ''' 
    genero = producto_html.find('h2').text.strip()
    titulo = producto_html.find('div', class_='titulo').text.strip()
    autor = producto_html.find('div', class_='autor').text.strip()
    precio = producto_html.find('div', class_='precio').text.strip()
    disponible = producto_html.find('div', class_='disponible').text.strip()
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
        
        xml = ET.fromstring(str_xml_editor) # es estricto, en caso de no ser un documento xml
        productos_xml = xml.findall('libro') # retorna una lista de productos
        for producto_xml in productos_xml:
            productos.append(extraer_producto_de_xml(producto_xml))
        if not productos:
            raise Exception("No hay libros o se ha cargado un xml no compatible.")

    except SyntaxError:
        tmb.showerror("Error", "Parece que la sintaxis no es XML.") # muestra ventana emergente de error 
    except Exception as e:
        tmb.showerror("Error", f'{e}')
    else:
        # mostramos en el editor
        editor.delete('1.0','end')
        # texto_a_insertar = ''
        # for producto in productos:
        #     texto_a_insertar += str(producto) + '\n'
        # join es más eficiente que += => "separador".join(COLECCIÓN_DE_ELEMENTOS)
        texto_a_insertar = "\n".join(str(producto) for producto in productos)

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
        # no se si se considera un error que intente coger cualquier objeto y transformarlo

    else:
        # creamos elementos libro
        for libro in lista_objetos:
            try:
                objeto_producto = eval(libro) 
                # eval(), evalúa cualquier tipo de dato, por lo que es conveniente comprobar si
                # el tipo de dato es de tipo Producto de la siguiente manera:
                if not isinstance(objeto_producto, Producto):
                    raise ValueError(f'El elemento {libro} no es un objeto Producto válido.')
                
            except Exception as e:
                tmb.showerror("Error", f'Línea inválida, no representa un objeto Producto'+
                              f' válido:\n{libro}\n\n{e}')
                return # se cierra la función sin que realice cambios para mejorar la ux
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
    try:
        # paso 1: Se obtiene texto del editor.
        productos=[]
        str_html_editor = editor.get('1.0', 'end')

        if str_html_editor =='\n':
            raise Exception('No hay libros o se ha cargado un html no compatible.')
        # Antes de pasar al siguiente bloque, con BeautifulSoup, es conveniente comprobar
        # si el html tiene un formato similar, es decir, "<" o ">".
        if '<' not in str_html_editor or '>' not in str_html_editor: 
            raise Exception('Parece que la sintaxis no es HTML.')
        
        # paso 2: Se obtiene objeto html con BeautifulSoup con la librería lxml que es más rápida
        html = BeautifulSoup(str_html_editor,'lxml')

        # paso 3: Se obtiene una lista de divs de clase libro (list[str])
        productos_divs_html = html.find_all('div', class_ = 'libro')
        # se obtiene una lista de strings -> (list[str]) llamada productos
        # Se utiliza .text.strip() para poder visualizar la estructura sin etiquetas
        # si lo quito me aparece las etiquetas pero se complica al utilizar los datos
        # para pasar de objeto a html en la siguiente función.
        # paso 4. Se procesa cada uno de los divs y se obtiene una lista de Productos        
        for producto_html in productos_divs_html:
            productos.append(extraer_producto_de_html(producto_html))
        
        if not productos:
            raise Exception("No hay libros o se ha cargado un html no compatible.")        

    except SyntaxError:
        tmb.showerror("Error", "Parece que la sintaxis no es HTML.")
        # No se añade el icono "warning", aunque se puede probar 
    except Exception as e:
        tmb.showerror("Error", f'{e}')
    else:
        # paso 5. Se muestra en el editor los objetos Producto obtenidos.
        # se muestra en el editor
        editor.delete('1.0','end')
        
        # "separador".join(COLECCIÓN_DE_ELEMENTOS) -> 2 opciones
        texto_a_insertar = "\n".join(str(producto) for producto in productos)

        # se añade a la interfaz tkinter            
        editor.insert(f'1.0',texto_a_insertar)


def objetos_a_html(editor):
    '''genera un texto html a partir de los objetos (en texto) que hay en el editor
    Args:
        editor(ScrolledText): zona para editar/visualizar datos
    '''
    try:
        # paso 1. Se obtiene el texto del editor
        texto_objetos = editor.get('1.0','end-1c') # 1c para evitar el \n final
        # de Tkinter, que da problemas

        # paso 2. Se obtiene una lista de texto_objetos separando por \n
        lista_objetos = texto_objetos.split(sep='\n')

        # paso 3. Se quita basura ('')
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
        # paso 4. Se crea el documento HTML con beautifulsoup
        soup = BeautifulSoup('<html><head></head><body></body><footer>'\
                             '</footer></html>', 'html.parser')
        title = soup.new_tag('title')
        title.string = 'Libros de la librería'
        soup.head.append(title)
        # los css con style
        style = soup.new_tag('style')
        style.string = '''body {text-align: center;}
        h1 {color: grey;}
        h2 {color: navy;}
        .precio {font-weight: bold}
        footer {background: gray; color: white; margin: 20px;padding: 20px;}
        '''
        soup.head.append(style)
        h1 =soup.new_tag('h1')
        h1.string = 'librería'
        soup.body.append(h1)
        #---------------------------------------------------------------------
        #                  AÑADIENDO LOS OBJETOS A HTML
        #---------------------------------------------------------------------
        # Se añaden los objetos del editor y se transforma a html y se crea
        # elementos libro
        for libro in lista_objetos:
            # Limpiando espacios en blanco para evitar errores
            libro = libro.strip()
            try:
                objeto_producto = eval(libro) # se obtiene el objeto producto
                # eval(), evalúa cualquier tipo de dato, por lo que es conveniente comprobar si
                # el tipo de dato es de tipo Producto de la siguiente manera:
                if not isinstance(objeto_producto, Producto):
                    raise ValueError(f'El elemento {libro} no es un objeto Producto válido.')
                
            except Exception as e:
                tmb.showerror("Error", f'Línea inválida, no representa un objeto Producto'+
                                f' válido:\n{libro}\n\n{e}')
                return # se cierra la función sin que realice cambios para mejorar la ux
            else:
                div_libro =soup.new_tag('div', attrs={'class':'libro'})
                h2_genero =soup.new_tag('h2')
                h2_genero.string = str(objeto_producto.genero)
                div_libro.append(h2_genero)
                div_titulo =soup.new_tag('div', attrs={'class':'titulo'})
                div_titulo.string = str(objeto_producto.titulo)
                div_libro.append(div_titulo)
                div_autor =soup.new_tag('div', attrs={'class':'autor'})
                div_autor.string = str(objeto_producto.autor)
                div_libro.append(div_autor)
                div_precio =soup.new_tag('div', attrs={'class':'precio'})
                div_precio.string = str(objeto_producto.precio)
                div_libro.append(div_precio)
                div_disponible =soup.new_tag('div', attrs={'class':'disponible'})
                div_disponible.string = 'si' if objeto_producto.disponible else 'no' 
                div_libro.append(div_disponible)
        
                soup.body.append(div_libro)
                #---------------------------------------------------------------------
            
        soup.footer.string='Me gusta Python'        

        # Se configura la identación con el metodo prettyfy()
        texto_html = soup.prettify()

        # paso 6. Se muestra en el editor
        editor.delete(1.0,'end')
        editor.insert('1.0', texto_html)  


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
    return Producto(dct['genero'], dct['titulo'], dct['autor'],
                    dct['precio'], dct['disponible'])

class ProductoEncoder(json.JSONEncoder):
    '''Si el objeto es de tipo Producto lo pasa a dict para que json.JSONEncoder pueda codificarlo.
    En otro caso, json.JOSNEncoder lo codifica directamente
    '''
    def default(self, o):
        if isinstance(o, Producto):
            return dict(genero=o.genero, titulo=o.titulo, autor=o.autor,
                         precio=float(o.precio), disponible=o.disponible)
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

def pickle_a_objetos(editor): # VUELTA: Se debe ejecutar con el pickle en el editor
    '''deserializa los objetos pickle del editor a objetos Python (muestra el resultado en el editor).
    En la variable global lista_objetos_pickle está el resultado de la serialización anterior.

    Args:
        editor(ScrolledText): zona para editar/visualizar datos
    '''
    pass

def objetos_a_pickle(editor): # IDA: Se debe ejecutar con los productos en el editor
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

# Configuración de la raíz (root)
root = tk.Tk()
root.geometry("800x600+50+50") # ancho x alto + x + y
root.title('Files')

# Marco para el texto
marco_texto = tk.Frame(root, height='400')
marco_texto.config(background='white')
marco_texto['borderwidth'] = 5  #Ancho del borde
marco_texto['relief'] = 'sunken' #Relieve, otros: flat, groove, raised, ridge, sunken.
marco_texto.pack(fill='x')

etiqueta_texto = ttk.Label(marco_texto, text="VISOR/EDITOR DE CONTENIDO",
                           font= ("Verdana", 10),
                           foreground = "white",
                           background = "grey")
# etiqueta_texto.config(background='white')
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

# Botones que faltan de la fila 0
# botón xml -> obj
boton_xml_objetos = ttk.Button(marco_botones, text="xml->obj", command=partial(xml_a_objetos, texto))
boton_xml_objetos.config(padding=10, width=20)
boton_xml_objetos.grid(row=0, column=0, padx=5, pady=5)

# botón html -> obj
boton_html_objetos = ttk.Button(marco_botones, text="html->obj", command=partial(html_a_objetos, texto))
boton_html_objetos.config(padding=10, width=20)
boton_html_objetos.grid(row=0, column=1, padx=5, pady=5)

# botón csv -> obj
boton_csv_objetos = ttk.Button(marco_botones, text="csv->obj", command=partial(csv_a_objetos, texto))
boton_csv_objetos.config(padding=10, width=20)
boton_csv_objetos.grid(row=0, column=2, padx=5, pady=5)

# botón json -> obj
boton_json_objetos = ttk.Button(marco_botones, text="json->obj", command=partial(json_a_objetos, texto))
boton_json_objetos.config(padding=10, width=20)
boton_json_objetos.grid(row=0, column=3, padx=5, pady=5)

# botón pickle -> obj
boton_pickle_objetos = ttk.Button(marco_botones, text="pickle->obj", command=partial(pickle_a_objetos, texto))
boton_pickle_objetos.config(padding=10, width=20)
boton_pickle_objetos.grid(row=0, column=4, padx=5, pady=5)

# Bbotones que faltan de la fila 1
# botón xml -> obj
boton_objetos_xml = ttk.Button(marco_botones, text="obj->xml", command=partial(objetos_a_xml, texto))
boton_objetos_xml.config(padding=10, width=20)
boton_objetos_xml.grid(row=1, column=0, padx=5, pady=5)

# botón obj -> html
boton_objetos_html = ttk.Button(marco_botones, text="obj->html", command=partial(objetos_a_html, texto))
boton_objetos_html.config(padding=10, width=20)
boton_objetos_html.grid(row=1, column=1, padx=5, pady=5)

# botón obj -> csv
boton_objetos_csv = ttk.Button(marco_botones, text="obj->csv", command=partial(objetos_a_csv, texto))
boton_objetos_csv.config(padding=10, width=20)
boton_objetos_csv.grid(row=1, column=2, padx=5, pady=5)
# botón obj -> json
boton_objetos_json = ttk.Button(marco_botones, text="obj->json", command=partial(objetos_a_json, texto))
boton_objetos_json.config(padding=10, width=20)
boton_objetos_json.grid(row=1, column=3, padx=5, pady=5)

# botón obj -> pickle
boton_objetos_pickle = ttk.Button(marco_botones, text="obj->pickle", command=partial(objetos_a_pickle, texto))
boton_objetos_pickle.config(padding=10, width=20)
boton_objetos_pickle.grid(row=1, column=4, padx=5, pady=5)

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
