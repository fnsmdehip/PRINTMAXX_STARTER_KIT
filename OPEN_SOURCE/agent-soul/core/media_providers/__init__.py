"""
Media Providers -- individual provider implementations for sovrun media router.

Each provider inherits from MediaProvider and implements:
    generate()      - produce the media asset
    get_cost()      - estimated cost per generation
    is_available()  - whether this provider can run right now
"""
from __future__ import annotations

from .base import MediaProvider, ProviderResult

__all__ = ["MediaProvider", "ProviderResult"]
