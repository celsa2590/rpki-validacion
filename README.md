# 🛰️ Validación de rutas BGP con RPKI

Este repositorio contiene scripts y procedimientos para validar rutas BGP (IPv4 e IPv6) anunciadas por un peer específico (ej. NIC Chile), usando ROAs obtenidos desde Routinator y dumps de RouteViews. Además, permite filtrar y analizar prefijos delegados a Chile.

---

## 🐍 Scripts incluidos

| Script                           | Descripción                                               |
|----------------------------------|-----------------------------------------------------------|
| `valida_rpki_peer_NIC_IPv4_v2.py` | Valida rutas IPv4 del peer especificado contra ROAs      |
| `valida_rpki_peer_NIC_IPv6_v2.py` | Valida rutas IPv6 del peer especificado contra ROAs      |
| `extrae_prefijos_chile.py`        | Extrae prefijos de Chile del archivo delegated-lacnic-latest|
| `filtra_prefijos_chilenos.py`     | Selecciona prefijos IPv4 de Chile desde rib.txt          |
| `filtra_prefijos_chilenos_IPv6.py`| Selecciona prefijos IPv6 de Chile desde rib.txt          |
| `valida_prefijos_filtrados.py`    | Valida solo los prefijos chilenos (IPv4)                 |
| `valida_prefijos_filtrados_IPv6.py`| Valida solo los prefijos chilenos (IPv6)                |
| `ranking_rpki_invalid_NIC_IPv4.py`| Genera lista de ASN y cantidad de prefijos invalid ipv4  |
| `ranking_rpki_invalid_NIC_IPv6.py`| Genera lista de ASN y cantidad de prefijos invalid ipv6  |

---

## 📦 Estructura general del proceso

### 1. Instalar bgpdump

```bash
sudo apt install bgpdump
```

### 2. Descargar un RIB de RouteViews

```bash
wget http://archive.routeviews.org/route-views.chile/bgpdata/2025.06/RIBS/rib.20250617.0000.bz2
bgpdump -m rib.20250617.0000 > rib.txt
```

### 3. Obtener archivo de ROAs desde Routinator

```bash
routinator vrps --output vrps.json --format json
```
Leer documento README_Routinator.md para más detalle.

### 4. Instalar dependencias

```bash
sudo apt install python3-pip python3-tqdm
git clone https://github.com/jsommers/pytricia.git
cd pytricia
python3 setup.py install --user
python3 -c "import pytricia; print('PyTricia OK')"
```

## 5. Datos LACNIC

Descargar listado actualizado de prefijos delegados en la región:

```bash
wget https://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-latest
```

### 6. Correr script de validación global IPv4

```bash
python3 valida_rpki_peer_NIC_IPv4_v2.py
```
Salida esperada:
Resultados para rutas IPv4 recibidas desde NIC Chile:
  VALID: 553147 - 56.0%
  INVALID: 1216 - 0.1%
  NOTFOUND: 433006 - 43.9%

Archivo que genera: resultados_nic_chile_ipv4.csv

## 7. 🇨🇱 Filtrar los prefijos delegados a Chile

```bash
python3 extrae_prefijos_chile.py
```

El script `extrae_prefijos_chile.py` procesa el archivo oficial de LACNIC `delegated-lacnic-latest`.

Salida esperada:
Prefijos IPv4 de Chile: 809
Prefijos IPv6 de Chile: 313

Archivos que genera:
- `chile_prefixes_ipv4.txt` → contiene todos los bloques IPv4 asignados a Chile
- `chile_prefixes_ipv6.txt` → contiene todos los bloques IPv6 asignados a Chile

### 8. 🔁 Correr script de filtrado de prefijos de Chile

```bash
python3 filtra_prefijos_chilenos.py
```

El script utiliza el archivo `chile_prefixes_ipv4.txt` generado en el paso anterior, para seleccionar únicamente las rutas chilenas desde el dump BGP.

Salida esperada:
✅ Prefijos chilenos IPv4 desde NIC Chile: 5844 rutas exportadas.

Archivo que genera: prefijos_chilenos_nic_chile_ipv4.csv

### 9. 🔁 Correr script de validación de prefijos de Chile

```bash
python3 valida_prefijos_filtrados.py
```

El script utiliza el archivo generado en el paso anterior para analizar únicamente los prefijos chilenos y generar las estadísticas finales de validación RPKI.

Salida esperada:
✅ Resultados para rutas IPv4 chilenas desde NIC Chile:
  VALID: 5283 - 90.4%
  INVALID: 35 - 0.6%
  NOTFOUND: 526 - 9.0%

Archivo que genera: resultados_nic_chile_filtrados_ipv4.csv

### 10. 🔁 Correr script de Ranking de prefijos validados

```bash
python3 ranking_rpki_invalid_NIC_IPv4.py
```
Se genera una lista con el top de ASN y cantidad de prefijos con estado inválido.

### 11. Seguir el mismo procedimiento para IPv6


---
