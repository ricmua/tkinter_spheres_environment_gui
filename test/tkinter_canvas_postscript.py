""" Utility functionality for manipulating postscript data extracted from 
    Tkinter Canvases.
    
Examples
--------

Initialize a Tkinter interface.

>>> import tkinter
>>> root = tkinter.Tk()

Display a Tkinter canvas with a rectangle drawn on it.

>>> canvas = tkinter.Canvas(master=root)
>>> canvas.pack()
>>> rectangle = canvas.create_rectangle(100, 100, 200, 200)
>>> root.update()

Extract the postscript image data from the canvas.

>>> ps_a = extract(canvas)

Destroy the canvas and recreate it. Although the canvas will appear identical, 
this will cause some of the postscript metadata (e.g., `CreationDate`) to be 
re-written.

>>> canvas.destroy()
>>> canvas = tkinter.Canvas(master=root)
>>> canvas.pack()
>>> rectangle = canvas.create_rectangle(100, 100, 200, 200)
>>> root.update()

Extract the postscript image data from the canvas a second time.

>>> ps_b = extract(canvas)

Confirm that the raw postscript data differ.

>>> ps_a == ps_b
False

Confirm that the rendered postscript images are identical.

>>> equals(ps_a, ps_b)
True

Remove the rectangle from the canvas.

>>> canvas.delete(rectangle)
>>> canvas.update()

Extract the postscript image data from the canvas one more time.

>>> ps_c = extract(canvas)

Confirm that the newly-rendered postscript image does not match the prior two.

>>> equals(ps_a, ps_c)
False
>>> equals(ps_b, ps_c)
False

Cleanup.

>>> root.destroy()

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


## Load postscript image data from file.
#def load(filepath):
#    """ Load postscript image data from a file.
#    
#    Arguments
#    ---------
#    filepath : str
#        Path to a postscript image file.
#    
#    Returns
#    -------
#    ps : str
#        Postscript image data.
#    """
#    
#    # Load the postscript data.
#    with open(filepath, 'r') as f: ps = f.read()
#    
#    # Return the result.
#    return ps
#    
#  
#
## Save postscript image data to file.
#def save(ps, filepath):
#    """ Save postscript image data to a file.
#    
#    Arguments
#    ---------
#    ps : str
#        Postscript image data.    
#    filepath : str
#        Path to a postscript image file.
#    
#    Returns
#    -------
#    None
#    """
#    with open(filepath, 'w') as f: f.write(ps)
#    
#  
#

# Extract postscript data from a Tkinter Canvas.
def extract(canvas):
    """ Extract postscript data from a Tkinter Canvas.
    
    Arguments
    ---------
    canvas : tkinter.Canvase
        A Tkinter Canvas widget.
    
    Returns
    -------
    ps : str
        Postscript image data.    
    """
    return canvas.postscript(colormode='color')
    
  

# Convert postscript image data into a Python Imaging Library image object.
def convert_to_image(ps):
    """ Convert postscript image data into a [Python Imaging Library] image 
        object.
    
    Arguments
    ---------
    ps : str
        Postscript image data.
    
    Returns
    -------
    image : PIL.Image
        The postscript data rendered as a [Python Imaging Library] image object.
    
    References
    ----------
    [Python Imaging Library]: https://pillow.readthedocs.io/en/stable/
    """
    
    # Create a bytes buffer.
    image_buffer = io.BytesIO()
    
    # Create a codec writer to convert the postscript string into bytes.
    Writer = codecs.getwriter('utf-8')
    writer = Writer(image_buffer)
    
    # Write the postscript data to the buffer and rewind the position.
    print(ps, file=writer)
    image_buffer.seek(0)
    
    # Open the buffer as a PIL image object.
    image = PIL.Image.open(image_buffer) #, formats=['ps'])
    
    # Return the result.
    return image
    

# Test whether or not two postscript image data strings produce equivalent 
# rendered images.
def equals(ps_a, ps_b):
    """ Test whether or not two postscript image data strings produce 
        equivalent rendered images.
    
    The postscript image data are converted to rendered images. The postscript 
    strings are not compared directly, because non-visual information -- such 
    as metadata or comments -- might differ.
    
    Arguments
    ---------
    ps_a : str
        Postscript image data for the first image to compare.
    ps_b : str
        Postscript image data for the second image to compare.
    
    Returns
    -------
    equals : bool
        True if the images described by the two postscript strings are 
        visually-equivalent.
    """
    
    # Render image A from postscript data.
    image_a = convert_to_image(ps_a)
    
    # Render image B from postscript data.
    image_b = convert_to_image(ps_b)
    
    # Return the result.
    return (image_a.tobytes() == image_b.tobytes())
    
  

# __main__
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
  

