init -1400 python:

    @renpy.pure
    class ShowMenu(Action, DictEquality):
        def __init__(self, screen=None, *args, **kwargs):
            self.screen = screen
            self.transition = kwargs.pop("_transition", None)
            self.args = args
            self.kwargs = kwargs

        def predict(self):
            if renpy.has_screen(self.screen):
                if store._game_menu_screen:
                    renpy.predict_screen(store._game_menu_screen, *self.args, **self.kwargs)
                renpy.predict_screen(self.screen, *self.args, **self.kwargs)

        def __call__(self):

            if not self.get_sensitive():
                return

            orig_screen = screen = self.screen or store._game_menu_screen

            if not (renpy.has_screen(screen) or renpy.has_label(screen)):
                screen = screen + "_screen"

            if renpy.context()._menu:

                if renpy.has_screen(screen):

                    renpy.transition(self.transition or config.intra_transition, layer="screens")
                    renpy.show_screen(screen, _transient=True, *self.args, **self.kwargs)
                    renpy.restart_interaction()

                elif renpy.has_label(screen):
                    renpy.transition(config.intra_transition)

                    ui.layer("screens")
                    ui.remove_above(None)
                    ui.close()

                    renpy.jump(screen)

                else:
                    renpy.error("%r is not a screen or a label." % orig_screen)

            else:
                renpy.call_in_new_context("_game_menu", *self.args, _game_menu_screen=screen, **self.kwargs)

        def get_selected(self):
            screen = self.screen or store._game_menu_screen

            if screen is None:
                return False

            return renpy.get_screen(screen)

        def get_sensitive(self):
            screen = self.screen or store._game_menu_screen

            if screen is None:
                return False

            if screen in config.show_menu_enable:
                return eval(config.show_menu_enable[screen])
            else:
                return True