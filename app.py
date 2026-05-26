import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# ── Page config ──────────────────────────────────────────
st.set_page_config(page_title="Insurance Claims Dashboard", page_icon="📊", layout="wide")

# ── Styling ───────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    .title { font-size: 2rem; font-weight: 700; color: #1F4E79; }
    .subtitle { font-size: 1rem; color: #555; margin-bottom: 1.5rem; }
    .metric-box { background: white; border-radius: 12px; padding: 1.2rem;
                  border: 1px solid #e2e8f0; text-align: center; }
    .metric-val { font-size: 2rem; font-weight: 700; color: #1F4E79; }
    .metric-label { font-size: 0.85rem; color: #777; margin-top: 4px; }
    .footer { font-size: 0.75rem; color: #aaa; text-align: center; margin-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────
st.markdown('<div class="title">📊 Insurance Claims Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">UK Insurance Submission & Clearance — Process Monitoring System</div>', unsafe_allow_html=True)

# ── Session state for claims ──────────────────────────────
if "claims" not in st.session_state:
    sample_claims = [
        {"Claim ID": "CLM-001", "Client Name": "James Wilson",    "Type": "Motor",    "Amount (£)": 3200, "Submitted": "2024-11-01", "Status": "Approved",   "Processing Days": 3, "Quality Score": 99},
        {"Claim ID": "CLM-002", "Client Name": "Sarah Thompson",  "Type": "Property", "Amount (£)": 8500, "Submitted": "2024-11-05", "Status": "Pending",    "Processing Days": 7, "Quality Score": 97},
        {"Claim ID": "CLM-003", "Client Name": "Mohammed Al Sayed","Type": "Health",  "Amount (£)": 1200, "Submitted": "2024-11-08", "Status": "Approved",   "Processing Days": 2, "Quality Score": 100},
        {"Claim ID": "CLM-004", "Client Name": "Emily Clarke",    "Type": "Travel",   "Amount (£)": 650,  "Submitted": "2024-11-10", "Status": "Rejected",   "Processing Days": 4, "Quality Score": 98},
        {"Claim ID": "CLM-005", "Client Name": "Robert Davies",   "Type": "Motor",    "Amount (£)": 5100, "Submitted": "2024-11-12", "Status": "Pending",    "Processing Days": 5, "Quality Score": 96},
        {"Claim ID": "CLM-006", "Client Name": "Priya Sharma",    "Type": "Property", "Amount (£)": 12000,"Submitted": "2024-11-15", "Status": "Approved",   "Processing Days": 3, "Quality Score": 99},
        {"Claim ID": "CLM-007", "Client Name": "David Brown",     "Type": "Health",   "Amount (£)": 900,  "Submitted": "2024-11-18", "Status": "Approved",   "Processing Days": 2, "Quality Score": 100},
        {"Claim ID": "CLM-008", "Client Name": "Anna Foster",     "Type": "Travel",   "Amount (£)": 430,  "Submitted": "2024-11-20", "Status": "Pending",    "Processing Days": 6, "Quality Score": 95},
    ]
    st.session_state.claims = sample_claims

df = pd.DataFrame(st.session_state.claims)

# ── KPI Metrics ───────────────────────────────────────────
st.subheader("📈 Key Performance Metrics")
col1, col2, col3, col4 = st.columns(4)

total        = len(df)
approved     = len(df[df["Status"] == "Approved"])
pending      = len(df[df["Status"] == "Pending"])
rejected     = len(df[df["Status"] == "Rejected"])
avg_quality  = round(df["Quality Score"].mean(), 1)
avg_days     = round(df["Processing Days"].mean(), 1)
total_amount = df["Amount (£)"].sum()

with col1:
    st.markdown(f'<div class="metric-box"><div class="metric-val">{total}</div><div class="metric-label">Total Claims</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-box"><div class="metric-val" style="color:#0F6E56">{avg_quality}%</div><div class="metric-label">Avg Quality Score</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-box"><div class="metric-val" style="color:#854F0B">{avg_days} days</div><div class="metric-label">Avg Processing Time</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-box"><div class="metric-val">£{total_amount:,}</div><div class="metric-label">Total Claims Value</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ── Status breakdown ──────────────────────────────────────
st.subheader("📋 Claims Status Overview")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="metric-box"><div class="metric-val" style="color:#0F6E56">{approved}</div><div class="metric-label">✅ Approved</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-box"><div class="metric-val" style="color:#854F0B">{pending}</div><div class="metric-label">⏳ Pending</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-box"><div class="metric-val" style="color:#9B1C1C">{rejected}</div><div class="metric-label">❌ Rejected</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ── Filters ───────────────────────────────────────────────
st.subheader("🔍 Filter Claims")
col1, col2 = st.columns(2)
with col1:
    status_filter = st.selectbox("Filter by Status", ["All", "Approved", "Pending", "Rejected"])
with col2:
    type_filter = st.selectbox("Filter by Type", ["All", "Motor", "Property", "Health", "Travel"])

filtered_df = df.copy()
if status_filter != "All":
    filtered_df = filtered_df[filtered_df["Status"] == status_filter]
if type_filter != "All":
    filtered_df = filtered_df[filtered_df["Type"] == type_filter]

st.dataframe(filtered_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ── Add new claim ─────────────────────────────────────────
st.subheader("➕ Submit New Claim")
col1, col2, col3 = st.columns(3)
with col1:
    client_name = st.text_input("Client Name")
    claim_type  = st.selectbox("Claim Type", ["Motor", "Property", "Health", "Travel"])
with col2:
    amount      = st.number_input("Claim Amount (£)", min_value=0, step=100)
    status      = st.selectbox("Status", ["Pending", "Approved", "Rejected"])
with col3:
    proc_days   = st.number_input("Processing Days", min_value=1, max_value=30, value=3)
    quality     = st.slider("Quality Score (%)", min_value=80, max_value=100, value=98)

if st.button("📥 Submit Claim", use_container_width=True):
    if client_name:
        new_id = f"CLM-{str(len(st.session_state.claims) + 1).zfill(3)}"
        st.session_state.claims.append({
            "Claim ID": new_id,
            "Client Name": client_name,
            "Type": claim_type,
            "Amount (£)": amount,
            "Submitted": datetime.today().strftime("%Y-%m-%d"),
            "Status": status,
            "Processing Days": proc_days,
            "Quality Score": quality,
        })
        st.success(f"✅ Claim {new_id} submitted successfully!")
        st.rerun()
    else:
        st.warning("Please enter a client name.")

# ── Footer ────────────────────────────────────────────────
st.markdown('<div class="footer">Built by Reethu Abraham | Insurance Operations Specialist | Infosys BPM<br>Inspired by real-world UK Insurance Submission & Clearance experience</div>', unsafe_allow_html=True)
