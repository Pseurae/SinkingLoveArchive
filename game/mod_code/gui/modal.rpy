## Modal screens
## -------------
## Screens used to get the player's input.
##
## Contains 3 screens:
## - Name Input
## - Dialog
## - Confirm

init python in _modal_blur:
    import io, threading

    from renpy.display.scale import smoothscale
    from renpy.display.render import mutated_surface
    from renpy.display.im import Blur, Data
    from renpy.display.module import save_png
    from store import NoRollback, Null

    from renpy.exports import invoke_in_thread
    from renpy.config import start_interact_callbacks

    modal_screenshot_data = None

    def clear_screenshot_data(*args, **kwargs):
        global modal_screenshot_data
        modal_screenshot_data = None

    start_interact_callbacks.append(clear_screenshot_data)

    def nostore_screenshot():
        global modal_screenshot_data
        if not modal_screenshot_data:
            surf = renpy.display.draw.screenshot(renpy.game.interface.surftree) # Draw is initiated after start
            surf = smoothscale(surf, (renpy.config.thumbnail_width, renpy.config.thumbnail_height))
            mutated_surface(surf)

            with io.BytesIO() as sio:
                save_png(surf, sio, 0)
                modal_screenshot_data = sio.getvalue()

        return modal_screenshot_data

    def modal_bg():
        return Blur(Data(nostore_screenshot(), "screenshot.png"), 3.0)

screen modal_frame(title, can_close=True, frame_width=None, return_action=Return()):
    style_prefix "modal_frame"

    add "#0008"

    frame:
        if frame_width:
            xsize frame_width

        vbox:
            hbox spacing gui.preference_header_divider_spacing:
                text _(title) style "preferences_label_text"
                add "preferences_header_divider" yalign 0.5

            null height 15
            transclude

style modal_frame_frame:
    background RoundedFrame("game_menu_frame_background").add_radius(10.0)
    xalign 0.5 yalign 0.5
    padding (25, 20, 25, 20)

screen name_input(ok_action):
    tag modal

    modal True

    zorder 200

    style_prefix "name_input"

    key "K_RETURN" action [ Play("sound", gui.activate_sound), ok_action ]

    use modal_frame("Name", can_close=False, frame_width=420):

        vbox:
            xalign 0.5 yalign 0.5
            spacing 20


            frame:
                has vbox
                input default "" value VariableInputValue("player"):
                    style "name_input"
                    xalign 0.0 yalign 0.5
                    length 12
                    allow "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

            textbutton _("Ok"):
                xalign 0.5
                action ok_action

style name_input_frame:
    xsize 280
    background Transform(RoundedFrame(Solid("#DCC8A0")).add_radius(25.0), alpha=0.2)
    padding (12, 10)

style name_input:
    font gui.interface_font
    size 18
    color "#fff"

    caret HBox(Null(width=2), "name_input_caret")
    kerning 18 * 0.1

image name_input_caret:
    Solid("#DCC8A0")
    yoffset 1
    xsize 1 ysize 18
    block:
        linear 0.35 alpha 0
        linear 0.35 alpha 1
        repeat

style modal_label_text:
    text_align 0.5
    size 18
    kerning 18 * 0.1

screen dialog(message, ok_action):
    tag modal

    modal True
    style_prefix "dialog"

    zorder 200

    use modal_frame("{size=20}{message}{/size}  Dialog", can_close=False, frame_width=600):

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _(message):
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("Ok") action ok_action

style dialog_label is empty
style dialog_label_text is modal_label_text

style dialog_button is empty:
    xalign 0.5

screen confirm(message, yes_action, no_action):
    tag modal

    modal True
    style_prefix "confirm"

    zorder 200

    use modal_frame("{size=20}{message_text}{/size}  Confirm", can_close=False, frame_width=600):

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _(message):
                xalign 0.5

            vbox spacing 10:
                xalign 0.5

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    key "game_menu" action no_action

style confirm_label is empty
style confirm_label_text is modal_label_text

style confirm_button is empty:
    xalign 0.5

## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen fake_skip_indicator():
    use skip_indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 6

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat

style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    font "DejaVuSans.ttf"
