## Database + NoSQL — Complete Guide

---

### SQL vs NoSQL

SQL = structured, table-based, fixed schema, ACID compliant। PostgreSQL, MySQL। Banking-এর মতো consistent data-এ perfect।

NoSQL = flexible schema, document/key-value/graph। MongoDB, Redis, Elasticsearch। High-scale, unstructured data-এ ভালো।

```
Banking transaction → SQL ✅ (ACID দরকার)
User activity log   → NoSQL ✅ (schema flexible)
```

---

### Primary Key vs Unique Key

```sql
-- Primary Key: NULL হবে না, একটাই থাকবে
account_id VARCHAR(20) PRIMARY KEY

-- Unique Key: NULL হতে পারে, একাধিক থাকতে পারে
email VARCHAR(100) UNIQUE
phone VARCHAR(15) UNIQUE

-- পার্থক্য:
-- Primary Key → Clustered Index তৈরি করে
-- Unique Key  → Non-clustered Index তৈরি করে
```

---

### Index কী

> Index = বইয়ের সূচিপত্র — পুরো table scan না করে দ্রুত data খোঁজার mechanism।

```sql
-- Without index: Full table scan → O(n)
SELECT * FROM accounts WHERE account_id = 'SB-001';
-- সব row দেখে 😱

-- With index: B-tree search → O(log n)
CREATE INDEX idx_account_id ON accounts(account_id);
-- সরাসরি যায় ✅

-- Banking-এ কোথায় index দেবে:
CREATE INDEX idx_txn_account_date
ON transactions(account_id, created_at DESC);

CREATE INDEX idx_account_user
ON accounts(user_id, is_active);
```

**Index-এর ভেতরে — B-Tree:**
```
        [SB-050]
       /         \
  [SB-025]    [SB-075]
  /     \      /     \
[SB-001][SB-030][SB-060][SB-090]
```

---

### Clustered vs Non-clustered Index

```sql
-- Clustered Index:
-- Data physically সেই order-এ store হয়
-- প্রতি table-এ একটাই হতে পারে
-- Primary Key automatically Clustered Index

-- PostgreSQL-এ:
CLUSTER accounts USING idx_account_id;
-- Data physically reorder হবে ✅

-- Non-clustered Index:
-- আলাদা structure — pointer রাখে actual data-এর দিকে
-- একটা table-এ অনেকগুলো হতে পারে
CREATE INDEX idx_name ON accounts(name);
CREATE INDEX idx_balance ON accounts(balance);
```

| | Clustered | Non-clustered |
|---|---|---|
| Data order | Physical | Logical (pointer) |
| Per table | ১টা | অনেক |
| Speed | দ্রুত (range) | কিছুটা ধীর |
| Storage | কম | বেশি |

---

### Normalization কী

> Data redundancy কমানো আর integrity বাড়ানোর process।

```
একই data বারবার না রেখে
আলাদা table-এ রাখো — relation দিয়ে যোগ করো
```

---

### 1NF, 2NF, 3NF

**1NF — Atomic values, no repeating groups:**
```sql
-- ❌ 1NF violate
account_id | phones
SB-001     | 01711, 01811   -- multiple values!

-- ✅ 1NF
account_id | phone
SB-001     | 01711
SB-001     | 01811
```

**2NF — 1NF + No partial dependency:**
```sql
-- ❌ 2NF violate (composite key: account_id + product_id)
account_id | product_id | account_name | product_name
SB-001     | P1         | Sourov       | Savings     -- account_name depends only on account_id

-- ✅ 2NF — separate করো
accounts: account_id | account_name
products: product_id | product_name
account_products: account_id | product_id
```

**3NF — 2NF + No transitive dependency:**
```sql
-- ❌ 3NF violate
account_id | branch_id | branch_name  -- branch_name depends on branch_id, not account_id

-- ✅ 3NF
accounts: account_id | branch_id
branches: branch_id  | branch_name
```

---

### Denormalization কখন

```sql
-- Performance দরকার হলে denormalize করো:

-- Join অনেক বেশি → slow query
-- Reporting/Analytics → read-heavy

-- Example: Transaction table-এ account_name রাখো
-- Join avoid করতে
transactions: txn_id | account_id | account_name | amount

-- ❌ Update anomaly হবে — account_name change হলে সব update করতে হবে
-- ✅ Read performance অনেক বাড়বে

-- Banking-এ কোথায়:
-- Statement generation → denormalized view
-- Dashboard analytics → materialized view
CREATE MATERIALIZED VIEW daily_summary AS
SELECT account_id, DATE(created_at), SUM(amount)
FROM transactions GROUP BY 1, 2;
```

---

### JOIN Types

```sql
-- Banking schema
accounts: account_id, name, branch_id
branches: branch_id, name, city
transactions: txn_id, account_id, amount

-- INNER JOIN → দুটোতেই match
SELECT a.name, b.name as branch
FROM accounts a
INNER JOIN branches b ON a.branch_id = b.branch_id;

-- LEFT JOIN → বাম table সব + match হলে ডান
SELECT a.name, b.name as branch
FROM accounts a
LEFT JOIN branches b ON a.branch_id = b.branch_id;
-- branch নেই এমন account-ও দেখাবে (NULL)

-- RIGHT JOIN → ডান table সব + match হলে বাম
SELECT a.name, b.name
FROM accounts a
RIGHT JOIN branches b ON a.branch_id = b.branch_id;
-- account নেই এমন branch-ও দেখাবে

-- FULL OUTER JOIN → দুটো table-এর সব
SELECT a.name, b.name
FROM accounts a
FULL OUTER JOIN branches b ON a.branch_id = b.branch_id;

-- CROSS JOIN → Cartesian product
SELECT a.name, b.name
FROM accounts a CROSS JOIN branches b;
-- n×m rows

-- SELF JOIN → একই table
SELECT a.name, m.name as manager
FROM employees a
JOIN employees m ON a.manager_id = m.id;
```

---

### INNER vs LEFT JOIN

```sql
-- INNER: শুধু match হলে
-- 100 accounts, 80-র branch আছে → 80 rows

-- LEFT: সব বাম + match
-- 100 accounts, 80-র branch আছে → 100 rows (20-তে NULL)

-- Banking use case:
-- সব account দেখাতে হবে, branch থাকুক বা না থাকুক → LEFT JOIN
SELECT a.account_id, a.name, COALESCE(b.name, 'No Branch') as branch
FROM accounts a
LEFT JOIN branches b ON a.branch_id = b.branch_id;
```

---

### Subquery vs JOIN

```sql
-- Subquery
SELECT * FROM accounts
WHERE balance > (
    SELECT AVG(balance) FROM accounts
);

-- Same result with JOIN (usually faster)
SELECT a.*
FROM accounts a
JOIN (SELECT AVG(balance) avg_bal FROM accounts) avg_table
ON a.balance > avg_table.avg_bal;

-- কখন কোনটা:
-- Subquery: একটা value দরকার, EXISTS check
-- JOIN: Multiple columns দরকার, large dataset

-- EXISTS (subquery) → দ্রুত
SELECT account_id FROM accounts a
WHERE EXISTS (
    SELECT 1 FROM transactions t
    WHERE t.account_id = a.account_id
    AND t.amount > 100000
);
```

---

### Transaction কী

> Transaction = **একটা logical unit of work** — সব হবে অথবা কিছুই না।

```sql
BEGIN;

UPDATE accounts SET balance = balance - 5000
WHERE account_id = 'SB-001';

UPDATE accounts SET balance = balance + 5000
WHERE account_id = 'SB-002';

-- এখানে error হলে দুটোই rollback
COMMIT;   -- সফল
-- বা
ROLLBACK; -- ব্যর্থ
```

---

### ACID Properties

```
A — Atomicity    → সব হবে অথবা কিছুই না
C — Consistency  → DB সবসময় valid state-এ থাকবে
I — Isolation    → একটা transaction অন্যটাকে affect করবে না
D — Durability   → Commit হলে data permanently save

Banking:
Transfer 5000 BDT:
A → Debit + Credit দুটোই হবে বা কোনোটাই না
C → Total balance আগে-পরে same থাকবে
I → অন্য transaction এই transfer দেখতে পারবে না (চলার সময়)
D → Power চলে গেলেও committed data থাকবে
```

---

### Isolation Levels

```sql
-- ১. Read Uncommitted — সবচেয়ে কম isolation
-- Dirty read সম্ভব — commit না হওয়া data দেখা যায়
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

-- ২. Read Committed — Default (PostgreSQL)
-- Dirty read নেই
-- Non-repeatable read সম্ভব
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- ৩. Repeatable Read — Default (MySQL)
-- Non-repeatable read নেই
-- Phantom read সম্ভব
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- ৪. Serializable — সবচেয়ে বেশি isolation
-- সব problem নেই কিন্তু slowest
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

| Level | Dirty Read | Non-repeatable | Phantom |
|---|---|---|---|
| Read Uncommitted | ✅ হয় | ✅ হয় | ✅ হয় |
| Read Committed | ❌ | ✅ হয় | ✅ হয় |
| Repeatable Read | ❌ | ❌ | ✅ হয় |
| Serializable | ❌ | ❌ | ❌ |

**Banking-এ:** Balance check → **Repeatable Read**, Audit → **Serializable**

---

### Deadlock কী

```sql
-- Transaction A                 Transaction B
BEGIN;                           BEGIN;
UPDATE accounts                  UPDATE accounts
SET balance = balance - 1000     SET balance = balance - 500
WHERE id = 1;  -- locks row 1    WHERE id = 2;  -- locks row 2

UPDATE accounts                  UPDATE accounts
SET balance = balance + 1000     SET balance = balance + 500
WHERE id = 2;  -- waits row 2    WHERE id = 1;  -- waits row 1
-- DEADLOCK! দুজন দুজনের জন্য অপেক্ষা করছে 😱

-- Fix:
-- সবসময় একই order-এ lock নাও
-- আগে id=1, তারপর id=2 — দুটো transaction-এই
-- PostgreSQL automatically detect করে একটাকে rollback করে
```

---

### Locking Mechanism

```sql
-- Row-level lock
SELECT * FROM accounts
WHERE account_id = 'SB-001'
FOR UPDATE;   -- এই row অন্য transaction পরিবর্তন করতে পারবে না

-- Shared lock (Read lock)
SELECT * FROM accounts FOR SHARE;
-- অন্যরা read করতে পারবে কিন্তু update করতে পারবে না

-- Advisory lock
SELECT pg_advisory_lock(42);
-- Custom lock — application-level

-- Django-তে:
Account.objects.select_for_update().get(id=1)
-- FOR UPDATE equivalent ✅

-- Optimistic Locking — version field
class Account(models.Model):
    balance = models.DecimalField(...)
    version = models.IntegerField(default=0)

UPDATE accounts SET balance=45000, version=version+1
WHERE id=1 AND version=5;
-- version match না হলে update fail → retry
```

---

### Query Optimization

```sql
-- ১. Index use করছে কিনা দেখো
EXPLAIN ANALYZE
SELECT * FROM transactions
WHERE account_id = 'SB-001'
AND created_at > '2024-01-01';

-- ২. Index যোগ করো
CREATE INDEX idx_txn_acc_date
ON transactions(account_id, created_at DESC);

-- ৩. SELECT * এড়াও
SELECT txn_id, amount, created_at   -- শুধু দরকারি fields
FROM transactions WHERE account_id = 'SB-001';

-- ৪. LIMIT use করো
SELECT * FROM transactions LIMIT 20 OFFSET 0;

-- ৫. Subquery-র বদলে JOIN
-- ৬. OR-এর বদলে UNION
SELECT * FROM accounts WHERE account_type = 'SB'
UNION
SELECT * FROM accounts WHERE account_type = 'CA';

-- ৭. NOT IN-এর বদলে NOT EXISTS
SELECT * FROM accounts a
WHERE NOT EXISTS (
    SELECT 1 FROM blacklist b WHERE b.account_id = a.account_id
);
```

---

### Explain Plan

```sql
-- EXPLAIN — query plan দেখায়
EXPLAIN SELECT * FROM transactions WHERE account_id = 'SB-001';

-- EXPLAIN ANALYZE — actually run করে, real time দেখায়
EXPLAIN ANALYZE
SELECT t.*, a.name
FROM transactions t
JOIN accounts a ON t.account_id = a.account_id
WHERE t.created_at > NOW() - INTERVAL '30 days';

-- Output দেখতে হয়:
-- Seq Scan   → Index নেই, full scan 😱
-- Index Scan → Index use করছে ✅
-- Nested Loop → Small dataset
-- Hash Join  → Large dataset
-- Sort       → ORDER BY-এ Index নেই

-- cost=0.00..1500.00 → কম cost ভালো
-- rows=1000 → আনুমানিক row count
-- actual time=0.050..15.000 → real time (ms)
```

---

### Slow Query Fix

```sql
-- Step 1: Slow query খুঁজো
-- PostgreSQL: pg_stat_statements
SELECT query, calls, total_time/calls avg_time, rows
FROM pg_stat_statements
ORDER BY avg_time DESC LIMIT 10;

-- MySQL: slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;  -- 1 second-এর বেশি

-- Step 2: EXPLAIN দিয়ে analyze করো
-- Step 3: Index যোগ করো
-- Step 4: Query rewrite করো
-- Step 5: Cache করো (Redis)

-- Common slow query patterns:
-- ❌ Function on indexed column
WHERE YEAR(created_at) = 2024   -- Index use হবে না!
-- ✅ Fix
WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31'

-- ❌ Leading wildcard
WHERE name LIKE '%Sourov%'   -- Full scan!
-- ✅ Full-text search use করো
WHERE to_tsvector(name) @@ to_tsquery('Sourov')

-- ❌ N+1
-- ✅ JOIN বা batch query
```

---

### Partitioning

```sql
-- Large table কে ছোট ছোট ভাগ করো
-- Query শুধু relevant partition scan করে

-- Range Partitioning — Banking transaction-এ perfect
CREATE TABLE transactions (
    txn_id SERIAL,
    account_id VARCHAR(20),
    amount DECIMAL(15,2),
    created_at TIMESTAMP
) PARTITION BY RANGE (created_at);

-- মাসিক partition
CREATE TABLE transactions_2024_01
PARTITION OF transactions
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE transactions_2024_02
PARTITION OF transactions
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Jan 2024 query → শুধু transactions_2024_01 scan করে ✅
SELECT * FROM transactions
WHERE created_at BETWEEN '2024-01-01' AND '2024-01-31';

-- List Partitioning
CREATE TABLE accounts PARTITION BY LIST (account_type);
CREATE TABLE accounts_savings PARTITION OF accounts
FOR VALUES IN ('SB');
CREATE TABLE accounts_current PARTITION OF accounts
FOR VALUES IN ('CA');
```

---

### Sharding

```
Horizontal scaling — data আলাদা আলাদা server-এ

Shard 1 (Server 1): account_id 1-1000000
Shard 2 (Server 2): account_id 1000001-2000000
Shard 3 (Server 3): account_id 2000001-3000000

Sharding strategies:
1. Range-based   → account_id range
2. Hash-based    → hash(account_id) % n_shards
3. Directory     → lookup table

Banking challenge:
Cross-shard transaction → distributed transaction দরকার
2-Phase Commit protocol use করতে হয়
```

---

### Replication

```sql
-- Primary → Replica (copy)

-- Streaming Replication (PostgreSQL)
-- Primary-এ:
ALTER SYSTEM SET wal_level = replica;
ALTER SYSTEM SET max_wal_senders = 3;

-- Replica-এ:
-- primary_conninfo = 'host=primary_ip port=5432'

-- Types:
-- Synchronous  → Primary commit করার আগে Replica confirm দেয়
--               Data loss নেই কিন্তু latency বেশি
-- Asynchronous → Primary commit করে, তারপর Replica update
--               Fast কিন্তু small data loss possible

-- Banking: Financial data → Synchronous ✅
ALTER SYSTEM SET synchronous_standby_names = 'replica1';
```

---

### Read Replica

```python
# Write → Primary, Read → Replica
# settings.py
DATABASES = {
    "default": {   # Write
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "primary-db.ucb.com",
    },
    "replica": {   # Read
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "replica-db.ucb.com",
    }
}

# Database Router
class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        return "replica"   # Read → Replica

    def db_for_write(self, model, **hints):
        return "default"   # Write → Primary

    def allow_relation(self, obj1, obj2, **hints):
        return True

# Use:
Account.objects.using("replica").filter(is_active=True)
Account.objects.create(...)   # Primary automatically
```

---

### Backup Strategy

```bash
# ১. Full Backup — সব data
pg_dump -Fc ucb_banking > backup_$(date +%Y%m%d).dump

# ২. Incremental — শুধু change
# WAL archiving enable করো
archive_command = 'cp %p /backup/wal/%f'

# ৩. Point-in-time Recovery (PITR)
pg_restore --target-time="2024-01-15 10:30:00" backup.dump

# Backup Strategy — Banking:
# Full backup   → Daily (রাত ২টায়)
# WAL archive   → Continuous (real-time)
# Replica       → Always on
# Retention     → 30 days minimum
# Test restore  → Monthly

# Automated backup script
0 2 * * * pg_dump ucb_banking | gzip > /backup/daily/$(date +\%Y\%m\%d).gz
```

---

### MySQL vs PostgreSQL

| | MySQL | PostgreSQL |
|---|---|---|
| **ACID** | ✅ InnoDB | ✅ Full |
| **JSON** | Basic | ✅ Advanced (JSONB) |
| **Full-text** | Basic | ✅ Advanced |
| **Window functions** | ✅ 8.0+ | ✅ |
| **Partitioning** | ✅ | ✅ Better |
| **Replication** | ✅ | ✅ |
| **Concurrency** | MVCC | ✅ Better MVCC |
| **Banking choice** | ✅ OK | ✅ Better |

> UCB-এর মতো banking-এ **PostgreSQL** — JSON support, better ACID, advanced indexing।

---

### JSON Field PostgreSQL

```sql
-- JSONB — binary stored, indexable, faster
ALTER TABLE accounts ADD COLUMN metadata JSONB;

-- Insert
UPDATE accounts SET metadata = '{
    "kyc_status": "verified",
    "nominee": {"name": "Rahim", "relation": "father"},
    "preferences": {"sms_alert": true, "email_alert": false}
}'::jsonb WHERE account_id = 'SB-001';

-- Query
SELECT * FROM accounts
WHERE metadata->>'kyc_status' = 'verified';

SELECT * FROM accounts
WHERE metadata->'preferences'->>'sms_alert' = 'true';

-- Index on JSONB
CREATE INDEX idx_kyc ON accounts USING GIN(metadata);

-- Django-তে:
class Account(models.Model):
    metadata = models.JSONField(default=dict)

Account.objects.filter(metadata__kyc_status="verified")
Account.objects.filter(metadata__preferences__sms_alert=True)
```

---

### Full-text Search

```sql
-- PostgreSQL Full-text Search
-- tsvector = searchable document
-- tsquery  = search query

-- Index তৈরি করো
ALTER TABLE accounts ADD COLUMN search_vector tsvector;

UPDATE accounts SET search_vector =
    to_tsvector('english', name || ' ' || account_id);

CREATE INDEX idx_search ON accounts USING GIN(search_vector);

-- Search করো
SELECT * FROM accounts
WHERE search_vector @@ to_tsquery('english', 'Sourov');

-- Partial match
WHERE search_vector @@ to_tsquery('english', 'Sou:*');

-- Ranking
SELECT *, ts_rank(search_vector, query) as rank
FROM accounts, to_tsquery('Sourov') query
WHERE search_vector @@ query
ORDER BY rank DESC;

-- Django-তে:
from django.contrib.postgres.search import SearchVector, SearchQuery

Account.objects.annotate(
    search=SearchVector("name", "account_id")
).filter(search=SearchQuery("Sourov"))
```

---

### Index Optimization

```sql
-- ১. Composite Index — column order matter করে
-- Most selective column আগে
CREATE INDEX idx_acc_type_balance
ON accounts(account_type, balance DESC);

-- ২. Partial Index — condition-based
CREATE INDEX idx_active_accounts
ON accounts(account_id)
WHERE is_active = TRUE;   -- শুধু active accounts index-এ

-- ৩. Covering Index — query সব data index থেকে পাবে
CREATE INDEX idx_covering
ON transactions(account_id)
INCLUDE (amount, created_at, txn_type);
-- Table access-ই লাগবে না ✅

-- ৪. Expression Index
CREATE INDEX idx_lower_name
ON accounts(LOWER(name));
-- WHERE LOWER(name) = 'sourov' → Index use করবে ✅

-- ৫. Index maintenance
REINDEX INDEX idx_account_id;  -- Bloated index rebuild
VACUUM ANALYZE accounts;       -- Statistics update

-- ৬. Unused index খুঁজো
SELECT indexrelname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0;   -- কখনো use হয়নি → drop করো
```

---

### Bulk Insert

```sql
-- ❌ Slow — একটা একটা করে
INSERT INTO transactions VALUES (1, 'SB-001', 500);
INSERT INTO transactions VALUES (2, 'SB-001', 1000);

-- ✅ COPY — সবচেয়ে দ্রুত
COPY transactions(account_id, amount, txn_type)
FROM '/tmp/transactions.csv' CSV HEADER;

-- ✅ Multi-row INSERT
INSERT INTO transactions(account_id, amount)
VALUES
    ('SB-001', 500),
    ('SB-002', 1000),
    ('SB-003', 750);

-- ✅ INSERT ... SELECT
INSERT INTO archive_transactions
SELECT * FROM transactions
WHERE created_at < '2023-01-01';

-- Django bulk_create
Transaction.objects.bulk_create([
    Transaction(account_id="SB-001", amount=500),
    Transaction(account_id="SB-002", amount=1000),
], batch_size=1000)   # ১০০০ করে insert করে
```

---

### Migration Strategy

```bash
# Production migration best practices:

# ১. Backward compatible migration আগে deploy করো
# নতুন column nullable রাখো
python manage.py makemigrations  # nullable column add
python manage.py migrate         # deploy
# তারপর application update করো
# তারপর NOT NULL করো

# ২. Large table migration — CONCURRENTLY
CREATE INDEX CONCURRENTLY idx_balance ON accounts(balance);
-- Table lock নেয় না ✅

# ৩. Zero-downtime migration steps:
# Step 1: নতুন column add (nullable)
# Step 2: Application দুটো column-ই write করে
# Step 3: Backfill data
# Step 4: Application নতুন column read করে
# Step 5: পুরনো column drop

# ৪. Migration rollback plan সবসময় রাখো
python manage.py migrate accounts 0010  # Rollback to 0010
```

---

### Schema Design

```sql
-- Banking schema — UCB style
CREATE TABLE accounts (
    id          BIGSERIAL PRIMARY KEY,
    account_id  VARCHAR(20) UNIQUE NOT NULL,
    user_id     BIGINT REFERENCES users(id),
    branch_id   INTEGER REFERENCES branches(id),
    account_type VARCHAR(2) CHECK (account_type IN ('SB','CA','FD','LD')),
    balance     DECIMAL(15,2) NOT NULL DEFAULT 0
                CHECK (balance >= 0),
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE transactions (
    id          BIGSERIAL PRIMARY KEY,
    txn_id      UUID DEFAULT gen_random_uuid() UNIQUE,
    account_id  BIGINT REFERENCES accounts(id),
    txn_type    CHAR(2) CHECK (txn_type IN ('DR','CR')),
    amount      DECIMAL(15,2) NOT NULL CHECK (amount > 0),
    balance_after DECIMAL(15,2) NOT NULL,
    description TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- Indexes
CREATE INDEX idx_txn_account ON transactions(account_id, created_at DESC);
CREATE INDEX idx_txn_id ON transactions(txn_id);
```

---

### Foreign Key Constraints

```sql
-- RESTRICT — parent delete করতে পারবে না child থাকলে
account_id BIGINT REFERENCES accounts(id) ON DELETE RESTRICT

-- CASCADE — parent delete হলে child-ও delete
ON DELETE CASCADE

-- SET NULL — parent delete হলে child-এর FK = NULL
ON DELETE SET NULL

-- SET DEFAULT — parent delete হলে child-এর FK = default
ON DELETE SET DEFAULT

-- Banking:
-- Transaction → Account: RESTRICT (account থাকলে delete করা যাবে না)
-- Document → Account: CASCADE (account delete হলে doc-ও যাবে)
-- Account → Branch: SET NULL (branch close হলে account থাকবে)
```

---

### Cascade Delete

```python
# Django-তে
class Transaction(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,   # Account delete করা যাবে না
    )

class Document(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,   # Account delete হলে doc-ও
    )

# Banking rule:
# Transaction → PROTECT (audit trail রাখতে হবে)
# Session → CASCADE (user delete হলে session-ও)
# Notification → CASCADE
```

---

### Soft Delete

```python
# Hard delete না — is_deleted flag

class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(User, null=True,
                                   on_delete=models.SET_NULL)

    def delete(self, deleted_by=None):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = deleted_by
        self.save()

    class Meta:
        abstract = True

# Custom Manager
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Account(SoftDeleteModel):
    objects = ActiveManager()   # Default: deleted বাদ
    all_objects = models.Manager()   # সব সহ
```

---

### Time-series Data Handling

```sql
-- TimescaleDB — PostgreSQL extension for time-series
CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE account_balance_history (
    time        TIMESTAMPTZ NOT NULL,
    account_id  VARCHAR(20),
    balance     DECIMAL(15,2)
);

-- Hypertable — automatically chunks করে
SELECT create_hypertable('account_balance_history', 'time');

-- Automatic compression
ALTER TABLE account_balance_history
SET (timescaledb.compress = true);

-- Retention policy — 2 বছর পরে delete
SELECT add_retention_policy('account_balance_history',
    INTERVAL '2 years');

-- Query
SELECT time_bucket('1 day', time) as day,
       account_id,
       LAST(balance, time) as closing_balance
FROM account_balance_history
WHERE time > NOW() - INTERVAL '30 days'
GROUP BY day, account_id;
```

---

### Audit Log Design

```sql
-- Audit log table
CREATE TABLE audit_logs (
    id          BIGSERIAL PRIMARY KEY,
    table_name  VARCHAR(50) NOT NULL,
    record_id   BIGINT NOT NULL,
    action      VARCHAR(10) CHECK (action IN ('INSERT','UPDATE','DELETE')),
    old_data    JSONB,
    new_data    JSONB,
    changed_by  BIGINT REFERENCES users(id),
    changed_at  TIMESTAMPTZ DEFAULT NOW(),
    ip_address  INET,
    user_agent  TEXT
);

-- PostgreSQL Trigger-এ auto audit
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_logs(table_name, record_id, action, old_data, new_data)
        VALUES (TG_TABLE_NAME, NEW.id, 'UPDATE', row_to_json(OLD), row_to_json(NEW));
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_logs(table_name, record_id, action, old_data)
        VALUES (TG_TABLE_NAME, OLD.id, 'DELETE', row_to_json(OLD));
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER accounts_audit
AFTER UPDATE OR DELETE ON accounts
FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();
```

---

### Multi-tenant DB Design

```sql
-- Approach 1: Shared DB, Schema per tenant (PostgreSQL)
CREATE SCHEMA tenant_ucb;
CREATE SCHEMA tenant_nrb;

SET search_path = tenant_ucb;
CREATE TABLE accounts (...);

-- Approach 2: Shared DB, Shared table, tenant_id column
CREATE TABLE accounts (
    id          BIGSERIAL PRIMARY KEY,
    tenant_id   VARCHAR(20) NOT NULL,   -- UCB, NRB, etc
    account_id  VARCHAR(20) NOT NULL,
    ...
);

CREATE INDEX idx_tenant ON accounts(tenant_id);

-- Row Level Security (PostgreSQL)
ALTER TABLE accounts ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON accounts
USING (tenant_id = current_setting('app.tenant_id'));

-- Application-এ:
SET app.tenant_id = 'UCB';
-- এখন শুধু UCB-এর data দেখাবে ✅

-- Approach 3: Separate DB per tenant (Best isolation)
-- Complex কিন্তু সবচেয়ে secure
```

---

### Connection Pooling

```python
# PgBouncer — PostgreSQL connection pool

# pgbouncer.ini
[databases]
ucb_banking = host=localhost port=5432 dbname=ucb_banking

[pgbouncer]
pool_mode = transaction    # Transaction-level pooling
max_client_conn = 1000     # সর্বোচ্চ client connection
default_pool_size = 20     # DB-তে সর্বোচ্চ connection

# Django settings — PgBouncer দিয়ে
DATABASES = {
    "default": {
        "HOST": "pgbouncer",   # Direct DB-এর বদলে
        "PORT": "6432",         # PgBouncer port
        "CONN_MAX_AGE": 0,      # PgBouncer নিজেই manage করে
    }
}

# SQLAlchemy pool
from sqlalchemy import create_engine
engine = create_engine(
    "postgresql://user:pass@localhost/db",
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600   # 1 hour-এ connection recycle
)
```

---

### ORM vs Raw SQL

```python
# ORM — readable, safe, maintainable
accounts = Account.objects\
    .filter(is_active=True, balance__gt=10000)\
    .select_related("branch")\
    .order_by("-balance")[:10]

# Raw SQL — complex query, performance critical
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("""
        WITH monthly_totals AS (
            SELECT account_id,
                   DATE_TRUNC('month', created_at) as month,
                   SUM(amount) as total
            FROM transactions
            WHERE txn_type = 'DR'
            GROUP BY 1, 2
        )
        SELECT a.name, mt.month, mt.total
        FROM monthly_totals mt
        JOIN accounts a ON mt.account_id = a.id
        WHERE mt.total > %s
        ORDER BY mt.total DESC
    """, [100000])
    results = cursor.fetchall()

# কখন কোনটা:
# ORM → CRUD, simple queries, rapid development
# Raw SQL → Complex analytics, CTE, Window functions, Performance critical
```

---

### DB Scaling

```
Vertical Scaling (Scale Up):
→ বড় server — বেশি RAM, CPU, SSD
→ সহজ কিন্তু limit আছে
→ Single point of failure

Horizontal Scaling (Scale Out):
→ অনেক server
→ Read Replica → Read load distribute করে
→ Sharding → Write load distribute করে
→ Partitioning → Single server-এ logical split

Banking scaling strategy:
1. Connection pooling (PgBouncer) — immediately
2. Read replica — read traffic 70-80% কমে
3. Caching (Redis) — frequent query cache করো
4. Partitioning — large table-এ
5. Sharding — extreme scale-এ
```

---

### High Availability

```
HA Setup — Banking:

                  Load Balancer
                 /             \
          Primary DB         Standby DB
          (Read/Write)    (Read + Failover)
               |                 |
          WAL Streaming ────────→|
          (Synchronous)

Failover:
Primary down → Standby promoted to Primary
Automatic failover: Patroni + etcd

tools:
- Patroni  → PostgreSQL HA manager
- HAProxy  → Load balancer
- etcd     → Consensus/leader election

RTO (Recovery Time Objective): < 30 seconds
RPO (Recovery Point Objective): 0 (Synchronous replication)
```

---

### MongoDB কী

> MongoDB = Document database — data JSON-like document-এ store করে। Schema নেই, flexible।

```javascript
// Collection = Table
// Document = Row (JSON format)

db.accounts.insertOne({
    account_id: "SB-001",
    name: "Sourov",
    balance: 50000,
    address: {           // Nested object — SQL-এ আলাদা table লাগতো
        city: "Dhaka",
        area: "Gulshan"
    },
    phones: ["01711", "01811"],   // Array
    kyc: {
        status: "verified",
        documents: ["nid", "photo"]
    }
})
```

---

### Document DB vs RDBMS

| | RDBMS | Document DB |
|---|---|---|
| **Schema** | Fixed | Flexible |
| **Relations** | JOIN | Embedded/Reference |
| **ACID** | ✅ Full | ✅ (4.0+) |
| **Scale** | Vertical | Horizontal |
| **Query** | SQL | Query API |
| **Use case** | Transactions | Catalog, CMS |

---

### Schema-less Design

```javascript
// একই collection-এ আলাদা structure
db.users.insertMany([
    {_id: 1, name: "Sourov", email: "s@ucb.com"},
    {_id: 2, name: "Karim", phone: "01711", age: 30},   // email নেই
    {_id: 3, name: "Rina", email: "r@ucb.com", premium: true}   // extra field
])

// Banking-এ benefit:
// KYC document type ভেদে আলাদা fields
db.kyc_documents.insertOne({
    account_id: "SB-001",
    doc_type: "NID",
    nid_number: "1234567890",
    issued_date: "2020-01-01"
    // Passport-এর জন্য আলাদা fields থাকবে
})
```

---

### Index in MongoDB

```javascript
// Single field index
db.accounts.createIndex({account_id: 1})  // 1 = ascending

// Compound index
db.transactions.createIndex({account_id: 1, created_at: -1})

// Text index — full-text search
db.accounts.createIndex({name: "text", description: "text"})
db.accounts.find({$text: {$search: "Sourov UCB"}})

// Partial index
db.accounts.createIndex(
    {balance: 1},
    {partialFilterExpression: {is_active: true}}
)

// TTL index — auto expire
db.sessions.createIndex(
    {created_at: 1},
    {expireAfterSeconds: 3600}   // 1 hour-এ auto delete
)

// Explain
db.transactions.find({account_id: "SB-001"}).explain("executionStats")
```

---

### Aggregation Pipeline

```javascript
// Pipeline = stages-এর chain
// Banking: Monthly transaction summary

db.transactions.aggregate([
    // Stage 1: Filter
    {$match: {
        created_at: {$gte: new Date("2024-01-01")},
        txn_type: "DR"
    }},

    // Stage 2: Group
    {$group: {
        _id: {
            account_id: "$account_id",
            month: {$dateToString: {format: "%Y-%m", date: "$created_at"}}
        },
        total_debit: {$sum: "$amount"},
        count: {$sum: 1},
        avg_amount: {$avg: "$amount"}
    }},

    // Stage 3: Filter on grouped data
    {$match: {total_debit: {$gt: 100000}}},

    // Stage 4: Sort
    {$sort: {total_debit: -1}},

    // Stage 5: Limit
    {$limit: 10},

    // Stage 6: Project — শুধু দরকারি fields
    {$project: {
        account_id: "$_id.account_id",
        month: "$_id.month",
        total_debit: 1,
        count: 1,
        _id: 0
    }}
])
```

---

### Sharding MongoDB

```javascript
// Shard key নির্বাচন — সবচেয়ে গুরুত্বপূর্ণ

// Enable sharding
sh.enableSharding("ucb_banking")

// Hashed sharding — even distribution
sh.shardCollection(
    "ucb_banking.transactions",
    {account_id: "hashed"}
)

// Range sharding — range query fast
sh.shardCollection(
    "ucb_banking.transactions",
    {created_at: 1}
)

// Bad shard key:
// Monotonically increasing (ObjectId) → hot spot
// Low cardinality (txn_type: DR/CR) → uneven

// Good shard key:
// account_id → high cardinality, even distribution
```

---

### Replication MongoDB

```javascript
// Replica Set — 3 nodes minimum
// Primary → Secondary → Secondary

// Initiate replica set
rs.initiate({
    _id: "ucb_rs",
    members: [
        {_id: 0, host: "primary:27017"},
        {_id: 1, host: "secondary1:27017"},
        {_id: 2, host: "secondary2:27017"}
    ]
})

// Write concern — data safety
db.transactions.insertOne(
    {amount: 5000},
    {writeConcern: {w: "majority", j: true}}
    // majority = বেশিরভাগ node confirm করলে ✅
)

// Read from secondary
db.getMongo().setReadPref("secondaryPreferred")
```

---

### CAP Theorem

```
CAP = Consistency, Availability, Partition Tolerance

একসাথে তিনটা পাওয়া impossible —
যেকোনো দুটো বেছে নিতে হবে

C — সব node একই data দেখে
A — সবসময় response পাবে
P — Network partition হলেও চলে

CP (Consistency + Partition):
→ MongoDB, HBase, ZooKeeper
→ Network issue হলে availability sacrifice করে
→ Banking transaction → CP ✅

AP (Availability + Partition):
→ Cassandra, DynamoDB, CouchDB
→ Network issue হলেও response দেয়, consistency later
→ Social media, DNS → AP

CA (Consistency + Availability):
→ Traditional RDBMS (Single node)
→ Real distributed system-এ P avoid করা যায় না
```

---

### ElasticSearch কী

> ElasticSearch = Distributed search engine — full-text search, log analysis, real-time analytics।

```python
from elasticsearch import Elasticsearch

es = Elasticsearch(["http://localhost:9200"])

# Index করো (=insert)
es.index(index="accounts", id="SB-001", body={
    "account_id": "SB-001",
    "name": "Sourov Ahmed",
    "address": "Gulshan, Dhaka",
    "balance": 50000
})

# Search করো
result = es.search(index="accounts", body={
    "query": {
        "multi_match": {
            "query": "Sourov Dhaka",
            "fields": ["name", "address"]
        }
    }
})

# Banking use case:
# Customer search (name, NID, phone)
# Transaction search
# Fraud pattern detection
# Log analysis
```

---

### Full-text Search কীভাবে কাজ করে

```
Text → Tokenization → Normalization → Inverted Index → Search

"Sourov Ahmed transfers money"
    ↓ Tokenize
["Sourov", "Ahmed", "transfers", "money"]
    ↓ Normalize (lowercase, stem)
["sourov", "ahmed", "transfer", "money"]
    ↓ Inverted Index-এ store

Search "transfer money":
→ "transfer" → doc1, doc3, doc5
→ "money"    → doc1, doc2, doc5
→ Intersection → doc1, doc5 (both match)
→ Ranking by relevance score
```

---

### Inverted Index

```
Word        → Documents (positions)

"sourov"    → [doc1(pos:0), doc3(pos:2)]
"ahmed"     → [doc1(pos:1), doc5(pos:0)]
"transfer"  → [doc1(pos:2), doc2(pos:0), doc5(pos:1)]
"dhaka"     → [doc2(pos:3), doc3(pos:1)]

Search "sourov transfer":
sourov  → doc1, doc3
transfer → doc1, doc2, doc5
Both    → doc1 ✅ (ranked highest)
```

---

### Tokenization

```python
# ElasticSearch tokenizer types:

# Standard tokenizer — word boundary-তে split
"Sourov Ahmed, Dhaka-1212" → ["Sourov", "Ahmed", "Dhaka", "1212"]

# Whitespace tokenizer
"Sourov Ahmed" → ["Sourov", "Ahmed"]

# N-gram tokenizer — partial match-এর জন্য
"Sourov" → ["Sou", "our", "uro", "rov"]  # 3-gram
# "our" search করলেও "Sourov" পাওয়া যাবে ✅

# Edge N-gram — prefix search
"Sourov" → ["S", "So", "Sou", "Sour", "Souro", "Sourov"]
# "Sou" search করলেও পাওয়া যাবে ✅

# Banking:
# Name search → Edge N-gram (prefix)
# Description search → Standard
# Account ID → Keyword (exact match)
```

---

### MongoDB vs PostgreSQL

| | MongoDB | PostgreSQL |
|---|---|---|
| **Schema** | Flexible | Fixed |
| **ACID** | ✅ 4.0+ | ✅ Full |
| **JOIN** | $lookup (slow) | ✅ Fast |
| **Transactions** | Multi-doc 4.0+ | ✅ |
| **Full-text** | Basic | ✅ Advanced |
| **JSON** | Native | ✅ JSONB |
| **Scaling** | ✅ Horizontal | Vertical + some |
| **Banking** | ❌ (use PostgreSQL) | ✅ |

---

### Use Case MongoDB

```
✅ MongoDB ভালো:
- Product catalog (e-commerce)
- User profiles (flexible attributes)
- CMS, Blog
- Real-time analytics
- IoT sensor data
- Session storage
- Event logs

❌ MongoDB ভালো না:
- Financial transactions (use PostgreSQL)
- Complex relationships
- Complex JOIN queries
- Strict ACID requirement
```

---

### Data Consistency Issue

```
Distributed system-এ consistency challenges:

1. Replication Lag
   Primary write → Replica-তে দেরিতে পৌঁছায়
   Secondary read করলে stale data পাওয়া যায়

2. Network Partition
   দুটো node communicate করতে পারছে না
   দুটোই write accept করলে conflict

3. Split Brain
   দুটো node নিজেকে primary মনে করে

Banking fix:
- Write-after-read: লেখার পরে পড়লে primary থেকে পড়ো
- Read Concern "majority": বেশিরভাগ node confirm করা data পড়ো
- Synchronous replication: Write confirm মানেই সব replica-তে আছে
```

---

### Eventual Consistency

```
Eventual Consistency:
→ এখন সব node same data না দেখালেও
→ কিছুক্ষণ পরে সব node same হয়ে যাবে

Example:
User A balance update করলো Primary-এ
User B এখনই Secondary থেকে পড়লে পুরনো balance দেখবে
5ms পরে Secondary sync হলে নতুন balance দেখাবে

কোথায় acceptable:
✅ Social media likes count
✅ Product view count
✅ Search index update
❌ Bank balance — Strong consistency দরকার
❌ Payment transaction
```

---

### Data Modeling MongoDB

```javascript
// Banking account model

// Embedded — related data একসাথে
{
    _id: ObjectId(),
    account_id: "SB-001",
    name: "Sourov",
    address: {              // Embedded
        street: "Road 5",
        city: "Dhaka"
    },
    nominee: {              // Embedded — সবসময় account-এর সাথে
        name: "Rahim",
        relation: "father",
        nid: "123456"
    }
}

// Referenced — separate collection
{
    _id: ObjectId(),
    account_id: "SB-001",
    branch_id: ObjectId("..."),  // Reference to branches collection
    user_id: ObjectId("...")     // Reference to users collection
}

// Hybrid
{
    account_id: "SB-001",
    branch: {                    // Embedded branch info (denormalized)
        branch_id: "B001",
        name: "Gulshan Branch"   // Join avoid করতে
    },
    recent_transactions: [       // Last 5 transactions embedded
        {amount: 500, date: "...", type: "DR"},
        {amount: 1000, date: "...", type: "CR"}
    ]
}
```

---

### Embedded vs Referenced

```
Embedded করো যখন:
✅ Data সবসময় একসাথে access হয়
✅ One-to-few relationship
✅ Data update কম হয়
✅ 16MB document limit-এর মধ্যে থাকে

Referenced করো যখন:
✅ Data independently access হয়
✅ One-to-many (অনেক বেশি)
✅ Data বারবার update হয়
✅ Many-to-many relationship

Banking:
Account + Nominee → Embedded (সাথেই দরকার হয়)
Account + Transactions → Referenced (millions হতে পারে)
Account + Branch → Reference + Embedded name (hybrid)
```

---

### Performance Tuning MongoDB

```javascript
// ১. Index use করছে কিনা দেখো
db.transactions.find({account_id: "SB-001"})
    .explain("executionStats")

// totalDocsExamined >> nReturned → Index নেই! 😱
// totalDocsExamined == nReturned → Index আছে ✅

// ২. Projection — দরকারি fields শুধু
db.transactions.find(
    {account_id: "SB-001"},
    {amount: 1, created_at: 1, _id: 0}   // শুধু এই দুটো
)

// ৩. Aggregation pipeline optimization
// $match আগে, $project পরে
// $sort-এর আগে $match করো
// $limit আগে করো যতটা পারো

// ৪. Read preference
db.getMongo().setReadPref("secondaryPreferred")

// ৫. Connection pooling
mongoose.connect(uri, {
    maxPoolSize: 10,
    serverSelectionTimeoutMS: 5000
})
```

---

### Large Dataset Handling

```python
# MongoDB — cursor দিয়ে
cursor = db.transactions.find({"account_id": "SB-001"})
for doc in cursor.batch_size(100):   # ১০০ করে fetch করে
    process(doc)

# PostgreSQL — server-side cursor
with connection.cursor("large_cursor") as cursor:
    cursor.execute("SELECT * FROM transactions")
    while True:
        rows = cursor.fetchmany(1000)
        if not rows:
            break
        process(rows)

# Django — iterator()
for txn in Transaction.objects.filter(
    account_id="SB-001"
).iterator(chunk_size=1000):
    process(txn)

# Streaming response — API-তে
import csv
from django.http import StreamingHttpResponse

def large_export(request):
    def generate():
        yield "txn_id,amount,date\n"
        for txn in Transaction.objects.all().iterator():
            yield f"{txn.txn_id},{txn.amount},{txn.created_at}\n"

    return StreamingHttpResponse(generate(), content_type="text/csv")
```

---

### Logging System Design

```python
# Centralized logging architecture

# Application → Filebeat → Logstash → Elasticsearch → Kibana
# (ELK Stack)

# Python logging → structured JSON
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "service": "banking-api",
            "message": record.getMessage(),
            "user_id": getattr(record, "user_id", None),
            "account_id": getattr(record, "account_id", None),
            "txn_id": getattr(record, "txn_id", None),
            "request_id": getattr(record, "request_id", None),
        })

# ElasticSearch index template
# logs-2024.01.15 → daily index
# ILM (Index Lifecycle Management):
# Hot (0-7 days) → SSD, fast
# Warm (7-30 days) → HDD, slower
# Cold (30-90 days) → compressed
# Delete (90+ days)
```

---

### Search System Design

```
Search System — Banking Customer Search

Architecture:
Application DB (PostgreSQL)
        ↓ (sync via Debezium/CDC)
Elasticsearch Index
        ↓
Search API → Client

Index mapping:
{
    "account_id": {"type": "keyword"},      // exact match
    "name": {"type": "text",                // full-text
              "analyzer": "standard",
              "fields": {
                  "keyword": {"type": "keyword"},  // exact sort
                  "suggest": {"type": "completion"} // autocomplete
              }},
    "phone": {"type": "keyword"},
    "address": {"type": "text"}
}

Search query:
- Name: multi_match with edge_ngram
- Phone: term (exact)
- Autocomplete: completion suggester
- Fuzzy search: fuzziness:1 (typo tolerance)
```

---

### Analytics DB vs Transactional DB

```
OLTP (Transactional) — PostgreSQL:
→ Short transactions
→ Many concurrent users
→ Row-oriented storage
→ INSERT/UPDATE/DELETE heavy
→ Normalized schema
→ Banking transactions, orders

OLAP (Analytics) — Redshift, BigQuery, ClickHouse:
→ Complex aggregation
→ Few concurrent queries
→ Column-oriented storage (fast aggregate)
→ SELECT heavy, read-only
→ Denormalized/Star schema
→ Monthly reports, trend analysis

Banking architecture:
PostgreSQL (OLTP) → ETL → Data Warehouse (OLAP)
Real-time: PostgreSQL read replica-তে analytics
Batch: nightly ETL to data warehouse
```

---

### Real-time System

```
Real-time banking:
1. WebSocket → balance update live দেখানো
2. Server-Sent Events → transaction notification
3. Redis Pub/Sub → event distribution
4. Kafka → event streaming

Django Channels + WebSocket:
```
```python
# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer

class BalanceConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope["user"]
        self.group_name = f"balance_{user.id}"
        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )
        await self.accept()

    async def balance_update(self, event):
        # Transaction হলে এই method call হবে
        await self.send(json.dumps({
            "type": "balance_update",
            "balance": event["balance"],
            "txn_id": event["txn_id"]
        }))

# Transaction হলে send করো
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()

async_to_sync(channel_layer.group_send)(
    f"balance_{account.user_id}",
    {"type": "balance_update", "balance": account.balance}
)
```

---

### Caching vs DB

```python
# Redis Cache → Frequently read, rarely changed data

# Cache-aside pattern
def get_account_balance(account_id):
    # Cache check
    cached = redis.get(f"balance:{account_id}")
    if cached:
        return float(cached)   # Cache hit ✅

    # DB থেকে পড়ো
    account = Account.objects.get(account_id=account_id)
    balance = account.balance

    # Cache-এ save করো (5 minutes)
    redis.setex(f"balance:{account_id}", 300, balance)

    return balance

# Write-through — লেখার সময় cache-ও update
def update_balance(account_id, new_balance):
    Account.objects.filter(account_id=account_id)\
        .update(balance=new_balance)
    redis.setex(f"balance:{account_id}", 300, new_balance)

# Cache invalidation
def invalidate_balance(account_id):
    redis.delete(f"balance:{account_id}")

# Banking-এ কী cache করবো:
# ✅ Exchange rates (1 minute TTL)
# ✅ Branch list (1 hour TTL)
# ✅ User profile (15 minute TTL)
# ❌ Account balance (transaction-এ stale হবে)
```

---

### Redis vs MongoDB

| | Redis | MongoDB |
|---|---|---|
| **Type** | In-memory K-V | Document DB |
| **Speed** | ✅ Fastest | দ্রুত |
| **Persistence** | Optional | ✅ Default |
| **Query** | Simple | Complex |
| **Data size** | RAM-limited | Disk |
| **Use case** | Cache, Session, Queue | Documents |

```
Banking:
Redis → Session, Cache, Rate limit, OTP, Queue
MongoDB → Activity logs, Notifications, Analytics
```

---

### Queue vs DB

```python
# Queue — Celery + Redis/RabbitMQ

# Task queue — async processing
from celery import Celery

app = Celery("banking")

@app.task(bind=True, max_retries=3)
def send_transaction_sms(self, account_id, amount, balance):
    try:
        sms_service.send(
            get_phone(account_id),
            f"TXN: {amount} BDT. Balance: {balance} BDT"
        )
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)

# View-এ:
def process_transaction(account_id, amount):
    # DB transaction sync
    with transaction.atomic():
        account.balance -= amount
        account.save()

    # SMS async — queue-এ পাঠাও
    send_transaction_sms.delay(account_id, amount, account.balance)
    # Request block হয় না ✅

# Queue কখন:
# Email/SMS sending
# PDF generation
# Report generation
# Third-party API calls
# Image processing
```

---

### Data Pipeline

```
Banking data pipeline:

Source Systems (PostgreSQL, MongoDB)
        ↓
CDC (Change Data Capture) — Debezium
        ↓
Message Queue (Kafka)
        ↓
Stream Processing (Spark Streaming / Flink)
        ↓
Data Warehouse (Redshift / BigQuery)
        ↓
BI Tools (Metabase / Tableau)

Real-time fraud detection pipeline:
Transaction event → Kafka → Flink → ML Model → Fraud score → Block/Allow
Latency: < 100ms ✅
```

---

### ETL Process

```python
# ETL = Extract, Transform, Load

# Extract — Source থেকে data নাও
def extract():
    return Transaction.objects.filter(
        created_at__date=yesterday()
    ).values("account_id", "amount", "txn_type", "created_at")

# Transform — Clean, enrich, aggregate করো
def transform(data):
    result = []
    for txn in data:
        result.append({
            "account_id": txn["account_id"],
            "date": txn["created_at"].date(),
            "amount": float(txn["amount"]),
            "txn_type": txn["txn_type"],
            "month": txn["created_at"].strftime("%Y-%m"),
            "quarter": f"Q{(txn['created_at'].month-1)//3+1}"
        })
    return result

# Load — Destination-এ load করো
def load(data):
    warehouse_db.bulk_insert("fact_transactions", data)

# Orchestration — Apache Airflow
from airflow import DAG
from airflow.operators.python import PythonOperator

dag = DAG("daily_etl", schedule_interval="0 3 * * *")  # রাত ৩টায়

extract_task = PythonOperator(task_id="extract", python_callable=extract)
transform_task = PythonOperator(task_id="transform", python_callable=transform)
load_task = PythonOperator(task_id="load", python_callable=load)

extract_task >> transform_task >> load_task
```

---

### System Design: Scalable Backend

```
UCB Banking — Scalable Architecture

┌─────────────────────────────────────────────┐
│              Client (Mobile/Web)            │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│           CDN (CloudFront/Cloudflare)        │
│           Static files, DDoS protection      │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│         API Gateway / Load Balancer          │
│         Rate limiting, SSL termination       │
└────────┬──────────────┬──────────────────────┘
         ↓              ↓
┌─────────────┐  ┌─────────────────────────────┐
│ Auth Service│  │      Banking API Service     │
│ JWT/OAuth2  │  │ (Django + Gunicorn × N pods) │
└─────────────┘  └──────────┬──────────────────┘
                            ↓
         ┌──────────────────┼──────────────────┐
         ↓                  ↓                  ↓
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  PostgreSQL  │    │    Redis    │    │  Celery     │
│  Primary    │    │  Cache      │    │  Workers    │
│     +       │    │  Session    │    │  (SMS/Email)│
│  Replica    │    │  Queue      │    └─────────────┘
└─────────────┘    └─────────────┘
         ↓
┌─────────────────────────────────────────────┐
│          Elasticsearch (Search + Logs)       │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│      Data Warehouse (Analytics + Reports)    │
└─────────────────────────────────────────────┘

Scaling numbers:
- API pods: 2-10 (auto-scale by CPU/RPS)
- DB connections: PgBouncer (1000 client → 20 DB)
- Cache hit rate: 80%+ (most reads from Redis)
- Celery workers: 5-20 (queue depth-based)
- Response time: p95 < 200ms
- Availability: 99.9% (8.7 hours downtime/year)
```

---

### 🎯 Final Interview Closing:

> *"Banking system-এ database choice সবচেয়ে critical decision। PostgreSQL ACID + JSONB + Full-text + Advanced indexing-এর কারণে primary datastore। Redis cache দিয়ে 80% read traffic absorb করি। ElasticSearch customer আর transaction search-এর জন্য। MongoDB activity log আর notification-এর জন্য। Query optimization-এ সবার আগে EXPLAIN ANALYZE দেখি — N+1 আর missing index দুটোই fix করলে 90% performance problem সমাধান হয়। Partition + Read Replica দিয়ে scale করি, Patroni দিয়ে HA maintain করি।"*