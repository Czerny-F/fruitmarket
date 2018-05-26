"""
統計処理のためのクラス群(Serviceレイヤ)

FruitSalesSet/FruitSalesStatsはライブラリに依存しない
"""
from abc import ABC
from typing import Iterator
import pandas as pd
from django.utils import timezone
from django.utils.functional import cached_property
from .managers import FruitSalesQuerySet
from .models import FruitSales


class FruitSalesSet(object):
    """
    果物別内訳クラス
    """

    def __init__(self, fruit, sales: list):
        self.fruit = fruit
        self.sales = sales

    @property
    def total_amount(self) -> int:
        return sum(s.amount for s in self.sales)

    @property
    def total_quantity(self) -> int:
        return sum(s.quantity for s in self.sales)


class FruitSalesStats(object):
    """
    FruitSalesのQuerySetをもとに総売上と果物別内訳を作る
    """

    def __init__(self, queryset: FruitSalesQuerySet):
        self._queryset = queryset

    @cached_property
    def queryset(self) -> FruitSalesQuerySet:
        """
        SQLクエリを減らすためselect_related()/cached_propertyを利用
        """
        return self._queryset.select_related()

    @cached_property
    def fruits(self) -> set:
        return set(obj.fruit for obj in self.queryset)

    @property
    def total_amount(self) -> int:
        return self.queryset.total_amount()

    def breakdown(self) -> Iterator[FruitSalesSet]:
        for fruit in self.fruits:
            sales = list(obj for obj in self.queryset if obj.fruit == fruit)
            yield FruitSalesSet(fruit, sales)


class AbstractSalesDataFrameStats(ABC):
    """
    総売上・数量計算のため、pandasのDataFrameをラッピングする抽象クラス
    """

    @cached_property
    def summed(self) -> pd.Series:
        return self.dataframe.sum()

    @property
    def total_amount(self) -> int:
        return int(self.summed.amount)

    @property
    def total_quantity(self) -> int:
        return int(self.summed.quantity)


class FruitSalesDataFrameSet(AbstractSalesDataFrameStats):
    """
    果物別内訳用DataFrameラッパークラス
    FruitSalesSetに対応するが、fruitは文字列型
    """

    def __init__(self, fruit: str, dataframe: pd.DataFrame):
        self.fruit = fruit
        self.dataframe = dataframe


class FruitSalesPeriodicStats(AbstractSalesDataFrameStats):
    """
    日別・月別のDataFrameラッパークラス
    上記のFruitSalesStatsに対応するが、dateはpandasのdatetimeラッパーのTimestamp
    """
    group_by = 'fruit'
    set_class = FruitSalesDataFrameSet

    def __init__(self, date: pd.Timestamp, dataframe: pd.DataFrame):
        self.date = date
        self.dataframe = dataframe

    def breakdown(self) -> Iterator:
        for group in self.dataframe.groupby(self.group_by):
            yield self.set_class(*group)


class FruitSalesDataFrameStats(AbstractSalesDataFrameStats):
    """
    果物販売情報DataFrameのラッパークラス

    pandasを利用するためSQLクエリ1〜2回で統計処理ができる
    """
    model = FruitSales
    date_field = 'sold_at'
    periodic_class = FruitSalesPeriodicStats

    @cached_property
    def dataframe(self) -> pd.DataFrame:
        """
        SQLクエリとDataFrame変換コストがあるためcached_propertyを利用
        期間別処理が必要なためindexに設定し、timezoneがUTCになるため変換する
        """
        df = self.model.objects.to_dataframe(index=self.date_field)
        return df.tz_convert(timezone.get_current_timezone_name())

    @property
    def gross(self) -> int:
        return self.total_amount

    def monthly(self, periods=3) -> Iterator:
        return self._periodic_stats(freq='M', periods=periods)

    def daily(self, periods=3) -> Iterator:
        return self._periodic_stats(freq='D', periods=periods)

    def _periodic_stats(self, freq: str, periods=3) -> Iterator:
        for period in list(self.dataframe.groupby(pd.Grouper(freq=freq)))[-periods:]:
            yield self.periodic_class(*period)
