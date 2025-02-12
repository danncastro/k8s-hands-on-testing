import { useState } from "react";
import api from "../services/api";

function LoginForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null); // Limpa mensagens de erro anteriores

    try {
      const response = await api.post("/auth/login", { username, password });
      localStorage.setItem("token", response.data.access_token);
      alert("Login realizado com sucesso!");
      window.location.href = "/dashboard"; // Redireciona após login
    } catch (err) {
      if (err.response && err.response.data) {
        const errorDetail = err.response.data.detail;

        if (Array.isArray(errorDetail)) {
          // Caso seja uma lista de erros
          setError(
            errorDetail.map((err) => `${err.msg} (Campo: ${err.input || "N/A"})`)
          );
        } else if (typeof errorDetail === "string") {
          // Caso seja uma string simples
          setError([errorDetail]);
        } else {
          console.error("Formato de erro inesperado:", errorDetail);
          setError(["Ocorreu um erro inesperado."]);
        }
      } else {
        setError(["Não foi possível se conectar ao servidor."]);
      }
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Usuário"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Senha"
          required
        />
        <button type="submit">Login</button>
      </form>

      {error && (
        <div style={{ color: "red", marginTop: "1rem" }}>
          <p>Erro(s):</p>
          <ul>
            {error.map((err, index) => (
              <li key={index}>{err}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default LoginForm;
