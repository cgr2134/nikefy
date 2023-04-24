# -*- coding: utf-8 -*-

"""
Internal preferences of the Navigator.

This module should contain all preferences for the Navigator components, that are constant for the current Navigator
release.

.. note::

    The primary goal of this file - is to have a single place with configurations, instead of spreading them across the
    whole application. Thus, if we need to change a single URL, period, behavior - we may just look into a single file
    instead of looking across the related components to what should be changed.

.. warning::

    If you need any additional data structure for any preference - put it in the
    :mod:`~anaconda_navigator.config.structures`.

    The :mod:`~anaconda_navigator.config.preferences` should contain only preference, which should make it much easier
    to navigate through the file.
"""

from __future__ import annotations

__all__ = ()

import os
import typing

from . import base

if typing.TYPE_CHECKING:
    import typing_extensions


SECONDS: 'typing_extensions.Final[int]' = 1
MINUTES: 'typing_extensions.Final[int]' = 60 * SECONDS
HOURS: 'typing_extensions.Final[int]' = 60 * MINUTES
DAYS: 'typing_extensions.Final[int]' = 24 * HOURS


# ╠═══════════════════════════════════════════════════════════════════════════════════════════════╡ Advertisements ╞═══╣

def __init_ad_configuration_paths() -> typing.MutableSequence[str]:
    """Initialize sequence of paths to search configurations in."""
    result: typing.List[str] = []

    if os.name == 'nt':
        # pylint: disable=import-outside-toplevel
        from anaconda_navigator.external.knownfolders import get_folder_path, FOLDERID  # type: ignore
        result.extend((
            os.path.join(get_folder_path(FOLDERID.ProgramData)[0], 'Anaconda3', 'etc', 'partner.yml'),
            os.path.join(get_folder_path(FOLDERID.ProgramData)[0], 'Miniconda3', 'etc', 'partner.yml'),
            os.path.join(os.path.expanduser('~'), 'Anaconda3', 'etc', 'partner.yml'),
            os.path.join(os.path.expanduser('~'), 'Miniconda3', 'etc', 'partner.yml'),
        ))

    else:
        result.extend((
            os.path.join('/', 'etc', 'anaconda', 'partner.yml'),
            os.path.join('opt', 'anaconda3', 'etc', 'partner.yml'),
            os.path.join('opt', 'miniconda3', 'etc', 'partner.yml'),
            os.path.join(os.path.expanduser('~'), 'anaconda3', 'etc', 'partner.yml'),
            os.path.join(os.path.expanduser('~'), 'miniconda3', 'etc', 'partner.yml'),
        ))

    result.append(base.get_conf_path('partner.yml'))

    return result


AD_CONFIGURATION_PATHS: 'typing_extensions.Final[typing.Sequence[str]]' = __init_ad_configuration_paths()
AD_SLIDESHOW_TIMEOUT: 'typing_extensions.Final[int]' = 60 * SECONDS
AD_SOURCES: 'typing_extensions.Final[typing.Sequence[str]]' = (
    'https://anaconda.cloud/api/billboard/v1/ads/navigator/partner/{partner_identity}',
    'https://anaconda.cloud/api/billboard/v1/ads/navigator',
    'https://www.anaconda.com/api/navigator/partner/{partner_identity}',
    'https://www.anaconda.com/api/navigator',
)
