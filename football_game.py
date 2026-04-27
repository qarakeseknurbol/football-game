import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Messi vs Ronaldo: Head Soccer", layout="centered")
st.title("⚽️ Head Soccer: Almaty Cup")

# Ссылка на твой репозиторий для картинок
# ВАЖНО: убедись, что твое имя пользователя в ссылке ниже правильное
github_url = "https://raw.githubusercontent.com/qarakaseknurbol/marketing/main/"

game_html = f"""
<div style="display: flex; flex-direction: column; align-items: center; font-family: 'Arial Black', sans-serif;">
    <div id="ui" style="display: flex; justify-content: space-between; width: 700px; background: rgba(0,0,0,0.7); color: white; padding: 10px; border-radius: 10px 10px 0 0;">
        <div id="timer">Time: 90s</div>
        <div id="score" style="font-size: 24px;">Messi 0 : 0 Ronaldo</div>
        <div id="round">Round: 1</div>
    </div>
    <canvas id="gameCanvas" width="700" height="400" style="border:3px solid #333; background: #87CEEB;"></canvas>
    <p style="margin-top: 10px;"><b>Управление:</b> Месси (W,A,D) | Роналду (Стрелки)</p>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Загрузка картинок
const messiImg = new Image(); messiImg.src = "{github_url}messi.png";
const ronaldoImg = new Image(); ronaldoImg.src = "{github_url}ronaldo.png";
const ballImg = new Image(); ballImg.src = "{github_url}ball.png";
const bgImg = new Image(); bgImg.src = "{github_url}background.png";
const goalImg = new Image(); goalImg.src = "{github_url}goal.png";

let p1 = {{ x: 80, y: 310, w: 70, h: 80, vy: 0, s: 0 }};
let p2 = {{ x: 550, y: 310, w: 70, h: 80, vy: 0, s: 0 }};
let ball = {{ x: 350, y: 150, r: 20, vx: 3, vy: 0 }};
let gravity = 0.6;
let timeLeft = 90;
let currentRound = 1;
let keys = {{}};

window.onkeydown = (e) => keys[e.code] = true;
window.onkeyup = (e) => keys[e.code] = false;

// Таймер
setInterval(() => {{
    if (timeLeft > 0) timeLeft--;
    else if (currentRound < 3) {{ timeLeft = 90; currentRound++; reset(); }}
}}, 1000);

function update() {{
    // Messi (W, A, D)
    if (keys["KeyA"] && p1.x > 0) p1.x -= 7;
    if (keys["KeyD"] && p1.x < 300) p1.x += 7;
    if (keys["KeyW"] && p1.y >= 310) p1.vy = -14;

    // Ronaldo (Arrows)
    if (keys["ArrowLeft"] && p2.x > 350) p2.x -= 7;
    if (keys["ArrowRight"] && p2.x < 630) p2.x += 7;
    if (keys["ArrowUp"] && p2.y >= 310) p2.vy = -14;

    p1.y += p1.vy; p1.vy += gravity;
    p2.y += p2.vy; p2.vy += gravity;
    if (p1.y > 310) {{ p1.y = 310; p1.vy = 0; }}
    if (p2.y > 310) {{ p2.y = 310; p2.vy = 0; }}

    ball.x += ball.vx; ball.y += ball.vy; ball.vy += 0.4;
    if (ball.y > 370) {{ ball.y = 370; ball.vy *= -0.7; }}
    if (ball.x < 15 || ball.x > 685) ball.vx *= -1;

    [p1, p2].forEach(p => {{
        if (ball.x + 15 > p.x && ball.x - 15 < p.x + p.w && ball.y + 15 > p.y && ball.y - 15 < p.y + p.h) {{
            ball.vy = -10;
            ball.vx = (ball.x - (p.x + p.w/2)) * 0.7;
        }}
    }});

    if (ball.x < 40 && ball.y > 250) {{ p2.s++; reset(); }}
    if (ball.x > 660 && ball.y > 250) {{ p1.s++; reset(); }}

    document.getElementById("score").innerText = `Messi ${{p1.s}} : ${{p2.s}} Ronaldo`;
    document.getElementById("timer").innerText = `Time: ${{timeLeft}}s`;
    document.getElementById("round").innerText = `Round: ${{currentRound}}`;
}}

function reset() {{
    ball.x = 350; ball.y = 100; ball.vx = (Math.random() > 0.5 ? 4 : -4); ball.vy = 0;
}}

function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Фон
    if (bgImg.complete) ctx.drawImage(bgImg, 0, 0, 700, 400);
    
    // Трава
    ctx.fillStyle = "rgba(0,150,0,0.3)"; ctx.fillRect(0, 380, 700, 20);

    // Ворота
    if (goalImg.complete) {{
        ctx.drawImage(goalImg, 0, 230, 60, 160);
        ctx.save();
        ctx.translate(700, 0); ctx.scale(-1, 1);
        ctx.drawImage(goalImg, 0, 230, 60, 160);
        ctx.restore();
    }}

    // Футболисты
    if (messiImg.complete) ctx.drawImage(messiImg, p1.x, p1.y, p1.w, p1.h);
    if (ronaldoImg.complete) ctx.drawImage(ronaldoImg, p2.x, p2.y, p2.w, p2.h);
    
    // Мяч
    if (ballImg.complete) ctx.drawImage(ballImg, ball.x-20, ball.y-20, 40, 40);
    else {{ ctx.fillStyle = "white"; ctx.beginPath(); ctx.arc(ball.x, ball.y, 15, 0, Math.PI*2); ctx.fill(); }}

    update();
    requestAnimationFrame(draw);
}}
draw();
</script>
"""

components.html(game_html, height=550)
