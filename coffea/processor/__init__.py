"""A framework for analysis scale-out

Details...
"""
from .processor import ProcessorABC
from .dataframe import (
    LazyDataFrame,
    PreloadedDataFrame,
)
from .helpers import Weights, PackedSelection
from .executor import (
    iterative_executor,
    futures_executor,
    run_uproot_job,
    run_parsl_job,
    run_spark_job
)
from .accumulator import (
    value_accumulator,
    set_accumulator,
    dict_accumulator,
    defaultdict_accumulator,
    column_accumulator,
)

__all__ = [
    'ProcessorABC',
    'LazyDataFrame',
    'PreloadedDataFrame',
    'Weights',
    'PackedSelection',
    'iterative_executor',
    'futures_executor',
    'run_uproot_job',
    'run_parsl_job',
    'run_spark_job',
    'value_accumulator',
    'set_accumulator',
    'dict_accumulator',
    'defaultdict_accumulator',
    'column_accumulator',
]
