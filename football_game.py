import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Head Soccer Fix", layout="centered")
st.title("⚽️ Head Soccer: Almaty Cup")

# Чистый HTML5 Canvas без внешних библиотек
game_html = """
<div style="display: flex; flex-direction: column; align-items: center;">
    <canvas id="gameCanvas" width="700" height="400" style="border:2px solid #000; background: #87CEEB;"></canvas>
    <p>Управление: Месси (W,A,D) | Роналду (Стрелки)</p>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let p1 = { x: 50, y: 300, w: 50, h: 70, color: "red", vy: 0, score: 0 };
let p2 = { x: 600, y: 300, w: 50, h: 70, color: "blue", vy: 0, score: 0 };
let ball = { x: 350, y: 200, r: 15, vx: 2, vy: 2 };
let gravity = 0.6;
let keys = {};

window.addEventListener("keydown", e => keys[e.code] = true);
window.addEventListener("keyup", e => keys[e.code] = false);

function update() {
    // Движение P1 (W, A, D)
    if (keys["KeyA"] && p1.x > 0) p1.x -= 5;
    if (keys["KeyD"] && p1.x < 300) p1.x += 5;
    if (keys["KeyW"] && p1.y === 330) p1.vy = -12;

    // Движение P2 (Стрелки)
    if (keys["ArrowLeft"] && p2.x > 350) p2.x -= 5;
    if (keys["ArrowRight"] && p2.x < 650) p2.x += 5;
    if (keys["ArrowUp"] && p2.y === 330) p2.vy = -12;

    // Физика игроков
    p1.y += p1.vy; p1.vy += gravity;
    p2.y += p2.vy; p2.vy += gravity;
    if (p1.y > 330) { p1.y = 330; p1.vy = 0; }
    if (p2.y > 330) { p2.y = 330; p2.vy = 0; }

    // Физика мяча
    ball.x += ball.vx; ball.y += ball.vy; ball.vy += 0.3;
    if (ball.y > 385) { ball.y = 385; ball.vy *= -0.8; }
    if (ball.x < 0 || ball.x > 700) ball.vx *= -1;

    // Столкновения с игроками
    [p1, p2].forEach(p => {
        if (ball.x > p.x && ball.x < p.x + p.w && ball.y > p.y && ball.y < p.y + p.h) {
            ball.vy = -8;
            ball.vx = (ball.x - (p.x + p.w/2)) * 0.5;
        }
    });

    // Голы
    if (ball.x < 20 && ball.y > 250) { p2.score++; resetBall(); }
    if (ball.x > 680 && ball.y > 250) { p1.score++; resetBall(); }
}

function resetBall() {
    ball.x = 350; ball.y = 100; ball.vx = 2; ball.vy = 0;
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Трава и Ворота
    ctx.fillStyle = "green"; ctx.fillRect(0, 390, 700, 10);
    ctx.fillStyle = "white"; 
    ctx.fillRect(0, 250, 10, 150); // Левые
    ctx.fillRect(690, 250, 10, 150); // Правые

    // Игроки (вместо фото пока блоки)
    ctx.fillStyle = p1.color; ctx.fillRect(p1.x, p1.y, p1.w, p1.h);
    ctx.fillStyle = p2.color; ctx.fillRect(p2.x, p2.y, p2.w, p2.h);
    
    // Мяч
    ctx.fillStyle = "white"; ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.r, 0, Math.PI*2); ctx.fill();

    // Счет
    ctx.fillStyle = "black"; ctx.font = "30px Arial";
    ctx.fillText(p1.score + " : " + p2.score, 320, 50);

    update();
    requestAnimationFrame(draw);
}
draw();
</script>
"""

components.html(game_html, height=500)
