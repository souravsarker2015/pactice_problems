## ACID Properties — Banking Context

---

### 🔑 এক কথায়:

> ACID = Database transaction-এর **4টা guarantee** — এগুলো নিশ্চিত করে যে banking-এর মতো critical system-এ data সবসময় **correct, consistent, আর safe** থাকে।

---

### A — Atomicity (সব অথবা কিছুই না)

> Transaction-এর সব operation **একটা unit** — যেকোনো একটা fail করলে **সব rollback** হয়।

```sql
-- Sourov থেকে Karim-এ 5000 BDT transfer

BEGIN;

UPDATE accounts
SET balance = balance - 5000
WHERE account_id = 'SB-001';   -- Step 1: Debit

-- এখানে server crash হলো! 😱

UPDATE accounts
SET balance = balance + 5000
WHERE account_id = 'SB-002';   -- Step 2: Credit (হলো না!)

COMMIT;
```

```
Without Atomicity:
Sourov-এর 5000 কাটা গেছে ✅
Karim-এর account-এ যোগ হয়নি ❌
5000 BDT হাওয়া! 💀

With Atomicity:
Step 2 fail → Step 1-ও rollback ✅
Sourov-এর balance আগের মতো ✅
কোনো টাকা হারায়নি ✅
```

**Django-তে:**
```python
from django.db import transaction

def transfer_money(from_id, to_id, amount):
    with transaction.atomic():   # ← Atomicity guarantee
        from_acc = Account.objects.select_for_update().get(
            account_id=from_id
        )
        to_acc = Account.objects.select_for_update().get(
            account_id=to_id
        )

        from_acc.balance -= amount
        to_acc.balance += amount

        from_acc.save()
        to_acc.save()   # এখানে fail হলে from_acc.save()-ও rollback ✅

        Transaction.objects.create(
            account=from_acc,
            txn_type="DR",
            amount=amount
        )
    # Block শেষে সব commit অথবা সব rollback
```

---

### C — Consistency (সবসময় valid state)

> Transaction-এর আগে আর পরে database সবসময় **valid state-এ** থাকবে — কোনো rule ভাঙবে না।

```sql
-- Consistency rules banking-এ:
-- ১. Balance কখনো negative হবে না
-- ২. Transfer-এ total money same থাকবে
-- ৩. Foreign key valid থাকবে

-- Constraint দিয়ে enforce করো
CREATE TABLE accounts (
    balance DECIMAL(15,2)
    CHECK (balance >= 0),        -- Rule 1 ✅

    account_id VARCHAR(20)
    REFERENCES accounts(id)      -- Rule 3 ✅
);

-- Transfer consistency check:
-- Before: Sourov=50000, Karim=30000, Total=80000
-- After:  Sourov=45000, Karim=35000, Total=80000 ✅
-- Money তৈরি হয়নি, ধ্বংসও হয়নি
```

```python
# Django Model-level consistency
class Account(models.Model):
    balance = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(balance__gte=0),
                name="balance_non_negative"   # DB-level enforce ✅
            )
        ]

    def clean(self):
        if self.balance < 0:
            raise ValidationError("Balance cannot be negative")
```

---

### I — Isolation (আলাদা থাকো)

> একটা transaction চলার সময় অন্য transaction সেটার **intermediate state দেখতে পারবে না।**

```sql
-- সমস্যা: দুটো transaction একসাথে চলছে

-- Transaction A (Sourov withdraw করছে)
BEGIN;
SELECT balance FROM accounts WHERE id=1;  -- 50000 দেখলো
-- এখনো commit হয়নি

-- Transaction B (একই সময়ে Sourov-এর balance চেক)
SELECT balance FROM accounts WHERE id=1;
-- কী দেখবে? 50000 (old) নাকি 45000 (new)?

-- Isolation Level অনুযায়ী ভিন্ন আচরণ
```

**Banking-এ Isolation Problems:**

```
১. Dirty Read:
   T1 balance 45000-এ নামালো (commit হয়নি)
   T2 সেই 45000 পড়লো
   T1 rollback করলো → T2 ভুল data পড়েছে! 😱

২. Non-repeatable Read:
   T1 balance দুবার পড়লো — দুবার আলাদা value
   মাঝখানে T2 update করেছে

৩. Phantom Read:
   T1 transactions count করলো — 10টা
   T2 নতুন transaction insert করলো
   T1 আবার count করলো — 11টা 😱
```

```sql
-- Banking-এ Serializable use করো critical operation-এ
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

BEGIN;
SELECT balance FROM accounts WHERE id=1 FOR UPDATE;  -- Lock নিলো
UPDATE accounts SET balance = balance - 5000 WHERE id=1;
COMMIT;
-- অন্য transaction এই row access করতে পারবে না ✅
```

```python
# Django-তে select_for_update() → Row lock
def withdraw(account_id, amount):
    with transaction.atomic():
        account = Account.objects\
            .select_for_update()\   # Row lock ✅
            .get(account_id=account_id)

        # অন্য কোনো transaction এই row touch করতে পারবে না
        if account.balance < amount:
            raise InsufficientBalanceError(account_id, amount, account.balance)

        account.balance -= amount
        account.save()
```

---

### D — Durability (চিরস্থায়ী)

> একবার **COMMIT** হলে data **চিরস্থায়ী** — power চলে গেলেও, server crash হলেও data থাকবে।

```sql
BEGIN;
UPDATE accounts SET balance = 45000 WHERE account_id = 'SB-001';
COMMIT;   -- এই line-এর পরে power গেলেও data safe ✅

-- কীভাবে PostgreSQL Durability নিশ্চিত করে:
-- WAL (Write-Ahead Log) — data change হওয়ার আগে log লেখে
-- fsync — disk-এ physically লেখে memory flush করে
-- Checkpoint — regular interval-এ data file sync করে
```

```
WAL Process:
Transaction COMMIT
      ↓
WAL Log disk-এ লেখা হয়  ← এটা হলেই COMMIT confirm
      ↓
User-কে success বলা হয়
      ↓
(Background-এ data file update হয়)

Power চলে গেলে:
WAL থেকে recover করে
Data file update হয়
কোনো data হারায় না ✅
```

---

### 🏦 Banking-এ ACID — Real Scenario:

```python
def process_payment(sender_id, receiver_id, amount):
    """
    ACID সব চারটা property এই একটা function-এ
    """
    try:
        with transaction.atomic():   # ← ATOMICITY শুরু

            # Row lock — ISOLATION
            sender = Account.objects\
                .select_for_update()\
                .get(account_id=sender_id)

            receiver = Account.objects\
                .select_for_update()\
                .get(account_id=receiver_id)

            # CONSISTENCY check
            if sender.balance < amount:
                raise InsufficientBalanceError(
                    sender_id, amount, sender.balance
                )
            if not sender.is_active or not receiver.is_active:
                raise AccountInactiveError()

            # Actual operation
            sender.balance -= amount
            receiver.balance += amount

            sender.save()    # ATOMICITY — দুটোই হবে
            receiver.save()  # বা কোনোটাই না

            # Transaction log — DURABILITY-র অংশ
            Transaction.objects.create(
                from_account=sender,
                to_account=receiver,
                amount=amount,
                status="completed"
            )

        # COMMIT — এখন DURABILITY নিশ্চিত
        # WAL-এ লেখা হয়েছে, disk-এ safe ✅
        return {"status": "success", "amount": amount}

    except Exception as e:
        # ROLLBACK — ATOMICITY নিশ্চিত
        # sender balance কাটা গেলেও ফিরে আসবে
        logger.error(f"Payment failed: {e}")
        raise
```

---

### 📊 ACID — এক নজরে:

| Property | গ্যারান্টি | Banking Example | ছাড়া কী হতো |
|---|---|---|---|
| **Atomicity** | সব অথবা কিছুই না | Transfer-এ debit হয় credit না হলে rollback | টাকা হারিয়ে যেত |
| **Consistency** | সবসময় valid state | Balance কখনো negative হবে না | Invalid state তৈরি হতো |
| **Isolation** | Transaction আলাদা থাকে | একসাথে দুজন withdraw করতে পারবে না | Double spend হতো |
| **Durability** | Commit মানে চিরস্থায়ী | Crash হলেও committed transaction থাকবে | Data হারিয়ে যেত |

---

### 🎯 Interview Closing line:

> *"ACID ছাড়া banking system চলতে পারে না। Atomicity নিশ্চিত করে টাকা কখনো শূন্যে মিলিয়ে যাবে না। Consistency নিশ্চিত করে balance negative হবে না। Isolation নিশ্চিত করে একই টাকা দুজন একসাথে তুলতে পারবে না — race condition থেকে রক্ষা করে। Durability নিশ্চিত করে COMMIT হলে power চলে গেলেও data safe। Django-তে `transaction.atomic()` আর `select_for_update()` দিয়ে এই চারটাই enforce করি।"*


## JOIN Types & Database Indexes
![alt text](image-4.png)
---

## ১. INNER JOIN vs LEFT JOIN vs FULL OUTER JOIN

---

### 🔑 Visual দিয়ে বোঝো:---

### 💻 Banking Schema দিয়ে সব JOIN দেখো:

```sql
-- Tables
accounts:     account_id | name    | branch_id
branches:     branch_id  | name    | city
transactions: txn_id     | account_id | amount

-- Data
accounts:  SB-001/Sourov/B1, SB-002/Karim/B2, SB-003/Rina/NULL
branches:  B1/Gulshan/Dhaka, B2/Banani/Dhaka, B3/Dhanmondi/Dhaka
```

---

**INNER JOIN — দুটোতেই match থাকলেই শুধু:**
```sql
SELECT a.name, b.name as branch
FROM accounts a
INNER JOIN branches b ON a.branch_id = b.branch_id;

-- Result: (2 rows — Rina বাদ, B3 বাদ)
-- Sourov | Gulshan
-- Karim  | Banani
-- Rina নেই (branch_id = NULL)
-- B3 নেই (কোনো account নেই)
```

**LEFT JOIN — বাম table সব + match হলে ডান:**
```sql
SELECT a.name, b.name as branch
FROM accounts a
LEFT JOIN branches b ON a.branch_id = b.branch_id;

-- Result: (3 rows — সব account)
-- Sourov | Gulshan
-- Karim  | Banani
-- Rina   | NULL    ← branch নেই কিন্তু Rina আছে ✅
```

**FULL OUTER JOIN — দুটো table-এর সব:**
```sql
SELECT a.name, b.name as branch
FROM accounts a
FULL OUTER JOIN branches b ON a.branch_id = b.branch_id;

-- Result: (4 rows)
-- Sourov | Gulshan
-- Karim  | Banani
-- Rina   | NULL      ← account আছে, branch নেই
-- NULL   | Dhanmondi ← branch আছে, account নেই (B3)
```

---

### 🏦 Banking-এ কোনটা কোথায়:

```sql
-- ১. INNER JOIN — শুধু valid data দরকার
-- Active account-এর statement
SELECT t.amount, t.created_at, a.name
FROM transactions t
INNER JOIN accounts a ON t.account_id = a.id
WHERE a.is_active = TRUE;
-- Invalid account-এর transaction দেখাবে না ✅

-- ২. LEFT JOIN — সব account দেখাতে হবে
-- Transaction আছে বা না থাকলেও সব account দেখাও
SELECT a.name,
       COUNT(t.id) as txn_count,
       COALESCE(SUM(t.amount), 0) as total
FROM accounts a
LEFT JOIN transactions t ON a.id = t.account_id
GROUP BY a.id, a.name;
-- Transaction নেই → count=0, total=0 ✅

-- ৩. FULL OUTER JOIN — reconciliation-এ
-- System A আর System B-এর data match করো
SELECT
    a.txn_id as system_a,
    b.txn_id as system_b,
    CASE
        WHEN b.txn_id IS NULL THEN 'Missing in B'
        WHEN a.txn_id IS NULL THEN 'Missing in A'
        ELSE 'Matched'
    END as status
FROM system_a_transactions a
FULL OUTER JOIN system_b_transactions b
ON a.txn_id = b.txn_id
WHERE a.txn_id IS NULL OR b.txn_id IS NULL;
-- Mismatch খুঁজে বের করো ✅
```

---

## ২. Database Indexes

---

### 🔑 Index কী — Visual:

এরপর index-এর B-tree structure দেখো:---
![alt text](image-5.png)
### 💻 Index ছাড়া vs সহ:

```sql
-- Without index: Full Table Scan — O(n)
SELECT * FROM transactions WHERE account_id = 'SB-001';
-- ১০ লাখ row → সব scan করে 😱 (~500ms)

-- With index: B-tree Search — O(log n)
CREATE INDEX idx_txn_account ON transactions(account_id);
-- ১০ লাখ row → মাত্র ~20 step (~1ms) ✅
```

---

### 💻 Index Types — Banking-এ:

```sql
-- ১. Single Column Index
CREATE INDEX idx_account_id ON accounts(account_id);
-- WHERE account_id = 'SB-001' ✅

-- ২. Composite Index — column order matter করে!
CREATE INDEX idx_txn_acc_date
ON transactions(account_id, created_at DESC);
-- WHERE account_id = 'SB-001' ✅
-- WHERE account_id = 'SB-001' AND created_at > '2024-01-01' ✅
-- WHERE created_at > '2024-01-01' ❌ (leading column নেই)

-- ৩. Partial Index — condition-based, smaller, faster
CREATE INDEX idx_active_accounts
ON accounts(account_id)
WHERE is_active = TRUE;
-- শুধু active accounts index-এ → 80% smaller ✅

-- ৪. Covering Index — table access-ই লাগে না
CREATE INDEX idx_covering
ON transactions(account_id)
INCLUDE (amount, created_at, txn_type);
-- এই query-র জন্য table touch করবে না:
SELECT amount, created_at, txn_type
FROM transactions WHERE account_id = 'SB-001';
-- Index-ই সব data দিচ্ছে ✅

-- ৫. Expression Index
CREATE INDEX idx_lower_name ON accounts(LOWER(name));
-- WHERE LOWER(name) = 'sourov' → Index use করবে ✅

-- ৬. GIN Index — JSONB, Array, Full-text
CREATE INDEX idx_metadata ON accounts USING GIN(metadata);
-- WHERE metadata @> '{"kyc": "verified"}' ✅
```

---

### ✅ Index কখন ADD করবে:

```sql
-- ১. Primary/Foreign Key — সবসময়
account_id BIGINT REFERENCES accounts(id)
-- FK-তে automatically index থাকলে JOIN fast হয়

-- ২. Frequently filtered column
WHERE is_active = TRUE     → index দাও
WHERE account_type = 'SB'  → index দাও
WHERE created_at > '...'   → index দাও

-- ৩. JOIN column
ON a.branch_id = b.id      → branch_id-এ index দাও

-- ৪. ORDER BY column
ORDER BY created_at DESC   → created_at-এ index দাও

-- ৫. High cardinality column — unique values বেশি
account_id (millions unique) → ✅ index উপকারী
txn_type (DR/CR শুধু)       → ❌ index কম উপকারী

-- ৬. EXPLAIN ANALYZE দেখে confirm করো
EXPLAIN ANALYZE
SELECT * FROM transactions WHERE account_id = 'SB-001';
-- Seq Scan দেখলে → index দাও
-- Index Scan দেখলে → already আছে ✅
```

---

### ❌ Index কখন AVOID করবে:

```sql
-- ১. Low cardinality — unique values কম
CREATE INDEX idx_gender ON accounts(gender);
-- ❌ শুধু M/F/O → full scan-এর চেয়ে slow হতে পারে!
-- Optimizer often ignores it anyway

-- ২. Write-heavy table
-- Index = প্রতিটা INSERT/UPDATE/DELETE-এ update হয়
-- High-frequency transaction log table-এ index কম রাখো
-- INSERT INTO audit_logs → বারবার index update হবে 😱

-- ৩. Small table
CREATE INDEX idx_branches ON branches(branch_id);
-- ❌ শুধু ১০টা branch → full scan-ই দ্রুত
-- Index overhead বেশি, benefit নেই

-- ৪. Rarely queried column
CREATE INDEX idx_notes ON accounts(internal_notes);
-- ❌ কেউ notes দিয়ে query করে না → waste

-- ৫. Function on indexed column
WHERE YEAR(created_at) = 2024
-- ❌ Index use হবে না!
-- ✅ Fix: WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31'

-- ৬. Leading wildcard
WHERE name LIKE '%Sourov%'
-- ❌ Index use হবে না
-- ✅ Fix: Full-text search বা edge n-gram
```

---

### 💻 Index কাজ করছে কিনা দেখো:

```sql
-- EXPLAIN ANALYZE দিয়ে verify করো
EXPLAIN ANALYZE
SELECT t.amount, a.name
FROM transactions t
JOIN accounts a ON t.account_id = a.id
WHERE t.created_at > NOW() - INTERVAL '30 days'
AND a.is_active = TRUE;

-- Good output:
-- Index Scan using idx_txn_date on transactions
-- cost=0.56..150.23 rows=1000

-- Bad output:
-- Seq Scan on transactions
-- cost=0.00..85000.00 rows=1000000 ← Full scan! 😱

-- Unused indexes খুঁজে বের করো
SELECT indexrelname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan ASC;
-- idx_scan = 0 → কখনো use হয়নি → DROP করো!

-- Index size দেখো
SELECT indexname, pg_size_pretty(pg_relation_size(indexname::text))
FROM pg_indexes WHERE tablename = 'transactions';
```

---

### 📊 JOIN Types Summary:

| JOIN | কী দেয় | Banking use |
|---|---|---|
| `INNER JOIN` | Match করা rows শুধু | Valid transaction report |
| `LEFT JOIN` | বাম সব + match | সব account-এর summary |
| `RIGHT JOIN` | ডান সব + match | সব branch-এর summary |
| `FULL OUTER JOIN` | দুটোর সব | Reconciliation |
| `SELF JOIN` | Same table | Employee hierarchy |

---

### 📊 Index Summary:

| | Add করো | Avoid করো |
|---|---|---|
| **Cardinality** | High (account_id) | Low (gender, status) |
| **Query** | Frequent WHERE/JOIN | Rarely queried |
| **Table size** | Large | Small (< 1000 rows) |
| **Operations** | Read-heavy | Write-heavy |
| **Pattern** | Exact/range match | Leading wildcard |

---

### 🎯 Interview Closing line:

> *"JOIN choice করি data requirement অনুযায়ী — transaction report-এ INNER JOIN কারণ শুধু valid data দরকার, account summary-তে LEFT JOIN কারণ transaction না থাকলেও account দেখাতে হবে, reconciliation-এ FULL OUTER JOIN কারণ দুটো system-এর mismatch খুঁজতে হবে। Index-এ সবার আগে EXPLAIN ANALYZE দেখি — Seq Scan দেখলে index দিই, কিন্তু write-heavy table-এ সতর্ক থাকি কারণ প্রতিটা write-এ index maintain করতে হয়। Composite index-এ column order সবচেয়ে গুরুত্বপূর্ণ — most selective column আগে।"*

## Clustered vs Non-clustered Index & Normalization Forms

---

## ১. Clustered vs Non-clustered Index

---### 💻 Clustered Index:

```sql
-- Primary Key → automatically Clustered Index (PostgreSQL-এ CLUSTER command দরকার)
CREATE TABLE accounts (
    account_id VARCHAR(20) PRIMARY KEY,  -- Clustered (default)
    name VARCHAR(100),
    balance DECIMAL(15,2)
);

-- Data physically account_id order-এ store হয়:
-- SB-001, SB-002, SB-003... (disk-এ এই order-এই)

-- Range query → খুব দ্রুত (physically consecutive)
SELECT * FROM accounts
WHERE account_id BETWEEN 'SB-001' AND 'SB-100';
-- Disk-এ পাশাপাশি থাকে → একটা read-এ অনেক data ✅

-- PostgreSQL-এ manually cluster করো
CLUSTER accounts USING accounts_pkey;
-- Data physically reorder হলো

-- Problem: Insert করলে reorder দরকার হতে পারে
-- SB-050 insert করলে মাঝখানে জায়গা করতে হবে
```

### 💻 Non-clustered Index:

```sql
-- আলাদা B-tree structure — data move হয় না
CREATE INDEX idx_balance ON accounts(balance);
-- Index: sorted by balance → pointer to actual row

-- Multiple non-clustered index allowed
CREATE INDEX idx_name    ON accounts(name);
CREATE INDEX idx_branch  ON accounts(branch_id);
CREATE INDEX idx_balance ON accounts(balance);
-- সবগুলো আলাদা structure, heap-এ point করে

-- Extra lookup দরকার হয়:
-- Index → row pointer → heap → actual data (2 steps)
-- Clustered: Index = data (1 step) ✅

-- Covering index দিয়ে heap lookup এড়ানো যায়
CREATE INDEX idx_covering
ON accounts(branch_id)
INCLUDE (name, balance);  -- এই query-তে heap যেতেই হবে না
SELECT name, balance FROM accounts WHERE branch_id = 1;
```

### 📊 পার্থক্য:

| | Clustered | Non-clustered |
|---|---|---|
| Data storage | Index-এই data | আলাদা heap-এ |
| Per table | ১টা মাত্র | অনেকগুলো |
| Range query | ✅ খুব দ্রুত | মাঝারি |
| Lookup steps | ১টা | ২টা (index + heap) |
| Insert cost | বেশি (reorder) | কম |
| Banking use | `account_id` PK | `balance`, `name`, `branch_id` |

---

## ২. Normalization — 1NF থেকে BCNFBanking-এ একটা খারাপ table ধরে ধাপে ধাপে normalize করা যাক।

![alt text](image-6.png)

---

### শুরু — Unnormalized Table:

```
account_transactions (খুব খারাপ design):

account_id | account_name | branch_id | branch_city | phones          | txn1_amt | txn2_amt
SB-001     | Sourov       | B1        | Dhaka       | 01711, 01811    | 500      | 1000
SB-002     | Karim        | B1        | Dhaka       | 01911           | 250      | NULL
SB-003     | Rina         | B2        | Chittagong  | 01611, 01711    | 750      | 500

সমস্যা:
- phones column-এ multiple values (01711, 01811)
- txn1_amt, txn2_amt repeating groups
- branch_city depends on branch_id, not account_id
```

---

### 1NF — Atomic Values, No Repeating Groups:

**Rule: প্রতিটা cell-এ একটাই value, কোনো repeating group নেই।**

```sql
-- ❌ 1NF violate
account_id | phones
SB-001     | "01711, 01811"    -- multiple values!
SB-001     | txn1=500, txn2=1000  -- repeating columns!

-- ✅ 1NF fix — atomic করো
-- Phone আলাদা table-এ
CREATE TABLE account_phones (
    account_id VARCHAR(20),
    phone      VARCHAR(15),
    PRIMARY KEY (account_id, phone)
);
-- SB-001 | 01711
-- SB-001 | 01811  ← আলাদা row ✅

-- Transaction আলাদা table-এ
CREATE TABLE transactions (
    txn_id     BIGSERIAL PRIMARY KEY,
    account_id VARCHAR(20),
    amount     DECIMAL(15,2)
);
-- txn1, txn2 column এর বদলে আলাদা rows ✅

-- 1NF result:
accounts (account_id, account_name, branch_id, branch_city)
account_phones (account_id, phone)
transactions (txn_id, account_id, amount)
```

---

### 2NF — No Partial Dependency:

**Rule: Composite key থাকলে non-key column সম্পূর্ণ key-এর উপর depend করতে হবে — শুধু একটা অংশের উপর না।**

```sql
-- ❌ 2NF violate (composite key: account_id + product_id)
account_products:
account_id | product_id | account_name | product_name | signup_date
SB-001     | LOAN       | Sourov       | Home Loan    | 2024-01-01
SB-001     | FD         | Sourov       | Fixed Dep.   | 2024-02-01
SB-002     | LOAN       | Karim        | Home Loan    | 2024-01-15

-- সমস্যা:
-- account_name depends only on account_id (partial dependency!) 😱
-- product_name depends only on product_id (partial dependency!) 😱
-- signup_date depends on BOTH → OK ✅

-- ✅ 2NF fix — আলাদা table-এ নাও
CREATE TABLE accounts (
    account_id   VARCHAR(20) PRIMARY KEY,
    account_name VARCHAR(100)   -- শুধু account_id-এর উপর depend ✅
);

CREATE TABLE products (
    product_id   VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(100)   -- শুধু product_id-এর উপর depend ✅
);

CREATE TABLE account_products (
    account_id  VARCHAR(20) REFERENCES accounts(account_id),
    product_id  VARCHAR(10) REFERENCES products(product_id),
    signup_date DATE,           -- composite key-এর উপর depend ✅
    PRIMARY KEY (account_id, product_id)
);
```

---

### 3NF — No Transitive Dependency:

**Rule: Non-key column অন্য non-key column-এর উপর depend করতে পারবে না।**

```sql
-- ❌ 3NF violate
accounts:
account_id | account_name | branch_id | branch_name | branch_city
SB-001     | Sourov       | B1        | Gulshan     | Dhaka
SB-002     | Karim        | B1        | Gulshan     | Dhaka  ← duplicate!
SB-003     | Rina         | B2        | Banani      | Dhaka  ← duplicate!

-- সমস্যা (Transitive Dependency):
-- account_id → branch_id ✅
-- branch_id  → branch_name, branch_city 😱
-- তাই: account_id → branch_name (transitively) ← 3NF violate!

-- Update anomaly:
-- Gulshan branch-এর city change হলে
-- SB-001 আর SB-002 দুটো row update করতে হবে 😱

-- ✅ 3NF fix — branch আলাদা table-এ
CREATE TABLE branches (
    branch_id   VARCHAR(10) PRIMARY KEY,
    branch_name VARCHAR(100),   -- branch_id-এর উপর directly depend ✅
    branch_city VARCHAR(50)     -- branch_id-এর উপর directly depend ✅
);

CREATE TABLE accounts (
    account_id   VARCHAR(20) PRIMARY KEY,
    account_name VARCHAR(100),
    branch_id    VARCHAR(10) REFERENCES branches(branch_id)
    -- branch_name, branch_city সরিয়ে দিলাম ✅
);

-- এখন branch city update হলে শুধু branches table-এ একবার change ✅
```

---

### BCNF — Boyce-Codd Normal Form (3NF-এর stronger version):

**Rule: প্রতিটা functional dependency-তে বাম পাশ অবশ্যই superkey হতে হবে।**

```sql
-- ❌ BCNF violate (3NF-এ আছে কিন্তু BCNF-এ নেই)
-- Scenario: একজন teller শুধু একটা branch-এ কাজ করে
--           একটা account শুধু একটা branch-এ থাকে

account_teller:
account_id | teller_id | branch_id
SB-001     | T01       | B1
SB-001     | T02       | B1        ← SB-001 একই branch-এ দুজন teller
SB-002     | T01       | B1

-- Functional Dependencies:
-- (account_id, teller_id) → branch_id  ← composite key → branch
-- teller_id → branch_id               ← teller থেকে branch! 😱
--                                         teller_id superkey না

-- ✅ BCNF fix
CREATE TABLE teller_branch (
    teller_id  VARCHAR(10) PRIMARY KEY,
    branch_id  VARCHAR(10) REFERENCES branches(branch_id)
    -- teller_id → branch_id (teller_id is superkey here) ✅
);

CREATE TABLE account_teller (
    account_id VARCHAR(20),
    teller_id  VARCHAR(10) REFERENCES teller_branch(teller_id),
    PRIMARY KEY (account_id, teller_id)
    -- branch_id সরিয়ে দিলাম ✅
);
```

---

### 💻 Final Normalized Banking Schema:

```sql
-- সব normalization apply করার পরে:

CREATE TABLE branches (
    branch_id   VARCHAR(10) PRIMARY KEY,
    branch_name VARCHAR(100) NOT NULL,
    city        VARCHAR(50)  NOT NULL
);

CREATE TABLE accounts (
    account_id   VARCHAR(20) PRIMARY KEY,
    account_name VARCHAR(100) NOT NULL,
    branch_id    VARCHAR(10) REFERENCES branches(branch_id),
    balance      DECIMAL(15,2) DEFAULT 0
);

CREATE TABLE account_phones (
    account_id VARCHAR(20) REFERENCES accounts(account_id),
    phone      VARCHAR(15) NOT NULL,
    PRIMARY KEY (account_id, phone)
);

CREATE TABLE products (
    product_id   VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(100)
);

CREATE TABLE account_products (
    account_id  VARCHAR(20) REFERENCES accounts(account_id),
    product_id  VARCHAR(10) REFERENCES products(product_id),
    signup_date DATE,
    PRIMARY KEY (account_id, product_id)
);

CREATE TABLE transactions (
    txn_id     BIGSERIAL PRIMARY KEY,
    account_id VARCHAR(20) REFERENCES accounts(account_id),
    amount     DECIMAL(15,2) NOT NULL,
    txn_type   CHAR(2),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

### 📊 Normalization Summary:

| Form | Rule | Fix করে | Banking Example |
|---|---|---|---|
| **1NF** | Atomic values, no repeating | Multi-value cells | phones → আলাদা table |
| **2NF** | No partial dependency | Composite key-এ partial | product_name → products table |
| **3NF** | No transitive dependency | Non-key → non-key | branch_city → branches table |
| **BCNF** | Every determinant = superkey | 3NF-এ missed cases | teller → branch আলাদা |

---

### 🎯 Interview Closing line:

> *"Clustered index মানে data physically sorted হয়ে store হয় — banking-এ account_id-এর Primary Key automatically clustered, তাই range query অনেক দ্রুত। Non-clustered index আলাদা structure — pointer দিয়ে heap-এ যায়, একটা table-এ অনেকগুলো থাকতে পারে balance বা name search-এর জন্য। Normalization-এ 1NF atomic করে, 2NF partial dependency সরায়, 3NF transitive dependency সরায়, BCNF আরো strict। Banking schema-তে branch city, product name — এগুলো আলাদা table-এ না রাখলে একটা city update-এ হাজারটা row change করতে হতো।"*


## Transaction, Isolation Levels, Deadlock, TRUNCATE vs DELETE vs DROP

---

## ১. Transaction কী?

> Transaction = **একটা logical unit of work** — ভেতরের সব operation হয় একসাথে সফল হয়, নয়তো সবটা rollback হয়।

```sql
BEGIN;

UPDATE accounts SET balance = balance - 5000
WHERE account_id = 'SB-001';   -- Step 1: Debit

UPDATE accounts SET balance = balance + 5000
WHERE account_id = 'SB-002';   -- Step 2: Credit

COMMIT;   -- সফল হলে
-- ROLLBACK;  -- ব্যর্থ হলে সব undo
```

Step 1 হয়ে Step 2-এ crash হলে → ROLLBACK → Sourov-এর টাকা ফিরে আসে। কোনো টাকা হারায় না।

---

## ২. Isolation Levels

---

### আগে — তিনটা সমস্যা বুঝতে হবে:

**Dirty Read** — commit হয়নি এমন data পড়া:
```sql
-- T1: balance 50000 → 45000 (commit হয়নি)
-- T2: balance পড়লো → 45000 দেখলো 😱
-- T1: ROLLBACK করলো → balance আবার 50000
-- T2 ভুল data দিয়ে কাজ করলো!
```

**Non-repeatable Read** — একই transaction-এ একই row দুবার পড়লে আলাদা result:
```sql
-- T1: balance পড়লো → 50000
-- T2: balance 50000 → 45000, COMMIT করলো
-- T1: balance আবার পড়লো → 45000 😱 (আগে 50000 ছিল!)
```

**Phantom Read** — একই query দুবার চালালে আলাদা rows:
```sql
-- T1: COUNT(*) → 100 transactions
-- T2: নতুন transaction INSERT করলো
-- T1: COUNT(*) আবার → 101 😱 (নতুন "phantom" row!)
```

---

### ৪টা Isolation Level:

```sql
-- ১. Read Uncommitted — সবচেয়ে কম isolation
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
-- Dirty read সম্ভব ❌ Banking-এ কখনো না

-- ২. Read Committed — PostgreSQL default
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- Dirty read নেই ✅
-- Non-repeatable read সম্ভব ⚠️

-- ৩. Repeatable Read — MySQL default
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- Dirty + Non-repeatable read নেই ✅
-- Phantom read সম্ভব ⚠️

-- ৪. Serializable — সবচেয়ে বেশি isolation
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- সব সমস্যা নেই ✅ কিন্তু সবচেয়ে slow
```

| Level | Dirty Read | Non-repeatable | Phantom | Banking Use |
|---|---|---|---|---|
| Read Uncommitted | হয় | হয় | হয় | ❌ কখনো না |
| Read Committed | নেই | হয় | হয় | ✅ General API |
| Repeatable Read | নেই | নেই | হয় | ✅ Balance check |
| Serializable | নেই | নেই | নেই | ✅ Audit, Transfer |

---

### Banking-এ কোনটা কোথায়:

```python
# Balance check → Repeatable Read
with transaction.atomic():
    connection.execute(
        "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
    )
    balance = Account.objects.get(account_id="SB-001").balance

# Transfer → Serializable + Row lock
with transaction.atomic():
    connection.execute(
        "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
    )
    account = Account.objects\
        .select_for_update()\   # Row lock
        .get(account_id="SB-001")
    account.balance -= 5000
    account.save()
```

---

## ৩. Deadlock কী?

> Deadlock = দুটো transaction একে অপরের lock-এর জন্য অপেক্ষা করছে — কেউ এগোতে পারছে না।

```sql
-- T1 চলছে           |  T2 চলছে
BEGIN;               |  BEGIN;
                     |
UPDATE accounts      |  UPDATE accounts
SET balance=45000    |  SET balance=25000
WHERE id=1;          |  WHERE id=2;
-- id=1 lock নিলো   |  -- id=2 lock নিলো
                     |
UPDATE accounts      |  UPDATE accounts
SET balance=55000    |  SET balance=35000
WHERE id=2;          |  WHERE id=1;
-- id=2-এর জন্য wait|  -- id=1-এর জন্য wait
-- DEADLOCK! 😱      |  -- DEADLOCK! 😱

-- T1 id=2 চায়, T2 আটকে রেখেছে
-- T2 id=1 চায়, T1 আটকে রেখেছে
-- চিরকাল অপেক্ষা করবে
```

PostgreSQL automatically detect করে → একটাকে rollback করে → অন্যটা চলে।

---

### Deadlock Prevention — ৪টা উপায়:

**উপায় ১ — সবসময় একই order-এ lock নাও (সবচেয়ে গুরুত্বপূর্ণ):**
```python
def transfer(from_id, to_id, amount):
    # সবসময় ছোট id আগে lock করো
    first_id  = min(from_id, to_id)
    second_id = max(from_id, to_id)

    with transaction.atomic():
        accounts = Account.objects\
            .select_for_update()\
            .filter(id__in=[first_id, second_id])\
            .order_by("id")   # consistent order ✅

        # T1: lock id=1, তারপর id=2
        # T2: lock id=1, তারপর id=2
        # কখনো deadlock হবে না ✅
```

**উপায় ২ — Lock Timeout দাও:**
```sql
-- নির্দিষ্ট সময় পরে give up করো
SET lock_timeout = '5s';
-- 5 সেকেন্ড পেলে না → error throw করো
-- Deadlock অনির্দিষ্টকাল আটকে থাকবে না ✅
```

**উপায় ৩ — Transaction ছোট রাখো:**
```python
# ❌ Bad — দীর্ঘ transaction, বেশিক্ষণ lock ধরে
with transaction.atomic():
    account = Account.objects.select_for_update().get(id=1)
    time.sleep(5)        # lock ধরে আছে 😱
    send_email()         # slow operation!
    account.balance -= 5000
    account.save()

# ✅ Good — lock-এর বাইরে slow কাজ করো
account = Account.objects.get(id=1)  # lock ছাড়া read
send_email()                          # lock-এর বাইরে ✅

with transaction.atomic():           # শুধু DB operation lock-এ
    account = Account.objects\
        .select_for_update().get(id=1)
    account.balance -= 5000
    account.save()
```

**উপায় ৪ — `select_for_update(nowait=True)`:**
```python
from django.db import OperationalError

try:
    with transaction.atomic():
        account = Account.objects\
            .select_for_update(nowait=True)\  # wait না করে error দাও
            .get(account_id="SB-001")
        account.balance -= 5000
        account.save()

except OperationalError:
    # Lock পাইনি → retry করো
    retry_transfer.delay(...)  # Celery-তে পাঠাও ✅
```

---

## ৪. TRUNCATE vs DELETE vs DROP

---

### এক কথায়:

```
DELETE   = নির্দিষ্ট rows মুছো (সার্জিক্যাল)
TRUNCATE = সব rows মুছো (দ্রুত)
DROP     = পুরো table মুছো (ধ্বংস)
```

---

### DELETE:

```sql
-- WHERE দিয়ে নির্দিষ্ট rows মুছো
DELETE FROM transactions
WHERE created_at < '2020-01-01';   -- পুরনো transaction মুছো

-- WHERE ছাড়া → সব rows (কিন্তু TRUNCATE-এর চেয়ে slow)
DELETE FROM temp_staging;

-- বৈশিষ্ট্য:
-- Rollback করা যায় ✅
-- WHERE clause দেওয়া যায় ✅
-- Trigger fire হয় ✅
-- Auto-increment reset হয় না ✅
-- Row-by-row delete → slow for large data
-- WAL log তৈরি হয় → recoverable

-- Banking use:
DELETE FROM sessions WHERE expired_at < NOW();
DELETE FROM otp_codes WHERE used = TRUE;
```

---

### TRUNCATE:

```sql
-- সব rows একসাথে মুছো — DELETE-এর চেয়ে অনেক দ্রুত
TRUNCATE TABLE temp_calculations;

-- বৈশিষ্ট্য:
-- Row-by-row না — পুরো data page deallocate করে → fast ✅
-- WHERE clause নেই ❌ সব যাবে
-- Trigger fire হয় না (PostgreSQL-এ TRUNCATE trigger আছে)
-- Auto-increment reset হয় ✅ (PostgreSQL)
-- PostgreSQL-এ Rollback করা যায় ✅ (transaction-এর মধ্যে)
-- MySQL-এ Rollback করা যায় না ❌

TRUNCATE TABLE temp_report_cache;
TRUNCATE TABLE staging_imports RESTART IDENTITY;  -- ID reset ✅

-- Banking use:
TRUNCATE TABLE daily_cache;        -- Daily cache clear
TRUNCATE TABLE temp_batch_process; -- Batch job শেষে cleanup
```

---

### DROP:

```sql
-- পুরো table structure + data মুছে ফেলো
DROP TABLE temp_staging;

-- Cascade — dependent tables-ও মুছো
DROP TABLE accounts CASCADE;  -- ⚠️ transactions-ও মুছে যাবে!

-- Safe drop
DROP TABLE IF EXISTS temp_table;  -- না থাকলে error নেই

-- বৈশিষ্ট্য:
-- Table + data + index + constraint সব মুছে যায়
-- Rollback করা যায় না ❌ (DDL operation)
-- Banking-এ production-এ DROP করবে না!

-- Banking use:
DROP TABLE temp_migration_20240115;  -- Migration শেষে temp table
DROP TABLE old_archive_2019;        -- পুরনো archive
```

---

### পার্থক্য এক জায়গায়:

| | DELETE | TRUNCATE | DROP |
|---|---|---|---|
| কী মুছে | Selected rows | সব rows | Table + সব কিছু |
| WHERE | ✅ হ্যাঁ | ❌ না | ❌ না |
| Rollback | ✅ হ্যাঁ | ✅ (PostgreSQL) | ❌ না |
| Trigger | ✅ fire হয় | ❌ না | ❌ না |
| Speed | ধীর (row-by-row) | দ্রুত | দ্রুত |
| Auto-increment | Reset হয় না | Reset হয় | N/A |
| Structure | রাখে | রাখে | মুছে দেয় |
| DML/DDL | DML | DDL | DDL |
| Banking use | Selective cleanup | Temp table clear | Temp table remove |

---

### ⚠️ Tricky Interview Questions:

```sql
-- ১. TRUNCATE vs DELETE — কোনটা দ্রুত কেন?
-- DELETE: প্রতিটা row WAL-এ log করে, trigger চালায়
-- TRUNCATE: data page deallocate করে, row-level log নেই
-- ১০ লাখ row → DELETE: মিনিট, TRUNCATE: সেকেন্ড

-- ২. DELETE-এ WHERE না দিলে কি TRUNCATE-এর মতো?
DELETE FROM transactions;   -- সব মুছে কিন্তু TRUNCATE-এর চেয়ে slow
-- কারণ এখনো row-by-row log হয়, trigger fire হয়

-- ৩. TRUNCATE-এ Foreign Key থাকলে?
TRUNCATE TABLE accounts;
-- ERROR: পারবে না যদি transactions table-এ FK থাকে
-- ✅ Fix:
TRUNCATE TABLE accounts CASCADE;  -- child tables-ও truncate

-- ৪. DROP করার পরে Rollback?
BEGIN;
DROP TABLE accounts;
ROLLBACK;   -- PostgreSQL-এ কাজ করে ✅ (DDL transactional)
            -- MySQL-এ কাজ করে না ❌
```

---

### 🎯 Interview Closing line:

> *"Transaction-এ সবচেয়ে গুরুত্বপূর্ণ হলো isolation level choice — banking-এ balance check-এ Repeatable Read, transfer-এ Serializable। Deadlock prevent করার সবচেয়ে কার্যকর উপায় হলো consistent lock ordering — সবসময় ছোট ID আগে lock নিলে circular wait হওয়া সম্ভব না। DELETE vs TRUNCATE-এ banking production-এ সবসময় DELETE — কারণ WHERE clause দিয়ে selective, rollback করা যায়, trigger fire হয় তাই audit log তৈরি হয়। TRUNCATE শুধু temp বা staging table-এ।"*

## Slow Query Optimization, Stored Procedures, HAVING vs WHERE

---

## ১. Slow Query কীভাবে Optimize করবে

---

### Step 1 — আগে খুঁজে বের করো:

```sql
-- PostgreSQL: কোন query সবচেয়ে slow?
SELECT query,
       calls,
       round(total_exec_time::numeric, 2) as total_ms,
       round(mean_exec_time::numeric, 2)  as avg_ms,
       rows
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- MySQL: Slow query log
SET GLOBAL slow_query_log    = 'ON';
SET GLOBAL long_query_time   = 1;    -- 1 second-এর বেশি log করো
SET GLOBAL slow_query_log_file = '/var/log/mysql/slow.log';

-- Django-তে all queries দেখো (development)
from django.db import connection
print(len(connection.queries))
for q in connection.queries:
    print(q["time"], q["sql"])
```

---

### Step 2 — EXPLAIN ANALYZE দিয়ে diagnose করো:

```sql
EXPLAIN ANALYZE
SELECT t.txn_id, t.amount, a.name
FROM transactions t
JOIN accounts a ON t.account_id = a.id
WHERE t.created_at > NOW() - INTERVAL '30 days'
AND   a.is_active = TRUE
ORDER BY t.created_at DESC;

-- Output দেখার নিয়ম:
-- Seq Scan      → index নেই 😱 → index দাও
-- Index Scan    → index আছে ✅
-- Index Only Scan → covering index ✅ (best)
-- Hash Join     → large table join
-- Nested Loop   → small table join
-- Sort          → ORDER BY-এ index নেই
-- cost=X..Y     → Y কম হলে ভালো
-- rows=N        → আনুমানিক row count
-- actual time   → real execution time (ms)
```

---

### Step 3 — সবচেয়ে Common Problems + Fix:

**সমস্যা ১ — Missing Index:**
```sql
-- ❌ Seq Scan দেখলে
SELECT * FROM transactions WHERE account_id = 'SB-001';
-- Execution: 800ms, Seq Scan on transactions (rows=1000000)

-- ✅ Fix: Index দাও
CREATE INDEX idx_txn_account ON transactions(account_id);
-- Execution: 1ms, Index Scan ✅
```

**সমস্যা ২ — Index-এ Function ব্যবহার:**
```sql
-- ❌ Index use হবে না
WHERE YEAR(created_at) = 2024
WHERE LOWER(name) = 'sourov'
WHERE DATE(created_at) = '2024-01-15'

-- ✅ Fix: Function এড়াও
WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31'
WHERE name = 'Sourov'   -- Case-insensitive দরকার হলে:

-- Expression index বানাও
CREATE INDEX idx_lower_name ON accounts(LOWER(name));
WHERE LOWER(name) = 'sourov'  -- এখন index use করবে ✅
```

**সমস্যা ৩ — SELECT \* এড়াও:**
```sql
-- ❌ সব column আনে — unnecessary data transfer
SELECT * FROM transactions WHERE account_id = 'SB-001';

-- ✅ শুধু দরকারি columns
SELECT txn_id, amount, created_at
FROM transactions WHERE account_id = 'SB-001';

-- Covering index → table access-ই লাগবে না
CREATE INDEX idx_covering
ON transactions(account_id)
INCLUDE (amount, created_at);
-- Index Only Scan ✅ (fastest)
```

**সমস্যা ৪ — N+1 Query:**
```python
# ❌ N+1 — 101 queries
accounts = Account.objects.all()  # 1 query
for acc in accounts:
    print(acc.branch.name)        # 100 queries 😱

# ✅ select_related — 1 query (JOIN)
accounts = Account.objects.select_related("branch").all()

# ✅ prefetch_related — 2 queries
accounts = Account.objects.prefetch_related("transactions").all()
```

**সমস্যা ৫ — OR-এর বদলে UNION:**
```sql
-- ❌ OR → index use নাও হতে পারে
SELECT * FROM accounts
WHERE account_type = 'SB' OR branch_id = 'B1';

-- ✅ UNION → প্রতিটা আলাদা index use করে
SELECT * FROM accounts WHERE account_type = 'SB'
UNION
SELECT * FROM accounts WHERE branch_id = 'B1';
```

**সমস্যা ৬ — NOT IN-এর বদলে NOT EXISTS:**
```sql
-- ❌ NOT IN → NULL handling সমস্যা + slow
SELECT * FROM accounts
WHERE account_id NOT IN (SELECT account_id FROM blacklist);

-- ✅ NOT EXISTS → দ্রুত, NULL safe
SELECT * FROM accounts a
WHERE NOT EXISTS (
    SELECT 1 FROM blacklist b
    WHERE b.account_id = a.account_id
);
```

**সমস্যা ৭ — Pagination optimization:**
```sql
-- ❌ Large offset → সব scan করে তারপর skip করে
SELECT * FROM transactions
ORDER BY id LIMIT 20 OFFSET 900000;   -- 900000 rows scan! 😱

-- ✅ Keyset/Cursor pagination
SELECT * FROM transactions
WHERE id > 900000          -- last seen id
ORDER BY id LIMIT 20;      -- সরাসরি index থেকে ✅
```

**সমস্যা ৮ — Unnecessary JOIN:**
```sql
-- ❌ JOIN শুধু একটা column-এর জন্য
SELECT t.amount, a.name
FROM transactions t
JOIN accounts a ON t.account_id = a.id;  -- name-এর জন্য join

-- ✅ Denormalize করো (read-heavy table-এ)
-- transactions-এ account_name রেখে দাও
-- বা subquery দিয়ে
SELECT t.amount,
       (SELECT name FROM accounts WHERE id = t.account_id) as name
FROM transactions t
WHERE t.account_id = 'SB-001';
-- শুধু দরকারি row-এর জন্য subquery চলবে
```

---

### Step 4 — Query Rewrite — Banking Example:

```sql
-- ❌ Original slow query (2500ms):
SELECT a.name,
       SUM(t.amount) as total,
       COUNT(*) as count
FROM accounts a
JOIN transactions t ON a.id = t.account_id
WHERE YEAR(t.created_at) = 2024
AND   a.is_active = TRUE
AND   a.account_type IN ('SB', 'CA')
GROUP BY a.id, a.name
HAVING SUM(t.amount) > 100000
ORDER BY total DESC;

-- ✅ Optimized query (45ms):
-- Step 1: transactions আগে filter করো (rows কমাও)
-- Step 2: Function সরাও index ব্যবহারের জন্য
-- Step 3: Needed columns শুধু

WITH filtered_txns AS (
    SELECT account_id,
           SUM(amount)  as total,
           COUNT(*)     as txn_count
    FROM transactions
    WHERE created_at >= '2024-01-01'    -- ✅ function নেই
    AND   created_at <  '2025-01-01'    -- index use করবে
    GROUP BY account_id
    HAVING SUM(amount) > 100000         -- HAVING aggregation-এ
)
SELECT a.name, ft.total, ft.txn_count
FROM filtered_txns ft
JOIN accounts a ON ft.account_id = a.id
WHERE a.is_active    = TRUE
AND   a.account_type IN ('SB', 'CA');

-- Index যোগ করো:
CREATE INDEX idx_txn_date_acc
ON transactions(created_at, account_id)
INCLUDE (amount);
```

---

### Optimization Checklist:

| সমস্যা | লক্ষণ | Fix |
|---|---|---|
| Missing index | Seq Scan | `CREATE INDEX` |
| Function on column | Index skip হয় | Expression index বা rewrite |
| SELECT * | বেশি data transfer | Specific columns |
| N+1 | অনেক ছোট query | `select_related` / JOIN |
| Large OFFSET | Slow pagination | Keyset pagination |
| NOT IN | Slow + NULL issue | NOT EXISTS |
| OR | Index miss | UNION |

---

## ২. Stored Procedure কী?

> Stored Procedure = Database-এ stored একটা reusable SQL program — application থেকে call করলে DB-তেই execute হয়।

---

### 💻 Basic Stored Procedure:

```sql
-- PostgreSQL
CREATE OR REPLACE PROCEDURE transfer_money(
    p_from_id  VARCHAR(20),
    p_to_id    VARCHAR(20),
    p_amount   DECIMAL(15,2)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_from_balance DECIMAL(15,2);
BEGIN
    -- Balance check
    SELECT balance INTO v_from_balance
    FROM accounts
    WHERE account_id = p_from_id
    FOR UPDATE;

    IF v_from_balance < p_amount THEN
        RAISE EXCEPTION 'Insufficient balance: % < %',
                        v_from_balance, p_amount;
    END IF;

    -- Debit
    UPDATE accounts
    SET balance = balance - p_amount
    WHERE account_id = p_from_id;

    -- Credit
    UPDATE accounts
    SET balance = balance + p_amount
    WHERE account_id = p_to_id;

    -- Log
    INSERT INTO transactions(account_id, txn_type, amount)
    VALUES (p_from_id, 'DR', p_amount),
           (p_to_id,   'CR', p_amount);

    COMMIT;

EXCEPTION WHEN OTHERS THEN
    ROLLBACK;
    RAISE;
END;
$$;

-- Call করো
CALL transfer_money('SB-001', 'SB-002', 5000);
```

---

### 💻 Banking-এ Real Stored Procedure:

```sql
-- Monthly interest calculation
CREATE OR REPLACE PROCEDURE calculate_monthly_interest()
LANGUAGE plpgsql
AS $$
DECLARE
    v_account  RECORD;
    v_interest DECIMAL(15,2);
BEGIN
    FOR v_account IN
        SELECT account_id, balance, interest_rate
        FROM accounts
        WHERE account_type = 'SB'
        AND   is_active = TRUE
    LOOP
        v_interest := v_account.balance * v_account.interest_rate / 12;

        UPDATE accounts
        SET balance = balance + v_interest
        WHERE account_id = v_account.account_id;

        INSERT INTO transactions(account_id, txn_type, amount, description)
        VALUES (v_account.account_id, 'CR', v_interest, 'Monthly interest');
    END LOOP;

    COMMIT;
    RAISE NOTICE 'Interest calculation completed';
END;
$$;

-- Scheduled call (pg_cron দিয়ে)
SELECT cron.schedule('monthly-interest',
                     '0 0 1 * *',        -- প্রতি মাসের ১ তারিখে
                     'CALL calculate_monthly_interest()');
```

---

### Stored Procedure vs Function:

```sql
-- Function — value return করে, SELECT-এ use হয়
CREATE FUNCTION get_balance(p_account_id VARCHAR)
RETURNS DECIMAL AS $$
    SELECT balance FROM accounts WHERE account_id = p_account_id;
$$ LANGUAGE SQL;

-- Use:
SELECT get_balance('SB-001');   -- SELECT-এ ✅

-- Procedure — action করে, CALL দিয়ে চালায়
-- Transaction control করতে পারে (COMMIT/ROLLBACK)
CALL transfer_money('SB-001', 'SB-002', 5000);
```

---

### কখন Stored Procedure use করবে:

```
✅ Use করো:
- Complex multi-step DB operation (transfer, interest calc)
- Batch processing (month-end jobs)
- Business logic যা DB-তে থাকা দরকার
- Performance critical — network round-trip কমাতে
- Legacy system integration

❌ Avoid করো:
- Simple CRUD — ORM-ই যথেষ্ট
- Business logic যা test করা দরকার (unit test কঠিন)
- Microservice architecture — DB coupling বাড়ে
- Frequent change হয় এমন logic
```

---

### Django-তে Stored Procedure call:

```python
from django.db import connection

def transfer_money(from_id, to_id, amount):
    with connection.cursor() as cursor:
        cursor.execute(
            "CALL transfer_money(%s, %s, %s)",
            [from_id, to_id, amount]
        )

# Function call
def get_balance(account_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT get_balance(%s)",
            [account_id]
        )
        return cursor.fetchone()[0]
```

---

## ৩. HAVING vs WHERE

---

### 🔑 Core পার্থক্য:

```
WHERE   → rows filter করে (GROUP BY আগে)
HAVING  → groups filter করে (GROUP BY পরে)
```

```sql
-- Query execution order:
-- FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
--          ↑ rows filter      ↑ groups filter
```

---

### 💻 পার্থক্য দেখো:

```sql
-- WHERE: individual rows filter করে
SELECT account_id, SUM(amount)
FROM transactions
WHERE txn_type = 'DR'        -- ← rows filter (GROUP BY আগে)
GROUP BY account_id;

-- HAVING: aggregated groups filter করে
SELECT account_id, SUM(amount) as total
FROM transactions
GROUP BY account_id
HAVING SUM(amount) > 100000; -- ← groups filter (GROUP BY পরে)
```

---

### 💻 Banking Example — দুটো একসাথে:

```sql
-- সব active account-এর মধ্যে
-- যাদের ২০২৪-এ total debit ১ লাখের বেশি
SELECT a.name,
       COUNT(t.id)     as txn_count,
       SUM(t.amount)   as total_debit
FROM accounts a
JOIN transactions t ON a.id = t.account_id

WHERE a.is_active = TRUE           -- ① rows filter (inactive বাদ)
AND   t.txn_type  = 'DR'           -- ② rows filter (শুধু debit)
AND   t.created_at >= '2024-01-01' -- ③ rows filter (2024)

GROUP BY a.id, a.name

HAVING SUM(t.amount) > 100000      -- ④ group filter (১ লাখের বেশি)
AND    COUNT(t.id)   > 10          -- ⑤ group filter (১০-এর বেশি txn)

ORDER BY total_debit DESC;
```

**Execution flow:**
```
FROM accounts + transactions
  ↓
WHERE: is_active=TRUE, txn_type='DR', 2024 → 50,000 rows বাদ গেল
  ↓
GROUP BY account_id → groups তৈরি হলো
  ↓
HAVING: SUM > 100000 → ছোট groups বাদ গেল
  ↓
SELECT + ORDER BY → final result
```

---

### ⚠️ Tricky Cases:

```sql
-- ❌ HAVING-এ aggregate ছাড়া column — WHERE-এ রাখো
SELECT account_type, SUM(balance)
FROM accounts
GROUP BY account_type
HAVING account_type = 'SB';  -- ❌ কাজ করে কিন্তু wrong practice

-- ✅ সঠিক
SELECT account_type, SUM(balance)
FROM accounts
WHERE account_type = 'SB'    -- ✅ WHERE-এ রাখো — দ্রুত
GROUP BY account_type;

-- কারণ: WHERE আগে filter করে GROUP BY-র rows কমায়
-- HAVING-এ রাখলে সব group তৈরি হওয়ার পরে filter হয় → slow


-- ❌ WHERE-এ aggregate function — error!
SELECT account_id, SUM(amount)
FROM transactions
WHERE SUM(amount) > 100000   -- ❌ ERROR! WHERE aggregate জানে না
GROUP BY account_id;

-- ✅ HAVING-এ রাখো
SELECT account_id, SUM(amount)
FROM transactions
GROUP BY account_id
HAVING SUM(amount) > 100000; -- ✅


-- Alias — HAVING-এ use করা যায় না (PostgreSQL-এ)
SELECT account_id, SUM(amount) as total
FROM transactions
GROUP BY account_id
HAVING total > 100000;  -- ❌ PostgreSQL-এ error (MySQL-এ চলে)

-- ✅ Fix
HAVING SUM(amount) > 100000;  -- alias-এর বদলে expression
```

---

### 📊 HAVING vs WHERE Summary:

| | WHERE | HAVING |
|---|---|---|
| কখন চলে | GROUP BY-র আগে | GROUP BY-র পরে |
| কী filter করে | Individual rows | Aggregated groups |
| Aggregate function | ❌ না | ✅ হ্যাঁ |
| Performance | দ্রুত (আগে filter) | ধীর (পরে filter) |
| Use case | Row condition | Group condition |

---

### 🎯 Interview Closing line:

> *"Slow query optimize করার সময় সবার আগে EXPLAIN ANALYZE দেখি — Seq Scan মানেই index দরকার। Banking-এ সবচেয়ে common mistake হলো WHERE-এ function ব্যবহার যেমন YEAR(created_at) — এটা index ভেঙে দেয়, range query দিয়ে fix করি। Stored Procedure banking-এ monthly interest calculation আর transfer-এর মতো complex multi-step operation-এ ভালো — কারণ network round-trip কমে আর DB-তেই transaction control করা যায়। HAVING vs WHERE-এ rule হলো non-aggregate condition সবসময় WHERE-এ রাখো কারণ আগে filter করলে GROUP BY-তে কম rows যায়।"*



## Views, Banking Schema Design, Optimistic vs Pessimistic Locking

---

## ১. Database Views কী?

> View = একটা **stored SQL query** — real table-এর মতো ব্যবহার করা যায়, কিন্তু data আলাদাভাবে store হয় না।

সহজ analogy:
```
Table   = আসল বই
View    = বইয়ের সূচিপত্র
         আসল data আলাদা নেই
         যতবার দেখো ততবার fresh data
```

---

### 💻 Basic View:

```sql
-- View তৈরি করো
CREATE VIEW active_account_summary AS
SELECT
    a.account_id,
    a.name,
    a.balance,
    b.branch_name,
    COUNT(t.id)   as txn_count,
    MAX(t.created_at) as last_txn
FROM accounts a
JOIN branches b     ON a.branch_id = b.id
LEFT JOIN transactions t ON a.id = t.account_id
WHERE a.is_active = TRUE
GROUP BY a.id, a.name, a.balance, b.branch_name;

-- Table-এর মতো use করো
SELECT * FROM active_account_summary
WHERE balance > 50000;

-- Join করা যায়
SELECT v.name, v.balance, l.loan_amount
FROM active_account_summary v
JOIN loans l ON v.account_id = l.account_id;
```

---

### 💻 View-এর Types:

**Simple View — updatable:**
```sql
CREATE VIEW active_accounts AS
SELECT account_id, name, balance
FROM accounts
WHERE is_active = TRUE;

-- Update করা যায় (single table, no aggregation)
UPDATE active_accounts
SET balance = 60000
WHERE account_id = 'SB-001';
-- আসলে accounts table-এ update হয় ✅
```

**Complex View — read only:**
```sql
-- JOIN, GROUP BY, aggregation থাকলে updatable না
CREATE VIEW branch_summary AS
SELECT b.branch_name,
       COUNT(a.id)    as account_count,
       SUM(a.balance) as total_deposits
FROM branches b
JOIN accounts a ON b.id = a.branch_id
GROUP BY b.id, b.branch_name;

-- UPDATE করা যাবে না ❌
```

**Materialized View — data actually stored:**
```sql
-- Regular view: query চালালে real-time execute হয়
-- Materialized view: result store করে → অনেক দ্রুত

CREATE MATERIALIZED VIEW daily_transaction_summary AS
SELECT
    DATE(created_at)   as txn_date,
    account_id,
    SUM(CASE WHEN txn_type='DR' THEN amount ELSE 0 END) as total_debit,
    SUM(CASE WHEN txn_type='CR' THEN amount ELSE 0 END) as total_credit,
    COUNT(*)           as txn_count
FROM transactions
GROUP BY DATE(created_at), account_id;

-- Index দাও materialized view-এ
CREATE INDEX idx_mat_view_date
ON daily_transaction_summary(txn_date, account_id);

-- Refresh করো (নতুন data দেখাতে)
REFRESH MATERIALIZED VIEW daily_transaction_summary;

-- Concurrent refresh — lock নেয় না
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_transaction_summary;

-- Schedule: প্রতিদিন রাত ১২টায়
SELECT cron.schedule('refresh-summary',
    '0 0 * * *',
    'REFRESH MATERIALIZED VIEW CONCURRENTLY daily_transaction_summary'
);
```

---

### 💻 Banking-এ Real View Examples:

```sql
-- ১. Customer statement view
CREATE VIEW customer_statement AS
SELECT
    t.txn_id,
    t.created_at,
    t.txn_type,
    t.amount,
    t.balance_after,
    t.description,
    a.account_id,
    a.name       as account_holder
FROM transactions t
JOIN accounts a ON t.account_id = a.id
ORDER BY t.created_at DESC;

-- Use:
SELECT * FROM customer_statement
WHERE account_id = 'SB-001'
AND   created_at >= '2024-01-01';


-- ২. Security view — sensitive data hide করো
CREATE VIEW account_public_info AS
SELECT
    account_id,
    name,
    account_type,
    -- balance দেখাবে না (sensitive)
    -- pin দেখাবে না
    branch_id,
    is_active
FROM accounts;

-- API layer-এ accounts table-এর বদলে এই view use করো
GRANT SELECT ON account_public_info TO api_user;
REVOKE SELECT ON accounts FROM api_user;  -- direct access বন্ধ


-- ৩. Fraud detection view
CREATE VIEW suspicious_transactions AS
SELECT
    account_id,
    COUNT(*)      as txn_count,
    SUM(amount)   as total_amount,
    MAX(amount)   as max_single_txn
FROM transactions
WHERE created_at > NOW() - INTERVAL '1 hour'
GROUP BY account_id
HAVING COUNT(*) > 10          -- ১ ঘণ্টায় ১০-এর বেশি
OR     SUM(amount) > 500000;  -- বা ৫ লাখের বেশি
```

---

### View-এর সুবিধা ও সীমাবদ্ধতা:

| সুবিধা | সীমাবদ্ধতা |
|---|---|
| Complex query একবার লেখো | Complex view update করা যায় না |
| Security — sensitive column hide | Regular view-এ performance overhead |
| Business logic centralize | Materialized view stale হতে পারে |
| Consistent interface | Nested view debug কঠিন |

---

## ২. Banking Transaction System — Schema Design

---

### Design Principles:

```
১. Immutability     → Transaction কখনো delete/update হবে না
২. Audit Trail      → সব change log থাকবে
৩. Referential Integrity → FK constraint সবসময়
৪. Separation       → Account, Transaction, User আলাদা
৫. Soft Delete      → Data physically delete হবে না
```

---

### 💻 Complete Schema:

```sql
-- ══════════════════════════════════
-- CORE TABLES
-- ══════════════════════════════════

-- Users
CREATE TABLE users (
    id           BIGSERIAL PRIMARY KEY,
    username     VARCHAR(50)  UNIQUE NOT NULL,
    email        VARCHAR(100) UNIQUE NOT NULL,
    phone        VARCHAR(15)  UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active    BOOLEAN      DEFAULT TRUE,
    last_login   TIMESTAMPTZ,
    created_at   TIMESTAMPTZ  DEFAULT NOW()
);

-- Branches
CREATE TABLE branches (
    id           SERIAL PRIMARY KEY,
    branch_code  VARCHAR(10)  UNIQUE NOT NULL,
    branch_name  VARCHAR(100) NOT NULL,
    city         VARCHAR(50)  NOT NULL,
    address      TEXT,
    is_active    BOOLEAN      DEFAULT TRUE
);

-- Account Types (reference table)
CREATE TABLE account_types (
    code         VARCHAR(5)   PRIMARY KEY,  -- SB, CA, FD, LD
    name         VARCHAR(50)  NOT NULL,
    interest_rate DECIMAL(5,4) DEFAULT 0,
    daily_limit  DECIMAL(15,2) DEFAULT 50000,
    min_balance  DECIMAL(15,2) DEFAULT 0
);

INSERT INTO account_types VALUES
    ('SB', 'Savings',       0.0600, 50000,  500),
    ('CA', 'Current',       0.0200, 200000, 0),
    ('FD', 'Fixed Deposit', 0.0900, 0,      10000),
    ('LD', 'Loan',          0.1200, 0,      0);

-- Accounts
CREATE TABLE accounts (
    id              BIGSERIAL PRIMARY KEY,
    account_id      VARCHAR(20)  UNIQUE NOT NULL,
    user_id         BIGINT       NOT NULL REFERENCES users(id),
    branch_id       INTEGER      NOT NULL REFERENCES branches(id),
    account_type    VARCHAR(5)   NOT NULL REFERENCES account_types(code),
    balance         DECIMAL(15,2) NOT NULL DEFAULT 0,
    is_active       BOOLEAN      DEFAULT TRUE,
    is_frozen       BOOLEAN      DEFAULT FALSE,
    freeze_reason   TEXT,
    daily_used      DECIMAL(15,2) DEFAULT 0,  -- আজকের ব্যবহার
    daily_reset_at  DATE         DEFAULT CURRENT_DATE,
    opened_at       TIMESTAMPTZ  DEFAULT NOW(),
    closed_at       TIMESTAMPTZ,
    version         INTEGER      DEFAULT 0,   -- Optimistic locking

    CONSTRAINT balance_non_negative
        CHECK (balance >= 0),
    CONSTRAINT valid_account_id
        CHECK (account_id ~ '^[A-Z]{2}-[0-9]{6}$')
);

-- ══════════════════════════════════
-- TRANSACTION TABLES
-- ══════════════════════════════════

-- Transaction Categories
CREATE TABLE txn_categories (
    id    SERIAL PRIMARY KEY,
    code  VARCHAR(20) UNIQUE,  -- TRANSFER, WITHDRAWAL, DEPOSIT, BILL_PAY
    name  VARCHAR(50)
);

-- Main Transaction Table (IMMUTABLE — never update/delete)
CREATE TABLE transactions (
    id              BIGSERIAL PRIMARY KEY,
    txn_id          UUID         DEFAULT gen_random_uuid() UNIQUE,
    account_id      BIGINT       NOT NULL REFERENCES accounts(id),
    txn_type        CHAR(2)      NOT NULL CHECK (txn_type IN ('DR','CR')),
    amount          DECIMAL(15,2) NOT NULL CHECK (amount > 0),
    balance_before  DECIMAL(15,2) NOT NULL,
    balance_after   DECIMAL(15,2) NOT NULL,
    category_id     INTEGER      REFERENCES txn_categories(id),
    reference_txn   UUID,        -- Transfer-এর counterpart txn_id
    description     TEXT,
    channel         VARCHAR(20)  DEFAULT 'BRANCH',  -- ATM, MOBILE, BRANCH
    ip_address      INET,
    created_at      TIMESTAMPTZ  DEFAULT NOW(),
    created_by      BIGINT       REFERENCES users(id)
) PARTITION BY RANGE (created_at);  -- Monthly partition

-- Monthly partitions
CREATE TABLE transactions_2024_01
    PARTITION OF transactions
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
CREATE TABLE transactions_2024_02
    PARTITION OF transactions
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
-- ... বাকি মাস

-- Transfer Records (DR + CR link করে)
CREATE TABLE transfers (
    id              BIGSERIAL PRIMARY KEY,
    transfer_id     UUID         DEFAULT gen_random_uuid() UNIQUE,
    from_account_id BIGINT       NOT NULL REFERENCES accounts(id),
    to_account_id   BIGINT       NOT NULL REFERENCES accounts(id),
    amount          DECIMAL(15,2) NOT NULL,
    debit_txn_id    UUID         REFERENCES transactions(txn_id),
    credit_txn_id   UUID         REFERENCES transactions(txn_id),
    status          VARCHAR(20)  DEFAULT 'PENDING',
    initiated_by    BIGINT       REFERENCES users(id),
    created_at      TIMESTAMPTZ  DEFAULT NOW(),

    CONSTRAINT different_accounts
        CHECK (from_account_id != to_account_id)
);

-- ══════════════════════════════════
-- SECURITY & AUDIT TABLES
-- ══════════════════════════════════

-- Audit Log (IMMUTABLE)
CREATE TABLE audit_logs (
    id           BIGSERIAL PRIMARY KEY,
    table_name   VARCHAR(50)  NOT NULL,
    record_id    BIGINT       NOT NULL,
    action       VARCHAR(10)  CHECK (action IN ('INSERT','UPDATE','DELETE')),
    old_data     JSONB,
    new_data     JSONB,
    changed_by   BIGINT       REFERENCES users(id),
    ip_address   INET,
    changed_at   TIMESTAMPTZ  DEFAULT NOW()
);

-- Failed Login Attempts
CREATE TABLE login_attempts (
    id           BIGSERIAL PRIMARY KEY,
    user_id      BIGINT       REFERENCES users(id),
    ip_address   INET         NOT NULL,
    success      BOOLEAN      NOT NULL,
    attempted_at TIMESTAMPTZ  DEFAULT NOW()
);

-- ══════════════════════════════════
-- INDEXES
-- ══════════════════════════════════

-- Accounts
CREATE INDEX idx_account_user     ON accounts(user_id);
CREATE INDEX idx_account_branch   ON accounts(branch_id);
CREATE INDEX idx_account_active   ON accounts(account_id) WHERE is_active = TRUE;

-- Transactions (most queried)
CREATE INDEX idx_txn_account_date ON transactions(account_id, created_at DESC);
CREATE INDEX idx_txn_id           ON transactions(txn_id);
CREATE INDEX idx_txn_date         ON transactions(created_at DESC);
CREATE INDEX idx_txn_type_date    ON transactions(txn_type, created_at DESC);

-- Audit
CREATE INDEX idx_audit_table      ON audit_logs(table_name, record_id);
CREATE INDEX idx_audit_date       ON audit_logs(changed_at DESC);
```

---

### 💻 Transfer Operation — Schema use করে:

```python
from django.db import transaction as db_transaction
from decimal import Decimal
import uuid

def process_transfer(from_acc_id, to_acc_id, amount):

    with db_transaction.atomic():

        # Deadlock এড়াতে consistent order-এ lock
        accounts = Account.objects\
            .select_for_update()\
            .filter(id__in=[from_acc_id, to_acc_id])\
            .order_by("id")

        from_acc = next(a for a in accounts if a.id == from_acc_id)
        to_acc   = next(a for a in accounts if a.id == to_acc_id)

        # Validation
        if from_acc.is_frozen:
            raise AccountFrozenError(from_acc.account_id)
        if from_acc.balance < amount:
            raise InsufficientBalanceError(
                from_acc.account_id, amount, from_acc.balance
            )

        transfer_ref = uuid.uuid4()

        # Debit transaction (IMMUTABLE record)
        dr_txn = Transaction.objects.create(
            account_id     = from_acc.id,
            txn_type       = "DR",
            amount         = amount,
            balance_before = from_acc.balance,
            balance_after  = from_acc.balance - amount,
            reference_txn  = transfer_ref,
            description    = f"Transfer to {to_acc.account_id}"
        )

        # Credit transaction (IMMUTABLE record)
        cr_txn = Transaction.objects.create(
            account_id     = to_acc.id,
            txn_type       = "CR",
            amount         = amount,
            balance_before = to_acc.balance,
            balance_after  = to_acc.balance + amount,
            reference_txn  = transfer_ref,
            description    = f"Transfer from {from_acc.account_id}"
        )

        # Balance update
        from_acc.balance -= amount
        to_acc.balance   += amount
        from_acc.save()
        to_acc.save()

        # Transfer record
        Transfer.objects.create(
            transfer_id    = transfer_ref,
            from_account   = from_acc,
            to_account     = to_acc,
            amount         = amount,
            debit_txn_id   = dr_txn.txn_id,
            credit_txn_id  = cr_txn.txn_id,
            status         = "COMPLETED"
        )
```

---

## ৩. Optimistic vs Pessimistic Locking

---

### Pessimistic Locking — আগে Lock, তারপর কাজ:

> "কেউ না কেউ এসে data change করবেই — তাই আগে থেকেই lock নিয়ে রাখো।"

```python
# SELECT ... FOR UPDATE → Row lock নেয়
def withdraw_pessimistic(account_id, amount):
    with transaction.atomic():

        # Lock নিলো — অন্য transaction wait করবে
        account = Account.objects\
            .select_for_update()\
            .get(account_id=account_id)

        if account.balance < amount:
            raise InsufficientBalanceError(...)

        account.balance -= amount
        account.save()
        # Lock release হলো ✅

# SQL:
# SELECT * FROM accounts WHERE account_id='SB-001' FOR UPDATE;
# অন্য transaction এই row touch করতে পারবে না
```

```sql
-- Variants:
SELECT ... FOR UPDATE;           -- exclusive lock
SELECT ... FOR UPDATE NOWAIT;    -- lock না পেলে এখনই error
SELECT ... FOR UPDATE SKIP LOCKED; -- locked rows skip করো
SELECT ... FOR SHARE;            -- shared lock (read করতে দেয়)
```

**কখন Pessimistic:**
```
✅ High contention — একই row অনেকে একসাথে update করে
✅ Banking transfer — race condition সহ্য হয় না
✅ Inventory — stock negative হওয়া যাবে না
✅ Ticket booking — same seat দুজন নিতে পারবে না
```

---

### Optimistic Locking — আশা করো conflict হবে না:

> "Conflict rare — lock নেওয়ার overhead বেশি। Version check দিয়ে conflict detect করো।"

```python
# Model-এ version field
class Account(models.Model):
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    version = models.IntegerField(default=0)

def withdraw_optimistic(account_id, amount, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Lock ছাড়াই পড়ো
            account = Account.objects.get(account_id=account_id)

            if account.balance < amount:
                raise InsufficientBalanceError(...)

            old_version = account.version

            # Update-এ version check করো
            updated = Account.objects.filter(
                account_id = account_id,
                version    = old_version    # ← এটাই magic
            ).update(
                balance = account.balance - amount,
                version = old_version + 1   # version বাড়াও
            )

            if updated == 0:
                # version match হয়নি → কেউ আগে change করেছে
                raise ConcurrentModificationError("Retry needed")

            return True   # সফল ✅

        except ConcurrentModificationError:
            if attempt == max_retries - 1:
                raise
            time.sleep(0.1 * (attempt + 1))  # Exponential backoff

# SQL equivalent:
# UPDATE accounts
# SET balance = balance - 5000,
#     version = version + 1
# WHERE account_id = 'SB-001'
# AND   version = 5;      ← version match না হলে 0 rows updated
```

---

### Django-তে built-in Optimistic Locking:

```python
# select_for_update-এর বিকল্প — F() দিয়ে atomic update
from django.db.models import F

# Optimistic approach without version field
Account.objects.filter(
    account_id = "SB-001",
    balance__gte = amount    # balance check একসাথে
).update(
    balance = F("balance") - amount   # atomic operation
)
# 0 rows updated মানে balance ছিল না বা কেউ আগে নিয়েছে
```

---

### পার্থক্য এক নজরে:

| | Pessimistic | Optimistic |
|---|---|---|
| কীভাবে | Lock নেয় আগে | Version check করে শেষে |
| Conflict | Prevent করে | Detect করে |
| Performance | Low (wait করতে হয়) | High (lock নেই) |
| Contention | High-এ ভালো | Low-এ ভালো |
| Deadlock | সম্ভব | নেই |
| Retry | লাগে না | লাগতে পারে |
| Banking use | Transfer, Withdrawal | Profile update, Settings |

---

### 💻 Banking-এ কোনটা কোথায়:

```python
# Pessimistic — High contention operations
# Balance debit/credit → দুজন একসাথে তুলতে পারে
Account.objects.select_for_update().get(...)

# Optimistic — Low contention operations
# Profile update, notification settings → conflict rare
Account.objects.filter(
    id=account_id,
    version=current_version
).update(
    email=new_email,
    version=F("version") + 1
)

# Hybrid — চেক করে decide করো
def update_account(account_id, operation_type, data):
    if operation_type in ["withdraw", "transfer"]:
        # High contention → Pessimistic
        with transaction.atomic():
            account = Account.objects\
                .select_for_update().get(id=account_id)
            # ...
    else:
        # Low contention → Optimistic
        updated = Account.objects.filter(
            id=account_id, version=data["version"]
        ).update(**data)
        if not updated:
            raise StaleDataError("Data was modified, please refresh")
```

---

### 🎯 Interview Closing line:

> *"View banking-এ দুটো কাজে use করি — security-তে sensitive column hide করতে (balance, PIN) আর complex reporting query centralize করতে। Materialized View monthly statement-এর মতো heavy aggregation-এ কারণ real-time execute করা expensive। Schema design-এ সবচেয়ে গুরুত্বপূর্ণ হলো Transaction table immutable রাখা — কখনো update বা delete হবে না, শুধু insert। Locking-এ rule হলো balance withdrawal-এ pessimistic কারণ race condition সহ্য হয় না, কিন্তু profile update-এ optimistic কারণ conflict rare আর lock overhead বেশি।"*