""" Tkinter-based 2D graphical interface for representing interactions among 
    spherical / circular objects in a 3D virtual environment.

Examples
--------

Initialize a canvas GUI.

>>> gui = GUI()
>>> canvas = gui.canvas

Reshape the canvas to be a square that fills the available space.

>>> canvas.dimensions = (600, 600)
>>> canvas.update()

Initialize a circle on the canvas.

>>> circle = tkinter_shapes.Circle(canvas=canvas)

The default color is black, so the circle will not be visible. Set the circle 
outline and fill color to blue.

>>> circle['outline'] = circle['fill'] = 'blue'
>>> canvas.update()

Set the position of the center of the circle.

>>> circle.position = (100, 100)
>>> canvas.update()

Query the dimensions of the circle bounding box, before and after resizing it.
Note that the width and/or height of the bounding box might not equal exactly 
twice the radius, since these dimensions are computed directly from the vertex 
pixel locations.

>>> circle.dimensions
(2.0, 2.0)
>>> circle.radius = 40
>>> tuple((80 - x) < 1e-6 for x in circle.dimensions)
(True, True)
>>> canvas.update()

Move the circle to the center of the canvas.

>>> circle.position = (300, 300)
>>> canvas.update()

Draw a red square, with sides of length equal to the radius of the circle.

>>> r = circle.radius
>>> vertices = [(-r, -r), (+r, -r), (+r, +r), (-r, +r)]
>>> square = tkinter_shapes.Polygon(canvas=canvas, vertices=vertices)
>>> square['outline'] = 'red'
>>> canvas.update()

The square is drawn at the origin, so it is only partially visible. Move the 
square to overlap with, and obscure part of, the circle.

>>> square.position = circle.position
>>> canvas.update()

The square now matches the bounding box of the circle. Make the square 
transparent, to make the circle visible once again.

>>> square['fill'] = ''
>>> canvas.update()

Remove a vertex from the square polygon to convert it to an isosceles triangle.

>>> triangle = square
>>> triangle.vertices = square.vertices[1:]
>>> canvas.update()

Remove the shapes from the canvas.

>>> triangle.delete()
>>> del circle
>>> canvas.update()

Cleanup by destroying the GUI.

>>> gui.destroy()

"""

# Copyright 2022 Carnegie Mellon University Neuromechatronics Lab (a.whit)
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# 
# Contact: a.whit (nml@whit.contact)


# Local tkinter_shapes.
import tkinter_shapes


# GUI class.
class GUI(tkinter_shapes.GUI):
    """ 2D canvas GUI.
        
    Attributes
    ----------
    *args : list
        Arguments passed to the `tkinter_shapes.GUI` constructor.
    dimensions : tuple of ints
        The desired width and height of the GUI window.
    **kwargs : dict
        Keyword arguments passed to the `tkinter_shapes.GUI` constructor.
    """
    def __init__(self, *args, dimensions=(800, 600), **kwargs):
        
        # Invoke the superclass constructor.
        super().__init__(*args, **kwargs)
        
        # Set the GUI dimensions.
        self.dimensions = dimensions
        
        # Show the GUI.
        self.update()
        
        # Initialize the canvas.
        self.initialize_canvas()
        
    def initialize_canvas(self):
        """ Initialize a canvas for drawing objects on. """
        
        # Create the canvas.
        self.canvas = tkinter_shapes.Canvas(self)
        
        # Invoke the tkinter pack geometry manager.
        # It is assumed that the canvas is the only widget in the toplevel.
        self.canvas.pack()
        
        # Update the GUI to show the canvas.
        self.update()
        
        # Set the default background color.
        self.canvas.background_color = 'black'
        
        # Size the canvas to match the toplevel GUI window.
        self.canvas.dimensions = self.dimensions
        
        ## Initialize a rectangular, black polygon, with the same size as the 
        ## canvas. This can be necessary to capture the black background.
        #(w, h) = self.canvas.dimensions
        #vertices = [(0, 0), (0, h), (w, h), (w, 0)]
        #rectangle = tkinter_shapes.Polygon(canvas=canvas, vertices=vertices)
        #rectangle['fill'] = rectangle['outline'] = 'black'
        
        # Update the canvas.
        self.canvas.update()
        
  

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
  


