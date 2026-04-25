from django.db import models


# =========================
# BANK
# =========================
class Bank(models.Model):
    name = models.CharField(max_length=100)
    is_pks = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# =========================
# PRODUCT
# =========================
class Product(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# =========================
# BANK PRODUCT SUPPORT
# =========================
class BankProduct(models.Model):
    bank = models.ForeignKey("Bank", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    description = models.TextField(blank=True, null=True)

    # =========================
    # V3: LIMITS
    # =========================
    min_tenor = models.IntegerField(blank=True, null=True)
    max_tenor = models.IntegerField(blank=True, null=True)

    min_plafond = models.BigIntegerField(blank=True, null=True)
    max_plafond = models.BigIntegerField(blank=True, null=True)

    max_age_end = models.IntegerField(
        blank=True,
        null=True,
        help_text="Maksimal usia saat kredit lunas (umur + tenor)"
    )

    min_lama_usaha = models.IntegerField(blank=True, null=True,
        help_text="Minimal lama usaha (dalam tahun)"
    )

    def __str__(self):
        return f"{self.bank.name} - {self.product.name}"


# =========================
# RULE CATEGORY
# =========================
class RuleCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# =========================
# RULE (MASTER)
# =========================
class Rule(models.Model):
    category = models.ForeignKey(RuleCategory, on_delete=models.CASCADE)
    key = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category.name} - {self.key}"



# =========================
# BANK RULE
# =========================
class BankRule(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)

    # OPTIONAL → only if rule is product-specific
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

    # OPTIONAL description
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.bank} - {self.rule}"
