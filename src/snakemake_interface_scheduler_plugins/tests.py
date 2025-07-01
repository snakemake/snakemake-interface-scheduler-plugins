from abc import ABC, abstractmethod
from typing import Dict, Iterable, List, Optional, Type, Union
from snakemake_interface_scheduler_plugins.base import SchedulerBase
from snakemake_interface_scheduler_plugins.interfaces.dag import SchedulerDAGInterface
from snakemake_interface_scheduler_plugins.interfaces.jobs import SchedulerJobInterface
from snakemake_interface_scheduler_plugins.settings import SchedulerSettingsBase
from snakemake_interface_common.io import AnnotatedStringInterface


class DummyJob(SchedulerJobInterface):
    def __init__(
        self,
        input: List[AnnotatedStringInterface],
        output: List[AnnotatedStringInterface],
        resources: Dict[str, Union[str, int, float]],
    ) -> None:
        self._input = input
        self._output = output

    def input(self) -> Iterable[AnnotatedStringInterface]:
        return self._input

    def output(self) -> Iterable[AnnotatedStringInterface]:
        return self._output

    def log(self) -> Iterable[AnnotatedStringInterface]:
        return []

    def benchmark(self) -> Iterable[AnnotatedStringInterface]:
        return []

    def resources(self) -> Dict[str, Union[str, int, float]]:
        return {}


class DummyDAG(SchedulerDAGInterface):
    def __init__(self) -> None:
        self._jobs = [
            DummyJob(
                input=[AnnotatedStringInterface("input1.txt")],
                output=[AnnotatedStringInterface("output1.txt")],
                resources={"cpu": 1, "mem_mb": 2048},
            ),
            DummyJob(
                input=[AnnotatedStringInterface("output1.txt")],
                output=[AnnotatedStringInterface("output2.txt")],
                resources={"cpu": 2, "mem_mb": 4096},
            ),
            DummyJob(
                input=[AnnotatedStringInterface("output1.txt")],
                output=[AnnotatedStringInterface("output3.txt")],
                resources={"cpu": 1, "mem_mb": 1024},
            ),
        ]
        self._dependencies: Dict[SchedulerJobInterface, List[SchedulerJobInterface]] = {
            self._jobs[1]: [self._jobs[0]],
            self._jobs[2]: [self._jobs[0]],
        }
        self._finished = set()

    def jobs(self) -> Iterable[SchedulerJobInterface]:
        return self._jobs

    def dependencies(
        self, job: SchedulerJobInterface
    ) -> Iterable[SchedulerJobInterface]:
        return self._dependencies.get(job, [])

    def finished(self, job: SchedulerJobInterface) -> bool:
        return job in self._finished


class TestSchedulerBase(ABC):
    __test__ = False

    @abstractmethod
    def get_scheduler_cls(self) -> Type[SchedulerBase]: ...

    @abstractmethod
    def get_scheduler_settings(self) -> Optional[SchedulerSettingsBase]: ...

    def test_scheduler(self):
        scheduler_cls = self.get_scheduler_cls()
        settings = self.get_scheduler_settings()
        scheduler = scheduler_cls(settings=settings)
        assert isinstance(scheduler, SchedulerBase), (
            "Scheduler instance is not of type SchedulerBase"
        )
        assert scheduler.settings == settings, (
            "Scheduler settings do not match expected settings"
        )

        dag = DummyDAG()

        scheduler.register_dag(dag)

        scheduled = list(
            scheduler.select_jobs(
                [dag._jobs[0]], available_resources={"cpu": 1, "mem_mb": 1024}
            )
        )
        assert scheduled == [], (
            "Scheduler should not select jobs exceeding available resources"
        )

        scheduled = list(
            scheduler.select_jobs(
                [dag._jobs[0]], available_resources={"cpu": 1, "mem_mb": 2048}
            )
        )
        assert scheduled == [dag._jobs[0]], "Scheduler did not select the expected job"

        dag._finished.add(dag._jobs[0])

        scheduled = list(
            scheduler.select_jobs(
                [dag._jobs[1], dag._jobs[2]],
                available_resources={"cpu": 5, "mem_mb": 10000},
            )
        )
        assert scheduled == [dag._jobs[1], dag._jobs[2]], (
            "Scheduler did not select the expected jobs"
        )
