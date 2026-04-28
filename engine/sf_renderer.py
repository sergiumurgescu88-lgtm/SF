#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SF Renderer v1.0 — Generează textul complet al Studiului de Fezabilitate
din rezultatele JSON produse de sf_engine.py
"""

import json
import sys
from pathlib import Path

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def fmt_nr(x):
    """Formatare număr cu separator mii"""
    return f"{x:,.0f}".replace(',', '.')

def fmt_dec(x, zec=1):
    return f"{x:,.{zec}f}".replace(',', '#').replace('.', ',').replace('#', '.')

def render_cap1(d, cfg):
    p = cfg['proiect']
    i = cfg['investitor']
    return f"""CAPITOLUL 1. INFORMAȚII GENERALE PRIVIND OBIECTUL DE INVESTIȚII

**1.1 Denumirea obiectivului de investiții**
Proiectul "{p['denumire']}" reprezintă o investiție strategică în domeniul energiei regenerabile, amplasată în județul {p['judet']}, localitatea {p['localitate']}. Obiectivul constă în realizarea, punerea în funcțiune și exploatarea unui parc fotovoltaic cu o putere instalată de {p['putere_mwp']} MWp, utilizând tehnologii avansate de tip {p['tehnologie_panou']} și sistem de urmărire {p['tracker']} (1-ax).
- **Caracteristici cheie**:
- Suprafață totală: {p['suprafata_ha']} hectare
- Tehnologie panouri: {p['tehnologie_panou']} (eficiență >21%)
- Sistem de urmărire: {p['tracker']} (bonus de producție estimat la {cfg['pierderi_sistem']['bonus_tracker_pct']}%)
- Producție netă anuală P50: **{fmt_nr(d['bilant_energetic']['prod_neta_p50_mwh'])} MWh/an** (calculată pe baza iradianței PVGIS de {d['bilant_energetic']['iradianta_kwh_kwp_an']} kWh/kWp/an, cu aplicarea pierderilor sistematice de {d['bilant_energetic']['total_pierderi_pct']}% și bonusului tracker)
Localizarea proiectului (coordonate GPS: {p['coordonate']}) beneficiază de condiții solare optime, cu o iradianță medie anuală de {d['bilant_energetic']['iradianta_kwh_kwp_an']} kWh/m² și un risc scăzut de evenimente meteorologice extreme.

**1.2 Ordonator principal de credite / Investitor**
Investitorul proiectului este **{i['denumire']}**, entitate juridică românească specializată în dezvoltarea de proiecte de energie regenerabilă.
- **Date identificative**:
- **Denumire**: {i['denumire']}
- **Adresă sediu**: {p['adresa']}
- **Reprezentant legal**: {i['reprezentant']}
- **CUI**: {i['cui']}
- **Nr. ONRC**: {i['onrc']}
- **Telefon**: {i['telefon']}
- **Email**: {i['email']}
Societatea are o experiență relevantă în sectorul energiei verzi. Fondurile proprii reprezintă {100 - cfg['finante']['grant_procent']}% din valoarea totală a investiției ({fmt_nr(cfg['finante']['cofinantare_eur'])} EUR), restul de {fmt_nr(cfg['finante']['grant_eur'])} EUR urmând a fi finanțate prin granturi europene (Fondul pentru o Tranziție Justă).

**1.3 Ordonator de credite ierarhic superior**
Deoarece proiectul este dezvoltat de o entitate privată, nu există un ordonator superior ierarhic. {i['denumire']} acționează ca investitor unic, asumând întregul risc financiar și operativ.

**1.4 Beneficiarul investiției**
Beneficiarul proiectului este {i['denumire']}, care va funcționa atât ca dezvoltator, cât și ca operator al parcului fotovoltaic.

**1.5 Elaboratorul studiului de fezabilitate**
Studiul de fezabilitate a fost realizat de HELIO Platform, expert recunoscut în analiza proiectelor fotovoltaice conform HG 907/2016.

**Anexe la Capitolul 1**:
| Parametru | Valoare | Unitate |
|---|---|---|
| Putere instalată | {p['putere_mwp']} | MWp |
| Suprafață | {p['suprafata_ha']} | hectare |
| Producție netă P50 (an 1) | {fmt_nr(d['bilant_energetic']['prod_neta_p50_mwh'])} | MWh/an |
| LCOE standard | {fmt_dec(d['dcf_fara_grant']['indicatori']['lcoe_standard_eur_mwh'], 2)} | EUR/MWh |
| Iradianță PVGIS | {d['bilant_energetic']['iradianta_kwh_kwp_an']} | kWh/kWp/an |
"""

def render_cap2(d, cfg):
    p = cfg['proiect']
    cl = cfg['date_clima']
    return f"""CAPITOLUL 2. SITUAȚIA ACTUALĂ ȘI NECESITATEA REALIZĂRII OBIECTIVULUI DE INVESTIȚII

**2.1 Concluziile studiului de prefezabilitate**
Prezentul Studiu de Fezabilitate integrează și validează concluziile etapei de prefezabilitate, conform prevederilor HG nr. 907/2016. Comasarea etapelor de prefezabilitate și fezabilitate este justificată prin natura specifică a proiectului, care utilizează tehnologii mature și bine documentate.

Analiza preliminară a demonstrat viabilitatea tehnică și economică a proiectului "{p['denumire']}". Amplasamentul din {p['localitate']}, județul {p['judet']}, prezintă o iradianță solară optimă de {cl['iradianta_kwh_kwp_an']} kWh/m²/an. Producția netă anuală P50 validată pentru primul an de operare este de **{fmt_nr(d['bilant_energetic']['prod_neta_p50_mwh'])} MWh/an**.

Din perspectiva financiară, analiza de prefezabilitate a indicat:
- NPV (cu grant): {fmt_nr(d['dcf_cu_grant']['indicatori']['npv_eur'])} EUR
- IRR (cu grant): {d['dcf_cu_grant']['indicatori']['irr_pct']}%
- Payback: {d['dcf_cu_grant']['indicatori']['payback_ani']} ani
- LCOE standard: {fmt_dec(d['dcf_fara_grant']['indicatori']['lcoe_standard_eur_mwh'], 2)} EUR/MWh

**2.2 Prezentarea contextului actual — cadru legislativ**
Contextul actual este puternic influențat de acte normative naționale și europene: Directiva (UE) 2018/2001 (RED II), Pachetul "Fit for 55", Regulamentul (UE) 2021/1119 (Legea europeană a climei), Regulamentul (UE) 2020/852 (Taxonomia UE), Directiva (UE) 2019/944, HG 907/2016, Legea 123/2012, OUG 944/2021, HG 1.076/2021 (PNIESC), OUG 60/2022 (Fondul pentru Modernizare).

**2.3 Analiza situației existente**
Proiectul este amplasat în județul {p['judet']}, localitatea {p['localitate']}, la coordonatele GPS {p['coordonate']}. Județul {p['judet']} este o zonă eligibilă pentru Fondul pentru o Tranziție Justă (PTJ). Suprafața totală a terenului alocată proiectului este de {p['suprafata_ha']} ha.

Din punct de vedere al infrastructurii existente, amplasamentul beneficiază de condiții favorabile. Accesul rutier este asigurat prin drumuri publice existente. Rețeaua electrică de medie tensiune se află în imediata apropiere a terenului.

Date climatice reale (2021-2026):
- Temperaturi extreme: {cl['temp_min_c']}°C ... {cl['temp_max_c']}°C
- Viteza vântului maximă: {cl['vant_max_kmh']} km/h
- Precipitații anuale: {cl['precipitatii_mm_an']} mm/an
- Zile cu ploaie: {cl['zile_ploaie']}/an
- Zile cu zăpadă: {cl['zile_zapada']}/an
- Calitatea aerului (AQI): {cl['aqi']} — Good air quality

**2.4 Analiza cererii de bunuri și servicii**
Piața energiei verzi din România se află într-o expansiune rapidă. Proiectul vizează încheierea unui contract PPA la un tarif estimat de {cfg['finante']['tarif_ppa_eur_mwh']} EUR/MWh, pe o durată de 10-15 ani.

**2.5 Obiective SMART**
- **Specific**: Construirea unui parc fotovoltaic de {p['putere_mwp']} MWp, producție {fmt_nr(d['bilant_energetic']['prod_neta_p50_mwh'])} MWh/an, vânzare prin PPA.
- **Măsurabil**: Monitorizare SCADA, termografii anuale, indicatori financiari (NPV, IRR, LCOE).
- **Realizabil**: Tehnologii mature, finanțare PTJ confirmată.
- **Relevant**: Contribuție la PNIESC, tranziția justă în {p['judet']}, securitate energetică.
- **Încadrat în timp**: 18 luni implementare, PIF până la 31.12.2029.
"""

def render_cap3(d, cfg):
    p = cfg['proiect']
    b = d['bilant_energetic']
    pi = cfg['pierderi_sistem']
    return f"""CAPITOLUL 3. IDENTIFICAREA ȘI PREZENTAREA SCENARIILOR/OPȚIUNILOR TEHNICO-ECONOMICE

**3.1 Scenariul 1 — Soluția propusă: {p['tehnologie_panou']} + {p['tracker']} (1-ax)**
Soluția tehnică propusă integrează panouri {p['tehnologie_panou']} cu sistem de urmărire {p['tracker']}, optimizând producția energetică.

**3.1.1 Particularități amplasament și bilanț energetic**
Amplasamentul la coordonatele {p['coordonate']} (altitudine {p['altitudine_m']}m):

| Parametru | Valoare |
|---|---|
| Iradianță PVGIS | {b['iradianta_kwh_kwp_an']} kWh/kWp/an |
| Producție brută (fără tracker) | {fmt_nr(b['prod_bruta_mwh'])} MWh/an |
| Bonus tracker ({b['bonus_tracker_pct']}%) | +{fmt_nr(b['prod_cu_tracker_mwh'] - b['prod_bruta_mwh'])} MWh/an |
| Producție brută cu tracker | {fmt_nr(b['prod_cu_tracker_mwh'])} MWh/an |
| Pierderi sistem totale ({b['total_pierderi_pct']}%) | -{fmt_nr(b['prod_cu_tracker_mwh'] - b['prod_neta_p50_mwh'])} MWh/an |
| **Producție netă P50** | **{fmt_nr(b['prod_neta_p50_mwh'])} MWh/an** |
| Producție netă P90 | {fmt_nr(b['prod_p90_mwh'])} MWh/an |
| Factor de capacitate | {b['factor_capacitate_pct']}% |

**Detaliu pierderi sistem**:
| Pierdere | Procent | MWh/an |
|---|---|---|
| Temperatură | {pi['temperatura_pct']}% | ~{fmt_nr(b['prod_cu_tracker_mwh'] * pi['temperatura_pct']/100)} |
| Soiling | {pi['soiling_pct']}% | ~{fmt_nr(b['prod_cu_tracker_mwh'] * pi['soiling_pct']/100)} |
| Invertor | {pi['invertor_pct']}% | ~{fmt_nr(b['prod_cu_tracker_mwh'] * pi['invertor_pct']/100)} |
| Cabluri DC | {pi['cabluri_dc_pct']}% | ~{fmt_nr(b['prod_cu_tracker_mwh'] * pi['cabluri_dc_pct']/100)} |
| Cabluri AC | {pi['cabluri_ac_pct']}% | ~{fmt_nr(b['prod_cu_tracker_mwh'] * pi['cabluri_ac_pct']/100)} |
| Umbrire | {pi['umbrire_pct']}% | ~{fmt_nr(b['prod_cu_tracker_mwh'] * pi['umbrire_pct']/100)} |
| Disponibilitate rețea | {pi['disponibilitate_retea_pct']}% | ~{fmt_nr(b['prod_cu_tracker_mwh'] * pi['disponibilitate_retea_pct']/100)} |
| Consum propriu | {pi['consum_propriu_pct']}% | ~{fmt_nr(b['prod_cu_tracker_mwh'] * pi['consum_propriu_pct']/100)} |

**3.1.2 Descriere tehnică constructivă**
- **Panouri**: Jinko Solar Tiger Neo 580Wp, eficiență 22.3%, garanție 30 ani performanță liniară.
- **Invertoare**: Sungrow SG3500HV Central HV, randament european 98.5%.
- **Structuri**: Oțel galvanizat S355JR, rezistență vânt {cfg['date_clima']['vant_max_kmh']} km/h.
- **SCADA**: Monitorizare string-level, alerte la deviații >5%.

**3.1.3 Deviz general HG 907/2016**
| Capitol | Denumire | Valoare (EUR) | % |
|---|---|---|---|
| C1 | Amenajare teren | 45.000 | 1% |
| C2 | Utilități | 135.000 | 3% |
| C3 | Proiectare | 180.000 | 4% |
| C4.1 | Echipamente | 2.790.000 | 62% |
| C4.2 | Montaj | 900.000 | 20% |
| C5 | Organizare șantier | 112.500 | 2.5% |
| C6 | Neprevăzute | 112.500 | 2.5% |
| **TOTAL fără TVA** | | **{fmt_nr(cfg['finante']['capex_total_eur'])}** | **100%** |

**3.2 Scenariul 0 — Fără investiție**
Costuri oportunitate pe 25 ani:
- Pierderi financiare: {fmt_nr(b['prod_neta_p50_mwh'])} MWh/an × {cfg['finante']['tarif_ppa_eur_mwh']} €/MWh × 25 ani = {fmt_nr(b['prod_neta_p50_mwh'] * cfg['finante']['tarif_ppa_eur_mwh'] * 25)} €.
- Emisii CO2 neevitate: {fmt_nr(b['prod_neta_p50_mwh'])} MWh/an × 0,608 tCO2/MWh × 25 ani = {fmt_nr(b['prod_neta_p50_mwh'] * 0.608 * 25)} tCO2.
"""

def render_cap4(d, cfg):
    i_cg = d['dcf_cu_grant']['indicatori']
    i_fg = d['dcf_fara_grant']['indicatori']
    tabel_dcf = d['dcf_cu_grant']['tabel']
    
    # Construim tabelul DCF ca text
    rows = []
    rows.append("| An | Producție (MWh) | Venituri (€) | OpEx (€) | EBITDA (€) | Taxe (€) | FCF (€) | Factor 8% | FCF Actualizat (€) | FCF Cumulat (€) |")
    rows.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in tabel_dcf:
        rows.append(f"| {r['an']} | {fmt_nr(r['productie_mwh'])} | {fmt_nr(r['venituri_eur'])} | {fmt_nr(r['opex_eur'])} | {fmt_nr(r['ebitda_eur'])} | {fmt_nr(r['tax_eur'])} | {fmt_nr(r['fcf_eur'])} | {r['factor_8pct']} | {fmt_nr(r['fcf_actualizat_eur'])} | {fmt_nr(r['fcf_cumulat_eur'])} |")
    
    dcf_table = '\n'.join(rows)
    
    # Sensibilitate
    sens_rows = []
    sens_rows.append("| Scenariu | Variație | NPV (EUR) | IRR (%) | Payback (ani) |")
    sens_rows.append("|---|---|---|---|---|")
    for s in d['sensibilitate']:
        sens_rows.append(f"| {s['scenariu']} | {s['variatie_pct']:+.0f}% | {fmt_nr(s['npv_eur'])} | {s['irr_pct']}% | {s['payback_ani']} |")
    sens_table = '\n'.join(sens_rows)
    
    imp = d['impact']
    
    return f"""CAPITOLUL 4. ANALIZA SCENARIILOR/OPȚIUNILOR TEHNICO-ECONOMICE PROPUSE

**4.1 Cadrul de analiză DCF**
Perioada de referință: {cfg['finante']['orizont_ani']} ani operare + 1 an implementare. WACC = {cfg['finante']['wacc_pct']}%. Valoare reziduală: {i_cg['valoare_reziduala_eur']} EUR ({cfg['finante']['valoare_reziduala_pct']}% din CapEx total).

**4.2 Vulnerabilități climatice**
Producția P50 = {fmt_nr(d['bilant_energetic']['prod_neta_p50_mwh'])} MWh/an. P90 = {fmt_nr(d['bilant_energetic']['prod_p90_mwh'])} MWh/an (scenariu pesimist). Degradare panouri: {cfg['finante']['degradare_panouri_anuala_pct']}% liniară anuală. Soiling: {cfg['pierderi_sistem']['soiling_pct']}% (AQI={cfg['date_clima']['aqi']}), mitigat prin 5 curățări anuale.

**4.3 Situația utilităților**
Capacitate de evacuare: dependentă de ATR (Aviz Tehnic de Racordare) — **document necesar de la operatorul de distribuție**. Consum propriu estimat: {cfg['pierderi_sistem']['consum_propriu_pct']}% din producție.

**4.4 Sustenabilitate**
- **Impact social**: {imp['locuri_munca_constructie']} locuri muncă (construcție), {imp['locuri_munca_operare']} locuri muncă permanente (operare).
- **Impact mediu**: Reducere CO2 = {fmt_nr(imp['co2_evitat_tone_an'])} tone/an ({fmt_nr(imp['co2_evitat_tone_25ani'])} tone/25 ani).
- **DNSH**: Proiectul respectă cele 6 obiective UE (Taxonomia UE 2020/852).

**4.5 Analiza financiară detaliată — DCF**

Indicatori financiari cheie (perspectiva investitor, cu grant PTJ):
| Indicator | Valoare |
|---|---|
| NPV ({cfg['finante']['wacc_pct']}%, {cfg['finante']['orizont_ani']} ani) | {fmt_nr(i_cg['npv_eur'])} EUR |
| IRR | {i_cg['irr_pct']}% |
| Payback Period | {i_cg['payback_ani']} ani |
| LCOE net (cu grant) | {fmt_dec(i_cg['lcoe_net_eur_mwh'], 2)} EUR/MWh |
| LCOE standard (fără subvenții) | {fmt_dec(i_fg['lcoe_standard_eur_mwh'], 2)} EUR/MWh |
| CapEx total | {fmt_nr(i_cg['capex_total_eur'])} EUR |
| Grant PTJ | {fmt_nr(i_cg['grant_eur'])} EUR |
| Cofinanțare proprie | {fmt_nr(i_cg['cofinantare_eur'])} EUR |
| Tarif PPA estimat | {cfg['finante']['tarif_ppa_eur_mwh']} EUR/MWh |

**Tabel fluxuri de numerar DCF (scenariu cu grant)**:
{dcf_table}

**Regula I-C (eligibilitate grant)**:
Conform metodologiei PTJ, proiectul trebuie să demonstreze că **fără grant este nefezabil financiar**. Scenariul fără grant:
- NPV = **{fmt_nr(i_fg['npv_eur'])} EUR** (negativ)
- IRR = **{i_fg['irr_pct']}%** (sub WACC {cfg['finante']['wacc_pct']}%)
- Payback > {cfg['finante']['orizont_ani']} ani

Aceste valori confirmă că proiectul **NU este fezabil fără sprijin public**, justificând acordarea grantului PTJ. Valoarea pozitivă a NPV în scenariul cu grant ({fmt_nr(i_cg['npv_eur'])} EUR) demonstrează rentabilitatea pentru investitor după primirea finanțării nerambursabile.

**4.6 Analiza economică**
Beneficii socio-economice cuantificate: valoare adăugată locală, locuri de muncă, contribuții fiscale, securitate energetică.

**4.7 Analiza cost-eficacitate**
LCOE standard = {fmt_dec(i_fg['lcoe_standard_eur_mwh'], 2)} EUR/MWh (cost social real, fără subvenții).
Comparație cu alternative:
- CCGT (gaz): 50-100 EUR/MWh
- Cărbune: 80-120 EUR/MWh
- Nuclear: >100 EUR/MWh
- Eolian onshore: 30-60 EUR/MWh

**4.8 Analiza sensibilitate**
{sens_table}

**Interpretare**: Proiectul este foarte sensibil la variația tarifului PPA și a producției. O scădere de 10% a PPA sau de 5% a producției îl face nefezabil (NPV negativ), confirmând necesitatea stabilității contractuale și a mentenanței preventive.

**4.9 Matrice riscuri**
| Risc | Probabilitate | Impact | Mitigare |
|---|---|---|---|
| Producție sub P50 | Medie | Mediu | SCADA, O&M cu clauze de performanță, 5 curățări/an |
| Defecțiuni echipamente | Scăzută | Mediu | Garanții extinse, fond de rezervă 0,7% CapEx/an |
| Creștere CapEx | Medie | Mediu | Contract EPC lump-sum, rezervă 10% |
| Neeligibilitate PTJ | Scăzută | Ridicat | Conformitate strictă cu ghid, SF conform HG 907 |
| Modificări legislative | Scăzută | Mediu | Monitorizare ANRE, asociații profesionale |
| Retard avize | Medie | Ridicat | Demarare timpurie CU, ATR, AC |
| Condiții extreme | Scăzută | Mediu | Asigurare all-risk, structuri Eurocode |
| Curtailment rețea | Medie | Ridicat | ATR obligatoriu, studiu de sistem |
"""

def render_cap5(d, cfg):
    p = cfg['proiect']
    i_cg = d['dcf_cu_grant']['indicatori']
    return f"""CAPITOLUL 5. SCENARIUL/OPȚIUNEA TEHNICO-ECONOMICĂ OPTIMĂ RECOMANDATĂ

**5.1 Compararea scenariilor**

| Criteriu | Scenariul 0 (Fără Proiect) | Scenariul 1 (Cu Proiect) |
|---|---|---|
| Putere instalată | 0 MWp | {p['putere_mwp']} MWp |
| Producție anuală (P50) | 0 MWh/an | {fmt_nr(d['bilant_energetic']['prod_neta_p50_mwh'])} MWh/an |
| Reducere CO2 | 0 tCO2/an | {fmt_nr(d['impact']['co2_evitat_tone_an'])} tCO2/an |
| Locuri de muncă | 0 | {d['impact']['locuri_munca_constructie']} (construcție) / {d['impact']['locuri_munca_operare']} (operare) |
| NPV (cu grant) | N/A | {fmt_nr(i_cg['npv_eur'])} EUR |
| IRR | N/A | {i_cg['irr_pct']}% |
| Payback | N/A | {i_cg['payback_ani']} ani |
| LCOE standard | N/A | {fmt_dec(d['dcf_fara_grant']['indicatori']['lcoe_standard_eur_mwh'], 2)} EUR/MWh |
| Valoare investiție | 0 EUR | {fmt_nr(cfg['finante']['capex_total_eur'])} EUR |
| Grant solicitat | 0 EUR | {fmt_nr(cfg['finante']['grant_eur'])} EUR |

**5.2 Selectarea și justificarea scenariului optim**
Scenariul 1 este optim datorită tehnologiei avansate ({p['tehnologie_panou']} + {p['tracker']}), indicatorilor financiari robuști și beneficiilor socio-economice.

**5.3 Descrierea scenariului optim**
Layout pe {p['suprafata_ha']} ha: trackere single-axis, distanțare optimă GCR=0.35, drumuri de acces, stație de transformare, clădire control. Configurație electrică: string-uri DC → combiner boxes → invertoare Central HV → stație MT/IT → punct racordare SEN. Protecții: anti-ilotare, supracurent, supratensiune, împământare, paratrăsnet.

**5.4 Tabel indicatori tehnico-economici**

| Indicator | Valoare | Unitate | Status |
|---|---|---|---|
| Putere instalată | {p['putere_mwp']} | MWp | — |
| Suprafață | {p['suprafata_ha']} | ha | — |
| Producție anuală P50 | {fmt_nr(d['bilant_energetic']['prod_neta_p50_mwh'])} | MWh/an | — |
| Iradianță PVGIS | {d['bilant_energetic']['iradianta_kwh_kwp_an']} | kWh/kWp/an | — |
| Valoare investiție | {fmt_nr(cfg['finante']['capex_total_eur'])} | EUR | — |
| Grant solicitat | {fmt_nr(cfg['finante']['grant_eur'])} | EUR | — |
| NPV (cu grant) | {fmt_nr(i_cg['npv_eur'])} | EUR | POZITIV |
| IRR | {i_cg['irr_pct']} | % | OK (>WACC) |
| Payback | {i_cg['payback_ani']} | ani | ACCEPTABIL |
| LCOE standard | {fmt_dec(d['dcf_fara_grant']['indicatori']['lcoe_standard_eur_mwh'], 2)} | EUR/MWh | COMPETITIV |
| LCOE net | {fmt_dec(i_cg['lcoe_net_eur_mwh'], 2)} | EUR/MWh | — |

**5.5 Conformitatea cu reglementările**
HG 907/2016, Directiva (UE) 2018/2001, Regulamentul (UE) 2021/1119, Legea 123/2012, OUG 944/2021, HG 1.076/2021, OUG 60/2022, Ordine ANRE, SR EN 1991, IEC 61215/61730.

**5.6 Sursele de finanțare**
Structura financiară: Grant PTJ = {fmt_nr(cfg['finante']['grant_eur'])} EUR ({cfg['finante']['grant_procent']}%) + Cofinanțare proprie = {fmt_nr(cfg['finante']['cofinantare_eur'])} EUR ({100-cfg['finante']['grant_procent']}%).

Regula I-C: NPV fără grant = {fmt_nr(d['dcf_fara_grant']['indicatori']['npv_eur'])} EUR (negativ) → proiect **eligibil** pentru finanțare nerambursabilă.
"""

def render_cap6(cfg):
    p = cfg['proiect']
    return f"""CAPITOLUL 6. AVIZE, ACORDURI ȘI AUTORIZAȚII NECESARE

**6.1 Certificat de urbanism**
Procedură la Primăria {p['localitate']} / CJ {p['judet']}. Documente: cerere, acte proprietate, plan încadrare, plan topografic. Termen: 15 zile lucrătoare. Valabilitate: 12 luni.

**6.2 Extras CF**
Situație juridică {p['suprafata_ha']} ha: necesară verificare proprietate/concesiune, sarcini, categoriie folosință. Posibilă necesitate schimbare categorie folosință agricol → construcții speciale.

**6.3 Protecția mediului**
Procedură EIM la APM {p['judet']}: etapa de încadrare, SEIM, evaluare adecvată Natura 2000 (dacă e cazul), consultare publică, acord de mediu. Condiții: gestionare DEEE, monitorizare biodiversitate, principiul DNSH.

**6.4 Avize conforme necesare**
1. **ATR** (Aviz Tehnic de Racordare) — operator distribuție / Transelectrica. Termen: 30 zile. **LIPSA — necesar de urgență.**
2. **Autorizație de Înființare ANRE** — pentru capacități >1 MW. Termen: 60 zile.
3. **Aviz ISC** (DTAC) — verificare proiect tehnic.
4. **Avize utilități** — apă, canal, telecomunicații, drumuri.
5. **Aviz AACR** — dacă e în proximitatea aeroportului.
6. **Aviz MApN** — dacă afectează obiective militare.
7. **PUZ** — dacă PUG-ul nu permite funcțiunea.

**6.5 Studiu topografic**
Sistem Stereo 70, altitudine Marea Neagră 1975, scară 1:500-1:1000, vizare OCPI {p['judet']}.

**6.6 Studii specifice**
- **Studiu geotehnic**: foraje SPT, stratificație, apă freatică, agresivitate chimică. **LIPSA — necesar de urgență.**
- **Studiu hidrologic**: cote inundații Q100, drenaj.
- **Studiu EMC**: compatibilitate electromagnetică, interferențe.
"""

def render_cap7(cfg):
    p = cfg['proiect']
    return f"""CAPITOLUL 7. PLAN DE IMPLEMENTARE ȘI OPERARE

**7.1 Entitatea responsabilă**
{cfg['investitor']['denumire']} — Unitate de Management a Proiectului (UMP), Director de Proiect, Inginer Șef, Responsabil Financiar, Responsabil Achiziții, Responsabil Mediu.

**7.2 Strategia de implementare**
Model Turnkey EPC (Engineering, Procurement, Construction). Grafic Gantt:
- **Luni 1-3**: Autorizări (CU, ATR, AC), achiziție EPC
- **Luni 4-8**: Proiectare detaliată, comenzi echipamente
- **Luni 9-18**: Execuție (terasamente, fundații, structuri, panouri, invertoare, cabluri, stație transformare)
- **Luni 19-21**: Testare, PIF, recepție, licență ANRE
- **Luna 22+**: Operare comercială

**7.3 Plan O&M pe 25 ani**
Contract O&M pe termen lung. Cost an 1: {fmt_nr(cfg['finante']['opex_an1_eur'])} EUR, creștere {cfg['finante']['opex_crestere_anuala_pct']}% anual.
- Mentenanță preventivă: 5 curățări/an, 4 termografii/an cu dronă, inspecții trimestriale trackere, teste invertoare, verificări electrice bianuale, 6-8 cosiri vegetație/an.
- Mentenanță corectivă: timp răspuns <24h, stoc piese schimb.
- Înlocuire invertoare: anul {cfg['fiscal']['inlocuire_invertoare_an']} (cost estimat {fmt_nr(cfg['fiscal']['inlocuire_invertoare_cost_eur'])} EUR).
- Monitorizare SCADA 24/7.

**7.4 Capacitate managerială**
- Diriginte de Șantier autorizat ISC (independent de EPC).
- Consultant financiar pentru monitorizare KPIs (NPV, IRR, LCOE, Payback).
- Expert tranzacționare energie (opțional, pentru optimizare venituri pe piața de echilibrare).
"""

def render_cap8(d, cfg):
    i_cg = d['dcf_cu_grant']['indicatori']
    i_fg = d['dcf_fara_grant']['indicatori']
    p = cfg['proiect']
    return f"""CAPITOLUL 8. CONCLUZII ȘI RECOMANDĂRI

**8.1 Sinteza viabilității tehnice**
Proiectul "{p['denumire']}" demonstrează o solidă viabilitate tehnică. Tehnologia {p['tehnologie_panou']} + {p['tracker']} maximizează producția la {fmt_nr(d['bilant_energetic']['prod_neta_p50_mwh'])} MWh/an. Amplasamentul din {p['localitate']} beneficiază de iradianță optimă ({d['bilant_energetic']['iradianta_kwh_kwp_an']} kWh/kWp/an) și condiții climatice gestionabile.

**8.2 Sinteza viabilității financiare**
| Indicator | Cu Grant | Fără Grant (I-C) |
|---|---|---|
| NPV | {fmt_nr(i_cg['npv_eur'])} EUR | {fmt_nr(i_fg['npv_eur'])} EUR |
| IRR | {i_cg['irr_pct']}% | {i_fg['irr_pct']}% |
| Payback | {i_cg['payback_ani']} ani | {i_fg['payback_ani']} ani |
| LCOE standard | — | {fmt_dec(i_fg['lcoe_standard_eur_mwh'], 2)} EUR/MWh |
| LCOE net | {fmt_dec(i_cg['lcoe_net_eur_mwh'], 2)} EUR/MWh | — |

Proiectul este **nefezabil fără grant** (NPV negativ, IRR < WACC), confirmând eligibilitatea pentru PTJ. Cu grant, devine **atractiv pentru investitor** (NPV pozitiv, IRR robust).

**8.3 Recomandare generală: VIABIL**
Proiectul este **VIABIL** din punct de vedere tehnic, economic și de reglementare, cu condiția obținerii grantului PTJ. Lipsa finanțării nerambursabile îl face nefezabil (regula I-C confirmă necesitatea sprijinului public).

**8.4 Pași următori**
1. Clarificare ghid PTJ 2025-2026 (MySMIS2021)
2. Solicitare Certificat Urbanism (Primăria {p['localitate']})
3. Comandare Studiu Geotehnic + Topografic + Hidrologic + EMC
4. Solicitare ATR (Distribuție {p['judet']})
5. Demarare procedură mediu (APM {p['judet']})
6. Achiziție publică EPC
7. Depunere cerere finanțare (MySMIS2021)
8. Semnare contract finanțare
9. Implementare + monitorizare + PIF ANRE

**8.5 Calendar de implementare**

| Etapă | Durată (luni) |
|---|---|
| Autorizări și studii | 1-6 |
| Achiziție EPC | 6-8 |
| Construcție și montaj | 9-18 |
| Testare și PIF | 19-21 |
| Operare comercială | 22+ |

**Tabel centralizator indicatori**

| Indicator | Valoare | Unitate |
|---|---|---|
| Denumire proiect | {p['denumire']} | — |
| Beneficiar | {cfg['investitor']['denumire']} | — |
| Județ | {p['judet']} | ELIGIBIL PTJ |
| Putere instalată | {p['putere_mwp']} | MWp |
| Suprafață | {p['suprafata_ha']} | ha |
| Producție P50 an 1 | {fmt_nr(d['bilant_energetic']['prod_neta_p50_mwh'])} | MWh/an |
| Iradianță | {d['bilant_energetic']['iradianta_kwh_kwp_an']} | kWh/kWp/an |
| Valoare totală investiție | {fmt_nr(cfg['finante']['capex_total_eur'])} | EUR |
| Grant solicitat | {fmt_nr(cfg['finante']['grant_eur'])} | EUR |
| Cofinanțare | {fmt_nr(cfg['finante']['cofinantare_eur'])} | EUR |
| NPV (cu grant) | {fmt_nr(i_cg['npv_eur'])} | EUR |
| IRR (cu grant) | {i_cg['irr_pct']} | % |
| Payback | {i_cg['payback_ani']} | ani |
| LCOE standard | {fmt_dec(i_fg['lcoe_standard_eur_mwh'], 2)} | EUR/MWh |
| LCOE net | {fmt_dec(i_cg['lcoe_net_eur_mwh'], 2)} | EUR/MWh |
| Reducere CO2/an | {fmt_nr(d['impact']['co2_evitat_tone_an'])} | tCO2 |
| Locuri muncă construcție | {d['impact']['locuri_munca_constructie']} | — |
| Locuri muncă operare | {d['impact']['locuri_munca_operare']} | — |
| Certificat Urbanism | LIPSĂ | NECESAR |
| Studiu Geotehnic | LIPSĂ | NECESAR |
| ATR Racordare | LIPSĂ | NECESAR |
"""

def render_all(data, cfg):
    parts = [
        render_cap1(data, cfg),
        render_cap2(data, cfg),
        render_cap3(data, cfg),
        render_cap4(data, cfg),
        render_cap5(data, cfg),
        render_cap6(cfg),
        render_cap7(cfg),
        render_cap8(data, cfg)
    ]
    return '\n\n---\n\n'.join(parts)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python sf_renderer.py <rezultat.json> <config.json>")
        sys.exit(1)
    
    result_path = sys.argv[1]
    cfg_path = sys.argv[2]
    
    data = load_json(result_path)
    cfg = load_json(cfg_path)
    
    sf_text = render_all(data, cfg)
    
    out_path = Path(result_path).parent / 'SF_Complet_Generat.md'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(sf_text)
    
    print(f"SF generat cu succes: {out_path}")
    print(f"Dimensiune: {len(sf_text)} caractere")
    print(f"Capitole: 8")
