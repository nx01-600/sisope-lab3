import argparse
import random


def fcfs(requests, head):
  movimientos = 0
  actual = head
  recorrido = [head]

  for req in requests:
    movimientos += abs(req - actual)
    actual = req
    recorrido.append(actual)

  return movimientos, recorrido


def scan(requests, head, mov_arriba=True, max_cilindro=4999):
  movimientos = 0
  actual = head
  recorrido = [head]

  if mov_arriba:
    #request mayores o iguales a la posicion actual
    up_reqs = sorted([r for r in requests if r >= actual])
    down_reqs = sorted([r for r in requests if r < actual], reverse=True)

    for req in up_reqs:
      movimientos += abs(req - actual)
      actual = req
      recorrido.append(actual)

    #si hay request hacia abajo, el brazo llega hasta el extremo superior del disco
    if down_reqs:
      if actual < max_cilindro:
        movimientos += max_cilindro - actual
        actual = max_cilindro
        recorrido.append(actual)

      for req in down_reqs:
        movimientos += abs(req - actual)
        actual = req
        recorrido.append(actual)
  else:
    #request menores o iguales a la posicion actual
    down_reqs = sorted([r for r in requests if r <= actual], reverse=True)
    up_reqs = sorted([r for r in requests if r > actual])

    for req in down_reqs:
      movimientos += abs(req - actual)
      actual = req
      recorrido.append(actual)

    # si hay requests hacia arriba el brazo llega hasta el extremo inferior (cilindro 0)
    if up_reqs:
      if actual > 0:
        movimientos += actual - 0
        actual = 0
        recorrido.append(actual)

      for req in up_reqs:
        movimientos += abs(req - actual)
        actual = req
        recorrido.append(actual)

  return movimientos, recorrido


def cScan(requests, head, max_cilindro=4999):
  movimientos = 0
  actual = head
  recorrido = [head]

  up_reqs = sorted([r for r in requests if r >= actual])
  down_reqs = sorted([r for r in requests if r < actual])

  #atiende los request en direccion ascendente
  for req in up_reqs:
    movimientos += abs(req - actual)
    actual = req
    recorrido.append(actual)

  if down_reqs:
    #llega al limite del disco si aun no esta en el
    if actual < max_cilindro:
      movimientos += max_cilindro - actual
      actual = max_cilindro
      recorrido.append(actual)

    #regreso al inicio del disco (cilindro 0)
    movimientos += max_cilindro  # Desplazamiento desde el extremo hasta 0
    actual = 0
    recorrido.append(actual)

    #sigue atendiendo los request restantes en direccion ascendente
    for req in down_reqs:
      movimientos += abs(req - actual)
      actual = req
      recorrido.append(actual)

  return movimientos, recorrido


def generar_requests(n=1000, max_cilindro=4999, semilla=None):
  rnd = random.Random(semilla)
  return [rnd.randint(0, max_cilindro) for _ in range(n)]


def autoprueba():
  #ejemplo de Silberschatz (pregunta 2 de la parte 1)
  q = [2069, 1212, 2296, 2800, 544, 1618, 356, 1523, 4965, 3681]
  assert fcfs(q, 2150)[0] == 13011
  assert scan(q, 2150)[0] == 7492
  assert cScan(q, 2150)[0] == 9917


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Planificacion de disco: FCFS, SCAN y C-SCAN")
  parser.add_argument("head", type=int, help="posicion inicial de la cabeza (0 a 4999)")
  parser.add_argument("--semilla", type=int, default=None, help="semilla para repetir la misma serie de requests")
  args = parser.parse_args()

  if not 0 <= args.head <= 4999:
    parser.error("la posicion de la cabeza debe estar entre 0 y 4999")

  autoprueba()
  requests = generar_requests(semilla=args.semilla)

  print(f"Cabeza inicial: {args.head} | Requests: {len(requests)} | Cilindros: 0-4999")
  print(f"FCFS   : {fcfs(requests, args.head)[0]:>9} cilindros")
  print(f"SCAN   : {scan(requests, args.head)[0]:>9} cilindros")
  print(f"C-SCAN : {cScan(requests, args.head)[0]:>9} cilindros")
