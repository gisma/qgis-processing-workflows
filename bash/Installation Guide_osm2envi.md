
## Installation Guide: Adding Bash Script to QGIS Processing Tools

This guide provides instructions to install and integrate a custom Bash script into QGIS Processing Tools for Windows, Linux, and macOS.

---

## Step 1: Locate the QGIS Processing Scripts Folder

- Open QGIS.
- Navigate to `Settings` > `Options` > `Processing` tab.
- Enable `Scripts` under `Providers` if not already enabled.
- Note the `Scripts folder` path for placing your custom scripts.

---

## Step 2: Copy the Scripts

- Copy the Python script (`osm2envi_qgis.py`) and Bash script (`osm2envi_qgis.sh`) into the QGIS `Scripts folder`.

---

## Step 3: Grant Execute Permissions (Linux/macOS Only)

```bash
chmod +x /path/to/your/qgis/scripts/osm2envi_qgis.sh
```

---

## Step 4: Install Bash (If Not Installed)

- **Windows**:
  - Install [Git Bash](https://git-scm.com/download/win).
  - Ensure `bash.exe` is located at: `C:\Program Files\Git\bin\bash.exe`

- **Linux/macOS**: Bash is pre-installed by default.

---

## Step 5: Restart QGIS

Restart QGIS to detect the new processing script.

---

## Step 6: Running the Script

- Open the Processing Toolbox (`Ctrl + Alt + T`).
- Navigate to `Scripts > Envi_met Tools > OSM2Envi_met`.
- Select the required input files (OSM, DEM, DSM) and specify the CRS and extent.
- Run the script and monitor the feedback panel for updates.

---

## Troubleshooting

- Ensure the Scripts provider is enabled in QGIS Options.
- Verify that scripts are in the correct `Scripts folder`.
- Ensure Git Bash is installed on Windows.
- For Linux/macOS, confirm the Bash script is executable:

```bash
chmod +x /path/to/osm2envi_qgis.sh
```

---

Your custom Bash script is now integrated into QGIS Processing Tools under `Scripts > Envi_met Tools > OSM2Envi_met`.
