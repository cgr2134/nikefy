# -*- coding: utf-8 -*-

"""Extra solvers to migrate trusted_servers to domain-only format."""

from __future__ import annotations

__all__ = ()

import configparser
import contextlib
import html
import typing
from . import core

if typing.TYPE_CHECKING:
    import typing_extensions


class MigrationItem(typing.NamedTuple):
    """Instructions on how a preference should be migrated."""

    section: str
    from_option: str
    to_option: str


MIGRATION: 'typing_extensions.Final[typing.Sequence[MigrationItem]]' = (
    MigrationItem(section='main', from_option='anaconda_server_api_url', to_option='team_edition_api_url'),
    MigrationItem(section='main', from_option='anaconda_server_token', to_option='team_edition_token'),
    MigrationItem(section='main', from_option='anaconda_server_token_id', to_option='team_edition_token_id'),
    MigrationItem(section='main', from_option='anaconda_professional_url', to_option='commercial_edition_url'),
)


@core.CONFIGURATION_POOL.register
def migrate_branding(context: core.ConfigurationContext) -> typing.Optional[core.SolvedError]:
    """Migrate options affected by branding changes."""
    item: MigrationItem
    issues: typing.List[MigrationItem] = []
    for item in MIGRATION:
        new_value: typing.Optional[str]
        try:
            new_value = context.config.get(item.section, item.from_option)
        except configparser.NoOptionError:
            pass
        else:
            with contextlib.suppress(configparser.NoOptionError):
                default: typing.Any = context.config.get_default(item.section, item.to_option)
                if context.config.get(item.section, item.to_option) != default:
                    issues.append(item)
            context.config.set(item.section, item.to_option, new_value)
            context.config.remove_option(item.section, item.from_option)

    if issues:
        return core.SolvedError(
            caption='Conflicting preferences in navigator configuration',
            message='<br>'.join(
                f'<b>{html.escape(issue.to_option)}</b> was overwritten by <b>{html.escape(issue.from_option)}</b>'
                for issue in issues
            ),
            tags='branding_overlap',
        )
    return None
