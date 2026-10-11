# -*- coding: utf-8 -*-
"""
engine/indexing/__init__.py
---------------------------
Instant Indexing Subsystem for Google & Bing / IndexNow.
"""

from .instant_indexer import InstantIndexer, submit_url_instantly

__all__ = ["InstantIndexer", "submit_url_instantly"]
