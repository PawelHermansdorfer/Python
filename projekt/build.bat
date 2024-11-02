@echo off

clang -Os -fno-builtin -Wall -Wextra -Wswitch-enum --target=wasm32 --no-standard-libraries -Wl,--export=init -Wl,--export=render -Wl,--export=update -Wl,--export=keydown -Wl,--export=mouse_pressed -Wl,--no-entry -Wl,--allow-undefined  -o main.wasm main.c
