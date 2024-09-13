varying highp vec2 coord;
uniform sampler2D sdf;

void main(void) {
    highp float distance = texture2D(sdf, coord).a;
    highp float color = (1. - distance / .07) * 2.0;
    gl_FragColor = vec4(color, color, color, 1);
    if (distance > .08) discard;
}
