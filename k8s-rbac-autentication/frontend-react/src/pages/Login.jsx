// eslint-disable-next-line no-unused-vars
import React, { useState } from "react";
import { login } from "../services/authService";

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLogin = async (e) => {
        e.preventDefault();

        // Criando um objeto FormData para enviar no formato correto
        const formData = new FormData();
        formData.append("username", username);
        formData.append("password", password);

        try {
            // Chama o serviço de login e espera a resposta
            const response = await login(formData);
            
            // Caso o login seja bem-sucedido, exibe o alerta com a resposta
            alert("Login bem-sucedido: " + JSON.stringify(response));
        } catch (err) {
            // Se ocorrer um erro, extrai a mensagem de erro
            if (err.response && err.response.data && err.response.data.detail) {
                // Para erros de API (retornados com status HTTP diferente de 2xx)
                setError(err.response.data.detail); // Pega o erro da resposta
            } else {
                // Para erros gerais
                setError("Ocorreu um erro inesperado. Tente novamente.");
            }
        }
    };

    return (
        <div>
            <h1>Login</h1>
            <form onSubmit={handleLogin}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit">Entrar</button>
            </form>

            {/* Exibe a mensagem de erro se houver */}
            {error && <p style={{ color: "red" }}>{error}</p>}
        </div>
    );
};

export default Login;
