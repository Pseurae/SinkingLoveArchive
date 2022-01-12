## Splash (splash.rpy)
## -------------------
## Contains resources for the splashscreen and other special labels (`before_main_menu` and `quit`).

init python:
    splash_message_default = "This game is an unofficial fan game, unaffiliated with Team Salvato."

image splash_warning = ParameterizedText(style="splash_text", xalign=0.5, yalign=0.5)

# Main Menu Images
image menu_logo:
    "mod_assets/gui/logo.png"
    size (384, 384)
    subpixel True
    xcenter 1140
    ycenter 180
    zoom 0.60
    menu_logo_move

image menu_bg:
    topleft
    "gui/menu_bg.png"
    menu_bg_move

# 720 + 700
image menu_clouds:
    xalign 0.5
    ysize 720 + 900

image sky_gradient:
    LinearGradient("#5ADEFF", "#87CEEB")
    ysize 720 + 700

image main_menu_bg_clouds:
    contains:
        "sky_gradient"

    contains:
        yoffset 700
        contains:
            "mod_assets/gui/menu_art.png"

    menu_bg_movetoplace

transform menu_bg_movetoplace:
    subpixel True
    topleft
    parallel:
        ypos 0
        time 0.65
        ease_cubic 2.5 ypos -700

image main_menu_nav_frame:
    "mod_assets/gui/overlay/main_menu.png"
    zoom 0.5
    xalign 1.0

image main_menu_nav:
    size (1280, 720)

    contains:
        "main_menu_nav_frame"
    contains:
        'menu_logo'

transform menu_logo_move:
    subpixel True
    yoffset -300
    easein_bounce 1.5 yoffset 0

# Team Salvato Splash Screen

image intro:
    truecenter
    "white"
    0.5
    "bg/splash.png" with Dissolve(0.5, alpha=True)
    2.5
    "#2e2e2e" with Dissolve(0.5, alpha=True)
    0.5

# Special Mod Message Text

image warning:
    truecenter
    "white"
    "splash_warning" with Dissolve(0.5, alpha=True)
    2.5
    "#2e2e2e" with Dissolve(0.5, alpha=True)
    0.5

# Startup Disclaimer Images
image tos:
    contains:
        "sky_gradient"
        yoffset -700
    contains:
        "mod_assets/gui/tos.png"
        xalign 0.5 yalign 0.5

image canvas:
    "mod_assets/images/canvas.png"
    blend "multiply"

image teamlogo:
    contains:
        "#2e2e2e"

    contains:
        "mod_assets/gui/teamlogo.png"
        zoom 0.5 transform_anchor True
        xalign 0.5 yalign 0.5

# Startup Disclaimer
default persistent.first_run = False

label disclaimer:
    python hide:
        quick_menu = False

    scene white
    pause 0.5
    scene tos:
        matrixcolor SaturationMatrix(0.5)
    show canvas
    with Dissolve(1.0)
    pause 1.0

    "[config.name] is a Doki Doki Literature Club fan mod that is not affiliated in anyway with Team Salvato."
    "It is designed to be played only after the official game has been completed, and contains spoilers for the official game."
    "Game files for Doki Doki Literature Club are required to play this mod and can be downloaded for free {a=http://ddlc.moe}here{/a} or on Steam."

    menu:
        "By playing [config.name] you agree that you have completed Doki Doki Literature Club and accept any spoilers contained within."
        "I agree.":
            pass

    $ persistent.first_run = True
    show tos:
        matrixcolor IdentityMatrix()
    hide canvas
    with Dissolve(1.0)
    scene expression "#2e2e2e"
    with Dissolve(0.5)
    pause 1.0
    return

label splashscreen:
    python hide:
        missing_archives = { "fonts", "audio", "images" } - set(config.archives)
        print(missing_archives)

        if missing_archives:
            if sl_config.getboolean("STARTUP", "disable_explorer", fallback=False):
                formatted_missing_archives = ", ".join(map(lambda x: x + ".rpa", missing_archives))
                renpy.error("DDLC archive files not found in /game folder. Check your installation and try again.\nMissing archives are %s." % formatted_missing_archives)
            else:
                renpy.jump("choose_ddlc_zip")

    python hide:
        sl_framework.execute_pre_splash_callbacks()
        basedir = config.basedir.replace('\\', '/')

    # Startup Disclaimer
    if not persistent.first_run:
        call disclaimer from _call_disclaimer

    python hide:
        config.allow_skipping = False
        config.main_menu_music = audio.t1
        renpy.music.play(config.main_menu_music)

    show expression "#2e2e2e"
    show teamlogo
    with Dissolve(0.5, alpha=True)

    pause 2.5

    hide teamlogo with Dissolve(0.5, alpha=True)

    show splash_warning "[splash_message_default]" with Dissolve(0.5, alpha=True)

    pause 2.0

    hide splash_warning
    with Dissolve(0.5, alpha=True)

    $ config.allow_skipping = True
    return

# Warning Screen
label warningscreen:
    hide intro
    show warning
    pause 3.0

label before_main_menu:
    python hide:
        config.main_menu_music = audio.t1

    show expression gui.main_menu_background as main_menu_image onlayer master
    return

label quit:
    python hide:
        sl_framework.execute_quit_label_callbacks()

    return