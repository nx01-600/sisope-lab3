# Lab 3 - Sistemas Operativos

Código del Lab 3 de Sistemas Operativos (dispositivos y planificación de disco), Pontificia Universidad Javeriana Cali, 2026.

Integrantes: Nicolás Carreño Tascón, David Leandro Cruz y Ricardo Perez.

## Contenido

- `lab3Punto2.py`: FCFS, SCAN y C-SCAN sobre un disco de 5000 cilindros (0 a 4999) con 1000 pedidos aleatorios. Recibe la posición inicial de la cabeza por línea de comandos y muestra el movimiento total de cada algoritmo.
- `lab3Punto3.py`: gráficas de movimiento de la cabeza, comparación de rendimiento y tiempo de respuesta. Las guarda en `graficas/`.
- `build_informe.py`: genera `informe.docx` con las tres partes del laboratorio.
- `graficas/` y `salidas/`: resultados de las ejecuciones con la semilla 42.
- `informe.pdf`: informe entregado.

## Uso

Requiere Python 3.10 o superior y matplotlib (`pip install matplotlib`).

```
python lab3Punto2.py 2150 --semilla 42
python lab3Punto3.py 2150
```
