""" [unittest]-compatible test case for testing the graphical user interface 
    for the `tkinter_spheres_environment_gui` package.

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
from tkinter_spheres_environment_gui.gui import GUI


# Define test case.
class TestCase(unittest.TestCase):
    """ Test case for testing GUI manipulations. """
    
    def __init__(self, *args, write_expected_data=False, **kwargs):
        self.write_expected_data = write_expected_data
        super().__init__(*args, **kwargs)
        
    def setUp(self):
        """ Initialize the GUI and shapes. """
        
        self.gui = GUI()
        canvas = self.gui.canvas
        canvas.dimensions = (600, 600)
        self.circle = tkinter_shapes.Circle(canvas=canvas)
        self.polygon = tkinter_shapes.Polygon(canvas=canvas)
        self.box = None
        self.triangle = None
        canvas.update()
        
    def tearDown(self):
        """ Terminate. """
        del self.triangle
        del self.box
        self.circle.delete()
        self.gui.destroy()
        
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
        observed_ps = self.gui.canvas.postscript(colormode='color')
        
        # To generate the image.
        if self.write_expected_data:
          self.gui.canvas.postscript(file=filepath, colormode='color')
        
        # Load the expected postscript data.
        with open(filepath, 'r') as f: expected_ps = f.read()
        
        # Verify that the observed canvas postscript matches expectations.
        is_expected_state = self.is_same_image(expected_ps, observed_ps)
        
        # Return the result.
        return is_expected_state
        
    def test_baseline(self):
        """ Verify that the baseline canvas matches expectations following 
            setup. 
        """
        
        # Verify that the observed canvas postscript matches expectations.
        filepath = 'data/test_gui-baseline-1.ps'
        self.assertTrue(self.is_expected_state(filepath))
    
    def test_circle(self):
        """ Test manipulation of a circle object. """
        
        # Initialize shorthand.
        circle = self.circle
        
        # Change the color of the circle.
        circle['outline'] = circle['fill'] = 'blue'
        
        # Set the circle position.
        circle.position = (300, 300)
        
        # Set the circle radius.
        circle.radius = 40
        
        # Query the dimensions of the circle bounding box, after resizing it.
        # Note that the width and/or height of the bounding box might not equal 
        # exactly twice the radius, since these dimensions are computed 
        # directly from the vertex pixel locations.
        tolerance = 1e-6
        expected_diameter = 2*circle.radius
        self.assertTrue(all((80 - x) < 1e-6 for x in circle.dimensions))
        
        # Update the canvas.
        self.gui.canvas.update()
        
        # Verify that the observed canvas postscript matches expectations.
        filepath = 'data/test_gui-circle-2.ps'
        self.assertTrue(self.is_expected_state(filepath))
    
    def test_box(self):
        """ Test manipulation of a bounding rectangle object. """
        
        # Initialize shorthand.
        polygon = self.polygon
        
        # Run the circle test in order to set up the expected state.
        self.test_circle()
        
        # Create a red bounding box to fit the circle.
        r = self.circle.radius
        box = self.box = self.polygon
        box.vertices = [(-r, -r), (+r, -r), (+r, +r), (-r, +r)]
        
        # Move the box to overlap with the circle.
        box.position = self.circle.position
        
        # Make the box transparent, with a red outline.
        box['fill'] = ''
        box['outline'] = 'red'
        
        # Update the canvas.
        self.gui.canvas.update()
        
        # Verify that the observed canvas postscript matches expectations.
        filepath = 'data/test_gui-box-3.ps'
        self.assertTrue(self.is_expected_state(filepath))
        
    def test_triangle(self):
        """ Test conversion of the bounding box into a rectangle. """
        
        # Run the box test in order to set up the expected state.
        self.test_box()
        
        # Initialize shorthand.
        circle = self.circle
        box = self.box
        triangle = self.triangle = box
        
        # Halve the width of the box.
        box.width = box.width / 2
        
        # Convert the box into a rectangle by removing a vertex.
        triangle.vertices = box.vertices[1:]
        
        # Change the color of the triangle.
        box['outline'] = box['fill'] = 'green'
        
        # Move the bottom of the rectangle up to match the center of the circle.
        (x, y) = circle.position
        r = circle.radius
        h = triangle.height
        box.position = (x, y-r+h/2)
        
        # Update the canvas.
        self.gui.canvas.update()
        
        # Verify that the observed canvas postscript matches expectations.
        filepath = 'data/test_gui-triangle-4.ps'
        self.assertTrue(self.is_expected_state(filepath))
    
  

# Main.
if __name__ == '__main__': unittest.main()


