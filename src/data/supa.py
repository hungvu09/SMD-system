import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)



admin_key: str = os.environ.get("SUPABASE_ROLE_KEY")
supabase_admin: Client = create_client(url, admin_key)


print("Supabase client initialized successfully!")