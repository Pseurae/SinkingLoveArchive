init python:
    renpy.register_shader("sl.rounded_corners", variables="""
        uniform float u_radius;
        uniform sampler2D tex0;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        uniform vec2 res0;
    """, vertex_200="""
        v_tex_coord = a_tex_coord;
    """, fragment_200="""
        #define RC_CENTER res0.xy / 2.0

        // https://www.iquilezles.org/www/articles/distfunctions/distfunctions.htm
        #define ROUNDED_RECT(p, b, r) (length(max(abs(p) - b + r, 0.0)) - r)

        float crop = ROUNDED_RECT((v_tex_coord.xy * res0) - RC_CENTER, RC_CENTER, u_radius);
        gl_FragColor = mix(texture2D(tex0, v_tex_coord), vec4(0.0), smoothstep(-1.0, 1.0, crop));
    """)