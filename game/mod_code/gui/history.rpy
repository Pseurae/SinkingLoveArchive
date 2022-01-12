## History (history.rpy)
## ---------------------
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.

screen history(return_action=Return()):
    tag menu
    predict False
    style_prefix "history"

    use game_menu(_("{open_book}  History"), return_action):
        if _history_list:
            fixed:
                viewport align (0.5, 0.5):
                    id "history_vp"

                    mousewheel True
                    draggable True
                    yinitial 1.0

                    has vbox:
                        xfill True
                        spacing 10

                    for h in _history_list:
                        hbox:
                            label h.who or "" style "history_name"
                            text h.what

                vbar value YScrollValue("history_vp") xalign 0.975 yalign 0.5

        else:
            label _("The dialogue history is empty.") xalign 0.5 yalign 0.5

style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xsize 120

style history_name_text:
    font "mod_assets/gui/font/AlegreyaSansSC/AlegreyaSansSC-Regular.ttf"
    size 24

style history_text:
    xalign 0.0
    text_align 0.0
    xfill True
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_viewport:
    xysize (920, 500)

style history_side:
    spacing 50

style history_vscrollbar is vscrollbar:
    ysize 500
    unscrollable "hide"

style history_label_text:
    font "mod_assets/gui/font/AlegreyaSansSC/AlegreyaSansSC-Regular.ttf"