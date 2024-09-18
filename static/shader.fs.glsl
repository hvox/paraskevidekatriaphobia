uniform highp vec3 color;
uniform highp vec2 shadowmap_position;
uniform sampler2D shadowmap;

varying highp vec3 pos;
varying highp vec3 normal;

void main(void) {
    highp vec3 normal = normalize(normal);
    highp vec3 sun = vec3(.5, .5, .6);
    highp float brightness = max(.2, 1.3 * dot(sun, normal));
    highp float shadow = 20.0 * (0.5 - texture2D(shadowmap, (pos.xy - pos.z / 2.0 - shadowmap_position) / 60.0 + 0.5).r);
    highp float culling = dot(normal, normalize(vec3(-.5, -.5, -1)));
    if (shadow > pos.z - 0.03 && culling < 0.0) brightness = max(.2, .75 * brightness);
    gl_FragColor = vec4(color.rgb * brightness, 1);
    // gl_FragColor = vec4( 100.0*(shadow - pos.z), 0, 100.0*(pos.z - shadow), 5) / 5.0;
}
