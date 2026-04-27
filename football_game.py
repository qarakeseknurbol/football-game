import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Head Soccer: Messi vs Ronaldo", layout="centered")
st.title("⚽️ Super Cup: Almaty Edition")

# Игровой движок
game_code = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
<script>
let p1, p2, ball;
let gravity = 0.6;
let round = 1, timer = 90, score1 = 0, score2 = 0;
let isGameOver = false;

let messiImg, ronaldoImg, ballImg, bgImg, goalImg;

function preload() {
  // Используем прямые ссылки на сырые файлы из GitHub (Raw)
  // ВАЖНО: Замени 'qarakaseknurbol' на свое имя пользователя, если оно другое
  let baseUrl = 'https://raw.githubusercontent.com/qarakaseknurbol/marketing/main/';
  
  messiImg = loadImage(baseUrl + 'messi.png');
  ronaldoImg = loadImage(baseUrl + 'ronaldo.png');
  ballImg = loadImage(baseUrl + 'ball.png');
  bgImg = loadImage(baseUrl + 'background.png');
  goalImg = loadImage(baseUrl + 'goal.png');
}

function setup() {
  let canvas = createCanvas(800, 500);
  p1 = new Player(100, messiImg, 65, 68, 87); 
  p2 = new Player(width - 200, ronaldoImg, LEFT_ARROW, RIGHT_ARROW, UP_ARROW);
  ball = new Ball();
}

function draw() {
  if (bgImg && bgImg.width > 1) { background(bgImg); } 
  else { background(135, 206, 235); }
  
  fill(34, 139, 34, 150);
  rect(0, height - 30, width, 30);
  
  if (goalImg && goalImg.width > 1) {
     image(goalImg, 0, height - 200, 80, 180);
     push();
     translate(width, height - 200);
     scale(-1,1);
     image(goalImg, 0, 0, 80, 180);
     pop();
  }

  if (!isGameOver) {
    p1.update(); p2.update(); ball.update();
    if (frameCount % 60 == 0 && timer > 0) timer--;
    if (timer == 0) {
      if (round < 3) { round++; timer = 90; resetLevel(); } 
      else { isGameOver = true; }
    }
  }

  p1.show(); p2.show(); ball.show();
  ball.checkCol(p1); ball.checkCol(p2);
  showUI();
}

function resetLevel() {
    p1.x = 100; p2.x = width - 200;
    ball.x = width/2; ball.y = height/2;
    ball.vx = 0; ball.vy = 0;
}

function showUI() {
    fill(0, 0, 0, 120);
    rect(0, 0, width, 60);
    fill(255); textAlign(CENTER); textSize(32);
    text(score1 + " : " + score2, width/2, 40);
    textSize(20); textAlign(LEFT); text("Round: " + round, 20, 35);
    textAlign(RIGHT); text("Time: " + timer + "s", width - 20, 35);
    if (isGameOver) {
        fill(0, 150); rect(0,0, width, height);
        fill(255); textAlign(CENTER); textSize(60);
        let winner = score1 > score2 ? "Messi Wins!" : (score1 < score2 ? "Ronaldo Wins!" : "Draw!");
        text("GAME OVER", width/2, height/2 - 20);
        textSize(40); text(winner, width/2, height/2 + 40);
    }
}

class Player {
  constructor(x, img, l, r, u) {
    this.x = x; this.y = height - 130;
    this.w = 90; this.h = 110;
    this.img = img; this.vy = 0;
    this.l = l; this.r = r; this.u = u;
  }
  show() {
    if (this.img && this.img.width > 1) { image(this.img, this.x, this.y, this.w, this.h); } 
    else { fill(200); rect(this.x, this.y, this.w, this.h); }
  }
  update() {
    if (keyIsDown(this.l)) this.x -= 8;
    if (keyIsDown(this.r)) this.x += 8;
    if (keyIsDown(this.u) && this.y >= height - 130) this.vy = -15;
    this.y += this.vy; this.vy += gravity;
    this.y = constrain(this.y, 0, height - 130);
    this.x = constrain(this.x, 0, width - this.w);
  }
}

class Ball {
  constructor() { this.x = width/2; this.y = height/2; this.vx = 0; this.vy = 0; this.d = 40; }
  show() {
    if (ballImg && ballImg.width > 1) { image(ballImg, this.x - 20, this.y - 20, 40, 40); } 
    else { fill(255); ellipse(this.x, this.y, this.d); }
  }
  update() {
    this.x += this.vx; this.y += this.vy;
    this.vy += gravity * 0.5; this.vx *= 0.99;
    if (this.y > height - 45) { this.y = height - 45; this.vy *= -0.7; }
    if (this.x < 20 || this.x > width - 20) { this.vx *= -1; }
    if (this.x < 50 && this.y > height - 200) { score2++; resetLevel(); }
    if (this.x > width - 50 && this.y > height - 200) { score1++; resetLevel(); }
  }
  checkCol(p) {
    if (this.x > p.x && this.x < p.x + p.w && this.y > p.y && this.y < p.y + p.h) {
      this.vy = -10;
      this.vx = (this.x - (p.x + p.w/2)) * 0.6;
    }
  }
}
</script>
"""

components.html(game_code, height=550, width=850)
