# Castle Chess - Tournament Manager
<h1 align="center">
  <img alt="castle chess logo" src="img/CastleChessLogo.png" width="224px"/><br/>
</h1>

## Introduction
Manage a chess tournament efficiently with this standalone offline program. It uses the Python3 language and runs on the console.

## Quick start
To use this program, clone this project and run it through the console:
```bash
python3 main.py
```
Make sure to comply with the [package requirements](#package-requirements).

- You can create a new tournament, or add new players in the system.

- Once a tournament is created, you can add players to the tournament and start round the first round.

- Reports are available to show:
  - All players in the system by alphabetical or ranking order
  - All tournaments 
    - All rounds executed in the tournament, with all matches
    - Tournament players by alphabetical or ranking order

## Package requirements

Before using the application, please install all the packages as stated in [requirements.txt](requirements.txt)

From the terminal, use the command:

```
pip install -r requirements.txt
```

## Flake8 HTML Report
Order a new flake8 html report from the console:
```
flake8 --format=html --htmldir=flake8_report
```
Then open index.html from the [flake8_report repository](/flake8_report):
