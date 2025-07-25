import pandas as pd

# Cargar archivo de resultados
archivo = "resultados_nic_chile_filtrados_ipv6.csv"
df = pd.read_csv(archivo)

# Filtrar solo prefijos inválidos
df_invalidos = df[df["validation_state"] == "invalid"]

# Contar cuántos prefijos inválidos tiene cada ASN
conteo_asn = df_invalidos["origin_asn"].value_counts().reset_index()
conteo_asn.columns = ["origin_asn", "invalid_prefix_count"]

# Ordenar de mayor a menor
conteo_asn = conteo_asn.sort_values(by="invalid_prefix_count", ascending=False)

# Mostrar los primeros 20
print("Top 20 ASN con más prefijos inválidos en IPv6 (Chile):")
print(conteo_asn.head(20).to_string(index=False))

# Guardar resultados en un nuevo archivo
conteo_asn.to_csv("ranking_asn_invalidos_ipv6_chile.csv", index=False)
