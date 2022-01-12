## Globals (global.rpy)
## -------------------
## Contains common frameworks and functions.
##
## Contains 3 frameworks:
## - Common framework (SinkingLoveFramework)
## - Preferences (SinkingLovePreferences)
## - Config file (SinkingLoveExternalConfig)

default -10 persistent.sl_prefs = {
    "music_indicator": False,
    "discord_rpc": False
}

default current_day = 9
define gui.main_frame_border = Borders(25, 25, 25, 25)

style main_frame:
    background RoundedFrame(Solid("#2e3440")).add_radius(25.0)
    padding (25, 25)

define dissolve_gui = Dissolve(0.25, alpha=True)

define -5 sl_prefs = SinkingLovePreferences(persistent.sl_prefs) # Preferences
define -5 sl_config = SinkingLoveExternalConfig() # config file reader

init python in sl_framework:
    from store import (
        DiscordPresence
    )

    quit_label_callbacks = []
    pre_splash_callbacks = []

    def execute_callbacks(callbacks):
        for i in callbacks:
            i()

    def execute_quit_label_callbacks():
        global quit_label_callbacks
        execute_callbacks(quit_label_callbacks)

    def execute_pre_splash_callbacks():
        global pre_splash_callbacks
        execute_callbacks(pre_splash_callbacks)

    def formatted_date(day):
        import datetime
        return datetime.date(1912, 4, day).strftime("%d %b %Y")

    # discord_rpc = DiscordPresence()
    # discord_rpc.set_callbacks()
    # pre_splash_callbacks.append(discord_rpc.initialize_rpc)
    # quit_label_callbacks.append(discord_rpc.quit_callback)

init -10 python:
    class SinkingLovePreferences(object):
        __blacklist__ = [ "deserialized_done", "pref_dict" ]
        __slots__ = "music_indicator", "discord_rpc"

        def __init__(self, pref_dict):
            self.pref_dict = pref_dict

        # Screen Actions
        def SetPreferences(self, pref, value):
            return [ SetDict(self.pref_dict, pref, value) ]

        def TogglePreferences(self, pref, default_val=None):
            # Default it off before the action is called
            self.pref_dict.setdefault(pref, default_val)
            return [ ToggleDict(self.pref_dict, pref) ]

    import os, configparser

    class SinkingLoveExternalConfig(configparser.ConfigParser):
        default_config = {
            "STARTUP": {
                "disable_explorer": False
            },

            "ACCESSIBILITY": {
                "color_correction": "normal"
            },

            "MISC": {
                "lod_bias": -1.0,
                "fast_redraw_frames": 0,
                "disable_menu_blur": False
            }
        }

        def __init__(self, *args, **kwargs):
            super(SinkingLoveExternalConfig, self).__init__(*args, **kwargs)
            self.initialize()

        def initialize(self):
            self.read_dict(self.default_config)
            self.config_file_path = os.path.join(config.basedir, "sinkinglove.conf")

            try:
                self.read_conf()
            except IOError: 
                self.write_conf()

        def read_conf(self):
            with open(self.config_file_path, "r") as config_file:
                self.read_file(config_file)

        def write_conf(self):
            with open(self.config_file_path, "w+") as config_file:
                self.write(config_file)

# Icon fonts and glyph defines
init -10 python in icon_res:
    import renpy.exports as renpy
    from renpy.defaultstore import config

    nerdfont_font = "mod_assets/gui/font/DejaVu Sans-NerdFonts.ttf"
    feathericon_font = "mod_assets/gui/font/Feather.ttf"

    def nerdfont_tag(tag, arguments, contents):
        global powerline_font
        return [
                (renpy.TEXT_TAG, u"font=%s" % nerdfont_font),
            ] + contents + [
                (renpy.TEXT_TAG, u"/font"),
            ]

    config.custom_text_tags["nf"] = nerdfont_tag

    @renpy.curry
    def nf_icon(icon, tag, argument):
        return [ ( renpy.TEXT_TAG, "nf"), (renpy.TEXT_TEXT, icon), (renpy.TEXT_TAG, "/nf") ]

    def feathericon_tag(tag, arguments, contents):
        global feathericon_font
        return [
                (renpy.TEXT_TAG, u"font=%s" % feathericon_font),
            ] + contents + [
                (renpy.TEXT_TAG, u"/font"),
            ]

    config.custom_text_tags["fi"] = feathericon_tag

    @renpy.curry
    def fi_icon(icon, tag, argument):
        return [ ( renpy.TEXT_TAG, "fi"), (renpy.TEXT_TEXT, icon), (renpy.TEXT_TAG, "/fi") ]

    config.self_closing_custom_text_tags["cube"] = fi_icon("")
