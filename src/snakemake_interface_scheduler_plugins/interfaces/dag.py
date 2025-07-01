from abc import ABC, abstractmethod
from typing import Iterable

from snakemake_interface_scheduler_plugins.interfaces.jobs import SchedulerJobInterface


class SchedulerDAGInterface(ABC):
    @abstractmethod
    def jobs(self) -> Iterable[SchedulerJobInterface]:
        """Return an iterable of jobs in the DAG."""
        ...

    @abstractmethod
    def dependencies(
        self, job: SchedulerJobInterface
    ) -> Iterable[SchedulerJobInterface]:
        """Return an iterable of jobs that are dependencies of the given job."""
        ...

    @abstractmethod
    def finished(self, job: SchedulerJobInterface) -> bool:
        """Check if the job is finished."""
        ...
