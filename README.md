# Ground Turnaround Performance Analysis

An interactive airline operations analytics portfolio project built with
**Python, Streamlit, Pandas, and Plotly**, supported by a standalone
HTML dashboard preview and Power BI starter files.

> **Important data note:** The dataset is simulated and is not sourced
> from a real airline. Findings are illustrative, not verified
> operational results or proven cost savings.

## Explore the dashboards

-   **Live Streamlit dashboard:** [Open the interactive
    application](https://ground-turnaround-performance-analysis.streamlit.app/)
-   **Standalone HTML preview:** [Open
    `Dashboard-preview.html`]([View Interactive Dashboard Preview](./Dashboard_Preview.html))

The Streamlit application is the primary live demo. The HTML file is a
separate, standalone preview; it is **not** a native Power BI `.pbix`
report. If the HTML file in your repository has a different filename or
is inside a subfolder, update the link above to match its actual GitHub
path.

## Business objective

Demonstrate how an operations leader can use performance data to monitor
ground turnaround, identify where SLA breaches are concentrated, compare
station and ground-handler performance, and prioritise operational
investigation.

## Dashboard features

-   KPI cards for flight volume, SLA breach rate, on-time performance,
    average turnaround variance, and average departure delay.
-   Interactive filtering by date, station, ground handler, and time
    band.
-   Comparative charts for station, time-band, and handler performance.
-   Daily performance trend.
-   Station performance summary table.
-   Descriptive comparisons of delay-driver flags to support further
    investigation.
-   Download of filtered records from the Streamlit app.

## Dataset and KPI definitions

The exercise uses 1,500 simulated turnaround records.

-   **Turnaround variance:** actual turnaround minus planned turnaround,
    in minutes.
-   **SLA breach rate:** share of records where `sla_breach_flag = 1`,
    according to the simulated source definition.
-   **On-time performance:** share of records whose `otp_status` is
    `On time`.
-   **Average departure delay:** average of `departure_delay_min` for
    the selected records.

The synthetic SLA target uses planned turnaround plus a 10-minute
tolerance. The source OTP label uses a departure-delay threshold of 15
minutes. These are exercise assumptions, not official airline-wide
standards.

## Key analytical observations

In the full simulated dataset, the overall SLA breach rate is
approximately **45.7%**, on-time performance is **74.7%**, and average
turnaround variance is approximately **+10.1 minutes**. These figures
describe only the synthetic dataset and must not be presented as actual
airline performance.

The dashboard helps identify segments for investigation. It does not
prove that a station, handler, time band, or delay flag caused a result.

## Technology

-   Python
-   Streamlit
-   Pandas
-   Plotly
-   CSV-based simulated data
-   Optional Power BI supporting assets: DAX measures and theme JSON

## Run locally

1.  Install Python 3.10 or later.

2.  Open a terminal in the repository folder.

3.  Create and activate a virtual environment (recommended):

    ``` bash
    py -m venv .venv
    .venv\\Scripts\\activate
    ```

4.  Install dependencies:

    ``` bash
    pip install -r requirements.txt
    ```

5.  Start the application:

    ``` bash
    python -m streamlit run app.py
    ```

Keep the dataset in the `data/` folder as expected by `app.py`.

## Suggested repository structure

``` text
ground-turnaround-performance-analysis/
├── app.py
├── requirements.txt
├── README.md
├── Dashboard-preview.html
└── data/
    ├── ground_turnaround_simulated_dataset.csv
    └── ground_turnaround_data_dictionary.csv
```

If you have included additional files such as the Power BI theme, DAX
measures, or case-study presentation, keep them in the repository and
add links to them here.

## Analytical limitations

-   All records are simulated; results are not operational evidence.
-   Delay-driver flags can overlap. Flagged-vs-unflagged comparisons are
    descriptive associations, not proof of causation.
-   Station and handler comparisons can be affected by flight mix,
    aircraft type, weather, traffic, staffing, and other operating
    conditions.
-   Do not describe the synthetic estimated delay-cost field as realised
    savings.
-   Validate data definitions, timestamps, sample sizes, and operational
    context before using any analysis for real decisions.

## Portfolio summary

**Ground Turnaround Performance Dashboard \| Python, Streamlit, Pandas,
Plotly**

Developed an interactive operations dashboard using 1,500 simulated
flight-turnaround records to monitor SLA adherence, turnaround variance,
on-time performance, and station-level trends. Implemented filters,
comparative visualisations, trend monitoring, downloadable records, and
management-oriented investigation prompts.

-   Live application:
    https://ground-turnaround-performance-analysis.streamlit.app/
-   HTML preview: `dashboard-preview.html` in this repository.
