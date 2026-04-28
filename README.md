# SF Generator v2.1

## Structura
sf-generator/
  data/         - JSON-uri proiecte
  engine/       - sf_engine.py, sf_renderer.py, verify_sf.py
  output/       - rezultate
  run.sh        - script master

## Utilizare
1. cp data/proiect_TEMPLATE.json data/proiect_nou.json
2. Editeaza proiect_nou.json cu datele reale
3. ./run.sh data/proiect_nou.json
4. python3 engine/verify_sf.py
5. cat output/SF_Complet_Generat.md

## Versiune: v2.1 (2026-04-28)
