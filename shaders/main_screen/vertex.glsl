#version 330 core
layout (location = 0) in vec3 vertexPos;
layout (location = 1) in vec2 vertexTexCoord;
uniform vec2 player_loc;
uniform vec2 scroll_loc;
out vec2 fragmentTexCoord;

void main() {
	gl_Position = vec4(vertexPos.x,vertexPos.y,vertexPos.z, 1.0);
	fragmentTexCoord = vertexTexCoord;
}

