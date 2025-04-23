# A Gymnasium interface for Balatro

**Status:** pre-release

This package will provide a gym interface to the rougelike deck building game Balatro.


## Bug Tracker
Found a bug ? Please open an issue and describe what you found.

## Road Map
There are many things missing.

- [x] Basic game loop
- [x] Seals
- [x] Card enhancements
- [x] Card editions
- [ ] Joker ordering
- [ ] Boss blind effects
- [ ] Blind skips & rewards
- [ ] Shop system, purchasing
- [ ] Shop system, selling
- [ ] Tarot card redemption
- [ ] Planet card redemption
- [ ] Voucher system
- [ ] Deck stakes
- [ ] 6 / 150 Joker cards
- [ ] 0 / 22 Tarot cards
- [ ] 0 / Planet cards
- [ ] 1 / 15 Decks
- [ ] 0 / 20 Challenge Decks
- [ ] 0 / 32 Vouchers

## Contributing

Contributions are welcome. Please fork the repository and open a pull request in this repository.

### Setting up a dev environment

1) Install `uv` for your platform via the instructions [here](https://docs.astral.sh/uv/getting-started/installation/).

2) Clone this repository

3) (Optional, but recommended) Create a virtual environment in the project directory
```
: ~/balatro-gym$ uv venv
```
4) Finally, install the dependencies
```
: ~/balatro-gym$ uv sync
```
