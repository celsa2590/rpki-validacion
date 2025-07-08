import ipaddress

archivo = "delegated-lacnic-latest"
chile_v4 = []
chile_v6 = []

with open(archivo) as f:
    for line in f:
        if line.startswith("lacnic|CL|ipv4|"):
            partes = line.strip().split("|")
            base = partes[3]
            cantidad = int(partes[4])
            # Calcular prefijo
            mask = 32 - (cantidad - 1).bit_length()
            chile_v4.append(f"{base}/{mask}")
        elif line.startswith("lacnic|CL|ipv6|"):
            partes = line.strip().split("|")
            base = partes[3]
            prefix_len = partes[4]
            chile_v6.append(f"{base}/{prefix_len}")

# Guardar en archivos
with open("chile_prefixes_ipv4.txt", "w") as f:
    f.write("\n".join(chile_v4))

with open("chile_prefixes_ipv6.txt", "w") as f:
    f.write("\n".join(chile_v6))

print(f"Prefijos IPv4 de Chile: {len(chile_v4)}")
print(f"Prefijos IPv6 de Chile: {len(chile_v6)}")
