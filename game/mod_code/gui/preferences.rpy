## Preferences (preferences.rpy)
## -----------------------------
## The preferences screen allows the player to configure the game to better suit
## themselves.

screen preferences(return_action=Return()):
    tag menu

    style_prefix "pref"

    use game_menu("{settings}  Preferences", return_action):
        use preferences_display()
        use preferences_skip()
        use preferences_general()
        use preferences_audio()
        use preferences_speed()

style preferences_label is empty
style preferences_label_text:
    font "mod_assets/gui/font/AlegreyaSansSC/AlegreyaSansSC-Regular.ttf"
    size absolute(24.0)

##############################################################################################
#- Sections ----------------------------------------------------------------------------------
##############################################################################################

define gui.preference_header_divider_spacing = 16

screen preferences_display():
    vbox:
        style "preferences_display_vbox"
        hbox spacing gui.preference_header_divider_spacing:
            text _("Display") style "preferences_label_text"
            add "preferences_header_divider" yalign 0.5

        null height 20

        hbox spacing 48:
            use big_imagebutton("preferences_fullscreen_icon", Preference("display", "fullscreen"), "Fullscreen")
            use big_imagebutton("preferences_windowed_icon", Preference("display", "window"), "Windowed")

style preferences_display_vbox is empty:
    xpos 171 ypos 115
    xsize 400 ysize 210

screen preferences_skip():
    vbox:
        style "preferences_skip_vbox"
        hbox spacing gui.preference_header_divider_spacing:
            text _("Skip") style "preferences_label_text"
            add "preferences_header_divider" yalign 0.5

        null height 20

        hbox spacing 48:
            use big_imagebutton("preferences_unseen_text_icon", Preference("skip", "toggle"), "Unseen Text")
            use big_imagebutton("preferences_after_choices_icon", Preference("after choices", "toggle"), "After Choices")

style preferences_skip_vbox is empty:
    xpos 171 ypos 400
    xsize 400 ysize 210

screen preferences_general():
    vbox:
        style "preferences_general_vbox"
        hbox spacing gui.preference_header_divider_spacing:
            text _("General") style "preferences_label_text"
            add "preferences_header_divider" yalign 0.5

        null height 18

        vbox spacing 12:
            use checkbox(sl_prefs.TogglePreferences("music_indicator", False), "Music Indication")
            use checkbox(sl_prefs.TogglePreferences("discord_rpc", False), "Rich Presence (Restart required)")


style preferences_general_vbox is empty:
    xpos 690 ypos 115
    xsize 400

screen preferences_audio():
    vbox:
        style "preferences_audio_vbox"
        hbox spacing gui.preference_header_divider_spacing:
            text _("Audio") style "preferences_label_text"
            add "preferences_header_divider" yalign 0.5

        null height 18

        vbox spacing 5:
            use audio_slider("music", "BGM")
            use audio_slider("sound", "Sound")
            use audio_slider("amb", "Surround")
            null height 10
            use checkbox(Preference("all mute", "toggle"), "Mute All")

style preferences_audio_vbox is empty:
    xpos 687 ypos 250
    xsize 400

screen preferences_speed():
    vbox:
        style "preferences_speed_vbox"
        hbox spacing gui.preference_header_divider_spacing:
            text _("Speed") style "preferences_label_text"
            add "preferences_header_divider" yalign 0.5

        null height 18

        vbox spacing 30:
            use speed_slider("Text", Preference("text speed"))
            use speed_slider("Auto", Preference("auto-forward time"))

style preferences_speed_vbox is empty:
    xpos 687 ypos 440
    xsize 400

##############################################################################################
#- Components --------------------------------------------------------------------------------
##############################################################################################

# Imagebutton with caption
screen big_imagebutton(_image, _action, _title):
    style_prefix "big_button"

    button:
        xysize (175, 132)
        action _action

        vbox spacing 9:
            at ContainerEventWrapper
            add _image
            text _(_title)

style big_button_button:
    padding (0, 0)
    xysize (175, 132)

style big_button_text:
    selected_idle_color gui.idle_color
    selected_hover_color gui.hover_color

    size 16 kerning 16 * 0.1
    xalign 0.5

# Check buttons
screen checkbox(_action, _text):
    style_prefix "check"

    button:
        action _action
        hbox at ContainerEventWrapper:
            spacing 15

            add "checkbox"
            text _(_text) style "check_button_text"

style check_button is empty:
    padding (0, 0)
    # left_padding 30
    # background "checkbox"

style check_button_text:
    selected_idle_color gui.idle_color
    selected_hover_color gui.hover_color

    size 16 kerning 16 * 0.1

# Slider style
style preferences_slider is bar

transform slider_animation:
    on idle:
        ease 0.25 matrixcolor BrightnessMatrix(0.0)

    on hover:
        ease 0.25 matrixcolor BrightnessMatrix(0.15)

# Sliders for audio (<title>  -*------------------)
screen audio_slider(_mixer, _title):
    hbox spacing 40:
        label _(_title) style "audio_slider_label"
        bar style "audio_slider_bar" value MixerValue(_mixer) yalign 0.5 at slider_animation

style audio_slider_label:
    size_group "audio_slider_text"

style audio_slider_label_text:
    size 16 kerning 16 * 0.1

style audio_slider_bar is preferences_slider

# Slider for speed settings
# Slow          <title>          Fast
# -----------------------------------
screen speed_slider(_title, _value):
    vbox spacing 16:

        hbox xfill True:
            label _("Slow") xalign 0.0 style "speed_slider_label"
            label _(_title) xalign 0.5 style "speed_slider_label"
            label _("Fast") xalign 1.0 style "speed_slider_label"

        bar value _value style "speed_slider_bar" at slider_animation

style speed_slider_bar is preferences_slider
style speed_slider_label:
    padding (0, 0)

style speed_slider_label_text:
    size 16 kerning 16 * 0.1

##############################################################################################
#- Images ------------------------------------------------------------------------------------
##############################################################################################

image checkbox:
    subpixel True
    zoom 0.5 yoffset -1
    on idle:
        "mod_assets/gui/preferences/checkbox_unchecked.png" with dissolve_gui

    on hover:
        "mod_assets/gui/preferences/checkbox_unchecked.png" with dissolve_gui

    on selected_idle:
        "mod_assets/gui/preferences/checkbox_checked.png" with dissolve_gui

    on selected_hover:
        "mod_assets/gui/preferences/checkbox_checked.png" with dissolve_gui

image preferences_header_divider:
    RoundedFrame(Solid("#E0A733")).add_radius(1)
    ysize 2

image preferences_fullscreen_icon:
    subpixel True
    zoom 0.5

    on idle:
        "mod_assets/gui/preferences/icons/icon_fullscreen_idle.png" with dissolve_gui

    on hover:
        "mod_assets/gui/preferences/icons/icon_fullscreen_hover.png" with dissolve_gui

    on selected_idle:
        "mod_assets/gui/preferences/icons/icon_fullscreen_selected.png" with dissolve_gui

    on selected_hover:
        im.Alpha("mod_assets/gui/preferences/icons/icon_fullscreen_selected.png", 0.6) with dissolve_gui

image preferences_windowed_icon:
    subpixel True
    zoom 0.5
    alpha 1.0

    on idle:
        "mod_assets/gui/preferences/icons/icon_windowed_idle.png" with dissolve_gui

    on hover:
        "mod_assets/gui/preferences/icons/icon_windowed_hover.png" with dissolve_gui

    on selected_idle:
        "mod_assets/gui/preferences/icons/icon_windowed_selected.png" with dissolve_gui

    on selected_hover:
        im.Alpha("mod_assets/gui/preferences/icons/icon_windowed_selected.png", 0.60) with dissolve_gui

image preferences_unseen_text_icon:
    subpixel True
    zoom 0.5

    on idle:
        "mod_assets/gui/preferences/icons/icon_unseen_text_idle.png" with dissolve_gui

    on hover:
        "mod_assets/gui/preferences/icons/icon_unseen_text_hover.png" with dissolve_gui

    on selected_idle:
        "mod_assets/gui/preferences/icons/icon_unseen_text_selected.png" with dissolve_gui

    on selected_hover:
        im.Alpha("mod_assets/gui/preferences/icons/icon_unseen_text_selected.png", 0.6) with dissolve_gui

image preferences_after_choices_icon:
    subpixel True
    zoom 0.5

    on idle:
        "mod_assets/gui/preferences/icons/icon_after_choices_idle.png" with dissolve_gui

    on hover:
        "mod_assets/gui/preferences/icons/icon_after_choices_hover.png" with dissolve_gui

    on selected_idle:
        "mod_assets/gui/preferences/icons/icon_after_choices_selected.png" with dissolve_gui

    on selected_hover:
        im.Alpha("mod_assets/gui/preferences/icons/icon_after_choices_selected.png", 0.6) with dissolve_gui

##############################################################################################
#- Misc --------------------------------------------------------------------------------------
##############################################################################################

init python:
    class ContainerEventWrapper(renpy.Displayable):
        """
        Transform events don't propogate through containers (i.e, hbox, vbox, fixed etc).
        This class fixes that by applying the events manually to all the children of the
        specified container.
        """

        def __init__(self, container, **properties):
            super(ContainerEventWrapper, self).__init__(**properties)
            self.container = container

        def set_style_prefix(self, prefix, root):
            super(ContainerEventWrapper, self).set_style_prefix(prefix, root)
            for child in self.container.children:
                child.set_style_prefix(prefix, root)

        def set_transform_event(self, event):
            super(ContainerEventWrapper, self).set_transform_event(event)
            for child in self.container.children:
                child.set_transform_event(event)

        def focus(self, default=False):
            super(ContainerEventWrapper, self).focus(default)
            for child in self.container.children:
                child.focus(default)

        def unfocus(self, default=False):
            super(ContainerEventWrapper, self).unfocus(default)
            for child in self.container.children:
                child.unfocus(default)

        def render(self, *args):
            return renpy.render(self.container, *args)