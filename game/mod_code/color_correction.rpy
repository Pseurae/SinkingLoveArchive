## Color Correction (color_correction.rpy)
## ---------------------------------------
## Color blindness filters.

define persistent.correction_filter = None

init python:
    import difflib
    filters = {
        "normal": None,
        "protanopia": Matrix([0.567, 0.433, 0.0, 0.558, 0.442, 0.0, 0.0, 0.242, 0.758]),
        "protanomaly": Matrix([0.817, 0.183, 0.0, 0.333, 0.667, 0.0, 0.0, 0.125, 0.875]),
        "deuteranopia": Matrix([0.625, 0.375, 0.0, 0.7, 0.3, 0.0, 0.0, 0.3 ,0.7]),
        "deuteranomaly": Matrix([0.8, 0.2, 0.0,0.258, 0.742, 0.0, 0.0, 0.142, 0.858]),
        "tritanopia": Matrix([0.95 , 0.05, 0.0, 0.0, 0.433, 0.567, 0.0, 0.475, 0.525]),
        "tritanomaly": Matrix([0.967, 0.033, 0.0, 0.0, 0.733, 0.267, 0.0, 0.183, 0.817]),
        "achromatopsia": Matrix([0.299, 0.587, 0.114, 0.299, 0.587, 0.114, 0.299, 0.587, 0.114]),
        "achromatomaly": Matrix([0.618, 0.320, 0.062, 0.163, 0.775, 0.062, 0.163, 0.320, 0.516])
    }

    config_filter = sl_config.get("ACCESSIBILITY", "color_correction", fallback="normal")

    if config_filter not in filters:
        config_filter = difflib.get_close_matches(config_filter, filters.keys(), n=1)[0]
        sl_config["ACCESSIBILITY"]["color_correction"] = config_filter

    persistent.correction_filter = filters.get(config_filter, None)

python early hide:
    from functools import partial

    class ColorCorrectionWrapper(object):
        def __init__(self, func):
            self.func = func

        def __get__(self, obj, objtype):
            return partial(self.__call__, obj)

        def __call__(self, *args, **kwargs):
            rv = self.func(*args, **kwargs)

            if persistent.correction_filter is not None:
                if callable(persistent.correction_filter):
                    persistent.correction_filter = persistent.correction_filter()

                rv.mesh = True
                rv.add_shader("renpy.matrixcolor")
                rv.add_uniform("u_renpy_matrixcolor", persistent.correction_filter)

            return rv

    # renpy.display.render.render_screen = ColorCorrectionWrapper(renpy.display.render.render_screen)