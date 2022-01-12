init python:
    LINEAR_FRAC = """
float lg_currentAngle = u_angle;

vec4 lg_startColor = vec4(u_gradient_0);
vec4 lg_endColor = vec4(u_gradient_1);

vec2 lg_uv = v_tex_coord.xy;

vec2 lg_origin = vec2(0.5, 0.5);
lg_uv -= lg_origin;

float lg_angle = radians(90.0) - radians(lg_currentAngle) + atan(lg_uv.y, lg_uv.x);

float lg_len = length(lg_uv);
lg_uv = vec2(cos(lg_angle) * lg_len, sin(lg_angle) * lg_len) + lg_origin;
    
gl_FragColor = mix(lg_startColor, lg_endColor, smoothstep(0.0, 1.0, lg_uv.x));
"""

    renpy.register_shader("sl.linear_gradient", variables="""
        uniform vec4 u_gradient_0;
        uniform vec4 u_gradient_1;
        uniform float u_angle;

        uniform sampler2D tex0;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        uniform vec2 res0;
    """, vertex_200="""
        v_tex_coord = a_tex_coord;
    """, fragment_200=LINEAR_FRAC)