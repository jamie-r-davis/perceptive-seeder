# PC Seeder

Small script that will generate sample payloads for image volume testing.


## Setup

To get going, follow two steps:

1. Install dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

2. Add source pdfs to `src` directory.


## Usage

Run the script to generate a random number of pdfs split across randomly partitioned zipfiles. All zip files will be stored in the `output` directory.

To control the output, use the `--pdfs` and `--zipsize` options:

```bash
app.py --pdfs 1000 --zipsize 75
```

This will generate 1,000 pdfs and put them into zip files containing 75 pdfs a piece.

By default, all files will be added to the zips without compression. To add compression, use the `--compressed` option:

```bash
app.py --pdfs 15000 --zipsize 1000 --compressed
```
