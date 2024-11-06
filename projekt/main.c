#include <stddef.h>

typedef unsigned char u8;
typedef unsigned int u32;
typedef unsigned long long u64;
typedef int i32;
typedef int b32;
typedef float f32;

void platform_fill_rect(i32 x, i32 y, i32 w, i32 h, u32 color);
void platform_stroke_rect(i32 x, i32 y, i32 w, i32 h, u32 color);
void platform_fill_text(i32 x, i32 y, const char *text, u32 size, u32 color);
u32 platform_text_width(char *text, u32 size);
void print(char *message);

void init(u32 width, u32 height);
void resize(u32 width, u32 height);
void render(void);
void update(f32 dt);
void keydown(int key);
void mouse_down(int x, int y);


////////////////////////////////////////
int rect_x = 0;
int rect_y = 0;

void
init(u32 width, u32 height)
{
}

void
resize(u32 width, u32 height)
{
}

void
render(void)
{
}

void
update(f32 dt)
{
    platform_fill_rect(rect_x, rect_y, 50, 50, 0xFFFF00FF);
}

void
keydown(int key)
{
    // char str[2] = {(char)key, 0};
    // print(str);
}

void
mouse_pressed(int x, int y)
{
    // print("Pressed!!!");
    rect_x = x;
    rect_y = y;
}
