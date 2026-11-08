import argparse
import statistics
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from lab3Punto2 import fcfs, scan, cScan, generar_requests

ALGORITMOS = {"FCFS": fcfs, "SCAN": scan, "C-SCAN": cScan}
COLORES = {"FCFS": "#d1495b", "SCAN": "#2e86ab", "C-SCAN": "#3b8b5a"}
SALIDA = Path(__file__).parent / "graficas"


def tiempos_respuesta(recorrido, requests):
  #movimiento acumulado de la cabeza en el momento en que se atiende cada request
  #(los extremos 0 y 4999 que agregan SCAN y C-SCAN no son requests y se saltan)
  pendientes = Counter(requests)
  acumulado = 0
  tiempos = []
  for anterior, actual in zip(recorrido, recorrido[1:]):
    acumulado += abs(actual - anterior)
    if pendientes[actual] > 0:
      pendientes[actual] -= 1
      tiempos.append(acumulado)
  return tiempos


def grafica_recorrido(nombre, requests, head, n_mostrar):
  #con pocos requests se alcanza a ver el recorrido
  total, recorrido = ALGORITMOS[nombre](requests[:n_mostrar], head)
  fig, ax = plt.subplots(figsize=(8, 4.5))
  ax.plot(recorrido, range(len(recorrido)), marker="o", markersize=3, color=COLORES[nombre])
  ax.invert_yaxis()
  ax.set_xlim(0, 4999)
  ax.set_xlabel("Cilindro")
  ax.set_ylabel("Paso")
  ax.set_title(f"{nombre}: recorrido de la cabeza ({n_mostrar} requests, cabeza en {head}, movimiento {total})")
  ax.grid(alpha=0.3)
  fig.tight_layout()
  fig.savefig(SALIDA / f"recorrido_{nombre.lower().replace('-', '')}.png", dpi=150)
  plt.close(fig)


def grafica_total(resultados, head):
  fig, ax = plt.subplots(figsize=(7, 4.5))
  nombres = list(resultados)
  totales = [resultados[n]["total"] for n in nombres]
  barras = ax.bar(nombres, totales, color=[COLORES[n] for n in nombres])
  ax.bar_label(barras, labels=[f"{t:,}" for t in totales])
  ax.set_yscale("log")
  ax.set_ylabel("Movimiento total (cilindros, escala log)")
  ax.set_title(f"Movimiento total con 1000 requests (cabeza en {head})")
  fig.tight_layout()
  fig.savefig(SALIDA / "comparacion_total.png", dpi=150)
  plt.close(fig)


def grafica_respuesta(resultados):
  fig, ax = plt.subplots(figsize=(7, 4.5))
  nombres = list(resultados)
  ax.boxplot([resultados[n]["tiempos"] for n in nombres], tick_labels=nombres, showfliers=False)
  ax.set_yscale("log")
  ax.set_ylabel("Cilindros recorridos hasta atender el request (log)")
  ax.set_title("Tiempo de respuesta por request")
  ax.grid(alpha=0.3, axis="y")
  fig.tight_layout()
  fig.savefig(SALIDA / "tiempo_respuesta.png", dpi=150)
  plt.close(fig)


def grafica_varias_cabezas(semilla):
  cabezas = list(range(0, 5000, 250))
  requests = generar_requests(semilla=semilla)
  fig, ax = plt.subplots(figsize=(8, 4.5))
  for nombre in ("SCAN", "C-SCAN"):
    ax.plot(cabezas, [ALGORITMOS[nombre](requests, h)[0] for h in cabezas],
            marker="o", label=nombre, color=COLORES[nombre])
  ax.set_xlabel("Posición inicial de la cabeza")
  ax.set_ylabel("Movimiento total (cilindros)")
  ax.set_title("SCAN vs C-SCAN según la posición inicial (FCFS ~1.6 millones, fuera de escala)")
  ax.legend()
  ax.grid(alpha=0.3)
  fig.tight_layout()
  fig.savefig(SALIDA / "scan_vs_cscan_cabezas.png", dpi=150)
  plt.close(fig)


def main():
  parser = argparse.ArgumentParser(description="Graficas de planificacion de disco")
  parser.add_argument("head", type=int, help="posicion inicial de la cabeza (0 a 4999)")
  parser.add_argument("--semilla", type=int, default=42)
  args = parser.parse_args()
  if not 0 <= args.head <= 4999:
    parser.error("la posicion de la cabeza debe estar entre 0 y 4999")

  SALIDA.mkdir(exist_ok=True)
  requests = generar_requests(semilla=args.semilla)

  resultados = {}
  for nombre, algoritmo in ALGORITMOS.items():
    total, recorrido = algoritmo(requests, args.head)
    tiempos = tiempos_respuesta(recorrido, requests)
    assert len(tiempos) == len(requests)
    resultados[nombre] = {"total": total, "tiempos": tiempos}
    grafica_recorrido(nombre, requests, args.head, 30)

  grafica_total(resultados, args.head)
  grafica_respuesta(resultados)
  grafica_varias_cabezas(args.semilla)

  print(f"{'Algoritmo':<8} {'Total':>10} {'Resp. prom':>11} {'Resp. max':>10} {'Desv. est.':>11}")
  for nombre, r in resultados.items():
    t = r["tiempos"]
    print(f"{nombre:<8} {r['total']:>10} {statistics.mean(t):>11.0f} {max(t):>10} {statistics.pstdev(t):>11.0f}")
  print(f"Graficas guardadas en {SALIDA}")


if __name__ == "__main__":
  main()
