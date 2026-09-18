import streamlit as st
from google import genai

# Nastavení vzhledu stránky
st.set_page_config(page_title="Moje Rodinná AI", page_icon="🤖")

# --- KROK: ZABEZPEČENÍ HESLEM ---
ZADANE_HESLO = st.text_input("Zadej heslo pro přístup k AI:", type="password")

# Zde si nastav své vlastní heslo (místo 'tajneheslo123')
TAJNE_HESLO = "tajneheslo123"

if ZADANE_HESLO != TAJNE_HESLO:
    if ZADANE_HESLO != "":
        st.error("Nesprávné heslo! Přístup odepřen.")
    st.warning("Pro použití aplikace musíš zadat správné heslo.")
    st.stop() # Zastaví načítání zbytku aplikace, dokud není heslo správně

# --- JAKMILE JE HESLO SPRÁVNĚ, NAČTE SE CHAT ---
st.title("🤖 Naše Rodinná AI")
st.write("Vítej! Jsem tvoje osobní AI asistentka.")

# Načtení API klíče z trezoru Streamlitu
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Chybí API klíč v nastavení Streamlitu!")
    st.stop()

# Inicializace Gemini klienta
client = genai.Client(api_key=api_key)

# Uchování historie chatu v paměti relace
if "messages" not in st.session_state:
    st.session_state.messages = []

# Zobrazení dosavadní historie správ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Vstupní pole pro dotaz od uživatele
if prompt := st.chat_input("Napiš něco..."):
    # Zobraz zprávu uživatele
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Získej odpověď od Gemini
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            full_response = response.text
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Chyba při komunikaci s AI: {e}")
