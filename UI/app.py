import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="IRD Tax Assistant", layout="centered")

st.title("🇱🇰 IRD Tax Intelligence Assistant")
st.caption("Answers based only on official IRD documents")

st.divider()

# ---------------- Upload PDF ----------------
st.header("📄 Upload IRD PDF")
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
    r = requests.post(f"{API_BASE}/documents/upload", files=files)
    if r.ok:
        st.success("PDF uploaded successfully")
    else:
        st.error(r.text)

# ---------------- Index PDFs ----------------
st.header("📚 Index Documents")
if st.button("Index All PDFs"):
    r = requests.post(f"{API_BASE}/documents/index")
    if r.ok:
        data = r.json()
        st.success(f"Indexed {data['total_chunks']} chunks")
    else:
        st.error(r.text)

# ---------------- Ask Question ----------------
st.header("💬 Ask a Tax Question")
question = st.text_input("Enter your question")

if st.button("Ask") and question.strip():
    payload = {"question": question}
    r = requests.post(f"{API_BASE}/query", json=payload)

    if r.ok:
        res = r.json()

        st.subheader("✅ Answer")
        st.write(res["answer"])

        if res["citations"]:
            st.subheader("📌 Citations")
            for c in res["citations"]:
                st.markdown(
                    f"- **{c['document']}** | Page {c['page']} | Section: {c['section']}"
                )

        st.info(res["disclaimer"])
    else:
        st.error(r.text)
