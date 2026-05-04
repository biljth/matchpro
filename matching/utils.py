from banks.models import Bank, BankRule, BankProduct
from django.db.models import Q


# =========================
# CLIENT → FEATURES
# =========================
def get_client_features(client):
    features = []

    # PRODUCT
    features.append(f"PRODUCT_{client.jenis_pinjaman}")

    # PROFILE
    features.append(f"PROFILE_{client.pekerjaan}")
    # features.append(f"JOBSTATUS_{client.status_pekerjaan}")

    # COLLATERAL
    features.append(f"COLLATERAL_{client.jaminan}")

    # SLIK
    features.append(f"SLIK_{client.status_slik}")

    # FAST APPROVAL
    features.append(f"APPROVAL_{client.instant_approval}")

    # FINANCE
    features.append(f"FINANCE_{client.sumber_penghasilan}")

    # COMPANY
    features.append(f"COMPANY_{client.bentuk_perusahaan}")

    return features


# =========================
# MAIN MATCHING ENGINE
# =========================
def match_banks_dynamic(client):

    client_features = get_client_features(client)

    banks = Bank.objects.all()
    results = []

    for bank in banks:

        score = 0
        reasons = []
        rejected = False

        # =========================
        # 1. PRODUCT FILTER
        # =========================
        if not BankProduct.objects.filter(
            bank=bank,
            product__name=client.jenis_pinjaman
        ).exists():
            continue

        # =========================
        # PRODUCT DESCRIPTION
        # =========================
        bank_product = BankProduct.objects.filter(
            bank=bank,
            product__name=client.jenis_pinjaman
        ).first()

        # TENOR
        if bank_product.min_tenor and client.tenor < bank_product.min_tenor:
            reasons.append(f"⚠ Tenor terlalu pendek (min {bank_product.min_tenor} tahun)")
            continue

        if bank_product.max_tenor and client.tenor > bank_product.max_tenor:
            reasons.append(f"⚠ Tenor terlalu panjang (max {bank_product.max_tenor} tahun)")
            continue

        # =========================
        # V3: AGE vs TENOR
        # =========================
        if client.umur and client.tenor:
            umur_akhir = client.umur + (client.tenor / 12)

            # if bank_product.max_age_end and umur_akhir > bank_product.max_age_end:
            #     reasons.append(
            #         f"⚠ Umur akhir {umur_akhir:.1f} tahun melebihi batas bank ({bank_product.max_age_end})"
            #     )
            #     continue

        # PLAFOND
        if bank_product.min_plafond and client.jumlah_pinjaman < bank_product.min_plafond:
            reasons.append(f"⚠ Plafond terlalu kecil (min {bank_product.min_plafond:,})")
            continue

        if bank_product.max_plafond and client.jumlah_pinjaman > bank_product.max_plafond:
            reasons.append(f"⚠ Plafond terlalu besar (max {bank_product.max_plafond:,})")
            continue

        # =========================
        # 2. GET BANK RULES
        # =========================
        bank_rules = BankRule.objects.filter(bank=bank)

        bank_features = set()
        rule_descriptions = {}

        for r in bank_rules:
            key = f"{r.rule.category.name}_{r.rule.key}"
            bank_features.add(key)

            # ONLY store description if exists
            if r.description:
                rule_descriptions[key] = r.description

        # =========================
        # 3. HARD FILTER
        # =========================

        # 🔥 FINANCE
        finance_rules = BankRule.objects.filter(
            bank=bank,
            rule__category__name="INCOME"
        )

        if client.sumber_penghasilan != "GAJI_TRANSFER":

            if not finance_rules.exists():
                rejected = True
                continue

            if not finance_rules.filter(
                rule__key=client.sumber_penghasilan
            ).exists():
                rejected = True
                continue
        
        if bank_product.min_lama_usaha and client.lama_usaha < bank_product.min_lama_usaha:
            reasons.append(
                f"❌ Lama Usaha minimal {bank_product.min_lama_usaha} tahun"
            )
            score -= 20
        
        # =========================
        # 🔥 COMPANY TYPE (HARD FILTER)
        # =========================
        if client.tipe_client == "PERUSAHAAN" and client.bentuk_perusahaan != "PT":
       
            company_rules = BankRule.objects.filter(
                bank=bank,
                rule__category__name="COMPANY"
            )

            # Kalau bank ga punya rule company sama sekali → reject
            if not company_rules.exists():
                rejected = True
                continue

            # Kalau bentuk perusahaan client tidak ada di rule bank → reject
            if not company_rules.filter(
                rule__key=client.bentuk_perusahaan
            ).exists():
                rejected = True
                continue


        # =========================
        # FEATURE FILTER
        # =========================
        is_perusahaan = client.tipe_client == "PERUSAHAAN"

        for feature in client_features:
            category = feature.split("_")[0]

            # =========================
            # PROFILE (SKIP for perusahaan)
            # =========================
            if category == "PROFILE":

                if is_perusahaan:

                    # 🔥 ONLY allow banks that support BADAN USAHA
                    if "PROFILE_BADAN_USAHA" not in bank_features:
                        rejected = True
                        break

                    continue  # skip other profile checks

                # =========================
                # PERORANGAN LOGIC
                # =========================
                else:
                    if not client.status_pekerjaan:
                        continue

                    if feature == f"PROFILE_{client.status_pekerjaan}":
                        if client.status_pekerjaan.lower() == "tetap":
                            continue

                    if feature not in bank_features:
                        rejected = True
                        break

            # =========================
            # COLLATERAL
            # =========================
            elif category == "COLLATERAL":

                if feature not in bank_features:
                    rejected = True
                    break
            
            # elif category == "COMPANY":

            #     if feature not in bank_features:
            #         rejected = True
            #         break

            # =========================
            # SLIK, APPROVAL (SKIP for perusahaan)
            # =========================
            elif category == "SLIK":

                if is_perusahaan:
                    continue

                if not client.status_slik:
                    continue

                slik_value = client.status_slik.lower()

                if slik_value in ["-", "kol1", "kol2"]:
                    continue

                if feature not in bank_features:
                    rejected = True
                    break
            
            elif category == "APPROVAL":

                if is_perusahaan:
                    continue

                if not client.instant_approval:
                    continue

                fast_approval = client.instant_approval.lower()
                
                if fast_approval in ["tidak"]:
                    continue

                if feature not in bank_features:
                    rejected = True
                    break


        if rejected:
            continue

        # =========================
        # 4. BASE SCORE
        # =========================
        score += 30

        if bank_product and bank_product.description:
            reasons.append(f"✔ Produk sesuai → {bank_product.description}") 

        else:
            reasons.append(f'✔ Produk sesuai')

        if client.tipe_client == "PERUSAHAAN" and client.bentuk_perusahaan:
            reasons.append(f"✔ Bentuk Perusahaan → {client.bentuk_perusahaan.replace('_', ' ').title()}")

        # =========================
        # 5. MATCHING + DESCRIPTION
        # =========================
        for feature in client_features:

            if feature in bank_features:

                category = feature.split("_")[0]
                desc = rule_descriptions.get(feature)

                # BUILD CLEAN LABEL
                label = feature.replace("_", " ").title()

                # ADD DESCRIPTION ONLY IF EXISTS
                if desc:
                    reasons.append(f"✔ {label} → {desc}")
                elif category == "COMPANY":
                    continue
                else:
                    reasons.append(f"✔ {label}")

                # SCORING
                if category == "COLLATERAL":
                    score += 20
                elif category == "PROFILE":
                    score += 20
                elif category == "SLIK":
                    score += 15
                elif category == "APPROVAL":
                    score += 10
                elif category == "FINANCE":
                    score += 10
                elif category == "COMPANY":
                    score += 15


        if bank_product.bank.is_pks:
            score += 20
            # reasons.append("Bank PKS")

        # =========================
        # 6. SPECIAL RULES (FILTERED BY PRODUCT)
        # =========================
        special_rules = BankRule.objects.filter(
            bank=bank,
            rule__category__name="SPECIAL"
        ).filter(
            Q(product__name=client.jenis_pinjaman) |
            Q(product__isnull=True)
        )

        for sr in special_rules:
            if sr.description:
                reasons.append(f"⚠ {sr.description}")
        
        

        # =========================
        # 7. SAVE RESULT
        # =========================
        results.append({
            "bank": bank.name,
            "score": score,
            "reasons": reasons,
            "is_pks": bank_product.bank.is_pks,
        })

    return sorted(results, key=lambda x: x['score'], reverse=True)

