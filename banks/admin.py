from django.contrib import admin
from .models import Bank, Product, BankProduct, RuleCategory, Rule, BankRule


# =========================
# INLINE: Products inside Bank
# =========================
class BankProductInline(admin.TabularInline):
    model = BankProduct
    extra = 1
    can_delete = True


# =========================
# INLINE: Rules inside Bank
# =========================
class BankRuleInline(admin.TabularInline):
    model = BankRule
    extra = 1
    autocomplete_fields = ['rule', 'product']
    can_delete = True


# =========================
# BANK ADMIN (MAIN PAGE)
# =========================
@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

    inlines = [BankProductInline, BankRuleInline]


# =========================
# PRODUCT ADMIN
# =========================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name']


# =========================
# RULE CATEGORY ADMIN
# =========================
@admin.register(RuleCategory)
class RuleCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


# =========================
# RULE ADMIN
# =========================
@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ['category', 'key']
    list_filter = ['category']
    search_fields = ['key']


# =========================
# BANK PRODUCT ADMIN
# =========================
@admin.register(BankProduct)
class BankProductAdmin(admin.ModelAdmin):
    list_display = ['bank', 'product']
    list_filter = ['bank', 'product']


# =========================
# BANK RULE ADMIN
# =========================
@admin.register(BankRule)
class BankRuleAdmin(admin.ModelAdmin):
    list_display = ['bank', 'rule', 'product']
    list_filter = ['bank', 'rule__category']
    search_fields = ['bank__name', 'rule__key']
