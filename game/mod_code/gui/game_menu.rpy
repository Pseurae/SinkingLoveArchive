## Game Menu (game_menu.rpy)
## -------------------------
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.

screen game_menu(title, return_action=Return()):
    add "game_menu_frame_background"

    label _(title) style "game_menu_label" at move_top

    frame:
        style "game_menu_content_frame"
        fixed at fadein_screen:
            transclude

    use game_menu_ending_decor(title)

    button action return_action:
        style "game_menu_close_button"

        add "game_menu_close_button_image"

    key "game_menu" action return_action

screen game_menu_ending_decor(title):
    hbox spacing 18:
        yalign 0.96 xalign 0.5

        at transform:
            alpha 0.25
            move_bottom

        add "game_menu_ending_divider_left" yalign 0.5
        label _(title) style "game_menu_ending_label"
        add "game_menu_ending_divider_right" yalign 0.5

transform fadein_screen():
    subpixel True
    xalign 0.5 yalign 0.5

    alpha 0.0
    1.5
    easein_quad 0.75 alpha 1.0
    subpixel False

transform move_top():
    subpixel True
    crop_relative True

    yoffset 275 
    crop (0.5, 0.0, 0.0, 1.0)
    0.5
    easein_quad 0.25 crop (0.0, 0.0, 1.0, 1.0)
    0.25
    easein_quad 0.75 yoffset 0

transform move_bottom():
    subpixel True
    crop_relative True

    yoffset -275
    crop (0.5, 0.0, 0.0, 1.0)
    0.5
    easein_quad 0.25 crop (0.0, 0.0, 1.0, 1.0)
    0.25
    easein_quad 0.75 yoffset 0

style game_menu_content_frame is empty:
    yfill True
    xalign 0.5 yalign 0.5
    padding (0, 0)

style game_menu_label:
    xalign 0.5 ypos 40

style game_menu_label_text:
    font "mod_assets/gui/font/AlegreyaSansSC/AlegreyaSansSC-Medium.ttf"
    size absolute(28.0)

style game_menu_ending_label is empty
style game_menu_ending_label_text is game_menu_label_text

style game_menu_close_button:
    xpos 1205 ypos 35
    xsize 40 ysize 40

image game_menu_close_button_image:
    subpixel True
    zoom 0.5
    xoffset -8 yoffset -8
    on idle:
        "mod_assets/gui/game_menu/close_idle.png" with dissolve

    on hover:
        "mod_assets/gui/game_menu/close_hover.png" with dissolve

image game_menu_frame_background:
    subpixel True
    LinearGradient("#2e2e2e", "#2e2e2ef2")

image game_menu_ending_divider_left:
    "mod_assets/gui/game_menu/line.png"
    zoom 0.5

image game_menu_ending_divider_right:
    "mod_assets/gui/game_menu/line.png"
    zoom 0.5
    rotate 180.0 rotate_pad False transform_anchor True
