#!/usr/bin/env python3
import sys, re, json
from pathlib import Path

def verify(sf_path, result_path):
    with open(sf_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    with open(result_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    b = data['bilant_energetic']
    i_cg = data['dcf_cu_grant']['indicatori']
    i_fg = data['dcf_fara_grant']['indicatori']
    p50 = b['prod_neta_p50_mwh']
    npv_cg = i_cg['npv_eur']
    irr_cg = i_cg['irr_pct']
    npv_fg = i_fg['npv_eur']
    irr_fg = i_fg['irr_pct']
    lcoe_std = i_fg['lcoe_standard_eur_mwh']
    lcoe_net = i_cg['lcoe_net_eur_mwh']
    wacc = 8.0
    
    # Formatare număr cu punct ca separator mii
    p50_str = f"{p50:,.1f}".replace(',', '.').replace('.', ',', 1).replace(',', '.', 1)
    npv_cg_str = f"{npv_cg:,.0f}".replace(',', '.')
    npv_fg_str = f"{npv_fg:,.0f}".replace(',', '.')
    irr_cg_str = f"{irr_cg:.1f}".replace('.', ',')
    irr_fg_str = f"{irr_fg:.1f}".replace('.', ',')
    lcoe_std_str = f"{lcoe_std:.2f}".replace('.', ',')
    lcoe_net_str = f"{lcoe_net:.2f}".replace('.', ',')
    
    # Verificări
    checks = []
    
    # P50 prezent în text
    p50_found = p50_str in text or f"{p50:.1f}" in text or f"{p50:.0f}" in text or str(int(p50)) in text
    checks.append(("P50 corect în text", p50_found))
    
    # NPV cu grant pozitiv
    npv_cg_found = npv_cg_str in text or str(npv_cg) in text
    checks.append(("NPV cu grant pozitiv", npv_cg_found and npv_cg > 0))
    
    # NPV fără grant negativ
    npv_fg_found = npv_fg_str in text or str(npv_fg) in text
    checks.append(("NPV fara grant negativ", npv_fg_found and npv_fg < 0))
    
    # IRR cu grant > WACC
    irr_cg_found = irr_cg_str in text or str(irr_cg) in text
    checks.append(("IRR cu grant > WACC", irr_cg_found and irr_cg > wacc))
    
    # IRR fără grant < WACC
    irr_fg_found = irr_fg_str in text or str(irr_fg) in text
    checks.append(("IRR fara grant < WACC", irr_fg_found and irr_fg < wacc))
    
    # LCOE standard
    lcoe_std_found = lcoe_std_str in text or str(lcoe_std) in text
    checks.append(("LCOE standard prezent", lcoe_std_found))
    
    # LCOE net
    lcoe_net_found = lcoe_net_str in text or str(lcoe_net) in text
    checks.append(("LCOE net prezent", lcoe_net_found))
    
    # Fără eroarea veche 6.362
    checks.append(("FARA 6.362 (eroarea veche)", "6.362" not in text and "6362" not in text))
    
    # Regula I-C
    checks.append(("Regula I-C explicata", "I-C" in text or "eligibil" in text.lower()))
    
    # Fără text metacognitiv
    checks.append(("FARA text metacognitiv", "discrepanță" not in text and "contradictorie" not in text))
    
    # Capitole
    checks.append(("Capitolul 1 prezent", "CAPITOLUL 1" in text))
    checks.append(("Capitolul 8 prezent", "CAPITOLUL 8" in text))
    checks.append(("Tabel DCF prezent", "| An |" in text))
    checks.append(("Matrice riscuri prezenta", "Matrice riscuri" in text or "matricea riscurilor" in text.lower()))
    checks.append(("Analiza sensibilitate prezenta", "sensibilitate" in text.lower()))
    
    # Documente lipsă
    checks.append(("LIPSA ATR mentionat", "ATR" in text and ("LIPS" in text or "lips" in text.lower())))
    checks.append(("LIPSA Studiu Geotehnic", "Geotehnic" in text and ("LIPS" in text or "lips" in text.lower())))
    checks.append(("Certificat Urbanism LIPSA", "Urbanism" in text and ("LIPS" in text or "lips" in text.lower())))
    
    # Print
    print("=" * 60)
    print("VERIFICARE SF GENERAT")
    print("=" * 60)
    passed = 0
    for name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        if result: passed += 1
        print(f"{status} — {name}")
    
    print("=" * 60)
    print(f"Total: {passed}/{len(checks)} passed")
    if passed == len(checks):
        print("🎉 SF-ul este VALID și gata de utilizare!")
    else:
        print(f"⚠️  {len(checks)-passed} erori — necesită corecție.")
    print("=" * 60)
    return passed == len(checks)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 verify_sf.py <SF.md> <rezultat.json>")
        sys.exit(1)
    verify(sys.argv[1], sys.argv[2])
