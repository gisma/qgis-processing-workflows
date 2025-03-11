
## Installation Guide: Adding Bash Script to QGIS Processing Tools

This guide will help you install and integrate a custom Bash script into QGIS Processing Tools for **Windows**, **Linux**, and **macOS**.

---

## Step 1: Locate the QGIS Processing Scripts Folder

- Open **QGIS**.
- Go to **`Settings` > `Options`**.
- Navigate to the **`Processing`** tab.
- Under the **`Providers`** section, enable **`Scripts`** if not already enabled.
- Note the **`Scripts folder`** path. This is where you will place your custom Bash script and Python integration script.

---

## Step 2: Copy the Bash Script and Python Integration Script

1. **Download or Prepare Your Files**:
   - **Python Script** (`osm2envi_qgis.py`): This integrates the Bash script into QGIS Processing Tools.
   - **Bash Script** (`osm2envi_qgis`): The actual Bash script performing the processing.

2. **Copy the Files**:
   - Copy **both** scripts into the QGIS **Scripts folder** noted in Step 1.

---

## Step 3: Grant Execute Permissions (Linux/macOS Only)

For **Linux/macOS**, make the Bash script executable:

```bash
chmod +x /path/to/your/qgis/scripts/osm2envi_qgis.sh
```

---

## Step 4: Install Bash (If Not Installed)

- **Windows**:
  - Install [**Git Bash**](https://git-scm.com/download/win).
  - Ensure `bash.exe` is located at:  
    `C:\Program Files\Git\bin\bash.exe`

- **Linux/macOS**:
  - Bash is pre-installed by default.

---

## Step 5: Restart QGIS

- Restart **QGIS** to ensure it detects the new processing script.

---

## Step 6: Running the Script in QGIS

1. Open the **Processing Toolbox** (`Ctrl + Alt + T`).
2. Under **`Scripts` > `Custom Scripts`**, you should see **`Run Bash Script`**.
3. Double-click to run the tool:
   - Select your **OSM**, **DEM**, and **DSM** files.
   - Define the **CRS** and **Extent**.
   - Run the script and check the Processing Feedback for updates.

---

##  Troubleshooting

- If the script is not appearing:
  - Ensure the **Scripts provider** is enabled in QGIS Options.
  - Verify the script is in the correct **Scripts folder**.
  - Ensure **Git Bash** is installed on **Windows**.
  
- For Linux/macOS, ensure executable permission is correctly set with:

```bash
chmod +x /path/to/osm2envi_qgis.sh
```

---

And you're done! Your custom Bash script is now integrated into **QGIS Processing Tools** You can find it under `Scripts->Envi_met Tools->OSM2Envi_met`.

