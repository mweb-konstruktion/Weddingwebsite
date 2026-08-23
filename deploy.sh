#!/bin/bash
# Deploy via scp. Ausfuehren: bash deploy.sh
set -e

REMOTE="ubuntu@179.237.111.178"
REMOTE_DIR="/home/ubuntu/wedding_page"

echo "==> Temporaeres Archiv erstellen..."
COPYFILE_DISABLE=1 tar --exclude='.git' \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='config.yaml' \
    --exclude='db.sqlite3' \
    --exclude='media' \
    --exclude='static/CACHE' \
    --exclude='node_modules' \
    --exclude='package-lock.json' \
    --exclude='package.json' \
    --exclude='.DS_Store' \
    --exclude='deploy.sh' \
    --exclude='deploy' \
    --exclude='.vscode' \
    --exclude='secret.py' \
    --exclude='readme.md' \
    -czf /tmp/ga_deploy.tar.gz .

echo "==> Archiv auf Server kopieren..."
scp /tmp/ga_deploy.tar.gz "$REMOTE:/tmp/ga_deploy.tar.gz"
rm /tmp/ga_deploy.tar.gz

echo "==> Auf Server entpacken und deployen..."
ssh "$REMOTE" "
  set -e
  mkdir -p $REMOTE_DIR
  tar -xzf /tmp/ga_deploy.tar.gz -C $REMOTE_DIR
  rm /tmp/ga_deploy.tar.gz

  cd $REMOTE_DIR
  source venv/bin/activate
  pip install -r requirements.txt --quiet
  python manage.py migrate --no-input
  python manage.py collectstatic --no-input
  sudo systemctl restart gunicorn
  sudo systemctl is-active gunicorn
"

echo "==> Deploy erfolgreich abgeschlossen."
