
import os
from qgis.core import QgsApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsVectorLayer,
                       QgsProject,                      
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterFolderDestination,
                       QgsProcessingParameterCrs,
                       QgsProcessingParameterExtent)
from qgis import processing
from qgis.processing import alg
import subprocess

import platform
import re
import threading
from queue import Queue, Empty

def strip_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def enqueue_output(pipe, queue):
    for line in iter(pipe.readline, ''):
        queue.put(line)
    pipe.close()

@alg(name="run_bash", label="OSM2Envi_met", group="Envi_met Tools", group_label="Envi_met Tools")
#@alg.input(type=alg.FILE, name="SCRIPT", label="Bash Script (Must be an .sh file)")
@alg.input(type=alg.FILE, name="OSM", label="OSM File (Required)")
@alg.input(type=alg.FILE, name="DEM", label="DEM File (Optional, must be used with DSM)", optional=True)
@alg.input(type=alg.FILE, name="DSM", label="DSM File (Optional, must be used with DEM)", optional=True)
@alg.input(type=alg.CRS, name="CRS", label="Select Target CRS")
@alg.input(type=alg.EXTENT, name="EXTENT", label="Select Extent")
@alg.input(type=alg.BOOL, name="LOAD_LAYERS", label="Load Result Layers in QGIS", default=True)
@alg.output(type=alg.FOLDER, name="RESULT", label="Processed Output Directory")
def run_bash_script(instance, parameters, context, feedback, values=None):
    """
 Runs the 'osm2envi_gis.sh' bash script, which is assumed to be in the same directory as the qgis interface script, as a QGIS processing tool. You will need to provide a correctly digitised extent file and the target CRS. A DSM and DEM will be required to extract building heights.    """
    # Get the default QGIS profile directory
    # Compatible with older QGIS versions
    try:
        profile_path = QgsApplication.qgisSettingsDirPath()
    except AttributeError:
        profile_path = QgsApplication.qgisUserSettingsDirPath()

    # Construct the path to the processing scripts folder
    scripts_folder = os.path.join(profile_path, 'processing', 'scripts')

    # Define the script path
    script_path = os.path.join(scripts_folder, "osm2envi_qgis.sh")

    
    osm_file = parameters["OSM"]
    dem_file = parameters.get("DEM", None)
    dsm_file = parameters.get("DSM", None)
    target_crs = parameters["CRS"].authid()
    extent = parameters["EXTENT"]

    feedback.pushInfo(f"🔧 Running Bash script: {script_path}")
    feedback.pushInfo(f"📂 OSM File: {osm_file}")
    feedback.pushInfo(f"🌐 Target CRS: {target_crs}")
    feedback.pushInfo(f"📐 Selected Extent: {extent}")

    if (dem_file and not dsm_file) or (dsm_file and not dem_file):
        feedback.reportError("❌ Error: DEM and DSM must both be provided or both omitted.", fatalError=True)
        return {"RESULT": ""}

    if dem_file and dsm_file:
        feedback.pushInfo(f"📂 DEM File: {dem_file}")
        feedback.pushInfo(f"📂 DSM File: {dsm_file}")

    if platform.system() == "Windows":
        bash_path = r"C:\\Program Files\\Git\\bin\\bash.exe"
    else:
        bash_path = "/bin/bash"

    # Make script executable on non-Windows
    if platform.system() != "Windows":
        subprocess.run(["chmod", "+x", script_path], check=True)

    # Prepare command with unbuffered output using 'stdbuf'
    command = [bash_path, script_path, "-i", osm_file, "-c", target_crs, "-e", extent]
    if dem_file and dsm_file:
        command.extend(["-s", dsm_file, "-d", dem_file])

    if platform.system() != "Windows":
        command = ["stdbuf", "-oL", "-eL"] + command

    # Start the subprocess with unbuffered output
    # Compatible subprocess for older Python versions
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True
    )

    # Setup queue and threads for stdout and stderr
    q_stdout = Queue()
    q_stderr = Queue()

    t_stdout = threading.Thread(target=enqueue_output, args=(process.stdout, q_stdout))
    t_stderr = threading.Thread(target=enqueue_output, args=(process.stderr, q_stderr))
    t_stdout.start()
    t_stderr.start()

    try:
        while True:
            try:
                # Process stdout
                line = q_stdout.get_nowait()
                if line:
                    feedback.pushInfo(strip_ansi_codes(line.strip()))
            except Empty:
                pass

            try:
                # Process stderr
                err = q_stderr.get_nowait()
                if err:
                    feedback.reportError(strip_ansi_codes(err.strip()), fatalError=False)
            except Empty:
                pass

            if process.poll() is not None:
                break

        t_stdout.join()
        t_stderr.join()

        if process.returncode != 0:
            feedback.reportError(f"❌ Script execution failed with exit code {process.returncode}.", fatalError=True)
            return {"RESULT": ""}

    except Exception as e:
        feedback.reportError(f"❌ Exception during script execution: {str(e)}", fatalError=True)
        return {"RESULT": ""}

    # Retrieve the 'LOAD_LAYERS' parameter correctly
    load_layers = parameters.get("LOAD_LAYERS", False)

    # Determine the output directory relative to the input OSM file
    input_dir = os.path.dirname(osm_file)
    output_dir = os.path.join(os.path.dirname(input_dir), 'output')

    # Define expected result layers
    result_layers = [
        os.path.join(output_dir, f"{os.path.basename(osm_file).replace('.osm', '')}_surface_final_envimet.gpkg"),
        os.path.join(output_dir, f"{os.path.basename(osm_file).replace('.osm', '')}_vegetation_final_envimet.gpkg"),
        os.path.join(output_dir, f"{os.path.basename(osm_file).replace('.osm', '')}_buildings_final_envimet.gpkg")
    ]

    # Conditionally load the layers if the checkbox is checked
    if load_layers:
        for layer_path in result_layers:
            if os.path.exists(layer_path):
                layer = QgsVectorLayer(layer_path, os.path.basename(layer_path), "ogr")
                if layer.isValid():
                    QgsProject.instance().addMapLayer(layer)
                    feedback.pushInfo(f"✅ Loaded layer: {layer_path}")
                else:
                    feedback.reportError(f"❌ Invalid layer: {layer_path}")
            else:
                feedback.reportError(f"❌ Layer file not found: {layer_path}")
    else:
        feedback.pushInfo("ℹ️ User chose not to load the resulting layers.")
