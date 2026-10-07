import streamlit as st
import svg_art

GREEN, DARK, CREAM, GOLD = "#2E7D4F", "#1B4D32", "#FBF8F0", "#E3A72F"

CSS = f"""
<style>
.block-container {{ padding-top: 1.4rem; padding-bottom: 3rem; max-width: 1250px; }}
h1, h2, h3 {{ color: {DARK}; letter-spacing: -0.3px; }}
[data-testid="stSidebar"] {{ background: linear-gradient(180deg, #E4EFE0 0%, #F3F7EE 100%); border-right: 1px solid #d4e3cf; }}
.brand {{ background: linear-gradient(135deg, {DARK}, {GREEN}); color: #fff; border-radius: 16px; padding: 16px 18px; margin-bottom: 10px; }}
.brand b {{ font-size: 1.35rem; }} .brand span {{ opacity: .85; font-size: .82rem; }}
.userchip {{ background:#fff; border:1px solid #d4e3cf; border-radius:14px; padding:10px 14px; margin-bottom:8px; }}
.userchip small {{ color:#6b7a6b; }}
.hero {{ display:flex; align-items:center; gap:10px; background: linear-gradient(120deg, {DARK} 0%, {GREEN} 55%, #5BAA55 100%);
        border-radius: 22px; color:#fff; overflow:hidden; margin-bottom: 18px; box-shadow: 0 8px 24px rgba(27,77,50,.25); }}
.hero .txt {{ padding: 28px 8px 28px 34px; flex: 1.1; }}
.hero h1 {{ color:#fff; margin:0 0 6px 0; font-size: 2.1rem; }}
.hero p {{ margin:0; opacity:.92; font-size: 1.02rem; }}
.hero img {{ flex: 1.3; max-width: 58%; display:block; align-self:flex-end; }}
.pagehead {{ display:flex; align-items:center; gap:14px; background: linear-gradient(120deg, #E4EFE0, #F7F3E2); border:1px solid #d4e3cf;
            border-radius:18px; padding: 14px 22px; margin-bottom: 16px; }}
.pagehead .ic {{ font-size: 2rem; }} .pagehead h2 {{ margin:0; font-size:1.5rem; }} .pagehead p {{ margin:0; color:#5d6b5d; font-size:.92rem; }}
.kpi {{ background:#fff; border-radius:18px; padding:16px 18px; border:1px solid #e4ecdf; box-shadow: 0 3px 12px rgba(0,0,0,.05); border-left: 6px solid {GREEN}; }}
.kpi .l {{ color:#6b7a6b; font-size:.82rem; text-transform:uppercase; letter-spacing:.6px; }}
.kpi .v {{ font-size:1.9rem; font-weight:700; color:{DARK}; line-height:1.2; }}
.kpi .s {{ font-size:.82rem; color:#6b7a6b; }}
.kpi.gold {{ border-left-color:{GOLD}; }} .kpi.red {{ border-left-color:#D9534F; }} .kpi.blue {{ border-left-color:#3B82C4; }}
.acard {{ background:#fff; border:1px solid #e4ecdf; border-radius:18px; padding:8px 12px 12px; box-shadow:0 3px 12px rgba(0,0,0,.05); margin-bottom:14px; }}
.acard .pic {{ background: linear-gradient(180deg,#DDF0FA,#EAF5DF); border-radius:12px; padding:6px; }}
.acard .pic img {{ width:100%; display:block; }}
.acard .nm {{ font-weight:700; font-size:1.05rem; color:{DARK}; margin-top:6px; }}
.acard .meta {{ color:#6b7a6b; font-size:.82rem; }}
.chip {{ display:inline-block; padding:2px 10px; border-radius:20px; font-size:.75rem; font-weight:600; margin-top:6px; }}
.chip.ok {{ background:#DDF3E3; color:#1d7a3e; }} .chip.soon {{ background:#FFF1CC; color:#9a6b00; }} .chip.bad {{ background:#FBD9D7; color:#b02a25; }} .chip.none {{ background:#EEE; color:#666; }}
.loginbox {{ background:#fff; border:1px solid #e4ecdf; border-radius:20px; padding: 10px 18px 6px; box-shadow:0 6px 22px rgba(0,0,0,.07); }}
.demo {{ background:#FFF8E1; border:1px dashed #E3A72F; border-radius:12px; padding:10px 14px; font-size:.86rem; color:#6b5200; }}
div.stButton > button, div.stFormSubmitButton > button {{ border-radius: 12px; font-weight:600; }}
div.stFormSubmitButton > button[kind="primary"], div.stButton > button[kind="primary"] {{ background: {GREEN}; border-color: {GREEN}; }}
footer {{ visibility: hidden; }}
</style>
"""

def inject():
    st.markdown(CSS, unsafe_allow_html=True)

def hero(title, subtitle):
    uri = svg_art.to_data_uri(svg_art.scene_svg())
    st.markdown(f'<div class="hero"><div class="txt"><h1>{title}</h1><p>{subtitle}</p></div><img src="{uri}"/></div>', unsafe_allow_html=True)

def pagehead(icon, title, sub=""):
    st.markdown(f'<div class="pagehead"><div class="ic">{icon}</div><div><h2>{title}</h2><p>{sub}</p></div></div>', unsafe_allow_html=True)

def kpi(label, value, sub="", color=""):
    st.markdown(f'<div class="kpi {color}"><div class="l">{label}</div><div class="v">{value}</div><div class="s">{sub}</div></div>', unsafe_allow_html=True)

def animal_card(a, status, css):
    uri = svg_art.to_data_uri(svg_art.animal_svg(a["species"]))
    st.markdown(f'''<div class="acard"><div class="pic"><img src="{uri}"/></div>
        <div class="nm">{a["name"]} <span class="meta">&middot; {a["tag"]}</span></div>
        <div class="meta">{a["species"]} &middot; {a["breed"]} &middot; {a["age_months"]} months &middot; {a["weight_kg"]:.0f} kg</div>
        <div class="meta">Owner: {a["owner"]}</div><span class="chip {css}">{status}</span></div>''', unsafe_allow_html=True)
