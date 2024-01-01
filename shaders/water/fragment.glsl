
in vec2 fragmentTexCoord;
uniform sampler2D imageTexture;
uniform float tx;
uniform float ty;
out vec4 color;

vec2 SineWave(vec2 p){
	float x = sin(25.0 * p.y + 30.0 * p.x + 6.28 *tx)*0.01;
	float y = sin(25.0 * p.y + 30.0 * p.x + 6.28 *ty)*0.01;
	return vec2(p.x + x,p.y + y);
}

void main(){
	color = texture(imageTexture,SineWave(fragmentTexCoord));
}