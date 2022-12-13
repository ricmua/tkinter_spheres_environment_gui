""" [unittest]-compatible test case for testing spheres object interfaces for 
    the `tkinter_spheres_environment_gui` package.

[unittest]: https://docs.pytest.org
"""

# Copyright 2022 Carnegie Mellon University Neuromechatronics Lab (a.whit)
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# 
# Contact: a.whit (nml@whit.contact)


# Import io and codecs.
import io
import codecs

# Import unittest.
import unittest

# Import the Python Imaging Library.
import PIL.Image

# Import tkinter_shapes.
import tkinter_shapes

# Local imports.
from tkinter_spheres_environment_gui.sphere import Sphere


# Define a base class for testing Tkinter canvases.
class CanvasTestCase(unittest.TestCase):
    """ Base test case for verifying that Tkinter canvases match expectations.
    """
    
    def __init__(self, *args, write_expected_data=False, **kwargs):
        self.write_expected_data = write_expected_data
        super().__init__(*args, **kwargs)
        
    def convert_ps_to_image(self, postscript):
        """ Convert a postscript string into a PIL image. """
        
        # Create a bytes buffer.
        image_buffer = io.BytesIO()
        
        # Create a codec writer to convert the postscript string into bytes.
        Writer = codecs.getwriter('utf-8')
        writer = Writer(image_buffer)
        
        # Write the postscript data to the buffer and rewind the position.
        print(postscript, file=writer)
        image_buffer.seek(0)
        
        # Open the buffer as a PIL image object.
        image = PIL.Image.open(image_buffer) #, formats=['ps'])
        
        # Return the result.
        return image
        
    def is_same_image(self, expected_ps, observed_ps):
        """ Compares two images specified as Postscript strings.
        
        The Postscript strings cannot be compared directly because the metadata 
        and comments might differ.
        """
        
        # Load the expected image.
        image_e = self.convert_ps_to_image(expected_ps)
        
        # Load the observed image.
        image_o = self.convert_ps_to_image(observed_ps)
        
        # Compare the binary data.
        is_same_image = (image_e.tobytes() == image_o.tobytes())
        
        # Return the result.
        return is_same_image
        
    def is_expected_state(self, filepath):
        """ Tests whether or not the current canvas matches some expected 
            state.
            
        Arguments
        ---------
        filepath : str
            File path to a postscript file containing the expected state of the 
            canvas.
        
        Returns
        -------
        is_expected_state : bool
            A boolean value indicating whether or not the observed canvas state 
            matches the expected canvas state.
        """
        
        # Generate postscript data for the current canvas.
        observed_ps = self.canvas.postscript(colormode='color')
        
        # To generate the image.
        if self.write_expected_data:
          self.canvas.postscript(file=filepath, colormode='color')
        
        # Load the expected postscript data.
        with open(filepath, 'r') as f: expected_ps = f.read()
        
        # Verify that the observed canvas postscript matches expectations.
        is_expected_state = self.is_same_image(expected_ps, observed_ps)
        
        # Return the result.
        return is_expected_state
    
  

# Define test case.
class TestCase(CanvasTestCase):
    """ Test case for testing Sphere object manipulations. """
    
    def setUp(self):
        """ Initialize the GUI and shapes. """
        
        # Initialize a GUI top level window.
        gui = self.gui = tkinter_shapes.GUI()
        gui.dimensions = (800, 600)
        
        # Initialize a canvas.
        canvas = self.canvas = tkinter_shapes.Canvas(gui)
        canvas.dimensions = (600, 600)
        canvas.background_color = 'black'
        canvas.pack()
        
        # Update the GUI.
        gui.update()
        
    def tearDown(self):
        """ Terminate. """
        self.gui.destroy()
        
    def test_baseline(self):
        """ Verify that the baseline canvas matches expectations following 
            setup. 
        """
        
        # Update the canvas.
        self.canvas.update()
        
        # Verify that the observed canvas postscript matches expectations.
        filepath = 'data/test_sphere-baseline-1.ps'
        self.assertTrue(self.is_expected_state(filepath))
    
    def test_initialization(self):
        """ Verify Sphere initialization. """
        
        # Create a sphere.
        sphere = self.sphere = Sphere('sphere', canvas=self.canvas)
        
        # Change the color.
        sphere.color = (1, 0, 0, 1)
        
        # Update the canvas.
        self.canvas.update()
        
        # Verify that the observed canvas postscript matches expectations.
        filepath = 'data/test_sphere-initialization-2.ps'
        self.assertTrue(self.is_expected_state(filepath))
        
    def test_radius(self):
        """ Verify Sphere radius adjustments. """
        
        # Run the initialization test in order to set up the expected state.
        self.test_initialization()
        
        # Initialize shorthand.
        sphere = self.sphere
        
        # Adjust the radius.
        sphere.radius = 0.1
        
        # Update the canvas.
        self.canvas.update()
        
        # Verify that the observed canvas postscript matches expectations.
        filepath = 'data/test_sphere-radius-3.ps'
        self.assertTrue(self.is_expected_state(filepath))
        
    def test_position(self):
        """ Verify Sphere position adjustments. """
        
        # Run the radius test in order to set up the expected state.
        self.test_radius()
        
        # Initialize shorthand.
        sphere = self.sphere
        
        # Adjust the radius.
        sphere.position = (0.5, 0.5, 0.5)
        
        # Update the canvas.
        self.canvas.update()
        
        # Verify that the observed canvas postscript matches expectations.
        filepath = 'data/test_sphere-position-4.ps'
        self.assertTrue(self.is_expected_state(filepath))
        
        
        

    
    
  

# Main.
if __name__ == '__main__': unittest.main()


