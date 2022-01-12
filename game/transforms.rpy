## Transforms (transform.rpy)
## --------------------------
## ATL used for positioning and special effects.

init python in transform_positions:
    from math import floor, ceil
    from renpy.config import screen_width
    from store import (
        tcommon,
        tinstant,
        focus,
        sink,
        hop,
        sink,
        dip,
        panic,
        leftin,
        rightin
    )

    # a(n) = a(0) + (n - 1)d
    def calculate_position(n, i, margin=80):
        assert n >= i
        assert i > 0

        if n == 1:
            return int(screen_width / 2)

        mult = ceil(n * 1.5)
        dist = (screen_width - margin) / mult

        first = floor(dist)
        last = floor(screen_width - dist)

        common_difference = (last - first) / (n - 1)

        return int(floor(first + (i - 1) * common_difference))

    def calculate_positions(n, margin=80):
        for i in range(n):
            for j in range(i):
                yield calculate_position(i + 1, j + 1, margin)

    base_transform_map = {
        "t": tcommon,
        "i": tinstant,
        "f": focus,
        "s": sink,
        "h": hop,
        "d": dip,
        "p": panic,
        "l": leftin,
        "r": rightin
    }

    def iterate_transform_info(transform):
        def iterate_matrix(n):
            for i in range(n):
                for j in range(i + 1):
                    yield (i + 1), (j + 1)

        for prefix, base_transform in base_transform_map.items():
            for num, i in iterate_matrix(4):
                yield "%s%s%s" % (prefix, num, i), calculate_position(num, i), base_transform

        del iterate_matrix

    for name, xpos, base_transform in iterate_transform_info(base_transform_map):
        setattr(
            renpy.store,
            name,
            base_transform(xpos)
        )

init offset = -1

# Base for other transforms (not used in the game)
transform tcommon(x=640, z=0.80):
    yanchor 1.0 subpixel True

    on show:
        ypos 1.03
        zoom z*0.95 alpha 0.00
        xcenter x yoffset -20
        easein .25 yoffset 0 zoom z*1.00 alpha 1.00

    on replace:
        alpha 1.00
        parallel:
            easein .25 xcenter x zoom z*1.00
        parallel:
            easein .15 yoffset 0 ypos 1.03

transform tinstant(x=640, z=0.80):
    xcenter x yoffset 0 zoom z*1.00 alpha 1.00 yanchor 1.0 ypos 1.03

# This pulls out the character that is talking and makes them bigger
transform focus(x=640, z=0.80):
    yanchor 1.0 ypos 1.03 subpixel True

    on show:
        zoom z*0.95 alpha 0.00
        xcenter x yoffset -20
        easein .25 yoffset 0 zoom z*1.05 alpha 1.00
        yanchor 1.0 ypos 1.03

    on replace:
        alpha 1.00
        parallel:
            easein .25 xcenter x zoom z*1.05
        parallel:
            easein .15 yoffset 0

# This causes the character to sink down
transform sink(x=640, z=0.80):
    xcenter x yoffset 0 yanchor 1.0 ypos 1.03 zoom z*1.00 alpha 1.00 subpixel True
    easein .5 ypos 1.06

# This makes the character jump
transform hop(x=640, z=0.80):
    xcenter x yoffset 0 yanchor 1.0 ypos 1.03 zoom z*1.00 alpha 1.00 subpixel True
    easein .1 yoffset -20
    easeout .1 yoffset 0

# Like hop but for a character that is focused
transform hopfocus(x=640, z=0.80):
    xcenter x yoffset 0 yanchor 1.0 ypos 1.03 zoom z*1.05 alpha 1.00 subpixel True
    easein .1 yoffset -21
    easeout .1 yoffset 0

# This causes the character to dip down for a second and come back up
transform dip(x=640, z=0.80):
    xcenter x yoffset 0 yanchor 1.0 ypos 1.03 zoom z*1.00 alpha 1.00 subpixel True
    easein .25 yoffset 25
    easeout .25 yoffset 0

# This causes the character to wobble from side to side and up and down
transform panic(x=640, z=0.80):
    xcenter x yoffset 0 yanchor 1.0 ypos 1.03 zoom z*1.00 alpha 1.00 subpixel True
    parallel:
        ease 1.2 yoffset 25
        ease 1.2 yoffset 0
        repeat
    parallel:
        easein .3 xoffset 20
        ease .6 xoffset -20
        easeout .3 xoffset 0
        repeat

# This causes the character to fly in
transform leftin(x=640, z=0.80):
    xcenter -300 yoffset 0 yanchor 1.0 ypos 1.03 zoom z*1.00 alpha 1.00 subpixel True
    easein .25 xcenter x

transform rightin(x=640, z=0.80):
    xcenter 2000 yoffset 0 yanchor 1.0 ypos 1.03 zoom z*1.00 alpha 1.00 subpixel True
    easein .25 xcenter x

# This hides the character
transform thide(z=0.80):
    subpixel True
    transform_anchor True
    on hide:
        easein .25 zoom z*0.95 alpha 0.00 yoffset -20

transform lhide(t=0.25):
    subpixel True
    on hide:
        easeout t xcenter -300

transform rhide(t=0.25):
    subpixel True
    on hide:
        easeout t xcenter 2000

# When MC opens his eyes to Sayori's face
transform face(z=0.80, y=500):
    subpixel True
    xcenter 640
    yanchor 1.0 ypos 1.03
    yoffset y
    zoom z*2.00

# Fade for a new CG
transform cgfade():
    on show:
        alpha 0.0
        linear 0.5 alpha 1.0
    on hide:
        alpha 1.0
        linear 0.5 alpha 0.0

# A little wiggle for Natsuki in the closet
transform n_cg2_wiggle():
    subpixel True
    xoffset 0
    easein 0.15 xoffset 20
    easeout 0.15 xoffset 0
    easein 0.15 xoffset -15
    easeout 0.15 xoffset 0
    easein 0.15 xoffset 10
    easeout 0.15 xoffset 0
    easein 0.15 xoffset -5
    ease 0.15 xoffset 0

transform n_cg2_wiggle_loop():
    n_cg2_wiggle
    1.0
    repeat

# Zoom after falling where MC sees Natsuki's face
transform n_cg2_zoom:
    subpixel True
    truecenter
    xoffset 0
    easeout 0.20 zoom 2.5 xoffset 200

# White noises and effects
image noise:
    truecenter
    "images/bg/noise1.jpg"
    pause 0.1
    "images/bg/noise2.jpg"
    pause 0.1
    "images/bg/noise3.jpg"
    pause 0.1
    "images/bg/noise4.jpg"
    pause 0.1
    xzoom -1
    "images/bg/noise1.jpg"
    pause 0.1
    "images/bg/noise2.jpg"
    pause 0.1
    "images/bg/noise3.jpg"
    pause 0.1
    "images/bg/noise4.jpg"
    pause 0.1
    yzoom -1
    "images/bg/noise1.jpg"
    pause 0.1
    "images/bg/noise2.jpg"
    pause 0.1
    "images/bg/noise3.jpg"
    pause 0.1
    "images/bg/noise4.jpg"
    pause 0.1
    xzoom 1
    "images/bg/noise1.jpg"
    pause 0.1
    "images/bg/noise2.jpg"
    pause 0.1
    "images/bg/noise3.jpg"
    pause 0.1
    "images/bg/noise4.jpg"
    pause 0.1
    yzoom 1
    repeat

# Makes a noise overlay transparent
transform noise_alpha:
    alpha 0.25

# Have the noise fade in to 40%
transform noisefade(t=0):
    alpha 0.0
    t
    linear 5.0 alpha 0.40

# Vignette around the edge of the screen
image vignette:
    truecenter
    "images/bg/vignette.png"

# Have the vignette fade in
transform vignettefade(t=0):
    alpha 0.0
    t
    linear 25.0 alpha 1.00

# A random flicker in and out of Vignette
transform vignetteflicker(t=0):
    alpha 0.0
    t + 2.030
    parallel:
        alpha 1.00
        linear 0.2 alpha 0.8
        0.1
        alpha 0.7
        linear 0.1 alpha 1.00
        alpha 0.0
        1.19
        repeat
    parallel:
        easeout 20 zoom 3.0

transform layerflicker(t=0):
    truecenter
    t + 2.030
    parallel:
        zoom 1.05
        linear 0.2 zoom 1.04
        0.1
        zoom 1.035
        linear 0.1 zoom 1.05
        zoom 1.0
        1.19
        repeat
    parallel:
        easeout_bounce 0.3 xalign 0.6
        easeout_bounce 0.3 xalign 0.4
        repeat

# Rewind Effect used in Act 2
transform rewind:
    truecenter
    zoom 1.20
    parallel:
        easeout_bounce 0.2 xalign 0.55
        easeout_bounce 0.2 xalign 0.45
        repeat
    parallel:
        easeout_bounce 0.33 yalign 0.55
        easeout_bounce 0.33 yalign 0.45
        repeat

# Heartbeat effect used with Yandere Yuri and the Final Act
transform heartbeat:
    heartbeat2(1)

transform heartbeat2(m):
    truecenter
    parallel:
        0.144
        zoom 1.00 + 0.07 * m
        easein 0.250 zoom 1.00 + 0.04 * m
        easeout 0.269 zoom 1.00 + 0.07 * m
        zoom 1.00
        1.479
        repeat
    parallel:
        easeout_bounce 0.3 xalign 0.5 + 0.02 * m
        easeout_bounce 0.3 xalign 0.5 - 0.02 * m
        repeat

# Motion for Yuri's Eyes
transform yuripupils_move:
    function yuripupils_function

init python:
    def yuripupils_function(trans, st, at):
        trans.xoffset = -1 + random.random() * 9 - 4
        trans.yoffset = 3 + random.random() * 6 - 3
        return random.random() * 1.2 + 0.3

# Have a character pop in instantly with a given transparency
transform malpha(a=1.00):
    i11
    alpha a

transform ship_rock_loop:
    subpixel True
    xoffset 0 yoffset 0
    parallel:
        easein renpy.random.uniform(2.0, 3.0) xoffset renpy.random.uniform(10.0, 15.0)
        easeout renpy.random.uniform(2.0, 3.0) xoffset 0
        easein renpy.random.uniform(2.0, 3.0) xoffset renpy.random.uniform(-15.0, -10.0)
        easeout renpy.random.uniform(2.0, 3.0) xoffset 0
    parallel:
        easein renpy.random.uniform(2.0, 2.5) yoffset renpy.random.uniform(6.0, 10.0)
        easeout renpy.random.uniform(2.0, 3.0) yoffset 0
        easein renpy.random.uniform(2.0, 3.0) yoffset renpy.random.uniform(-10.0, -6.0)
        easeout renpy.random.uniform(2.0, 3.0) yoffset 0
    repeat

transform notify_appear_up_to_down():
    xalign 1.0 ypos 30
    on show:
        yoffset -15.0 alpha 0.0
        easein 0.5 yoffset 0.0 alpha 1.0

    on hide:
        easeout 0.5 yoffset 15.0 alpha 0.0

transform notify_appear_left_to_right():
    ypos 30
    on show:
        xpos 1.0 xanchor 0.0 alpha 0.0
        easein 0.5 xalign 1.0 alpha 1.0

    on hide:
        easeout 0.5 xpos 1.0 xanchor 0.0 alpha 0.0