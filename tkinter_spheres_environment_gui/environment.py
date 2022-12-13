""" Wrapper for a Tkinter-based environment GUI that exposes an interface 
    conforming with that defined by the `spheres_environment` package.

Examples
--------

Initialize a virtual environment.

>>> environment = Environment()

Verify that the environment is empty

>>> environment
{}

Add a sphere object to the environment.

>>> sphere = environment.initialize_object('sphere')
>>> sphere == environment['sphere']
True

Verify that the environment now contains an object.

>>> list(environment)
['sphere']

Verify the properties of the sphere object.

>>> sphere.object_properties
['position', 'radius']

Verify the default values of the sphere object.

>>> sphere
{'position': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'radius': 1.0}

Change the properties from the default values.

>>> sphere.position = (1, 2, 3)
>>> sphere.radius = 2
>>> sphere
{'position': {'x': 1.0, 'y': 2.0, 'z': 3.0}, 'radius': 2.0}

Add a second object to the environment.

>>> other = environment.initialize_object('other')
>>> list(environment)
['sphere', 'other']
>>> sphere == environment['other']
False
>>> other == environment['other']
True

Remove the second object from the environment.

>>> environment.destroy_object('other')
>>> list(environment)
['sphere']

Cleanup by destroying the environment.

>>> del environment

"""

# Copyright 2022 Carnegie Mellon University Neuromechatronics Lab (a.whit)
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# 
# Contact: a.whit (nml@whit.contact)


# Spheres environment imports.
import spheres_environment

# Local imports.
from tkinter_spheres_environment_gui.gui import GUI
from tkinter_spheres_environment_gui.sphere import Sphere


# Environment class.
class Environment(spheres_environment.Environment):
    """ 2D canvas GUI.
    """
    
    object_type_map = dict(sphere=Sphere)
    
    def __init__(self, *args, gui_kwargs={}, **kwargs):
        
        # Initialize a GUI canvas.
        self.gui = GUI(**gui_kwargs)
        
        # Re-size the GUI canvas.
        self.gui.canvas.dimensions = (600, 600)
        
        # Invoke the superclass constructor.
        super().__init__(*args, **kwargs)
        
    def initialize_object(self, *args, **kwargs):
        
        # Add the GUI canvas as a keyword argument to the Sphere constructor.
        kwargs = {'canvas': self.gui.canvas, **kwargs}
        
        # Invoke the superclass method.
        obj = super().initialize_object(*args, **kwargs)
        
        # Return the result.
        return obj
        
    def update(self):
        """ Update the GUI canvas. """
        
        # Update the canvas.
        self.gui.canvas.update()
    
    def __del__(self):
        """ Cleanup by destroying canvas objects and the GUI. """
        
        # Destroy canvas items.
        for obj in self: del obj
        
        # Destroy the canvas.
        self.gui.destroy()
    
  

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
  


