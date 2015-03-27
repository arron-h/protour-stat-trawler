ProTrawler
====================

Trawls Wikipedia for UCI ProTour cyclist stats (height, weight, country, age) to work out averages.

## Usage

### Rebuilding the database
To rebuild the database, simply run `python ProTrawler.py`. This will output `data.js` to the current working directory.

### Rebuilding the web app

1. Rebuild the database as described above, then move `data.js` to `web/app/scripts/data/`.
2. Install/update Javascript dependencies with `npm install` and `bower install` whilst in the `web/` directory.
3. Run `grunt build` and the built web app will be in `dist/`.
