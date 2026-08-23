#!/bin/bash
# Einmaliges Server-Setup. Ausfuehren: bash deploy/setup_server.sh
set -e

REMOTE="ubuntu@179.237.111.178"
REMOTE_DIR="/home/ubuntu/wedding_page"

echo "==> Verzeichnis anlegen..."
ssh "$REMOTE" "mkdir -p $REMOTE_DIR"

echo "==> config.yaml auf Server kopieren..."
scp config.yaml "$REMOTE:$REMOTE_DIR/config.yaml"
echo "    WICHTIG: config.yaml auf dem Server auf DEBUG: false und richtige Domain anpassen!"
echo "    ssh $REMOTE 'nano $REMOTE_DIR/config.yaml'"
read -p "    Enter druecken sobald config.yaml angepasst ist..."

echo "==> Dateien synchronisieren..."
rsync -avz --delete \
  --exclude='.git/' \
  --exclude='venv/' \
  --exclude='__pycache__/' \
  --exclude='*.pyc' \
  --exclude='config.yaml' \
  --exclude='db.sqlite3' \
  --exclude='media/' \
  --exclude='static/CACHE/' \
  --exclude='staticfiles/' \
  --exclude='node_modules/' \
  ./ "$REMOTE:$REMOTE_DIR/"

echo "==> Python-Umgebung einrichten..."
ssh "$REMOTE" "
  set -e
  cd $REMOTE_DIR
  python3 -m venv venv
  source venv/bin/activate
  pip install --upgrade pip --quiet
  pip install -r requirements.txt --quiet
  pip install gunicorn --quiet

  python manage.py migrate --no-input
  python manage.py collectstatic --no-input --clear

  sudo mkdir -p /var/log/gunicorn
  sudo chown \$USER:www-data /var/log/gunicorn
"

echo ""
echo "==> Abschliessende Schritte auf dem Server:"
echo ""
echo "  1. gunicorn.service installieren (USER ersetzen):"
echo "     sudo cp $REMOTE_DIR/deploy/gunicorn.service /etc/systemd/system/gunicorn.service"
echo "     sudo nano /etc/systemd/system/gunicorn.service"
echo "     sudo systemctl daemon-reload && sudo systemctl enable --now gunicorn"
echo ""
echo "  2. Nginx konfigurieren (USER + Domain ersetzen):"
echo "     sudo cp $REMOTE_DIR/deploy/nginx.conf /etc/nginx/sites-available/wedding_page"
echo "     sudo nano /etc/nginx/sites-available/wedding_page"
echo "     sudo ln -s /etc/nginx/sites-available/wedding_page /etc/nginx/sites-enabled/"
echo "     sudo nginx -t && sudo systemctl reload nginx"
echo ""
echo "==> Setup abgeschlossen."
