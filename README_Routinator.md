# 🛠️ Instalación de Routinator desde código fuente en Ubuntu (sin usar root)

Este repositorio documenta paso a paso cómo instalar y configurar **Routinator**, el validador RPKI de NLnetLabs, compilándolo desde código fuente en un sistema Ubuntu.  

---

## 👤 1. Crear un usuario dedicado

```bash
sudo adduser --system --home /home/routinator --shell /bin/bash routinator
sudo groupadd routinator
sudo usermod -g routinator routinator
sudo chown -R routinator:routinator /home/routinator
```

---

## 🔐 2. Iniciar sesión como el usuario `routinator`

```bash
sudo -u routinator -i
```

---

## 🧰 3. Instalar Rust y Routinator

Ya dentro del usuario `routinator`:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
cargo install --locked routinator
```

---

## ✅ 4. Verificar instalación

```bash
~/.cargo/bin/routinator --version
~/.cargo/bin/routinator config
```

---

## ⚙️ 5. Configurar Routinator como servicio

Salir del usuario routinator:
```bash
exit
```

Crear el archivo de servicio:

```bash
sudo nano /etc/systemd/system/routinator.service
```

Contenido sugerido:

```
[Unit]
Description=Routinator RPKI Validator
After=network.target

[Service]
ExecStart=/home/routinator/.cargo/bin/routinator server --rtr 3323 --http 8323
User=routinator
WorkingDirectory=/home/routinator
Environment=ROUTINATOR_CACHE_DIR=/home/routinator/.rpki-cache
Environment=PATH=/home/routinator/.cargo/bin:/usr/bin:/bin
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

---

## ▶️ 6. Activar servicio Routinator

```bash
sudo systemctl daemon-reload
sudo systemctl enable routinator
sudo systemctl start routinator
```

---

## ⏱️ 7. Asegurar hora correcta para validación RPKI

```bash
sudo timedatectl set-timezone America/Santiago
```

---

## ✅ 8. Obtener archivo de ROAs

```bash
routinator vrps --output vrps.json --format json
```

---

## 🙌 Créditos

Instrucciones compiladas por Celsa Sánchez — NIC Chile  
Basado en la documentación oficial: [https://routinator.docs.nlnetlabs.nl/en/stable/building.html](https://routinator.docs.nlnetlabs.nl/en/stable/building.html)
