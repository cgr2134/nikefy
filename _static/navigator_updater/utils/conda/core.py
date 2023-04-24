# -*- coding: utf-8 -*-

"""Collection of the core utilities."""

from __future__ import annotations

__all__ = ['is_conda_available', 'get_conda_info']

import os
import sys
import typing
import json
from . import exceptions
from . import launch

if typing.TYPE_CHECKING:
    import typing_extensions
    from . import types as conda_types


WIN: 'typing_extensions.Final[bool]' = (os.name == 'nt')


def get_conda_cmd_path() -> typing.Optional[str]:
    """Check if conda is found on path."""
    bin_folder: str = 'Scripts' if WIN else 'bin'
    conda_exe: str = 'conda-script.py' if WIN else 'conda'
    env_prefix: str = os.path.dirname(os.path.dirname(sys.prefix))
    cmds: typing.List[str] = [
        os.path.join(env_prefix, bin_folder, conda_exe),
        os.path.join(sys.prefix, bin_folder, conda_exe),
        'conda',
    ]

    cmd: str
    for cmd in cmds:
        stdout: str
        stderr: str
        error: bool
        stdout, stderr, error = launch.run_process(cmd_list=[cmd, '--version'])

        if (not error) and any(item.startswith('conda ') for item in (stdout, stderr)):
            return cmd

    return None


def is_conda_available() -> bool:
    """Check if conda is available in path."""
    return get_conda_cmd_path() is not None


def get_conda_info() -> typing.Optional['conda_types.CondaInfoOutput']:
    """Return conda info as a dictionary."""
    conda_cmd: typing.Optional[str] = get_conda_cmd_path()
    if conda_cmd is None:
        return None

    out: str = launch.run_process(cmd_list=[conda_cmd, 'info', '--json']).stdout

    result: typing.Union['conda_types.CondaInfoOutput', 'conda_types.CondaErrorOutput']
    try:
        result = json.loads(out)
    except (TypeError, ValueError):
        return None

    if 'error' not in result:
        return typing.cast('conda_types.CondaInfoOutput', result)

    raise exceptions.CondaError(error=typing.cast('conda_types.CondaErrorOutput', result))
