# Деплой StatusLazer на VPS (Ubuntu/Debian)

## 1. Подключитесь к серверу по SSH
```bash
ssh user@your-server-ip
```

## 2. Установите Python и Git
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git
```

## 3. Склонируйте репозиторий
```bash
cd /opt
sudo git clone https://github.com/davronzaripov1-svg/statuslazer.git
sudo chown -R $USER:$USER /opt/statuslazer
cd /opt/statuslazer
```

## 4. Создайте виртуальное окружение и установите зависимости
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install aiogram gspread google-auth python-dotenv
```

## 5. Создайте файл .env
```bash
nano .env
```
Вставьте:
```
BOT_TOKEN=7836680018:AAxxxxxxxxxxxxxxxxxxxxxxxxx
PRODUCTION_GROUP_ID=-100xxxxxxxxxx
MANAGER_CONTACT=@username
```

## 6. Скопируйте credentials.json
Загрузите файл `credentials.json` на сервер:
```bash
# С локального компьютера:
scp credentials.json user@your-server-ip:/opt/statuslazer/
```

## 7. Создайте systemd сервис
```bash
sudo nano /etc/systemd/system/statuslazer.service
```

Вставьте:
```ini
[Unit]
Description=StatusLazer Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/statuslazer
Environment=PYTHONPATH=/opt/statuslazer
ExecStart=/opt/statuslazer/.venv/bin/python bot/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## 8. Запустите бота
```bash
sudo systemctl daemon-reload
sudo systemctl enable statuslazer
sudo systemctl start statuslazer
```

## Полезные команды
```bash
# Статус бота
sudo systemctl status statuslazer

# Логи бота
sudo journalctl -u statuslazer -f

# Перезапуск
sudo systemctl restart statuslazer

# Остановка
sudo systemctl stop statuslazer
```

## Обновление бота
```bash
cd /opt/statuslazer
git pull
sudo systemctl restart statuslazer
```
