# --- Script 1: Extraer prefijos IPv6 chilenos del peer (filtra_prefijos_chilenos_ipv6.py) ---
import pytricia
from ipaddress import ip_network, IPv6Network
import csv

PEER_OBJETIVO = "2001:1398:32:177::24"
DESCRIPCION_PEER = "NIC Chile"

chile_tree = pytricia.PyTricia(128)
with open("chile_prefixes_ipv6.txt") as f:
    for line in f:
        prefix = line.strip()
        if prefix:
            chile_tree.insert(prefix, True)

def pertenece_a_chile(prefix):
    try:
        net = ip_network(prefix)
        return isinstance(net, IPv6Network) and chile_tree.get_key(net) is not None
    except ValueError:
        return False

csv_out = open(f"prefijos_chilenos_{DESCRIPCION_PEER.lower().replace(' ', '_')}_ipv6.csv", "w", newline="")
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
        if ":" not in prefix or not pertenece_a_chile(prefix):
            continue

        as_path = partes[6].strip().split()
        if not as_path:
            continue

        origin_asn = as_path[-1]
        writer.writerow([prefix, origin_asn, peer_ip])
        total += 1

csv_out.close()
print(f"\n✅ Prefijos chilenos IPv6 desde {DESCRIPCION_PEER}: {total} rutas exportadas.")
