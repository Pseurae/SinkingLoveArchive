## Config Options (options.rpy)
## ----------------------------
## Configuration variables and other fixed options. Mostly a Copy-Paste from Weiss' Mod Template.
## (https://github.com/GanstaKingofSA/DDLCModTemplate2.0)

# This is where you will name your mod!
# Change "DDLC Mod Template 2.0" to your mod name (e.g. "Yuri")
define config.name = "Doki Doki Sinking Love"

# This controls whether you want your mod name to show in the main menu.
# If your mod name is big, it is suggested to turn this off
define gui.show_name = False

# This is where you will input the version of your mod.
# If you have multiple versions of your mod, this will be pretty useful to change.
# If you are starting out, set this to "1.0"
define config.version = ""

# This adds information about your mod in the About section.
# DDLC does not have a about section so you can leave this blank.
define gui.about = _("")

# This is the name of your build that the Ren'Py SDK will read.
# The build name is ASCII only so no numbers, spaces, or semicolons.
# Example: Doki Doki Yuri Time to DokiDokiYuriTime
define build.name = "DokiDokiSinkingLove"

# This configures whether your mod has sound effects (e.g. slap sound effects) or not.
# It is best to leave this set to True default.
define config.has_sound = True

# This configures whether your mod has music (e.g. Your Reality) or not.
# It is best to leave this set to True default.
define config.has_music = True

# This configures whether your mod has voices!
# If your using voice actors in your mod, set this to True, else leave it at False.
define config.has_voice = False

# This configures what song/music will play when you launch your mod.
# audio.t1 is the Doki Doki Literature Club Main Menu Music.
# If you want to change this, change the "t1" to the song you want.
define config.main_menu_music = audio.t1

# These two settings control the transition effects of DDLC on the game menu.
# Dissolve(.2) sets the transition effect you see.
# config.enter_transition controls the effect seen when entering the game menu.
# config.exit_transition controls the effect when returning to the game.
define config.enter_transition = Dissolve(.2)
define config.exit_transition = Dissolve(.2)
define config.intra_transition = Dissolve(.2)

define config.enter_yesno_transition = Dissolve(.2)
define config.exit_yesno_transition = Dissolve(.2)

# This controls the transition effect of DDLC when loading a saved game.
# By default, this is set to None and you can customize what transition you want to show.
# If you are unsure about this setting, leave it as is.
define config.after_load_transition = None

# This controls the transition effect of DDLC when your mod has ended.
# Dissolve(.2) sets the transition effect you see.
define config.end_game_transition = Dissolve(.5)

# This controls the textbox that the characters use to speak.
# "auto" sets the textbox to hide during scenes and show when a character speaks
# "show" sets the textbox to show at all times
# "hide" only shows dialogue when a character speaks.
define config.window = "auto"

# This controls the transition effects of the textbox.
# Dissolve(.2) sets the transition effect you see.
# config.window_show_transition controls the effect when the textbox is shown.
# config.window_hide_transition controls the effect when the textbox is hidden.
define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)

# This sets the text speed of your mod.
# By default this is set to 50. 
# Increasing this number will speed up text while decreasing the number slows down text speed.
# 0 is instant text display.
default preferences.text_cps = 50

# This controls the auto-forward speed
# 15 is DDLC's default speed.
# You can change it from 0-30
default preferences.afm_time = 15

# This controls the audio level of your mod.
# Increasing this will make the music louder while decreasing will make it quieter.
# SFX controls the sound effects volume.
default preferences.music_volume = 0.75
default preferences.sfx_volume = 0.75

# This controls the save directory of your mod.
# Change "DDLCModTemplate2" to your mod's name
# Windows Directory for Saves: %AppData%/RenPy/
# macOS Directory for Saves: $HOME/Library/RenPy/ (Un-hide the Library Folder)
# Linux Directory for Saves $HOME/.renpy/
define config.save_directory = "DDSL"

# This controls the window logo of your mod.
# By default this defaults to the DDLC Icon PNG.
define config.window_icon = "mod_assets/gui/logo.png"

# This controls whether your mod allows skipping dialogue.
define config.allow_skipping = True

# This controls whether your mod saves automatically.
define config.has_autosave = False

# This controls whether you mod saves when quitting the game.
define config.autosave_on_quit = False

# This controls the number of slots auto-saving can use
define config.autosave_slots = 0

# This controls the layers of screens, images, and more. 
# Best not to leave this alone.
define config.layers = [ 'master', 'transient', 'screens', 'overlay', 'front' ]

# Stuff to leave alone also.
define config.image_cache_size = 64
define config.predict_statements = 50
define config.rollback_enabled = config.developer
define config.menu_clear_layers = [ "front" ]
define config.gl_test_image = "black"

init python:
    if len(renpy.loadsave.location.locations) > 1:
        del renpy.loadsave.location.locations[1]

    renpy.game.preferences.pad_enabled = False

    def replace_text(s):
        s = s.replace('--', u'\u2014') 
        s = s.replace(' - ', u'\u2014') 
        return s

    config.replace_text = replace_text

    def game_menu_check():
        if quick_menu: renpy.call_in_new_context('_game_menu')

    config.game_menu_action = game_menu_check
