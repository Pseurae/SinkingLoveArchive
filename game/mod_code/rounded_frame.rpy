## Rounded Frame (rounded_frame.rpy)
## ---------------------------------
## Subclassed Frame which uses a shader to round the border corners.
## (Shader in `shaders/rounded_corners.rpy`)

init python:
    class RoundedFrame(Frame):
        def __init__(self, *args, **kwargs):
            super(RoundedFrame, self).__init__(*args, **kwargs)
            self.radius = 0.0

        def add_radius(self, radius):
            if isinstance(radius, (float, int)):
                self.radius = radius
            else:
                renpy.error("Expected float or int, got %s" % type(radius))
            return self

        def render(self, width, height, st, at):
            rv = super(RoundedFrame, self).render(width, height, st, at)

            if self.radius:
                rv.mesh = True
                rv.add_shader("sl.rounded_corners")

                if self.radius > 1.0:
                    rv.add_uniform("u_radius", self.radius * renpy.display.draw.draw_per_virt)
                else:
                    factor = rv.width * (height / width)
                    rv.add_uniform("u_radius", factor * self.radius * renpy.display.draw.draw_per_virt)

            return rv
