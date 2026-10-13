# Ground Turnaround Performance Dashboard

An airline operations analytics portfolio project built with **Python,
Streamlit, Pandas, and Plotly**, using a simulated dataset of 1,500
flight-turnaround records.

## View the dashboards

-   **Live interactive application:**
    <https://ground-turnaround-performance-analysis.streamlit.app/>
-   **Standalone dashboard preview:** [Open
    Dashboard_Preview.html](./Dashboard_Preview.html)

> **Data note:** The records and results are simulated for portfolio
> demonstration. They do not represent actual airline performance or
> verified cost savings. The HTML file is a standalone dashboard
> preview, not a native Power BI `.pbix` file.

## What the project demonstrates

-   Monitoring of turnaround variance, SLA breach rate, on-time
    performance, and departure delay.
-   Comparisons across stations, ground handlers, and scheduled time
    bands.
-   Interactive filtering and management-focused prompts for further
    investigation.
-   Translating operational measures into clear performance reporting.

## Key figures in the simulated dataset

-   **Records:** 1,500
-   **SLA breach rate:** approximately 45.7%
-   **On-time performance:** approximately 74.7%
-   **Average turnaround variance:** approximately +10.1 minutes

These are descriptive results from the synthetic dataset only. They
should not be presented as actual airline results. Differences between
stations, handlers, or time bands do not establish cause and effect.

## Technology

Python · Streamlit · Pandas · Plotly · CSV

## Run locally

Install Python 3.10 or later, then run these commands from the project
folder:

``` bash
py -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python -m streamlit run app.py
```

The dataset should remain in the `data/` folder as expected by `app.py`.

## Resume-ready summary

**Ground Turnaround Performance Dashboard \| Python, Streamlit, Pandas,
Plotly**

Developed and deployed an interactive operations dashboard using 1,500
simulated flight-turnaround records to monitor SLA compliance,
turnaround variance, on-time performance, and station-level trends.
Added interactive filters, comparative visualisations, and
management-oriented investigation prompts.

**Live demo:**
https://ground-turnaround-performance-analysis.streamlit.app/
