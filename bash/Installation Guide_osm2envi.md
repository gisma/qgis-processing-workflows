## Installation Guide: Adding Bash Script to QGIS Processing Tools

This guide provides instructions to install and integrate a custom Bash script into QGIS Processing Tools for Windows, Linux, and macOS.

**Tested for QGIS 3.x up to 3.4.x**

---

## Step 1: Install Bash (Windows Only)

- **Windows**:

  - Install [Git Bash](https://git-scm.com/download/win).
  - Ensure `bash.exe` is located at: `C:\Program Files\Git\bin\bash.exe`

- **Linux/macOS**: Bash is pre-installed by default.

---

## Step 2: Locate the QGIS Processing Scripts Folder

- Open QGIS.
- Navigate to `Settings` > `Options` > `Processing` tab.
- Enable `Scripts` under `Providers` if not already enabled.
- Note the `Scripts folder` path for placing your custom scripts.

> **Note for Linux Users:**
>
> - For a generic QGIS installation, the scripts folder is typically located at `~/.local/share/QGIS/QGIS3/profiles/default/processing/scripts`.
> - For Flatpak installations, the folder is located at `~/.var/app/org.qgis.qgis/data/QGIS/QGIS3/profiles/default/processing/scripts`.
> - For Snap installations, it's located at `/home/$USER/snap/qgis/current/.local/share/QGIS/QGIS3/profiles/default/processing/scripts`.
> - Ensure you have proper permissions and access to the scripts folder.

---

## Step 3: Copy the Scripts

- Copy the Python script (`osm2envi_qgis.py`) and Bash script (`osm2envi_qgis.sh`) into the QGIS `Scripts folder`.

---

## Step 4: Restart QGIS

Restart QGIS to detect the new processing script.

---

## Step 5: Running the Script

- Open the Processing Toolbox (`Ctrl + Alt + T`).
- The script is located under `Processing Toolbox` > `Scripts` > `Envi_met Tools` > `OSM2Envi_met`.
- Select the required input files (OSM, DEM, DSM) and specify the CRS and extent.
- Run the script and monitor the feedback panel for updates.

---

## Troubleshooting

- Ensure the Scripts provider is enabled in QGIS Options.
- Verify that scripts are in the correct `Scripts folder`.
- Ensure Git Bash is installed on Windows.
- For Linux/macOS, if you encounter permission issues, manually make the Bash script executable with:

```bash
chmod +x /path/to/osm2envi_qgis.sh
```

> **Linux Flatpak/Snap Users:**
>
> - For Flatpak, the scripts folder is typically located at `~/.var/app/org.qgis.qgis/data/QGIS/QGIS3/profiles/default/processing/scripts`.
> - For Snap, it's located at `/home/$USER/snap/qgis/current/.local/share/QGIS/QGIS3/profiles/default/processing/scripts`.
> - If you encounter issues with paths, check the sandboxed environment and ensure QGIS has access to the necessary directories.

---

## Additional Tip

- The Bash script can also be executed directly from the command line. Use the `-h` flag to display help information:

```bash
./osm2envi_qgis.sh -h
```

This will display available command-line options and usage details.

---

Your custom Bash script is now integrated into QGIS Processing Tools under `Scripts > Envi_met Tools > OSM2Envi_met`.

