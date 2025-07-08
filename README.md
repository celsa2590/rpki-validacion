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
bgpdump -m rib.20250617.0000 > rib_20250617.txt
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

---

## 🐍 Scripts incluidos

| Script                           | Descripción                                               |
|----------------------------------|-----------------------------------------------------------|
| `valida_rpki_peer_NIC_IPv4_v2.py` | Valida rutas IPv4 del peer especificado contra ROAs      |
| `valida_rpki_peer_NIC_IPv6_v2.py` | Valida rutas IPv6 del peer especificado contra ROAs      |
| `filtra_prefijos_chilenos.py`     | Extrae prefijos IPv4 delegados a Chile                   |
| `filtra_prefijos_chilenos_IPv6.py`| Extrae prefijos IPv6 delegados a Chile                   |
| `valida_prefijos_filtrados.py`    | Valida solo los prefijos chilenos (IPv4)                 |
| `valida_prefijos_filtrados_IPv6.py`| Valida solo los prefijos chilenos (IPv6)                |

---

## 🌎 Datos LACNIC

Descargar listado actualizado de prefijos delegados en la región:

```bash
wget https://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-latest
```

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
