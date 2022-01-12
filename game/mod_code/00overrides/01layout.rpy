init python:

    @layout
    def yesno_screen(message, yes=None, no=None):
        if config.confirm_screen and renpy.has_screen('confirm'):
            screen = "confirm"
        elif renpy.has_screen("yesno_prompt"):
            screen = "yesno_prompt"
        else:
            screen = None

        if screen is not None:

            yes_action = [ Hide(screen, config.exit_yesno_transition) ]
            no_action = [ Hide(screen, config.exit_yesno_transition) ]

            if yes is not None:
                yes_action.append(yes)
            if no is not None:
                no_action.append(no)

            if config.enter_yesno_transition:
                renpy.transition(config.enter_yesno_transition)

            if renpy.context()._menu:
                renpy.show_screen(
                    screen,
                    message=message,
                    yes_action=yes_action,
                    no_action=no_action
                )
                renpy.restart_interaction()

            else:
                renpy.call_in_new_context(
                    "_confirm_screen", 
                    message=message,
                    yes_action=yes_action,
                    no_action=no_action + [ Return() ])

            return

        if renpy.invoke_in_new_context(layout.invoke_yesno_prompt, None, message):
            if yes is not None:
                yes()
        else:
            if no is not None:
                no()


    def __auto_save_extra_info():
        return save_name

    config.auto_save_extra_info = __auto_save_extra_info


label _confirm_screen(*args, **kwargs):
    window hide None
    call screen confirm(*args, **kwargs)
    window show
