// Water Fragment Shader
#version 330
in vec2 fragmentTexCoord;
uniform sampler2D imageTexture;
uniform sampler1D colorTexture;
uniform vec2 player_pos;
uniform vec2 scroll;
uniform vec2 resolution;
uniform vec2 t;
uniform float time;
out vec4 color;
vec4 Warm_color(vec4 p) {
    p.r = p.r * 1.3;
    p.g = p.g * 0.95;
    p.b = p.b * 1.02;
    return vec4(p.r, p.g, p.b, 1.0);
}
vec4 Cold_color(vec4 p) {
    p.r = p.r * 0.9;
    p.g = p.g * 0.9;
    p.b = p.b * 1.4;
    return vec4(p.r, p.g, p.b, 1.0);
}
vec4 Green_color(vec4 p) {
    p.r = p.r * 0.9;
    p.g = p.g * 1.3;
    p.b = p.b * 0.9;
    return vec4(p.r, p.g, p.b, 1.0);
}
vec4 Grey_color(vec4 p) {
    float greykey;
    greykey = (p.r + p.g + p.b) / 3.0;
    return vec4(greykey, greykey, greykey, 1.0);
}

vec2 SineWave(vec2 p){
	float x = sin(25.0 * p.y + 30.0 * p.x + 6.28 *t.x)*0.01;
	float y = sin(25.0 * p.y + 30.0 * p.x + 6.28 *t.y)*0.01;
	return vec2(p.x + x,p.y + y);
}
vec4 fog_effect(vec4 p){
	vec2 uv = (gl_FragCoord.xy - 0.5*resolution.xy)/resolution.y;
	vec3 col = vec3(p.r,p.g,p.b);
	col += 0.2 * length(uv);
	p = vec4(col,1.0);
	return p;
}

void main() {
    // Get the original color from the texture
    vec4 originalColor = texture(imageTexture, fragmentTexCoord);

    //originalColor.b += 0.1 * sin(fragmentTexCoord.x * 10.0 + fragmentTexCoord.y * 10.0);

    //originalColor = fog_effect(originalColor);   
    //originalColor = Grey_color(originalColor);
    originalColor = Warm_color(originalColor);
    originalColor = Cold_color(originalColor);
    originalColor = Green_color(originalColor);



    // Assign the modified color to the output
    color = originalColor;

}
