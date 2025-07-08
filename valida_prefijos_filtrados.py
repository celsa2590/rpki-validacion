import json
from ipaddress import ip_network, IPv4Network
import csv
from tqdm import tqdm

# --- CONFIGURACIÓN ---
INPUT_FILE = "prefijos_chilenos_nic_chile_ipv4.csv"
DESCRIPCION_PEER = "NIC Chile"

# --- Cargar ROAs IPv4 desde vrps.json como lista ---
with open("vrps.json") as f:
    roas = json.load(f)["roas"]

roas_v4_list = []
for roa in roas:
    prefix = roa["prefix"]
    if ":" in prefix:
        continue
    asn = roa["asn"].replace("AS", "")
    maxlen = int(roa["maxLength"])
    net = ip_network(prefix)
    roas_v4_list.append((asn, net, maxlen))

# --- Función de validación optimizada ---
def validar(asn, prefix):
    try:
        net = ip_network(prefix)
        if not isinstance(net, IPv4Network):
            return "notfound"
    except ValueError:
        return "notfound"

    hay_cobertura = False
    for roa_asn, roa_net, maxlen in roas_v4_list:
        if net.subnet_of(roa_net):
            hay_cobertura = True
            if asn == roa_asn and net.prefixlen <= maxlen:
                return "valid"
    return "invalid" if hay_cobertura else "notfound"

# --- Validar prefijos del archivo filtrado ---
contadores = {"valid": 0, "invalid": 0, "notfound": 0}
csv_out = open(f"resultados_{DESCRIPCION_PEER.lower().replace(' ', '_')}_chile_ipv4.csv", "w", newline="")
writer = csv.writer(csv_out)
writer.writerow(["prefix", "origin_asn", "validation_state", "peer_ip"])

with open(INPUT_FILE) as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    filas = list(reader)

for fila in tqdm(filas, desc="Validando prefijos"):
    prefix, origin_asn, peer_ip = fila
    estado = validar(origin_asn, prefix)
    contadores[estado] += 1
    writer.writerow([prefix, origin_asn, estado, peer_ip])

csv_out.close()

print(f"\n✅ Resultados para rutas IPv4 chilenas desde {DESCRIPCION_PEER}:")
for estado in ["valid", "invalid", "notfound"]:
    print(f"  {estado.upper()}: {contadores[estado]}")
