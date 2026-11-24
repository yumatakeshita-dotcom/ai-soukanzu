"""日本時間(JST)の「今日」をそろえる小さな道具。

クラウドの機械はUTC(世界標準時)で動く。朝7〜9時(日本時間)の作業は、UTCだと
まだ「前日」なので、date.today() や time.strftime() を使うと日付が1日前になる
(ファイル名が前日になる・「-2」が付く)。日付は必ずここから取る。
"""
import datetime

JST = datetime.timezone(datetime.timedelta(hours=9))


def now():
    return datetime.datetime.now(JST)


def today():
    """日本時間の今日(datetime.date)。date.today() の代わり。"""
    return now().date()


def strftime(fmt="%Y-%m-%d"):
    """日本時間の今。time.strftime(fmt) の代わり。"""
    return now().strftime(fmt)
