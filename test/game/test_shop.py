import pytest

from balatro_gym.cards.voucher import ALL_VOUCHERS
from balatro_gym.game.shop import Shop, ShopState
from balatro_gym.interfaces import Booster


@pytest.mark.unit
def test_generate_shop_state() -> None:
    shop = Shop()
    state = shop.generate_shop_state(1)
    voucher = state.vouchers[0]
    assert isinstance(state, ShopState)
    assert all([isinstance(pack, Booster) for pack in state.booster_packs])
    assert len(state.booster_packs) == shop.num_booster_packs
    state = shop.generate_shop_state(2)
    # Make sure we use the same voucher for the entire ante
    assert state.vouchers[0] == voucher
    shop.buy_voucher(voucher)
    state = shop.generate_shop_state(3)
    assert len(state.vouchers) == 0
    # We should have a new voucher
    assert any([shop.generate_shop_state(4).vouchers[0] != voucher for _ in range(5)])


@pytest.mark.unit
def test_dependent_vouchers() -> None:
    shop = Shop()
    vouchers_to_buy = set([v for v in ALL_VOUCHERS if v.dependency is None])
    for v in vouchers_to_buy:
        shop.buy_voucher(v)
    state = shop.generate_shop_state(4)
    # Verify we don't include any of the vouchers that have been bought
    assert state.vouchers[0] not in vouchers_to_buy
