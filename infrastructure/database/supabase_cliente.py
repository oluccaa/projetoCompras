from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

def get_client() -> Client:
    """Retorna a instância do cliente Supabase."""
    return create_client(SUPABASE_URL, SUPABASE_KEY)