import logging
import csv
import os
import random
import uuid
from datetime import datetime as dt
from io import StringIO
from tempfile import TemporaryDirectory
from zipfile import ZipFile, ZIP_DEFLATED

import click

logging.basicConfig(level=logging.DEBUG)

INDEXES = [
    {"drawer": "SIS PROD", "doctype": "APPLICATION"},
    {"drawer": "SIS PROD", "doctype": "RECOMMENDATIONS"},
    {"drawer": "SIS PROD", "doctype": "TRANSCRIPTS"},
]

SRC_FILES = os.listdir("src")
CAREERS = ["ULSA", "UMUS", "UENG", "UJND", "UBA", "UART", "UARC", "UNUR", "UKIN"]


def generate_emplid():
    return f"{random.randint(0, 99999999):08}"


def get_timestamp():
    return dt.now().strftime("%Y%m%dT%H%M%S%f")


@click.command()
@click.option("--pdfs", type=int, default=0)
@click.option("--zipsize", type=int, default=0)
def main(pdfs, zipsize):
    if pdfs == 0:
        pdfs = random.randint(1, 10000)
    if zipsize == 0:
        zipsize = random.randint(1, 5000)
    generated = 0
    while generated < pdfs:
        zdttm = get_timestamp()
        zfn = f"SLTIMG_{zdttm}_test_files.zip"
        zfp = os.path.join("output", zfn)
        logging.debug(f"Opening {zfn}")
        with ZipFile(zfp, "w", compression=ZIP_DEFLATED) as zf:
            idxs = []
            for i in range(zipsize):
                src = random.choice(SRC_FILES)
                emplid = generate_emplid()
                career = random.choice(CAREERS)
                index = random.choice(INDEXES)
                guid = str(uuid.uuid4())
                dttm = get_timestamp()
                img_idx = "|".join(
                    [
                        "",
                        index["drawer"],
                        emplid,
                        str(dt.now().year),
                        index["doctype"],
                        career,
                        "",
                        "",
                        "NY",
                    ]
                )
                pdffn = f"SLT_{guid}_{dttm}.pdf"
                idxs.append(
                    {
                        "ext_adm_appl_nbr": emplid,
                        "m_ra_file_source": "SLT",
                        "filename": pdffn,
                        "m_ra_img_indexes": img_idx,
                    }
                )
                zf.write(os.path.join("src", src), pdffn)
                generated += 1
                logging.debug(f"{generated} - {i+1} / {zipsize} {pdffn}")
                if generated >= pdfs:
                    break

            with StringIO() as f:
                writer = csv.DictWriter(f, fieldnames=idxs[0].keys())
                writer.writeheader()
                writer.writerows(idxs)
                f.seek(0)
                zf.writestr(f"SLT_{zdttm}.csv", f.read())
                logging.debug(f"Index added")


if __name__ == "__main__":
    main()
