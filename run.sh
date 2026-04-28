#!/bin/bash
CONFIG="${1:-data/proiect_dolj.json}"
ENGINE="engine/sf_engine.py"
RENDERER="engine/sf_renderer.py"
VERIFY="engine/verify_sf.py"
OUTDIR="output"

echo "=========================================="
echo "SF GENERATOR v2.1"
echo "=========================================="
echo "Config: $CONFIG"

# Step 1: Calcul
echo "[1/3] Calcul engine..."
python3 "$ENGINE" "$CONFIG"
if [ $? -ne 0 ]; then
    echo "EROARE la calcul. Oprire."
    exit 1
fi

# Step 2: Find result file (nume dinamic)
BASE=$(basename "$CONFIG" .json | sed 's/proiect_/rezultat_/')
RESULT="$OUTDIR/${BASE}_v21.json"
echo "[2/3] Rezultat: $RESULT"

# Step 3: Render
echo "[3/3] Generare text SF..."
python3 "$RENDERER" "$RESULT" "$CONFIG"
if [ $? -ne 0 ]; then
    echo "EROARE la generare text."
    exit 1
fi

SF_FILE="$OUTDIR/SF_Complet_Generat.md"
echo ""
echo "=========================================="
echo "✅ SF GENERAT CU SUCCES"
echo "=========================================="
echo "Fisier: $SF_FILE"
wc -c "$SF_FILE" | awk '{print "Dimensiune: " $1 " bytes"}'
echo ""
echo "Verificare: python3 $VERIFY $SF_FILE $RESULT"
