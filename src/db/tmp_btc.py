import logging
import sqlite3
from utils.config import RAW_SCHEMA_PATH as PATH


LOGGER = logging.getLogger()
s_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
s_handler.setFormatter(formatter)
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(s_handler)

conn = sqlite3.connect(PATH)
c = conn.cursor()

LOGGER.info("Creating schema RAW at:")
LOGGER.info(f"{PATH}")


##################################################################
#                          BTC
##################################################################

CREATE_BTC_KEY_FUND_INFORMATION = """

CREATE TABLE IF NOT EXISTS btc_key_fund_information (

    file_name           TEXT    NOT NULL,
    ref_date            TEXT    NOT NULL,
    aum                 REAL,
    n_shares            INT,
    n_coins             REAL,

    PRIMARY KEY (ref_date)
)
"""

CREATE_BTC_DAILY_PERFORMANCE = """

CREATE TABLE IF NOT EXISTS btc_daily_performance (

    file_name                       TEXT    NOT NULL,
    ref_date                        TEXT    NOT NULL,
    market_price                    REAL,
    daily_share_volume_traded       INT,

    PRIMARY KEY (ref_date)
)
"""

c.execute(CREATE_BTC_KEY_FUND_INFORMATION)
c.execute(CREATE_BTC_DAILY_PERFORMANCE)

c.execute("INSERT into btc_key_fund_information VALUES ('','2024-07-30',0,0,0)")
c.execute("INSERT into btc_key_fund_information VALUES ('','2024-07-31',0,0,0)")
c.execute("INSERT into btc_daily_performance VALUES ('','2024-07-30',0,0)")
c.execute("INSERT into btc_daily_performance VALUES ('','2024-07-31',0,0)")

LOGGER.info("Created table BTC_KEY_FUND_INFORMATION")
LOGGER.info("Created table BTC_DAILY_PERFORMANCE")
