import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="King County Permits", layout="wide", page_icon="🏗️")

# ── Theme / CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    h1 { font-weight: 700 !important; font-size: 2rem !important; color: #1a1a2e !important; }
    h2, h3 { font-weight: 600 !important; color: #1a1a2e !important; }
    .block-container { padding-top: 2rem; }
    .stDataFrame { border-radius: 8px; overflow: hidden; }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #f8f9ff 0%, #eef1ff 100%);
        border: 1px solid #e0e4f2; border-radius: 12px; padding: 16px 20px;
    }
    div[data-testid="stMetric"] label { color: #555 !important; font-size: 13px !important; }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #1a1a2e !important; font-weight: 700 !important; }

    /* ── Modern tab styling ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: transparent;
        border-bottom: 2px solid #eee;
        padding-bottom: 0;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #6c757d !important;
        padding: 14px 24px !important;
        border-radius: 10px 10px 0 0 !important;
        border-bottom: 3px solid transparent !important;
        transition: all 0.2s ease;
        white-space: nowrap;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #4361ee !important;
        background: #f0f3ff;
    }
    .stTabs [aria-selected="true"] {
        font-weight: 700 !important;
        color: #4361ee !important;
        border-bottom: 3px solid #4361ee !important;
        background: #f0f3ff;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }
    .stTabs [data-baseweb="tab-border"] { display: none; }

    /* Lucide SVG icons via ::before on each tab */
    .stTabs [data-baseweb="tab"] p::before {
        content: "";
        display: inline-block;
        width: 18px; height: 18px;
        margin-right: 8px;
        vertical-align: -3px;
        background-size: contain;
        background-repeat: no-repeat;
    }
    /* Tab 1: clock (Durations) */
    .stTabs [data-baseweb="tab"]:nth-child(1) p::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%236c757d' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='10'/%3E%3Cpolyline points='12 6 12 12 16 14'/%3E%3C/svg%3E");
    }
    /* Tab 2: trending-up (Duration Trends) */
    .stTabs [data-baseweb="tab"]:nth-child(2) p::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%236c757d' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='22 7 13.5 15.5 8.5 10.5 2 17'/%3E%3Cpolyline points='16 7 22 7 22 13'/%3E%3C/svg%3E");
    }
    /* Tab 3: milestone (Milestones) */
    .stTabs [data-baseweb="tab"]:nth-child(3) p::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%236c757d' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M18 6H5a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h13l4-3.5L18 6Z'/%3E%3Cpath d='M12 13v8'/%3E%3Cpath d='M12 3v3'/%3E%3C/svg%3E");
    }
    /* Tab 4: calendar (Permits by Year) */
    .stTabs [data-baseweb="tab"]:nth-child(4) p::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%236c757d' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M8 2v4'/%3E%3Cpath d='M16 2v4'/%3E%3Crect width='18' height='18' x='3' y='4' rx='2'/%3E%3Cpath d='M3 10h18'/%3E%3C/svg%3E");
    }
    /* Tab 5: bar-chart-3 (Count by Type) */
    .stTabs [data-baseweb="tab"]:nth-child(5) p::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%236c757d' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='18' x2='18' y1='20' y2='10'/%3E%3Cline x1='12' x2='12' y1='20' y2='4'/%3E%3Cline x1='6' x2='6' y1='20' y2='14'/%3E%3C/svg%3E");
    }
    /* Active tab: recolor icons to primary blue */
    .stTabs [aria-selected="true"] p::before {
        filter: brightness(0) saturate(100%) invert(29%) sepia(93%) saturate(1352%) hue-rotate(218deg) brightness(101%) contrast(91%);
    }
""", unsafe_allow_html=True)

# ── Palette ────────────────────────────────────────────────────────────────────
PAL = {
    "primary": "#4361ee", "secondary": "#3a0ca3", "accent": "#f72585",
    "warn": "#f77f00", "success": "#06d6a0", "dark": "#1a1a2e",
    "gray": "#6c757d", "light": "#f8f9fa", "grid": "#eee",
}
COLORS = ["#4361ee", "#3a86ff", "#06d6a0", "#f77f00", "#f72585",
          "#7209b7", "#4cc9f0", "#ff006e", "#8338ec", "#fb5607",
          "#3a0ca3", "#4895ef"]

PLOTLY_LAYOUT = dict(
    plot_bgcolor="white",
    font=dict(family="Inter, sans-serif"),
    hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter, sans-serif", bordercolor="#ddd"),
    margin=dict(l=10, r=30, t=60, b=40),
)

# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("king-county-permits-matched.csv")
    for col in ["Application Date", "Open Date", "Intake Complete Date",
                "Ready to Issue Date", "Issued Date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    df["Year"] = df["Issued Date"].dt.year.astype("Int64")
    df["Month"] = df["Issued Date"].dt.to_period("M").astype(str)
    df["Type Label"] = (
        df["PERMIT TYPE"]
        .str.replace("Building/", "", regex=False)
        .str.replace("Fire/", "", regex=False)
        .str.replace("SiteDevCA/", "", regex=False)
        .str.replace("Engineering/", "", regex=False)
        .str.replace("Planning/", "", regex=False)
        .str.replace("/NA", "", regex=False)
    )
    # Group small categories (<=10 total) into "Other"
    type_counts = df["Type Label"].value_counts()
    small_types = type_counts[type_counts <= 10].index
    df["Type Group"] = df["Type Label"].where(~df["Type Label"].isin(small_types), "Other")
    return df

df = load_data()

DURATION_COLS = {
    "TOTAL: Intake Complete → Issued (99.9% data)": "Days - Intake Complete to Issued (total)",
    "Intake Complete → Ready to Issue":             "Days - Intake Complete to Ready to Issue",
    "Ready to Issue → Issued":                      "Days - Ready to Issue to Issued",
    "Open → Intake Complete (49% data)":            "Days - Open to Intake Complete",
    "TOTAL: Open → Issued (49% data)":              "Days - Open to Issued (total)",
}
_LIMITED_STAGES = {"Open → Intake Complete (49% data)", "TOTAL: Open → Issued (49% data)"}
YEARS        = sorted([int(y) for y in df["Year"].dropna().unique()])
YEAR_OPTIONS = ["All"] + [str(y) for y in YEARS]

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("King County Permit Dashboard")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Permits", f"{len(df):,}")
m2.metric("Permit Types", f"{df['Type Group'].nunique()}")
m3.metric("Date Range", "2023 – 2026")
# Exclude 0-day mechanical permits for a meaningful median
_nonzero = df.loc[df["Days - Intake Complete to Issued (total)"] > 0,
                  "Days - Intake Complete to Issued (total)"]
m4.metric("Median Days to Issue", f"{_nonzero.median():.0f} days",
          help="Median days from Intake Complete to Issued, excluding same-day permits")

st.write("")
tab3, tab4, tab5, tab2, tab1 = st.tabs(["Durations", "Duration Trends", "Milestones", "Permits by Year", "Count by Type"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Count by Permit Type
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    c1, c2, _ = st.columns([1, 1, 4])
    with c1:
        year_filter = st.selectbox("Year", YEAR_OPTIONS, key="t1_year")
    with c2:
        sort_by = st.radio("Sort by", ["Count", "Name"], key="t1_sort", horizontal=True)

    filtered = df.copy()
    if year_filter != "All":
        filtered = filtered[filtered["Year"] == int(year_filter)]

    counts = filtered.groupby("Type Group").size().reset_index(name="Count")
    if sort_by == "Name":
        counts = counts.sort_values("Type Group", ascending=True)
    else:
        counts = counts.sort_values("Count", ascending=True)

    title_year = f" — {year_filter}" if year_filter != "All" else " — All Years"

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        y=counts["Type Group"], x=counts["Count"],
        orientation="h",
        marker=dict(color=PAL["primary"], opacity=0.88),
        text=[f"{v:,}" for v in counts["Count"]],
        textposition="outside", textfont=dict(size=11, color=PAL["dark"]),
        hovertemplate="<b>%{y}</b><br>Count: %{x:,}<extra></extra>",
    ))
    fig1.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text=f"Permits by Type{title_year}",
                   font=dict(size=15, color=PAL["dark"])),
        xaxis=dict(title=dict(text="Number of Permits", font=dict(color=PAL["gray"])),
                   gridcolor=PAL["grid"], zeroline=False, tickfont=dict(color=PAL["gray"])),
        yaxis=dict(tickfont=dict(size=11, color=PAL["dark"])),
        height=max(380, len(counts) * 34),
        showlegend=False,
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.dataframe(
        counts.sort_values("Count", ascending=False)
              .rename(columns={"Type Group": "Permit Type"}),
        use_container_width=True, hide_index=True
    )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Timeline
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    c1, c2, c3, _ = st.columns([1, 1, 1, 2])
    with c1:
        view = st.radio("View by", ["Year", "Month"], key="t2_view", horizontal=True)
    with c2:
        top_n = st.slider("Top N types", 3, 12, 6, key="t2_topn")
    with c3:
        stack = st.checkbox("Stacked", value=True, key="t2_stack")

    top_types = df.groupby("Type Group").size().nlargest(top_n).index.tolist()
    if "Other" in top_types:
        top_types.remove("Other")
    tdf = df[df["Type Group"].isin(top_types)].copy()

    if view == "Year":
        grp = tdf.groupby(["Year", "Type Group"]).size().unstack(fill_value=0)
        grp.index = grp.index.astype(str)
    else:
        grp = tdf.groupby(["Month", "Type Group"]).size().unstack(fill_value=0).sort_index()

    fig2 = go.Figure()
    for i, col in enumerate(grp.columns):
        fig2.add_trace(go.Bar(
            x=grp.index.tolist(), y=grp[col],
            name=col, marker_color=COLORS[i % len(COLORS)],
            hovertemplate=f"<b>{col}</b><br>" + "%{x}<br>Count: %{y:,}<extra></extra>",
        ))

    fig2.update_layout(
        **PLOTLY_LAYOUT,
        barmode="stack" if stack else "group",
        title=dict(text=f"Permits by {view} — Top {top_n} Types",
                   font=dict(size=15, color=PAL["dark"])),
        xaxis=dict(tickfont=dict(color=PAL["gray"])),
        yaxis=dict(title=dict(text="Permits", font=dict(color=PAL["gray"])),
                   gridcolor=PAL["grid"], zeroline=False, tickfont=dict(color=PAL["gray"])),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
                    font=dict(size=12)),
        height=500,
    )
    st.plotly_chart(fig2, use_container_width=True)

    if view == "Year":
        pivot = df.groupby(["Type Group", "Year"]).size().unstack(fill_value=0).reset_index()
        pivot.columns = ["Permit Type"] + [str(int(c)) for c in pivot.columns[1:]]
        pivot["Total"] = pivot.iloc[:, 1:].sum(axis=1)
        st.dataframe(pivot.sort_values("Total", ascending=False), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Durations
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    c1, c2, _ = st.columns([1, 1, 3])
    with c1:
        year_filter3 = st.selectbox("Year", YEAR_OPTIONS, key="t3_year")
    with c2:
        dur_label = st.selectbox("Stage", list(DURATION_COLS.keys()), key="t3_dur")

    if dur_label in _LIMITED_STAGES:
        st.warning("⚠️ **Open Date** is only available for permits before July 2024 (~49% of records). "
                   "Results here cover roughly half the dataset. Use *Intake Complete → Issued* for full coverage.")

    dur_col = DURATION_COLS[dur_label]
    filtered3 = df.copy()
    if year_filter3 != "All":
        filtered3 = filtered3[filtered3["Year"] == int(year_filter3)]
    filtered3 = filtered3[filtered3[dur_col].notna()]

    summary = (
        filtered3.groupby("Type Group")[dur_col]
        .agg(Count="count", Min="min", Average="mean", Median="median",
             P75=lambda x: x.quantile(0.75),
             P90=lambda x: x.quantile(0.90),
             Max="max")
        .round(1).reset_index()
        .rename(columns={"Type Group": "Permit Type"})
        .sort_values("Count", ascending=False)
    )

    chart_df = summary.nlargest(15, "Count").sort_values("Median", ascending=True)
    yr = year_filter3 if year_filter3 != "All" else "All Years"

    # Build shared hover text for each row
    hover_text = [
        f"<b>{row['Permit Type']}</b><br>"
        f"Count: {int(row['Count']):,}<br>"
        f"Min: {row['Min']:.0f}d &nbsp;|&nbsp; Median: {row['Median']:.0f}d<br>"
        f"Average: {row['Average']:.0f}d &nbsp;|&nbsp; P75: {row['P75']:.0f}d<br>"
        f"P90: {row['P90']:.0f}d &nbsp;|&nbsp; Max: {row['Max']:.0f}d"
        for _, row in chart_df.iterrows()
    ]

    fig3 = go.Figure()

    # Median bars
    fig3.add_trace(go.Bar(
        y=chart_df["Permit Type"], x=chart_df["Median"],
        orientation="h", name="Median",
        marker=dict(color=PAL["primary"], opacity=0.88, line=dict(width=0)),
        hovertext=hover_text, hoverinfo="text",
    ))
    # Average dots
    fig3.add_trace(go.Scatter(
        y=chart_df["Permit Type"], x=chart_df["Average"],
        mode="markers", name="Average",
        marker=dict(color=PAL["warn"], size=10, line=dict(color="white", width=1.5)),
        hovertext=hover_text, hoverinfo="text",
    ))
    # P90 diamonds
    fig3.add_trace(go.Scatter(
        y=chart_df["Permit Type"], x=chart_df["P90"],
        mode="markers", name="P90",
        marker=dict(color=PAL["accent"], size=10, symbol="diamond",
                    line=dict(color="white", width=1.5)),
        hovertext=hover_text, hoverinfo="text",
    ))

    fig3.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text=f"{dur_label}  ·  {yr}  ·  n={len(filtered3):,}",
                   font=dict(size=15, color=PAL["dark"])),
        xaxis=dict(title=dict(text="Days", font=dict(color=PAL["gray"])),
                   gridcolor="#eee", zeroline=False,
                   tickfont=dict(color=PAL["gray"])),
        yaxis=dict(tickfont=dict(size=11, color=PAL["dark"])),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(size=12)),
        height=max(380, len(chart_df) * 38),
        barmode="overlay",
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.dataframe(summary, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — Duration Trends (Year over Year)
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    c1, c2, _ = st.columns([1, 1, 3])
    with c1:
        dur_label4 = st.selectbox("Stage", list(DURATION_COLS.keys()), key="t4_dur")
    with c2:
        top_n4 = st.slider("Top N types", 3, 10, 6, key="t4_topn")

    if dur_label4 in _LIMITED_STAGES:
        st.warning("⚠️ **Open Date** is only available for permits before July 2024 (~49% of records). "
                   "2024 and 2025 data is incomplete for this stage. Use *TOTAL: Intake Complete → Issued* for full coverage.")

    dur_col4 = DURATION_COLS[dur_label4]
    tdf4 = df[df[dur_col4].notna() & df["Year"].notna()].copy()
    tdf4 = tdf4[tdf4["Year"].isin([2023, 2024, 2025])]  # full years only

    # Only consider permit types with 90+ permits in the entire dataset
    _type_counts4 = df.groupby("Type Group").size()
    _eligible4 = _type_counts4[(_type_counts4 >= 90) & (_type_counts4.index != "Other")].index
    tdf4 = tdf4[tdf4["Type Group"].isin(_eligible4)]
    top_types4 = tdf4.groupby("Type Group").size().nlargest(top_n4).index.tolist()
    tdf4 = tdf4[tdf4["Type Group"].isin(top_types4)]

    years_list = [2023, 2024, 2025]
    metrics = ["Median", "Average", "P75", "P90"]
    agg_funcs = {
        "Median": "median", "Average": "mean",
        "P75": lambda x: x.quantile(0.75),
        "P90": lambda x: x.quantile(0.90),
    }

    fig4 = make_subplots(rows=2, cols=2, subplot_titles=metrics,
                         horizontal_spacing=0.08, vertical_spacing=0.12)

    # Track which types have been added to legend (only show once)
    legend_shown = set()

    for idx, metric_name in enumerate(metrics):
        row = idx // 2 + 1
        col = idx % 2 + 1
        agg_func = agg_funcs[metric_name]

        pivot = tdf4.groupby(["Year", "Type Group"])[dur_col4].agg(agg_func).unstack()
        pivot = pivot.loc[pivot.index.isin(years_list)]

        for i, ptype in enumerate(pivot.columns):
            vals = pivot[ptype].values
            show_legend = ptype not in legend_shown
            legend_shown.add(ptype)

            fig4.add_trace(go.Scatter(
                x=[str(y) for y in pivot.index.astype(int)],
                y=vals,
                mode="lines+markers",
                name=ptype,
                legendgroup=ptype,
                showlegend=show_legend,
                line=dict(color=COLORS[i % len(COLORS)], width=2.5),
                marker=dict(size=8, line=dict(color="white", width=1.5)),
                hovertemplate=(
                    f"<b>{ptype}</b><br>"
                    f"{metric_name}: " + "%{y:.0f} days<br>"
                    "Year: %{x}<extra></extra>"
                ),
            ), row=row, col=col)

    fig4.update_layout(
        plot_bgcolor="white",
        font=dict(family="Inter, sans-serif"),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter, sans-serif", bordercolor="#ddd"),
        title=dict(text=f"{dur_label4}  ·  Year-over-Year Trend",
                   font=dict(size=15, color=PAL["dark"])),
        height=700,
        legend=dict(orientation="h", yanchor="top", y=-0.06, xanchor="center", x=0.5,
                    font=dict(size=12)),
        margin=dict(l=50, r=30, t=80, b=80),
    )

    # Style all subplots
    for i in range(1, 5):
        fig4.update_xaxes(tickfont=dict(color=PAL["gray"]), row=(i-1)//2+1, col=(i-1)%2+1)
        fig4.update_yaxes(title=dict(text="Days", font=dict(color=PAL["gray"], size=10)),
                          gridcolor=PAL["grid"], zeroline=False,
                          tickfont=dict(color=PAL["gray"]),
                          row=(i-1)//2+1, col=(i-1)%2+1)

    st.plotly_chart(fig4, use_container_width=True)

    # Also show the numbers in a table
    trend_data = []
    for metric_name in metrics:
        agg_func = agg_funcs[metric_name]
        for tg in top_types4:
            for yr in years_list:
                subset = tdf4[(tdf4["Type Group"] == tg) & (tdf4["Year"] == yr)][dur_col4]
                if len(subset) > 0:
                    trend_data.append({
                        "Permit Type": tg, "Year": yr, "Metric": metric_name,
                        "Days": round(agg_func(subset) if callable(agg_func) else getattr(subset, agg_func)(), 1)
                    })

    trend_df = pd.DataFrame(trend_data)
    if len(trend_df) > 0:
        pivot_display = trend_df.pivot_table(index=["Permit Type", "Metric"], columns="Year", values="Days")
        pivot_display = pivot_display.reset_index()
        pivot_display.columns = [str(c) for c in pivot_display.columns]
        st.dataframe(pivot_display, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — Milestone Breakdown (Pre vs Post June 2024)
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("##### Average duration breakdown by milestone for the **top 7 longest permit types** (≥ 90 permits)")

    cutoff = pd.Timestamp("2024-06-01")

    # Stage definitions (name, column)
    STAGE_OPEN_IC = ("Open → Intake Complete",         "Days - Open to Intake Complete")
    STAGE_IC_RTI  = ("Intake Complete → Ready to Issue","Days - Intake Complete to Ready to Issue")
    STAGE_RTI_ISS = ("Ready to Issue → Issued",        "Days - Ready to Issue to Issued")

    STAGE_COLORS = {
        "Open → Intake Complete":           "#7209b7",
        "Intake Complete → Ready to Issue": "#4361ee",
        "Ready to Issue → Issued":          "#06d6a0",
    }

    # Top 7 by mean total duration (Intake Complete → Issued – 99.9% data)
    # Only include permit types with 90+ permits in the entire dataset
    _total_col = "Days - Intake Complete to Issued (total)"
    _type_counts5 = df.groupby("Type Group").size()
    _eligible5 = _type_counts5[(_type_counts5 >= 90) & (_type_counts5.index != "Other")].index
    _rank_df = df[(df[_total_col].notna()) & (df["Type Group"].isin(_eligible5))]
    top7 = (
        _rank_df
        .groupby("Type Group")[_total_col]
        .mean()
        .nlargest(7)
        .index.tolist()
    )

    # Split by period
    pre_df  = df[df["Issued Date"] < cutoff].copy()
    post_df = df[df["Issued Date"] >= cutoff].copy()

    def _stage_means(data, types, stages):
        """Compute mean days per stage for each permit type."""
        means, counts = {}, {}
        for tg in types:
            sub = data[data["Type Group"] == tg]
            counts[tg] = len(sub)
            means[tg] = {}
            for name, col in stages:
                vals = sub[col].dropna()
                means[tg][name] = vals.mean() if len(vals) > 0 else 0
        return means, counts

    pre_stages  = [STAGE_OPEN_IC, STAGE_IC_RTI, STAGE_RTI_ISS]
    post_stages = [STAGE_IC_RTI, STAGE_RTI_ISS]

    pre_means,  pre_counts  = _stage_means(pre_df,  top7, pre_stages)
    post_means, post_counts = _stage_means(post_df, top7, post_stages)

    # ── Build side-by-side subplots ──
    fig5 = make_subplots(
        rows=1, cols=2,
        subplot_titles=[
            "Pre June 2024 · Open → Issued",
            "Post June 2024 · Intake Complete → Issued",
        ],
        shared_yaxes=True,
        horizontal_spacing=0.10,
    )

    y_labels = list(reversed(top7))  # longest at top
    legend_shown = set()

    # --- Left chart: Pre-June 2024 (3 segments) ---
    for stage_name, _ in pre_stages:
        x_vals = [max(pre_means[tg][stage_name], 0) for tg in y_labels]
        hover = [
            f"<b>{tg}</b><br>"
            f"<b>{stage_name}</b>: {pre_means[tg][stage_name]:.0f} days<br>"
            f"Total: {sum(pre_means[tg].values()):.0f} days<br>"
            f"n = {pre_counts[tg]:,}"
            for tg in y_labels
        ]
        show_leg = stage_name not in legend_shown
        legend_shown.add(stage_name)
        fig5.add_trace(go.Bar(
            y=y_labels, x=x_vals,
            name=stage_name, orientation="h",
            marker_color=STAGE_COLORS[stage_name],
            legendgroup=stage_name, showlegend=show_leg,
            text=[f"{v:.0f}d" if v >= 15 else "" for v in x_vals],
            textposition="inside",
            textfont=dict(size=11, color="white", family="Inter, sans-serif"),
            hovertext=hover, hoverinfo="text",
        ), row=1, col=1)

    # Total annotations (right of pre bars)
    pre_totals = [sum(pre_means[tg].values()) for tg in y_labels]
    fig5.add_trace(go.Scatter(
        y=y_labels, x=[t + 8 for t in pre_totals],
        mode="text", text=[f"<b>{t:.0f}d</b>" for t in pre_totals],
        textfont=dict(size=11, color=PAL["dark"], family="Inter, sans-serif"),
        textposition="middle right", showlegend=False, hoverinfo="skip",
    ), row=1, col=1)

    # --- Right chart: Post-June 2024 (2 segments) ---
    for stage_name, _ in post_stages:
        x_vals = [max(post_means[tg].get(stage_name, 0), 0) for tg in y_labels]
        hover = [
            f"<b>{tg}</b><br>"
            f"<b>{stage_name}</b>: {post_means[tg].get(stage_name, 0):.0f} days<br>"
            f"Total: {sum(post_means[tg].values()):.0f} days<br>"
            f"n = {post_counts[tg]:,}"
            for tg in y_labels
        ]
        show_leg = stage_name not in legend_shown
        legend_shown.add(stage_name)
        fig5.add_trace(go.Bar(
            y=y_labels, x=x_vals,
            name=stage_name, orientation="h",
            marker_color=STAGE_COLORS[stage_name],
            legendgroup=stage_name, showlegend=show_leg,
            text=[f"{v:.0f}d" if v >= 15 else "" for v in x_vals],
            textposition="inside",
            textfont=dict(size=11, color="white", family="Inter, sans-serif"),
            hovertext=hover, hoverinfo="text",
        ), row=1, col=2)

    # Total annotations (right of post bars)
    post_totals = [sum(post_means[tg].values()) for tg in y_labels]
    fig5.add_trace(go.Scatter(
        y=y_labels, x=[t + 8 for t in post_totals],
        mode="text", text=[f"<b>{t:.0f}d</b>" for t in post_totals],
        textfont=dict(size=11, color=PAL["dark"], family="Inter, sans-serif"),
        textposition="middle right", showlegend=False, hoverinfo="skip",
    ), row=1, col=2)

    fig5.update_layout(
        plot_bgcolor="white",
        font=dict(family="Inter, sans-serif"),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter, sans-serif", bordercolor="#ddd"),
        barmode="stack",
        title=dict(
            text="Milestone Breakdown — Top 7 Permit Types by Duration (Average Days)",
            font=dict(size=15, color=PAL["dark"]),
        ),
        legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5,
                    font=dict(size=12)),
        height=580,
        margin=dict(l=10, r=50, t=100, b=110),
    )

    # Make subplot titles larger and bolder
    fig5.update_annotations(font=dict(size=15, color=PAL["dark"], family="Inter, sans-serif"))

    for c in [1, 2]:
        fig5.update_xaxes(
            title=dict(text="Days", font=dict(color=PAL["gray"], size=12)),
            gridcolor=PAL["grid"], zeroline=False,
            tickfont=dict(color=PAL["gray"]),
            row=1, col=c,
        )
    fig5.update_yaxes(tickfont=dict(size=11, color=PAL["dark"]), row=1, col=1)

    st.plotly_chart(fig5, use_container_width=True)

    # ── Summary table ──
    table_rows = []
    for tg in top7:
        pre_total  = sum(pre_means[tg].values())
        post_total = sum(post_means[tg].values())
        table_rows.append({
            "Permit Type": tg,
            "Pre: Open→IC (days)":   round(pre_means[tg].get("Open → Intake Complete", 0)),
            "Pre: IC→RTI (days)":    round(pre_means[tg].get("Intake Complete → Ready to Issue", 0)),
            "Pre: RTI→Iss (days)":   round(pre_means[tg].get("Ready to Issue → Issued", 0)),
            "Pre: Total":            round(pre_total),
            "Post: IC→RTI (days)":   round(post_means[tg].get("Intake Complete → Ready to Issue", 0)),
            "Post: RTI→Iss (days)":  round(post_means[tg].get("Ready to Issue → Issued", 0)),
            "Post: Total":           round(post_total),
            "n (Pre)":  pre_counts[tg],
            "n (Post)": post_counts[tg],
        })
    st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)
