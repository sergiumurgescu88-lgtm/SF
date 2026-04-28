#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SF Engine v2.1 — Motor de calcul Studiu de Fezabilitate Parc Fotovoltaic
Conform HG 907/2016. Realist: taxe, amortizare, inlocuiri, LCOE standard + net.
"""

import json
import sys
from pathlib import Path

def load_config(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def calc_bilant_energetic(cfg):
    p = cfg['proiect']
    cl = cfg['date_clima']
    pi = cfg['pierderi_sistem']
    
    putere_kwp = p['putere_mwp'] * 1000
    iradianta = cl['iradianta_kwh_kwp_an']
    
    prod_bruta_mwh = p['putere_mwp'] * iradianta
    bonus_pct = pi['bonus_tracker_pct']
    prod_cu_tracker = prod_bruta_mwh * (1 + bonus_pct / 100)
    total_pierderi_pct = pi['total_pierderi_pct']
    prod_neta_p50 = prod_cu_tracker * (1 - total_pierderi_pct / 100)
    prod_p90 = prod_neta_p50 * 0.91
    
    consum_propriu_pct = pi.get('consum_propriu_pct', 0.8)
    consum_propriu_mwh = prod_neta_p50 * (consum_propriu_pct / 100)
    livrat_retea = prod_neta_p50 - consum_propriu_mwh
    
    ore_an = 8760
    factor_capacitate = prod_neta_p50 / (p['putere_mwp'] * ore_an) * 100
    
    return {
        'putere_kwp': putere_kwp,
        'iradianta_kwh_kwp_an': iradianta,
        'prod_bruta_mwh': round(prod_bruta_mwh, 1),
        'bonus_tracker_pct': bonus_pct,
        'prod_cu_tracker_mwh': round(prod_cu_tracker, 1),
        'total_pierderi_pct': total_pierderi_pct,
        'prod_neta_p50_mwh': round(prod_neta_p50, 1),
        'prod_p90_mwh': round(prod_p90, 1),
        'consum_propriu_mwh': round(consum_propriu_mwh, 1),
        'livrat_retea_mwh': round(livrat_retea, 1),
        'factor_capacitate_pct': round(factor_capacitate, 2),
        'detaliu_pierderi': {
            'temperatura': pi['temperatura_pct'],
            'soiling': pi['soiling_pct'],
            'invertor': pi['invertor_pct'],
            'cabluri_dc': pi['cabluri_dc_pct'],
            'cabluri_ac': pi['cabluri_ac_pct'],
            'umbrire': pi['umbrire_pct'],
            'disponibilitate_retea': pi['disponibilitate_retea_pct'],
            'consum_propriu': consum_propriu_pct
        }
    }

def calc_producție_anuala(cfg):
    prod_an1 = calc_bilant_energetic(cfg)['prod_neta_p50_mwh']
    degradare = cfg['finante']['degradare_panouri_anuala_pct'] / 100
    ani = cfg['finante']['orizont_ani']
    return [round(prod_an1 * ((1 - degradare) ** (an - 1)), 1) for an in range(1, ani + 1)]

def calc_opex_anual(cfg, an):
    f = cfg['finante']
    fiscal = cfg.get('fiscal', {})
    base = f['opex_an1_eur'] * ((1 + f['opex_crestere_anuala_pct'] / 100) ** (an - 1))
    extra = (
        fiscal.get('asigurare_anuala_eur', 0) +
        fiscal.get('impozit_cladiri_anuala_eur', 0) +
        fiscal.get('taxe_echilibrare_anuala_eur', 0) +
        fiscal.get('administrare_anuala_eur', 0)
    ) * ((1 + f['opex_crestere_anuala_pct'] / 100) ** (an - 1))
    return round(base + extra, 0)

def calc_dcf_scenariu(cfg, productii=None, cu_grant=True):
    f = cfg['finante']
    fiscal = cfg.get('fiscal', {})
    p = cfg['proiect']
    
    if productii is None:
        productii = calc_producție_anuala(cfg)
    
    tarif = f['tarif_ppa_eur_mwh']
    wacc = f['wacc_pct'] / 100
    ani = f['orizont_ani']
    
    if cu_grant:
        capex_net = f['cofinantare_eur']
    else:
        capex_net = f['capex_total_eur']
    
    amortizare_anuala = f['capex_total_eur'] / fiscal.get('amortizare_ani', 25)
    tax_rate = fiscal.get('impozit_profit_pct', 16) / 100
    inv_an = fiscal.get('inlocuire_invertoare_an', 999)
    inv_cost = fiscal.get('inlocuire_invertoare_cost_eur', 0)
    val_reziduala = f['capex_total_eur'] * (f['valoare_reziduala_pct'] / 100)
    
    tabel = []
    fcf_cumulat = -capex_net
    pierdere_fiscala = 0.0
    
    for i, prod in enumerate(productii, 1):
        venituri = prod * tarif
        opex = calc_opex_anual(cfg, i)
        ebitda = venituri - opex
        dep = amortizare_anuala if i <= fiscal.get('amortizare_ani', 25) else 0
        profit_imp = ebitda - dep
        maint = inv_cost if i == inv_an else 0
        
        if profit_imp < 0:
            pierdere_fiscala += abs(profit_imp)
            tax = 0
        else:
            comp = min(pierdere_fiscala, profit_imp)
            profit_imp -= comp
            pierdere_fiscala -= comp
            tax = profit_imp * tax_rate if profit_imp > 0 else 0
        
        fcf = ebitda - tax - maint
        if i == ani:
            fcf += val_reziduala
        
        factor = 1 / ((1 + wacc) ** i)
        fcf_act = fcf * factor
        fcf_cumulat += fcf_act
        
        tabel.append({
            'an': i,
            'productie_mwh': round(prod, 1),
            'venituri_eur': round(venituri, 0),
            'opex_eur': round(opex, 0),
            'ebitda_eur': round(ebitda, 0),
            'depreciere_eur': round(dep, 0),
            'profit_impozabil_eur': round(profit_imp, 0),
            'tax_eur': round(tax, 0),
            'capex_maint_eur': round(maint, 0),
            'fcf_eur': round(fcf, 0),
            'factor_8pct': round(factor, 4),
            'fcf_actualizat_eur': round(fcf_act, 0),
            'fcf_cumulat_eur': round(fcf_cumulat, 0)
        })
    
    sum_fcf_act = sum(r['fcf_actualizat_eur'] for r in tabel)
    npv = sum_fcf_act - capex_net
    
    # IRR - metoda standard (fara cash inflow din grant)
    def npv_irr(rate):
        return -capex_net + sum(r['fcf_eur'] / ((1 + rate) ** r['an']) for r in tabel)
    
    low, high = -0.5, 2.0
    for _ in range(100):
        mid = (low + high) / 2
        if npv_irr(mid) > 0:
            low = mid
        else:
            high = mid
    irr = mid * 100
    
    # Payback actualizat
    payback = None
    for r in tabel:
        if r['fcf_cumulat_eur'] >= 0:
            prev = tabel[r['an'] - 2] if r['an'] > 1 else None
            if prev and (r['fcf_cumulat_eur'] - prev['fcf_cumulat_eur']) != 0:
                payback = prev['an'] + (0 - prev['fcf_cumulat_eur']) / (r['fcf_cumulat_eur'] - prev['fcf_cumulat_eur'])
            else:
                payback = r['an']
            break
    
    # LCOE STANDARD (CapEx total - cost social)
    capex_total_act = f['capex_total_eur']
    opex_total_act = sum(r['opex_eur'] * r['factor_8pct'] for r in tabel)
    maint_total_act = sum(r['capex_maint_eur'] * r['factor_8pct'] for r in tabel)
    rezidual_act = val_reziduala / ((1 + wacc) ** ani)
    costuri_total_act = capex_total_act + opex_total_act + maint_total_act - rezidual_act
    prod_total_act = sum(r['productie_mwh'] * r['factor_8pct'] for r in tabel)
    lcoe_standard = costuri_total_act / prod_total_act if prod_total_act > 0 else 0
    
    # LCOE NET (pe cofinantare - cost pentru investitor)
    if cu_grant:
        capex_net_act = f['cofinantare_eur']
        costuri_net_act = capex_net_act + opex_total_act + maint_total_act - rezidual_act
        lcoe_net = costuri_net_act / prod_total_act if prod_total_act > 0 else 0
    else:
        lcoe_net = lcoe_standard
    
    return {
        'tabel': tabel,
        'indicatori': {
            'scenariu': 'cu_grant' if cu_grant else 'fara_grant',
            'capex_total_eur': f['capex_total_eur'],
            'grant_eur': f['grant_eur'],
            'cofinantare_eur': f['cofinantare_eur'],
            'investitie_neta_eur': capex_net,
            'sum_fcf_actualizat_eur': round(sum_fcf_act, 0),
            'npv_eur': round(npv, 0),
            'irr_pct': round(irr, 1),
            'payback_ani': round(payback, 1) if payback else '>25',
            'lcoe_standard_eur_mwh': round(lcoe_standard, 2),
            'lcoe_net_eur_mwh': round(lcoe_net, 2) if cu_grant else None,
            'productie_total_25ani_mwh': round(sum(productii), 0),
            'venituri_total_25ani_eur': round(sum(r['venituri_eur'] for r in tabel), 0),
            'taxe_total_25ani_eur': round(sum(r['tax_eur'] for r in tabel), 0),
            'opex_total_25ani_eur': round(sum(r['opex_eur'] for r in tabel), 0),
            'valoare_reziduala_eur': round(val_reziduala, 0)
        }
    }

def calc_sensibilitate(cfg):
    f = cfg['finante']
    productii_base = calc_producție_anuala(cfg)
    capex_base = f['cofinantare_eur']
    tarif_base = f['tarif_ppa_eur_mwh']
    
    scenarii = [
        ('Bază', 0, None, None, None),
        ('Tarif PPA', +10, tarif_base * 1.10, None, None),
        ('Tarif PPA', -10, tarif_base * 0.90, None, None),
        ('CapEx Net', +15, None, capex_base * 1.15, None),
        ('CapEx Net', -15, None, capex_base * 0.85, None),
        ('Producție', +5, None, None, [p * 1.05 for p in productii_base]),
        ('Producție', -5, None, None, [p * 0.95 for p in productii_base]),
    ]
    
    rezultate = []
    for nume, var, tarif_ov, capex_ov, prod_ov in scenarii:
        cfg_orig_tarif = f['tarif_ppa_eur_mwh']
        cfg_orig_capex = f['cofinantare_eur']
        if tarif_ov:
            f['tarif_ppa_eur_mwh'] = tarif_ov
        if capex_ov:
            f['cofinantare_eur'] = capex_ov
        prod_use = prod_ov if prod_ov is not None else productii_base
        dcf = calc_dcf_scenariu(cfg, productii=prod_use, cu_grant=True)
        f['tarif_ppa_eur_mwh'] = cfg_orig_tarif
        f['cofinantare_eur'] = cfg_orig_capex
        
        ind = dcf['indicatori']
        rezultate.append({
            'scenariu': nume,
            'variatie_pct': var,
            'npv_eur': ind['npv_eur'],
            'irr_pct': ind['irr_pct'],
            'payback_ani': ind['payback_ani']
        })
    
    return rezultate

def calc_impact_mediu(cfg, prod_an1):
    imp = cfg['impact']
    co2_an = prod_an1 * 1000 * imp['factor_emisie_kg_co2_kwh'] / 1000
    co2_25ani = co2_an * cfg['finante']['orizont_ani']
    return {
        'co2_evitat_tone_an': round(co2_an, 1),
        'co2_evitat_tone_25ani': round(co2_25ani, 0),
        'locuri_munca_constructie': imp['locuri_munca_constructie'],
        'locuri_munca_operare': imp['locuri_munca_operare']
    }

def run_all(cfg_path):
    cfg = load_config(cfg_path)
    bilant = calc_bilant_energetic(cfg)
    prod_an1 = bilant['prod_neta_p50_mwh']
    productii = calc_producție_anuala(cfg)
    
    dcf_cu_grant = calc_dcf_scenariu(cfg, productii=productii, cu_grant=True)
    dcf_fara_grant = calc_dcf_scenariu(cfg, productii=productii, cu_grant=False)
    sensibilitate = calc_sensibilitate(cfg)
    impact = calc_impact_mediu(cfg, prod_an1)
    
    return {
        'meta': {'engine_version': '2.1.0', 'proiect': cfg['proiect']['denumire'], 'data_generare': '2026-04-28'},
        'bilant_energetic': bilant,
        'dcf_cu_grant': dcf_cu_grant,
        'dcf_fara_grant': dcf_fara_grant,
        'sensibilitate': sensibilitate,
        'impact': impact
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python sf_engine.py <config.json>")
        sys.exit(1)
    
    cfg_path = sys.argv[1]
    rez = run_all(cfg_path)
    base_name = Path(cfg_path).stem.replace("proiect_", "rezultat_")
    out_path = Path(cfg_path).parent.parent / "output" / f"{base_name}_v21.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(rez, f, indent=2, ensure_ascii=False)
    
    i1 = rez['dcf_cu_grant']['indicatori']
    i2 = rez['dcf_fara_grant']['indicatori']
    
    print("=" * 60)
    print("CU GRANT (perspectiva investitor)")
    print("=" * 60)
    print(f"NPV:         {i1['npv_eur']:>15,} EUR")
    print(f"IRR:         {i1['irr_pct']:>15.1f} %")
    print(f"Payback:     {i1['payback_ani']:>15} ani")
    print(f"LCOE net:    {i1['lcoe_net_eur_mwh']:>15.2f} EUR/MWh")
    print()
    print("=" * 60)
    print("FARA GRANT (eligibilitate I-C / cost social)")
    print("=" * 60)
    print(f"NPV:         {i2['npv_eur']:>15,} EUR")
    print(f"IRR:         {i2['irr_pct']:>15.1f} %")
    print(f"Payback:     {i2['payback_ani']:>15} ani")
    print(f"LCOE std:    {i2['lcoe_standard_eur_mwh']:>15.2f} EUR/MWh")
    print()
    print(f"P50 An1:     {rez['bilant_energetic']['prod_neta_p50_mwh']} MWh")
    print(f"Output:      {out_path}")
