import React, { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import { FaMicrophone, FaPlus, FaVideo } from "react-icons/fa";
import { FiImage } from "react-icons/fi";
import { BiDotsHorizontalRounded } from "react-icons/bi";
import "highlight.js/styles/github-dark.css";
import { motion } from "framer-motion";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

 const handleSend = async () => {
  if (!input.trim()) return;

  // Add user message to UI
  setMessages((prev) => [...prev, { sender: "user", text: input }]);

  try {
    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: input }),
    });

    const data = await res.json();

    // Add bot response to UI
    setMessages((prev) => [...prev, { sender: "bot", text: data.answer }]);

  } catch (error) {
    console.error("Error fetching from backend:", error);
    setMessages((prev) => [...prev, { sender: "bot", text: "⚠️ Could not connect to backend." }]);
  }

  setInput("");
};


  return (
    <div style={styles.container}>
      {/* Chat area */}
      <div style={styles.chatArea}>
        {messages.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            style={styles.greeting}
          >
            Hello, Harshit
          </motion.div>
        ) : (
          messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              style={{
                ...styles.message,
                alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
                background:
                  msg.sender === "user" ? "#3a3a3a" : "#1f1f1f",
              }}
            >
              {msg.sender === "bot" ? (
                <ReactMarkdown
                  children={msg.text}
                  remarkPlugins={[remarkGfm]}
                  rehypePlugins={[rehypeHighlight]}
                  components={{
                    a: ({ node, ...props }) => (
                      <a
                        {...props}
                        style={{ color: "#4d9eff" }}
                        target="_blank"
                        rel="noreferrer"
                      />
                    ),
                  }}
                />
              ) : (
                msg.text
              )}
            </motion.div>
          ))
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Input Bar */}
      <div style={styles.inputContainer}>
        <div style={styles.inputBar}>
          <FaPlus style={styles.icon} />
          <FaVideo style={styles.icon} />
          <FiImage style={styles.icon} />
          <input
            style={styles.input}
            placeholder="Ask LawBot"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <BiDotsHorizontalRounded style={styles.icon} />
          <FaMicrophone style={styles.icon} />
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    background: "#121212",
    color: "white",
    height: "100vh",
    display: "flex",
    flexDirection: "column",
  },
  chatArea: {
    flex: 1,
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    padding: "20px",
  },
  greeting: {
    fontSize: "32px",
    fontWeight: "500",
    color: "#4d9eff",
    marginTop: "40vh",
    textAlign: "center",
  },
  message: {
    maxWidth: "75%",
    padding: "12px 16px",
    borderRadius: "18px",
    marginBottom: "10px",
    wordBreak: "break-word",
    fontSize: "15px",
    lineHeight: 1.5,
  },
  inputContainer: {
    display: "flex",
    justifyContent: "center",
    padding: "10px 0",
    background: "#121212",
  },
  inputBar: {
    display: "flex",
    alignItems: "center",
    padding: "8px 16px",
    background: "#1f1f1f",
    borderRadius: "40px",
    width: "90%",
    maxWidth: "800px",
  },
  input: {
    flex: 1,
    border: "none",
    outline: "none",
    background: "transparent",
    color: "white",
    fontSize: "16px",
    padding: "8px",
  },
  icon: {
    fontSize: "18px",
    color: "#bbb",
    margin: "0 6px",
    cursor: "pointer",
  },
};
