import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import requests
import streamlit.components.v1 as components

st.set_page_config(page_title="Dashboard Produksi - CV Sinergi Adv Nusantara", layout="wide", initial_sidebar_state="expanded")

APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzugy_zS4cBvcpsIwvR_bpVotfpIkdt6qywY6EXv8HEG5R-iDtPics3gGhlNbltB3Rp/exec"

# ==============================================================================
# SVG ICONS
# ==============================================================================
ICON_FACTORY = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="15" rx="2"/><path d="M17 7V5a2 2 0 0 0-2-2H9a2 2 0 0 0-2 2v2"/><line x1="12" y1="12" x2="12" y2="17"/><line x1="9.5" y1="14.5" x2="14.5" y2="14.5"/></svg>'
ICON_DASHBOARD = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>'
ICON_CHECK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'
ICON_X = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>'
ICON_LIST = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>'
ICON_LOGOUT = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>'
ICON_CAMERA = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>'
ICON_KEYBOARD = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="2"/><line x1="6" y1="10" x2="6" y2="10"/><line x1="10" y1="10" x2="10" y2="10"/><line x1="14" y1="10" x2="14" y2="10"/><line x1="18" y1="10" x2="18" y2="10"/><line x1="6" y1="14" x2="18" y2="14"/></svg>'
ICON_CHART = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/><line x1="2" y1="20" x2="22" y2="20"/></svg>'
ICON_PIE = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>'
ICON_GEAR = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/><path d="M4.93 4.93a10 10 0 0 0 0 14.14"/></svg>'
ICON_USER = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
ICON_WARN = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'

def set_background(image_file, is_login):
    try:
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()

        if is_login:
            css = f"""
            <style>
            .stApp {{
                background-image: url(data:image/jpeg;base64,{encoded_string}) !important;
                background-size: cover !important;
                background-position: center !important;
                background-attachment: fixed !important;
            }}
            [data-testid="collapsedControl"] {{ display: none !important; }}
            [data-testid="stSidebar"] {{ display: none !important; }}
            [data-testid="stHeader"] {{ display: none !important; }}
            [data-testid="stForm"] {{
                background: linear-gradient(135deg, rgba(20,24,40,0.97) 0%, rgba(30,35,60,0.97) 100%) !important;
                border-radius: 20px !important;
                padding: 48px 44px !important;
                border: 1px solid rgba(92,103,242,0.5) !important;
                box-shadow: 0 24px 60px rgba(0,0,0,0.7) !important;
                margin-top: 50px;
            }}
            [data-testid="stForm"] label,
            [data-testid="stForm"] label p,
            [data-testid="stForm"] .stSelectbox label p {{
                color: #e2e8f0 !important;
                font-size: 13px !important;
                font-weight: 500 !important;
            }}
            [data-testid="stForm"] .stTextInput > div,
            [data-testid="stForm"] .stTextInput > div > div {{
                background-color: rgba(255,255,255,0.09) !important;
                border: 1px solid rgba(92,103,242,0.45) !important;
                border-radius: 10px !important;
            }}
            [data-testid="stForm"] .stTextInput input {{
                background-color: transparent !important;
                border: none !important;
                box-shadow: none !important;
                color: #ffffff !important;
                caret-color: #ffffff !important;
                font-size: 14px !important;
                padding: 10px 14px !important;
            }}
            [data-testid="stForm"] .stTextInput input::placeholder {{
                color: rgba(255,255,255,0.35) !important;
            }}
            [data-testid="stForm"] .stTextInput input:focus {{
                border-color: #5c67f2 !important;
                box-shadow: 0 0 0 3px rgba(92,103,242,0.25) !important;
                outline: none !important;
            }}
            [data-testid="stForm"] .stSelectbox > div > div {{
                background-color: rgba(255,255,255,0.09) !important;
                border: 1px solid rgba(92,103,242,0.45) !important;
                border-radius: 10px !important;
                color: #ffffff !important;
            }}
            [data-testid="stForm"] .stSelectbox svg {{
                fill: rgba(255,255,255,0.6) !important;
            }}
            [data-testid="stForm"] .stFormSubmitButton button {{
                background: linear-gradient(135deg, #5c67f2 0%, #4551d9 100%) !important;
                border: none !important;
                border-radius: 10px !important;
                color: white !important;
                font-weight: 600 !important;
                letter-spacing: 0.04em !important;
                padding: 12px 24px !important;
                width: 100% !important;
                margin-top: 8px !important;
                transition: opacity 0.2s !important;
            }}
            [data-testid="stForm"] .stFormSubmitButton button:hover {{
                opacity: 0.88 !important;
            }}
            </style>
            """
        else:
            css = """
            <style>
            .stApp {
                background-image: none !important;
                background: linear-gradient(160deg, #eef1f8 0%, #e7eaf6 45%, #eef1f8 100%) !important;
            }
            [data-testid="stHeader"] { display: block !important; background-color: transparent !important; }
            </style>
            """
        st.markdown(css, unsafe_allow_html=True)
    except:
        pass

# ==============================================================================
# GLOBAL STYLES
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        -webkit-font-smoothing: antialiased;
    }

    /* App background */
    .stApp {
        background: linear-gradient(160deg, #eef1f8 0%, #e7eaf6 45%, #eef1f8 100%) !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #c7cce6; border-radius: 8px; }
    ::-webkit-scrollbar-thumb:hover { background: #aab0d8; }

    /* Card wrapper used to group charts/sections like a real dashboard panel */
    .dash-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 18px 20px 8px;
        border: 1px solid #eceffa;
        box-shadow: 0 4px 18px rgba(31, 41, 90, 0.05);
        margin-bottom: 18px;
    }
    .dash-card-tight { padding-bottom: 18px; }

    /* Metric Cards */
    .metric-card {
        padding: 20px 22px;
        border-radius: 16px;
        text-align: left;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 24px -8px rgba(31, 41, 90, 0.35);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 30px -8px rgba(31, 41, 90, 0.42);
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: -30px; right: -30px;
        width: 110px; height: 110px;
        border-radius: 50%;
        background: rgba(255,255,255,0.10);
    }
    .metric-card::after {
        content: '';
        position: absolute;
        bottom: -40px; right: 10px;
        width: 90px; height: 90px;
        border-radius: 50%;
        background: rgba(255,255,255,0.06);
    }
    .metric-card .metric-row { display:flex; align-items:flex-start; justify-content:space-between; position:relative; z-index:1; }
    .metric-card .metric-icon {
        width: 38px; height: 38px;
        border-radius: 11px;
        background: rgba(255,255,255,0.18);
        display:flex; align-items:center; justify-content:center;
        color: white;
        flex-shrink: 0;
    }
    .metric-card p { margin: 14px 0 4px; font-size: 11.5px; font-weight: 600; letter-spacing: 0.07em; text-transform: uppercase; opacity: 0.88; color: white; position:relative; z-index:1; }
    .metric-card h2 { margin: 0; font-size: 32px; font-weight: 800; color: white; line-height: 1.1; position:relative; z-index:1; letter-spacing: -0.01em; }
    .metric-blue  { background: linear-gradient(135deg, #5b6af0 0%, #3a48d0 100%); }
    .metric-green { background: linear-gradient(135deg, #16c98c 0%, #089968 100%); }
    .metric-red   { background: linear-gradient(135deg, #f0585f 0%, #c93030 100%); }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #181c2c 0%, #232842 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.06) !important;
    }
    [data-testid="stSidebar"] * { color: #e2e6f0 !important; }
    [data-testid="stSidebar"] .stButton button {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
        color: #aab1cc !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        transition: all 0.18s ease !important;
        text-align: left !important;
        padding: 9px 14px !important;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background: rgba(92,103,242,0.22) !important;
        border-color: rgba(92,103,242,0.5) !important;
        color: #ffffff !important;
        transform: translateX(3px) !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.08) !important;
        margin: 12px 0 !important;
    }

    /* Main area */
    .main .block-container {
        padding-top: 1.6rem !important;
        padding-bottom: 2.4rem !important;
        max-width: 1400px;
    }

    /* Page header */
    .page-header {
        display: flex;
        align-items: center;
        gap: 14px;
        background: linear-gradient(135deg, #ffffff 0%, #f7f8fd 100%);
        border-radius: 14px;
        border: 1px solid #eceffa;
        border-left: 4px solid #5c67f2;
        padding: 16px 20px;
        margin-bottom: 18px;
        box-shadow: 0 4px 16px rgba(31, 41, 90, 0.04);
    }
    .page-header .icon-badge {
        width: 42px; height: 42px;
        min-width: 42px;
        border-radius: 12px;
        background: linear-gradient(135deg, #5c67f2, #4551d9);
        color: white;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 6px 14px -4px rgba(92,103,242,0.55);
    }
    .page-header h2 {
        color: #1a1e2d;
        margin: 0;
        font-size: 21px;
        font-weight: 700;
        letter-spacing: -0.01em;
    }
    .page-header p { color: #6b7280; margin: 3px 0 0; font-size: 12.5px; }

    /* Section label */
    .section-label {
        display: flex;
        align-items: center;
        gap: 7px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        color: #6b7280;
        margin: 0 0 12px;
    }
    .section-label svg { color: #5c67f2; }

    /* Action buttons */
    .stButton button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        transition: all 0.18s ease !important;
    }
    .main .stButton button:not([kind="secondary"]):hover {
        transform: translateY(-1px);
        filter: brightness(0.97);
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid #e8eaf2 !important;
    }

    /* Chart header */
    .chart-header {
        display: flex;
        align-items: center;
        gap: 7px;
        font-size: 13px;
        font-weight: 700;
        color: #1f2433;
        margin: 0 0 10px;
    }
    .chart-header svg { color: #5c67f2; }

    /* Analytics title */
    .analytics-title {
        display: flex;
        align-items: center;
        gap: 9px;
        font-size: 16px;
        font-weight: 800;
        color: #1a1e2d;
        margin: 6px 0 16px;
        letter-spacing: -0.01em;
    }
    .analytics-title svg { color: #5c67f2; }
    .analytics-title::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, #e2e5f5, transparent);
        margin-left: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATA DARI SPREADSHEET (REAL-TIME)
# ==============================================================================
@st.cache_data(ttl=2)
def tarik_data_spreadsheet():
    columns_default = ["Waktu", "Operator", "Departemen", "Barcode ID", "Status"]
    try:
        response = requests.get(APPS_SCRIPT_URL, timeout=10)
        if response.status_code == 200:
            res_json = response.json()
            if "data" in res_json:
                if len(res_json["data"]) > 0:
                    df = pd.DataFrame(res_json["data"])
                    df.columns = [str(c).strip() for c in df.columns]
                    return df
                else:
                    return pd.DataFrame(columns=columns_default)
            else:
                st.error(f"Pesan dari API: {res_json.get('message')}")
        else:
            st.error(f"Gagal Terhubung Kode HTTP: {response.status_code}")
    except Exception as e:
        st.error(f"Koneksi gagal. Error: {e}")

    st.warning("Menampilkan data cadangan karena gagal memuat data dari Spreadsheet. Pastikan Baris 1 di Spreadsheet berisi header: Waktu, Operator, Departemen, Barcode ID, Status.")
    return pd.DataFrame({
        "Waktu": ["13 Feb, 18:00", "13 Feb, 18:05", "13 Feb, 18:10"],
        "Operator": ["Dummy 1", "Dummy 2", "Dummy 3"],
        "Departemen": ["Sablon", "Jahit", "Cutting"],
        "Barcode ID": ["0001", "0002", "0003"],
        "Status": ["Selesai", "Reject", "Proses"]
    })

# ==============================================================================
# HELPER: TABEL DENGAN BADGE STATUS
# ==============================================================================
BADGE_COLORS = {
    "Proses":  {"bg": "#eef2ff", "text": "#3b56f5", "dot": "#5c67f2"},
    "Selesai": {"bg": "#ecfdf5", "text": "#0a8a5f", "dot": "#10b981"},
    "Reject":  {"bg": "#fef2f2", "text": "#dc2626", "dot": "#ef4444"},
}

def render_table(df):
    if df.empty:
        st.markdown("""
            <div style='text-align:center; padding:48px 20px; background:#ffffff; border-radius:16px; border:1px solid #eceffa;'>
                <p style='color:#94a3b8; font-size:13px; margin:0;'>Tidak ada data untuk ditampilkan.</p>
            </div>
        """, unsafe_allow_html=True)
        return
    html = """
    <div style='background:#ffffff; border-radius:16px; border:1px solid #eceffa; box-shadow:0 4px 18px rgba(31,41,90,0.05); overflow:hidden;'>
    <table style='width:100%; border-collapse:collapse; font-size:13px;'>
    """
    html += "<tr style='background:linear-gradient(135deg,#f8f9fd,#f1f3fb);'>"
    for col in df.columns:
        html += f"<th style='padding:13px 16px; text-align:left; font-weight:700; color:#5b6178; text-transform:uppercase; font-size:10.5px; letter-spacing:0.06em; border-bottom:1px solid #eceffa;'>{col}</th>"
    html += "</tr>"
    for i, (_, row) in enumerate(df.iterrows()):
        row_bg = "#fbfbfe" if i % 2 == 1 else "#ffffff"
        html += f"<tr style='background:{row_bg}; transition:background 0.15s;' onmouseover=\"this.style.background='#f0f1fb'\" onmouseout=\"this.style.background='{row_bg}'\">"
        for col in df.columns:
            val = str(row[col])
            if col == "Status":
                colors = BADGE_COLORS.get(val, {"bg": "#f1f5f9", "text": "#475569", "dot": "#94a3b8"})
                val = f"<span style='display:inline-flex; align-items:center; gap:6px; padding:4px 13px; border-radius:20px; font-size:11px; font-weight:700; background:{colors['bg']}; color:{colors['text']};'><span style='width:6px; height:6px; border-radius:50%; background:{colors['dot']}; display:inline-block;'></span>{val}</span>"
            html += f"<td style='padding:11px 16px; color:#1e293b; border-bottom:1px solid #f4f5fa;'>{val}</td>"
        html += "</tr>"
    html += "</table></div>"
    st.markdown(html, unsafe_allow_html=True)

# ==============================================================================
# CEK LOGIN SESSION
# ==============================================================================
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'page' not in st.session_state:
    st.session_state['page'] = 'Dashboard WIP'
if 'barcode_input' not in st.session_state:
    st.session_state['barcode_input'] = ''

# ==============================================================================
# HALAMAN LOGIN
# ==============================================================================
if not st.session_state['logged_in']:
    set_background('background.jpg', is_login=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.form("login_form"):
            st.markdown(f"""
                <div style='text-align:center; margin-bottom:24px;'>
                    <div style='display:inline-flex; align-items:center; justify-content:center;
                                width:52px; height:52px; background:rgba(92,103,242,0.2);
                                border-radius:14px; margin-bottom:12px; color:#a5b0ff;'>
                        {ICON_FACTORY}
                    </div>
                    <h2 style='color:#ffffff; font-size:20px; font-weight:700; margin:0 0 4px; letter-spacing:0.01em;'>Login Operator</h2>
                    <p style='color:rgba(255,255,255,0.4); font-size:12px; margin:0; letter-spacing:0.06em; text-transform:uppercase;'>CV Sinergi Adv Nusantara</p>
                </div>
            """, unsafe_allow_html=True)
            operator_name = st.text_input("Nama Operator", placeholder="Masukkan nama Anda")
            departemen = st.selectbox("Departemen", ["Jahit", "Sablon", "Cutting", "Packing", "Finishing"])
            submitted = st.form_submit_button("Masuk", use_container_width=True)
            if submitted:
                if operator_name:
                    st.session_state['logged_in'] = True
                    st.session_state['operator'] = operator_name
                    st.session_state['departemen'] = departemen
                    st.rerun()
                else:
                    st.warning("Masukkan nama operator terlebih dahulu!")

# ==============================================================================
# HALAMAN UTAMA (SETELAH LOGIN)
# ==============================================================================
else:
    set_background('background.jpg', is_login=False)

    df_master = tarik_data_spreadsheet()

    # SIDEBAR
    current_page = st.session_state['page']
    operator_name_sb = st.session_state['operator']
    departemen_sb    = st.session_state['departemen']
    initials = ''.join([w[0].upper() for w in operator_name_sb.split()[:2]])

    with st.sidebar:
        # CSS sidebar
        st.markdown("""
            <style>
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #1a1e2d 0%, #20263a 100%) !important;
                border-right: 1px solid rgba(255,255,255,0.06) !important;
            }
            [data-testid="stSidebar"] > div:first-child {
                padding-top: 1.4rem !important;
            }
            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] span {
                color: #e2e6f0 !important;
            }
            [data-testid="stSidebar"] hr {
                border-color: rgba(255,255,255,0.08) !important;
                margin: 12px 0 !important;
            }
            [data-testid="stSidebar"] .stButton > button {
                width: 100% !important;
                text-align: left !important;
                background: transparent !important;
                border: 1px solid transparent !important;
                border-radius: 10px !important;
                color: rgba(255,255,255,0.55) !important;
                font-size: 13px !important;
                font-weight: 500 !important;
                padding: 9px 14px !important;
                margin-bottom: 2px !important;
                transition: background 0.15s, border-color 0.15s, color 0.15s !important;
            }
            [data-testid="stSidebar"] .stButton > button:hover {
                background: rgba(255,255,255,0.07) !important;
                border-color: rgba(255,255,255,0.12) !important;
                color: #ffffff !important;
            }
            [data-testid="stSidebar"] .stButton > button:focus:not(:active) {
                background: rgba(92,103,242,0.25) !important;
                border-color: rgba(92,103,242,0.5) !important;
                color: #ffffff !important;
                box-shadow: none !important;
            }
            /* Logout button */
            [data-testid="stSidebar"] .stButton:last-of-type > button {
                color: rgba(255,255,255,0.35) !important;
                border-color: rgba(255,255,255,0.07) !important;
                margin-top: 2px !important;
            }
            [data-testid="stSidebar"] .stButton:last-of-type > button:hover {
                background: rgba(232,70,70,0.14) !important;
                border-color: rgba(232,70,70,0.38) !important;
                color: #f87171 !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # Brand
        st.markdown(f"""
            <div style="padding:0 4px 14px; border-bottom:1px solid rgba(255,255,255,0.07); margin-bottom:14px;">
                <p style="font-size:15px; font-weight:700; color:#ffffff !important; margin:0; letter-spacing:0.01em;">CV SINERGI ADV</p>
                <p style="font-size:10px; color:rgba(255,255,255,0.35) !important; letter-spacing:0.1em; text-transform:uppercase; margin:2px 0 0;">Nusantara</p>
            </div>
        """, unsafe_allow_html=True)

        # User card
        st.markdown(f"""
            <div style="background:linear-gradient(135deg, rgba(92,103,242,0.16), rgba(92,103,242,0.06)); border:1px solid rgba(92,103,242,0.28); border-radius:14px; padding:14px 14px; margin-bottom:18px; display:flex; align-items:center; gap:12px;">
                <div style="position:relative; width:40px; height:40px; min-width:40px;">
                    <div style="width:40px; height:40px; background:linear-gradient(135deg,#5c67f2,#4551d9); border-radius:11px; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; color:#fff; box-shadow:0 4px 10px -2px rgba(92,103,242,0.6);">{initials}</div>
                    <div style="position:absolute; bottom:-2px; right:-2px; width:11px; height:11px; background:#16c98c; border-radius:50%; border:2px solid #1c2138;"></div>
                </div>
                <div>
                    <p style="font-size:10px; color:rgba(255,255,255,0.38) !important; text-transform:uppercase; letter-spacing:0.07em; margin:0;">Operator aktif</p>
                    <p style="font-size:13px; font-weight:700; color:#ffffff !important; margin:2px 0 3px;">{operator_name_sb}</p>
                    <span style="font-size:10px; font-weight:600; color:#a5b0ff !important; background:rgba(92,103,242,0.22); padding:2px 9px; border-radius:20px; display:inline-block;">{departemen_sb}</span>
                </div>
            </div>
            <p style="font-size:10px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:rgba(255,255,255,0.28) !important; margin:0 0 8px 4px;">Navigasi</p>
        """, unsafe_allow_html=True)

        # Nav buttons — active page ditandai dengan CSS injection per-button
        nav_items = [
            ("Dashboard WIP",            "dashboard"),
            ("Data Selesai",             "selesai"),
            ("Data Reject",              "reject"),
            ("Rekapitulasi Data Harian", "rekap"),
        ]

        for label, key in nav_items:
            is_active = current_page == label
            if is_active:
                st.markdown(f"""
                    <style>
                    [data-testid="stSidebar"] [data-testid="stButton-nav_{key}"] > button {{
                        background: rgba(92,103,242,0.25) !important;
                        border-color: rgba(92,103,242,0.5) !important;
                        color: #ffffff !important;
                    }}
                    </style>
                """, unsafe_allow_html=True)
            if st.button(label, use_container_width=True, key=f"nav_{key}"):
                st.session_state['page'] = label
                st.rerun()

        st.markdown("---")
        if st.button("Log Keluar", use_container_width=True, key="logout_btn"):
            st.session_state['logged_in'] = False
            st.rerun()

    # ==========================================================================
    # 1. DASHBOARD WIP
    # ==========================================================================
    if st.session_state['page'] == 'Dashboard WIP':
        st.markdown(f"""
            <div class="page-header">
                <div class="icon-badge">{ICON_DASHBOARD}</div>
                <div>
                    <h2>Dashboard WIP &amp; Scan Produksi</h2>
                    <p>CV Sinergi Adv Nusantara &nbsp;·&nbsp; Dept: <b>{st.session_state['departemen']}</b></p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:6px;'></div>", unsafe_allow_html=True)

        def simpan_ke_sheet(status_pilihan):
            barcode = st.session_state.get('barcode_input', '').strip()
            if barcode:
                with st.spinner(f'Mengirim status {status_pilihan}...'):
                    payload = {
                        "operator": st.session_state['operator'],
                        "departemen": st.session_state['departemen'],
                        "barcode_id": barcode,
                        "status": status_pilihan
                    }
                    try:
                        response = requests.post(APPS_SCRIPT_URL, json=payload, timeout=10)
                        result = response.json()
                        if result.get("status") == "success":
                            st.success(f"Berhasil menyimpan [{status_pilihan}] untuk ID {barcode}!")
                            st.cache_data.clear()
                            st.session_state['barcode_input'] = ''
                            st.rerun()
                        else:
                            st.error(f"Gagal menyimpan: {result.get('message')}")
                    except Exception as e:
                        st.error(f"Gagal mengirim data. Cek koneksi internet.")
            else:
                st.warning("Silakan isi ID Barang terlebih dahulu!")

        col_cam, col_manual = st.columns(2)

        with col_cam:
            st.markdown('<div class="dash-card dash-card-tight">', unsafe_allow_html=True)
            st.markdown(f'<p class="section-label">{ICON_CAMERA} Scan QR Produksi</p>', unsafe_allow_html=True)


            st.markdown("<p style='font-size:12px; color:#94a3b8; margin-top:-2px; margin-bottom:6px; text-align:center;'>Arahkan QR ke kamera — otomatis terdeteksi.</p>", unsafe_allow_html=True)

            operator = st.session_state['operator']
            departemen = st.session_state['departemen']

            scanner_html = f"""
            <div id="qr-reader" style="width:100%;max-width:420px;margin:0 auto;border-radius:12px;overflow:hidden;"></div>
            <div id="qr-status" style="text-align:center;margin-top:10px;font-size:14px;color:#555;"></div>
            <script src="https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.min.js"></script>
            <script>
            var scanLock = false;
            var actionLock = false;
            var op = '{operator}';
            var dep = '{departemen}';
            var api = '{APPS_SCRIPT_URL}';
            var base = window.location.href.split('?')[0];

            function showMsg(html, color) {{
                document.getElementById('qr-status').innerHTML = html;
                var r = document.getElementById('qr-reader');
                if (r) r.style.display = 'none';
            }}

            function sendToSheet(decodedText, status, mode, cb) {{
                if (actionLock) return;
                actionLock = true;
                var uid = Date.now() + '-' + Math.random().toString(36).slice(2, 6);
                fetch(api + '?_=' + uid, {{
                    method: 'POST',
                    mode: 'no-cors',
                    headers: {{ 'Content-Type': 'text/plain' }},
                    body: JSON.stringify({{ operator: op, departemen: dep, barcode_id: decodedText, status: status, mode: mode }})
                }}).then(function() {{ actionLock = false; if (cb) cb(); }}).catch(function() {{ actionLock = false; if (cb) cb(); }});
            }}

            function processQR(decodedText) {{
                if (scanLock) return;
                scanLock = true;
                try {{ html5QrcodeScanner.clear(); }} catch(e) {{}}

                fetch(api + '?_=' + Date.now())
                    .then(function(r) {{ return r.json(); }})
                    .then(function(j) {{
                        var lastStatus = '';
                        if (j.data) {{
                            for (var i = j.data.length - 1; i >= 0; i--) {{
                                if (String(j.data[i]['Barcode ID']).trim() === decodedText) {{
                                    lastStatus = String(j.data[i]['Status']).trim().toLowerCase();
                                    break;
                                }}
                            }}
                        }}
                        if (!lastStatus) {{
                            sendToSheet(decodedText, 'Proses', 'new', function() {{
                                showMsg('<span style="color:#059669;font-weight:600;">Barang baru tercatat sebagai <b>Proses</b></span><br><small style="color:#94a3b8;">Scan lagi untuk menambah</small>', '');
                                setTimeout(function() {{
                                    scanLock = false;
                                    var r = document.getElementById('qr-reader');
                                    if (r) r.style.display = 'block';
                                    try {{ html5QrcodeScanner.render(onScanSuccess, onScanError); }} catch(e) {{}}
                                }}, 2000);
                            }});
                        }} else if (lastStatus === 'selesai' || lastStatus === 'reject') {{
                            sendToSheet(decodedText, 'Proses', 'new', function() {{
                                showMsg('<span style="color:#059669;font-weight:600;">Siklus baru: <b>Proses</b></span><br><small style="color:#94a3b8;">Scan lagi untuk menambah</small>', '');
                                setTimeout(function() {{
                                    scanLock = false;
                                    var r = document.getElementById('qr-reader');
                                    if (r) r.style.display = 'block';
                                    try {{ html5QrcodeScanner.render(onScanSuccess, onScanError); }} catch(e) {{}}
                                }}, 2000);
                            }});
                        }} else {{
                            showMsg('<span style="font-weight:600;color:#92400e;">Barang sedang diproses. Pilih aksi:</span>', '');
                            var b = document.getElementById('qr-status');
                            b.innerHTML +=
                                '<div style="display:flex;gap:8px;justify-content:center;margin-top:12px;">' +
                                '<button id="btn-selesai" onclick="doAction(\\'' + decodedText + '\\',\\'Selesai\\')" style="background:#059669;color:white;border:none;border-radius:8px;padding:9px 24px;font-weight:600;cursor:pointer;font-size:14px;">Selesai</button>' +
                                '<button id="btn-reject" onclick="doAction(\\'' + decodedText + '\\',\\'Reject\\')" style="background:#dc2626;color:white;border:none;border-radius:8px;padding:9px 24px;font-weight:600;cursor:pointer;font-size:14px;">Reject</button>' +
                                '</div>';
                        }}
                    }});
            }}

            function doAction(decodedText, status) {{
                var btnS = document.getElementById('btn-selesai');
                var btnR = document.getElementById('btn-reject');
                if (btnS) {{ btnS.disabled = true; btnS.style.opacity = '0.5'; }}
                if (btnR) {{ btnR.disabled = true; btnR.style.opacity = '0.5'; }}
                sendToSheet(decodedText, status, 'update', function() {{
                    showMsg('<span style="color:#059669;font-weight:600;">Status <b>' + status + '</b> tersimpan</span><br><small style="color:#94a3b8;">Scan lagi untuk barcode lain</small>', '');
                    setTimeout(function() {{
                        scanLock = false;
                        var r = document.getElementById('qr-reader');
                        if (r) r.style.display = 'block';
                        try {{ html5QrcodeScanner.render(onScanSuccess, onScanError); }} catch(e) {{}}
                    }}, 2000);
                }});
            }}

            function onScanSuccess(decodedText) {{
                if (scanLock) return;
                processQR(decodedText);
            }}
            function onScanError(err) {{}}

            var html5QrcodeScanner = new Html5QrcodeScanner("qr-reader", {{ fps: 10, qrbox: 250, showTorchButtonIfSupported: true }});
            html5QrcodeScanner.render(onScanSuccess, onScanError);
            </script>
            <style>
            #qr-reader {{ border: none !important; background: transparent !important; }}
            #qr-reader img[alt*="camera"] {{ max-width: 60px; }}
            #qr-reader button {{
                background: #5c67f2 !important; color: white !important;
                border: none !important; border-radius: 8px !important;
                padding: 7px 16px !important; margin: 4px !important;
                font-size: 13px !important; font-weight: 600 !important;
                cursor: pointer !important;
            }}
            #qr-reader select {{ border: 1px solid #ddd; border-radius: 8px; padding: 5px 10px; font-size: 13px; }}
            </style>
            """
            components.html(scanner_html, height=420)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_manual:
            st.markdown('<div class="dash-card dash-card-tight">', unsafe_allow_html=True)
            st.markdown(f'<p class="section-label">{ICON_KEYBOARD} Input ID Manual &amp; Aksi Status</p>', unsafe_allow_html=True)

            st.text_input(
                "ID Barcode",
                placeholder="Scan atau ketik ID Barang di sini...",
                label_visibility="collapsed",
                key="barcode_input"
            )

            st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)

            col_btn1, col_btn2, col_btn3 = st.columns(3)
            with col_btn1:
                st.markdown('<style>[data-testid="column"]:nth-of-type(1) button{background:#eef0fe!important;color:#4551d9!important;border:1px solid #c5cafc!important;}</style>', unsafe_allow_html=True)
                if st.button("⚙️ Proses", use_container_width=True): simpan_ke_sheet("Proses")
            with col_btn2:
                st.markdown('<style>[data-testid="column"]:nth-of-type(2) button{background:#ecfdf5!important;color:#068a5a!important;border:1px solid #a7f3d0!important;}</style>', unsafe_allow_html=True)
                if st.button("✓ Selesai", use_container_width=True): simpan_ke_sheet("Selesai")
            with col_btn3:
                st.markdown('<style>[data-testid="column"]:nth-of-type(3) button{background:#fff1f1!important;color:#c93030!important;border:1px solid #fecaca!important;}</style>', unsafe_allow_html=True)
                if st.button("✕ Reject", use_container_width=True): simpan_ke_sheet("Reject")

            st.markdown(f"""
                <div style='margin-top:20px; background:linear-gradient(135deg,#f8fafc,#f4f5fb); border:1px solid #e8eaf2; border-radius:12px; padding:14px 16px;'>
                    <p style='margin:0 0 10px; font-size:11px; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:#94a3b8;'>Panduan Aksi</p>
                    <div style='display:flex; align-items:center; gap:8px; margin-bottom:7px; font-size:12px; color:#64748b;'>
                        <span style='color:#4551d9;'>{ICON_GEAR}</span> <b style='color:#1e293b;'>Proses</b> — Barang sedang dikerjakan
                    </div>
                    <div style='display:flex; align-items:center; gap:8px; margin-bottom:7px; font-size:12px; color:#64748b;'>
                        <span style='color:#068a5a;'>{ICON_CHECK}</span> <b style='color:#1e293b;'>Selesai</b> — Lolos QC, siap kirim
                    </div>
                    <div style='display:flex; align-items:center; gap:8px; font-size:12px; color:#64748b;'>
                        <span style='color:#c93030;'>{ICON_X}</span> <b style='color:#1e293b;'>Reject</b> — Perlu rework / buang
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='margin:28px 0 12px;'></div>", unsafe_allow_html=True)
        st.markdown(f'<p class="analytics-title">{ICON_CHART} Analitik Real-Time</p>', unsafe_allow_html=True)

        # Kalkulasi Metrik
        if not df_master.empty and 'Status' in df_master.columns:
            df_master['Status_Clean'] = df_master['Status'].astype(str).str.strip().str.capitalize()
            jml_proses  = len(df_master[df_master['Status_Clean'] == 'Proses'])
            jml_selesai = len(df_master[df_master['Status_Clean'] == 'Selesai'])
            jml_reject  = len(df_master[df_master['Status_Clean'] == 'Reject'])
        else:
            jml_proses, jml_selesai, jml_reject = 0, 0, 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'''<div class="metric-card metric-blue">
                <div class="metric-row"><div class="metric-icon">{ICON_GEAR}</div></div>
                <p>Total Baju Proses</p><h2>{jml_proses:,}</h2>
            </div>''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''<div class="metric-card metric-green">
                <div class="metric-row"><div class="metric-icon">{ICON_CHECK}</div></div>
                <p>Selesai QC</p><h2>{jml_selesai:,}</h2>
            </div>''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''<div class="metric-card metric-red">
                <div class="metric-row"><div class="metric-icon">{ICON_X}</div></div>
                <p>Reject</p><h2>{jml_reject:,}</h2>
            </div>''', unsafe_allow_html=True)

        st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
        col_chart1, col_chart2 = st.columns([2, 1])

        with col_chart1:
            st.markdown('<div class="dash-card">', unsafe_allow_html=True)
            st.markdown(f'<p class="chart-header">{ICON_CHART} Produktivitas Departemen {st.session_state["departemen"]} Per Hari</p>', unsafe_allow_html=True)
            if not df_master.empty and 'Waktu' in df_master.columns and 'Departemen' in df_master.columns:
                df_master['Waktu_dt'] = pd.to_datetime(df_master['Waktu'], errors='coerce')
                df_filtered_dept = df_master[df_master['Departemen'] == st.session_state['departemen']].copy()

                day_map = {0:'Sen', 1:'Sel', 2:'Rab', 3:'Kam', 4:'Jum', 5:'Sab', 6:'Min'}
                df_filtered_dept['Hari_Num'] = df_filtered_dept['Waktu_dt'].dt.dayofweek
                df_filtered_dept['Hari']     = df_filtered_dept['Hari_Num'].map(day_map)

                df_chart_grouped = df_filtered_dept.groupby(['Hari_Num', 'Hari']).size().reset_index(name='Produktivitas')
                full_days = pd.DataFrame({'Hari_Num': range(7), 'Hari': ['Sen','Sel','Rab','Kam','Jum','Sab','Min']})
                df_chart_final = pd.merge(full_days, df_chart_grouped, on=['Hari_Num','Hari'], how='left').fillna(0)
            else:
                df_chart_final = pd.DataFrame({"Hari": ["Sen","Sel","Rab","Kam","Jum","Sab","Min"], "Produktivitas": [0]*7})

            fig = px.bar(df_chart_final, x="Hari", y="Produktivitas", color_discrete_sequence=['#5c67f2'])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font_family="Inter, sans-serif",
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(showgrid=False, title=None, tickfont=dict(size=12, color='#64748b')),
                yaxis=dict(gridcolor='#f1f5f9', title=None, tickfont=dict(size=12, color='#64748b')),
                bargap=0.35,
            )
            fig.update_traces(marker_line_width=0, marker_cornerradius=8)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_chart2:
            st.markdown('<div class="dash-card">', unsafe_allow_html=True)
            st.markdown(f'<p class="chart-header">{ICON_PIE} Komposisi Status Baju</p>', unsafe_allow_html=True)
            df_pie = pd.DataFrame({
                "Status": ["Selesai QC", "Reject", "Proses"],
                "Jumlah": [jml_selesai, jml_reject, jml_proses]
            })
            fig_pie = px.pie(
                df_pie, values='Jumlah', names='Status', hole=0.6,
                color='Status',
                color_discrete_map={'Selesai QC':'#0db97f', 'Reject':'#e84646', 'Proses':'#5c67f2'}
            )
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font_family="Inter, sans-serif",
                margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5, font=dict(size=11, color='#64748b')),
            )
            fig_pie.update_traces(textfont_size=12, marker=dict(line=dict(color='white', width=3)))
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown(f'<p class="chart-header">{ICON_CHART} Tren Produktivitas Per Hari — {st.session_state["departemen"]}</p>', unsafe_allow_html=True)
        if not df_master.empty and 'Waktu' in df_master.columns and 'Departemen' in df_master.columns and 'Status' in df_master.columns:
            df_line = df_master[df_master['Departemen'] == st.session_state['departemen']].copy()
            df_line['Waktu_dt'] = pd.to_datetime(df_line['Waktu'], errors='coerce')
            day_map = {0:'Sen', 1:'Sel', 2:'Rab', 3:'Kam', 4:'Jum', 5:'Sab', 6:'Min'}
            df_line['Hari_Num'] = df_line['Waktu_dt'].dt.dayofweek
            df_line['Hari'] = df_line['Hari_Num'].map(day_map)
            df_line['Status_Clean'] = df_line['Status'].astype(str).str.strip().str.capitalize()
            df_line_grouped = df_line.groupby(['Hari_Num', 'Hari', 'Status_Clean']).size().reset_index(name='Jumlah')
            full_days = pd.DataFrame({'Hari_Num': range(7), 'Hari': ['Sen','Sel','Rab','Kam','Jum','Sab','Min']})
            all_statuses = ['Proses', 'Selesai', 'Reject']
            full_grid = full_days.merge(pd.DataFrame({'Status_Clean': all_statuses}), how='cross')
            df_line_final = pd.merge(full_grid, df_line_grouped, on=['Hari_Num','Hari','Status_Clean'], how='left').fillna(0)
            fig_line = px.line(df_line_final, x='Hari', y='Jumlah', color='Status_Clean', markers=True,
                                color_discrete_map={'Proses':'#5c67f2', 'Selesai':'#0db97f', 'Reject':'#e84646'},
                                category_orders={'Hari': ['Sen','Sel','Rab','Kam','Jum','Sab','Min']})
            fig_line.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font_family="Inter, sans-serif",
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(showgrid=False, title=None, tickfont=dict(size=12, color='#64748b')),
                yaxis=dict(gridcolor='#f1f5f9', title=None, tickfont=dict(size=12, color='#64748b')),
                legend=dict(orientation='h', yanchor='bottom', y=-0.35, xanchor='center', x=0.5, font=dict(size=11, color='#64748b')),
            )
            fig_line.update_traces(line=dict(width=2.8), marker=dict(size=7))
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("Data untuk tren harian belum tersedia.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================================================
    # 2. DATA SELESAI
    # ==========================================================================
    elif st.session_state['page'] == 'Data Selesai':
        st.markdown(f"""
            <div class="page-header" style="border-color:#0db97f;">
                <div class="icon-badge" style="background:linear-gradient(135deg,#16c98c,#089968); box-shadow:0 6px 14px -4px rgba(16,201,140,0.55);">{ICON_CHECK}</div>
                <div>
                    <h2 style="color:#0a7c56;">Data Produksi — Selesai QC</h2>
                    <p>Daftar semua item yang telah lolos quality control</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:6px;'></div>", unsafe_allow_html=True)
        if not df_master.empty and 'Status' in df_master.columns:
            df_selesai = df_master[df_master['Status'].astype(str).str.strip().str.capitalize() == 'Selesai']
            render_table(df_selesai)
        else:
            st.info("Belum ada data barang berstatus Selesai, atau header kolom belum diatur di Spreadsheet.")

    # ==========================================================================
    # 3. DATA REJECT
    # ==========================================================================
    elif st.session_state['page'] == 'Data Reject':
        st.markdown(f"""
            <div class="page-header" style="border-color:#e84646;">
                <div class="icon-badge" style="background:linear-gradient(135deg,#f0585f,#c93030); box-shadow:0 6px 14px -4px rgba(232,70,70,0.55);">{ICON_X}</div>
                <div>
                    <h2 style="color:#c93030;">Data Produksi — Reject</h2>
                    <p>Daftar item yang perlu rework atau dibuang</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:6px;'></div>", unsafe_allow_html=True)
        if not df_master.empty and 'Status' in df_master.columns:
            df_reject = df_master[df_master['Status'].astype(str).str.strip().str.capitalize() == 'Reject']
            render_table(df_reject)
        else:
            st.info("Belum ada data barang berstatus Reject, atau header kolom belum diatur di Spreadsheet.")

    # ==========================================================================
    # 4. REKAPITULASI DATA HARIAN
    # ==========================================================================
    elif st.session_state['page'] == 'Rekapitulasi Data Harian':
        st.markdown(f"""
            <div class="page-header">
                <div class="icon-badge">{ICON_LIST}</div>
                <div>
                    <h2>Rekapitulasi Data Harian</h2>
                    <p>Keseluruhan data produksi dari semua departemen</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:6px;'></div>", unsafe_allow_html=True)
        if not df_master.empty:
            render_table(df_master)
        else:
            st.info("Gagal mengambil data database. Pastikan header di Baris 1 Spreadsheet sudah benar.")