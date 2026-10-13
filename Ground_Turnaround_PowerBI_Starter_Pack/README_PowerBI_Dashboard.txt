GROUND TURNAROUND PERFORMANCE - POWER BI STARTER PACK

Included:
- ground_turnaround_simulated_dataset.csv: 1,500 synthetic records
- ground_turnaround_powerbi_theme.json: import via View > Themes > Browse for themes
- ground_turnaround_dax_measures.txt: measures to add after importing data
- Ground_Turnaround_PowerBI_Dashboard_Preview.html: interactive visual preview, with station/handler/time-band filters

Build the native report in Power BI Desktop:
1. Get Data > Text/CSV, import ground_turnaround_simulated_dataset.csv.
2. Rename the table to Turnaround.
3. Set operation_date to Date, flags to Whole Number, KPI measures as shown in the DAX file.
4. View > Themes > Browse for themes, select the theme JSON.
5. Create a 16:9 report page with:
   - KPI cards: Flights Analysed, Average Turnaround Variance, SLA Breach Rate, OTP Rate
   - Bar chart: Station vs SLA Breach Rate, descending
   - Bar chart: Time Band vs SLA Breach Rate
   - Bar chart: Handler vs SLA Breach Rate
   - Table: Station, Flights Analysed, Average Turnaround Variance, SLA Breach Rate, OTP Rate
   - Slicers: Station, Handler, Time Band, Operation Date
6. Add a second page for driver investigation only after showing driver flags as overlapping exploratory indicators, not confirmed causes.

Important synthetic definitions:
- SLA target = planned turnaround + 10 minutes.
- OTP = departure delay <= 15 minutes.
- All records and results are synthetic.
- Delay driver flags may overlap. Do not present them as causal root causes.
- estimated_delay_cost_inr is a synthetic proxy, not actual savings or a validated cost model.

The HTML file is a standalone interactive preview, not a Power BI PBIX file. A native PBIX file must be assembled and saved in Power BI Desktop.
