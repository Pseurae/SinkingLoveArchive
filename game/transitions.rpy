
# Controls the default dissolve speed
define dissolve = Dissolve(0.25)

# Special dissolves for CGs and Scenes
define dissolve_cg = Dissolve(0.75)
define dissolve_scene = Dissolve(1.0)

# Dissolves the whole scene
define dissolve_scene_full = MultipleTransition([
    False, Dissolve(1.0),
    Solid("#000"), Pause(1.0),
    Solid("#000"), Dissolve(1.0),
    True])


# Dissolves out from black for start of a new scene
define dissolve_scene_half = MultipleTransition([
    Solid("#000"), Pause(1.0),
    Solid("#000"), Dissolve(1.0),
    True])

# Fade out to black
define close_eyes = MultipleTransition([
    False, Dissolve(0.5),
    Solid("#000"), Pause(0.25),
    True])

# Fade out from black
define open_eyes = MultipleTransition([
    False, Dissolve(0.5),
    True])

# Sudden Darkness
define trueblack = MultipleTransition([
    Solid("#000"), Pause(0.25),
    Solid("#000")
    ])

# Controls `wipeleft`'s wipe
define wipeleft = ImageDissolve("images/menu/wipeleft.png", 0.5, ramplen=64)
define wiperight = ImageDissolve(im.Flip("images/menu/wipeleft.png", horizontal=True, vertical=True), 0.5, ramplen=64)

# Wipes to black and then to a new scene
define wipeleft_scene = MultipleTransition([
    False, ImageDissolve("images/menu/wipeleft.png", 0.5, ramplen=64),
    Solid("#000"), Pause(0.25),
    Solid("#000"), ImageDissolve("images/menu/wipeleft.png", 0.5, ramplen=64),
    True])

define tpause = Pause(0.25)