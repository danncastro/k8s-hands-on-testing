-- Usar o banco de dados
\c kubeconfig;

-- Criação da tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,                -- ID único do usuário
    username VARCHAR(255) UNIQUE NOT NULL, -- Nome de usuário único
    password_hash TEXT NOT NULL,          -- Hash da senha
    email VARCHAR(255) UNIQUE,            -- Email (opcional)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Data de criação
);