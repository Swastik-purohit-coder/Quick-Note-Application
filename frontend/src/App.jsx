import { useState, useEffect } from "react";
import axios from "axios";
import Login from "./Login";
import Register from "./Register";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL;

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("token")
  );

  const [showRegister, setShowRegister] =
    useState(false);

  const [note, setNote] = useState("");
  const [notes, setNotes] = useState([]);
  const [editingId, setEditingId] =
    useState(null);

  const token = localStorage.getItem("token");

  const fetchNotes = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/notes`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setNotes(response.data);
    } catch (error) {
      console.error(
        "Error fetching notes:",
        error
      );

      if (
        error.response?.status === 401
      ) {
        localStorage.removeItem(
          "token"
        );
        setIsLoggedIn(false);
      }
    }
  };

  useEffect(() => {
    if (isLoggedIn) {
      fetchNotes();
    }
  }, [isLoggedIn]);

  const saveNote = async () => {
    if (!note.trim()) return;

    try {
      if (editingId) {
        await axios.put(
          `${API_URL}/notes/${editingId}`,
          {
            content: note,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        setEditingId(null);
      } else {
        await axios.post(
          `${API_URL}/notes`,
          {
            content: note,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
      }

      setNote("");
      fetchNotes();
    } catch (error) {
      console.error(error);
    }
  };

  const deleteNote = async (id) => {
    try {
      await axios.delete(
        `${API_URL}/notes/${id}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      fetchNotes();
    } catch (error) {
      console.error(error);
    }
  };

  const editNote = (item) => {
    setNote(item.content);
    setEditingId(item.id);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setIsLoggedIn(false);
  };

  if (!isLoggedIn) {
    if (showRegister) {
      return (
        <Register
          onBack={() =>
            setShowRegister(false)
          }
        />
      );
    }

    return (
      <Login
        onLogin={() =>
          setIsLoggedIn(true)
        }
        onRegister={() =>
          setShowRegister(true)
        }
      />
    );
  }

  return (
    <div className="container">
      <h1>🚀 Quick Notes</h1>

      <button
        onClick={logout}
        style={{
          marginBottom: "20px",
        }}
      >
        Logout
      </button>

      <textarea
        placeholder="Write your note here..."
        value={note}
        onChange={(e) =>
          setNote(e.target.value)
        }
      />

      <button onClick={saveNote}>
        {editingId
          ? "Update Note"
          : "Save Note"}
      </button>

      <h2>
        📝 Saved Notes ({notes.length})
      </h2>

      <div className="notes-list">
        {notes.map((item) => (
          <div
            className="note-card"
            key={item.id}
          >
            <p>{item.content}</p>

            <small>
              {new Date(
                item.created_at
              ).toLocaleString()}
            </small>

            <div className="actions">
              <button
                className="edit-btn"
                onClick={() =>
                  editNote(item)
                }
              >
                ✏️ Edit
              </button>

              <button
                className="delete-btn"
                onClick={() =>
                  deleteNote(item.id)
                }
              >
                🗑 Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;