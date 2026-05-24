from datetime import datetime, timedelta

import matplotlib.dates as mdates
import numpy as np
import streamlit as st
from matplotlib.axes import Axes
from matplotlib.colorbar import Colorbar
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure
from matplotlib.image import AxesImage
from matplotlib.pyplot import subplots, tight_layout

FREQ_MIN_GHZ = 0.830
FREQ_MAX_GHZ = 0.930

V_MIN_DB = -130
V_MAX_DB = -70

TIME_STEP_SECONDS = 1


def load_waterfall_from_file(path: str):
    rows = []

    with open(path, "r") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            try:
                line = line.strip("[]")

                parts = line.split(";")

                row = np.array([float(x.strip()) for x in parts if x.strip() != ""])

                if len(row) > 0:
                    rows.append(row)

            except Exception:
                continue

    if not rows:
        return np.array([]), []

    min_len = min(len(r) for r in rows)
    rows = [r[:min_len] for r in rows]

    data = np.vstack(rows)

    start_time = datetime.now()

    timestamps = [
        start_time + timedelta(seconds=i * TIME_STEP_SECONDS) for i in range(len(rows))
    ]

    return data, timestamps


def draw_waterfall(file_path: str) -> None:
    data, timestamps = load_waterfall_from_file(file_path)

    if data.size == 0:
        st.error("Brak danych do wyświetlenia.")
        return

    n_time, n_freq = data.shape

    frequencies = np.linspace(FREQ_MIN_GHZ, FREQ_MAX_GHZ, n_freq)

    time_nums = mdates.date2num(timestamps)

    fig: Figure
    ax: Axes

    fig, ax = subplots(figsize=(14, 7))

    im: AxesImage = ax.imshow(
        data,
        extent=[
            frequencies[0],
            frequencies[-1],
            time_nums[0],
            time_nums[-1],
        ],
        aspect="auto",
        origin="lower",
        cmap="jet",
        vmin=V_MIN_DB,
        vmax=V_MAX_DB,
    )

    ax.yaxis_date()
    ax.yaxis.set_major_formatter(DateFormatter("%H:%M:%S"))

    ax.set_title("RF Waterfall Plot")

    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("Time")

    cbar: Colorbar = fig.colorbar(im, ax=ax, pad=0.02)

    ticks = np.arange(V_MIN_DB, V_MAX_DB + 1, 10)

    cbar.set_ticks(ticks)
    cbar.ax.set_yticklabels([f"{x} dB" for x in ticks])

    tight_layout()

    st.pyplot(fig)


draw_waterfall("datasets-good/garden.txt")
