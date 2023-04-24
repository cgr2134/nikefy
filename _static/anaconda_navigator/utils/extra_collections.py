# -*- coding: utf-8 -*-

"""Additional data collections."""

from __future__ import annotations

__all__ = ['OrderedSet']

import collections
import typing

if typing.TYPE_CHECKING:
    import typing_extensions


TInv = typing.TypeVar('TInv', bound=typing.Hashable)


class OrderedSet(typing.MutableSet[TInv], typing.Generic[TInv]):
    """Set, that preserves order of items added to it."""

    __slots__ = ('__content',)

    def __init__(self, content: typing.Iterable[TInv] = ()) -> None:
        """Initialize new :class:`~OrderedSet` instance."""
        self.__content: typing_extensions.Final[typing.OrderedDict[TInv, None]] = collections.OrderedDict(
            (item, None)
            for item in content
        )

    def add(self, value: TInv) -> None:
        """Add new value to :class:`~OrderedSet` instance."""
        self.__content[value] = None

    def discard(self, value: TInv) -> None:
        """Discard a value from :class:`~OrderedSet` instance."""
        self.__content.pop(value, None)

    def __contains__(self, value: typing.Any) -> bool:
        """Check if `value` is in :class:`~OrderedSet` instance."""
        return value in self.__content

    def __iter__(self) -> typing.Iterator[TInv]:
        """Iterate through the added values to :class:`~OrderedSet` instance."""
        return iter(self.__content)

    def __len__(self) -> int:
        """Retrieve total number of added items in :class:`~OrderedSet` instance."""
        return len(self.__content)
