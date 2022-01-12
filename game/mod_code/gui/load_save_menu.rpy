## Load and Save (load_save_menu.rpy)
## ----------------------------------
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.

screen save(return_action=Return()):

    tag menu

    use file_slots(_("{floppy}  Save"), return_action=return_action)


screen load(return_action=Return()):

    tag menu

    use file_slots(_("{download}  Load"), return_action=return_action)

screen file_slots(title, return_action=Return()):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use game_menu(title, return_action):

        frame background None:
            has fixed:
                ## This ensures the input will get the enter event before any of the
                ## buttons do.
                order_reverse True

            ## The page name, which can be edited by clicking on a button.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                xalign 0.5 yalign 0.55

                spacing 25

                for i in range(gui.file_slot_cols * gui.file_slot_rows):
                    $ slot = i + 1

                    button xsize 256 + 20 ysize 206:
                        action FileAction(slot)

                        vbox:
                            fixed xysize (256 + 20, 144 + 20):
                                add "mod_assets/gui/file_slots/outline.png" zoom 0.5
                                add FileScreenshot(slot) size (256, 144) xalign 0.5 yalign 0.5

                            null height 20

                            text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                                style "slot_time_text"

                            text FileSaveName(slot):
                                style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            hbox:
                xalign 0.5
                yalign 0.9

                style_prefix "page"

                spacing gui.page_spacing

                # textbutton _("<") action FilePagePrevious()

                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)

                # textbutton _(">") action FilePageNext()


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    yalign 0.125

style page_label_text:
    text_align 0.5
    layout "subtitle"
    size 20

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.button_text_properties("page_button")
    outlines []

style slot_button:
    properties gui.button_properties("slot_button")
    background Null()

style slot_button_text:
    properties gui.button_text_properties("slot_button")
    outlines []
