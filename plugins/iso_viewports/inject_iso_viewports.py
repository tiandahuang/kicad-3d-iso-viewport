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

import pcbnew, json, math, wx
from pathlib import Path

class IsoViewportsPlugin(pcbnew.ActionPlugin):
    """
    fully vibecoded plugin. might not work.
    """

    def defaults(self):
        self.name = "Inject 8 Engineering ISO Viewports"
        self.category = "3D Viewer"
        self.description = "Adds 8 true orthographic isometric camera viewports to the project JSON file."
        self.show_toolbar_button = True
        self.show_toolbar_button = True
        self.icon_file_name = str(Path(__file__).parent / "icon.png")

    def Run(self):
        board_path = Path(pcbnew.GetBoard().GetFileName())
        proj_path = board_path.with_suffix(".kicad_pro")
        
        if not board_path.name or not proj_path.exists():
            wx.MessageBox(f"Project file not found:\n{proj_path}", "ISO Viewports Error", wx.OK | wx.ICON_ERROR)
            return

        p = math.degrees(math.atan(1 / math.sqrt(2)))
        yaws = [(45, "Front-Right"), (-45, "Front-Left"), (135, "Back-Right"), (-135, "Back-Left")]
        views = [(f"ISO {i+1} - Top-{n}", -p, y) for i, (y, n) in enumerate(yaws)] + \
                [(f"ISO {i+5} - Bottom-{n}", p, y) for i, (y, n) in enumerate(yaws)]

        d = json.loads(proj_path.read_text(encoding="utf-8"))
        b = d.setdefault("board", {})
        old = [v for v in b.get("3dviewports", []) if not v.get("name", "").startswith("ISO ")]
        
        new = []
        for name, pitch, yaw in views:
            r_p, r_y = math.radians(pitch) / 2, math.radians(yaw) / 2
            cp, sp, cy, sy = math.cos(r_p), math.sin(r_p), math.cos(r_y), math.sin(r_y)
            new.append({
                "name": name,
                "ww": round(cp * cy, 6),
                "wx": round(-sp * sy, 6),
                "wy": round(sp * cy, 6),
                "wz": round(-cp * sy, 6),
                "px": 0.0, "py": 0.0, "pz": 0.0, "zoom": 1.0, "projection": 0
            })
            
        b["3dviewports"] = old + new
        proj_path.write_text(json.dumps(d, indent=2), encoding="utf-8")

        wx.MessageBox(
            "Successfully injected 8 ISO viewports into the project file!\n\n"
            "If the 3D Viewer is open, close and reopen it to load the new viewports.",
            "ISO Viewports Complete", wx.OK | wx.ICON_INFORMATION
        )

IsoViewportsPlugin().register()