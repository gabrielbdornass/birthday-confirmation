from supabase import create_client, Client
from env_vars import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_to_supabase(st, sponsor_name, companions, total):

    try:
        data = {
            "sponsor_name": sponsor_name,
            "companions": companions,
            "total": total,
        }
        response = supabase.table("confirmations").insert(data).execute()
        if type(response.data[0]['id']) == int:
            return True
        else:
            st.error(f"Falha para salvar sua resposta: {response.json()}")
            return False
    except Exception as e:
        st.error(f"Algum erro aconteceu: {e}")
        return False
