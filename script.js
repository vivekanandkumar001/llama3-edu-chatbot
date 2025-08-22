// DOM Elements
const messagesEl = document.querySelector(".messages");
const inputEl = document.querySelector("#user-input");
const sendBtn = document.querySelector("#send-btn");

// Utility: Add message to chat window
function addMessage(text, sender = "bot") {
  const msgEl = document.createElement("div");
  msgEl.className = `msg ${sender}`;
  msgEl.textContent = text;
  messagesEl.appendChild(msgEl);
  messagesEl.scrollTop = messagesEl.scrollHeight; // auto-scroll
}

// API: Send message to backend
async function sendMessage(message) {
  try {
    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message, name: "User" })
    });

    if (!res.ok) {
      throw new Error("Server error: " + res.status);
    }

    const data = await res.json();
    return data.reply || "Sorry, I couldn’t find an answer.";
  } catch (err) {
    console.error("Chat error:", err);
    return "⚠️ Connection issue. Please try again.";
  }
}

// API: Save lead (if user provides info)
async function saveLead(name, email, phone) {
  try {
    const formData = new FormData();
    formData.append("name", name);
    formData.append("email", email);
    formData.append("phone", phone);

    const res = await fetch("http://127.0.0.1:8000/lead", {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
      throw new Error("Lead save failed: " + res.status);
    }

    const data = await res.json();
    return data.status;
  } catch (err) {
    console.error("Lead error:", err);
    return "⚠️ Could not save details.";
  }
}

// Handle send button / Enter key
async function handleSend() {
  const text = inputEl.value.trim();
  if (!text) return;

  addMessage(text, "user");
  inputEl.value = "";

  // Get bot reply
  const reply = await sendMessage(text);
  addMessage(reply, "bot");
}

// Event listeners (safe check)
if (sendBtn) {
  sendBtn.addEventListener("click", handleSend);
}
if (inputEl) {
  inputEl.addEventListener("keypress", (e) => {
    if (e.key === "Enter") handleSend();
  });
}

// Initial greeting
addMessage("👋 Hi, I’m EduBot! Ask me about our courses (Python, Data Science, AI, ML, GenAI, etc.)", "bot");
