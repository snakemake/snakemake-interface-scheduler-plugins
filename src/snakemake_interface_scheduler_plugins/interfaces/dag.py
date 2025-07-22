from abc import ABC, abstractmethod
from typing import Iterable, Mapping

from snakemake_interface_scheduler_plugins.interfaces.jobs import SingleJobSchedulerInterface
from snakemake_interface_common.io import AnnotatedStringInterface


class DAGSchedulerInterface(ABC):
    @abstractmethod
    def needrun_jobs(self) -> Iterable[SingleJobSchedulerInterface]:
        """Return an iterable of jobs in the DAG."""
        ...

    @abstractmethod
    def job_dependencies(
        self, job: SingleJobSchedulerInterface
    ) -> Iterable[SingleJobSchedulerInterface]:
        """Return an iterable of jobs that are dependencies of the given job."""
        ...

    @abstractmethod
    def finished(self, job: SingleJobSchedulerInterface) -> bool:
        """Check if the job is finished."""
        ...