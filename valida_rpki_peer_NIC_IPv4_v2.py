import json
import pytricia
import collections
from ipaddress import ip_network, IPv4Network
from tqdm import tqdm
import csv

# --- CONFIGURACIÓN ---
PEER_OBJETIVO = "200.16.114.53"
DESCRIPCION_PEER = "NIC Chile"

# --- Cargar ROAs desde vrps.json (solo IPv4) ---
with open("vrps.json") as f:
    roas = json.load(f)["roas"]

roa_trie = pytricia.PyTricia(32)
roa_dict = collections.defaultdict(list)

for roa in roas:
    prefix = roa["prefix"]
    if ":" in prefix:
        continue  # saltar IPv6
    asn = roa["asn"].replace("AS", "")
    maxlen = int(roa["maxLength"])
    if prefix not in roa_trie:
        roa_trie[prefix] = True
    roa_dict[prefix].append((asn, maxlen))

# --- Función de validación para IPv4 optimizada ---
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

# --- Archivo CSV de salida IPv4 ---
csv_out = open(f"resultados_{DESCRIPCION_PEER.lower().replace(' ', '_')}_ipv4.csv", "w", newline="")
writer = csv.writer(csv_out)
writer.writerow(["prefix", "origin_asn", "validation_state", "peer_ip"])

# --- Contadores ---
contadores = {"valid": 0, "invalid": 0, "notfound": 0}

# --- Contar rutas IPv4 entregadas por ese peer ---
with open("rib.txt") as f:
    total = sum(
        1 for l in f if l.startswith("TABLE_DUMP2")
        and len(l.strip().split("|")) >= 7
        and l.strip().split("|")[3].strip() == PEER_OBJETIVO
        and ":" not in l.strip().split("|")[5]  # solo prefijos IPv4
    )

# --- Procesar rutas IPv4 ---
with open("rib.txt") as f, tqdm(total=total, desc=f"Rutas IPv4 de {DESCRIPCION_PEER}") as pbar:
    for line in f:
        if not line.startswith("TABLE_DUMP2"):
            continue
        partes = line.strip().split("|")
        if len(partes) < 7:
            pbar.update(1)
            continue

        peer_ip = partes[3].strip()
        if peer_ip != PEER_OBJETIVO:
            pbar.update(1)
            continue

        prefix = partes[5].strip()
        if ":" in prefix:
            pbar.update(1)
            continue  # saltar IPv6

        as_path = partes[6].strip().split()
        if not as_path:
            pbar.update(1)
            continue

        origin_asn = as_path[-1]
        estado = validar(origin_asn, prefix)
        contadores[estado] += 1
        writer.writerow([prefix, origin_asn, estado, peer_ip])
        pbar.update(1)

# --- Cierre y reporte final ---
csv_out.close()

print(f"\nResultados para rutas IPv4 recibidas desde {DESCRIPCION_PEER}:")
total_resultados = sum(contadores.values())
for estado in ["valid", "invalid", "notfound"]:
    cantidad = contadores[estado]
    porcentaje = (cantidad / total_resultados * 100) if total_resultados else 0
    print(f"  {estado.upper()}: {cantidad} - {porcentaje:.1f}%")
