# 飞机大战小游戏 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete airplane battle (飞机大战) arcade game with Flask backend, HTML5 Canvas frontend, and JSON data persistence.

**Architecture:** Python Flask serves the game page and provides REST APIs for reading/writing game stats. The frontend is a single HTML file with inline CSS and JS rendering a vertical-scrolling shooter on Canvas. Game data (high score, kill counts) persists in `data.json` on the server.

**Tech Stack:** Python 3 + Flask, HTML5 Canvas, Vanilla JS, JSON file storage

---

## File Structure

```
c:\Users\lenovo\Desktop\飞机大战2\
├── app.py                   # Flask 后端: 静态文件 + REST API
├── requirements.txt         # pip 依赖
├── data.json                # JSON 数据存储
└── templates/
    └── index.html           # 游戏前端 (全部 HTML + CSS + JS 在此)
```

## Dependency Graph

```
Task 1 (Backend) ──────────────────────────────┐
                                               │
Task 2 (HTML/CSS skeleton) ◄───────────────────┤
                                               │
Task 3 (Player + Controls) ◄───────────────────┤
                                               │
Task 4 (Enemy System) ◄────────────────────────┤
                                               │
Task 5 (Collision + Damage) ◄──────────────────┤
                                               │
Task 6 (Scoring + API + Game Flow) ◄───────────┘
                                               │
Task 7 (Final Integration) ◄───────────────────┘
```

Tasks 2-6 all modify `templates/index.html`. They build on each other sequentially — Task 6 depends on all prior JS components being in place.

---

### Task 1: Flask 后端 + JSON 数据层

**Files:**
- Create: `c:\Users\lenovo\Desktop\飞机大战2\requirements.txt`
- Create: `c:\Users\lenovo\Desktop\飞机大战2\data.json`
- Create: `c:\Users\lenovo\Desktop\飞机大战2\app.py`

- [ ] **Step 1: 创建 requirements.txt**

```txt
flask>=3.0
```

- [ ] **Step 2: 创建 data.json（初始数据）**

```json
{
  "high_score": 0,
  "total_games": 0,
  "total_kills": 0,
  "kills_by_type": {
    "small": 0,
    "medium": 0,
    "boss": 0
  },
  "last_score": 0
}
```

- [ ] **Step 3: 创建 app.py（Flask 后端）**

```python
import json
import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json')

def load_data():
    """从 JSON 文件读取游戏数据"""
    if not os.path.exists(DATA_FILE):
        return {
            "high_score": 0,
            "total_games": 0,
            "total_kills": 0,
            "kills_by_type": {"small": 0, "medium": 0, "boss": 0},
            "last_score": 0
        }
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    """保存游戏数据到 JSON 文件"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    """返回游戏主页"""
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    """获取游戏数据（最高分、统计等）"""
    return jsonify(load_data())

@app.route('/api/save', methods=['POST'])
def save_game_data():
    """更新游戏数据（保存新成绩）"""
    data = load_data()
    new_data = request.json
    # 只合并顶层已知字段
    for key in ('high_score', 'total_games', 'total_kills', 'kills_by_type', 'last_score'):
        if key in new_data:
            data[key] = new_data[key]
    save_data(data)
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

- [ ] **Step 4: 安装依赖并验证后端**

```bash
cd "c:\Users\lenovo\Desktop\飞机大战2"
pip install flask
python app.py
```

预期: 终端显示 `Running on http://127.0.0.1:5000`，浏览器访问该地址应返回 404（尚未创建模板），但访问 `http://localhost:5000/api/data` 应返回 JSON 数据。按 Ctrl+C 停止。

---

### Task 2: 前端 HTML 结构 + CSS 样式

**Files:**
- Create: `c:\Users\lenovo\Desktop\飞机大战2\templates\index.html`（写入 HTML 骨架 + CSS）

- [ ] **Step 1: 创建 index.html（HTML 骨架 + CSS）**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>飞机大战</title>
    <style>
        /* ============ 全局 ============ */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #0a0a2e;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            overflow: hidden;
        }

        /* ============ 游戏容器 ============ */
        #game-wrapper {
            position: relative;
            border: 2px solid #334;
            border-radius: 8px;
            box-shadow: 0 0 40px rgba(0, 100, 255, 0.3);
        }

        canvas {
            display: block;
            background: #0d0d3b;
            border-radius: 6px;
            cursor: none;
        }

        /* ============ 覆盖层（开始 / 结束） ============ */
        .overlay {
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: rgba(0, 0, 0, 0.75);
            border-radius: 6px;
            z-index: 10;
        }

        .overlay h1 {
            color: #fff;
            font-size: 48px;
            margin-bottom: 10px;
            text-shadow: 0 0 20px rgba(0, 150, 255, 0.8);
        }

        .overlay .subtitle {
            color: #aac;
            font-size: 18px;
            margin-bottom: 30px;
        }

        .overlay .stats {
            color: #ccc;
            font-size: 16px;
            margin-bottom: 10px;
            line-height: 1.8;
        }

        .overlay .stats span {
            color: #ffd700;
            font-weight: bold;
        }

        .btn {
            padding: 12px 40px;
            font-size: 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            background: linear-gradient(135deg, #4CAF50, #2196F3);
            color: #fff;
            font-weight: bold;
            transition: transform 0.15s, box-shadow 0.15s;
            margin-top: 20px;
        }

        .btn:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(76, 175, 80, 0.5);
        }

        .btn:active { transform: scale(0.95); }

        /* ============ HUD ============ */
        #hud {
            position: absolute;
            top: 0; left: 0;
            width: 100%;
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            pointer-events: none;
            z-index: 5;
            font-size: 18px;
            color: #fff;
            text-shadow: 0 0 10px rgba(0,0,0,0.8);
        }

        #hud-hp { font-size: 22px; }
        #hud-score { font-weight: bold; color: #ffd700; }

        .hidden { display: none !important; }
    </style>
</head>
<body>
    <div id="game-wrapper">
        <canvas id="gameCanvas" width="800" height="600"></canvas>

        <!-- HUD -->
        <div id="hud">
            <span id="hud-hp">❤️❤️❤️❤️❤️</span>
            <span id="hud-score">0</span>
        </div>

        <!-- 开始画面 -->
        <div id="startOverlay" class="overlay">
            <h1>✈️ 飞机大战</h1>
            <p class="subtitle">消灭敌机 · 争取高分</p>
            <button class="btn" id="startBtn">开始游戏</button>
        </div>

        <!-- 游戏结束画面 -->
        <div id="gameOverOverlay" class="overlay hidden">
            <h1>💥 游戏结束</h1>
            <div class="stats" id="gameOverStats"></div>
            <button class="btn" id="restartBtn">再来一局</button>
        </div>
    </div>

    <script>
        // ============================================================
        // 所有 JavaScript 游戏代码将在 Task 3 ~ 6 中逐步添加
        // ============================================================
    </script>
</body>
</html>
```

- [ ] **Step 2: 验证页面显示**

```bash
cd "c:\Users\lenovo\Desktop\飞机大战2"
python app.py
```

浏览器访问 `http://localhost:5000`，应看到：
- 深蓝色背景的游戏画布（800×600）
- "开始游戏" 按钮覆盖层
- 左上角 ❤️❤️❤️❤️❤️，右上角 0

按 Ctrl+C 停止。

---

### Task 3: 前端 JS — 玩家飞机 + 键盘控制 + 自动射击

**Files:**
- Modify: `c:\Users\lenovo\Desktop\飞机大战2\templates\index.html`（在 `<script>` 标签中添加 JS 代码）

- [ ] **Step 1: 在 `<script>` 标签中添加 Canvas 初始化 + 游戏常量 + 玩家系统**

```javascript
// ============================================================
// 飞机大战 — 游戏引擎
// ============================================================

// ---------- Canvas 初始化 ----------
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const W = 800, H = 600;

// ---------- DOM 元素 ----------
const hudHp = document.getElementById('hud-hp');
const hudScore = document.getElementById('hud-score');
const startOverlay = document.getElementById('startOverlay');
const gameOverOverlay = document.getElementById('gameOverOverlay');
const gameOverStats = document.getElementById('gameOverStats');

// ---------- 游戏常量 ----------
const PLAYER_SPEED = 7;           // 玩家移动速度（水平快）
const PLAYER_FIRE_INTERVAL = 200; // 自动射击间隔 (ms)
const PLAYER_SIZE = 24;           // 玩家飞机尺寸

// 三种敌机配置
const ENEMY_CONFIG = {
    small: { hp: 1, speed: 3, fireRate: 1500, score: 100, size: 18, color: '#4CAF50', label: '小型机' },
    medium: { hp: 2, speed: 2, fireRate: 1200, score: 200, size: 28, color: '#FF9800', label: '中型机' },
    boss: { hp: 5, speed: 1.2, fireRate: 800, score: 500, size: 42, color: '#f44336', label: '大型机' }
};

// ---------- 游戏状态 ----------
const state = {
    status: 'START',          // START | PLAYING | GAME_OVER
    score: 0,
    hp: 5,
    maxHp: 5,
    frame: 0,
    lastFireTime: 0,
    enemies: [],
    playerBullets: [],
    enemyBullets: [],
    keys: {},
    killCounts: { small: 0, medium: 0, boss: 0 },
    dataLoaded: false,
    highScore: 0,
    totalGames: 0
};

// ---------- 玩家对象 ----------
const player = {
    x: W / 2,
    y: H - 80,
    w: PLAYER_SIZE,
    h: PLAYER_SIZE
};

// ---------- 键盘事件 ----------
document.addEventListener('keydown', (e) => {
    state.keys[e.key] = true;
    // 阻止箭头键滚动页面
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '].includes(e.key)) {
        e.preventDefault();
    }
});

document.addEventListener('keyup', (e) => {
    state.keys[e.key] = false;
});

// ---------- 绘制玩家飞机 ----------
function drawPlayer() {
    const { x, y, w } = player;
    ctx.save();

    // 机身 (三角形)
    ctx.beginPath();
    ctx.moveTo(x, y - w * 0.7);          // 机头
    ctx.lineTo(x - w * 0.6, y + w * 0.5); // 左下
    ctx.lineTo(x, y + w * 0.3);           // 中下
    ctx.lineTo(x + w * 0.6, y + w * 0.5); // 右下
    ctx.closePath();

    // 渐变填充
    const grad = ctx.createLinearGradient(x, y - w, x, y + w);
    grad.addColorStop(0, '#64B5F6');
    grad.addColorStop(1, '#1565C0');
    ctx.fillStyle = grad;
    ctx.fill();
    ctx.strokeStyle = '#90CAF9';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // 驾驶舱
    ctx.beginPath();
    ctx.arc(x, y - w * 0.2, w * 0.15, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(144, 202, 249, 0.5)';
    ctx.fill();

    // 尾焰
    const flicker = Math.random() * 6 + 4;
    ctx.beginPath();
    ctx.moveTo(x - w * 0.2, y + w * 0.3);
    ctx.lineTo(x, y + w * 0.3 + flicker);
    ctx.lineTo(x + w * 0.2, y + w * 0.3);
    ctx.fillStyle = '#FF9800';
    ctx.fill();

    ctx.restore();
}

// ---------- 玩家移动 ----------
function updatePlayer() {
    const k = state.keys;
    if (k['ArrowLeft'] || k['a'] || k['A']) player.x -= PLAYER_SPEED;
    if (k['ArrowRight'] || k['d'] || k['D']) player.x += PLAYER_SPEED;
    if (k['ArrowUp'] || k['w'] || k['W']) player.y -= PLAYER_SPEED;
    if (k['ArrowDown'] || k['s'] || k['S']) player.y += PLAYER_SPEED;

    // 边界限制
    player.x = Math.max(player.w * 0.6, Math.min(W - player.w * 0.6, player.x));
    player.y = Math.max(player.w * 0.7, Math.min(H - player.w * 0.5, player.y));
}

// ---------- 子弹系统 ----------
function fireBullet(x, y, speed, isEnemy, w, h, color) {
    return {
        x: x, y: y,
        w: w || 4, h: h || 12,
        speed: speed,
        isEnemy: isEnemy || false,
        color: color || '#FFD700'
    };
}

// 玩家自动射击
function autoShoot() {
    const now = Date.now();
    if (now - state.lastFireTime >= PLAYER_FIRE_INTERVAL) {
        state.playerBullets.push(
            fireBullet(player.x, player.y - player.w * 0.7, -8, false, 4, 14, '#FFD700')
        );
        state.lastFireTime = now;
    }
}

// 更新子弹位置
function updateBullets() {
    // 玩家子弹
    for (let i = state.playerBullets.length - 1; i >= 0; i--) {
        state.playerBullets[i].y += state.playerBullets[i].speed;
        if (state.playerBullets[i].y + state.playerBullets[i].h < 0 || state.playerBullets[i].y > H) {
            state.playerBullets.splice(i, 1);
        }
    }

    // 敌机子弹
    for (let i = state.enemyBullets.length - 1; i >= 0; i--) {
        state.enemyBullets[i].y += state.enemyBullets[i].speed;
        if (state.enemyBullets[i].y > H || state.enemyBullets[i].y + state.enemyBullets[i].h < 0) {
            state.enemyBullets.splice(i, 1);
        }
    }
}

// ---------- 绘制子弹 ----------
function drawBullets() {
    // 玩家子弹
    for (const b of state.playerBullets) {
        ctx.save();
        const grad = ctx.createLinearGradient(b.x, b.y - b.h/2, b.x, b.y + b.h/2);
        grad.addColorStop(0, '#FFF176');
        grad.addColorStop(1, '#FFD700');
        ctx.fillStyle = grad;
        ctx.fillRect(b.x - b.w/2, b.y - b.h/2, b.w, b.h);
        ctx.restore();
    }

    // 敌机子弹
    for (const b of state.enemyBullets) {
        ctx.save();
        ctx.fillStyle = '#FF5252';
        ctx.shadowBlur = 8;
        ctx.shadowColor = '#FF5252';
        ctx.beginPath();
        ctx.arc(b.x, b.y, b.w/2, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }
}

// ---------- 简单测试函数 ----------
function testPlayerControls() {
    console.log('[任务3] 玩家系统已加载');
    console.log(`[任务3] 射速: ${PLAYER_FIRE_INTERVAL}ms/发`);
    console.log('[任务3] 方向键/WASD 移动');
}
```

- [ ] **Step 2: 添加临时渲染循环验证**

```javascript
// ---------- 临时渲染循环（验证玩家显示和移动） ----------
function tempGameLoop(timestamp) {
    // 清屏
    ctx.fillStyle = '#0d0d3b';
    ctx.fillRect(0, 0, W, H);

    // 画星星背景
    for (let i = 0; i < 50; i++) {
        const sx = (i * 137 + 50) % W;
        const sy = (i * 97 + timestamp / 50) % H;
        ctx.fillStyle = `rgba(255,255,255,${0.3 + (i % 3) * 0.3})`;
        ctx.fillRect(sx, sy, 1.5, 1.5);
    }

    updatePlayer();
    autoShoot();
    updateBullets();
    drawPlayer();
    drawBullets();
    requestAnimationFrame(tempGameLoop);
}
```

等待 Task 6 将临时循环替换为正式游戏循环。现在先用 `testPlayerControls()` 验证加载。

- [ ] **Step 3: 启动前端验证**

启动 Flask 后打开浏览器 → F12 控制台输入 `testPlayerControls()` → 确认三条日志输出。

---

### Task 4: 前端 JS — 三种敌机系统

**Files:**
- Modify: `c:\Users\lenovo\Desktop\飞机大战2\templates\index.html`（在 Task 3 代码后面追加敌机系统）

- [ ] **Step 1: 创建敌机生成函数 + 三种敌机绘制**

在 Task 3 的 `testPlayerControls()` 函数之后添加以下代码：

```javascript
// ============================================================
// 敌机系统
// ============================================================

// ---------- 生成单个敌机 ----------
function spawnEnemy() {
    const types = ['small', 'medium', 'boss'];
    // 权重: 小型 60%, 中型 30%, Boss 10%
    const weights = [0.60, 0.30, 0.10];
    let r = Math.random(), cum = 0, chosenType = 'small';
    for (let i = 0; i < types.length; i++) {
        cum += weights[i];
        if (r <= cum) { chosenType = types[i]; break; }
    }

    const cfg = ENEMY_CONFIG[chosenType];
    const x = cfg.size + Math.random() * (W - cfg.size * 2);
    return {
        type: chosenType,
        x: x,
        y: -cfg.size,
        w: cfg.size,
        h: cfg.size,
        hp: cfg.hp,
        maxHp: cfg.hp,
        speed: cfg.speed,
        fireRate: cfg.fireRate,
        score: cfg.score,
        color: cfg.color,
        lastFireTime: Date.now()
    };
}

// ---------- 更新敌机位置 ----------
function updateEnemies() {
    // 生成新敌机（帧率60fps，每40帧生成一架，逐渐加快）
    const spawnRate = Math.max(15, 40 - Math.floor(state.score / 500));
    if (state.frame % spawnRate === 0) {
        state.enemies.push(spawnEnemy());
    }

    // 移动敌机 + 敌机射击
    const now = Date.now();
    for (let i = state.enemies.length - 1; i >= 0; i--) {
        const e = state.enemies[i];
        e.y += e.speed;

        // 敌机射击
        if (now - e.lastFireTime >= e.fireRate) {
            state.enemyBullets.push(
                fireBullet(e.x, e.y + e.h/2, 4, true, 6, 6, '#FF5252')
            );
            e.lastFireTime = now;
        }

        // 出界移除
        if (e.y > H + e.h) {
            state.enemies.splice(i, 1);
        }
    }
}

// ---------- 绘制敌机 ----------
function drawEnemies() {
    for (const e of state.enemies) {
        ctx.save();
        const { x, y, w, h, color, type, hp, maxHp } = e;

        // 机身
        ctx.beginPath();
        if (type === 'boss') {
            // Boss: 六边形
            for (let i = 0; i < 6; i++) {
                const angle = (Math.PI / 3) * i - Math.PI / 6;
                const px = x + w/2 * Math.cos(angle);
                const py = y + h/2 * Math.sin(angle);
                i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
            }
        } else if (type === 'medium') {
            // 中型机: 倒三角形
            ctx.moveTo(x, y + h/2);
            ctx.lineTo(x - w/2, y - h/2);
            ctx.lineTo(x + w/2, y - h/2);
        } else {
            // 小型机: 小倒三角
            ctx.moveTo(x, y + h/2);
            ctx.lineTo(x - w/2, y - h/2);
            ctx.lineTo(x + w/2, y - h/2);
        }
        ctx.closePath();

        ctx.fillStyle = color;
        ctx.fill();
        ctx.strokeStyle = 'rgba(255,255,255,0.3)';
        ctx.lineWidth = 1;
        ctx.stroke();

        // 血条（多血量敌机显示）
        if (maxHp > 1) {
            const barW = w;
            const barH = 4;
            const barX = x - barW/2;
            const barY = y - h/2 - 8;
            // 背景
            ctx.fillStyle = 'rgba(0,0,0,0.6)';
            ctx.fillRect(barX, barY, barW, barH);
            // 血量
            const ratio = hp / maxHp;
            ctx.fillStyle = ratio > 0.5 ? '#4CAF50' : ratio > 0.25 ? '#FF9800' : '#f44336';
            ctx.fillRect(barX, barY, barW * ratio, barH);
        }

        ctx.restore();
    }
}
```

- [ ] **Step 2: 在临时循环中添加敌机更新和绘制**

找到 `tempGameLoop` 函数，在 `autoShoot()` 之后和 `updateBullets()` 之前添加：

```javascript
    updateEnemies();
```

在 `drawPlayer()` 之后添加：

```javascript
    drawEnemies();
```

- [ ] **Step 3: 前端验证**

启动 Flask 后打开浏览器 → 使用 Task 6 之前的临时设置验证：
- 控制台运行 `state.status = 'PLAYING'; requestAnimationFrame(tempGameLoop);`
- 应看到三种颜色的敌机从顶部出现
- 敌机会向下移动并发射红色子弹
- Boss 有血条显示，需多枪击毁

---

### Task 5: 前端 JS — 碰撞检测 + 伤害系统

**Files:**
- Modify: `c:\Users\lenovo\Desktop\飞机大战2\templates\index.html`（追加碰撞检测代码）

- [ ] **Step 1: 添加 AABB 碰撞检测函数**

在敌机系统的 `drawEnemies()` 函数之后添加：

```javascript
// ============================================================
// 碰撞检测系统
// ============================================================

// ---------- AABB 矩形碰撞检测 ----------
function checkCollision(a, b) {
    return a.x - a.w/2 < b.x + b.w/2 &&
           a.x + a.w/2 > b.x - b.w/2 &&
           a.y - a.h/2 < b.y + b.h/2 &&
           a.y + a.h/2 > b.y - b.h/2;
}

// ---------- 处理所有碰撞 ----------
function handleCollisions() {
    // 1) 玩家子弹 vs 敌机
    for (let bi = state.playerBullets.length - 1; bi >= 0; bi--) {
        const bullet = state.playerBullets[bi];
        let bulletUsed = false;

        for (let ei = state.enemies.length - 1; ei >= 0; ei--) {
            const enemy = state.enemies[ei];
            if (checkCollision(bullet, enemy)) {
                enemy.hp--;
                bulletUsed = true;

                if (enemy.hp <= 0) {
                    // 击毁敌机
                    state.score += enemy.score;
                    state.killCounts[enemy.type]++;
                    state.total_kills = (state.total_kills || 0) + 1;
                    state.enemies.splice(ei, 1);

                    // 爆炸特效粒子
                    spawnExplosion(enemy.x, enemy.y, enemy.color);
                }
                break; // 一颗子弹只打中一个敌机
            }
        }

        if (bulletUsed) {
            state.playerBullets.splice(bi, 1);
        }
    }

    // 2) 敌机子弹 vs 玩家
    for (let bi = state.enemyBullets.length - 1; bi >= 0; bi--) {
        const bullet = state.enemyBullets[bi];
        if (checkCollision(bullet, player)) {
            state.enemyBullets.splice(bi, 1);
            takeDamage();
        }
    }

    // 3) 敌机 vs 玩家（碰撞）
    for (let ei = state.enemies.length - 1; ei >= 0; ei--) {
        const enemy = state.enemies[ei];
        if (checkCollision(enemy, player)) {
            state.enemies.splice(ei, 1);
            takeDamage();
            spawnExplosion(enemy.x, enemy.y, enemy.color);
        }
    }
}

// ---------- 受伤处理 ----------
function takeDamage() {
    state.hp--;
    updateHUD();
    if (state.hp <= 0) {
        gameOver();
    }
}

// ---------- 更新 HUD ----------
function updateHUD() {
    const hearts = '❤️'.repeat(Math.max(0, state.hp)) + '🖤'.repeat(Math.max(0, state.maxHp - state.hp));
    hudHp.textContent = hearts || '💀';
    hudScore.textContent = state.score;
}
```

- [ ] **Step 2: 添加爆炸粒子特效（视觉反馈）**

```javascript
// ============================================================
// 粒子特效系统
// ============================================================

const particles = [];

function spawnExplosion(x, y, color) {
    for (let i = 0; i < 12; i++) {
        const angle = (Math.PI * 2 / 12) * i + Math.random() * 0.3;
        const speed = 1 + Math.random() * 3;
        particles.push({
            x: x, y: y,
            vx: Math.cos(angle) * speed,
            vy: Math.sin(angle) * speed,
            life: 30 + Math.random() * 20,
            maxLife: 50,
            size: 2 + Math.random() * 3,
            color: color
        });
    }
}

function updateParticles() {
    for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.life--;
        if (p.life <= 0) {
            particles.splice(i, 1);
        }
    }
}

function drawParticles() {
    for (const p of particles) {
        const alpha = p.life / p.maxLife;
        ctx.save();
        ctx.globalAlpha = alpha;
        ctx.fillStyle = p.color;
        ctx.shadowBlur = 10;
        ctx.shadowColor = p.color;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size * alpha, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }
}
```

- [ ] **Step 3: 在临时循环中添加碰撞和粒子**

在 `tempGameLoop` 的 `updateBullets()` 之后添加：

```javascript
    handleCollisions();
    updateParticles();
```

在 `drawEnemies()` 之后添加：

```javascript
    drawParticles();
```

- [ ] **Step 4: 前端验证**

运行游戏循环，验证：
- 玩家子弹击中小型机 → 直接爆炸消失 + 粒子特效
- 击中中型机 → 血条减少，需2枪击毁
- 被敌机子弹击中 → HP 减少
- 与敌机碰撞 → HP 减少 + 敌机消失
- HP 归零 → 控制台输出伤害日志

---

### Task 6: 前端 JS — 积分系统 + API 集成 + 游戏流程

**Files:**
- Modify: `c:\Users\lenovo\Desktop\飞机大战2\templates\index.html`（替换临时循环为正式游戏循环 + API 调用）

- [ ] **Step 1: 添加 API 通信层**

在粒子系统代码之后添加：

```javascript
// ============================================================
// API 通信层
// ============================================================

async function loadGameData() {
    try {
        const res = await fetch('/api/data');
        const data = await res.json();
        state.highScore = data.high_score || 0;
        state.totalGames = data.total_games || 0;
        state.total_kills = data.total_kills || 0;
        // 合并 kills_by_type
        if (data.kills_by_type) {
            state.killCounts.small += data.kills_by_type.small || 0;
            state.killCounts.medium += data.kills_by_type.medium || 0;
            state.killCounts.boss += data.kills_by_type.boss || 0;
        }
        state.dataLoaded = true;
        console.log('[API] 游戏数据已加载');
    } catch (err) {
        console.warn('[API] 加载失败，使用本地数据', err);
        state.dataLoaded = true;
    }
}

async function saveGameData() {
    const cumulative = {
        high_score: Math.max(state.score, state.highScore),
        total_games: state.totalGames + 1,
        total_kills: (state.total_kills || 0) + Object.values(state.killCounts).reduce((a,b) => a+b, 0),
        kills_by_type: {
            small: state.killCounts.small,
            medium: state.killCounts.medium,
            boss: state.killCounts.boss
        },
        last_score: state.score
    };
    try {
        await fetch('/api/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(cumulative)
        });
        console.log('[API] 游戏数据已保存');
    } catch (err) {
        console.warn('[API] 保存失败', err);
    }
}
```

- [ ] **Step 2: 替换临时循环为正式游戏主循环**

移除旧的 `tempGameLoop` 函数（从 `function tempGameLoop` 到文件末尾），替换为：

```javascript
// ============================================================
// 游戏主循环
// ============================================================

function gameLoop(timestamp) {
    if (state.status === 'PLAYING') {
        state.frame++;

        // 更新
        updatePlayer();
        autoShoot();
        updateEnemies();
        updateBullets();
        handleCollisions();
        updateParticles();

        // 渲染
        render();
    }

    requestAnimationFrame(gameLoop);
}

function render() {
    // 清屏
    ctx.fillStyle = '#0d0d3b';
    ctx.fillRect(0, 0, W, H);

    // 星空背景
    for (let i = 0; i < 60; i++) {
        const sx = (i * 137 + 50) % W;
        const sy = (i * 97 + performance.now() / 50) % H;
        const brightness = 0.2 + (i % 4) * 0.2;
        ctx.fillStyle = `rgba(255,255,255,${brightness})`;
        const starSize = i % 3 === 0 ? 2 : 1;
        ctx.fillRect(sx, sy, starSize, starSize);
    }

    // 绘制游戏对象
    drawPlayer();
    drawEnemies();
    drawBullets();
    drawParticles();
}

// ---------- 游戏启动 ----------
function startGame() {
    // 重置状态
    state.status = 'PLAYING';
    state.score = 0;
    state.hp = state.maxHp;
    state.frame = 0;
    state.lastFireTime = 0;
    state.enemies = [];
    state.playerBullets = [];
    state.enemyBullets = [];
    state.killCounts = { small: 0, medium: 0, boss: 0 };

    // 重置玩家位置
    player.x = W / 2;
    player.y = H - 80;

    // 隐藏覆盖层
    startOverlay.classList.add('hidden');
    gameOverOverlay.classList.add('hidden');

    updateHUD();
}

// ---------- 游戏结束 ----------
function gameOver() {
    state.status = 'GAME_OVER';

    // 保存数据
    saveGameData();

    // 更新最高分
    if (state.score > state.highScore) {
        state.highScore = state.score;
    }

    // 显示结算面板
    const totalKilled = Object.values(state.killCounts).reduce((a,b) => a+b, 0);
    gameOverStats.innerHTML = `
        得分: <span>${state.score}</span> 分<br>
        最高分: <span>${state.highScore}</span> 分<br>
        击落小型机: <span>${state.killCounts.small}</span> 架<br>
        击落中型机: <span>${state.killCounts.medium}</span> 架<br>
        击落大型机: <span>${state.killCounts.boss}</span> 架<br>
        共击落: <span>${totalKilled}</span> 架
    `;
    gameOverOverlay.classList.remove('hidden');
}
```

- [ ] **Step 3: 绑定按钮事件 + 初始化**

```javascript
// ============================================================
// 初始化
// ============================================================

document.getElementById('startBtn').addEventListener('click', () => {
    startGame();
});

document.getElementById('restartBtn').addEventListener('click', () => {
    startGame();
});

// 页面加载后读数据并启动循环
loadGameData().then(() => {
    gameLoop();
});
```

- [ ] **Step 4: 在 HUD 更新中同步显示最高分（可选）**

更新 `updateHUD()` 函数中 `hudScore.textContent` 行，在 `hudScore.textContent = state.score;` 之前或之后可以显示额外信息。当前保持简洁。

- [ ] **Step 5: 完整功能验证**

```bash
cd "c:\Users\lenovo\Desktop\飞机大战2"
python app.py
```

浏览器测试清单：
- [ ] 初始页面显示开始画面和最高分（从 API 加载）
- [ ] 点击"开始游戏" → 游戏开始，HUD 显示 ❤️❤️❤️❤️❤️ 和 0分
- [ ] 方向键/WASD 控制玩家移动
- [ ] 玩家自动连续射击
- [ ] 敌机从顶部出现并下落
- [ ] 三种敌机颜色/大小/血量不同
- [ ] 敌机发射红色子弹
- [ ] 击落小型机 +100分，中型机 +200分，Boss +500分
- [ ] 被子弹击中或碰撞 → HP 减少
- [ ] HP 归零 → 游戏结束面板显示统计
- [ ] 数据保存到后端（检查 data.json 是否更新）
- [ ] 再次开始游戏 → 最高分保留

---

### Task 7: 最终集成 + 视觉打磨

**Files:**
- Modify: `c:\Users\lenovo\Desktop\飞机大战2\templates\index.html`（调整代码 / 修复问题）
- Verify: 启动完整游戏

- [ ] **Step 1: 代码完整性审查**

检查以下内容是否到位：
- `updateHUD()` 在 `startGame()` 中被调用
- `takeDamage()` 正确调用 `gameOver()` 当 HP = 0
- 玩家子弹不会超出画布（边界移除逻辑）
- 敌机出界被移除
- 游戏结束后不再更新游戏对象（检查 `state.status` 守卫）

修复可能的问题：

**问题1: 游戏结束后玩家仍可移动**

在 `updatePlayer()` 函数开头添加守卫：

```javascript
function updatePlayer() {
    if (state.status !== 'PLAYING') return;
    // ...原有代码...
}
```

**问题2: 自动射击在游戏结束后不应继续**

在 `autoShoot()` 开头添加守卫：

```javascript
function autoShoot() {
    if (state.status !== 'PLAYING') return;
    // ...原有代码...
}
```

**问题3: 加载数据时等待**

确认 `startGame()` 只在 `dataLoaded = true` 后可用。如按钮在数据加载前被点击，应等待。

在 `startBtn` 和 `restartBtn` 的点击事件中添加检查：

```javascript
document.getElementById('startBtn').addEventListener('click', () => {
    if (!state.dataLoaded) return;
    startGame();
});
```

- [ ] **Step 2: 启动全功能测试**

```bash
cd "c:\Users\lenovo\Desktop\飞机大战2"
python app.py
```

打开 `http://localhost:5000`，进行完整游戏流程测试。

- [ ] **Step 3: 最终代码检查 — 确认完整文件**

读取最终 `templates/index.html`，确保所有部分完整连接：
1. HTML 骨架 + CSS 样式
2. Canvas 初始化 + DOM 引用
3. 游戏常量 + 状态管理
4. 玩家系统（移动、绘制、射击）
5. 敌机系统（生成、移动、射击、绘制）
6. 碰撞检测 + 伤害系统 + 粒子特效
7. API 通信层（加载/保存数据）
8. 游戏主循环 + 渲染
9. 游戏流程控制（开始/结束/重新开始）
10. 按钮事件绑定 + 初始化

## 验证清单

完成所有任务后，逐一验证：

| # | 验证项 | 预期结果 |
|---|--------|---------|
| 1 | 启动后端 | `http://localhost:5000` 打开游戏 |
| 2 | 开始游戏 | 点击按钮后覆盖层消失，游戏启动 |
| 3 | 玩家移动 | 方向键/WASD 控制飞机 |
| 4 | 自动射击 | 玩家持续发射金色子弹 |
| 5 | 三种敌机 | 绿(小)、橙(中)、红(大) 从顶部出现 |
| 6 | 敌机射击 | 敌机发射红色子弹 |
| 7 | 击毁得分 | 小型+100、中型+200、Boss+500 |
| 8 | 受伤扣血 | 被击中后 ❤️ 减少 |
| 9 | 5次死亡 | 游戏结束，显示结算 |
| 10 | 数据持久化 | 刷新页面后最高分保留 |
| 11 | 重玩 | 点击"再来一局"后重置游戏 |
