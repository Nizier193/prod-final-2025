from enum import Enum

METRIC_COLUMNS = 4
DATE_SLIDER_HELP = "Здесь можно выбрать с какого дня по какой выбрать."

# Constants
class Mode(Enum):
    DAILY = "DAILY"
    AGGREGATE = "AGGREGATE"