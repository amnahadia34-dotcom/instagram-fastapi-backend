from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Instagram Autoreply Bot</title>
    <style>
        body { margin:0; font-family:Arial; }
        .sidebar {
            width:260px;
            background:#111;
            color:white;
            height:100vh;
            padding:20px;
            position:fixed;
        }
        .main {
            margin-left:280px;
            padding:20px;
        }
        input, textarea {
            width:100%; padding:10px; margin-top:5px;
        }
        button {
            padding:10px 16px;
            background:#0066ff;
            color:white;
            border:none;
            cursor:pointer;
            margin-top:10px;
        }
        #statusPanel p { margin:5px 0; }
    </style>
</head>
<body>

<div class="sidebar">
    <h2>INSTAGRAM<br>AUTOREPLY BOT</h2>

    <h3>Settings</h3>
    <label>OpenAI API Key:</label>
    <input id="openaiKey" type="password">

    <label>Instagram Token:</label>
    <input id="igToken" type="password">

    <label>Instagram ID:</label>
    <input id="igID">

    <button onclick="saveSettings()">Save Settings</button>

    <h3>AutoReply Mode</h3>
    <button onclick="toggleAutoreply(true)" style="background:#00cc44;">Enable</button>
    <button onclick="toggleAutoreply(false)" style="background:#cc0000;">Disable</button>

    <h3>Status</h3>
    <div id="statusPanel"></div>
</div>

<div class="main">
    <h2>AI Reply Generator</h2>

    <textarea id="commentBox" rows="4" placeholder="Incoming Instagram Comment..."></textarea>
    <button onclick="generateReply()">Generate Reply</button>

    <h3>Generated Reply:</h3>
    <div id="replyBox" style="padding:15px; background:#eee;"></div>
</div>

<script>
async function loadSettings() {
    let res = await fetch("/settings/");
    let data = await res.json();

    document.getElementById("openaiKey").value = data.openai_key;
    document.getElementById("igToken").value = data.instagram_token;
    document.getElementById("igID").value = data.instagram_id;

    let s = document.getElementById("statusPanel");
    s.innerHTML = `
        <p>${data.openai_key ? "✔ OpenAI Ready" : "❌ Missing OpenAI Key"}</p>
        <p>${data.instagram_token ? "✔ Token OK" : "❌ No Instagram Token"}</p>
        <p>${data.instagram_id ? "✔ ID Loaded" : "❌ Missing Instagram ID"}</p>
        <p>Autoreply: ${data.autoreply_enabled ? "🟢 Enabled" : "🔴 Disabled"}</p>
    `;
}

async function saveSettings() {
    let payload = {
        openai_key: document.getElementById("openaiKey").value,
        instagram_token: document.getElementById("igToken").value,
        instagram_id: document.getElementById("igID").value,
        autoreply_enabled: false
    };

    await fetch("/settings/update", {
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body: JSON.stringify(payload)
    });

    alert("Settings Saved!");
    loadSettings();
}

async function toggleAutoreply(state) {
    let res = await fetch("/settings/");
    let data = await res.json();
    data.autoreply_enabled = state;

    await fetch("/settings/update", {
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body: JSON.stringify(data)
    });

    loadSettings();
}

async function generateReply() {
    let text = document.getElementById("commentBox").value;
    if (!text) return alert("Enter a comment");

    let res = await fetch("/webhook/generate", {
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body: JSON.stringify({ comment: text })
    });

    let data = await res.json();
    document.getElementById("replyBox").innerHTML = data.reply;
}

loadSettings();
</script>

</body>
</html>
"""

@router.get("/", response_class=HTMLResponse)
def home_page():
    return html
