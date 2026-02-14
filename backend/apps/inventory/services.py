from .models import CavaleteHistory, SlotHistory, Action
from apps.cavaletes.models import Slot


def create_cavalete_structure(cavalete, slots_a: int, slots_b: int):
    """
    Gera automaticamente os slots para um cavalete recém-criado.
    slots_a: Quantidade de slots no Lado A.
    slots_b: Quantidade de slots no Lado B.
    """
    new_slots = []

    for i in range(1, slots_a + 1):
        new_slots.append(
            Slot(
                cavalete=cavalete,
                side=Slot.Side.SIDE_A,
                number=i,
                status=Slot.Status.AVAILABLE,
            )
        )

    for i in range(1, slots_b + 1):
        new_slots.append(
            Slot(
                cavalete=cavalete,
                side=Slot.Side.SIDE_B,
                number=i,
                status=Slot.Status.AVAILABLE,
            )
        )

    Slot.objects.bulk_create(new_slots)


def log_cavalete_action(cavalete, user, action, description=""):
    """Registra uma ação no histórico do cavalete."""
    CavaleteHistory.objects.create(
        cavalete=cavalete, user=user, action=action, description=description
    )


def log_slot_action(slot, user, action, description="", old_data=None, new_data=None):
    """
    Registra uma ação no histórico do slot.
    old_data/new_data: dicts com product_code e quantity
    """
    old_product = old_data.get("product_code") if old_data else None
    old_qty = old_data.get("quantity") if old_data else None

    new_product = new_data.get("product_code") if new_data else None
    new_qty = new_data.get("quantity") if new_data else None

    SlotHistory.objects.create(
        slot=slot,
        user=user,
        action=action,
        description=description,
        old_product_code=old_product,
        old_quantity=old_qty,
        new_product_code=new_product,
        new_quantity=new_qty,
    )
