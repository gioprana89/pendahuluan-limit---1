"""Simulasi Kalkulus: 2.1.1 Kecepatan Sesaat (s(t) = t^2).

Referensi pengantar: Varberg, Purcell, Rigdon, Calculus Early Transcendentals,
Bab 2, Section 2.1 (Introduction to Limits). Contoh numerik ini disusun
sebagai bahan ajar pendamping, bukan kutipan soal verbatim buku.

Jalankan: streamlit run streamlit_app.py
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Kalkulus Interaktif | Limit dan Kecepatan Sesaat",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Nilai awal sengaja dibuat tetap sesuai contoh kasus di modul.
T0 = 3.0  # detik
S0 = T0**2  # meter
V_LIMIT = 2 * T0  # m/s; dihitung dari limit hasil faktorisasi
H_VALUES = [1.0, 0.5, 0.2, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0001]


def position(t: float) -> float:
    """Model posisi kendaraan, s(t) = t^2 (t >= 0)."""
    return t**2


def average_velocity(t: float) -> float:
    """Kecepatan rata-rata dari t=3 ke t != 3."""
    if t == T0:
        raise ValueError("Kecepatan rata-rata berbentuk 0/0 pada t = 3.")
    return (position(t) - S0) / (t - T0)


def tidy(value: float, decimals: int = 7) -> str:
    """Format angka agar tabel mudah dibaca tanpa nol yang berlebih."""
    result = f"{value:.{decimals}f}".rstrip("0").rstrip(".")
    return result if result not in {"", "-0"} else "0"


def draw_position_graph(h: float, zoom: bool) -> go.Figure:
    """Kurva posisi, dua garis secan, dan garis acuan limitnya."""
    if zoom:
        radius = min(3.0, max(3.0 * h, 0.0006))
        x_min, x_max = max(0.0, T0 - radius), T0 + radius
    else:
        x_min, x_max = 1.3, 4.7

    width = x_max - x_min
    ts = [x_min + width * j / 300 for j in range(301)]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=ts,
            y=[position(t) for t in ts],
            mode="lines",
            name="Posisi kendaraan s(t) = t²",
            line=dict(color="#0f9d95", width=4),
            hovertemplate="t = %{x:.5f} detik<br>s(t) = %{y:.5f} meter<extra></extra>",
        )
    )

    t_left, t_right = T0 - h, T0 + h
    left_v, right_v = average_velocity(t_left), average_velocity(t_right)
    line_specs = [
        ("Secan dari kiri", left_v, "#2764cf", "dot"),
        ("Secan dari kanan", right_v, "#e18b25", "dot"),
        ("Garis acuan: kemiringan 6", V_LIMIT, "#8357aa", "dash"),
    ]
    for name, slope, color, dash in line_specs:
        fig.add_trace(
            go.Scatter(
                x=[x_min, x_max],
                y=[S0 + slope * (x_min - T0), S0 + slope * (x_max - T0)],
                mode="lines",
                name=name,
                line=dict(color=color, width=2, dash=dash),
                hovertemplate=f"{name}<br>Kemiringan: {tidy(slope)} m/s<extra></extra>",
            )
        )

    for name, t, color in [
        ("Titik dari kiri", t_left, "#2764cf"),
        ("Titik dari kanan", t_right, "#e18b25"),
        ("Titik acuan t = 3", T0, "#0f9d95"),
    ]:
        fig.add_trace(
            go.Scatter(
                x=[t],
                y=[position(t)],
                mode="markers",
                name=name,
                marker=dict(size=12, color=color, line=dict(width=2, color="white")),
                hovertemplate=f"{name}<br>t = {tidy(t)} detik<br>s(t) = {tidy(position(t))} meter<extra></extra>",
            )
        )

    fig.add_vline(x=T0, line_dash="dash", line_color="gray", opacity=0.45)
    fig.update_layout(
        height=510,
        margin=dict(l=14, r=14, t=30, b=12),
        xaxis_title="Waktu, t (detik)",
        yaxis_title="Posisi, s(t) (meter)",
        legend=dict(orientation="h", y=-0.22, x=0, font=dict(size=11)),
        hovermode="closest",
    )
    fig.update_xaxes(range=[x_min, x_max], showgrid=True, zeroline=False)
    if zoom:
        values = [position(x_min), position(x_max)]
        pad = max(0.0006, (max(values) - min(values)) * 0.15)
        fig.update_yaxes(range=[min(values) - pad, max(values) + pad])
    else:
        fig.update_yaxes(range=[0, 24], rangemode="tozero")
    return fig


def draw_convergence_graph(selected_index: int) -> go.Figure:
    """Tunjukkan dua kecepatan rata-rata yang konvergen ke 6."""
    xs = list(range(len(H_VALUES)))
    left = [V_LIMIT - h for h in H_VALUES]
    right = [V_LIMIT + h for h in H_VALUES]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=xs, y=left, mode="lines+markers", name="Pendekatan kiri",
            line=dict(color="#2764cf", width=2),
            marker=dict(size=[13 if i == selected_index else 8 for i in xs]),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=xs, y=right, mode="lines+markers", name="Pendekatan kanan",
            line=dict(color="#e18b25", width=2),
            marker=dict(size=[13 if i == selected_index else 8 for i in xs]),
        )
    )
    fig.add_hline(y=V_LIMIT, line_color="#8357aa", line_dash="dash", annotation_text="Limit = 6 m/s")
    fig.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=25, b=25),
        xaxis=dict(
            tickmode="array", tickvals=xs, ticktext=[tidy(h, 4) for h in H_VALUES],
            title="Jarak waktu ke t=3, h (semakin kecil ke kanan)",
        ),
        yaxis_title="Kecepatan rata-rata (m/s)",
        legend=dict(orientation="h", y=-0.35, x=0),
    )
    return fig


def make_table() -> pd.DataFrame:
    rows = []
    for h in H_VALUES:
        for direction, t in [("Dari kiri", T0 - h), ("Dari kanan", T0 + h)]:
            v = average_velocity(t)
            rows.append(
                {
                    "h": tidy(h),
                    "Arah": direction,
                    "Waktu t (detik)": tidy(t),
                    "Posisi s(t) (meter)": tidy(position(t)),
                    "Kecepatan rata-rata (m/s)": tidy(v),
                    "Galat terhadap 6 (m/s)": tidy(abs(v - V_LIMIT)),
                }
            )
    return pd.DataFrame(rows)


st.markdown(
    """<style>
    .block-container {padding-top: 1.6rem; padding-bottom: 3rem;}
    .hero {padding: 1.2rem 1.45rem; border-radius: 18px; background: linear-gradient(120deg,#053f54,#107e82); color: white; margin-bottom: 1rem;}
    .hero h1 {font-size: 1.8rem; margin: 0 0 .4rem 0; color:white;}
    .hero p {font-size: 1.02rem; margin: 0; color:#e6f7f6;}
    .stMetric {border:1px solid rgba(128,128,128,.18); padding:.7rem; border-radius:12px;}
    </style>""",
    unsafe_allow_html=True,
)

st.markdown(
    """<div class="hero"><h1>🚗 Laboratorium Limit: Kecepatan Sesaat</h1>
    <p>Bab 2 · Subbab 2.1 · Contoh Kasus 1 — Menghitung Kecepatan Sesaat Sebuah Kendaraan</p></div>""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("📚 Panduan Penggunaan")
    st.write("**Tujuan:** Menyelidiki kecepatan kendaraan tepat pada detik ke-3.")
    st.markdown(
        "1. Tekan **▶ Putar** untuk menjalankan animasi.\n"
        "2. Amati titik biru dan oranye mendekati waktu 3 detik.\n"
        "3. Perhatikan perubahan tabel dan kemiringan garis secan.\n"
        "4. Coba **🔎 Perbesar grafik**, lalu kerjakan pertanyaan refleksi."
    )
    st.divider()
    st.markdown("**Model yang digunakan:**")
    st.latex(r"s(t) = t^2, \quad t\geq 0")
    st.latex(r"s(3)=9\text{ meter}")
    st.caption("Penting: t=3 tidak boleh disubstitusikan ke rumus kecepatan rata-rata karena penyebut menjadi nol.")
    st.divider()
    st.caption("Acuan konsep: Varberg, Purcell & Rigdon, *Calculus Early Transcendentals*, Bab 2, §2.1. Contoh numerik dikembangkan untuk modul kuliah.")

st.subheader("A. Permasalahan")
st.write(
    "Sebuah kendaraan bergerak lurus dengan model posisi **s(t) = t²**, "
    "dengan t dalam detik dan s(t) dalam meter. "
    "**Berapa kecepatan kendaraan tepat pada detik ke-3?**"
)
st.latex(r"\bar v(t)=\frac{s(t)-s(3)}{t-3}=\frac{t^2-9}{t-3},\qquad t\ne3")
st.info(
    "💡 Pertanyaan untuk mahasiswa: apa yang terjadi pada kecepatan rata-rata "
    "ketika t mendekati 3 dari kiri dan kanan?"
)

for key, initial in [("h_index", 0), ("playing", False), ("zoom", False)]:
    if key not in st.session_state:
        st.session_state[key] = initial


def pause_on_manual_change() -> None:
    st.session_state.playing = False


@st.fragment(run_every="850ms")
def interactive_lab() -> None:
    st.subheader("B. Simulasi Interaktif")
    start_col, pause_col, reset_col = st.columns(3)
    if start_col.button("▶ Putar animasi", use_container_width=True, type="primary"):
        if st.session_state.h_index == len(H_VALUES) - 1:
            st.session_state.h_index = 0
        st.session_state.playing = True
    if pause_col.button("⏸ Jeda", use_container_width=True):
        st.session_state.playing = False
    if reset_col.button("↻ Ulangi", use_container_width=True):
        st.session_state.playing = False
        st.session_state.h_index = 0

    # Setiap interval animasi memilih h yang lebih kecil.
    if st.session_state.playing:
        if st.session_state.h_index < len(H_VALUES) - 1:
            st.session_state.h_index += 1
        else:
            st.session_state.playing = False

    index = st.slider(
        "Langkah pendekatan (geser ke kanan agar t semakin dekat ke 3)",
        min_value=0,
        max_value=len(H_VALUES) - 1,
        key="h_index",
        on_change=pause_on_manual_change,
        format="%d",
    )
    h = H_VALUES[index]
    st.caption(f"Langkah {index+1}/{len(H_VALUES)} — h = {tidy(h, 4)} detik")
    st.toggle("🔎 Perbesar grafik di sekitar t = 3", key="zoom")

    col_plot, col_stats = st.columns([1.85, 1], gap="large")
    with col_plot:
        st.plotly_chart(draw_position_graph(h, st.session_state.zoom), use_container_width=True, key="position_graph")
    with col_stats:
        st.markdown("**Nilai saat ini**")
        st.metric("Jarak interval h", f"{tidy(h, 4)} detik")
        st.metric("Dari kiri: t = 3 − h", f"{tidy(3-h)} detik", f"{tidy(6-h)} m/s", delta_color="off")
        st.metric("Dari kanan: t = 3 + h", f"{tidy(3+h)} detik", f"{tidy(6+h)} m/s", delta_color="off")
        st.success("**Nilai kecepatan sesaat yang didekati: 6 m/s**")
        st.caption("Semakin kecil h, nilai dari kedua sisi semakin dekat ke 6 m/s.")

    st.markdown("#### C. Tabel Perhitungan Saat Ini")
    current = pd.DataFrame(
        [
            {"Pendekatan": "Dari kiri", "t (detik)": tidy(T0-h), "s(t) (meter)": tidy(position(T0-h)), "v̄ (m/s)": tidy(average_velocity(T0-h))},
            {"Pendekatan": "Tepat t = 3", "t (detik)": "3", "s(t) (meter)": "9", "v̄ (m/s)": "0/0 — tidak terdefinisi"},
            {"Pendekatan": "Dari kanan", "t (detik)": tidy(T0+h), "s(t) (meter)": tidy(position(T0+h)), "v̄ (m/s)": tidy(average_velocity(T0+h))},
        ]
    )
    st.dataframe(current, hide_index=True, use_container_width=True)

    st.markdown("#### D. Perhitungan Manual Sesuai Langkah Animasi")
    st.latex(r"\bar v_{\mathrm{kiri}}=\frac{(3-h)^2-9}{(3-h)-3}=6-h")
    st.latex(r"\bar v_{\mathrm{kanan}}=\frac{(3+h)^2-9}{(3+h)-3}=6+h")
    st.write(
        f"Untuk **h = {tidy(h,4)}**, diperoleh kecepatan rata-rata kiri "
        f"**{tidy(V_LIMIT-h)} m/s** dan kanan **{tidy(V_LIMIT+h)} m/s**."
    )
    st.markdown("#### E. Konvergensi Kecepatan Rata-rata")
    st.plotly_chart(draw_convergence_graph(index), use_container_width=True, key="convergence_graph")


interactive_lab()

with st.expander("📋 Lihat tabel semua percobaan (kiri dan kanan)", expanded=False):
    st.dataframe(make_table(), use_container_width=True, hide_index=True)
    st.caption("Tabel ini merupakan evaluasi deterministik dari model s(t) = t², bukan data observasi atau simulasi acak.")

st.subheader("F. Kesimpulan Matematis")
st.latex(
    r"\lim_{t\to 3}\frac{t^2-9}{t-3}"
    r"=\lim_{t\to 3}\frac{(t-3)(t+3)}{t-3}"
    r"=\lim_{t\to 3}(t+3)=\boxed{6}"
)
st.write(
    "Pencoretan faktor **(t − 3)** hanya berlaku saat **t ≠ 3**. "
    "Meskipun kecepatan rata-rata pada interval nol tidak terdefinisi, "
    "nilai limitnya ada dan sama dengan **6 m/s**. Inilah kecepatan sesaat pada detik ke-3."
)
st.warning(
    "**Catatan metode:** Tabel dan grafik membantu memperkirakan limit, "
    "sedangkan faktorisasi memberi alasan matematis untuk nilai limit pada contoh ini. "
    "Komputer tidak boleh dijadikan satu-satunya bukti keberadaan limit."
)

st.subheader("G. Pertanyaan Diskusi Mahasiswa")
with st.form("student_quiz"):
    ans1 = st.radio(
        "1. Ketika t tepat sama dengan 3, apa yang terjadi pada rumus kecepatan rata-rata?",
        ["Nilainya 6", "Menjadi bentuk 0/0 yang tidak terdefinisi", "Nilainya 0"],
        index=None,
    )
    ans2 = st.radio(
        "2. Ketika interval h semakin kecil, kecepatan rata-rata dari kiri dan kanan mendekati...",
        ["0 m/s", "3 m/s", "6 m/s", "9 m/s"],
        index=None,
    )
    submitted = st.form_submit_button("Periksa jawaban")
if submitted:
    if ans1 is None or ans2 is None:
        st.info("Silakan jawab kedua pertanyaan dahulu.")
    else:
        score = int(ans1 == "Menjadi bentuk 0/0 yang tidak terdefinisi") + int(ans2 == "6 m/s")
        st.success(f"Skor: {score}/2") if score == 2 else st.warning(f"Skor: {score}/2. Diskusikan kembali grafik dan tabelnya.")
        st.write("**Penjelasan:** Kecepatan rata-rata tidak terdefinisi untuk interval waktu nol, tetapi limitnya dapat dihitung melalui pendekatan dari kedua sisi.")

st.divider()
st.caption("Materi: Bab 2 · 2.1 Pendahuluan Limit · 2.1.1 Contoh Kasus 1 | Pendamping pembelajaran Kalkulus")
