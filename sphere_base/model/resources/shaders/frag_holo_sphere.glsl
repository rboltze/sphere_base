#version 330 core

in vec2 TexCoord;
in vec4 v_color;

out vec4 color;
out vec4 FragColor;

uniform sampler2D texture1;
uniform int switcher;

void main()
{
    vec4 texColor = texture(texture1, TexCoord);
    if(texColor.a < 0.1)
        discard;
    FragColor = texColor;

        if (switcher == 0) {
            color = FragColor * v_color;
        }
        else if (switcher == 1){
            color = FragColor;
        }
        else if (switcher == 2){
            color = v_color;
        }

}