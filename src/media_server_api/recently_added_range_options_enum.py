from datetime import datetime
from enum import Enum, unique

from dateutil.relativedelta import relativedelta


@unique
class RecentlyAddedRangeOptions(Enum):
    ONE_DAY = relativedelta(days=1)
    THREE_DAYS = relativedelta(days=3)
    ONE_WEEK = relativedelta(weeks=1)
    TWO_WEEKS = relativedelta(weeks=2)
    THREE_WEEKS = relativedelta(weeks=3)
    ONE_MONTH = relativedelta(months=1)
    TWO_MONTHS = relativedelta(months=2)
    THREE_MONTHS = relativedelta(months=3)

    def __sub__(self, other):
        if isinstance(other, relativedelta | datetime):
            return self.value - other
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, relativedelta | datetime):
            return other - self.value
        return NotImplemented
