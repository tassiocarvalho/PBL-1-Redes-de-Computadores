 #!/usr/bin/env python3
import mercury
import sys
from datetime import datetime


param = 2300

if len(sys.argv) > 1:
        param = int(sys.argv[1])

# configura a leitura na porta serial onde esta o sensor
reader = mercury.Reader("tmr:///dev/ttyUSB0")

# para funcionar use sempre a regiao "NA2" (Americas)
reader.set_region("NA2")

# nao altere a potencia do sinal para nao prejudicar a placa
reader.set_read_plan([1], "GEN2", read_power=param)

# realiza a leitura das TAGs proximas e imprime na tela
# print(reader.read())

epcs = map(lambda tag: tag, reader.read())
for tag in epcs:
    tag.epc