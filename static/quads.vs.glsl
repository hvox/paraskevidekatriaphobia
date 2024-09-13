attribute vec2 vertex_position;
attribute vec2 uv;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform vec3 pivot;
uniform vec2 ratio;

varying vec2 coord;

void main(void) {
    coord = uv / vec2(1, 64);
    vec4 ws_pivot = projection * view * model * vec4(pivot, 1);
    ws_pivot /= ws_pivot.w;
     gl_Position = ws_pivot + vec4(vertex_position / ratio / vec2(30, 15), 0, 0);
	gl_Position.z = -.99;
}
