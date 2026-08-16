import React, { useState, useEffect, useRef } from "react";
import "./App.css";
import IconButton from "@mui/material/IconButton";
import Refresh from "@mui/icons-material/Refresh";
function App() {

  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState("");

  const [chat, setChat] = useState(() => {
    const saved = localStorage.getItem("chatHistory");
    return saved
      ? JSON.parse(saved)
      : [{ sender: "bot", text: "Hi 👋 I'm your University Helpdesk Assistant. Ask your issue." }];
  });

  const [suggestions, setSuggestions] = useState([]);
  const [categories, setCategories] = useState([]);
  const [issues, setIssues] = useState([]);

  const [typing, setTyping] = useState(false);

  const [quickOpen, setQuickOpen] = useState(true);   //  quick help collapse

  const [showTicket, setShowTicket] = useState(false);
  const [description, setDescription] = useState("");
  const [file, setFile] = useState(null);

  const [rotating, setRotating] = useState(false);   //  refresh animation state

  const chatEndRef = useRef(null);
  const socketRef = useRef(null);

  // -----------------------------
  // Refresh Chat
  // -----------------------------

  const refreshChat = () => {

    setRotating(true);   // start rotate animation

    localStorage.removeItem("chatHistory");

    setChat([
      { sender: "bot", text: "Hi 👋 I'm your University Helpdesk Assistant. Ask your issue." }
    ]);

    setSuggestions([]);
    setIssues([]);
    setTyping(false);
    setShowTicket(false);
    setDescription("");
    setFile(null);

    // scroll bottom
    setTimeout(() => {
      chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, 100);

    // stop rotate animation
    setTimeout(() => {
      setRotating(false);
    }, 500);
  };
  // -----------------------------
  // Save chat history
  // -----------------------------

  useEffect(() => {
    localStorage.setItem("chatHistory", JSON.stringify(chat));
  }, [chat]);

  // -----------------------------
  // Auto scroll
  // -----------------------------

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat]);

  // -----------------------------
  // Load categories
  // -----------------------------

  useEffect(() => {

    fetch("http://127.0.0.1:8000/categories")
      .then(res => res.json())
      .then(data => setCategories(data))
      .catch(() => console.log("Category load failed"));

  }, []);

  // -----------------------------
  // WebSocket connect
  // -----------------------------

  useEffect(() => {

    socketRef.current = new WebSocket("ws://127.0.0.1:8000/ws/chat");

    socketRef.current.onmessage = (event) => {

      const data = JSON.parse(event.data);

      setTyping(false);

      if (data.suggestions) {

        setSuggestions(data.suggestions);

        setChat(prev => [
          ...prev,
          { sender: "bot", text: "Did you mean one of these issues?" }
        ]);

      }

    };

    return () => socketRef.current.close();

  }, []);

  // -----------------------------
  // Send message
  // -----------------------------

  const sendMessage = () => {

  if (!message.trim()) return;

  setIssues([]);
  setSuggestions([]);

  const userMsg = {
    sender: "user",
    text: message,
    time: new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})
  };

  setChat(prev => [...prev, userMsg]);

  setTyping(true);

  socketRef.current.send(message);

  setMessage("");
};
  // -----------------------------
  // Suggestion clicked
  // -----------------------------

  const selectIssue = async (issue) => {

    setSuggestions([]);
    setIssues([]);

    setChat(prev => [...prev, { sender: "user", text: issue }]);

    try {

      setTyping(true);

      const response = await fetch("http://127.0.0.1:8000/issue-response", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ issue: issue })
      });

      const data = await response.json();

      setTyping(false);

      setChat(prev => [
        ...prev,
        { sender: "bot", text: data.response },
        { sender: "bot", text: "Did this solve your issue?" }
      ]);

    } catch {

      setTyping(false);

      setChat(prev => [
        ...prev,
        { sender: "bot", text: "⚠️ Server error." }
      ]);

    }

  };

  // -----------------------------
  // Category click
  // -----------------------------

  const selectCategory = (category) => {

    const selected = categories.find(c => c.category === category);

    if (selected) {
      setIssues(selected.issues);
      setSuggestions([]);
    }

  };

  // -----------------------------
  // Quick issue click
  // -----------------------------

  const selectQuickIssue = async (issue) => {

    setIssues([]);

    setChat(prev => [...prev, { sender: "user", text: issue }]);

    try {

      setTyping(true);

      const response = await fetch("http://127.0.0.1:8000/issue-response", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ issue: issue })
      });

      const data = await response.json();

      setTyping(false);

      setChat(prev => [
        ...prev,
        { sender: "bot", text: data.response },
        { sender: "bot", text: "Did this solve your issue?" }
      ]);

    } catch {

      setTyping(false);

      setChat(prev => [
        ...prev,
        { sender: "bot", text: "⚠️ Server error." }
      ]);

    }

  };

  // -----------------------------
  // YES
  // -----------------------------

  const resolveIssue = () => {

    setChat(prev => [
      ...prev,
      { sender: "bot", text: "Glad I could help 😊" }
    ]);

  };

  // -----------------------------
  // NO
  // -----------------------------

  const raiseTicket = () => {

    setShowTicket(true);

  };

  // -----------------------------
  // Create ticket
  // -----------------------------

  const submitTicket = async () => {

    if (!description.trim()) {
      alert("Please describe your issue");
      return;
    }

    const formData = new FormData();

    formData.append("description", description);

    if (file) formData.append("file", file);

    try {

      const response = await fetch("http://127.0.0.1:8000/create-ticket", {
        method: "POST",
        body: formData
      });

      const data = await response.json();

      setChat(prev => [
        ...prev,
        { sender: "bot", text: "🎫 Ticket Created: " + data.ticket_id }
      ]);

      setShowTicket(false);
      setDescription("");
      setFile(null);

    } catch {

      setChat(prev => [
        ...prev,
        { sender: "bot", text: "⚠️ Ticket creation failed." }
      ]);

    }

  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (

    <>

      <div className="chatWidget" onClick={() => setIsOpen(!isOpen)}>
        💬
      </div>

      {isOpen && (

      <div className="container">

        <div className="header">

<span>🎓 University Helpdesk</span>

<IconButton
  className={rotating ? "rotate" : ""}
  onClick={refreshChat}
  aria-label="refresh"
  title="Refresh Chat"
>
  <Refresh />
</IconButton>
          
</div>

        {/* Quick Help */}

        <div className="quickHelp">

          <div
            className="quickHelpTop"
            onClick={() => setQuickOpen(!quickOpen)}
          >
            <h4>Quick Help</h4>
            <span className="quickArrow">
              {quickOpen ? "▲" : "▼"}
            </span>
          </div>

          {quickOpen && (

          <div className="categories">

            {categories.map((c, i) => (

              <button
                key={i}
                className="quickBtn"
                onClick={() => selectCategory(c.category)}
              >
                {c.category}
              </button>

            ))}

          </div>

          )}

        </div>

        {issues.length > 0 && (

          <div className="suggestions">

            {issues.map((issue, i) => (

              <button
                key={i}
                className="suggestBtn"
                onClick={() => selectQuickIssue(issue)}
              >
               {issue}
              </button>

            ))}

          </div>

        )}

        {/* Chat */}

        <div className="chatbox">

          {chat.map((msg, index) => (

            <div
              key={index}
              className={`message ${msg.sender}`}
            >
              {msg.text}
            </div>

          ))}

          {/* Typing dots */}

          {typing && (
            <div className="typing">
              <span></span>
              <span></span>
              <span></span>
            </div>
          )}

          {suggestions.length > 0 && (

            <div className="suggestions">

              {suggestions.map((s, i) => (

                <button
                  key={i}
                  className="suggestBtn"
                  onClick={() => selectIssue(s.issue)}
                >
                  {s.issue}
                </button>

              ))}

            </div>

          )}

          {suggestions.length === 0 &&
           chat.length > 0 &&
           chat[chat.length - 1].text === "Did this solve your issue?" && (

            <div className="suggestions">

              <button className="suggestBtn" onClick={resolveIssue}>
                Yes 👍
              </button>

              <button className="suggestBtn" onClick={raiseTicket}>
                No ❌
              </button>

            </div>

          )}

          {showTicket && (

            <div className="ticketForm">

              <textarea
                placeholder="Describe your issue..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />

              <input
                type="file"
                onChange={(e) => setFile(e.target.files[0])}
              />

              <button onClick={submitTicket}>
                Create Ticket
              </button>

            </div>

          )}

          <div ref={chatEndRef}></div>

        </div>

        <div className="inputBox">

          <input
            type="text"
            placeholder="Ask your issue..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyPress}
          />

          <button onClick={sendMessage}>
            Send
          </button>

        </div>

      </div>

      )}

    </>
  );

}

export default App;