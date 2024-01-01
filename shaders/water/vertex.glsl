#version 330 core
layout (location = 0) in vec3 vertexPos;
layout (location = 1) in vec2 vertexTexCoord;
out vec2 fragmentTexCoord;
//0.00134
void main() {
    gl_Position = vec4(vertexPos.x,vertexPos.y,vertexPos.z,1.0);
    fragmentTexCoord = vertexTexCoord;
}
