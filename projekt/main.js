'use strict';

let canvas = document.getElementById("canvas");
let ctx = canvas.getContext("2d");
let wasm = null;
let iota = 0;

function cstrlen(mem, ptr) {
    let len = 0;
    while (mem[ptr] != 0) {
        len++;
        ptr++;
    }
    return len;
}

function cstr_by_ptr(mem_buffer, ptr) {
    const mem = new Uint8Array(mem_buffer);
    const len = cstrlen(mem, ptr);
    const bytes = new Uint8Array(mem_buffer, ptr, len);
    return new TextDecoder().decode(bytes);
}

function color_hex(color) {
    const r = ((color>>(0*8))&0xFF).toString(16).padStart(2, '0');
    const g = ((color>>(1*8))&0xFF).toString(16).padStart(2, '0');
    const b = ((color>>(2*8))&0xFF).toString(16).padStart(2, '0');
    const a = ((color>>(3*8))&0xFF).toString(16).padStart(2, '0');
    return "#"+r+g+b+a;
}

function platform_fill_rect(x, y, w, h, color) {
    ctx.fillStyle = color_hex(color); 
    ctx.fillRect(x, y, w, h);
}

function platform_stroke_rect(x, y, w, h, color) {
    ctx.strokeStyle = color_hex(color); 
    ctx.strokeRect(x, y, w, h);
}

function platform_text_width(text_ptr, size) {
    const buffer = wasm.instance.exports.memory.buffer;
    const text = cstr_by_ptr(buffer, text_ptr);
    ctx.font = size+"px AnekLatin";
    return ctx.measureText(text).width;
}

function platform_fill_text(x, y, text_ptr, size, color) {
    const buffer = wasm.instance.exports.memory.buffer;
    const text = cstr_by_ptr(buffer, text_ptr);
    ctx.fillStyle = color_hex(color);
    ctx.font = size+"px AnekLatin";
    ctx.fillText(text, x, y);
}

function print(message_ptr) {
    const buffer = wasm.instance.exports.memory.buffer;
    const message = cstr_by_ptr(buffer, message_ptr);
    console.log(message);
}

let prev = null;
let touchStartX = null;
let touchStartY = null;
let touchEndX = null;
let touchEndY = null;
let touchStartTimestamp = null;
function loop(timestamp) {
    if (prev !== null) {
        wasm.instance.exports.update((timestamp - prev)*0.001);
        wasm.instance.exports.render();
    }
    prev = timestamp;
    window.requestAnimationFrame(loop);
}

WebAssembly.instantiateStreaming(fetch('main.wasm'), {
    env: {
        platform_fill_rect,
        platform_stroke_rect,
        platform_fill_text,
        print,
        platform_text_width,
    }
}).then((w) => {
    wasm = w;

    wasm.instance.exports.init(canvas.width, canvas.height);

    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;

    document.addEventListener('keydown', (e) => {
        wasm.instance.exports.keydown(e.key.charCodeAt());
    });

    document.addEventListener('click', (e) => {
        let x = event.clientX;
        let y = event.clientY;
        wasm.instance.exports.mouse_pressed(x, y);
    });


    const buffer = wasm.instance.exports.memory.buffer;
    window.requestAnimationFrame(loop);
});
