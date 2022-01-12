## Pause Menu (pause_menu.rpy)
## ---------------------------
## A menu used for displaying stats and navigating to other specific use menus.
## 
## Code for the stats system is in `pause_menu_core.rpy`

define _game_menu_screen = "pause_menu"

screen pause_menu():
    tag menu
    style_prefix "pause_menu"

    add "#0008"

    frame:
        use game_menu("Pause"):
            frame style_suffix "parent_frame":

                has hbox:
                    style "pause_menu_hbox"

                use pause_navigation()
                add RoundedFrame(gui.selected_color).add_radius(2):
                    xsize 2 ysize 450
                use pause_stats()

    key "game_menu" action Return()

style pause_menu_frame is empty:
    background None
    xsize 1020
    xalign 0.5

style pause_menu_parent_frame is empty:
    xmargin 75
    yfill True

style pause_menu_hbox is empty:
    spacing 50
    yalign 0.5

screen pause_navigation(return_action=ShowMenu("pause_menu")):
    style_prefix "pause_navigation"
    vbox:
        use pause_navigation_entry("Resume", Return())
        use pause_navigation_entry("Preferences", ShowMenu("preferences", return_action))
        use pause_navigation_entry("Main Menu", MainMenu())
        use pause_navigation_entry("History", ShowMenu("history", return_action))
        use pause_navigation_entry("Load Game", ShowMenu("load", return_action))
        use pause_navigation_entry("Save Game", ShowMenu("save", return_action))

style pause_navigation_vbox:
    spacing 30

screen pause_navigation_entry(button_label, button_action):
    style_prefix "pause_navigation_entry"
    textbutton _(button_label):
        at pause_navigation_entry_transform
        action button_action

transform pause_navigation_entry_transform():
    on idle:
        ease 0.1 matrixcolor BrightnessMatrix(0.0)
    on hover:
        ease 0.1 matrixcolor BrightnessMatrix(-0.1)

style pause_navigation_entry_button:
    # size_group "pause_navigation"
    xsize 200 ysize 50
    background RoundedFrame(gui.hover_color).add_radius(10.0)
    padding (20, 10)

style pause_navigation_entry_button_text:
    size 22
    xalign 0.5 yalign 0.5
    font "mod_assets/gui/font/AlegreyaSansSC/AlegreyaSansSC-Medium.ttf"
    kerning absolute(22 * 0.05)
    idle_color "#5A3C00"
    yoffset 2

screen pause_stats():
    style_prefix "pause_stats"

    vbox:
        use stats_container("Session Runtime", stats.Runtime)
        use stats_container("Total Progress", stats.TotalProgress)
        use stats_container("Current Track", stats.CurrentPlaying)

style pause_stats_vbox:
    spacing 25

screen stats_container(stat_label, disp_func):
    style_prefix "stats_container"
    hbox:
        label _("[stat_label]") xalign 0.0
        add disp_func() xalign 1.0 yalign 0.5

    add Solid(gui.hover_color):
        alpha 0.1
        xsize 565 ysize 2

style stats_container_vbox:
    spacing 15

style stats_container_hbox:
    spacing 15
    xfill True

style stats_container_label is empty
style stats_container_label_text is gui_label_text

style stats_container_label:
    size_group "stats"

style stats_container_label_text:
    size 24
    font "mod_assets/gui/font/AlegreyaSansSC/AlegreyaSansSC-Regular.ttf"

