"""
Inject 8 Engineering ISO Viewports for KiCad 10+
Copyright (C) 2026

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

---
DISCLOSURE: This plugin (including this docstring) was fully vibe-coded.
---
"""

from .inject_iso_viewports import IsoViewportsPlugin

IsoViewportsPlugin().register()
