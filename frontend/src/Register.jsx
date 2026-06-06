import { useState } from "react";
import axios from "axios";

function Register({ onBack }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const registerUser = async () => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/register",
        {
          email,
          password,
        }
      );

      alert(response.data.message);

      onBack();
    } catch (error) {
      alert(
        error.response?.data?.message ||
        "Registration Failed"
      );
    }
  };

  return (
    <div className="container">
      <h1>📝 Register</h1>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) =>
          setEmail(e.target.value)
        }
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) =>
          setPassword(e.target.value)
        }
      />

      <button onClick={registerUser}>
        Register
      </button>

      <button onClick={onBack}>
        Back To Login
      </button>
    </div>
  );
}

export default Register;