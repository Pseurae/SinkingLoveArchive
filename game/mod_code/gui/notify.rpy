## Notify (notify.rpy)
## -------------------
## The notify screen is used to show the player a message. (For example, when
## the game is quicksaved or a screenshot has been taken.)

screen notify(message, trans=notify_appear):

    zorder 100
    style_prefix "notify"

    frame at trans:
        vbox:

            label _(message) yalign 0.5

    button at trans:
        action Hide('notify')
        add "notify_close_button_image"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .25 alpha 0.0

style notify_frame is empty
style notify_button is empty
style notify_label is empty

style notify_frame:
    xanchor 1.0 yanchor 0.0
    xpos 0.975 ypos 0.025
    background RoundedFrame("game_menu_frame_background").add_radius(10.0)
    padding (15, 15)


style notify_button:
    xanchor 0.5 yanchor 0.5
    xpos 0.975 ypos 0.025

style notify_label_text:
    size gui.notify_text_size

style notify_bar is empty:
    left_bar "notify_timer_thumb"
    right_bar "notify_timer_background"
    ysize 2

screen track_notify(message, trans=notify_appear):

    zorder 100
    style_prefix "track_notify"

    frame at trans:
        vbox xminimum 400:
            hbox spacing 16:
                add "notify_music"
                label _(message) yalign 0.5

            null height 18

    button at trans:
        action Hide('track_notify')
        add "notify_close_button_image"

    timer 3.25 action Hide('track_notify')

style track_notify_frame is empty
style track_notify_button is empty
style track_notify_label is empty

style track_notify_frame:
    xanchor 0.0 yanchor 0.0
    xpos 0.025 ypos 0.025
    background RoundedFrame("game_menu_frame_background").add_radius(20.0)
    padding (15, 15)

style track_notify_button:
    xanchor 0.5 yanchor 0.5
    xpos 0.04 ypos 0.025

style track_notify_label_text:
    size gui.notify_text_size

style track_notify_bar is empty:
    left_bar "notify_timer_thumb"
    right_bar "notify_timer_background"
    ysize 2

##############################################################################################
#- Images ------------------------------------------------------------------------------------
##############################################################################################

image notify_message:
    "mod_assets/gui/notify/message_bubble.png"
    zoom 0.5

image notify_music:
    "mod_assets/gui/choices/note.png"
    zoom 0.3

image notify_close_button_image:
    subpixel True
    zoom 0.3
    xoffset -5
    yoffset 10
    on idle:
        "mod_assets/gui/game_menu/close_idle.png" with dissolve

    on hover:
        "mod_assets/gui/game_menu/close_hover.png" with dissolve
