## Base Screens (screens.rpy)
## --------------------------
## Contains common screens.
## Special purpose and heavily edited screens are in `mod_code/gui`

## Initialization

init offset = -1

## Styles

style default:
    font gui.default_font
    size gui.text_size
    color gui.text_color
    line_overlap_split 1
    line_spacing 1
    hinting "none"

style default_monika is normal:
    slow_cps 30

style normal is default:
    xpos gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos

    layout ("subtitle" if gui.text_xalign else "tex")

style input:
    color gui.accent_color

style hyperlink_text:
    color gui.accent_color
    hover_color gui.hover_color
    hover_underline True

style splash_text:
    size 24
    color gui.accent_color
    font gui.default_font
    text_align 0.5
    outlines []

style poemgame_text:
    yalign 0.5
    font "gui/font/Halogen.ttf"
    size 30
    color "#000"
    outlines []

    hover_xoffset -3
    hover_outlines [(3, "#fef", 0, 0), (2, "#fcf", 0, 0), (1, "#faf", 0, 0)]

style gui_text:
    font gui.interface_font
    color gui.interface_text_color
    size gui.interface_text_size

style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.button_text_properties("button")
    yalign 0.5

style label_text is gui_text:
    color gui.accent_color
    size gui.label_text_size

style prompt_text is gui_text:
    color gui.text_color
    size gui.interface_text_size

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

image slider_base_bar:
    contains:
        RoundedFrame(Solid("#DCC8A0"), tile=False).add_radius(1)
        ysize 2 yalign 0.5

    ysize 16

image slider_thumb:
    transform_anchor True rotate_pad False

    Solid("#DCC8A0")
    size (11, 11)

    xoffset absolute(5.5) yoffset absolute(5.5)
    rotate 45.0

style bar:
    ysize 16
    base_bar "slider_base_bar"
    thumb "slider_thumb"
    thumb_offset 4

    left_gutter 3
    right_gutter 3

image vscrollbar_thumb:
    RoundedFrame(Solid("#E0A733"), tile=True).add_radius(3)
    xsize 6

image vscrollbar_base_bar:
    RoundedFrame(Solid("#DCC8A0"), tile=True).add_radius(3)
    xsize 6

style scrollbar:
    ysize 18
    thumb Transform("vscrollbar_thumb", transform_anchor=True, rotate=90)
    base_bar Transform("vscrollbar_base_bar", transform_anchor=True, rotate=90)
    unscrollable "hide"

style vscrollbar:
    xsize 18
    xalign 1.0

    base_bar "vscrollbar_base_bar"
    thumb "vscrollbar_thumb"

    thumb_offset 5
    top_gutter 5 bottom_gutter 5
    unscrollable "hide"

style frame:
    padding gui.frame_borders.padding

## In-Game Screens

# Say Screen

# This screen is used to show dialogue to the player.
# It takes two variables 'who' and 'what', where 'who' is the
# character speaking and 'what' the text they are saying.
# (Who can be set to None if no name is given)

# This screen must create a text displayable with id "what", as Ren'Py uses
# this to manage text display. It can also create displayables with id "who"
# and id "window" to apply style properties.

## https://www.renpy.org/doc/html/screen_special.html#say

screen date_display():
    style_prefix "date_display"
    vbox:
        text _(sl_framework.formatted_date(current_day))

style date_display_vbox:
    xcenter 200 yalign 0.9

style date_display_text:
    font "mod_assets/gui/font/AlegreyaSansSC/AlegreyaSansSC-Regular.ttf"

screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        text what id "what"

        if who is not None:
            window:
                style "namebox"
                text who id "who" style 'say_dialogue'

    # If there's a side image, display it above the text. Do not display
    # on the phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0

    use date_display()

    vbox style "quick_menu_container":
        use quick_menu

style quick_menu_container:
    xanchor 0.5 xpos 0.525
    yalign 0.99

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label

style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("mod_assets/gui/textbox.png", xalign=0.5, yalign=1.0)

style window_monika is window:
    background Image("gui/textbox_monika.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    ypos gui.name_ypos

style say_label:
    color gui.accent_color
    font gui.name_font
    size gui.name_text_size
    xalign gui.name_xalign
    yalign 0.5
    outlines [(3, "#48a9c8", 0, 0), (1, "#48a9c8", 1, 1)]

style say_dialogue:
    font gui.dialogue_font

    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos

    hinting 'bytecode'
    # outlines [(2, "#00000088", 0, 0)]
    outlines [(0, "#0000", 0, 0)]

    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

image ctc:
    xalign 0.91 yalign 0.925 xoffset -5 alpha 0.0 subpixel True
    "gui/ctc.png"
    block:
        easeout 0.75 alpha 1.0 xoffset 0
        easein 0.75 alpha 0.5 xoffset -5
        repeat

## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## http://www.renpy.org/doc/html/screen_special.html#input

image input_caret:
    Solid("#DCC8A0")
    size (2,25) subpixel True
    block:
        linear 0.35 alpha 0
        linear 0.35 alpha 1
        repeat

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 30

            text prompt style "input_prompt"
            input id "input"


style input_prompt is default

style input_prompt:
    xmaximum gui.text_width
    xalign 0.5
    text_align gui.text_xalign

style input:
    caret "input_caret"
    xmaximum gui.text_width
    xalign 0.5
    text_align 0.5


## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## http://www.renpy.org/doc/html/screen_special.html#choice

transform fadein_text_choice(t=0.0):
    subpixel True
    alpha 0.0 yoffset -10
    time t
    ease_quad 0.5 alpha 1.0 yoffset 0
    subpixel False

screen choice(items):
    style_prefix "choice"

    vbox:
        for i, item in enumerate(items):
            textbutton _(item.caption) at fadein_text_choice((i + 1) * 0.5):
                action item.action

## When this is true, menu captions will be spoken by the narrator. When false,
## menu captions will be displayed as empty buttons.
define config.narrator_menu = True

style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 270
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")
    idle_background Frame('mod_assets/gui/choices/choice_idle_background.png', gui.choice_button_borders)
    hover_background Frame('mod_assets/gui/choices/choice_hover_background.png', gui.choice_button_borders)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")
    outlines []


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

screen quick_menu():

    # Ensure this appears on top of other screens.
    zorder 100

    if quick_menu:
        style_prefix "quick"

        # Add an in-game quick menu.
        hbox:
            xalign 0.5
            yalign 0.99

            #textbutton _("Back") action Rollback()
            textbutton _("History") action ShowMenu('history')
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Save") action ShowMenu('save')
            textbutton _("Load") action ShowMenu('load')
            textbutton _("Main Menu") action MainMenu()
            #textbutton _("Q.Save") action QuickSave()
            #textbutton _("Q.Load") action QuickLoad()
            textbutton _("Settings") action ShowMenu('preferences')


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
#init python:
#    config.overlay_screens.append("quick_menu")

default quick_menu = True

#style quick_button is default
#style quick_button_text is button_text

style quick_hbox:
    xalign 0.5
    yalign 0.99
    spacing 25

style quick_button:
    properties gui.button_properties("quick_button")
    activate_sound gui.activate_sound

style quick_button_text:
    properties gui.button_text_properties("quick_button")
    xalign 0.5 yalign 0.5
    outlines []


################################################################################
# Main and Game Menu Screens
################################################################################

## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## http://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu_team():
    style_prefix "main_menu_team"

    frame:
        label _("{cube}  Made by Team Icebreaker")

style main_menu_team_frame is empty
style main_menu_team_label is empty
style main_menu_team_label_text is empty

style main_menu_team_frame:
    xalign 0.01 yalign 0.99
    padding (20, 15)
    background RoundedFrame("#fff").add_radius(0.25)

style main_menu_team_label_text:
    font gui.default_font
    hinting "default"
    size 18
    color "#000"

screen main_menu():

    # This ensures that any other menu screen is replaced.
    tag menu

    style_prefix "main_menu"

    ## The use statement includes another screen inside this one. The actual
    ## contents of the main menu are in the navigation screen.
    use navigation
    use main_menu_team

    key "K_ESCAPE" action Quit(confirm=False)


style main_menu_frame is empty
style main_menu_vbox is vbox

## About screen ################################################################
##
## This screen gives credit and copyright information about the game and Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():
    tag menu
    ## This use statement includes the game_menu screen inside this one. The
    ## vbox child is then included inside the viewport inside the game_menu
    ## screen.
    use game_menu(_("About")):
        vbox:
            spacing 10
            text "[config.name!t] is fan made mod of Doki Doki Literature Club, which is meant to be played after finishing the original game."
            text "Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"

## This is redefined in options.rpy to add text to the about screen.
define gui.about = ""


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size

################################################################################
## Additional screens
################################################################################

## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## http://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Displays dialogue in either a vpgrid or the vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Displays the menu, if given. The menu may be displayed incorrectly if
        ## config.narrator_menu is set to True, as it is above.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## This controls the maximum number of NVL-mode entries that can be displayed at
## once.
define config.nvl_list_length = 6

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    text_align gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    text_align gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    text_align gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.button_text_properties("nvl_button")

