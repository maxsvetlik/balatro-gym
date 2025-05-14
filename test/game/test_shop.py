import pytest

from balatro_gym.cards.voucher import ALL_VOUCHERS
from balatro_gym.game.shop import Shop, ShopState


@pytest.mark.unit
def test_generate_shop_state() -> None:
    shop = Shop()
    state = shop.generate_shop_state(1)
    voucher = state.vouchers[0]
    assert isinstance(state, ShopState)
    state = shop.generate_shop_state(2)
    # Make sure we use the same voucher for the entire ante
    assert state.vouchers[0] == voucher

    # We should have a new voucher
    assert any([shop.generate_shop_state(4).vouchers[0] != voucher for _ in range(5)])
    bought_vouchers = [v for v in ALL_VOUCHERS if v.dependency is None]
    shop.bought_vouchers = bought_vouchers
    state = shop.generate_shop_state(4)
    # Verify we don't include any of the vouchers that have been bought
    assert state.vouchers[0] not in bought_vouchers
