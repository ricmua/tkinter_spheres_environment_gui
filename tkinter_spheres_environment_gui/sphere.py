""" Wrapper for a circular Tkinter canvas object that exposes an interface 
    conforming with that defined by the Sphere class of the 
    `spheres_environment` package.

Maps Tkinter canvas coordinates to/from normalized coordinates.

Examples
--------

Initilialize a GUI.

>>> gui = tkinter_shapes.GUI()
>>> gui.dimensions = (800, 600)

Shapes are drawn on a canvas widget. Initialize a square canvas with a black 
background color.

>>> canvas = tkinter_shapes.Canvas(gui)
>>> canvas.dimensions = (600, 600)
>>> canvas.background_color = 'black'
>>> canvas.pack()
>>> gui.update()

Add a red Sphere to the canvas. The sphere should be visible, once the canvas 
has been updated.

>>> sphere = Sphere('sphere', canvas=canvas)
>>> sphere.color = (1, 0, 0, 1)
>>> canvas.update()

Verify `spheres_environment` properties.

>>> sphere
{'position': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'radius': 1.0}
>>> sphere.object_properties
['position', 'radius']

Re-size the sphere.

>>> sphere.radius = 0.1
>>> canvas.update()

Verify the size change.

>>> sphere.radius = sphere.radius * 2
>>> sphere.radius == 0.2
True
        
Re-position the sphere.

>>> sphere.position = (0.5, 0.5, 0.5)
>>> canvas.update()

Verify the position change.

>>> sphere.position
{'x': 0.5, 'y': 0.5, 'z': 0.5}

Clean up by destroying the shapes and the GUI.

>>> del sphere
>>> gui.destroy()

"""

# Copyright 2022-2023 Carnegie Mellon University Neuromechatronics Lab (a.whit)
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# 
# Contact: a.whit (nml@whit.contact)


# Import spheres environment
import spheres_environment

# Import wrappers for Tkinter shapes.
import tkinter_shapes



# Sphere class.
class Sphere(spheres_environment.Sphere):
    """ A `spheres_environment` interface for circular Tkinter canvas items. """
    
    def __init__(self, *args, canvas, **kwargs):
        
        # Initialize a circular canvas item with default attributes.
        self._circle = tkinter_shapes.Circle(canvas=canvas)
        
        # Invoke the superclass constructor.
        super().__init__(*args, **kwargs)
        
        # Set the default values of the circle to match those of the spheres 
        # environment.
        self.position = super().position
        self.radius = super().radius
        self.color = super().color
        
    @spheres_environment.Sphere.position.getter
    def position(self):
        """ Three dimensional position of the sphere, in normalized 
            coordinates. 
        
        Coordinate values lie in the range [-1.0, +1.0]. The third coordinate 
        (z) always assumes the last value set.
        """
        
        # Invoke the superclass property accessor.
        position = spheres_environment.Sphere.position.fget(self)
        
        # A choice was made here to store and return the position as a local 
        # variable due to the introduction of uncertainty in position, radius, 
        # and other measurements. This is due to the fact that `tkinter_shapes` 
        # calculates those quantities using the discretized pixel values. An 
        # alternative to this local storage approach that might reduce 
        # discrepancies between returned and expected values could be to fit a 
        # unit circle to the pixels (i.e., apply a circle constraint).
        
        ## Retrieve the current pixel coordinates of the circle center of mass.
        #(x, y) = self._circle.position
        #
        ## Transform pixel coordinates into normalized coordinates.
        #span = min(self._circle.canvas.dimensions)
        #(x, y) = (+1*(2*x/span - 1), 
        #          -1*(2*y/span - 1))
        #
        ## Update the position.
        #position.update(x=x, y=y)
        
        # Return the result.
        return position
    
    @position.setter
    def position(self, value):
        
        # Invoke the superclass property accessor.
        # Record the current values set (normalized coordinates).
        # This is useful for filling in the missing z dimension.
        spheres_environment.Sphere.position.fset(self, value)
        
        # Broadcast individual coordinate dimensions.
        (x, y, z) = (self['position'][k] for k in ['x', 'y', 'z'])
        
        # Convert normalized coordinates to pixel coordinates.
        span = min(self._circle.canvas.dimensions)
        (x, y) = ((+x+1)/2*span,
                  (-y+1)/2*span)
        
        # Set the pixel coordinates of the circle center of mass.
        self._circle.position = (x, y)
        
    @spheres_environment.Sphere.radius.getter
    def radius(self):
        """ Radius of the sphere, in normalized coordinates.
        
        When the radius is one, the circle exactly intersects with the edges of 
        the workspace.
        """
        
        # Invoke the superclass property accessor to ensure initialization.
        r = spheres_environment.Sphere.radius.fget(self)
        
        # A choice was made here to store and return the position as a local 
        # variable due to the introduction of uncertainty in position, radius, 
        # and other measurements. This is due to the fact that `tkinter_shapes` 
        # calculates those quantities using the discretized pixel values. An 
        # alternative to this local storage approach that might reduce 
        # discrepancies between returned and expected values could be to fit a 
        # unit circle to the pixels (i.e., apply a circle constraint).
        
        ## Retrieve the radius of the circle, in pixel coordinates.
        #r = self._circle.radius
        #
        ## Convert to normalized coordinates.
        #span = min(self._circle.canvas.dimensions)
        #r = r / span * 2
        
        # Return the result.
        return  r 
    
    @radius.setter
    def radius(self, value):
        
        # Invoke the superclass property accessor.
        # Record the current value (normalized coordinates).
        # This is useful for applying any superclass transforms.
        spheres_environment.Sphere.radius.fset(self, value)
        
        # Convert from normalized coordinates to pixel coordinates.
        span = min(self._circle.canvas.dimensions)
        r = self['radius'] * span / 2
        
        # Set the radius of the circle, in pixel coordinates.
        self._circle.radius = r
    
    @spheres_environment.Sphere.color.getter
    def color(self):
        """ Fill and outline color of the circle, represented as dict of 
            float values in the range [0.0, 1.0].
        """
        
        ## Invoke the superclass property accessor.
        #color = spheres_environment.Sphere.color.fget(self)
        
        assert self._circle['fill'] == self._circle['outline']
        alpha = 1.0 if self._circle['fill'] else 0.0
        to_rgb = self._circle.canvas.winfo_rgb
        color = to_rgb(self._circle['fill']) if alpha else (0, 0, 0)
        white = to_rgb('white')
        rgb = (c/w for (c, w) in zip(color, white)) 
        keys = ['r', 'g', 'b', 'a']
        return dict(zip(keys, (*rgb, alpha)))
    
    @color.setter
    def color(self, value):
        
        # Invoke the superclass property accessor.
        # Record the current value (normalized coordinates).
        # This is useful for applying any superclass transforms.
        spheres_environment.Sphere.color.fset(self, value)
        
        #assert isinstance(value, tuple) and (len(value) == 4)
        keys = ['r', 'g', 'b', 'a']
        value = dict(zip(keys, value)) if isinstance(value, tuple) else value
        assert isinstance(value, dict)
        assert (list(value) == keys)
        value = tuple(value[k] for k in keys)
        (r, g, b) = (round(255*min(max(c, 0), 1)) for c in value[:-1])
        #a = bool(value[-1])
        a = float(value[-1] > 0)
        color_string = f'#{r:02x}{g:02x}{b:02x}'.upper() if a else ''
        self._circle['fill'] = self._circle['outline'] = color_string
    
    def __del__(self):
        """ Sphere destructor cleans up and removes the circle from the 
            canvas. """
        del self._circle
        #super().__del__()
    
    def to_foreground(self, *args, **kwargs):
        """ Adjust the z-order of the circle on the canvas by raising to the 
            foreground.
        """
        item_id = self._circle.id
        self._circle.canvas.tag_raise(item_id, *args, **kwargs)
    
  

# Main.
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
  

