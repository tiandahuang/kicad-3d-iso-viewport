# Engineering ISO 3D Viewports for KiCad 10+

A KiCad PCB Editor Action Plugin that injects **8 true orthographic isometric camera angles** into your `.kicad_pro` project file.

Standard CAD tools often lack quick hotkeys or presets for all 8 isometric octants. This plugin programmatically calculates and injects standard engineering isometric camera angles directly into your project's viewports menu.

> 🤖 **Vibe-Coded Disclosure:** Generated via prompt-and-pray. Use at great risk.

---

## Features

* **8 Complete Octants:** Generates Top-Front-Right, Top-Front-Left, Top-Back-Right, Top-Back-Left, and the corresponding 4 Bottom views.
* **Engineering Standard Angle:** Uses $\arctan(1/\sqrt{2}) \approx 35.264389^\circ$ camera pitch tilt so that all three principal axes ($X, Y, Z$) maintain equal spatial foreshortening on screen.
* **True Drafting Scale:** Forces **Orthographic Projection** (`"projection": 0`) on all injected viewports, keeping parallel lines parallel without perspective distortion.
* **Non-Destructive:** Preserves any existing custom non-ISO viewports already present in your `.kicad_pro` file.

---

## Installation

### Method 1: KiCad Package and Content Manager (Recommended)

1. Open KiCad and launch the **Package and Content Manager** from the main project window.
2. Search for `Engineering ISO 3D Viewports` in the official repository.
3. Click **Install**, then click **Apply Pending Changes** at the bottom right.
4. Restart KiCad to load the new plugin into the PCB Editor toolbar.

#### Via Custom Repository / ZIP URL
If installing from a custom repository or raw release ZIP:
1. Open the **Package and Content Manager**.
2. Click **Manage...** (or the settings gear) to add a custom repository URL, or click **Install from File...** at the bottom of the window.
3. Select the plugin `.zip` package and click **Apply Pending Changes**.

---

### Method 2: Manual Installation

Copy the `iso_viewports` plugin directory into your KiCad 10.0 scripting plugins folder:

* **Windows:** `%APPDATA%\kicad\10.0\scripting\plugins\`
* **Linux:** `~/.local/share/kicad/10.0/scripting/plugins/`
* **macOS:** `~/Library/Preferences/kicad/10.0/scripting/plugins/`

---

## Usage

1. Open your PCB layout in KiCad's **PCB Editor**.
2. Click the **Inject 8 Engineering ISO Viewports** button on the top toolbar (or access it via `Tools` $\rightarrow$ `External Plugins` $\rightarrow$ `Inject 8 Engineering ISO Viewports`).
3. A confirmation dialog will appear once the viewports are injected into `.kicad_pro`.
4. Open the **3D Viewer** (`Alt + 3`).
5. In the top menu bar, go to **View** $\rightarrow$ **Viewports** (or click the Viewports dropdown) and select any of the 8 isometric camera presets.

> **Note:** If the 3D Viewer was already open before running the plugin, close and reopen it so KiCad reloads the updated project settings from disk.

---

## Repository Structure

```text
kicad-iso-viewports/
├── plugins/
│   └── iso_viewports/
│       ├── __init__.py
│       └── icon.png
├── metadata.json
├── LICENSE
└── README.md