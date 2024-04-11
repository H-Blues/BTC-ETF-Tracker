import argparse
from datetime import date
from datetime import timedelta
import logging
from product.etp.arkb import ARKB
from product.etp.bitb import BITB
from product.etp.brrr import BRRR
from product.etp.btco import BTCO
from product.etp.ezbc import EZBC
from product.etp.fbtc import FBTC
from product.etp.gbtc import GBTC
from product.etp.hodl import HODL
from product.etp.ibit import IBIT
import sqlite3
from utils.config import RAW_SCHEMA_PATH


LOGGER = logging.getLogger()
s_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
s_handler.setFormatter(formatter)
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(s_handler)

parser = argparse.ArgumentParser(description="update all tables in schema raw")
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "-d",
    "--date",
    help="target date",
    required=False,
    type=date.fromisoformat
)
group.add_argument(
    "-fd",
    "--from-date",
    help="from target date",
    required=False,
    type=date.fromisoformat
)

conn = sqlite3.connect(RAW_SCHEMA_PATH)
c = conn.cursor()

services = [

    ARKB,
    BITB,
    BRRR,
    BTCO,
    GBTC,
    EZBC,
    FBTC,
    HODL,
    IBIT

]

################
# INPUTS
args = parser.parse_args()
ref_date = args.date
from_ref_date = args.from_date

if ref_date is not None:
    target_dates = [ref_date]

else:
    start = date.fromisoformat("2024-02-25")
    end = date.today()
    n_days = (end - start).days + 1

    target_dates = [start + timedelta(d) for d in range(n_days)]

    if from_ref_date is not None:

        target_dates = [d for d in target_dates if d >= from_ref_date]


for date_ in target_dates:

    LOGGER.info("##############################################")
    LOGGER.info(date_)

    for Service in services:

        try:
            s = Service(date_.isoformat())
            s.read()
            s.extract()
            s.update_db(conn)
        except:
            LOGGER.warning(f"{s} has failed")
