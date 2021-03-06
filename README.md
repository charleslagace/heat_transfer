# heat_transfer
Visual simulation of heat diffusion.

<h3>Heat Trasfer Simulation Guidelines</h3>

<p>
The purpose of this program is to generate a 2-dimensional heat map.
To do this, you just need to add the objects and windows you want and to
specify the temperature of the field. Where there is an object, the initial
temperature will be the one you specified for the object. Otherwise,
the initial temperature will simply be the temperature of the field. Where
there is a window, the temperature variation over time won't be null at the
borders of the heat map. It will depend on the outside temperature.</p>
<p>
To add an object, open the <i>Object</i> menu and click on <i>Add Object</i>.
This will open a new window where you are asked to specify the name, the x-
and y- position, the x- and y- dimensions, and the temperature of this object.
The position will determine where the object will be centered, and the dimensions
will define its length and its width. The object you just created will appear on
the heat map with a red border. After at least one object has been created, you
can also modify or delete an object in the same menu.</p>
<p>
You can add a window in a similar way, using the <i>Window</i> menu. For a
given window, you can specify the name, the side - either left, right, top,
or bottom, the lower or left edge, and the upper or right edge. For instance,
if the side is left, the window will apppear on the left border of the heat
map between the lower and upper y-values. Like objects, windows can be modified
or deleted with the appropriate commands.</p>
<p>
It is also possible to export all the temperature values at some specific
points in the field. To do so, use the <i>Follow Point</i> command in the <i>File</i>
menu, then enter the (x, y) coordinate that you wish to follow. While the
simulation is running, the temperature at each time incrementation will be
sent to a work sheet in Excel. You can save this sheet on your computer at
any time, using the <i>Export</i> command. You can also follow more than one
point if you want; in this case, the temperature values for each point will
appear in different columns of the Excel work sheet.</p>
<p>
After you added all everything you want, click on the Start Simulation button.
The initial temperature field will be generated. Then, an algorithm will
determine the color for each pixel based on its temperature and show the
initial 2-dimensional map. Then another algorithm based on discrete
incrementation of temperature derivatives over position and time will
determine the new temperature for each point after a small increment, which
will produce a new temperature field. The same color algorithm will receive
these new values and generate a new heat map. This process will continue
until you decide either to pause the simulation - in which case you can resume
it later - or to end it - in which case the temperature data and the heat map
will be deleted.</p>
