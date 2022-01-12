init python:
    class Interpolator(object):
        def __init__(self, duration):
            self.init_time = time.time()
            self.duration = duration

        def reset(self):
            self.init_time = time.time()

        @property
        def elapsed_time(self):
            return (time.time() - self.init_time) * renpy.display.core.time_mult

        @property
        def current_interpolation(self):
            interpolation = self.elapsed_time / self.duration

            # Clamp it between 0.0 and 1.0
            interpolation = max(interpolation, 0.0)
            interpolation = min(interpolation, 1.0)

            return interpolation

init python in sprite_wrapper:
    from store import NoRollback, Flatten

    wrappers = [ ]

    class ImplementAsWrapper(object):
        def __init__(self, priority=0):
            self.priority = priority

        def __call__(self, cls):
            global wrappers
            wrappers.append((self.priority, cls))
            return cls

    class SpriteWrapper(renpy.Displayable, NoRollback):

        def __init__(self, name, **kwargs):
            super(SpriteWrapper, self).__init__(**kwargs)
            self.name = name

        @property
        def current_attributes(self):
            return renpy.get_attributes(self.name, "master") or tuple()

        @property
        def is_talking(self):
            return renpy.get_say_image_tag() == self.name

        @classmethod
        def get_wrappers(cls):
            global wrappers
            wrappers = sorted(wrappers, key=lambda x: x[0])
            return filter(lambda x: x.apply_flag(), map(lambda x: x[1], wrappers))

        @classmethod
        def apply_flag(self):
            return False

        def turn_on_flag(self):
            return False

        def __call__(self, child):
            child = Flatten(child)

            for i in self.get_wrappers():
                child = i(child=child, name=self.name)

            return child

        def render(self, *args, **kwargs):
            renpy.error("%s cannot be rendered." % type(self))

    renpy.add_to_all_stores("SpriteWrapper", SpriteWrapper)
    renpy.add_to_all_stores("ImplementAsWrapper", ImplementAsWrapper)

init python in autofocus:
    from store import (
        _warper,
        Transform,
        BrightnessMatrix,
        Interpolator
    )
    import time

    class AutofocusBase(SpriteWrapper):
        characters = set()

        # `focused_data` -> <character name> -> <type of autofocus> -> boolean
        focused_data = { }

        minimum_char_requirement = 2
        condition_mismatch_behaviour = "focused"

        switch_tag = None # Disables the usage of the autofocus routine if applied to the sprite (Used in the subclasses)

        def __init__(self, child, name, *args, **kwargs):
            super(AutofocusBase, self).__init__(name, *args, **kwargs)
            self.child = renpy.displayable(child)
            self.characters.add(name)
            self.set_autofocus_vars()

        def set_autofocus_vars(self, levels=(0.0, 1.0), duration=1.0, warper=_warper.linear, **kwargs):
            self.levels = levels
            self.duration = duration
            self.warper = warper

            if isinstance(self.warper, basestring):
                self.warper = getattr(_warper, self.warper)

            self.target = self.levels[0] if self.focused else self.levels[1]
            self.current = self.previous = self.target

            self.interpolator = Interpolator(self.duration)

        def turn_on_flag(self):
            return self.switch_tag in self.current_attributes

        @staticmethod
        def lerp(start, end, coeff, warper):
            return start + (end - start) * warper(coeff)

        @classmethod
        def get_classname(cls):
            return cls.__name__

        @property
        def sufficient_active_characters(self):
            return len(filter(renpy.showing, self.characters)) >= self.minimum_char_requirement

        @property
        def focused(self):
            character_focused_data = self.focused_data.setdefault(self.name, { })

            return character_focused_data.setdefault(self.get_classname(), self.is_talking)

        @focused.setter
        def focused(self, value):
            self.focused_data.setdefault(self.name, { })[self.get_classname()] = value

        def set_focus_status(self, status):
            if self.focused != status:
                self.previous = self.target
                self.target = self.levels[0 if status is True else 1]
                self.interpolator.reset()

            self.focused = status

            return

        def handle_logic(self):
            if not self.sufficient_active_characters:
                behavior = (self.condition_mismatch_behaviour == "focused")
                self.set_focus_status(behavior)
            else:
                self.set_focus_status(self.is_talking)

        def process_child(self, child, coeff):
            renpy.error("Method not implemented.")

        def get_current_level(self):
            coeff = self.interpolator.current_interpolation
            return self.lerp(self.previous, self.target, coeff, self.warper)

        def render(self, width, height, st, at):
            renpy.redraw(self, 0)
            self.handle_logic()

            self.current = self.get_current_level()

            if self.turn_on_flag():
                child = self.process_child(self.child, self.current)
            else:
                child = self.child

            return renpy.render(child, width, height, st, at)

    @ImplementAsWrapper(1)
    class AutofocusZoom(AutofocusBase):
        switch_tag = "afz"
        condition_mismatch_behaviour = "unfocused"

        def __init__(self, child, name, *args, **kwargs):
            super(AutofocusZoom, self).__init__(child, name, *args, **kwargs)

            arguments = dict(
                levels=(1.05, 1.0),
                duration=0.25,
                warper=_warper.easein
            )
            self.set_autofocus_vars(**arguments)

        @classmethod
        def apply_flag(self):
            return True

        def process_child(self, child, level):
            return Transform(child, subpixel=True, zoom=level)

    @ImplementAsWrapper(1)
    class AutofocusFilter(AutofocusBase):
        switch_tag = "aff"

        def __init__(self, child, name, *args, **kwargs):
            super(AutofocusFilter, self).__init__(child, name, *args, **kwargs)

            arguments = dict(
                levels=(0.0, -0.1),
                duration=0.25,
                warper=_warper.easein
            )
            self.set_autofocus_vars(**arguments)

        @classmethod
        def apply_flag(self):
            return renpy.config.gl2

        def process_child(self, child, level):
            return Transform(child, subpixel=True, matrixcolor=BrightnessMatrix(level))

default hour = 0
default minute = 0

init python in time_of_day:
    from store import (
        TintMatrix,
        IdentityMatrix,
        SaturationMatrix,
        BrightnessMatrix,

        Transform,
        Color
    )

    @ImplementAsWrapper(0)
    class TimeOfDay(SpriteWrapper):
        FILTER_MAP = {
            "dawn": TintMatrix((102, 76, 127)) * SaturationMatrix(0.8),
            "day": IdentityMatrix(),
            "sunset": TintMatrix((255, 202, 202)),
            "evening": TintMatrix((131, 102, 127)) * BrightnessMatrix(0.25),
            "night": SaturationMatrix(0.8) * TintMatrix((115, 115, 165))
        }

        def get_time_of_day_tag(self):
            for tag in self.FILTER_MAP:
                if tag in self.current_attributes:
                    return tag

            return None

        def __init__(self, child, name, *args, **kwargs):
            super(TimeOfDay, self).__init__(name)
            self.child = renpy.displayable(child)

        def render(self, width, height, st, at):
            filter_type = self.get_time_of_day_tag()

            if filter_type is not None:
                child = Transform(self.child, matrixcolor=self.FILTER_MAP[filter_type])
            else:
                child = self.child

            return renpy.render(child, width, height, st, at)

        def per_interact(self):
            renpy.redraw(self, 0)

        @classmethod
        def apply_flag(cls):
            return renpy.config.gl2

init python in zorder_mouth:
    from renpy.config import start_callbacks

    class ZorderMouth(SpriteWrapper):

        autofm_manual_mouth_tags = [ "ma", "mb", "mc", "md", "me", "mf", "mg", "mh", "mi", 
                                     "mj", "mk", "ml", "mm", "mn", "mo", "mp", "mq", "mr" ]

        autozorder_switch_tag = "az"
        automouth_switch_tag = "am"

        def __init__(self, name, *args, **kwargs):
            super(ZorderMouth, self).__init__(name, **kwargs)

        def can_do_automouth(self):
            has_automouth_attribute = self.automouth_switch_tag in self.current_attributes
            other_mouth_applied = any([tag in self.autofm_manual_mouth_tags for tag in self.current_attributes])
            return has_automouth_attribute and not other_mouth_applied

        def can_do_autozorder(self):
            return self.autozorder_switch_tag in self.current_attributes

        def apply_zorder(self, zorder):
            # RenPy 7.4.3 has a dedicated function for this
            if "change_zorder" in dir(renpy):
                renpy.change_zorder(self.layer, self.name, zorder)
            else: # Use `renpy.show` if it doesn't exist, probably an older version
                renpy.show(self.name, layer=self.layer, zorder=zorder)

        def apply_mouth(self, mouth):
            renpy.show("{name} {mouth}".format(name=self.name, mouth=mouth), layer="master")

        def __call__(self, event, interact=True, **kwargs):
            if not interact:
                return

            def apply(zorder, mouth):
                if self.can_do_autozorder():
                    self.apply_zorder(zorder)

                if self.can_do_automouth():
                    self.apply_mouth(mouth)

            if event == "begin":
                apply(3, "om")

            elif event == "end":
                apply(2, "cm")

            del apply

    def apply_callback():
        from store import (
            s, n, y, m
        )

        for i in [ s, n, y, m ]:
            if not i.image_tag: continue
            i.display_args["callback"] = ZorderMouth(i.image_tag)

    start_callbacks.append(apply_callback)

