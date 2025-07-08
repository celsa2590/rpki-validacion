import pytricia
from ipaddress import ip_network, IPv4Network
import csv

# --- CONFIGURACIÓN ---
PEER_OBJETIVO = "200.16.114.53"
DESCRIPCION_PEER = "NIC Chile"

# --- Cargar prefijos IPv4 de Chile en un trie ---
chile_tree = pytricia.PyTricia(32)
with open("chile_prefixes_ipv4.txt") as f:
    for line in f:
        prefix = line.strip()
        if prefix:
            chile_tree.insert(prefix, True)

def pertenece_a_chile(prefix):
    try:
        net = ip_network(prefix)
        return isinstance(net, IPv4Network) and chile_tree.get_key(net) is not None
    except ValueError:
        return False

# --- Archivo de salida ---
csv_out = open(f"prefijos_chilenos_{DESCRIPCION_PEER.lower().replace(' ', '_')}_ipv4.csv", "w", newline="")
writer = csv.writer(csv_out)
writer.writerow(["prefix", "origin_asn", "peer_ip"])

total = 0
with open("rib.txt") as f:
    for line in f:
        if not line.startswith("TABLE_DUMP2"):
            continue
        partes = line.strip().split("|")
        if len(partes) < 7:
            continue

        peer_ip = partes[3].strip()
        if peer_ip != PEER_OBJETIVO:
            continue

        prefix = partes[5].strip()
        if ":" in prefix or not pertenece_a_chile(prefix):
            continue

        as_path = partes[6].strip().split()
        if not as_path:
            continue

        origin_asn = as_path[-1]
        writer.writerow([prefix, origin_asn, peer_ip])
        total += 1

csv_out.close()
print(f"✅ Prefijos chilenos IPv4 desde {DESCRIPCION_PEER}: {total} rutas exportadas.")
