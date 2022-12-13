""" [unittest]-compatible test case for testing the 
    `tkinter_spheres_environment_gui` package.

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
from tkinter_shapes import Polygon

# Local imports.
from tkinter_spheres_environment_gui import Environment


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
    """ Test case for testing the tkinter_spheres_environment_gui package. """
    
    def setUp(self):
        """ Initialize the Environment and shapes. """
        
        # Initialize a canvas GUI  environment.
        environment = self.environment = Environment()
        canvas = self.canvas = environment.gui.canvas
        
        # Initialize a rectangular, black polygon, with the same size as the 
        # canvas. This is necessary because the postscript data does not 
        # capture the black background.
        (w, h) = canvas.dimensions
        vertices = [(0, 0), (0, h), (w, h), (w, 0)]
        rectangle = self.rectangle = Polygon(canvas=canvas, vertices=vertices)
        rectangle['fill'] = 'black'
        rectangle['outline'] = 'black' #'white'
        canvas.update()
        
    def tearDown(self):
        """ Terminate. """
        del self.environment
        
    def test_baseline(self):
        """ Verify that the baseline canvas matches expectations following 
            setup. 
        """
        
        ## Update the canvas.
        #self.canvas.update()
        
        # Verify that the observed canvas postscript matches expectations.
        filepath = 'data/test_package-baseline-1.ps'
        self.assertTrue(self.is_expected_state(filepath))
    
    def test_cursor(self):
        """ Verify cursor initialization. """
        
        # Initialize shorthand.
        environment = self.environment
        
        # Create a cursor.
        cursor = self.cursor = environment.initialize_object('cursor')
        
        # Verify the default parameters are as expected.
        expected = {'position': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'radius': 1.0}
        self.assertTrue(environment['cursor'] == expected)
        
        # Change the cursor color to green.
        cursor.color = (0.0, 1.0, 0.0, 1.0)
        environment.update()
        
        # Verify that the observed canvas postscript matches expectations.
        filepath = 'data/test_package-cursor-2.ps'
        self.assertTrue(self.is_expected_state(filepath))
        
        # Change the cursor radius and position.
        cursor.radius = 0.1
        cursor.position = (-0.25, 0.25, 1.0)
        environment.update()
        
        # Verify that the observed canvas postscript matches expectations.
        filepath = 'data/test_package-cursor-3.ps'
        self.assertTrue(self.is_expected_state(filepath))
    
    def test_target(self):
        """ Verify target. """
        
        # Initialize shorthand.
        environment = self.environment
        
        # Create a cursor.
        self.test_cursor()
        
        # Create a target.
        target = self.target = environment.initialize_object('target')
        
        # Change the target color to blue.
        target.color = (0.0, 0.0, 1.0, 1.0)
        environment.update()
        
        # Change the target radius and position.
        target.radius = 0.2
        target.position = (0.5, -0.5, 0.0)
        environment.update()
        
        # Verify that the observed canvas postscript matches expectations.
        filepath = 'data/test_package-target-4.ps'
        self.assertTrue(self.is_expected_state(filepath))
        
        # Change the cursor position to overlap with the target.
        self.cursor.position = (0.35, -0.35, 1.0)
        environment.update()
        
        # Verify that the observed canvas postscript matches expectations.
        filepath = 'data/test_package-target-5.ps'
        self.assertTrue(self.is_expected_state(filepath))
        
        # Adjust the z-order to bring the cursor to the foreground.
        self.cursor.to_foreground()
        
        # Verify that the observed canvas postscript matches expectations.
        filepath = 'data/test_package-target-6.ps'
        self.assertTrue(self.is_expected_state(filepath))
        
        
        
        
        
    
  

# Main.
if __name__ == '__main__': unittest.main()


