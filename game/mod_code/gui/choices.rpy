## Choices (choices.rpy)
## ---------------------
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## Contains:
## `girls_choice` screen - Special screen used for input between the girl names.

screen girls_choice(items):
    add "#0007" at fadein_vignette(1.0)

    frame at fadein_vignette(5.0):
        background None
        padding (50, 0)

        add "choice_outline":
            xalign 0.5 yalign 0.15

        add "choice_outline":
            xalign 0.5 yalign 1.0 - 0.15

    hbox spacing 20:
        xalign 0.5 yalign 0.5
        for i, item in enumerate(items):
            use single_choice(i, item)

transform fadein_vignette(t):
    alpha 0.0
    easein t alpha 1.0

transform fadein_choice(d):
    alpha 0.0 yoffset -300
    time d

    ease_quad 0.75 alpha 1.0 yoffset 0

    on idle:
        easein 0.25 yoffset 0

    on hover:
        easein 0.25 yoffset -20

##############################################################################################
#- Components --------------------------------------------------------------------------------
##############################################################################################

screen single_choice(i, item):
    button at fadein_choice(i * 0.5 + 0.2):
        style "single_choice_button"
        action item.action

        vbox xalign 0.5 yfill True:
            add item.kwargs.get("im", Null()) xalign 0.5
            null height 35

            vbox yalign 1.0:
                add "choice_divider_line"

                null height 25
                label _(item.caption) xalign 0.5 style "single_choice_label"
                null height 25

                add "choice_divider_line"

style single_choice_button:
    xsize 256 + 20 ysize 320 + 20
    background RoundedFrame(Solid("#2e2e2e")).add_radius(25.0)
    padding (25, 40)

style single_choice_label_text:
    size 16

##############################################################################################
#- Testing -----------------------------------------------------------------------------------
##############################################################################################

label process_girl_choice(menu_set):

    menu (screen="girls_choice"):
        # "Test"
        set menu_set

        "Talk to Sayori" (im="sayori_cookie"):
            return "sayori"

        "Talk to Natsuki" (im="natsuki_cupcake"):
            return "natsuki"

        "Talk to Yuri" (im="yuri_teacup"):
            return "yuri"

        "Talk to Monika" (im="monika_note"):
            return "monika"

    return "error"

##############################################################################################
#- Images ------------------------------------------------------------------------------------
##############################################################################################

image sayori_cookie:
    SameSizeImage("mod_assets/gui/choices/cookie.png")
    zoom 0.6

image natsuki_cupcake:
    SameSizeImage("mod_assets/gui/choices/cupcake.png")
    zoom 0.6

image monika_note:
    SameSizeImage("mod_assets/gui/choices/note.png")
    zoom 0.6

image yuri_teacup:
    SameSizeImage("mod_assets/gui/choices/cup.png")
    zoom 0.6
    xoffset 10

image choice_divider_line:
    "mod_assets/gui/choices/divider.png"
    zoom 0.5

define gui.choice_outline_border = Borders(30, 0, 30, 0)

image choice_outline_image:
    "mod_assets/gui/choices/line.png"
    zoom 0.5

image choice_outline:
    Frame("choice_outline_image", gui.choice_outline_border)
    ysize 12

##############################################################################################
#- Misc --------------------------------------------------------------------------------------
##############################################################################################

init python:
    class SameSizeImage(renpy.display.im.Image):
        max_width = 0
        max_height = 0

        def __init__(self, filename, **properties):
            super(SameSizeImage, self).__init__(filename, **properties)
            renpy.display.im.cache.preload_image(self)

        @classmethod
        def update_max_vals(cls, width, height):
            cls.max_width = max(cls.max_width, width)
            cls.max_height = max(cls.max_height, height)

        def load(self, unscaled=False):
            rv = super(SameSizeImage, self).load(unscaled)

            self.update_max_vals(*rv.get_size())

            return rv

        def render(self, width, height, st, at):
            self.load()
            rv = renpy.Render(self.max_width, self.max_height)

            image_render = super(SameSizeImage, self).render(width, height, st, at)
            image_width, image_height = image_render.get_size()

            rv.blit(image_render, ((self.max_width - image_width) / 2, (self.max_height - image_height) / 2))
            return rv
