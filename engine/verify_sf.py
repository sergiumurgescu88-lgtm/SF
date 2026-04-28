#!/usr/bin/env python3
import sys, json

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
    
    # Helper: check if number appears in text (handles both 7.221 and 7221 formats)
    def num_in_text(val, decimals=0):
        s1 = f"{val:,.0f}".replace(',', '.')  # e.g., 7.221
        s2 = f"{val:,.1f}".replace(',', '.').replace('.', ',', 1).replace(',', '.', 1)  # 7.221,3
        s3 = str(int(val))  # 7221
        s4 = f"{val:.1f}"   # 7221.3
        s5 = f"{val:.0f}"   # 7221
        return s1 in text or s2 in text or s3 in text or s4 in text or s5 in text
    
    checks = []
    
    # P50: check integer part appears near "MWh"
    p50_int = str(int(p50))
    p50_found = p50_int in text and "MWh" in text
    checks.append(("P50 corect în text", p50_found))
    
    # NPV cu grant pozitiv
    checks.append(("NPV cu grant pozitiv", num_in_text(npv_cg) and npv_cg > 0))
    
    # NPV fara grant negativ
    checks.append(("NPV fara grant negativ", num_in_text(npv_fg) and npv_fg < 0))
    
    # IRR cu grant > WACC
    checks.append(("IRR cu grant > WACC", num_in_text(irr_cg, 1) and irr_cg > wacc))
    
    # IRR fara grant < WACC
    checks.append(("IRR fara grant < WACC", num_in_text(irr_fg, 1) and irr_fg < wacc))
    
    # LCOE standard
    checks.append(("LCOE standard prezent", num_in_text(lcoe_std, 2)))
    
    # LCOE net
    checks.append(("LCOE net prezent", num_in_text(lcoe_net, 2)))
    
    # FARA 6.362
    checks.append(("FARA 6.362 (eroarea veche)", "6.362" not in text and "6362" not in text))
    
    # Regula I-C
    checks.append(("Regula I-C explicata", "I-C" in text or "eligibil" in text.lower()))
    
    # FARA text metacognitiv
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
