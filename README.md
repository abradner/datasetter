# Datasetter

This repo is designed to allow me to rapidly pull and analyse hunks of data for different purposes

Right now that purpose is singlular so it's not very generic

## Installation

This repo uses Poetry as a python dependecy management system. Tested on python 3.9

```bash
git clone https://github.com/abradner/datasetter.git
brew install python poetry # at a minimum install poetry
cd datasetter
poetry install
```

One of the dependencies - `Geohash` - hasn't been kept up to date and you will need to make a one-liner change. to do this:

1. open up your venv directory (find it with `poetry env info -p`)
2. open up `lib/python3.9/site-packages/Geohash/__init__.py` (you may need to adapt the path for later versions)
3. on line 21 add a '.' before geohash:

```diff
- from geohash import decode_exactly, decode, encode
+ from .geohash import decode_exactly, decode, encode
```

Alternatively in an IDE like vscode you can just follow the `Geohash` import (<kbd>F12</kbd> / <kbd>Command + Click</kbd>) in `app/geohash_functions.py` to find the file then make the above change.

## Config

All config is stored in `app/settings.py` you'll need to supply values for every `CHANGE`

## Running

Two ways to run this. The best is through jupyter lab but it can also run throuh CLI

### Jupyter

```bash
poetry shell
jupyter-lab
```

Then load up the `Full-Reindex` and `Benchmark` notebooks and play them back

### CLI

To run everything (Load from snowflake, process, index, benchmark):

```bash
poetry shell
python main.py 
```

Just benchmark:

```bash
poetry shell
python main.py --skip_indexing=true
```
