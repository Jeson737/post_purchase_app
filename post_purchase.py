import streamlit as st
import os

st.set_page_config(page_title="Order Upload", layout="centered")

st.title("🏠 Custom House Portrait - Upload Details")

# --- URL PARAMS (NEW STREAMLIT API FIX) ---
query_params = st.query_params

email = query_params.get("email", "unknown")
order_id = query_params.get("order_id", "no-id")

# normalize (Streamlit sometimes returns list)
if isinstance(email, list):
    email = email[0]

if isinstance(order_id, list):
    order_id = order_id[0]

st.write(f"📧 Email: **{email}**")
st.write(f"🧾 Order ID: **{order_id}**")

st.divider()

# --- INPUTS ---
address = st.text_input("Property address")
notes = st.text_area("Special instructions")

image = st.file_uploader("Upload house image", type=["png", "jpg", "jpeg"])

# --- SAVE LOGIC ---
if st.button("Submit Order Details"):

    # base folder
    os.makedirs("orders", exist_ok=True)

    # unique folder per order
    folder_name = f"orders/{order_id or email}"
    os.makedirs(folder_name, exist_ok=True)

    data = {
        "email": email,
        "order_id": order_id,
        "address": address,
        "notes": notes
    }

    # save text data
    with open(f"{folder_name}/data.txt", "w") as f:
        for k, v in data.items():
            f.write(f"{k}: {v}\n")

    # save image
    if image:
        img_path = f"{folder_name}/{image.name}"
        with open(img_path, "wb") as f:
            f.write(image.getbuffer())

    st.success("✅ Order details saved successfully!")
    st.write("Saved in:", folder_name)
