""" Tests conforming with [pytest] framework requirements, for testing the 
    `tkinter_spheres_environment_gui` package.

[pytest]: https://docs.pytest.org

Usage examples: 

`pytest test_tkinter_spheres_environment_gui`

`pytest test_tkinter_spheres_environment_gui::test_reference_images`

`pytest -k test_reference_images test_tkinter_spheres_environment_gui`

"""

# Copyright 2022 Carnegie Mellon University Neuromechatronics Lab (a.whit)
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# 
# Contact: a.whit (nml@whit.contact)


# Import pytest.
import pytest

# Import Tkinter canvas postscript utilities.
from . import tkinter_canvas_postscript

# Import fixtures.
from .fixtures import reference_environment_gui
from .fixtures import images_basepath
from .fixtures import reference_image_sequence

# Import the reference image generator.
from .fixtures import reference_image_generator \
  as reference_image_generator_function


# Test generated reference images against copies stored on disk.
# Save the generated image to disk, if any file does not exist.
def test_reference_images(reference_image_sequence, images_basepath):
    
    # Iterate through all reference images in the sequence.
    for (index, postscript) in enumerate(reference_image_sequence):
        
        # Initialize parameters.
        filename = f'reference_image_{index}.ps'
        
        # Initialize the file path.
        from os import sep
        filepath = f'{images_basepath}{sep}{filename}'
        
        # If a postscript image file does not exist at the specified path, then 
        # generate such a file by saving the reference image postscript data.
        # Save the generated image to disk, if the file does not exist.
        import os.path
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f: f.write(postscript)
        
        # Load a copy of the reference postscript image data from disk.
        with open(filepath, 'r') as f: postscript_d = f.read()
        
        # Test the generated image against the image stored on disk.
        # Verify that the data loaded from disk matches the fixture.
        assert tkinter_canvas_postscript.equals(postscript_d, postscript)
    
  

# Test object color property.
def test_reference_image_states(reference_environment_gui):
    
    # Initialize parameters.
    key_a = 'object_a'
    key_b = 'object_b'
    
    # Initialize the generator.
    reference_image_generator \
      = reference_image_generator_function(reference_environment_gui)
    
    # Image 0: baseline.
    ps = next(reference_image_generator)
    assert len(reference_environment_gui.keys()) == 0
    
    # Image 1: Initialize a new object and update the color property.
    ps = next(reference_image_generator)
    color = dict(r=0.0, g=0.0, b=1.0, a=1.0)
    assert reference_environment_gui[key_a].color == color
    
    # Image 2: Re-size the object.
    ps = next(reference_image_generator)
    assert reference_environment_gui[key_a].radius == 0.20
    
    # Image 3: Re-position the object.
    ps = next(reference_image_generator)
    position = dict(zip(['x', 'y', 'z'], (0.50, -0.55, 1.00)))
    assert reference_environment_gui[key_a].position == position
    
    # Image 4: Initialize a second object and update the color, position,  
    #          and size properties.
    ps = next(reference_image_generator)
    color = dict(zip(['r', 'g', 'b', 'a'], (0.0, 1.0, 0.0, 1.0)))
    position = dict(zip(['x', 'y', 'z'], (-0.25, 0.25, 0.00)))
    radius = 0.10
    assert reference_environment_gui[key_b].color == color
    assert reference_environment_gui[key_b].position == position
    assert reference_environment_gui[key_b].radius == radius
    
    # Image 5: Move the second object to overlap with the first.
    ps = next(reference_image_generator)
    position = dict(zip(['x', 'y', 'z'], (0.35, -0.35, 1.0)))
    assert reference_environment_gui[key_b].position == position
    
  

# __main__
if __name__ == '__main__':
    pytest.main(['test_tkinter_spheres_environment_gui.py'])
    
  


