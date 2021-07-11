import jschon

CATALOGUE = jschon.Catalogue.create_default_catalogue("2020-12")

ONE_BIN_KB: int = 1024  # 2^10
ONE_BIN_MB: int = 0x100000  # 2^20
ONE_BIN_GB: int = 0x40000000  # 2^30
ONE_BIN_TB: int = 0x10000000000  # 2^40
ONE_BIN_PB: int = 0x4000000000000  # 2^50

ONE_OF_1024: float = 0.0009765625  # 1/1024

APP_NAME: str = "mybigdata"

MYBIGDATA_CONF_NAME: str = "mybigdata_configuration"

DEFAULT_JSON_SCHEMA_DIRECTORY_RELATIVE_PATH: str = "mybigdata/src/main/resources/json/schema/"
