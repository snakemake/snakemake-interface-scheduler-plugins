from abc import ABC, abstractmethod
from typing import Dict, Iterable, Union

from snakemake_interface_common.io import AnnotatedStringInterface


class SchedulerJobInterface(ABC):
    @abstractmethod
    def input(self) -> Iterable[AnnotatedStringInterface]:
        """Return an iterable of input files for the job."""
        ...

    @abstractmethod
    def output(self) -> Iterable[AnnotatedStringInterface]:
        """Return an iterable of output files for the job."""
        ...

    @abstractmethod
    def log(self) -> Iterable[AnnotatedStringInterface]:
        """Return an iterable of log files for the job."""
        ...

    @abstractmethod
    def benchmark(self) -> Iterable[AnnotatedStringInterface]:
        """Return an iterable of benchmark files for the job."""
        ...

    @abstractmethod
    def resources(self) -> Dict[str, Union[str, int, float]]:
        """Return a dictionary of resources used by the job."""
        ...
