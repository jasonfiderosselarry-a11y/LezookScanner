#!/bin/bash
# LEZOOK SCANNER - Lanceur Linux/macOS
echo "╔══════════════════════════════════╗"
echo "║      LEZOOK SCANNER v3.0         ║"
echo "║  +261 32 542 10                  ║"
echo "╚══════════════════════════════════╝"
echo ""
echo "[*] Vérification des dépendances..."
pip install kivymd kivy --quiet
echo "[*] Lancement de Lezook Scanner..."
python3 main.py
