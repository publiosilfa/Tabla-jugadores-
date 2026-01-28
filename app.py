import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tabla de Jugadores", page_icon="🎮", layout="centered")

st.title("🎮 Tabla de jugadores")
st.caption("Escribe un valor para un jugador y se acumula. Puedes reiniciar cuando quieras.")

# --- Estado inicial ---
if "players" not in st.session_state:
    st.session_state.players = ["Jugador 1", "Jugador 2", "Jugador 3", "Jugador 4", "Jugador 5", "Jugador 6"]

if "scores" not in st.session_state:
    st.session_state.scores = {name: 0 for name in st.session_state.players}

if "history" not in st.session_state:
    st.session_state.history = []  # lista de dicts: {"Jugador":..., "Valor":...}

# --- Configuración de nombres ---
st.subheader("👥 Jugadores (puedes cambiar nombres)")

cols = st.columns(3)
new_names = []
for i, name in enumerate(st.session_state.players):
    with cols[i % 3]:
        new_names.append(st.text_input(f"Jugador {i+1}", value=name, key=f"name_{i}").strip() or f"Jugador {i+1}")

# Si cambian nombres, migrar puntajes conservando valores por posición
if new_names != st.session_state.players:
    old_scores = [st.session_state.scores.get(n, 0) for n in st.session_state.players]
    st.session_state.players = new_names
    st.session_state.scores = {new_names[i]: int(old_scores[i]) for i in range(len(new_names))}

st.divider()

# --- Agregar puntos ---
st.subheader("➕ Agregar valor")

c1, c2, c3 = st.columns([2, 2, 1])
with c1:
    jugador = st.selectbox("Jugador", st.session_state.players)
with c2:
    valor = st.number_input("Valor a sumar", value=0, step=1)
with c3:
    st.write("")
    st.write("")
    if st.button("Sumar ✅", use_container_width=True):
        st.session_state.scores[jugador] = int(st.session_state.scores.get(jugador, 0) + valor)
        st.session_state.history.append({"Jugador": jugador, "Valor": int(valor)})
        st.toast(f"Sumado {int(valor)} a {jugador}", icon="✅")

# --- Tabla ---
st.subheader("📊 Acumulado")

df = pd.DataFrame(
    [{"Jugador": k, "Acumulado": v} for k, v in st.session_state.scores.items()]
).sort_values("Acumulado", ascending=False, ignore_index=True)

st.dataframe(df, use_container_width=True, hide_index=True)

# --- Historial y reinicio ---
with st.expander("🧾 Ver historial de sumas"):
    if st.session_state.history:
        st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True, hide_index=True)
    else:
        st.info("Todavía no has sumado valores.")

st.divider()

colr1, colr2 = st.columns(2)
with colr1:
    if st.button("🔄 Reiniciar acumulados", use_container_width=True):
        st.session_state.scores = {name: 0 for name in st.session_state.players}
        st.session_state.history = []
        st.toast("Reiniciado.", icon="🔄")

with colr2:
    total = int(df["Acumulado"].sum()) if not df.empty else 0
    st.metric("Total acumulado", total)
