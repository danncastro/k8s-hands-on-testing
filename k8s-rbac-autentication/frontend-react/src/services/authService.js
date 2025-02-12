import api from "./api";

// Função para registrar um novo usuário
export const register = async (username, password) => {
    try {
        const response = await api.post("/auth/register", { username, password });
        return response.data;
    } catch (error) {
        throw error.response?.data?.detail || "Erro ao registrar o usuário";
    }
};

// Função para autenticar o usuário
export const login = async (username, password) => {
    try {
        // Criando o corpo da solicitação como um objeto simples
        const response = await api.post("/auth/login", new URLSearchParams({
            username: username,
            password: password
        }), {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded", // Usando o cabeçalho correto para enviar dados de formulário
            },
        });

        return response.data;
    } catch (error) {
        throw error.response?.data?.detail || "Erro ao autenticar o usuário";
    }
};
