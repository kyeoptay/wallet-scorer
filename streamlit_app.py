import streamlit as st

# --- Helpers ---
def deterministic_score(addr: str) -> int:
    if not addr:
        return 0
    h = 0
    for ch in addr:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF  # 32-bit wrap like JS >>> 0
    return h % 101  # 0..100

def classify(score: int) -> str:
    if score >= 75:
        return "Low Risk"
    if score >= 40:
        return "Medium Risk"
    return "High Risk"

# --- UI ---
st.set_page_config(page_title="Wallet Scorer", page_icon="⚡", layout="centered")

st.title("Wallet Scorer (Demo)")
st.caption("Deterministic demo using the same formula from the overlay/userscript")

# Read address from query param (?address=...)
addr = ""
# Try new API first, fallback to experimental for older Streamlit
try:
    qp = st.query_params  # type: ignore[attr-defined]
    if isinstance(qp, dict):
        addr = qp.get("address", [""])[0] if isinstance(qp.get("address"), list) else qp.get("address", "")
except Exception:
    try:
        qp = st.experimental_get_query_params()
        addr = qp.get("address", [""])[0] if "address" in qp else ""
    except Exception:
        addr = ""

# Input
addr = st.text_input("Solana wallet address", value=addr, placeholder="Paste a Solana address (32–44 chars Base58)")

if addr:
    score = deterministic_score(addr)
    bucket = classify(score)

    # badge-style headers
    st.metric(label="Score", value=score)
    st.write(f"**Risk bucket:** {bucket}")

    # Simple visualization
    st.progress(score/100)

    st.write("---")
    st.caption("Deep link to this result (shareable):")
    url = st.experimental_get_query_params  # fallback name while supporting both
    # set query param in page URL
    try:
        st.query_params.update({"address": addr})  # type: ignore[attr-defined]
    except Exception:
        st.experimental_set_query_params(address=addr)
    st.code(f"?address={addr}")

else:
    st.info("Enter a wallet address above or open this app via a link like `?address=<PUBKEY>`.")

st.write("---")
st.caption("Note: This is a demo formula for parity with your browser overlay; replace with real scoring when ready.")
