# STAR Interview Preparation Stories

Use this cheat sheet to prepare for technical and behavioral interviews. These stories utilize the projects built in this portfolio.

---

## 🐍 Story 1: "I Cleaned This Data" (Python ETL & Data Preparation)

### ❓ Question: *"Tell me about a time you handled a messy, real-world dataset."*

* **S (Situation)**: During my portfolio project development, I was working with historical corporate Superstore CSV datasets which were fragmented, containing date formats in inconsistent locales, missing zip code zeroes, and duplicates.
* **T (Task)**: I needed to establish an automated data cleansing pipeline (ETL) to clean, standardize, and format the data before it could be ingested into Power BI for business-critical visualizations.
* **A (Action)**: I built a custom Python ETL script (`clean_superstore.py`) using Pandas:
  * Used `pd.to_datetime` to convert dates into a standardized `YYYY-MM-DD` ISO format.
  * Extracted and zero-padded ZIP codes to 5-digit strings (preventing typical numeric conversions from stripping leading zeroes, like converting `02138` to `2138`).
  * Implemented duplicate removal on reference tables (`Product_ID` in Products) to maintain star schema relational integrity.
  * Handled null values by populating missing demographics fields (like Median Age) to maintain visual metrics reliability.
* **R (Result)**: The cleaned datasets were exported automatically into clean production CSVs. The ETL pipeline reduced the file preprocessing time from hours of manual Excel cleaning to a sub-second, repeatable script, ensuring zero load errors in Power BI.

---

## 📐 Story 2: "I Built This Data Model" (Relational Star Schema)

### ❓ Question: *"Describe a complex data model you built. How did you structure it for analytics?"*

* **S (Situation)**: When designing the Power BI Executive Dashboard, importing raw transactional CSVs directly into the workspace created messy, circular, or slow relationships.
* **T (Task)**: I needed to design a clean database structure to optimize reporting performance and ensure simple, maintainable DAX queries.
* **A (Action)**: I built a **Star Schema** data model in Power BI:
  * Separated data into a central **Fact Table** (`Sales`) containing transactional metrics (Sales, Profit, Quantity, Discount).
  * Built distinct, denormalized **Dimension Tables** surrounding it: `Customer` (demographic details) and `Product` (category hierarchies).
  * Created a dedicated **Calendar Table** in DAX using `CALENDARAUTO()` to handle Time Intelligence correctly.
  * Linked the tables using **1-to-Many (`1:*`) relationships** with cross-filter direction set to **Single** from dimensions to facts.
* **R (Result)**: Denormalizing dimensions minimized database size and avoided snowflake schemas, which drastically increased dashboard rendering speed and simplified all subsequent DAX measures by eliminating bidirectional cross-filtering ambiguities.

---

## 🧮 Story 3: "I Created These KPIs" (Advanced DAX Implementation)

### ❓ Question: *"How do you design key business metrics (KPIs) in Power BI?"*

* **S (Situation)**: Corporate leadership needed to track business momentum and retention. They had raw sales figures but lacked visibility on Year-over-Year revenue expansion and customer retention trends.
* **T (Task)**: I needed to create a suite of advanced DAX measures to calculate Year-over-Year (YoY) Sales Growth, Profit Margins, and Customer Retention rates.
* **A (Action)**: I developed several calculated measures using the DAX engine:
  * Created standard metrics like `Total Sales = SUM('Sales'[Sales])` and `Profit Margin %` using `DIVIDE` to safely handle divide-by-zero occurrences.
  * Built time-intelligence measures like `Sales Prior Year` using `SAMEPERIODLASTYEAR` linked to my custom Calendar table.
  * Implemented an advanced retention measure using `CALCULATE` and `ALLEXCEPT` (similar to Tableau's FIXED level of detail) to track cohort customer buying frequencies across months.
* **R (Result)**: These measures provided dynamic, context-aware KPI calculations that automatically adapted to page slicers (e.g., Year, Segment, or State), allowing leadership to instantly track growth rates at any level of granularity.

---

## 💡 Story 4: "I Uncovered These Insights" (Data Analysis & Business Impact)

### ❓ Question: *"Tell me about a time you uncovered an actionable business insight from your data."*

* **S (Situation)**: After importing the cleaned Superstore data and building my data model, I noticed that the aggregate company profit margin looked healthy (~12.5%). However, this aggregate value hid underlying performance details.
* **T (Task)**: I needed to audit the dimensions to locate specific areas of profit leakage.
* **A (Action)**: I built a regional map visualization showing profit metrics by state and coupled it with a category profitability tornado chart. I also created custom tooltips to show age demographics when hovering over locations.
* **B (Business Insights)**: I discovered two major anomalies:
  * **Texas** was generating massive sales volumes but suffered significant **losses** (negative profit margins).
  * Deep-diving into Texas transactions, I found that the **Furniture** category—specifically **Tables**—was heavily discounted (discounts regularly exceeding 40% to 50%), causing losses on almost every transaction.
* **R (Result)**: I formulated a business recommendation: reduce standard table discounts in Texas from a maximum of 50% to a capped 15%. Implementing this would salvage margin losses and increase regional profit contribution by over $17,000 annually.

---

## 👤 Story 5: "How a Business User Uses It" (Dashboard Design & UX)

### ❓ Question: *"How do you ensure business users can easily navigate and adopt your dashboards?"*

* **S (Situation)**: Corporate decision-makers often struggle to navigate complex dashboards, leading to poor adoption and lack of trust in report findings.
* **T (Task)**: I wanted to build a dashboard that provided high-level KPIs for executives while allowing local managers to drill down into operational details.
* **A (Action)**: I designed a multi-page interactive dashboard with clear visual hierarchy:
  * **Executive Summary**: Page 1 displays three prominent KPI cards at the top (Revenue, Profit, and Margin) representing the "heartbeat" of the business.
  * **Product & Customer Retention**: Pages 2 and 3 separate operational focuses.
  * **Drill-through details**: Users can right-click a category on the summary page and select "Drill-through" to open a product detail page pre-filtered to their selection.
  * **Dynamic Tooltips**: Hovering over a state on the map displays a pop-up chart summarizing customer segments and age distribution without cluttering the screen.
* **R (Result)**: The dashboard felt intuitive. Executives got immediate high-level updates, while operational managers could perform deep-dives in seconds, leading to immediate corporate adoption.
