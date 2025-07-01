__author__ = "Johannes Köster"
__copyright__ = "Copyright 2025, Johannes Köster"
__email__ = "johannes.koester@uni-due.de"
__license__ = "MIT"

from typing import Dict, Iterable, Optional, Union
from snakemake_interface_scheduler_plugins.interfaces.dag import SchedulerDAGInterface
from snakemake_interface_scheduler_plugins.interfaces.jobs import SchedulerJobInterface
from snakemake_interface_scheduler_plugins.settings import (
    SchedulerSettingsBase,
)
from abc import ABC, abstractmethod


class SchedulerBase(ABC):
    def __init__(
        self,
        settings: Optional[SchedulerSettingsBase],
    ) -> None:
        self.settings = settings
        self.__post_init__()

    def __post_init__(self) -> None:
        pass

    @abstractmethod
    def register_dag(self, dag: SchedulerDAGInterface) -> None:
        """This method is called when the DAG is updated."""
        ...

    @abstractmethod
    def select_jobs(
        self,
        open_jobs: Iterable[SchedulerJobInterface],
        available_resources: Dict[str, Union[int, float, str]],
    ) -> Iterable[SchedulerJobInterface]:
        """Select jobs from the open jobs iterable. Thereby, ensure that the selected
        jobs do not exceed the available resources.
        """
        ...
