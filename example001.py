#%%


#from solid2 import cube
from common import save_as_scad_and_stl
from jupyterscad import view_stl
from groove_cube import create_grooved_cube

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
    #part = cube([base_width, base_width,3*base_width])
    part = create_grooved_cube((base_width, base_width,number_of_minicubes*base_width), grooves=[
      (groove_width,groove_height,first_groove),
      (groove_width,groove_height,second_groove)
    ])
    return part

# Main program
part = base_part()


# Save both as .scad and .stl
save_as_scad_and_stl(part, __file__)
view_stl("example001.stl")



# %%
