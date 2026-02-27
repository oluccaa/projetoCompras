import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    supabase_url: str
    supabase_key: str
    caminho_excel: str
    app_env: str

def _get_env_var(nome: str) -> str:
    valor = os.getenv(nome)
    if not valor:
        raise EnvironmentError(f"Variável obrigatória não encontrada: {nome}")
    return valor

def get_settings() -> Settings:
    return Settings(
        supabase_url=_get_env_var("SUPABASE_URL"),
        supabase_key=_get_env_var("SUPABASE_KEY"),
        caminho_excel=_get_env_var("CAMINHO_EXCEL"),
        app_env=os.getenv("APP_ENV", "development"),
    )