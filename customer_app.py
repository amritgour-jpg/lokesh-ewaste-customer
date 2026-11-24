from streamlit_geolocation import streamlit_geolocation
import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import date

st.set_page_config(
    page_title="Lokesh Seth E Waster Manager",
    page_icon="♻️",
    layout="centered"
)

# Create a separate Supabase client for this browser session.
# Do not share an authenticated client between customers.
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

st.title("♻️ Lokesh Seth E Waster Manager")
st.subheader("E-Waste Collection Service")

# ---------------------------------
# LOGIN AND REGISTRATION
# ---------------------------------

if not st.session_state.get("access_token"):

    menu = st.radio(
        "Choose an option",
        ["Login", "Register"],
        horizontal=True
    )

    if menu == "Register":

        st.header("Create Customer Account")

        with st.form("register_form"):
            name = st.text_input("Full Name")
            phone = st.text_input("Mobile Number")
            email = st.text_input("Email Address")
            password = st.text_input(
                "Create Password",
                type="password"
            )

            submit = st.form_submit_button("Register")

            if submit:
                if not all([name, phone, email, password]):
                    st.error("Please complete all fields.")

                elif len(password) < 8:
                    st.error("Password must be at least 8 characters.")

                else:
                    try:
                        response = supabase.auth.sign_up({
                            "email": email,
                            "password": password,
                            "options": {
                                "data": {
                                    "full_name": name,
                                    "phone": phone
                                }
                            }
                        })

                        st.success(
                            "Registration submitted. "
                            "Confirm your email if requested, "
                            "then log in."
                        )

                    except Exception as e:
                        st.error("Registration failed.")
                        st.code(str(e))

    else:

        st.header("Customer Login")

        with st.form("login_form"):
            email = st.text_input("Email Address")
            password = st.text_input(
                "Password",
                type="password"
            )

            submit = st.form_submit_button("Login")

            if submit:
                try:
                    response = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })

                    session = response.session
                    user = response.user

                    st.session_state["access_token"] = session.access_token
                    st.session_state["refresh_token"] = session.refresh_token
                    st.session_state["customer_id"] = str(user.id)

                    metadata = user.user_metadata or {}

                    st.session_state["customer_name"] = metadata.get(
                        "full_name", ""
                    )
                    st.session_state["customer_phone"] = metadata.get(
                        "phone", ""
                    )

                    st.rerun()

                except Exception as e:
                    st.error("Login failed.")
                    st.code(str(e))

# ---------------------------------
# CUSTOMER DASHBOARD
# ---------------------------------

else:

    customer_id = st.session_state["customer_id"]

    st.success(
        "Welcome, " +
        (st.session_state.get("customer_name") or "Customer")
    )

    st.info("Proposed service city: Kolkata")

    page = st.radio(
        "Customer Menu",
        ["Book a Pickup", "My Bookings"],
        horizontal=True
    )

    # ---------------------------------

    # ---------------------------------
    # BOOK A PICKUP
    # ---------------------------------

    if page == "Book a Pickup":

        st.header("Request E-Waste Pickup")

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
                    "Allow location access in your browser "
                    "to detect your pickup location."
                )

            city = st.text_input(
                "Service City",
                value="Kolkata",
                disabled=True
            )

            category = st.selectbox(
                "E-Waste Category",
                [
                    "Computers",
                    "Laptops",
                    "Mobile Phones",
                    "Batteries",
                    "Cables",
                    "Circuit Boards",
                    "Printers",
                    "Other"
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
                [
                    "Morning",
                    "Afternoon",
                    "Evening"
                ]
            )

            notes = st.text_area(
                "Additional Information (Optional)"
            )

            submit = st.form_submit_button("Submit Pickup Request")

            if submit:

                if not name.strip() or not phone.strip() or not address.strip():
                    st.error(
                        "Please enter your name, mobile number "
                        "and complete pickup address."
                    )

                else:
                    try:
                        result = supabase.table(
                            "customer_bookings"
                        ).insert({
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

                        st.success(
                            "Your pickup request has been submitted!"
                        )

                    except Exception as e:
                        st.error("Unable to submit pickup request.")
                        st.code(str(e))

    # ---------------------------------
    # MY BOOKINGS
    # ---------------------------------

    elif page == "My Bookings":

        st.header("My Pickup Requests")

        try:
            response = supabase.table(
                "customer_bookings"
            ).select(
                "id, e_waste_category, estimated_weight, "
                "preferred_pickup_date, preferred_pickup_time, "
                "booking_status, created_at"
            ).eq(
                "customer_user_id", customer_id
            ).order(
                "created_at", desc=True
            ).execute()

            if response.data:
                st.dataframe(
                    pd.DataFrame(response.data),
                    use_container_width=True
                )
            else:
                st.info("You have not submitted any pickup requests yet.")

        except Exception as e:
            st.error("Unable to load your bookings.")
            st.code(str(e))

    st.divider()

    if st.button("Logout"):
        for key in [
            "access_token",
            "refresh_token",
            "customer_id",
            "customer_name",
            "customer_phone"
        ]:
            st.session_state.pop(key, None)

        st.rerun()

st.caption("Lokesh Seth E Waster Manager")
