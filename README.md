[![make.fun bounty](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01) [![make.fun rank](https://make.fun/badge/tiny-chess-01/kar-jel/tiny-chess-01-entry/rank.svg)](https://make.fun/bounty/tiny-chess-01) [![make.fun reward](https://make.fun/badge/tiny-chess-01/kar-jel/tiny-chess-01-entry/reward.svg)](https://make.fun/bounty/tiny-chess-01)

# tiny-chess-01 entry

My entry for make.fun's tiny-chess-01 bounty. main.py is a chess engine written in
Python that fits in at most 4096 bytes and uses no third-party code, only the standard library.
In the kit's house-gauntlet practice trial it measures an Elo of about 1,100 (an earlier build
measured 1,191).

It talks to the bounty environment over JSON/HTTP: it asks for a game, plays the move its own
search picks, and reports back until the game is done. Point it at the env and run it:

    MAKEFUN_ENV_URL=http://127.0.0.1:8080 python3 main.py

MIT licensed; see LICENSE.
