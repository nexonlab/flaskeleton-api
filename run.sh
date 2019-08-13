#!/bin/bash
echo "=> Instalando pacotes de requirements.txt necessarios a aplicacao flaskeleton-api..."
pip install -r requirements.txt
echo ""
echo "=> O waitress-server deu inicio ao processo de deploy da aplicação..."
gunicorn --workers=4 --bind=0.0.0.0:5000 --log-level=debug app:'create_app()'
