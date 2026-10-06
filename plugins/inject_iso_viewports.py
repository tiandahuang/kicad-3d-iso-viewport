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
        self.icon_file_name = str(Path(__file__).parent / "icon.png")

    def Run(self):
        board_path = Path(pcbnew.GetBoard().GetFileName())
        proj_path = board_path.with_suffix(".kicad_pro")
        
        if not board_path.name or not proj_path.exists():
            wx.MessageBox(f"Project file not found:\n{proj_path}", "ISO Viewports Error", wx.OK | wx.ICON_ERROR)
            return

        # Load board and calculate bounding box center in mm
        board = pcbnew.GetBoard()
        bbox = board.GetBoundingBox()
        center = bbox.GetCenter()
        cx = pcbnew.ToMM(center.x)
        cy = pcbnew.ToMM(center.y)

        # Iso angles
        c30_ce = math.sqrt(0.5)      # 0.707107
        s30_ce = math.sqrt(1.0/6.0)  # 0.408248
        se     = math.sqrt(1.0/3.0)  # 0.577350
        ce     = math.sqrt(2.0/3.0)  # 0.816497

        # 4 Quadrants for standard isometric top/bottom angles
        top_views = [
            ("ISO 1 - Top-Front-Right",  [-c30_ce, -s30_ce,  se], [ c30_ce, -s30_ce,  se], [0.0,  ce,  se]),
            ("ISO 2 - Top-Back-Right",   [ c30_ce, -s30_ce,  se], [ c30_ce,  s30_ce, -se], [0.0,  ce,  se]),
            ("ISO 3 - Top-Back-Left",    [ c30_ce,  s30_ce, -se], [-c30_ce,  s30_ce, -se], [0.0, -ce, -se]),
            ("ISO 4 - Top-Front-Left",   [-c30_ce,  s30_ce, -se], [-c30_ce, -s30_ce,  se], [0.0, -ce, -se])
        ]

        bottom_views = [
            ("ISO 5 - Bottom-Front-Right", [-c30_ce, -s30_ce, -se], [ c30_ce, -s30_ce, -se], [0.0,  ce, -se]),
            ("ISO 6 - Bottom-Back-Right",  [ c30_ce, -s30_ce, -se], [ c30_ce,  s30_ce,  se], [0.0,  ce, -se]),
            ("ISO 7 - Bottom-Back-Left",   [ c30_ce,  s30_ce,  se], [-c30_ce,  s30_ce,  se], [0.0, -ce,  se]),
            ("ISO 8 - Bottom-Front-Left",  [-c30_ce,  s30_ce,  se], [-c30_ce, -s30_ce, -se], [0.0, -ce,  se])
        ]

        views = top_views + bottom_views

        # Project file modification
        d = json.loads(proj_path.read_text(encoding="utf-8"))
        b = d.setdefault("board", {})

        iso_names = {v[0].strip().casefold() for v in views}
        old = [v for v in b.get("3dviewports", []) if v.get("name", "").strip().casefold() not in iso_names]

        new = []
        for name, x_col, y_col, z_col in views:
            wx_dist = -(cx * x_col[0] - cy * y_col[0])
            wy_dist = -(cx * x_col[1] - cy * y_col[1])
            new.append({
                "name": name,
                "ww": 1.0, 
                "wx": round(wx_dist, 6), 
                "wy": round(wy_dist, 6), 
                "wz": -100.0,
                "xw": 0.0, "xx": round(x_col[0], 6), "xy": round(x_col[1], 6), "xz": round(x_col[2], 6),
                "yw": 0.0, "yx": round(y_col[0], 6), "yy": round(y_col[1], 6), "yz": round(y_col[2], 6),
                "zw": 0.0, "zx": round(z_col[0], 6), "zy": round(z_col[1], 6), "zz": round(z_col[2], 6)
            })

        b["3dviewports"] = old + new
        proj_path.write_text(json.dumps(d, indent=2), encoding="utf-8")

        wx.MessageBox(
            "Successfully injected 8 ISO viewports into the project file!\n\n"
            "Please relaunch KiCAD to see the changes applied.",
            "ISO Viewports Complete", wx.OK | wx.ICON_INFORMATION
        )
