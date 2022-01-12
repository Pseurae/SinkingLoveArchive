## Layer Blurring (layer_blur.rpy)
## ---------------------------
## Used for layering an entire layer without needing to use `renpy.show_layer_at`.
## (Shader in `shaders/gaussian.rpy`)

define override_blur = False

python early hide:
    from functools import partial
    import math

    # For the actual blur
    class BlurWrapper(object):
        def __init__(self, func):
            self.func = func

            self.radius = 20.0
            self.sqr_sigma = (self.radius / 2.0) ** 2.0
            self.norm_coeff = 1.0 / math.sqrt(2.0 * math.pi * self.sqr_sigma)

            if isinstance(func, type(self)):
                self.func = func.func

        def __call__(self, *args, **kwargs):
            render = self.func(*args, **kwargs)

            for s in [ "sl.gaussian_h", "sl.gaussian_v" ]:
                cr = render

                render = renpy.Render(*cr.get_size())
                render.mesh = True
                render.blit(cr, (0, 0))
                render.add_shader("-renpy.texture")
                render.add_shader("-renpy.geometry")
                render.add_shader(s)
                render.add_uniform("u_radius", self.radius)
                render.add_uniform("u_norm_coeff", self.norm_coeff)
                render.add_uniform("u_sqr_sigma", self.sqr_sigma)

            return render

        def __get__(self, instance, owner):
            return partial(self.__call__, instance)

    # For hooking up to the function
    class LayerBlurWrapper(NoRollback):
        def __init__(self, func):
            if hasattr(func, "func"):
                func = func.func

            self.func = func

        def __get__(self, obj, objtype):
            return partial(self.__call__, obj)

        def get_config_flag(self):
            sl_config = getattr(store, "sl_config", None)
            if not sl_config:
                return False

            return not sl_config.getboolean("MISC", "disable_menu_blur", fallback=False)

        def on_game_menu(self):
            return not main_menu and renpy.get_screen("menu")

        def __call__(self, obj, layer, properties):
            rv = self.func(obj, layer, properties)

            if layer == "master":
                on_correct_screen = (self.on_game_menu() or renpy.get_screen("modal"))
                if (self.get_config_flag() and on_correct_screen and not renpy.get_on_battery()) or getattr(store, "override_blur", False):
                    rv.render = BlurWrapper(rv.render)

            return rv

    renpy.display.core.SceneLists.make_layer = LayerBlurWrapper(renpy.display.core.SceneLists.make_layer)