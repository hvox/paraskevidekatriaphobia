attribute vec3 vertex_position;
attribute vec3 vertex_normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform vec3 color;

varying vec3 pos;
varying vec3 normal;

vec4 qtransform(vec4 q, vec4 v) {
    return vec4(v.xyz + 2.0 * cross(cross(v.xyz, q.xyz) + q.w * v.xyz, q.xyz), 1.0);
}

void main(void) {
    pos = (model * vec4(vertex_position, 1)).xyz;
    gl_Position = projection * view * vec4(pos, 1);
    normal = normalize(model * vec4(vertex_normal, 0)).xyz;
}
