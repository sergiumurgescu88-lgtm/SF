#!/usr/bin/env python3
import sys

path = '/tmp/sf-generator/output/SF_Complet_Generat.md'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

checks = [
    ("P50 corect (7.221)", "7.221" in text or "7221" in text),
    ("FARA 6.362 (eroarea veche)", "6.362" not in text and "6362" not in text),
    ("NPV cu grant pozitiv", "2.731.815" in text or "2731815" in text or "2,731,815" in text),
    ("NPV fara grant negativ", "-868.185" in text or "-868185" in text or "-868,185" in text),
    ("IRR cu grant 40.6%", "40,6%" in text or "40.6%" in text),
    ("IRR fara grant 5.6%", "5,6%" in text or "5.6%" in text),
    ("LCOE standard 79.24", "79,24" in text or "79.24" in text),
    ("LCOE net 30.60", "30,60" in text or "30.60" in text),
    ("Payback cu grant 2.8", "2,8" in text or "2.8" in text),
    ("Regula I-C explicata", "I-C" in text),
    ("FARA text metacognitiv 'discrepanță'", "discrepanță" not in text and "discrepanta" not in text),
    ("FARA 'Această situație este contradictorie'", "contradictorie" not in text),
    ("Capitolul 1 prezent", "CAPITOLUL 1" in text),
    ("Capitolul 8 prezent", "CAPITOLUL 8" in text),
    ("Tabel DCF prezent", "| An |" in text and "FCF Actualizat" in text),
    ("Matrice riscuri prezentă", "Matrice riscuri" in text),
    ("Analiza sensibilitate prezentă", "Analiza sensibilitate" in text),
    ("LIPSĂ ATR menționat", "ATR" in text and "LIPSĂ" in text),
    ("LIPSĂ Studiu Geotehnic", "Geotehnic" in text and "LIPSĂ" in text),
    ("Certificat Urbanism LIPSĂ", "Urbanism" in text and "LIPSĂ" in text),
]

print("=" * 60)
print("VERIFICARE SF GENERAT")
print("=" * 60)
passed = 0
failed = 0
for name, result in checks:
    status = "✅ PASS" if result else "❌ FAIL"
    if result:
        passed += 1
    else:
        failed += 1
    print(f"{status} — {name}")

print("=" * 60)
print(f"Total: {passed} passed, {failed} failed")
if failed == 0:
    print("🎉 SF-ul este VALID și gata de utilizare!")
else:
    print("⚠️  Sunt erori — necesită corecție.")
print("=" * 60)
