import React, { useState } from "react";
import axios from "axios";

export default function ChatBot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    // Add user message
    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        question: input,
      });
      setMessages([
        ...newMessages,
        { sender: "bot", text: res.data.answer || "No response." },
      ]);
    } catch (error) {
      setMessages([
        ...newMessages,
        { sender: "bot", text: "Error: Could not get response." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.chatBox}>
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              ...styles.message,
              alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
              background:
                msg.sender === "user" ? "#DCF8C6" : "white",
            }}
          >
            {msg.text}
          </div>
        ))}
        {loading && (
          <div style={styles.typing}>Bot is typing...</div>
        )}
      </div>
      <div style={styles.inputBox}>
        <input
          style={styles.input}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about UP laws..."
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button style={styles.button} onClick={handleSend}>
          Send
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    height: "100vh",
    background: "#f5f5f5",
    fontFamily: "Arial, sans-serif",
  },
  chatBox: {
    flex: 1,
    padding: "20px",
    display: "flex",
    flexDirection: "column",
    overflowY: "auto",
  },
  message: {
    padding: "10px 15px",
    borderRadius: "12px",
    marginBottom: "10px",
    maxWidth: "60%",
    boxShadow: "0 1px 2px rgba(0,0,0,0.1)",
  },
  inputBox: {
    display: "flex",
    padding: "10px",
    background: "#fff",
    borderTop: "1px solid #ddd",
  },
  input: {
    flex: 1,
    padding: "10px",
    borderRadius: "20px",
    border: "1px solid #ccc",
    outline: "none",
  },
  button: {
    marginLeft: "10px",
    padding: "10px 15px",
    borderRadius: "20px",
    border: "none",
    background: "#4285F4",
    color: "#fff",
    cursor: "pointer",
  },
  typing: {
    fontStyle: "italic",
    color: "#999",
  },
};
