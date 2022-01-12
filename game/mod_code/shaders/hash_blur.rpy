init python:
    HASH_BLUR_FUNC = """ 
#define SPREAD 15.0
#define OFFSET 7.0

vec2 hash23(vec3 p3) {
    p3 = fract(p3 * vec3(443.897, 441.423, 437.195));
    p3 += dot(p3, p3.yzx + 19.19);
    return fract(vec2((p3.x + p3.y) * p3.z, (p3.x + p3.z) * p3.y)) * 2.0 - 1.0;
}

vec4 sample(sampler2D tex0, vec2 uv, float n, vec2 res0) {
    vec2 offset = hash23(vec3(uv, n / 2.0)) * (SPREAD + OFFSET * n);
    vec2 p0 = uv + offset / res0.xy;
    p0 = clamp(p0, vec2(0.01), vec2(0.99));

    return texture2D(tex0, p0);
}
"""

    renpy.register_shader("sl.hash_blur", variables="""
        uniform sampler2D tex0;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        uniform vec2 res0;
    """, vertex_200="""
        v_tex_coord = a_tex_coord;
    """, fragment_functions=HASH_BLUR_FUNC,
        fragment_200="""
        vec2 uv = v_tex_coord;
        #define STEPS 2

        gl_FragColor = vec4(0.0);
        for (int i=0; i < STEPS; i++) {
            gl_FragColor += sample(tex0, uv, float(i), res0);
        }
        gl_FragColor /= float(STEPS);
    """)