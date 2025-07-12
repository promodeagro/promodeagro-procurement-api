# 🧾 Product Requirements Document (PRD)
**Product:** Procurement Management System  
**Version:** 1.0  
**Owner:** Procurement/Product Team  
**Target Platform:** Web (Admin, Procurement, Receiver) + Mobile App (Buyer)

## 🔰 1. Overview

### 🎯 Purpose
The Procurement Module facilitates a structured and transparent end-to-end purchasing process—from order creation to payment—while ensuring inventory accuracy, supplier accountability, and financial traceability.

### 👥 Target Users
- Procurement Officers
- Buyers (Mobile-first experience)
- Warehouse/Receivers
- Accounts/Finance Staff
- Admins/Managers

## 🧩 2. Module Breakdown
- **🔹 A. Purchase Order** - Create, manage, and send purchase orders to suppliers
- **🔹 B. Buyer (Mobile App)** - Buyers can view and process POs, purchase items, and update status
- **🔹 C. Receiver** - Verify delivered goods, mark missed items, and sync to inventory
- **🔹 D. Invoice** - Generate invoices based on received goods
- **🔹 E. Payments** - Track, record, and manage supplier payments

## 🧱 3. Functional Specifications

### 📦 Module A: Purchase Order (Web)

#### 1. Purchase Order Listing Page
- **Filters:** Timeframe, PO Status, Supplier Name
- **Table Columns:** PO No, Supplier, Status, Delivery Date, Order Date
- **Header Stats:** Draft, Confirmed, Pending, Rejected, Completed PO counts
- **Actions:** Create PO, View/Edit/Delete, Export

#### 2. Create Purchase Order Page
- **Inputs:**
    - Supplier (dropdown)
    - Delivery Date
    - Shipping Location (warehouse)
    - Payment Term (optional)
    - Notes to Supplier
- **Item Selection Options:**
    - Add New Item (modal)
    - Add from Inventory
    - Import CSV
    - Get Low Stock Items
- **Review Section:**
    - Item list with quantity, unit, category
    - Edit/Delete item inline
- **Submit:**
    - Save as Draft
    - Send to Buyer (Status → Pending)

### 📱 Module B: Buyer (Mobile App)

#### 1. Login + Dashboard
- **Secure login (email/password)**
- **Dashboard with:**
    - Purchase Order Summary (Pending, Confirmed, Completed, Rejected)
    - Payment Overview (To Receive, Received, Partials, Issues)
    - Notifications (PO Alerts, Payments, Missing Items)

#### 2. PO List View
- **Sort & filter:** Latest/Oldest, Status
- **PO Summary Card with:** PO No, Status, Delivery Date, Ship To, Payment Term
- **Tap → Detail View**

#### 3. PO Detail View
- **View Items + Notes**
- **Actions:**
    - Confirm
    - Reject

#### 4. Purchase Fulfillment Flow
- **After confirmation:**
    - View item details
    - Input Purchased Qty, Purchase Price, Selling Price
    - Mark Not Available (moves to tab)
- **Tabs:** Incomplete, Purchased, Not Available
- **Enter Shipping/Loading Charges**
- **Complete PO:** Moves to "Completed" section

### 📥 Module C: Receiver (Web)

#### 1. Purchase Receive Listing
- **Filter by Date, Supplier**
- **Table Columns:** Date, PO No, Supplier, Status, Billed (Y/N), Amount

#### 2. New Purchase Receive
- **Select Supplier → View POs**
- **Select PO → Shows purchased items**
- **Enter Received Quantity**
- **Mark Missed Items (deduct cost, notify buyer)**
- **Receive Items →**
    - Update Warehouse Inventory
    - Status: Received/Issue
    - Notify Procurement + Buyer

### 🧾 Module D: Invoice (Web)

#### 1. Invoice List Page
- **Filters:** Timeframe, PO/Invoice No
- **Table Columns:** Invoice Date, No, PO No, Supplier, Status, Due Date, Amount, Balance Due

#### 2. Create New Invoice
- **Auto-generated Invoice No**
- **Fields:** Invoice Date, Due Date, Supplier, PO, Payment Term
- **Received Items Table:** Code, Name, Qty, Price, Subtotal
- **Totals Calculated**
- **Action:** Create Invoice

### 💰 Module E: Payments Made (Web)

#### 1. Payment Made List
- **Filter:** Timeframe
- **Search by Invoice/PO**
- **Table:** Payment No, Date, Invoice No, Supplier, Mode, Amount

#### 2. Make New Payment
- **Select Supplier → Fetch Unpaid/Partially Paid Invoices**
- **Choose Payment Mode:** Cash/Bank
- **Paid Through:** Select Account
- **Enter Payment Amounts → Partial or Full**
- **Action:** Pay →
    - Update Invoice Status
    - Save Payment History

## 🔄 4. Workflow Integration

| Step | Trigger/Actor | Output/Next Step |
|------|---------------|------------------|
| PO Creation | Procurement | PO (Pending) → Sent to Buyer |
| PO Confirmation | Buyer | Status → Confirmed |
| Item Procurement | Buyer | Status → Completed |
| Goods Received | Receiver | Stock Updated, Missed Items Notified |
| Invoice Generated | Finance | Linked to PO & Received Items |
| Payment Recorded | Accounts | Against Invoice; History Updated |

## 📦 5. Data Models (Simplified)

**PurchaseOrder**
- id, po_no, supplier_id, delivery_date, status, items[], notes, created_at

**POItem**
- id, item_id, po_id, quantity, purchase_price, selling_price, status

**Invoice**
- id, invoice_no, po_id, date, due_date, supplier_id, items[], total_amount, status

**Payment**
- id, payment_no, invoice_id, supplier_id, amount, payment_mode, account, date

**ReceiveLog**
- id, po_id, receiver_id, received_items[], missed_items[], date, status

## 🔐 6. Permissions & Roles

| Role | Create PO | Confirm/Reject PO | Enter Received Qty | Generate Invoice | Make Payment |
|------|-----------|-------------------|-------------------|------------------|--------------|
| Procurement | ✅ | ❌ | ❌ | ✅ | ❌ |
| Buyer | ❌ | ✅ | ❌ | ❌ | ❌ |
| Receiver | ❌ | ❌ | ✅ | ❌ | ❌ |
| Accountant | ❌ | ❌ | ❌ | ✅ | ✅ |
| Admin | ✅ | ✅ | ✅ | ✅ | ✅ |

## ⚙️ 7. Integrations
- **Inventory System:** Auto-update quantities on receiving
- **Finance System/ERP:** Sync payment, invoice data
- **Notifications:** Email/SMS alerts for PO updates, payment reminders, missing items
- **Mobile App (Buyer):** API-powered endpoints

## 📊 8. Reporting
- Purchase Order Status Report
- Pending vs Completed Receives
- Payment Due & Overdue Invoices
- Supplier Performance
- Purchase Cost & Margin Analysis

## 📱 9. Mobile App (Buyer)
- **Platform:** Flutter/React Native
- **Secure Login (JWT/Auth0)**
- **Offline Purchase Draft Capability**
- **Sync when online**
- **Push Notifications**
- **QR Scanner (Future Scope for PO Receiving)**

## ✅ 10. Success Metrics

| Metric | Target |
|--------|--------|
| PO-to-Completion Time | ≤ 3 business days |
| On-Time Receipts | ≥ 90% |
| Invoice Accuracy | ≥ 98% |
| Missed Items < Threshold | ≤ 5% per PO |
| Payment Cycle Turnaround | ≤ 7 days from invoice |
