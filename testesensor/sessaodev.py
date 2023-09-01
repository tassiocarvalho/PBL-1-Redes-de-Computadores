#!/usr/bin/env python3
import mercury
import sys
from datetime import datetime

def leitor():
    param = 2300

    if len(sys.argv) > 1:
        param = int(sys.argv[1])

    # Configura a leitura na porta serial onde está o sensor
    reader = mercury.Reader("tmr:///dev/ttyUSB0")

    # Para funcionar use sempre a região "NA2" (Américas)
    reader.set_region("NA2")

    # Não altere a potência do sinal para não prejudicar a placa
    reader.set_read_plan([1], "GEN2", read_power=param)

    # Realiza a leitura das TAGs próximas
    epcs = reader.read()

    # Cria uma lista vazia para armazenar os EPCs
    epc_list = []

    # Adiciona cada tag EPC à lista
    for tag in epcs:
        epc_list.append(tag.epc)

    return epc_list

if __name__ == "__main__":
    tag_list = leitor()
    print("Lista de tags EPC:", tag_list)
