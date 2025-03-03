# NHL Playground

## Overview

A freetime project regarding NHL game analysis throught statistics and machine learning.

The final project should include all neccesary tools to scrape data using the official NHL API and several predictive models.

## Instalation


## Usage

Current version supports team stats and PbP scraping. Simply run `poetry run python scripts/run_scraping.py --save --filepath "<filename-path>"` to scrape team stats from 2021-2023 (including postseason) and save as csv file.

Additionally, the repo provides xG preprocessing script. Run `poetry run python scripts/run_xg_preprocessing.py -e add_prev_play_name` for running a preprocessing script. You can use `-s` to save model to output defined by `-o` flag.

## Status

### IDEAS

- xGoals
- xShots
- xGoals of teamg
- xShots of team

### TODO

- Simple model based on TeamStats scraping

### DONE

- TeamStats scraping
- Scraper base class
- Player stats scraper
- PbP scraping
