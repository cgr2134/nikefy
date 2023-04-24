# -*- coding: utf-8 -*-

"""Additional utilities to work with URLs."""

__all__ = ['join', 'netloc', 'inject_query_parameters', 'file_name']

import posixpath
import typing
from urllib import parse


def join(base: str, *args: str) -> str:
    """
    Join multiple URLS into a single one.

    :param base: Base URL to join parts to.
    :param args: URL parts to join.
    :return: Joined URL.
    """
    arg: str
    for arg in args:
        # This should prevent trimming of the last element for relative joins:
        # parse.urljoin('https://example.org/A', 'B/C') == 'https://example.org/B/C'
        # parse.urljoin('https://example.org/A/', 'B/C') == 'https://example.org/A/B/C'
        parsed_base: parse.ParseResult = parse.urlparse(base)
        if not parsed_base.path.endswith('/'):
            base = parse.urlunparse(
                parsed_base._replace(path=f'{parsed_base.path}/'),  # pylint: disable=protected-access
            )

        base = parse.urljoin(base, arg)

    return base


def netloc(url: typing.Union[None, bytes, str]) -> str:
    """
    Retrieve domain name from the `url`.

    This function is designed to work with both complete URLs like 'https://example.org/page' and schema-less URLs like
    'example.org/path'.

    :param url: URL to retrieve domain from.
    :return: Parsed domain name.
    """
    if url is None:
        return ''
    if not isinstance(url, str):
        url = url.decode()
    result: parse.ParseResult = parse.urlparse(url)
    if result.netloc:
        return result.netloc
    return result.path.split('/')[0]


def inject_query_parameters(url: str, params: typing.Mapping[str, typing.Any]) -> str:
    """
    Add or merge URL query parameters.

    :param url: URL to update.
    :param params: parameters to be ingested.
    :return: URL with update query params.
    """
    url_components: parse.ParseResult = parse.urlparse(url)
    original_params: typing.Mapping[str, typing.Sequence[str]] = parse.parse_qs(url_components.query)
    merged_params: typing.Mapping[str, typing.Any] = {**original_params, **params}
    updated_query: str = parse.urlencode(merged_params, doseq=True)
    return url_components._replace(query=updated_query).geturl()  # pylint: disable=protected-access


def file_name(url: typing.Union[None, bytes, str]) -> str:
    """Retrieve a file name from the url."""
    if url is None:
        return ''
    if not isinstance(url, str):
        url = url.decode()
    result: parse.ParseResult = parse.urlparse(url)
    left: str
    right: str
    left, right = posixpath.split(result.path)
    if (not left) and (not result.netloc):
        return ''
    if not right:
        left, right = posixpath.split(left)
    return right
