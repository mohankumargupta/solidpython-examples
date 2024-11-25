import subprocess
from pathlib import Path
import sys

openscad_location = "C:\\Users\\Mohan\\scoop\\apps\\openscad-dev\\current\\openscad.exe"

def root_name():
    filename_without_extension = Path(sys.argv[0]).with_suffix('').name
    return filename_without_extension

def save_as_scad(part, name):
    part.save_as_scad(f"{name}.scad")


def save_as_stl(name):
    subprocess.call([openscad_location, "-o", f"{name}.stl", f"{name}.scad"])

def save_as_scad_and_stl(part, python_file):
    stem = Path(python_file).stem
    save_as_scad(part, stem)
    save_as_stl(stem)


    
