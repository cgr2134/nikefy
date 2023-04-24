# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# Copyright (c) 2016-2017 Anaconda, Inc.
#
# May be copied and distributed freely only as part of an Anaconda or
# Miniconda installation.
# -----------------------------------------------------------------------------

"""Base configuration management."""

import os
import os.path as osp
from navigator_updater.utils import encoding


# -----------------------------------------------------------------------------
# --- Configuration paths
# -----------------------------------------------------------------------------

SUBFOLDER = os.path.join('.anaconda', 'navigator')


def get_home_dir():
    """Return user home directory."""
    path = None
    if os.name == 'nt':
        path_env_vars = ('HOME', 'APPDATA', 'USERPROFILE', 'TMP')
        # prefer locations that already have .anaconda/navigator folders
        for env_var in path_env_vars:
            path = os.path.join(encoding.to_unicode_from_fs(os.environ.get(env_var, '')), SUBFOLDER)
            if osp.isdir(path):
                break
            path = None

        # did not find .anaconda/navigator folder; find first existing variable
        if not path:
            for env_var in path_env_vars:
                # os.environ.get() returns a raw byte string which needs to be
                # decoded with the codec that the OS is using
                # to represent environment variables.
                path = encoding.to_unicode_from_fs(os.environ.get(env_var, ''))
                if osp.isdir(path):
                    break
                path = None

    else:
        try:
            # expanduser() returns a raw byte string
            # which needs to be decoded with the codec
            # that the OS is using to represent file paths.
            path = encoding.to_unicode_from_fs(osp.expanduser('~'))
        except Exception:  # pylint: disable=broad-except
            path = ''
    if path:
        return path
    raise RuntimeError('Please define environment variable $HOME')


def get_conf_path(filename=None):
    """Return absolute path for configuration file with specified filename."""
    conf_dir = osp.join(get_home_dir(), SUBFOLDER)
    if not osp.isdir(conf_dir):
        os.makedirs(conf_dir)
    if filename is None:
        return conf_dir
    return osp.join(conf_dir, filename)
