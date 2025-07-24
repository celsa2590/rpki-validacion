import json
import pytricia
import collections
from ipaddress import ip_network, IPv4Network
from tqdm import tqdm
import csv

INPUT_FILE = "prefijos_chilenos_nic_chile_ipv4.csv"
DESCRIPCION_PEER = "NIC Chile"

# --- Cargar ROAs desde vrps.json (solo IPv4) ---
with open("vrps.json") as f:
    roas = json.load(f)["roas"]

roa_trie = pytricia.PyTricia(32)
roa_dict = collections.defaultdict(list)

for roa in roas:
    prefix = roa["prefix"]
    if ":" in prefix:
        continue  # Saltar IPv6
    asn = roa["asn"].replace("AS", "")
    maxlen = int(roa["maxLength"])
    if prefix not in roa_trie:
        roa_trie[prefix] = True
    roa_dict[prefix].append((asn, maxlen))

# --- Función de validación optimizada con Trie ---
def validar(asn, prefix):
    try:
        net = ip_network(prefix)
        if not isinstance(net, IPv4Network):
            return "notfound"
    except ValueError:
        return "notfound"

    matches = []
    try:
        covering_prefix = roa_trie.get_key(net)
        while covering_prefix:
            matches.extend(roa_dict.get(covering_prefix, []))
            covering_prefix = roa_trie.parent(covering_prefix)
    except Exception:
        return "notfound"

    if not matches:
        return "notfound"

    for roa_asn, maxlen in matches:
        if asn == roa_asn and net.prefixlen <= maxlen:
            return "valid"

    return "invalid"

# --- Salida CSV ---
csv_out = open(f"resultados_{DESCRIPCION_PEER.lower().replace(' ', '_')}_filtrados_ipv4.csv", "w", newline="")
writer = csv.writer(csv_out)
writer.writerow(["prefix", "origin_asn", "validation_state", "peer_ip"])

contadores = {"valid": 0, "invalid": 0, "notfound": 0}

# --- Leer input CSV ---
with open(INPUT_FILE) as f:
    reader = csv.reader(f)
    next(reader)  # Saltar encabezado
    filas = list(reader)

# --- Validar con barra de progreso ---
for fila in tqdm(filas, desc="Validando prefijos IPv4"):
    prefix, origin_asn, peer_ip = fila
    estado = validar(origin_asn, prefix)
    contadores[estado] += 1
    writer.writerow([prefix, origin_asn, estado, peer_ip])

csv_out.close()

# --- Imprimir resultados ---
total = sum(contadores.values())
print(f"\n✅ Resultados para rutas IPv4 chilenas desde {DESCRIPCION_PEER}:")
for estado in ["valid", "invalid", "notfound"]:
    cantidad = contadores[estado]
    porcentaje = (cantidad / total * 100) if total else 0
    print(f"  {estado.upper()}: {cantidad} - {porcentaje:.1f}%")
