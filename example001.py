# %%


# from solid2 import cube
from solid2 import cube
from solid2.core.object_base import OpenSCADObject

# from dataclasses import dataclass
# from typing import Tuple, List
from common import save_as_scad_and_stl

# from jupyterscad import view_stl
from groove_cube import create_grooved_cube

import trimesh
import numpy as np


base_width = 25
base_depth = base_width
minicube_height = base_width
number_of_minicubes = 3
base_height = number_of_minicubes * minicube_height
groove_width = 2
groove_height = groove_width
groove_depth = 2
first_groove = minicube_height
second_groove = 2 * minicube_height


def base_part():
    # part = cube([base_width, base_width,3*base_width])
    part = create_grooved_cube(
        (base_width, base_width, number_of_minicubes * base_width),
        grooves=[
            (groove_width, groove_height, first_groove),
            (groove_width, groove_height, second_groove),
        ],
    )
    return part


def create_extruded_square(size) -> OpenSCADObject:
    return cube(size).translate([10, -5, first_groove + 10])


def diamond_pattern():
    pass


# Function to create labeled text for axes
def create_axis_labels():
    labels = []
    # Define axis end points and labels
    label_positions = {
        "X": [50, 0, 0],
        "Y": [0, 50, 0],
        "Z": [0, 0, 50],
    }

    for label, position in label_positions.items():
        # Create a text mesh
        text = trimesh.creation.text(label, font_size=5, depth=1)
        # Center the text
        text.apply_translation(position)
        labels.append(text)

    return labels


# Function to convert quaternion to a 4x4 rotation matrix
def quaternion_to_matrix(quaternion):
    w, x, y, z = quaternion
    return np.array(
        [
            [1 - 2 * y**2 - 2 * z**2, 2 * x * y - 2 * z * w, 2 * x * z + 2 * y * w, 0],
            [2 * x * y + 2 * z * w, 1 - 2 * x**2 - 2 * z**2, 2 * y * z - 2 * x * w, 0],
            [2 * x * z - 2 * y * w, 2 * y * z + 2 * x * w, 1 - 2 * x**2 - 2 * y**2, 0],
            [0, 0, 0, 1],
        ]
    )


# Function to create the scene with a provided mesh and quaternion rotation
def create_scene(mesh, quaternion):
    # Create a simple axis to show as a reference
    axis = trimesh.creation.axis(origin_size=2, axis_length=50)

    # Convert quaternion to 4x4 rotation matrix
    rotation_matrix = quaternion_to_matrix(quaternion)

    # Define the target (center of the box)
    target = np.array([0, 0, 75 / 2])  # Adjust if needed for other meshes

    # Set the camera position (FreeCAD-style isometric view)
    camera_direction = np.array([1, -1, 1])  # Isometric view direction
    camera_direction = camera_direction / np.linalg.norm(camera_direction)  # Normalize
    camera_distance = 150  # Adjust distance as needed
    camera_position = target + camera_direction * camera_distance

    # Define the up direction (aligned with Z-axis)
    up = np.array([0, 0, 1])

    # Compute the forward vector (view direction)
    forward = target - camera_position
    forward /= np.linalg.norm(forward)

    # Compute the right vector (perpendicular to forward and up)
    right = np.cross(up, forward)
    right /= np.linalg.norm(right)

    # Recompute the up vector (perpendicular to forward and right)
    up = np.cross(forward, right)

    # Construct the camera rotation matrix (for view setup)
    camera_rotation_matrix = np.array(
        [
            [right[0], right[1], right[2], 0],
            [up[0], up[1], up[2], 0],
            [-forward[0], -forward[1], -forward[2], 0],
            [0, 0, 0, 1],
        ]
    )

    # Combine the camera's rotation matrix and position into one transform
    camera_transform = np.dot(rotation_matrix, camera_rotation_matrix)

    # Create the scene with mesh, axis, and apply the camera transform
    scene = trimesh.Scene([mesh, axis])
    scene.camera_transform = camera_transform

    return scene


# Main program
part = base_part()
part += create_extruded_square(5)
# part = create_extruded_square(5).debug()
# Save both as .scad and .stl
save_as_scad_and_stl(part, __file__)
# view_stl("example001.stl")


mesh = trimesh.load("example001.stl")
# Example quaternion (this is the one you mentioned)
quaternion = (
    0.4247081321999479,
    0.1759200437218226,
    0.339851090706265,
    0.8204732639190053,
)

scene = create_scene(mesh, quaternion)
scene.show()
# %%
