# -*- coding: utf-8 -*-
"""
engine/distribution/__init__.py
-------------------------------
Multi-channel Social & Community Distribution Subsystem.
"""

from .multi_channel_distributor import MultiChannelDistributor, dispatch_to_all_channels

__all__ = ["MultiChannelDistributor", "dispatch_to_all_channels"]
