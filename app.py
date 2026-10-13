from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Ground Turnaround Performance",
    page_icon="✈️",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "data" / "ground_turnaround_simulated_dataset.csv"

st.markdown(
    """
    <style>
    .block-container {padding-top: 1.4rem; padding-bottom: 2rem;}
    div[data-testid="stMetric"] {
        background: #f7f9fc;
        border: 1px solid #e5eaf2;
        padding: 14px 16px;
        border-radius: 12px;
    }
    .small-note {font-size: 0.88rem; color: #64748b;}
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["operation_date"] = pd.to_datetime(df["operation_date"], errors="coerce")
    for col in [
        "sla_breach_flag",
        "adverse_weather_flag",
        "staff_shortage_flag",
        "equipment_delay_flag",
        "catering_delay_flag",
        "baggage_delay_flag",
        "maintenance_check_flag",
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    return df

st.title("✈️ Ground Turnaround Performance")
st.caption("Operations intelligence | SLA adherence | On-time performance | Delay investigation")

if not DATA_PATH.exists():
    st.error(
        f"Dataset not found at {DATA_PATH}. Keep the CSV in the project's data/ folder "
        "or update DATA_PATH in app.py."
    )
    st.stop()

df = load_data(str(DATA_PATH))
required = {
    "flight_id", "operation_date", "station", "handler", "time_band",
    "planned_turnaround_min", "actual_turnaround_min", "turnaround_variance_min",
    "sla_breach_flag", "departure_delay_min", "otp_status",
}
missing = required - set(df.columns)
if missing:
    st.error(f"The dataset is missing required columns: {', '.join(sorted(missing))}")
    st.stop()

min_date = df["operation_date"].min().date()
max_date = df["operation_date"].max().date()

with st.sidebar:
    st.header("Dashboard filters")
    selected_dates = st.date_input(
        "Operation date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    stations = sorted(df["station"].dropna().unique().tolist())
    handlers = sorted(df["handler"].dropna().unique().tolist())
    time_bands = sorted(df["time_band"].dropna().unique().tolist())
    selected_stations = st.multiselect("Station", stations, default=stations)
    selected_handlers = st.multiselect("Ground handler", handlers, default=handlers)
    selected_time_bands = st.multiselect("Time band", time_bands, default=time_bands)
    st.divider()
    st.caption("This portfolio project uses simulated data, not live airline operational data.")

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date = end_date = selected_dates

filtered = df[
    df["operation_date"].dt.date.between(start_date, end_date)
    & df["station"].isin(selected_stations)
    & df["handler"].isin(selected_handlers)
    & df["time_band"].isin(selected_time_bands)
].copy()

if filtered.empty:
    st.warning("No flights match these filters. Change one or more filters to continue.")
    st.stop()

def pct(series: pd.Series) -> float:
    return float(series.mean() * 100) if len(series) else 0.0

flight_count = len(filtered)
avg_planned = filtered["planned_turnaround_min"].mean()
avg_actual = filtered["actual_turnaround_min"].mean()
avg_variance = filtered["turnaround_variance_min"].mean()
sla_breach_rate = pct(filtered["sla_breach_flag"])
otp_rate = float((filtered["otp_status"].astype(str).str.lower() == "on time").mean() * 100)
avg_departure_delay = filtered["departure_delay_min"].mean()

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Flights analysed", f"{flight_count:,}")
m2.metric("SLA breach rate", f"{sla_breach_rate:.1f}%")
m3.metric("On-time performance", f"{otp_rate:.1f}%")
m4.metric("Avg. turnaround variance", f"{avg_variance:+.1f} min")
m5.metric("Avg. departure delay", f"{avg_departure_delay:.1f} min")

st.markdown(
    f"<div class='small-note'>Average planned turnaround: {avg_planned:.1f} min · "
    f"Average actual turnaround: {avg_actual:.1f} min · "
    f"Period: {start_date:%d %b %Y} – {end_date:%d %b %Y}</div>",
    unsafe_allow_html=True,
)
st.divider()

left, right = st.columns([1.15, 1])
with left:
    st.subheader("SLA breaches by station")
    station_summary = (
        filtered.groupby("station", as_index=False)
        .agg(
            Flights=("flight_id", "count"),
            SLA_Breach_Rate=("sla_breach_flag", "mean"),
            Avg_Variance=("turnaround_variance_min", "mean"),
            OTP_Rate=("otp_status", lambda x: (x.astype(str).str.lower() == "on time").mean()),
        )
    )
    station_summary["SLA_Breach_Rate"] *= 100
    station_summary["OTP_Rate"] *= 100
    station_summary = station_summary.sort_values("SLA_Breach_Rate", ascending=False)
    fig_station = px.bar(
        station_summary,
        x="station",
        y="SLA_Breach_Rate",
        text=station_summary["SLA_Breach_Rate"].map(lambda x: f"{x:.1f}%"),
        labels={"station": "Station", "SLA_Breach_Rate": "Flights breaching SLA (%)"},
        hover_data={"Flights": True, "Avg_Variance": ":.1f", "OTP_Rate": ":.1f"},
    )
    fig_station.update_layout(height=350, margin=dict(l=10, r=10, t=20, b=10), yaxis_ticksuffix="%")
    fig_station.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(fig_station, use_container_width=True)

with right:
    st.subheader("Performance by time band")
    time_summary = (
        filtered.groupby("time_band", as_index=False)
        .agg(
            Flights=("flight_id", "count"),
            SLA_Breach_Rate=("sla_breach_flag", "mean"),
            Avg_Variance=("turnaround_variance_min", "mean"),
        )
    )
    time_summary["SLA_Breach_Rate"] *= 100
    time_summary = time_summary.sort_values("SLA_Breach_Rate", ascending=False)
    fig_time = px.bar(
        time_summary,
        x="time_band",
        y="SLA_Breach_Rate",
        text=time_summary["SLA_Breach_Rate"].map(lambda x: f"{x:.1f}%"),
        labels={"time_band": "Time band", "SLA_Breach_Rate": "Flights breaching SLA (%)"},
        hover_data={"Flights": True, "Avg_Variance": ":.1f"},
    )
    fig_time.update_layout(height=350, margin=dict(l=10, r=10, t=20, b=10), yaxis_ticksuffix="%")
    fig_time.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(fig_time, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Ground handler comparison")
    handler_summary = (
        filtered.groupby("handler", as_index=False)
        .agg(
            Flights=("flight_id", "count"),
            SLA_Breach_Rate=("sla_breach_flag", "mean"),
            Avg_Variance=("turnaround_variance_min", "mean"),
            Avg_Departure_Delay=("departure_delay_min", "mean"),
        )
    )
    handler_summary["SLA_Breach_Rate"] *= 100
    handler_summary = handler_summary.sort_values("SLA_Breach_Rate", ascending=False)
    fig_handler = px.bar(
        handler_summary,
        x="handler",
        y="SLA_Breach_Rate",
        text=handler_summary["SLA_Breach_Rate"].map(lambda x: f"{x:.1f}%"),
        labels={"handler": "Ground handler", "SLA_Breach_Rate": "Flights breaching SLA (%)"},
        hover_data={"Flights": True, "Avg_Variance": ":.1f", "Avg_Departure_Delay": ":.1f"},
    )
    fig_handler.update_layout(height=330, margin=dict(l=10, r=10, t=20, b=10), yaxis_ticksuffix="%")
    fig_handler.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(fig_handler, use_container_width=True)

with right:
    st.subheader("Daily trend")
    daily = (
        filtered.groupby("operation_date", as_index=False)
        .agg(
            Flights=("flight_id", "count"),
            Avg_Variance=("turnaround_variance_min", "mean"),
            SLA_Breach_Rate=("sla_breach_flag", "mean"),
        )
    )
    daily["SLA_Breach_Rate"] *= 100
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=daily["operation_date"], y=daily["Avg_Variance"],
        mode="lines", name="Avg turnaround variance (min)"
    ))
    fig_trend.add_trace(go.Scatter(
        x=daily["operation_date"], y=daily["SLA_Breach_Rate"],
        mode="lines", name="SLA breach rate (%)", yaxis="y2"
    ))
    fig_trend.update_layout(
        height=330,
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Operation date",
        yaxis=dict(title="Variance (min)"),
        yaxis2=dict(title="SLA breach (%)", overlaying="y", side="right", ticksuffix="%"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    st.plotly_chart(fig_trend, use_container_width=True)

st.divider()
st.subheader("Station performance detail")
display_station = station_summary.copy()
display_station["SLA_Breach_Rate"] = display_station["SLA_Breach_Rate"].map(lambda x: f"{x:.1f}%")
display_station["OTP_Rate"] = display_station["OTP_Rate"].map(lambda x: f"{x:.1f}%")
display_station["Avg_Variance"] = display_station["Avg_Variance"].map(lambda x: f"{x:+.1f} min")
display_station.columns = ["Station", "Flights", "SLA breach rate", "Avg variance", "OTP rate"]
st.dataframe(display_station, use_container_width=True, hide_index=True)

with st.expander("Delay-driver flags: investigation guide"):
    flag_cols = {
        "adverse_weather_flag": "Adverse weather",
        "staff_shortage_flag": "Staff shortage",
        "equipment_delay_flag": "Equipment delay",
        "catering_delay_flag": "Catering delay",
        "baggage_delay_flag": "Baggage delay",
        "maintenance_check_flag": "Maintenance check",
    }
    rows = []
    for col, label in flag_cols.items():
        if col in filtered.columns:
            flagged = filtered[filtered[col] == 1]
            unflagged = filtered[filtered[col] == 0]
            rows.append({
                "Driver flag": label,
                "Flights flagged": len(flagged),
                "Flagged avg variance (min)": round(flagged["turnaround_variance_min"].mean(), 1) if len(flagged) else None,
                "Unflagged avg variance (min)": round(unflagged["turnaround_variance_min"].mean(), 1) if len(unflagged) else None,
            })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.caption(
        "These flags may overlap and are not mutually exclusive. Differences are descriptive associations, "
        "not proof of causation. Investigate event timestamps and control for station, handler, aircraft, "
        "traffic mix, and operating conditions before assigning root cause."
    )

st.subheader("Management interpretation")
worst_station = station_summary.sort_values("SLA_Breach_Rate", ascending=False).iloc[0]
worst_band = time_summary.sort_values("SLA_Breach_Rate", ascending=False).iloc[0]
st.markdown(
    f"""
    - **Priority station to investigate:** {worst_station['station']} has the highest observed SLA breach rate
      in the current filter selection ({worst_station['SLA_Breach_Rate']:.1f}% across {int(worst_station['Flights'])} flights).
    - **Priority time band to investigate:** {worst_band['time_band']} has the highest observed breach rate
      ({worst_band['SLA_Breach_Rate']:.1f}%).
    - **Suggested next step:** validate these patterns with operational teams, review timestamp-level delay
      reasons, and pilot targeted staffing/equipment coordination before claiming an improvement.
    """
)

st.caption(
    "Data note: this is a simulated portfolio dataset. SLA breach is defined in the source data using "
    "a synthetic target; on-time performance uses the source OTP label. No real airline savings or causal "
    "improvements are claimed."
)

csv_bytes = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered records (CSV)",
    data=csv_bytes,
    file_name="filtered_ground_turnaround_records.csv",
    mime="text/csv",
)


# Creator attribution
st.divider()
st.markdown(
    """
    <div style="text-align:center; padding: 0.6rem 0 0.2rem 0;">
        <div style="font-weight:600; font-size:0.95rem; color:#334155;">
            Built by Vikrant Thenge
        </div>
        <div style="margin-top:0.35rem; font-size:0.88rem;">
            <a href="https://www.linkedin.com/in/vthenge"
               target="_blank" rel="noopener noreferrer"
               style="text-decoration:none; margin:0 0.5rem;">
                LinkedIn ↗
            </a>
            <span style="color:#94a3b8;">|</span>
            <a href="https://github.com/Vikrantthenge"
               target="_blank" rel="noopener noreferrer"
               style="text-decoration:none; margin:0 0.5rem;">
                GitHub ↗
            </a>
        </div>
        <div style="margin-top:0.35rem; font-size:0.78rem; color:#64748b;">
            Airline Operations · Performance Analytics
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
