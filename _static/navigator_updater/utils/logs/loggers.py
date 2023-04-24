# -*- coding: utf-8 -*-

"""Store logger instances. """

from __future__ import annotations

__all__ = ['logger', 'conda_logger']

import logging

logger = logging.getLogger()
conda_logger = logging.getLogger('navigator_updater.conda')
