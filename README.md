# 🛰️ Validación de rutas BGP con RPKI

Este repositorio contiene scripts y procedimientos para validar rutas BGP (IPv4 e IPv6) anunciadas por un peer específico (ej. NIC Chile), usando ROAs obtenidos desde Routinator y dumps de RouteViews. Además, permite filtrar y analizar prefijos delegados a Chile.

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

### 4. Instalar dependencias

```bash
sudo apt install python3-pip python3-tqdm
git clone https://github.com/jsommers/pytricia.git
cd pytricia
python3 setup.py install --user
python3 -c "import pytricia; print('PyTricia OK')"
```

### 5. Correr script de validación global IPv4

```bash
python3 valida_rpki_peer_NIC_IPv4_v2.py
```

### 6. Correr script de validación global IPv6

```bash
python3 valida_rpki_peer_NIC_IPv6_v2.py
```
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

---

## 🌎 Datos LACNIC

Descargar listado actualizado de prefijos delegados en la región:

```bash
wget https://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-latest
```

---

## 🇨🇱 ¿Cómo se filtran los prefijos delegados a Chile?

El script `extrae_prefijos_chile.py` procesa el archivo oficial de LACNIC `delegated-lacnic-latest` y genera dos archivos:

- `chile_prefixes_ipv4.txt` → contiene todos los bloques IPv4 asignados a Chile
- `chile_prefixes_ipv6.txt` → contiene todos los bloques IPv6 asignados a Chile

### 🔁 Cómo se usa

1. Descargar el archivo actualizado desde LACNIC:
```bash
wget https://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-latest
```

2. Ejecutar el script:
```bash
python3 extrae_prefijos_chile.py
```

3. Luego, ejecuta los scripts de filtrado `filtra_prefijos_chilenos.py` y `filtra_prefijos_chilenos_IPv6.py` que utilizan los archivos `chile_prefixes_ipv4.txt` y `chile_prefixes_ipv6.txt` respectivamente, para seleccionar únicamente las rutas chilenas desde el dump BGP.

4. Finalmente, ejecuta los scripts de validación `valida_prefijos_filtrados.py` y `valida_prefijos_filtrados_IPv6.py` que utilizan los archivos generados en el paso anterior para analizar únicamente los prefijos chilenos y generar las estadísticas finales de validación RPKI.

---

## 📊 Resultados

Los resultados se exportan en formato `.csv`, indicando para cada prefijo:
- El ASN de origen
- El estado de validación: `valid`, `invalid`, `notfound`
- El peer que anunció la ruta

---

## 🧠 Requisitos

- Python 3.8 o superior
- PyTricia
- tqdm
- bgpdump
- Routinator
