import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Configurações do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# Configurações do Kubernetes
K8S_CLUSTER_URL = os.getenv("K8S_CLUSTER_URL", "https://localhost:6443")
K8S_CA_CERT_PATH = os.getenv("K8S_CA_CERT_PATH", "/path/to/ca.crt")
K8S_USER_NAME = os.getenv("K8S_USER_NAME", "default_user")
K8S_CONTEXT_NAME = os.getenv("K8S_CONTEXT_NAME", "default_context")
