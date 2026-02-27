
from supabase import create_client, Client
from config import get_settings

def get_client() -> Client:
    """Retorna a instância do cliente Supabase."""
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_key)    