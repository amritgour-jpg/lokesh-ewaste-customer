from streamlit_geolocation import streamlit_geolocation
import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import date

st.set_page_config(
    page_title="RecycleX | E-Waste Pickup",
    page_icon="♻️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------
# RECYCLEX CUSTOMER WEBSITE DESIGN
# ---------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --rx-green: #087A43;
    --rx-deep: #075B35;
    --rx-bright: #35B66A;
    --rx-pale: #EAF6EE;
    --rx-ink: #17251C;
    --rx-muted: #68776D;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 5% 0%, rgba(53,182,106,.13), transparent 24rem),
        linear-gradient(180deg, #F4FAF6 0%, #FFFFFF 48%);
    color: var(--rx-ink);
}

header[data-testid="stHeader"] {
    background: rgba(255,255,255,.72);
}

.block-container {
    max-width: 760px;
    padding-top: 1.3rem;
    padding-bottom: 2.5rem;
}

.rx-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 18px;
    border-radius: 22px;
    color: white;
    background: linear-gradient(120deg, #075B35, #0B874B);
    box-shadow: 0 12px 28px rgba(7,91,53,.18);
    margin-bottom: 22px;
}
.rx-mark {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 54px;
    height: 54px;
    flex: 0 0 54px;
    border-radius: 17px;
    background: rgba(255,255,255,.15);
    font-size: 31px;
}
.rx-brand-name {
    font-size: 27px;
    line-height: 1.05;
    font-weight: 800;
    letter-spacing: -.8px;
}
.rx-brand-tag {
    margin-top: 5px;
    color: rgba(255,255,255,.83);
    font-size: 12px;
    letter-spacing: .4px;
}
.rx-hero {
    padding: 6px 3px 18px;
}
.rx-eyebrow {
    color: var(--rx-green);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-size: 11px;
    font-weight: 800;
}
.rx-hero-title {
    color: var(--rx-deep);
    font-size: clamp(27px, 6vw, 38px);
    line-height: 1.12;
    letter-spacing: -1.2px;
    font-weight: 800;
    margin: 8px 0;
}
.rx-hero-copy {
    color: var(--rx-muted);
    font-size: 15px;
    line-height: 1.55;
}
.rx-feature {
    background: white;
    border: 1px solid #DFECE2;
    border-radius: 17px;
    padding: 14px;
    min-height: 95px;
    box-shadow: 0 7px 22px rgba(22,75,42,.045);
}
.rx-feature-icon {
    font-size: 23px;
}
.rx-feature-title {
    font-weight: 800;
    color: var(--rx-deep);
    margin-top: 5px;
    font-size: 14px;
}
.rx-feature-copy {
    color: var(--rx-muted);
    font-size: 11px;
    margin-top: 2px;
}
h1, h2, h3 {
    color: var(--rx-deep) !important;
    font-weight: 800 !important;
    letter-spacing: -.6px;
}
h1 { font-size: clamp(1.8rem, 6vw, 2.35rem) !important; }
h2 { font-size: 1.55rem !important; }
h3 { font-size: 1.15rem !important; }

div[data-testid="stForm"] {
    background: rgba(255,255,255,.97);
    border: 1px solid #DFECE2;
    border-radius: 20px;
    padding: 1.15rem 1.1rem .9rem;
    box-shadow: 0 10px 30px rgba(23,75,43,.055);
}
.stTextInput input, .stTextArea textarea, .stNumberInput input,
div[data-baseweb="select"] > div {
    border-radius: 12px !important;
    border-color: #D6E4D9 !important;
    background: #FBFDFB !important;
}
.stTextInput input:focus, .stTextArea textarea:focus,
.stNumberInput input:focus {
    border-color: var(--rx-green) !important;
    box-shadow: 0 0 0 1px var(--rx-green) !important;
}
.stButton > button, .stFormSubmitButton > button {
    background: linear-gradient(135deg, #159454, #087A43) !important;
    color: white !important;
    border: 0 !important;
    border-radius: 13px !important;
    min-height: 2.9rem;
    padding: .55rem 1.2rem;
    font-weight: 800 !important;
    box-shadow: 0 7px 18px rgba(8,122,67,.17);
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, #087A43, #075B35) !important;
}
div[role="radiogroup"] { gap: .55rem; }
div[role="radiogroup"] label {
    background: #F0F7F1;
    border: 1px solid #DCEADE;
    border-radius: 12px;
    padding: .42rem .75rem;
}
[data-testid="stAlert"] { border-radius: 13px; }
[data-testid="stDataFrame"] {
    border: 1px solid #DFECE2;
    border-radius: 13px;
    overflow: hidden;
}
hr { border-color: #E3ECE5; }
.rx-footer {
    color: #829087;
    text-align: center;
    font-size: 11px;
    padding: 22px 0 8px;
}
@media (max-width: 640px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: .8rem;
    }
    .rx-brand { padding: 13px 14px; border-radius: 18px; }
    .rx-brand-name { font-size: 24px; }
    div[data-testid="stForm"] {
        padding: .95rem .8rem .75rem;
        border-radius: 17px;
    }
    .stButton > button, .stFormSubmitButton > button { width: 100%; }
}
</style>
""", unsafe_allow_html=True)

# RecycleX visual header
st.markdown("""
<div class="rx-brand">
  <div class="rx-mark">♻️</div>
  <div>
    <div class="rx-brand-name">RecycleX</div>
    <div class="rx-brand-tag">SMART E-WASTE COLLECTION</div>
  </div>
</div>
<div class="rx-hero">
  <div class="rx-eyebrow">A cleaner tomorrow starts today</div>
  <div class="rx-hero-title">Give your e-waste a responsible next life.</div>
  <div class="rx-hero-copy">Book a convenient pickup for your old electronics. Simple, responsible e-waste collection in Kolkata.</div>
</div>
""", unsafe_allow_html=True)

# Small service highlights
f1, f2, f3 = st.columns(3)
with f1:
    st.markdown('<div class="rx-feature"><div class="rx-feature-icon">📦</div><div class="rx-feature-title">Easy pickup</div><div class="rx-feature-copy">Request collection online</div></div>', unsafe_allow_html=True)
with f2:
    st.markdown('<div class="rx-feature"><div class="rx-feature-icon">📍</div><div class="rx-feature-title">Location aware</div><div class="rx-feature-copy">Share your pickup GPS</div></div>', unsafe_allow_html=True)
with f3:
    st.markdown('<div class="rx-feature"><div class="rx-feature-icon">♻️</div><div class="rx-feature-title">Responsible</div><div class="rx-feature-copy">Support better recycling</div></div>', unsafe_allow_html=True)

st.write("")

# Create a separate Supabase client for this browser session.
# Keep customer sessions isolated; do not share authenticated clients.
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# Restore this customer's login session.
if st.session_state.get("access_token"):
    try:
        supabase.auth.set_session(
            st.session_state["access_token"],
            st.session_state["refresh_token"]
        )
    except Exception:
        for key in [
            "access_token", "refresh_token",
            "customer_id", "customer_name", "customer_phone"
        ]:
            st.session_state.pop(key, None)

# ---------------------------------
# LOGIN AND REGISTRATION
# ---------------------------------
if not st.session_state.get("access_token"):
    menu = st.radio(
        "Choose how to continue",
        ["Login", "Register"],
        horizontal=True,
        key="auth_menu"
    )

    if menu == "Register":
        st.header("Create your account")
        st.caption("Join RecycleX to arrange responsible e-waste collection.")

        with st.form("register_form"):
            name = st.text_input("Full Name")
            phone = st.text_input("Mobile Number")
            email = st.text_input("Email Address")
            password = st.text_input("Create Password", type="password")
            submit = st.form_submit_button("Create Account")

            if submit:
                if not all([name.strip(), phone.strip(), email.strip(), password]):
                    st.error("Please complete all fields.")
                elif len(password) < 8:
                    st.error("Password must be at least 8 characters.")
                else:
                    try:
                        supabase.auth.sign_up({
                            "email": email.strip(),
                            "password": password,
                            "options": {
                                "data": {
                                    "full_name": name.strip(),
                                    "phone": phone.strip()
                                }
                            }
                        })
                        st.success(
                            "Registration submitted. Confirm your email if requested, then log in."
                        )
                    except Exception:
                        st.error("Registration failed. Please check your details and try again.")

    else:
        st.header("Welcome back")
        st.caption("Log in to book a pickup or view your requests.")

        with st.form("login_form"):
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                try:
                    response = supabase.auth.sign_in_with_password({
                        "email": email.strip(),
                        "password": password
                    })

                    session = response.session
                    user = response.user

                    st.session_state["access_token"] = session.access_token
                    st.session_state["refresh_token"] = session.refresh_token
                    st.session_state["customer_id"] = str(user.id)

                    metadata = user.user_metadata or {}
                    st.session_state["customer_name"] = metadata.get("full_name", "")
                    st.session_state["customer_phone"] = metadata.get("phone", "")

                    st.rerun()
                except Exception:
                    st.error("Login failed. Please check your email and password.")

# ---------------------------------
# CUSTOMER DASHBOARD
# ---------------------------------
else:
    customer_id = st.session_state["customer_id"]
    customer_name = st.session_state.get("customer_name") or "Customer"

    st.success(f"Welcome, {customer_name}")
    st.info("📍 Currently serving: Kolkata")

    page = st.radio(
        "Your RecycleX dashboard",
        ["Book a Pickup", "My Bookings"],
        horizontal=True,
        key="customer_menu"
    )

    if page == "Book a Pickup":
        st.header("Schedule a pickup")
        st.caption("Tell us what you want collected and where we should come.")

        with st.form("pickup_booking_form"):
            name = st.text_input(
                "Full Name",
                value=st.session_state.get("customer_name", "")
            )
            phone = st.text_input(
                "Mobile Number",
                value=st.session_state.get("customer_phone", "")
            )
            address = st.text_area("Complete Pickup Address")

            st.subheader("Pickup GPS Location")
            location = streamlit_geolocation()

            latitude = None
            longitude = None

            if location and location.get("latitude") is not None:
                latitude = location["latitude"]
                longitude = location["longitude"]
                st.success("GPS location detected successfully!")
                st.write("Latitude:", latitude)
                st.write("Longitude:", longitude)
                map_data = pd.DataFrame({
                    "latitude": [latitude],
                    "longitude": [longitude]
                })
                st.map(map_data)
            else:
                st.info(
                    "Allow location access in your browser to detect your pickup location. "
                    "You can still enter your address manually."
                )

            st.text_input("Service City", value="Kolkata", disabled=True)

            category = st.selectbox(
                "E-Waste Category",
                [
                    "Computers", "Laptops", "Mobile Phones", "Batteries",
                    "Cables", "Circuit Boards", "Printers", "Other"
                ]
            )
            weight = st.number_input(
                "Estimated Weight (kg)",
                min_value=0.0,
                value=1.0,
                step=0.5
            )
            pickup_date = st.date_input(
                "Preferred Pickup Date",
                min_value=date.today()
            )
            pickup_time = st.selectbox(
                "Preferred Pickup Time",
                ["Morning", "Afternoon", "Evening"]
            )
            notes = st.text_area("Additional Information (Optional)")

            submit = st.form_submit_button("Submit Pickup Request")

            if submit:
                if not name.strip() or not phone.strip() or not address.strip():
                    st.error("Please enter your name, mobile number and complete pickup address.")
                else:
                    try:
                        supabase.table("customer_bookings").insert({
                            "customer_user_id": customer_id,
                            "customer_name": name.strip(),
                            "customer_phone": phone.strip(),
                            "pickup_address": address.strip(),
                            "city": "Kolkata",
                            "latitude": latitude,
                            "longitude": longitude,
                            "e_waste_category": category,
                            "estimated_weight": weight,
                            "preferred_pickup_date": pickup_date.isoformat(),
                            "preferred_pickup_time": pickup_time,
                            "customer_notes": notes.strip()
                        }).execute()

                        st.session_state["customer_name"] = name.strip()
                        st.session_state["customer_phone"] = phone.strip()
                        st.success("Your pickup request has been submitted!")
                    except Exception:
                        st.error("Unable to submit pickup request. Please try again or contact support.")

    elif page == "My Bookings":
        st.header("My pickup requests")
        st.caption("View the latest requests submitted from your account.")

        try:
            response = supabase.table("customer_bookings").select(
                "id, e_waste_category, estimated_weight, "
                "preferred_pickup_date, preferred_pickup_time, "
                "booking_status, created_at"
            ).eq(
                "customer_user_id", customer_id
            ).order(
                "created_at", desc=True
            ).execute()

            if response.data:
                bookings_df = pd.DataFrame(response.data)
                st.dataframe(bookings_df, use_container_width=True, hide_index=True)
            else:
                st.info("You have not submitted any pickup requests yet.")
        except Exception:
            st.error("Unable to load your bookings. Please try again.")

    st.divider()
    if st.button("Logout"):
        for key in [
            "access_token", "refresh_token", "customer_id",
            "customer_name", "customer_phone"
        ]:
            st.session_state.pop(key, None)
        st.rerun()

st.markdown(
    '<div class="rx-footer">RecycleX · Powered by Lokesh Seth E Waster Manager</div>',
    unsafe_allow_html=True
)
