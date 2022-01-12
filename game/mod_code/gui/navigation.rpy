## Navigation
## ----------
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.

init python in nav_icons:
    from store.icon_res import nf_icon, fi_icon
    from renpy.config import self_closing_custom_text_tags

    self_closing_custom_text_tags["open_book"] = nf_icon("")
    self_closing_custom_text_tags["floppy"] = nf_icon("")
    self_closing_custom_text_tags["download"] = nf_icon("")
    self_closing_custom_text_tags["music_note"] = nf_icon("")
    self_closing_custom_text_tags["settings"] = nf_icon("")
    self_closing_custom_text_tags["message"] = nf_icon("")
    self_closing_custom_text_tags["message_text"] = nf_icon("")
    self_closing_custom_text_tags["new"] = fi_icon("")
    self_closing_custom_text_tags["quit"] = nf_icon("")

init python:
    def FinishEnterName():
        if not player: return
        persistent.playername = player
        renpy.hide_screen("name_input")
        renpy.jump_out_of_context("start")

    def NewGame():
        return If(persistent.playername, true=[ Start() ], false=[ With(dissolve_gui), Show(screen="name_input", ok_action=Function(FinishEnterName)) ])

screen navigation():
    vbox:
        style_prefix "navigation"

        xanchor 1.0
        xpos 1280 - gui.navigation_xpos
        yalign 0.8

        spacing gui.navigation_spacing

        use navigation_entry(
            "New Game", 
            "{new}", 
            NewGame()
        )

        use navigation_entry(
            "Load Game", 
            "{download}", 
            ShowMenu("load")
        )

        use navigation_entry(
            "Music", 
            "{music_note}", 
            ShowMenu("music_menu")
        )

        use navigation_entry(
            "Preferences", 
            "{settings}", 
            ShowMenu("preferences")
        )

        use navigation_entry(
            "Quit", 
            "{quit}", 
            Quit(confirm=not main_menu)
        )

style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")
    left_padding gui.navigation_button_left_padding
    right_padding gui.navigation_button_right_padding
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    hover_background Frame('mod_assets/gui/overlay/gradient.png')

style navigation_button_text:
    outlines []
    properties gui.button_text_properties("navigation_button")
    font gui.interface_font
    color "#fff"
    insensitive_color "#ccc"

screen navigation_entry(button_label, button_icon, button_action):
    style_prefix "navigation_entry"
    textbutton _("[button_label]"):
        action button_action
        hover_foreground HBox(
            Text(
                button_icon, 
                style="navigation_entry_hover_icon_text"
            ), 
            style="navigation_entry_hover_icon_hbox"
        )

style navigation_entry_button is navigation_button
style navigation_entry_button_text is navigation_button_text

style navigation_entry_hover_icon_hbox is empty
style navigation_entry_hover_icon_text is empty

style navigation_entry_button_text:
    xalign 0.5 yalign 0.5

style navigation_entry_hover_icon_hbox:
    xfill True yfill True

style navigation_entry_hover_icon_text:
    yalign 0.5
    xalign 0.95 
