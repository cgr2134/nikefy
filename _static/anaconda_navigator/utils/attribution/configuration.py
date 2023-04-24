# -*- coding: utf-8 -*-

"""Additional configuration properties for the attribution."""

from __future__ import annotations

__all__ = ['APPLICABLE_HOSTS']

import typing

if typing.TYPE_CHECKING:
    import typing_extensions


APPLICABLE_HOSTS: 'typing_extensions.Final[typing.Sequence[str]]' = (
    'anaconda.*',
    '*.anaconda.*',
)
