# Genera informe.docx con las tres partes del Lab III. Lee el código y las salidas reales.
import subprocess
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt, RGBColor

HERE = Path(__file__).parent
GRAF = HERE / "graficas"
SAL = HERE / "salidas"
TITLE = "Lab III: Dispositivos y planificación de disco"
AUTHORS = "Nicolás Carreño Tascón, David Leandro Cruz, Ricardo Perez"
URL = "https://github.com/nx01-600/sisope-lab3"
SUBJ = "Sistemas Operativos, Ingeniería de Sistemas y Computación. Pontificia Universidad Javeriana Cali, 2026"


def correr(*args):
  return subprocess.run([sys.executable, *args], cwd=HERE, capture_output=True, text=True, check=True).stdout


def guardar_salidas():
  SAL.mkdir(exist_ok=True)
  for head in (50, 2150, 4900):
    (SAL / f"salida_{head}.txt").write_text(correr("lab3Punto2.py", str(head), "--semilla", "42"), encoding="utf-8")
  (SAL / "salida_graficas.txt").write_text(correr("lab3Punto3.py", "2150"), encoding="utf-8")


doc = Document()
st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(11)
for nombre in ("Title", "Heading 1", "Heading 2"):
  doc.styles[nombre].font.color.rgb = RGBColor(0, 0, 0)
for s in doc.sections:
  s.left_margin = s.right_margin = Cm(2.5)


def p(texto, bold=False, italic=False, align=None, size=None):
  par = doc.add_paragraph()
  r = par.add_run(texto)
  r.bold, r.italic = bold, italic
  if size:
    r.font.size = Pt(size)
  if align:
    par.alignment = align
  return par


def rich(texto):
  # **negrita** dentro de un párrafo
  par = doc.add_paragraph()
  for i, trozo in enumerate(texto.split("**")):
    par.add_run(trozo).bold = i % 2 == 1
  return par


def code(texto, size=8.5):
  par = doc.add_paragraph()
  r = par.add_run(texto.rstrip("\n"))
  r.font.name = "Consolas"
  r.font.size = Pt(size)
  par.paragraph_format.left_indent = Cm(0.5)
  return par


def tabla(filas):
  t = doc.add_table(rows=len(filas), cols=len(filas[0]))
  t.style = "Table Grid"
  for i, fila in enumerate(filas):
    for j, celda in enumerate(fila):
      t.cell(i, j).text = str(celda)
      if i == 0:
        t.cell(i, j).paragraphs[0].runs[0].bold = True
  doc.add_paragraph()


def figura(nombre, pie, ancho=15):
  doc.add_picture(str(GRAF / nombre), width=Cm(ancho))
  doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
  p(pie, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=9)


guardar_salidas()

# Portada
p(TITLE, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=18)
p(AUTHORS, align=WD_ALIGN_PARAGRAPH.CENTER)
p(SUBJ, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=10)
p(f"Repositorio con el código, las gráficas y las salidas: {URL}", align=WD_ALIGN_PARAGRAPH.CENTER, size=10)

# Parte 1
doc.add_heading("1. Revisión conceptual", level=1)

doc.add_heading("Pregunta 1", level=2)
p("Al driver del disco llegan pedidos para los cilindros 10, 22, 20, 2, 40, 6 y 38 en ese orden, cada cilindro de búsqueda toma 6 ms y en los tres casos el brazo arranca en el cilindro 20.")
rich("**a) FCFS.** Los pedidos se atienden en el mismo orden en que llegaron, sin importar qué tan lejos queden de la posición actual.")
code("20 -> 10 -> 22 -> 20 -> 2 -> 40 -> 6 -> 38\n"
     "|10-20| + |22-10| + |20-22| + |2-20| + |40-2| + |6-40| + |38-6|\n"
     "  10    +   12    +   2     +  18    +  38    +  34    +  32     = 146 cilindros\n"
     "146 x 6 ms = 876 ms")
rich("**b) Cilindro más cercano primero o SSTF.** En cada paso se atiende el pedido que esté más cerca del brazo. Hay que tener cuidado al salir del 22, ya que el pedido más cercano es el 10 que está a 12 cilindros y no el 38 que está a 16, por eso el brazo baja primero hasta el 2 y al final sube al 38 y al 40.")
code("20 -> 20 -> 22 -> 10 -> 6 -> 2 -> 38 -> 40\n"
     "|20-20| + |22-20| + |10-22| + |6-10| + |2-6| + |38-2| + |40-38|\n"
     "   0    +    2    +   12    +   4    +   4   +  36    +    2    = 60 cilindros\n"
     "60 x 6 ms = 360 ms")
rich("**c) Algoritmo del ascensor subiendo al inicio.** El brazo atiende todo lo que encuentra mientras sube y cuando ya no quedan pedidos en esa dirección se devuelve. Después de atender el cilindro 2 no queda ningún pedido pendiente, así que no tiene sentido que el brazo siga bajando hasta el 0 y el recorrido termina ahí.")
code("20 -> 20 -> 22 -> 38 -> 40 -> 10 -> 6 -> 2\n"
     "|20-20| + |22-20| + |38-22| + |40-38| + |10-40| + |6-10| + |2-6|\n"
     "   0    +    2    +   16    +    2    +   30    +   4    +   4   = 58 cilindros\n"
     "58 x 6 ms = 348 ms")
tabla([["Algoritmo", "Cilindros", "Tiempo de búsqueda"],
       ["FCFS", 146, "876 ms"], ["SSTF", 60, "360 ms"], ["Ascensor", 58, "348 ms"]])
p("En este caso el ascensor sale un poco mejor que SSTF, mientras que FCFS recorre más del doble que cualquiera de los otros dos.")

doc.add_heading("Pregunta 2", level=2)
p("El disco tiene 5000 cilindros numerados de 0 a 4999, la cabeza está atendiendo el cilindro 2150 y el pedido anterior fue el 1805, lo que indica que el brazo viene subiendo. La cola pendiente en orden FIFO es 2069, 1212, 2296, 2800, 544, 1618, 356, 1523, 4965 y 3681.")
rich("**a) FCFS.** Se recorre la cola en el orden FIFO.")
code("2150 -> 2069 -> 1212 -> 2296 -> 2800 -> 544 -> 1618 -> 356 -> 1523 -> 4965 -> 3681\n"
     "81 + 857 + 1084 + 504 + 2256 + 1074 + 1262 + 1167 + 3442 + 1284 = 13011 cilindros")
rich("**b) SCAN.** Como el brazo viene subiendo, primero atiende los pedidos mayores a 2150 hasta llegar al extremo 4999 y luego baja atendiendo el resto, el último pedido de la bajada es el 356 así que el recorrido termina en ese cilindro.")
code("Subida: 2150 -> 2296 -> 2800 -> 3681 -> 4965 -> 4999   = 4999 - 2150 = 2849\n"
     "Bajada: 4999 -> 2069 -> 1618 -> 1523 -> 1212 -> 544 -> 356 = 4999 - 356 = 4643\n"
     "Total = 2849 + 4643 = 7492 cilindros")
rich("**c) C-SCAN.** El brazo sube hasta 4999, regresa al cilindro 0 sin atender nada en el camino y vuelve a subir atendiendo los pedidos que faltan. En este cálculo se cuenta el regreso de 4999 a 0 como movimiento del brazo, igual que en el programa de la parte 2, si no se contara el total quedaría en 4918 cilindros.")
code("Subida:  2150 -> 2296 -> 2800 -> 3681 -> 4965 -> 4999          = 2849\n"
     "Regreso: 4999 -> 0                                              = 4999\n"
     "Subida:  0 -> 356 -> 544 -> 1212 -> 1523 -> 1618 -> 2069        = 2069\n"
     "Total = 2849 + 4999 + 2069 = 9917 cilindros")
tabla([["Algoritmo", "Distancia total en cilindros"], ["FCFS", "13011"], ["SCAN", "7492"], ["C-SCAN", "9917"]])

doc.add_heading("Pregunta 3", level=2)
p("La ventaja del ascensor modificado, que en la práctica es C-SCAN, está en que el tiempo de espera de los pedidos es más parejo. En el ascensor normal los cilindros del centro se visitan dos veces por ciclo, una al subir y otra al bajar, mientras que los de los extremos solo se visitan una vez. Además cuando el brazo cambia de sentido la zona por la que acaba de pasar casi no tiene pedidos, mientras que la zona del extremo contrario es la que acumula los pedidos más viejos, por lo que un pedido que llega a un extremo justo cuando el brazo se aleja puede llegar a esperar casi dos recorridos completos del disco.")
p("Si el brazo siempre barre en el mismo sentido y regresa rápido al inicio, todos los cilindros se visitan con la misma frecuencia y la espera depende mucho menos de dónde esté el pedido, es decir que la varianza del tiempo de respuesta baja y el servicio es más justo. A cambio el brazo se mueve un poco más por el regreso, como se vio en la pregunta anterior donde C-SCAN dio 9917 cilindros contra 7492 de SCAN.")

# Parte 2
doc.add_heading("2. Implementación práctica", level=1)
p("El programa lab3Punto2.py implementa FCFS, SCAN y C-SCAN sobre un disco de 5000 cilindros numerados de 0 a 4999, genera una serie aleatoria de 1000 pedidos, recibe la posición inicial de la cabeza por línea de comandos y reporta el movimiento total de cada algoritmo. Se ejecuta con python lab3Punto2.py <cabeza> y de forma opcional se le puede pasar --semilla N para repetir la misma serie de pedidos en varias ejecuciones.")
p("FCFS recorre la lista en el orden de llegada y va sumando la distancia absoluta entre cada pedido y la posición actual. SCAN separa los pedidos en los que son mayores o iguales a la cabeza y los que son menores, atiende los primeros en orden ascendente, sigue hasta el extremo 4999 si quedan pedidos por debajo y después atiende los menores en orden descendente. Por defecto empieza subiendo, aunque con mov_arriba=False arranca bajando. C-SCAN también atiende primero los pedidos mayores o iguales a la cabeza en orden ascendente, llega a 4999, salta al cilindro 0 sumando los 4999 cilindros del regreso y termina atendiendo los demás otra vez en orden ascendente.")
p("Antes de generar los pedidos aleatorios el programa corre una pequeña autoprueba con el ejemplo de la pregunta 2 de la parte 1 y comprueba que los tres algoritmos den 13011, 7492 y 9917, que son los mismos valores que se calcularon a mano. También rechaza cualquier posición de cabeza que esté por fuera del rango de 0 a 4999.")
doc.add_heading("Código", level=2)
code((HERE / "lab3Punto2.py").read_text(encoding="utf-8"), size=7.5)
doc.add_heading("Ejecución", level=2)
p("Se ejecutó el programa con la misma serie de 1000 pedidos, usando la semilla 42, y tres posiciones iniciales distintas.")
for head in (50, 2150, 4900):
  code(f"> python lab3Punto2.py {head} --semilla 42\n" + (SAL / f"salida_{head}.txt").read_text(encoding="utf-8"))
p("FCFS mueve la cabeza alrededor de 1,67 millones de cilindros porque salta de un lado a otro del disco sin tener en cuenta la distancia, con pedidos uniformes cada salto mide en promedio un tercio del disco, unos 1667 cilindros, y al multiplicarlo por 1000 pedidos se llega justo a esa cifra. SCAN y C-SCAN se quedan entre 5000 y 10000 cilindros, es decir entre 170 y 330 veces menos. SCAN depende bastante de dónde arranca la cabeza, ya que entre más arriba empiece menos le falta para llegar al extremo, por eso desde 4900 solo recorre 5095 cilindros, mientras que C-SCAN siempre se queda cerca de 9990 porque siempre cuenta el regreso completo de 4999 a 0.")

# Parte 3
doc.add_heading("3. Visualización de datos", level=1)
p("El programa lab3Punto3.py reutiliza las funciones de la parte 2 y genera las gráficas con matplotlib, se ejecutó con python lab3Punto3.py 2150 y la semilla 42.")

doc.add_heading("Movimiento de la cabeza", level=2)
p("En estas tres gráficas solo se dibujan los primeros 30 pedidos de la serie, ya que con los 1000 no se alcanza a distinguir el recorrido. El eje horizontal es el cilindro y el vertical es el orden en que se atiende cada pedido.")
figura("recorrido_fcfs.png", "Figura 1. FCFS, la cabeza cruza el disco de un lado a otro casi en cada paso.")
figura("recorrido_scan.png", "Figura 2. SCAN, sube hasta 4999 y luego baja atendiendo el resto.")
figura("recorrido_cscan.png", "Figura 3. C-SCAN, sube hasta 4999, regresa a 0 y vuelve a subir.")

doc.add_heading("Comparación de rendimiento", level=2)
figura("comparacion_total.png", "Figura 4. Movimiento total con los 1000 pedidos en escala logarítmica.")
figura("scan_vs_cscan_cabezas.png", "Figura 5. Movimiento total de SCAN y C-SCAN según la posición inicial de la cabeza.")
p("En la figura 5 se puede ver que C-SCAN recorre casi 10000 cilindros sin importar dónde empiece, mientras que SCAN recorre menos entre más cerca de 4999 esté la cabeza al inicio porque la subida es más corta. En la posición 0 los dos algoritmos dan lo mismo, ya que solo tienen que subir una vez y no hay bajada ni regreso.")

doc.add_heading("Capacidad de respuesta del sistema", level=2)
p("Para medir la capacidad de respuesta se calculó, para cada pedido, cuántos cilindros llevaba recorridos la cabeza en el momento de atenderlo. Si el tiempo de búsqueda por cilindro es fijo ese valor es proporcional al tiempo que el pedido tuvo que esperar.")
figura("tiempo_respuesta.png", "Figura 6. Distribución del tiempo de respuesta por pedido en escala logarítmica.")
lineas = (SAL / "salida_graficas.txt").read_text(encoding="utf-8").splitlines()
filas = [["Algoritmo", "Movimiento total", "Respuesta promedio", "Respuesta máxima", "Desviación estándar"]]
filas += [l.split() for l in lineas[1:4]]
tabla(filas)
p("Con FCFS un pedido típico espera unos 840000 cilindros, mientras que con SCAN y C-SCAN espera alrededor de 4000. En este experimento SCAN sale un poco mejor que C-SCAN incluso en respuesta, lo cual tiene sentido porque todos los pedidos llegan al mismo tiempo al principio y C-SCAN pierde 4999 cilindros en el regreso. La ventaja de C-SCAN que se explicó en la pregunta 3 se nota cuando los pedidos van llegando mientras el brazo se mueve, porque en SCAN los que caen justo detrás del brazo tienen que esperar una vuelta completa y los de los extremos esperan todavía más.")

doc.add_heading("Conclusiones", level=1)
p("Con una carga aleatoria grande FCFS mueve la cabeza entre 170 y 330 veces más que SCAN y C-SCAN, así que solo resulta razonable cuando hay muy pocos pedidos en cola. SCAN fue el que menos movió la cabeza en todas las pruebas, mientras que C-SCAN se movió un poco más por el regreso, pero su costo no depende de la posición inicial y reparte mejor la espera cuando los pedidos llegan de forma continua.")

doc.add_heading("Anexo. Código de la visualización", level=1)
p(f"Código de lab3Punto3.py, que genera las gráficas de la parte 3 a partir de las funciones de lab3Punto2.py. Requiere matplotlib y se ejecuta con python lab3Punto3.py <cabeza> [--semilla N]. Los dos programas también están en el repositorio {URL}.")
code((HERE / "lab3Punto3.py").read_text(encoding="utf-8"), size=7.5)

doc.save(HERE / "informe.docx")
print("informe.docx generado")
