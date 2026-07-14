# Power BI Service, Row-Level Security (RLS) & Scheduled Refresh Guide

This document acts as technical proof of my expertise deploying and configuring dashboards inside the **Power BI Service (SaaS)** environment.

---

## ☁️ 1. Publishing & Workspace Management

Publishing reports to a central, secure workspace is the standard method for corporate distribution.

### Publishing Workflow:
1. In Power BI Desktop, click **Publish** on the Home ribbon.
2. Select your target **Workspace** (e.g. `Executive Business Analytics Workspace`).
3. Once published, the dashboard creates two assets in the Service:
   * **Report**: The visual design layer (canvas, pages, interactions).
   * **Semantic Model (Dataset)**: The underlying tables, relationships, and DAX calculations.

### Workspace vs. App Distribution:
* **Workspace (Development)**: Add colleagues as Contributor/Member to co-develop, edit dashboards, and manage connections.
* **Power BI App (Production Distribution)**: Package reports into a clean user interface. End-users are granted **Viewer-only** access, separating developers from direct consumers.

---

## 🔒 2. Row-Level Security (RLS) Implementation

To ensure data confidentiality, we configure RLS to restrict data access based on a user's role or regional assignment.

### Step 1: Define Roles in Power BI Desktop
1. Click **Modeling** > **Manage Roles**.
2. Create a new role named `West Region Manager`.
3. Select the `Customer` table and enter the DAX filter expression:
   ```dax
   [Region] = "West"
   ```
4. Create a role named `East Region Manager` and write:
   ```dax
   [Region] = "East"
   ```

### Step 2: Test Roles locally
1. Click **Modeling** > **View as**.
2. Check the box for `West Region Manager`.
3. **Verification**: The entire dashboard canvas will automatically filter to show *only* data from the West region.

### Step 3: Map users in the Power BI Service
1. Navigate to the published **Dataset** in your web browser.
2. Click the three dots `...` and select **Security**.
3. Select the `West Region Manager` role.
4. Add user email addresses (e.g., `manager_west@company.com`) to assign them to the role.

> [!TIP]
> **Dynamic RLS**: For large organizations, instead of creating individual static roles, create a mapping table linking user emails to regions, and apply a dynamic DAX filter: `[User_Email] = USERPRINCIPALNAME()`.

---

## 🔄 3. Scheduled Refresh Setup (Gateway Config)

To keep reports updated automatically, we connect our local CSV/SQL data sources to the cloud service.

```
[Local CSV Data] ---> (On-Premises Gateway) ---> [Power BI Cloud Service] ---> [End Users]
```

### Steps to Configure scheduled refreshes:
1. **Install Gateway**: Install the **On-Premises Data Gateway (Standard Mode)** on the local host machine.
2. **Add Data Sources**:
   * Navigate to **Settings** > **Manage Connections and Gateways** in the Power BI Service.
   * Add a connection representing the local path to the raw files: `D:\Tableau resources\Sales.csv`.
3. **Configure Refresh Times**:
   * Open the Dataset settings.
   * Toggle **Scheduled Refresh** to **On**.
   * Set refresh frequency to **Daily** or **Weekly**.
   * Schedule precise times (e.g., 6:00 AM local time daily before business operations begin).
