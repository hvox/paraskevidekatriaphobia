uniform highp vec3 color;

varying highp vec3 pos;
varying highp vec3 normal;

void main(void) {
    highp vec3 normal = normalize(normal);
    highp vec3 sun = vec3(.5, .5, .6);
    highp float brightness = max(.3, 1.3 * dot(sun, normal));
    gl_FragColor = vec4(color.rgb * brightness, 1);
}
