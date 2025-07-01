# Snakemake Scheduler Plugin Interface

This package provides a stable interface for interactions between Snakemake and its scheduler plugins.

Plugins should implement the following skeleton to comply with this interface.
It is recommended to use Snakemake's poetry plugin to set up this skeleton (and automated testing) within a python package, see https://github.com/snakemake/poetry-snakemake-plugin.

In any case, a plugin implementing this interface

* has to be named `snakemake-scheduler-plugin-<name>`,
* has to be published on pypi.io, and
* has to offer the following code implemented in its main module

```python

from snakemake_interface_scheduler_plugins.settings import SchedulerSettingsBase
from snakemake_interface_scheduler_plugins.base import SchedulerBase
from snakemake_interface_scheduler_plugins.interfaces.dag import SchedulerDAGInterface
from snakemake_interface_scheduler_plugins.interfaces.jobs import SchedulerJobInterface

# Optional:
# Define settings for your scheduler plugin.
# They will occur in the Snakemake CLI as --scheduler-<plugin-name>-<param-name>
# Make sure that all defined fields are 'Optional' and specify a default value
# of None or anything else that makes sense in your case.
class Settings(SchedulerSettingsBase):
    myparam: Optional[int] = field(
        default=None,
        metadata={
            "help": "Some help text",
            # Optionally request that setting is also available for specification
            # via an environment variable. The variable will be named automatically as
            # SNAKEMAKE_<storage-plugin-name>_<param-name>, all upper case.
            # This mechanism should only be used for passwords, usernames, and other
            # credentials.
            # For other items, we rather recommend to let people use a profile
            # for setting defaults
            # (https://snakemake.readthedocs.io/en/stable/executing/cli.html#profiles).
            "env_var": False,
            # Optionally specify a function that parses the value given by the user.
            # This is useful to create complex types from the user input.
            "parse_func": ...,
            # If a parse_func is specified, you also have to specify an unparse_func
            # that converts the parsed value back to a string.
            "unparse_func": ...,
            # Optionally specify that setting is required when the executor is in use.
            "required": True,
            # Optionally specify multiple args with "nargs": True
        },
    )


class Scheduler(SchedulerBase):
    def __post_init__(self) -> None:
        # Optional, remove method if not needed.
        # Perform any actions that shall happen after initialization.
        # Do not overwrite the actual __init__ method, in order to ensure compatibility
        # with future interface versions.
        ...

    def register_dag(self, dag: SchedulerDAGInterface) -> None:
        # This method is called when the DAG is updated.
        # It can be used to learn the DAG dependency structure that might be used to
        # inform the scheduler. Implement this as pass in case the DAG structure
        # is irrelevant for your scheduler.
        ...

    def select_jobs(self, open_jobs: Iterable[SchedulerJobInterface]) -> Iterable[SchedulerJobInterface]:
        # Select jobs from the open jobs iterable.
        ...

```
