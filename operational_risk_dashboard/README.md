# 🏦 American Express GMNS | Enterprise Operational Risk & Regulatory Issues Intelligence Dashboard

[![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](operational_risk_dashboard/Enterprise_Operational_Risk_Dashboard.pbix)
[![DAX](https://img.shields.io/badge/DAX-Data_Analysis_Expressions-002663?style=for-the-badge)](operational_risk_dashboard/README.md)
[![Regulatory Data](https://img.shields.io/badge/CFPB-62K+_Records-059669?style=for-the-badge)](https://www.consumerfinance.gov/)

An end-to-end Operational Risk and Governance Analytics Dashboard engineered for **American Express Global Merchant & Network Services (GMNS) - Global Governance, Risk, Remediation & Operations (GRRO)** team.

---

## 🎯 Executive Summary & Business Problem
In enterprise payment network operations and merchant acquiring, operational breakdowns—such as merchant settlement batch timeouts, KYC verification backlogs, fee schedule miscalculations, and payment gateway latency—pose substantial regulatory, financial, and reputational risks.

This solution translates **62,516 real-world financial services complaint records** from the U.S. Consumer Financial Protection Bureau (CFPB) database into automated executive Key Risk Indicators (KRIs), root cause thematic insights, and remediation monitoring.

---

## 📊 Core Key Risk Indicators (KRIs)

| Metric | Value | Description & Formula |
| :--- | :---: | :--- |
| **Filtered Issue Volume** | **3,000** | `COUNTROWS('Real_CFPB_Consumer_Complaints')` |
| **SLA Timeliness Breaches** | **173** | `CALCULATE(COUNTROWS(...), [Timely response?] = "No")` |
| **SLA Breach Rate %** | **6.88%** | `DIVIDE([SLA Breaches], [Total Issues], 0)` |
| **Monetary Remediation** | **100** | Cases requiring direct customer monetary compensation |

---

## 🔍 Key Risk Findings & Insights

1. **Root Cause Concentration (Pareto Principle)**:
   - In Debt Collection & Payment Dispute operations, **"Attempts to collect debt not owed"** accounts for over **50% of all customer escalations (1,218 issues)**, followed by *Written notification omissions (459)*.
   - Targeting automated reconciliation at this specific handoff eliminates the majority of operational friction.

2. **Intake Channel Vulnerability**:
   - **89.26%** of all complaints originate via **Web / Digital Portals**, highlighting that digital interface self-service failures drive the bulk of regulatory inquiries.

3. **Geographic Risk Heatmap**:
   - **California (338 issues, 23 monetary settlements)** and **Florida (250 issues, 11 monetary settlements)** represent the primary jurisdictions of regulatory focus and settlement exposure.

---

## 🛠️ Data Model & Technical Stack

- **BI Platform**: Microsoft Power BI Desktop
- **Data Engine**: Power Query ETL & DAX Calculated Measures
- **Interactive Web Engine**: HTML5, Tailwind CSS, Chart.js
- **Dataset**: Consumer Financial Protection Bureau (CFPB) Federal Regulatory Issues Log (62,516 rows)

---

## 📥 Downloads & Interactive Access

- 📁 **[Download Working Power BI File (.pbix)](Enterprise_Operational_Risk_Dashboard.pbix)**
- 🌐 **[View Interactive Web Version (index.html)](index.html)**
- 📄 **[Dataset Source (CFPB Open Data)](https://www.consumerfinance.gov/data-research/consumer-complaints/)**
