# Ground Turnaround Performance Dashboard

An interactive airline-operations analytics portfolio project built with
**Python, Streamlit, Pandas, and Plotly**. It examines simulated
ground-turnaround performance across stations, ground handlers, and time
bands.

> **Data disclaimer:** The included dataset is simulated. It does not
> represent actual airline performance, and any cost field is a
> synthetic proxy---not validated savings or a financial forecast.

## Dashboard capabilities

-   Filter by operation date, station, ground handler, and time band.
-   Monitor flights analysed, SLA breach rate, on-time performance,
    average turnaround variance, and average departure delay.
-   Compare SLA breach rates by station, time band, and handler.
-   Review daily performance trends.
-   Inspect station-level KPI detail.
-   Explore overlapping delay-driver flags as investigation leads, not
    proven causes.
-   Download the currently filtered records as CSV.

## Run locally

1.  Install Python 3.10 or later.

2.  Open a terminal in this project folder.

3.  Create and activate a virtual environment (recommended).

4.  Install dependencies:

    ``` bash
    pip install -r requirements.txt
    ```

5.  Launch the dashboard:

    ``` bash
    streamlit run app.py
    ```

The dashboard should open in your browser. If it does not, open the
local URL printed in the terminal.

## Project structure

``` text
ground-turnaround-performance-analysis/
├── app.py
├── requirements.txt
├── README.md
└── data/
    ├── ground_turnaround_simulated_dataset.csv
    └── ground_turnaround_data_dictionary.csv
```

## KPI definitions

-   **Turnaround variance:** actual turnaround minus planned turnaround,
    in minutes.
-   **SLA breach rate:** share of records where `sla_breach_flag = 1`,
    as defined in the simulated source data.
-   **On-time performance:** share of records whose source `otp_status`
    label is `On time`.
-   **Average departure delay:** mean of `departure_delay_min` for the
    filtered records.

The simulated SLA definition is based on planned turnaround plus a
10-minute tolerance. The source OTP label uses a departure-delay
threshold of 15 minutes. These are exercise assumptions, not a statement
of any airline's official definitions.

## Analytical cautions

-   The dataset is synthetic; observed patterns are demonstrations, not
    operational evidence.
-   Delay-driver flags can overlap. Flagged-vs-unflagged differences are
    associations, not causal effects.
-   Handler and station comparisons can be affected by operating mix,
    aircraft type, time band, weather, and other factors.
-   Do not present the simulated estimated delay cost as realised
    savings.
-   Validate data definitions, timestamp quality, sample sizes, and
    operational context before making decisions.

## Suggested next improvements

1.  Add a native Power BI `.pbix` file if building the report in Power
    BI Desktop.
2.  Add a documented analysis of operational hypotheses and validation
    checks.
3.  Deploy the Streamlit app and add its public demo URL here.
4.  Replace the simulated data only if authorised, appropriately
    anonymised operational data becomes available.

## Portfolio description

**Ground Turnaround Performance Dashboard \| Python, Streamlit, Pandas,
Plotly**

Built an interactive operations dashboard using a simulated dataset of
1,500 turnaround records to monitor SLA adherence, turnaround variance,
on-time performance, and station/handler patterns. Added filtering,
trend analysis, downloadable records, and explicit analytical caveats to
support evidence-led operational investigation.
