init python:
    class LinearGradient(renpy.Displayable):
        def __init__(self, first, last, **kwargs):
            super(LinearGradient, self).__init__(**kwargs)
            self.first = renpy.easy.color(first)
            self.last = renpy.easy.color(last)

        def render(self, width, height, st, at):
            width = max(self.style.xminimum, width)
            height = max(self.style.yminimum, height)

            rv = renpy.Render(width, height)

            tex = renpy.render(Solid("#000"), width, height, st, at)
            rv.blit(tex, (0, 0))

            rv.mesh = True
            rv.add_shader("sl.linear_gradient")
            rv.add_uniform("u_gradient_0", Color(self.first).rgba)
            rv.add_uniform("u_gradient_1", Color(self.last).rgba)
            rv.add_uniform("u_angle", 0.0)
            return rv

