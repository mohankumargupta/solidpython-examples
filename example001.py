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


def create_isometric_view(mesh):
    """
    Create an isometric view of the given mesh

    Parameters:
    - mesh: Trimesh object to visualize

    Returns:
    - None (displays the mesh)
    """
    # Add a reference axis for orientation
    axis = trimesh.creation.axis(origin_size=2, axis_length=50)

    # Create a scene
    scene = trimesh.Scene([mesh, axis])

    # Set up isometric-like view
    # Rotate to approximate isometric perspective

    # scene.set_camera(angles=[np.pi / 4, 0, np.pi / 4], distance=200)
    # scene.set_camera(angles=[np.pi / 4, 0, 0], distance=200)
    scene.set_camera(angles=[np.pi / 6, np.pi / 4, 0], distance=200)
    return scene


# Function to create the scene with the provided mesh and quaternion rotation
def create_scene(mesh, quaternion):
    # Add a reference axis for orientation
    axis = trimesh.creation.axis(origin_size=2, axis_length=50)

    # Convert quaternion to 4x4 rotation matrix
    rotation_matrix = quaternion_to_matrix(quaternion)

    # Define the target (center of the box)
    # Adjust for specific mesh dimensions
    target = np.array([0, 0, 75 / 2])

    # Set the camera direction and position (isometric-style)
    camera_direction = np.array([1, -1, 1])  # Isometric direction
    camera_direction = camera_direction / np.linalg.norm(camera_direction)  # Normalize
    camera_distance = 200  # Move camera farther from the mesh
    camera_position = target + camera_direction * camera_distance

    # Compute forward (view direction), right, and up vectors
    forward = target - camera_position
    forward /= np.linalg.norm(forward)
    up = np.array([0, 0, 1])  # Default up direction
    right = np.cross(up, forward)
    right /= np.linalg.norm(right)
    up = np.cross(forward, right)

    # Debug: Print camera placement
    print(f"Camera Position: {camera_position}")
    print(f"Target: {target}")
    print(f"Forward Vector: {forward}")
    print(f"Up Vector: {up}")
    print(f"Right Vector: {right}")

    # Construct the camera's rotation matrix
    camera_rotation_matrix = np.array(
        [
            [right[0], right[1], right[2], 0],
            [up[0], up[1], up[2], 0],
            [-forward[0], -forward[1], -forward[2], 0],
            [0, 0, 0, 1],
        ]
    )

    # Combine quaternion rotation and camera orientation
    camera_transform = np.dot(rotation_matrix, camera_rotation_matrix)

    # Set camera position explicitly to avoid being "inside" the tower
    camera_transform[0:3, 3] = camera_position
    camera_transform[3, 3] = 1

    # Create a scene with the mesh and axis
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

# scene = create_scene(mesh, quaternion)
scene = create_isometric_view(mesh)
scene.show()
# %%
