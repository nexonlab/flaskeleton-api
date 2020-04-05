#!/bin/bash
echo "=> Instalando pacotes de requirements.txt necessarios a aplicacao flaskeleton-api..."
pip install -r requirements.txt
echo ""
echo "=> Iniciando gunicorn..."
gunicorn  --worker-class gevent --workers=4 --threads 50 --bind=0.0.0.0:5000 --log-level=info app:'create_app()'
