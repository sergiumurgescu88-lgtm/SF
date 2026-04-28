#!/bin/bash
CONFIG="${1:-data/proiect_dolj.json}"
ENGINE="engine/sf_engine.py"
RENDERER="engine/sf_renderer.py"
OUTDIR="output"

echo "=========================================="
echo "SF GENERATOR v2.1"
echo "=========================================="
echo "Config: $CONFIG"

echo "[1/3] Calcul engine..."
python3 "$ENGINE" "$CONFIG"
if [ $? -ne 0 ]; then echo "EROARE la calcul."; exit 1; fi

RESULT=$(ls -t $OUTDIR/rezultat_*_v21.json 2>/dev/null | head -1)
echo "[2/3] Rezultat: $RESULT"

echo "[3/3] Generare text SF..."
python3 "$RENDERER" "$RESULT" "$CONFIG"
if [ $? -ne 0 ]; then echo "EROARE la render."; exit 1; fi

SF_FILE="$OUTDIR/SF_Complet_Generat.md"
echo ""
echo "=========================================="
echo "✅ SF GENERAT CU SUCCES"
echo "=========================================="
echo "Fisier: $SF_FILE"
wc -c "$SF_FILE" | awk '{print "Dimensiune: " $1 " bytes"}'
echo ""
echo "Verificare: python3 engine/verify_sf.py"
