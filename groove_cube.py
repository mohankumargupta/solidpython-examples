from solid2 import cube, translate, union
from solid2.core.object_base import OpenSCADObject
from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class CubeConfig:
    """Configuration for the main cube"""
    width: float
    depth: float
    height: float

    @classmethod
    def from_tuple(cls, dimensions: Tuple[float, float, float]) -> 'CubeConfig':
        return cls(dimensions[0], dimensions[1], dimensions[2])

@dataclass
class GrooveConfig:
    """Configuration for a single groove"""
    width: float    # Height of the groove
    depth: float    # How deep the groove cuts
    offset: float   # Distance from bottom of cube

    @classmethod
    def from_tuple(cls, data: Tuple[float, float, float]) -> 'GrooveConfig':
        width, depth, offset = data
        return cls(width, depth, offset)

class GrooveGenerator:
    """Handles the creation of grooves for a cube"""
    
    def __init__(self, cube_config: CubeConfig):
        self.cube = cube_config

    def create_x_axis_groove(self, x_position: float, groove: GrooveConfig) -> OpenSCADObject:
        """Create a groove along the X axis (left/right sides)"""
        return translate([
            x_position,
            0,
            groove.offset
        ])(
            cube([
                groove.depth,
                self.cube.depth,
                groove.width
            ])
        )

    def create_y_axis_groove(self, y_position: float, groove: GrooveConfig) -> OpenSCADObject:
        """Create a groove along the Y axis (front/back sides)"""
        return translate([
            0,
            y_position,
            groove.offset
        ])(
            cube([
                self.cube.width,
                groove.depth,
                groove.width
            ])
        )

    def create_groove_set(self, groove: GrooveConfig) -> OpenSCADObject:
        """Create a complete set of grooves at one offset"""
        grooves = [
            # Front groove
            self.create_y_axis_groove(-groove.depth/2, groove),
            # Back groove
            self.create_y_axis_groove(self.cube.depth - groove.depth/2, groove),
            # Left groove
            self.create_x_axis_groove(-groove.depth/2, groove),
            # Right groove
            self.create_x_axis_groove(self.cube.width - groove.depth/2, groove)
        ]
        return union()(*grooves)

    def create_all_grooves(self, groove_configs: List[GrooveConfig]) -> OpenSCADObject:
        """Create and combine all groove sets"""
        all_sets = [self.create_groove_set(groove) for groove in groove_configs]
        return union()(*all_sets)

def create_grooved_cube(
    cube_size: Tuple[float, float, float] = (30, 30, 30),
    grooves: List[Tuple[float, float, float]] = None
) -> OpenSCADObject:
    """
    Creates a cube with multiple grooves on all sides.
    
    Args:
        cube_size: (width, depth, height) of the main cube
        grooves: List of groove configurations, each as:
                (width, depth, offset)
                where:
                - width is the height of the groove
                - depth is how deep the groove cuts into the cube
                - offset is the distance from the bottom of the cube
                
    Example:
        [(5, 3, 10),   # 5 wide, 3 deep, 10 units from bottom
         (5, 3, 20),   # 5 wide, 3 deep, 20 units from bottom
         (5, 3, 30)]   # 5 wide, 3 deep, 30 units from bottom
    
    Returns:
        OpenSCADObject: The resulting grooved cube
    """
    # Create cube configuration
    cube_config = CubeConfig.from_tuple(cube_size)
    
    # Handle default groove if none provided
    if grooves is None:
        grooves = [(5, 3, 10)]  # Default single groove 10 units from bottom
        
    # Convert tuples to GrooveConfig objects
    groove_configs = [GrooveConfig.from_tuple(g) for g in grooves]
    
    # Create main cube
    main_cube = cube([cube_config.width, cube_config.depth, cube_config.height])
    
    # Generate grooves
    generator = GrooveGenerator(cube_config)
    all_grooves = generator.create_all_grooves(groove_configs)
    
    # Subtract grooves from main cube
    return main_cube - all_grooves

# def example_usage():
#     """Example showing how to use the multi-grooved cube generator"""
#     # Create a cube with three equally-spaced grooves
#     basic_cube = create_grooved_cube(
#         cube_size=(40, 40, 40),
#         grooves=[
#             (5, 3, 10),  # 10 units from bottom
#             (5, 3, 20),  # 20 units from bottom
#             (5, 3, 30)   # 30 units from bottom
#         ]
#     )
#     scad_render_to_file(basic_cube, "basic_grooved_cube.scad")
    
#     # Create a cube with varied groove sizes
#     varied_cube = create_grooved_cube(
#         cube_size=(50, 50, 50),
#         grooves=[
#             (3, 2, 10),  # Small groove near bottom
#             (5, 3, 25),  # Medium groove in middle
#             (8, 4, 40)   # Large groove near top
#         ]
#     )
#     scad_render_to_file(varied_cube, "varied_grooved_cube.scad")

# if __name__ == "__main__":
#     example_usage()