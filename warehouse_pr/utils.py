from warehouse_pr.catalog.models import Category, Nomenclature
from warehouse_pr.inventory.models import NomenclatureRemain


def barcode_db_check(barcode: int) -> Nomenclature:
    if Nomenclature.objects.get(barcode=barcode).exists():
        return Nomenclature.objects.get(barcode=barcode)


def remainings_db_check(nomenclature: Nomenclature):
    return NomenclatureRemain.objects.get(nomenclature=nomenclature).exists()


def remains_init(barcode: int):
    nomenclature = barcode_db_check(barcode)
    if nomenclature and remainings_db_check(nomenclature):
        quantity = NomenclatureRemain.objects.get_or_create(
            nomenclature).quantity
        return quantity
