## Django Architecture

---

### 🔑 Django = MVT Architecture:

```
User Request
     ↓
  URLs (urls.py)        ← কোথায় যাবে?
     ↓
  View (views.py)       ← কী করবে?
     ↓
  Model (models.py)     ← Data কোথা থেকে?
     ↓
  Template (templates/) ← কীভাবে দেখাবে?
     ↓
User Response
```

> Django **MVT** — Model, View, Template
> MVC-র মতোই — তবে Controller-এর কাজ Django নিজেই করে।

---

### 🧠 MVT vs MVC:

| MVC | MVT (Django) | কাজ |
|---|---|---|
| Model | Model | Data + Business logic |
| View | Template | UI presentation |
| Controller | View | Request handle করে |
| Router | URLs | Route করে |

---

### 🏗️ Django-র Full Structure:

```
mybank/                     ← Project root
│
├── manage.py               ← Django CLI tool
├── requirements.txt
│
├── mybank/                 ← Project settings
│   ├── settings.py         ← Configuration
│   ├── urls.py             ← Main URL router
│   ├── wsgi.py             ← Production server
│   └── asgi.py             ← Async server
│
├── accounts/               ← App 1
│   ├── models.py           ← Database tables
│   ├── views.py            ← Business logic
│   ├── urls.py             ← App-level routes
│   ├── serializers.py      ← API data format
│   ├── admin.py            ← Admin panel
│   └── tests.py            ← Unit tests
│
├── transactions/           ← App 2
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
└── templates/              ← HTML files
```

---

### 💻 ১. Model — Database Layer:

```python
# accounts/models.py
from django.db import models

class Account(models.Model):
    ACCOUNT_TYPES = [
        ("SB", "Savings"),
        ("CA", "Current"),
        ("FD", "Fixed Deposit"),
    ]

    account_id   = models.CharField(max_length=20, unique=True)
    name         = models.CharField(max_length=100)
    account_type = models.CharField(max_length=2, choices=ACCOUNT_TYPES)
    balance      = models.DecimalField(max_digits=15, decimal_places=2)
    is_active    = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "accounts"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.account_id} — {self.name}"

    # Business logic model-এ রাখা যায়
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Invalid amount")
        self.balance += amount
        self.save()

    def can_withdraw(self, amount):
        return self.balance >= amount


class Transaction(models.Model):
    TXN_TYPES = [
        ("DR", "Debit"),
        ("CR", "Credit"),
    ]

    account    = models.ForeignKey(
                    Account,
                    on_delete=models.PROTECT,   # account delete হলে error
                    related_name="transactions"
                 )
    txn_type   = models.CharField(max_length=2, choices=TXN_TYPES)
    amount     = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transactions"
        indexes = [
            models.Index(fields=["account", "-created_at"])
        ]
```

---

### 💻 ২. URLs — Route Layer:

```python
# mybank/urls.py — Main router
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/transactions/", include("transactions.urls")),
]


# accounts/urls.py — App-level router
from django.urls import path
from . import views

urlpatterns = [
    path("", views.AccountListView.as_view(), name="account-list"),
    path("<str:account_id>/", views.AccountDetailView.as_view(), name="account-detail"),
    path("<str:account_id>/deposit/", views.DepositView.as_view(), name="deposit"),
    path("<str:account_id>/withdraw/", views.WithdrawView.as_view(), name="withdraw"),
    path("<str:account_id>/statement/", views.StatementView.as_view(), name="statement"),
]
```

---

### 💻 ৩. View — Logic Layer:

```python
# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer


class AccountDetailView(APIView):

    def get(self, request, account_id):
        try:
            account = Account.objects.get(account_id=account_id)
            serializer = AccountSerializer(account)
            return Response(serializer.data)

        except Account.DoesNotExist:
            return Response(
                {"error": "Account not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class WithdrawView(APIView):

    def post(self, request, account_id):
        amount = request.data.get("amount")

        try:
            # Atomic transaction — সব হবে নইলে rollback
            with transaction.atomic():
                account = Account.objects.select_for_update().get(
                    account_id=account_id
                )   # Row-level lock ✅

                if not account.is_active:
                    return Response(
                        {"error": "Account inactive"},
                        status=status.HTTP_403_FORBIDDEN
                    )

                if not account.can_withdraw(amount):
                    return Response(
                        {"error": "Insufficient balance"},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY
                    )

                # Balance update
                account.balance -= amount
                account.save()

                # Transaction log
                Transaction.objects.create(
                    account=account,
                    txn_type="DR",
                    amount=amount,
                    balance_after=account.balance,
                    description="Withdrawal"
                )

            return Response({
                "status": "success",
                "balance": account.balance
            })

        except Account.DoesNotExist:
            return Response(
                {"error": "Account not found"},
                status=status.HTTP_404_NOT_FOUND
            )
```

---

### 💻 ৪. Serializer — Data Format Layer:

```python
# accounts/serializers.py
from rest_framework import serializers
from .models import Account, Transaction

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ["account_id", "name", "account_type", "balance", "is_active"]
        read_only_fields = ["account_id", "balance"]

    # Custom validation
    def validate_balance(self, value):
        if value < 0:
            raise serializers.ValidationError("Balance cannot be negative")
        return value


class TransactionSerializer(serializers.ModelSerializer):
    account_id = serializers.CharField(source="account.account_id")

    class Meta:
        model = Transaction
        fields = ["id", "account_id", "txn_type", "amount",
                  "balance_after", "description", "created_at"]
```

---

### 💻 ৫. Settings — Configuration:

```python
# settings.py
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "rest_framework",      # DRF
    "corsheaders",         # CORS
    "accounts",            # our app
    "transactions",        # our app
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "ucb_banking",
        "USER": "ucb_user",
        "PASSWORD": "secret",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20
}
```

---

### 🔄 Full Request Lifecycle — একটা Request-এ কী হয়:

```
Client: POST /api/accounts/SB-001/withdraw/ {amount: 5000}
                      ↓
1. WSGI/ASGI         request receive করে
                      ↓
2. Middleware         Authentication check করে
   (JWT verify)      Permission check করে
                      ↓
3. URL Router        urls.py দেখে
   (urls.py)         WithdrawView match করে
                      ↓
4. View              Business logic চালায়
   (views.py)        Model-এ data পাঠায়
                      ↓
5. Model             Database query চালায়
   (models.py)       ORM → SQL → PostgreSQL
                      ↓
6. Serializer        Response data format করে
   (serializers.py)  JSON বানায়
                      ↓
7. Response          Client-এ পাঠায়
   HTTP 200          {status: "success", balance: 45000}
```

---

### 💻 Middleware — Request/Response Pipeline:

```python
# custom middleware
class BankingAuditMiddleware:
    """সব request/response log করে"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Request আসার আগে
        import time
        start = time.time()

        # View চালাও
        response = self.get_response(request)

        # Response যাওয়ার আগে
        duration = time.time() - start
        print(f"[{request.method}] {request.path} "
              f"→ {response.status_code} "
              f"({duration:.2f}s)")

        return response


# settings.py-তে add করো
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "mybank.middleware.BankingAuditMiddleware",   # custom ✅
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    ...
]
```

---

### 📊 Django-র Key Components:

| Component | File | কাজ |
|---|---|---|
| **Model** | `models.py` | Database schema + ORM |
| **View** | `views.py` | Business logic |
| **URL** | `urls.py` | Routing |
| **Serializer** | `serializers.py` | JSON conversion |
| **Middleware** | `middleware.py` | Request pipeline |
| **Settings** | `settings.py` | Configuration |
| **Admin** | `admin.py` | Admin dashboard |
| **Migration** | `migrations/` | DB schema version |

---

### 🎯 Interview Closing line:

> *"Django-র MVT architecture banking system-এর জন্য ideal — Model-এ data validation, View-এ business logic, Serializer-এ consistent API response। `transaction.atomic()` দিয়ে database consistency নিশ্চিত করা যায়, `select_for_update()` দিয়ে concurrent withdrawal-এ race condition এড়ানো যায়। Middleware দিয়ে authentication আর audit logging centrally handle হয় — প্রতিটা View-এ আলাদা করতে হয় না।"*

---

পরের গুরুত্বপূর্ণ topics:
- **Django ORM — Query Optimization**
- **JWT Authentication**
- **REST API Design**
- **SOLID Principles**

কোনটা নিয়ে আগাবে?

## Python Reflection API

---

### 🔑 এক কথায়:

> Reflection মানে — **runtime-এ** নিজের বা অন্য object সম্পর্কে **জানা, examine করা, এমনকি modify করা।** Code নিজেই নিজেকে inspect করতে পারে।

সহজ analogy:
```
Normal code  = অন্ধকারে কাজ করা
               কী আছে জানো না

Reflection   = আয়নায় নিজেকে দেখা
               runtime-এ জানতে পারো —
               এই object-এ কী কী আছে?
               কোন method আছে?
               কোন type?
```

---

### 🧠 Python Reflection-এর ৪টা স্তম্ভ:

```
Reflection API
├── 1. Introspection  → object সম্পর্কে জানো
├── 2. getattr/setattr → dynamically access করো
├── 3. inspect module → deep examine করো
└── 4. type/metaclass → class নিজেই modify করো
```

---

## ১. Introspection — Object সম্পর্কে জানো

---

### 💻 `type()` — কী ধরনের object:

```python
account = {"name": "Sourov", "balance": 50000}
amount = 5000
name = "UCB Bank"

print(type(account))   # <class 'dict'>
print(type(amount))    # <class 'int'>
print(type(name))      # <class 'str'>

# Class check
class BankAccount:
    pass

acc = BankAccount()
print(type(acc))              # <class '__main__.BankAccount'>
print(type(acc) == BankAccount)  # True
```

---

### 💻 `isinstance()` vs `type()`:

```python
class Account:
    pass

class SavingsAccount(Account):
    pass

acc = SavingsAccount()

# type() — exact match
print(type(acc) == Account)         # False ← parent match করে না
print(type(acc) == SavingsAccount)  # True

# isinstance() — inheritance chain দেখে
print(isinstance(acc, SavingsAccount))  # True
print(isinstance(acc, Account))         # True ✅ parent-ও match করে

# Banking-এ use:
def process(account):
    if isinstance(account, SavingsAccount):
        apply_savings_interest(account)
    elif isinstance(account, Account):
        apply_default_rules(account)
```

---

### 💻 `dir()` — কী কী আছে দেখো:

```python
class BankAccount:
    MAX_LIMIT = 500000

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

acc = BankAccount("Sourov", 50000)

# সব attributes আর methods দেখো
print(dir(acc))
# ['MAX_LIMIT', '__class__', '__init__', ...,
#  'balance', 'deposit', 'name', 'withdraw']

# Custom attributes filter করো (__ ছাড়া)
custom = [x for x in dir(acc) if not x.startswith("__")]
print(custom)
# ['MAX_LIMIT', 'balance', 'deposit', 'name', 'withdraw']
```

---

### 💻 `hasattr()`, `getattr()`, `setattr()`, `delattr()`:

```python
class BankAccount:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

acc = BankAccount("Sourov", 50000)

# hasattr — আছে কিনা check
print(hasattr(acc, "balance"))    # True
print(hasattr(acc, "loan"))       # False

# getattr — dynamically access করো
field = "balance"
print(getattr(acc, field))        # 50000

# Default value দেওয়া যায়
print(getattr(acc, "loan", 0))    # 0 (default)

# setattr — dynamically set করো
setattr(acc, "balance", 75000)
print(acc.balance)                # 75000

setattr(acc, "branch", "Dhaka")   # নতুন attribute ✅
print(acc.branch)                 # Dhaka

# delattr — dynamically delete করো
delattr(acc, "branch")
print(hasattr(acc, "branch"))     # False
```

---

## ২. Dynamic Method Call — Runtime-এ Method চালানো

---

### 💻 `getattr()` দিয়ে method call:

```python
class PaymentProcessor:
    def process_bkash(self, amount):
        print(f"Bkash: {amount} BDT")

    def process_nagad(self, amount):
        print(f"Nagad: {amount} BDT")

    def process_bank(self, amount):
        print(f"Bank transfer: {amount} BDT")


processor = PaymentProcessor()
payment_type = "bkash"   # Runtime-এ আসে

# ❌ Bad — if/elif chain
if payment_type == "bkash":
    processor.process_bkash(500)
elif payment_type == "nagad":
    processor.process_nagad(500)
elif payment_type == "bank":
    processor.process_bank(500)

# ✅ Good — Reflection দিয়ে dynamic call
method_name = f"process_{payment_type}"

if hasattr(processor, method_name):
    method = getattr(processor, method_name)
    method(500)   # Bkash: 500 BDT ✅
else:
    raise ValueError(f"Unknown payment type: {payment_type}")
```

---

### 💻 Banking — Dynamic Report Generator:

```python
class ReportGenerator:

    def generate_daily(self):
        return "Daily report data"

    def generate_weekly(self):
        return "Weekly report data"

    def generate_monthly(self):
        return "Monthly report data"

    def generate_annual(self):
        return "Annual report data"


def get_report(report_type: str):
    generator = ReportGenerator()
    method_name = f"generate_{report_type}"

    # Method আছে কিনা check
    if not hasattr(generator, method_name):
        raise ValueError(f"Report type '{report_type}' not supported")

    # Dynamic call
    method = getattr(generator, method_name)
    return method()

# Use:
print(get_report("daily"))    # Daily report data
print(get_report("monthly"))  # Monthly report data
print(get_report("yearly"))   # ValueError: not supported
```

---

## ৩. `inspect` Module — Deep Examination

---

### 💻 Function/Method সম্পর্কে জানো:

```python
import inspect

def transfer_money(from_account: str, to_account: str,
                   amount: float, note: str = "Transfer"):
    """
    একটা account থেকে অন্যটায় টাকা পাঠাও।
    """
    pass

# Parameters দেখো
sig = inspect.signature(transfer_money)
print(sig)
# (from_account: str, to_account: str,
#  amount: float, note: str = 'Transfer')

# প্রতিটা parameter detail
for name, param in sig.parameters.items():
    print(f"{name}: default={param.default}, "
          f"annotation={param.annotation}")
# from_account: default=<empty>, annotation=str
# to_account: default=<empty>, annotation=str
# amount: default=<empty>, annotation=float
# note: default=Transfer, annotation=str

# Docstring দেখো
print(inspect.getdoc(transfer_money))
# একটা account থেকে অন্যটায় টাকা পাঠাও।

# Source code দেখো
print(inspect.getsource(transfer_money))
```

---

### 💻 Class সম্পর্কে জানো:

```python
import inspect

class BankAccount:
    MAX_LIMIT = 500000

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def _validate(self, amount):
        return amount > 0

# সব methods দেখো
methods = inspect.getmembers(BankAccount, predicate=inspect.isfunction)
for name, method in methods:
    print(name)
# __init__
# _validate
# deposit

# Class hierarchy দেখো
print(inspect.getmro(BankAccount))
# (<class 'BankAccount'>, <class 'object'>)

# কোন file-এ আছে
print(inspect.getfile(BankAccount))
# /path/to/accounts/models.py
```

---

## ৪. `vars()` এবং `__dict__` — Object-এর ভেতরে:

```python
class Transaction:
    def __init__(self, txn_id, amount, txn_type):
        self.txn_id = txn_id
        self.amount = amount
        self.txn_type = txn_type

txn = Transaction("TXN-001", 5000, "DR")

# Object-এর সব attribute dict হিসেবে
print(vars(txn))
# {'txn_id': 'TXN-001', 'amount': 5000, 'txn_type': 'DR'}

print(txn.__dict__)
# {'txn_id': 'TXN-001', 'amount': 5000, 'txn_type': 'DR'}

# Dynamic update
txn.__dict__.update({"branch": "Dhaka", "status": "completed"})
print(txn.branch)    # Dhaka ✅
print(txn.status)    # completed ✅
```

---

## ৫. Real Banking Use Cases:

---

### 💻 Auto API Validator — Reflection দিয়ে:

```python
import inspect

def validate_request(func, data: dict):
    """
    Function-এর parameters দেখে
    automatically request validate করো
    """
    sig = inspect.signature(func)
    errors = []

    for name, param in sig.parameters.items():
        if name == "self":
            continue

        # Required field missing?
        if (param.default is inspect.Parameter.empty
                and name not in data):
            errors.append(f"'{name}' is required")

        # Type check
        if (name in data
                and param.annotation != inspect.Parameter.empty):
            expected = param.annotation
            if not isinstance(data[name], expected):
                errors.append(
                    f"'{name}' must be {expected.__name__}, "
                    f"got {type(data[name]).__name__}"
                )

    return errors


def transfer_money(from_account: str, to_account: str, amount: float):
    pass


# Test:
data = {"from_account": "SB-001", "amount": "5000"}  # to_account missing, amount wrong type

errors = validate_request(transfer_money, data)
print(errors)
# ["'to_account' is required",
#  "'amount' must be float, got str"]
```

---

### 💻 Dynamic Model Serializer:

```python
def serialize(obj, fields=None):
    """
    যেকোনো object-কে dict-এ convert করো
    Reflection দিয়ে — manually field লিখতে হবে না
    """
    data = {}
    attrs = vars(obj)

    for key, value in attrs.items():
        # Private field skip করো
        if key.startswith("_"):
            continue

        # Specific fields চাইলে filter করো
        if fields and key not in fields:
            continue

        data[key] = value

    return data


class Account:
    def __init__(self, account_id, name, balance, _pin):
        self.account_id = account_id
        self.name = name
        self.balance = balance
        self._pin = _pin   # private — serialize হবে না


acc = Account("SB-001", "Sourov", 50000, "1234")

print(serialize(acc))
# {'account_id': 'SB-001', 'name': 'Sourov', 'balance': 50000}
# _pin বাদ গেছে ✅

print(serialize(acc, fields=["name", "balance"]))
# {'name': 'Sourov', 'balance': 50000}
```

---

### 💻 Plugin System — Dynamic Loading:

```python
import importlib
import inspect

class PaymentGatewayLoader:
    """
    Runtime-এ payment gateway load করো
    নতুন gateway যোগ করতে core code change করতে হবে না
    """

    def load_gateway(self, gateway_name: str):
        # Dynamic module import
        module = importlib.import_module(
            f"payments.gateways.{gateway_name}"
        )

        # Module-এ সব class খোঁজো
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if hasattr(obj, "process_payment"):
                return obj()   # Gateway instance return ✅

        raise ValueError(f"No gateway found in {gateway_name}")

    def process(self, gateway_name, amount):
        gateway = self.load_gateway(gateway_name)
        return gateway.process_payment(amount)


# Use — নতুন gateway যোগ করতে শুধু file বানাও
loader = PaymentGatewayLoader()
loader.process("bkash", 500)     # payments/gateways/bkash.py ✅
loader.process("nagad", 1000)    # payments/gateways/nagad.py ✅
```

---

### 📊 Reflection API — সব Tools এক নজরে:

| Function | কাজ | Example |
|---|---|---|
| `type(obj)` | Type জানো | `type(acc)` → `BankAccount` |
| `isinstance(obj, cls)` | Type check | `isinstance(acc, Account)` |
| `hasattr(obj, name)` | Attribute আছে? | `hasattr(acc, "balance")` |
| `getattr(obj, name)` | Dynamic access | `getattr(acc, "balance")` |
| `setattr(obj, name, val)` | Dynamic set | `setattr(acc, "balance", 5000)` |
| `delattr(obj, name)` | Dynamic delete | `delattr(acc, "branch")` |
| `dir(obj)` | সব attributes | `dir(acc)` |
| `vars(obj)` | `__dict__` | `vars(acc)` |
| `inspect.signature()` | Parameters | function signature |
| `inspect.getmembers()` | সব members | class inspection |
| `inspect.getsource()` | Source code | debugging |
| `importlib.import_module()` | Dynamic import | plugin system |

---

### 🎯 Interview Closing line:

> *"Python-এর Reflection API banking system-এ অনেক জায়গায় কাজে লাগে। Dynamic payment gateway loading মানে নতুন Bkash বা Nagad integration-এ core code touch করতে হয় না — শুধু নতুন file বানালেই হয়। Auto request validation মানে প্রতিটা API-এ manually check লিখতে হয় না। Serializer মানে কোন field expose হবে সেটা runtime-এ control করা যায়। এটাই Open/Closed Principle — extend করা যাবে কিন্তু modify করতে হবে না।"*

---

পরের গুরুত্বপূর্ণ topics:
- **Django ORM + Query Optimization**
- **JWT Authentication**
- **REST API Design**
- **SOLID Principles**
- **Design Patterns**

কোনটা নিয়ে আগাবে?

## Django Request Lifecycle

---

### 🔑 এক কথায়:

> একটা HTTP request Django-তে ঢুকে Response হয়ে বের হওয়া পর্যন্ত **নির্দিষ্ট কিছু ধাপ** পার করে — এটাই Request Lifecycle।

---

### 🧠 Full Lifecycle — Bird's Eye View:

```
Client (Browser/Mobile)
         ↓  HTTP Request
    Web Server (Nginx)
         ↓
    WSGI/ASGI Server (Gunicorn)
         ↓
    Django Entry Point
         ↓
    Middleware (chain) ←─────────┐
         ↓                       │
    URL Router (urls.py)         │
         ↓                       │
    View (views.py)              │
         ↓                       │
    ORM → Database               │
         ↓                       │
    Serializer/Template          │
         ↓                       │
    Response ────────────────────┘
         ↓  HTTP Response
    Client
```

---

## ধাপ ১ — Web Server (Nginx):

```
Client → Nginx

Nginx কী করে:
├── Static files serve করে (CSS, JS, Images)
├── SSL/TLS terminate করে (HTTPS)
├── Load balance করে
└── Dynamic request → Gunicorn-এ পাঠায়
```

```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name ucb.com.bd;

    # Static files — Django-তে যাবে না
    location /static/ {
        alias /var/www/static/;   # Nginx নিজেই serve করে ✅
    }

    # Dynamic request — Gunicorn-এ
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

---

## ধাপ ২ — WSGI/ASGI Server:

```python
# wsgi.py — Sync (Traditional)
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mybank.settings")
application = get_wsgi_application()

# asgi.py — Async (Modern)
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mybank.settings")
application = get_asgi_application()
```

```
WSGI = Web Server Gateway Interface
     → Sync requests handle করে
     → Gunicorn, uWSGI

ASGI = Async Server Gateway Interface
     → Async + WebSocket handle করে
     → Uvicorn, Daphne
```

---

## ধাপ ৩ — Django Entry Point:

```python
# Django প্রথমে settings load করে
INSTALLED_APPS = ["accounts", "transactions", ...]
MIDDLEWARE = [...]
DATABASES = {...}

# তারপর WSGIHandler/ASGIHandler তৈরি হয়
# এটাই সব request-এর entry point
```

---

## ধাপ ৪ — Middleware Chain (সবচেয়ে গুরুত্বপূর্ণ):

```
Request আসছে ↓        Response যাচ্ছে ↑

SecurityMiddleware      →      SecurityMiddleware
SessionMiddleware       →      SessionMiddleware
AuthMiddleware          →      AuthMiddleware
CsrfMiddleware          →      CsrfMiddleware
MessageMiddleware       →      MessageMiddleware
CustomAuditMiddleware   →      CustomAuditMiddleware
         ↓                              ↑
        View                         View
```

> Middleware **onion-এর মতো** — request ঢোকার সময় উপর থেকে নিচে, response যাওয়ার সময় নিচ থেকে উপরে।

```python
# settings.py — Middleware order matter করে!
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",      # 1st
    "django.contrib.sessions.middleware.SessionMiddleware", # 2nd
    "django.middleware.csrf.CsrfViewMiddleware",          # 3rd
    "django.contrib.auth.middleware.AuthenticationMiddleware", # 4th
    "mybank.middleware.JWTAuthMiddleware",                # Custom
    "mybank.middleware.AuditLogMiddleware",               # Custom
]
```

**Custom Middleware — Banking Audit:**
```python
import time
import logging

logger = logging.getLogger(__name__)

class AuditLogMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # ── REQUEST আসার আগে ──
        start_time = time.time()
        request.start_time = start_time

        logger.info(
            f"REQUEST | {request.method} {request.path} "
            f"| User: {getattr(request.user, 'id', 'anonymous')}"
        )

        # View চালাও
        response = self.get_response(request)

        # ── RESPONSE যাওয়ার আগে ──
        duration = time.time() - start_time

        logger.info(
            f"RESPONSE | {request.method} {request.path} "
            f"| Status: {response.status_code} "
            f"| Time: {duration:.3f}s"
        )

        # Response-এ custom header যোগ করো
        response["X-Response-Time"] = f"{duration:.3f}s"
        response["X-Bank"] = "UCB"

        return response

    def process_exception(self, request, exception):
        # Unhandled exception হলে
        logger.error(
            f"EXCEPTION | {request.path} | {exception}",
            exc_info=True
        )
        return None   # None → Django default error handling
```

---

## ধাপ ৫ — URL Resolution:

```python
# mybank/urls.py — Main router
from django.urls import path, include

urlpatterns = [
    path("api/accounts/", include("accounts.urls")),
    path("api/transactions/", include("transactions.urls")),
    path("api/auth/", include("authentication.urls")),
]

# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path("", views.AccountListView.as_view()),
    # এই URL pattern match হলে → সেই View call হবে
    path("", views.AccountListView.as_view()),
    path("<str:account_id>/", views.AccountDetailView.as_view()),
    path("<str:account_id>/withdraw/", views.WithdrawView.as_view()),
]
```

**URL Resolution Process:**
```
Request: GET /api/accounts/SB-001/

Step 1: mybank/urls.py
        "api/accounts/" → accounts.urls-এ যাও

Step 2: accounts/urls.py
        "<str:account_id>/" → AccountDetailView
        account_id = "SB-001" ← URL থেকে extract

Step 3: View call করো
        AccountDetailView(account_id="SB-001")
```

---

## ধাপ ৬ — View Execution:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

class WithdrawView(APIView):

    # ── Authentication check (DRF করে) ──
    permission_classes = [IsAuthenticated]

    def post(self, request, account_id):

        # ── Request Data Validation ──
        amount = request.data.get("amount")
        if not amount or amount <= 0:
            return Response(
                {"error": "Invalid amount"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # ── Database Operation ──
            with transaction.atomic():

                # Row lock — concurrent withdrawal safe
                account = Account.objects.select_for_update().get(
                    account_id=account_id,
                    is_active=True
                )

                if account.balance < amount:
                    raise InsufficientBalanceError(
                        account_id, amount, account.balance
                    )

                # Balance update
                account.balance -= amount
                account.save()

                # Transaction log
                txn = Transaction.objects.create(
                    account=account,
                    txn_type="DR",
                    amount=amount,
                    balance_after=account.balance
                )

            # ── Response তৈরি ──
            serializer = TransactionSerializer(txn)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except Account.DoesNotExist:
            return Response(
                {"error": "Account not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except InsufficientBalanceError as e:
            return Response(
                e.to_dict(),
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
```

---

## ধাপ ৭ — ORM → Database:

```python
# Django ORM → SQL translation

# ORM
Account.objects.select_for_update().get(
    account_id="SB-001",
    is_active=True
)

# Generated SQL:
# SELECT * FROM accounts
# WHERE account_id = 'SB-001'
# AND is_active = TRUE
# FOR UPDATE;          ← Row lock

# ORM
Transaction.objects.filter(
    account=account
).order_by("-created_at")[:10]

# Generated SQL:
# SELECT * FROM transactions
# WHERE account_id = 1
# ORDER BY created_at DESC
# LIMIT 10;
```

---

## ধাপ ৮ — Response তৈরি:

```python
# Serializer → Python object → JSON
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["txn_id", "amount", "balance_after", "created_at"]

# View-এ:
serializer = TransactionSerializer(txn)
return Response(serializer.data)

# Final JSON Response:
# {
#   "txn_id": "TXN-001",
#   "amount": 5000.00,
#   "balance_after": 45000.00,
#   "created_at": "2024-01-15T10:30:00Z"
# }
```

---

## সম্পূর্ণ Example — Withdraw Request:

```
POST /api/accounts/SB-001/withdraw/
Authorization: Bearer <JWT Token>
Body: {"amount": 5000}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1: Nginx
        → HTTPS terminate
        → Gunicorn-এ forward

STEP 2: Gunicorn
        → HTTP parse করে
        → Django-তে পাঠায়

STEP 3: SecurityMiddleware
        → HTTPS enforce করে
        → XSS header যোগ করে

STEP 4: AuthenticationMiddleware
        → JWT token verify করে
        → request.user = User(id=42)

STEP 5: AuditLogMiddleware
        → Request log করে
        → Timer শুরু

STEP 6: URL Router
        → /api/accounts/ → accounts.urls
        → SB-001/withdraw/ → WithdrawView
        → account_id = "SB-001"

STEP 7: WithdrawView.post()
        → amount = 5000 validate
        → DB: SELECT ... FOR UPDATE
        → balance check
        → balance update
        → Transaction create

STEP 8: TransactionSerializer
        → Transaction object → dict → JSON

STEP 9: Response build
        → HTTP 200
        → JSON body

STEP 10: AuditLogMiddleware (return)
         → Response time log
         → X-Response-Time header যোগ

STEP 11: Nginx
         → Client-এ response পাঠায়
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total time: ~50ms ✅
```

---

### 📊 Lifecycle Summary:

| ধাপ | Component | কাজ |
|---|---|---|
| **1** | Nginx | SSL, static files, proxy |
| **2** | Gunicorn/Uvicorn | HTTP parse, Django call |
| **3** | Django Handler | Settings load |
| **4** | Middleware (in) | Auth, CSRF, Audit |
| **5** | URL Router | View match |
| **6** | View | Business logic |
| **7** | ORM | Database query |
| **8** | Serializer | JSON format |
| **9** | Middleware (out) | Header add, log |
| **10** | Nginx | Client-এ deliver |

---

### 🎯 Interview Closing line:

> *"Django-র request lifecycle-এর সবচেয়ে গুরুত্বপূর্ণ অংশ হলো Middleware chain — এখানেই Authentication, CSRF protection, আর Audit logging centrally handle হয়। Banking system-এ প্রতিটা request-এ JWT verify, IP whitelist check, আর audit log — এগুলো Middleware-এ রাখলে প্রতিটা View-এ আলাদা লিখতে হয় না। `select_for_update()` দিয়ে row lock নিশ্চিত করা আর `transaction.atomic()` দিয়ে data consistency রাখা — এই দুটো banking system-এ অপরিহার্য।"*

---

পরের গুরুত্বপূর্ণ topics:
- **Django ORM + Query Optimization**
- **JWT Authentication — কীভাবে কাজ করে**
- **REST API Design Best Practices**
- **SOLID Principles**

কোনটা নিয়ে আগাবে?


## Middleware কী? Custom Middleware কীভাবে বানাবে?

---

### 🔑 এক কথায়:

> Middleware হলো Django-র **request/response pipeline-এর মাঝখানে বসা layer** — প্রতিটা request View-এ পৌঁছানোর আগে এবং প্রতিটা response Client-এ যাওয়ার আগে এখান দিয়ে যায়।

সহজ analogy:
```
Airport Security = Middleware

Plane-এ উঠতে:              Plane থেকে নামতে:
✓ Ticket check              ✓ Passport check
✓ Luggage scan              ✓ Customs check
✓ Body scan                 ✓ Baggage claim

প্রতিটা Passenger (Request)  প্রতিটা Passenger (Response)
এই ধাপ পার করতেই হবে        এই ধাপ পার করতেই হবে
```

---

### 🧠 Middleware Chain — Onion Model:

```
Request ↓                    Response ↑

┌─────────────────────────────────────┐
│  SecurityMiddleware                 │
│  ┌─────────────────────────────┐    │
│  │  SessionMiddleware          │    │
│  │  ┌───────────────────────┐  │    │
│  │  │  AuthMiddleware       │  │    │
│  │  │  ┌─────────────────┐  │  │    │
│  │  │  │  CsrfMiddleware │  │  │    │
│  │  │  │  ┌───────────┐  │  │  │    │
│  │  │  │  │   VIEW    │  │  │  │    │
│  │  │  │  └───────────┘  │  │  │    │
│  │  │  └─────────────────┘  │  │    │
│  │  └───────────────────────┘  │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘

Request:  বাইরে থেকে ভেতরে (উপর → নিচ)
Response: ভেতর থেকে বাইরে (নিচ → উপর)
```

---

### 💻 Django Built-in Middleware:

```python
# settings.py
MIDDLEWARE = [
    # ১. HTTPS enforce, XSS headers
    "django.middleware.security.SecurityMiddleware",

    # ২. Session data manage করে
    "django.contrib.sessions.middleware.SessionMiddleware",

    # ৩. CORS headers
    "corsheaders.middleware.CorsMiddleware",

    # ৪. Trailing slash redirect
    "django.middleware.common.CommonMiddleware",

    # ৫. CSRF token verify করে
    "django.middleware.csrf.CsrfViewMiddleware",

    # ৬. request.user set করে
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    # ৭. Flash messages
    "django.contrib.messages.middleware.MessageMiddleware",

    # ৮. Clickjacking protection
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

---

## Custom Middleware — ৩টা উপায়:

---

### 💻 উপায় ১ — Function-based (সহজ):

```python
def simple_middleware(get_response):
    # Startup-এ একবার চলে
    print("Middleware initialized")

    def middleware(request):
        # ── REQUEST আসার আগে ──
        print(f"Before view: {request.path}")

        response = get_response(request)   # View চালাও

        # ── RESPONSE যাওয়ার আগে ──
        print(f"After view: {response.status_code}")

        return response

    return middleware
```

---

### 💻 উপায় ২ — Class-based (Recommended):

```python
class SimpleMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # Server startup-এ একবার চলে

    def __call__(self, request):
        # ── REQUEST আগে ──
        # কাজ করো

        response = self.get_response(request)

        # ── RESPONSE পরে ──
        # কাজ করো

        return response
```

---

### 💻 উপায় ৩ — Hooks দিয়ে (Fine-grained control):

```python
class HookMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # URL match হওয়ার পরে, View চালানোর আগে
        print(f"About to call: {view_func.__name__}")
        return None   # None → View চলবে, Response → View skip

    def process_exception(self, request, exception):
        # View-এ unhandled exception হলে
        print(f"Exception caught: {exception}")
        return None   # None → Django default handling

    def process_template_response(self, request, response):
        # Template render হওয়ার আগে
        return response
```

---

## Real Banking Middleware Examples:

---

### 💻 ১. JWT Authentication Middleware:

```python
import jwt
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User

class JWTAuthMiddleware:

    # এই paths-এ JWT দরকার নেই
    PUBLIC_PATHS = [
        "/api/auth/login/",
        "/api/auth/register/",
        "/api/health/",
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Public path → skip
        if request.path in self.PUBLIC_PATHS:
            return self.get_response(request)

        # Token check
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return JsonResponse(
                {"error": "Token missing"},
                status=401
            )

        token = auth_header.split(" ")[1]

        try:
            # Token decode করো
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )

            # User set করো
            user = User.objects.get(id=payload["user_id"])
            request.user = user      # View-এ request.user পাবে ✅

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token expired"}, status=401)

        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=401)

        return self.get_response(request)
```

---

### 💻 ২. Request/Response Audit Middleware:

```python
import time
import json
import logging

logger = logging.getLogger("banking.audit")

class AuditLogMiddleware:

    SENSITIVE_FIELDS = ["password", "pin", "cvv", "otp"]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Request body read করো (একবারই পড়া যায়)
        request_body = self._get_body(request)
        start_time = time.time()

        # Request log
        logger.info(self._format_request(request, request_body))

        response = self.get_response(request)

        # Response log
        duration = time.time() - start_time
        logger.info(self._format_response(request, response, duration))

        # Response-এ timing header যোগ করো
        response["X-Response-Time"] = f"{duration * 1000:.2f}ms"

        return response

    def _get_body(self, request):
        try:
            body = json.loads(request.body)
            # Sensitive field mask করো
            return self._mask_sensitive(body)
        except Exception:
            return {}

    def _mask_sensitive(self, data: dict) -> dict:
        masked = {}
        for key, value in data.items():
            if key.lower() in self.SENSITIVE_FIELDS:
                masked[key] = "***"   # PIN, password লুকাও ✅
            else:
                masked[key] = value
        return masked

    def _format_request(self, request, body):
        return (
            f"REQUEST | "
            f"Method: {request.method} | "
            f"Path: {request.path} | "
            f"User: {getattr(request.user, 'id', 'anonymous')} | "
            f"IP: {self._get_ip(request)} | "
            f"Body: {body}"
        )

    def _format_response(self, request, response, duration):
        return (
            f"RESPONSE | "
            f"Path: {request.path} | "
            f"Status: {response.status_code} | "
            f"Duration: {duration * 1000:.2f}ms"
        )

    def _get_ip(self, request):
        # Load balancer-এর পেছনে থাকলে
        return (
            request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0]
            or request.META.get("REMOTE_ADDR", "")
        )

    def process_exception(self, request, exception):
        logger.error(
            f"EXCEPTION | {request.path} | {exception}",
            exc_info=True
        )
        return None   # Django default error handling
```

---

### 💻 ৩. Rate Limiting Middleware:

```python
import time
from django.core.cache import cache
from django.http import JsonResponse

class RateLimitMiddleware:
    """
    Banking API-তে per-user rate limiting
    Brute force attack থেকে রক্ষা
    """

    RATE_LIMITS = {
        "/api/auth/login/":      (5, 60),    # 5 requests per 60s
        "/api/accounts/transfer/": (10, 60), # 10 per 60s
        "default":               (100, 60),  # 100 per 60s
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Rate limit check
        limit_result = self._check_rate_limit(request)

        if limit_result["exceeded"]:
            return JsonResponse({
                "error": "Rate limit exceeded",
                "retry_after": limit_result["retry_after"]
            }, status=429)

        response = self.get_response(request)

        # Response-এ rate limit info যোগ করো
        response["X-RateLimit-Remaining"] = limit_result["remaining"]
        response["X-RateLimit-Reset"] = limit_result["reset"]

        return response

    def _check_rate_limit(self, request):
        # IP বা User দিয়ে key বানাও
        user_id = getattr(request.user, "id", None)
        ip = request.META.get("REMOTE_ADDR")
        identifier = f"user_{user_id}" if user_id else f"ip_{ip}"

        # Path-specific limit
        max_requests, window = self.RATE_LIMITS.get(
            request.path,
            self.RATE_LIMITS["default"]
        )

        cache_key = f"ratelimit_{identifier}_{request.path}"
        current = cache.get(cache_key, {"count": 0, "reset": time.time() + window})

        # Window শেষ হয়ে গেলে reset
        if time.time() > current["reset"]:
            current = {"count": 0, "reset": time.time() + window}

        current["count"] += 1
        cache.set(cache_key, current, window)

        return {
            "exceeded": current["count"] > max_requests,
            "remaining": max(0, max_requests - current["count"]),
            "reset": int(current["reset"]),
            "retry_after": int(current["reset"] - time.time())
        }
```

---

### 💻 ৪. IP Whitelist Middleware — Banking Security:

```python
from django.http import JsonResponse
from django.conf import settings

class IPWhitelistMiddleware:
    """
    Admin panel শুধু office IP থেকে access করা যাবে
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_ips = getattr(settings, "ADMIN_ALLOWED_IPS", [])

    def __call__(self, request):

        # Admin path check
        if request.path.startswith("/admin/"):
            client_ip = self._get_ip(request)

            if client_ip not in self.allowed_ips:
                return JsonResponse({
                    "error": "Access denied from this IP"
                }, status=403)

        return self.get_response(request)

    def _get_ip(self, request):
        return (
            request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip()
            or request.META.get("REMOTE_ADDR")
        )


# settings.py
ADMIN_ALLOWED_IPS = [
    "10.0.0.1",      # Office IP
    "192.168.1.100", # Dev machine
]
```

---

### 💻 ৫. Maintenance Mode Middleware:

```python
from django.http import JsonResponse
from django.core.cache import cache

class MaintenanceModeMiddleware:
    """
    System maintenance-এ সব request block করো
    Banking-এ scheduled downtime handle করার জন্য
    """

    EXEMPT_PATHS = ["/api/health/", "/admin/"]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Exempt paths skip করো
        if any(request.path.startswith(p) for p in self.EXEMPT_PATHS):
            return self.get_response(request)

        # Cache থেকে maintenance flag check করো
        is_maintenance = cache.get("maintenance_mode", False)

        if is_maintenance:
            maintenance_info = cache.get("maintenance_info", {})
            return JsonResponse({
                "error": "System under maintenance",
                "message": maintenance_info.get("message", ""),
                "expected_back": maintenance_info.get("expected_back", "")
            }, status=503)

        return self.get_response(request)
```

---

### 💻 Settings-এ Register করো:

```python
# settings.py
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",

    # Custom Middleware — Order matter করে!
    "mybank.middleware.MaintenanceModeMiddleware",  # ১ম — maintenance check
    "mybank.middleware.IPWhitelistMiddleware",      # ২য় — IP check
    "mybank.middleware.RateLimitMiddleware",        # ৩য় — rate limit
    "mybank.middleware.JWTAuthMiddleware",          # ৪র্থ — auth check
    "mybank.middleware.AuditLogMiddleware",         # ৫ম — logging

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]
```

---

### 📊 কোন Middleware কী করে:

| Middleware | কাজ | Order |
|---|---|---|
| `MaintenanceModeMiddleware` | Downtime handle | ১ম |
| `IPWhitelistMiddleware` | IP block | ২য় |
| `RateLimitMiddleware` | Request limit | ৩য় |
| `JWTAuthMiddleware` | Token verify | ৪র্থ |
| `AuditLogMiddleware` | Request log | ৫ম |

---

### ⚠️ Middleware Order কেন Important:

```
❌ Wrong order:
   AuditLog → JWT Auth
   (user anonymous হলে log-এ user নেই)

✅ Correct order:
   JWT Auth → AuditLog
   (আগে user identify, তারপর log)

❌ Wrong:
   RateLimit → Maintenance
   (maintenance-এও rate limit count হচ্ছে)

✅ Correct:
   Maintenance → RateLimit
   (maintenance-এ আগেই return)
```

---

### 🎯 Interview Closing line:

> *"Middleware হলো banking system-এর security আর observability-র backbone। আমি JWT authentication, rate limiting, audit logging, আর IP whitelist — চারটাই custom middleware দিয়ে implement করেছি। এগুলো Middleware-এ রাখার সবচেয়ে বড় সুবিধা হলো — প্রতিটা View-এ আলাদা করে লিখতে হয় না, একটা জায়গায় change করলে সব জায়গায় apply হয়। Order অনেক important — Maintenance আগে check না করলে down থাকার সময়ও rate limit count হতে থাকবে।"*

---

পরের গুরুত্বপূর্ণ topics:
- **JWT Authentication — কীভাবে কাজ করে**
- **Django ORM + Query Optimization**
- **REST API Design Best Practices**
- **SOLID Principles**

কোনটা নিয়ে আগাবে?

## Django ORM, select_related vs prefetch_related, N+1 Problem

---

## ১. ORM কীভাবে কাজ করে

---

### 🔑 এক কথায়:

> ORM = Object Relational Mapper — Python code লিখলে সে নিজেই SQL বানায় এবং Database-এ চালায়। তুমি SQL না জেনেও Database-এ কাজ করতে পারো।

```
Python Object  ←→  ORM  ←→  SQL  ←→  Database
BankAccount()      ↕        ↕         PostgreSQL
.save()         Translate  Execute
.filter()       to SQL     Query
```

---

### 💻 ORM vs Raw SQL:

```python
# Raw SQL — সরাসরি
cursor.execute("""
    SELECT * FROM accounts
    WHERE is_active = TRUE
    AND balance > 10000
    ORDER BY created_at DESC
    LIMIT 10
""")

# Django ORM — Python-এ
Account.objects.filter(
    is_active=True,
    balance__gt=10000
).order_by("-created_at")[:10]

# দুটো একই SQL generate করে ✅
# ORM version অনেক বেশি readable, safe (SQL injection নেই)
```

---

### 💻 ORM-এর Core — QuerySet:

```python
# QuerySet = Lazy — SQL এখনো চলেনি!
accounts = Account.objects.filter(is_active=True)
# এখানে কোনো DB call হয়নি 😮

# Evaluation হলে তখন SQL চলে:
list(accounts)          # ← এখন SQL চলে
for acc in accounts:    # ← এখন SQL চলে
accounts[0]             # ← এখন SQL চলে
len(accounts)           # ← এখন SQL চলে
bool(accounts)          # ← এখন SQL চলে
```

**Lazy Evaluation-এর সুবিধা:**
```python
# Chain করা যায় — একটাই SQL হয়
result = Account.objects\
    .filter(is_active=True)\
    .filter(balance__gt=10000)\
    .exclude(account_type="FD")\
    .order_by("-balance")\
    .values("account_id", "name", "balance")[:10]

# Generated SQL — একটাই query ✅
# SELECT account_id, name, balance
# FROM accounts
# WHERE is_active = TRUE
# AND balance > 10000
# AND account_type != 'FD'
# ORDER BY balance DESC
# LIMIT 10;
```

---

### 💻 Common ORM Operations:

```python
# ── CREATE ──
acc = Account.objects.create(
    account_id="SB-001",
    name="Sourov",
    balance=50000
)

# ── READ ──
# একটা object
acc = Account.objects.get(account_id="SB-001")

# অনেকগুলো
accounts = Account.objects.filter(is_active=True)

# First/Last
first = Account.objects.filter(is_active=True).first()

# Exists — COUNT না করে efficient check
if Account.objects.filter(account_id="SB-001").exists():
    print("Account found")

# ── UPDATE ──
# Single object
acc.balance = 60000
acc.save()

# Bulk update — একটাই SQL
Account.objects.filter(
    account_type="SB"
).update(interest_rate=0.06)
# UPDATE accounts SET interest_rate=0.06
# WHERE account_type='SB'

# ── DELETE ──
Account.objects.filter(is_active=False).delete()

# ── AGGREGATION ──
from django.db.models import Sum, Avg, Count, Max, Min

stats = Account.objects.aggregate(
    total_balance=Sum("balance"),
    avg_balance=Avg("balance"),
    account_count=Count("id"),
    max_balance=Max("balance")
)
print(stats)
# {'total_balance': 5000000, 'avg_balance': 50000, ...}
```

---

### 💻 ORM-এ Generated SQL দেখো:

```python
# Debug করার সময় SQL দেখতে চাইলে
queryset = Account.objects.filter(is_active=True)
print(queryset.query)
# SELECT "accounts"."id", "accounts"."name", ...
# FROM "accounts"
# WHERE "accounts"."is_active" = TRUE

# Django Debug Toolbar দিয়েও দেখা যায়
```

---

## ২. select_related vs prefetch_related

---

### 🔑 কেন দরকার:

```python
# Model relationship
class Account(models.Model):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey("Branch", on_delete=models.PROTECT)

class Transaction(models.Model):
    account = models.ForeignKey(Account, related_name="transactions")
    amount = models.DecimalField(max_digits=15, decimal_places=2)

class Branch(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
```

---

### 💻 `select_related` — SQL JOIN দিয়ে:

> **ForeignKey / OneToOne** relationship-এ use করো — একটাই SQL query-তে সব আনে।

```python
# ❌ Without select_related — 2 queries
account = Account.objects.get(id=1)   # Query 1
branch = account.branch                # Query 2 (extra!)

# ✅ With select_related — 1 query
account = Account.objects.select_related("branch").get(id=1)
branch = account.branch               # No extra query! ✅

# Generated SQL:
# SELECT accounts.*, branches.*
# FROM accounts
# INNER JOIN branches ON accounts.branch_id = branches.id
# WHERE accounts.id = 1;
```

**Multiple levels:**
```python
# Transaction → Account → Branch — সব একসাথে
transactions = Transaction.objects.select_related(
    "account",           # Transaction → Account
    "account__branch"    # Account → Branch
).filter(txn_type="DR")

# Generated SQL — একটাই JOIN query ✅
# SELECT transactions.*, accounts.*, branches.*
# FROM transactions
# JOIN accounts ON transactions.account_id = accounts.id
# JOIN branches ON accounts.branch_id = branches.id
# WHERE transactions.txn_type = 'DR'
```

---

### 💻 `prefetch_related` — Separate Query দিয়ে:

> **ManyToMany / Reverse ForeignKey** relationship-এ use করো — আলাদা query করে Python-এ merge করে।

```python
# ❌ Without prefetch_related
accounts = Account.objects.all()
for acc in accounts:
    txns = acc.transactions.all()   # প্রতিটা account-এ আলাদা query! 😱
    # 100 accounts → 101 queries (N+1 problem!)

# ✅ With prefetch_related — 2 queries মাত্র
accounts = Account.objects.prefetch_related("transactions").all()

for acc in accounts:
    txns = acc.transactions.all()   # No extra query! ✅

# Generated SQL — দুটো query:
# Query 1: SELECT * FROM accounts;
# Query 2: SELECT * FROM transactions
#          WHERE account_id IN (1, 2, 3, ...);
# Python-এ merge হয় ✅
```

**`Prefetch` object দিয়ে filter:**
```python
from django.db.models import Prefetch

# শুধু Debit transactions prefetch করো
debit_txns = Transaction.objects.filter(txn_type="DR")

accounts = Account.objects.prefetch_related(
    Prefetch(
        "transactions",
        queryset=debit_txns,
        to_attr="debit_transactions"   # আলাদা attribute-এ রাখো
    )
).all()

for acc in accounts:
    print(acc.debit_transactions)   # Filtered transactions ✅
```

---

### 📊 select_related vs prefetch_related:

| | `select_related` | `prefetch_related` |
|---|---|---|
| **কীভাবে** | SQL JOIN | Separate query |
| **কতটা query** | ১টা | ২টা |
| **কোথায় merge** | Database | Python |
| **Relationship** | FK, OneToOne | M2M, Reverse FK |
| **Large data** | ❌ JOIN heavy | ✅ Better |
| **Filter করা যায়?** | ❌ | ✅ Prefetch() দিয়ে |

---

## ৩. N+1 Query Problem

---

### 🔑 এক কথায়:

> N+1 মানে — ১টা query দিয়ে N টা object আনলে, তারপর সেই N টা object-এর জন্য আরো N টা query চলে। মোট = N+1 queries।

---

### 💻 N+1 Problem — দেখো কী হয়:

```python
# ❌ N+1 Problem
accounts = Account.objects.all()   # Query 1: সব account আনো

for acc in accounts:
    # প্রতিটা account-এর জন্য আলাদা query!
    print(acc.branch.name)         # Query 2, 3, 4, ... N+1 😱

# ১০০টা account → ১০১টা query!
# ১০০০টা account → ১০০১টা query! 💀

# Log দেখলে:
# SELECT * FROM accounts;
# SELECT * FROM branches WHERE id = 1;
# SELECT * FROM branches WHERE id = 2;
# SELECT * FROM branches WHERE id = 3;
# ... (N বার)
```

**আরো ভয়াবহ example:**
```python
# ❌ Deeply nested N+1
accounts = Account.objects.all()   # 1 query

for acc in accounts:               # 100 accounts
    for txn in acc.transactions.all():  # 100 queries
        print(txn.amount)

# ১ + ১০০ = ১০১ queries 😱
# আর প্রতিটা account-এ ১০টা করে transaction হলে
# ১ + ১০০ = ১০১ queries (still!)
# কিন্তু data অনেক বেশি আসছে
```

---

### 💻 N+1 Detect করো:

```python
# Django Debug Toolbar — development-এ
# settings.py
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

# বা manually:
from django.db import connection, reset_queries
from django.conf import settings

settings.DEBUG = True

reset_queries()

# Code চালাও
accounts = Account.objects.all()
for acc in accounts:
    print(acc.branch.name)

# কতটা query হলো দেখো
print(f"Total queries: {len(connection.queries)}")
# Total queries: 101 😱

for q in connection.queries:
    print(q["sql"])
```

---

### 💻 N+1 Fix করো:

**Fix 1 — `select_related` (ForeignKey):**
```python
# ❌ N+1
accounts = Account.objects.all()
for acc in accounts:
    print(acc.branch.name)   # প্রতিটায় query!

# ✅ Fixed
accounts = Account.objects.select_related("branch").all()
for acc in accounts:
    print(acc.branch.name)   # No extra query ✅

# Queries: 101 → 1 ✅
```

**Fix 2 — `prefetch_related` (Reverse FK):**
```python
# ❌ N+1
accounts = Account.objects.all()
for acc in accounts:
    txns = acc.transactions.all()   # প্রতিটায় query!

# ✅ Fixed
accounts = Account.objects.prefetch_related("transactions").all()
for acc in accounts:
    txns = acc.transactions.all()   # No extra query ✅

# Queries: 101 → 2 ✅
```

**Fix 3 — Deeply nested:**
```python
# ❌ Nested N+1
accounts = Account.objects.all()
for acc in accounts:
    for txn in acc.transactions.all():
        print(txn.account.branch.name)   # Triple N+1! 💀

# ✅ Fixed — সব একসাথে
accounts = Account.objects\
    .select_related("branch")\
    .prefetch_related(
        Prefetch(
            "transactions",
            queryset=Transaction.objects.select_related("account__branch")
        )
    ).all()

# Queries: hundreds → 3 ✅
```

---

### 💻 Banking-এ Real Example — Statement API:

```python
# ❌ BAD — N+1 nightmare
def get_account_statement(request, account_id):
    account = Account.objects.get(account_id=account_id)  # 1 query
    transactions = account.transactions.all()              # 1 query

    result = []
    for txn in transactions:
        result.append({
            "txn_id": txn.txn_id,
            "amount": txn.amount,
            "branch": txn.account.branch.name,    # N query! 😱
            "teller": txn.teller.name,            # N query! 😱
            "category": txn.category.label,       # N query! 😱
        })

    return JsonResponse({"transactions": result})
# ১০০ transaction → ৩০০+ queries! 💀


# ✅ GOOD — Optimized
def get_account_statement(request, account_id):
    account = Account.objects\
        .select_related("branch")\
        .get(account_id=account_id)          # 1 query

    transactions = Transaction.objects\
        .select_related(
            "account__branch",               # JOIN
            "teller",                        # JOIN
            "category"                       # JOIN
        )\
        .filter(account=account)\
        .order_by("-created_at")\
        .only(                               # Needed fields only
            "txn_id", "amount", "created_at",
            "account__branch__name",
            "teller__name",
            "category__label"
        )                                    # 1 query

    result = []
    for txn in transactions:
        result.append({
            "txn_id": txn.txn_id,
            "amount": txn.amount,
            "branch": txn.account.branch.name,    # No query ✅
            "teller": txn.teller.name,            # No query ✅
            "category": txn.category.label,       # No query ✅
        })

    return JsonResponse({"transactions": result})
# ৩০০+ queries → 2 queries ✅
```

---

### 💻 Extra Optimization — `only()` vs `defer()`:

```python
# only() — শুধু এই fields আনো
accounts = Account.objects.only(
    "account_id", "name", "balance"
)
# SELECT account_id, name, balance FROM accounts;
# অন্য fields access করলে extra query হবে

# defer() — এই fields বাদে বাকি সব আনো
accounts = Account.objects.defer("transaction_history", "notes")
# SELECT account_id, name, balance, ... (notes বাদে)
# Large text fields skip করলে performance বাড়ে

# values() — dict হিসেবে আনো (object তৈরি হয় না)
accounts = Account.objects.values("account_id", "name", "balance")
# [{"account_id": "SB-001", "name": "Sourov", ...}]
# সবচেয়ে lightweight ✅

# values_list() — tuple হিসেবে
ids = Account.objects.values_list("account_id", flat=True)
# ["SB-001", "SB-002", ...] ← flat=True মানে list of values
```

---

### 💻 Bulk Operations — N+1 Alternative:

```python
# ❌ Loop-এ save — N queries
for account in accounts:
    account.interest_rate = 0.06
    account.save()   # প্রতিটায় UPDATE 😱

# ✅ Bulk update — 1 query
Account.objects.filter(
    account_type="SB"
).update(interest_rate=0.06)


# ❌ Loop-এ create — N queries
for data in transaction_data:
    Transaction.objects.create(**data)   # প্রতিটায় INSERT 😱

# ✅ Bulk create — 1 query
Transaction.objects.bulk_create([
    Transaction(**data) for data in transaction_data
])
```

---

### 📊 Query Optimization Cheatsheet:

| সমস্যা | Solution | Queries কমে |
|---|---|---|
| FK N+1 | `select_related()` | N+1 → 1 |
| Reverse FK N+1 | `prefetch_related()` | N+1 → 2 |
| Filtered prefetch | `Prefetch()` object | N+1 → 2 |
| Extra fields | `only()` / `defer()` | Data কমে |
| No object needed | `values()` / `values_list()` | Memory কমে |
| Loop insert | `bulk_create()` | N → 1 |
| Loop update | `bulk_update()` | N → 1 |
| Existence check | `exists()` | COUNT → EXISTS |

---

### 🎯 Interview Closing line:

> *"ORM-এর সবচেয়ে বড় trap হলো N+1 problem — banking system-এ statement API-তে ১০০ transaction-এর জন্য ৩০০+ query হতে পারে। `select_related` দিয়ে ForeignKey JOIN করি, `prefetch_related` দিয়ে Reverse FK আলাদা query করে Python-এ merge করি। Production-এ Django Debug Toolbar দিয়ে query count monitor করি। `only()` দিয়ে unnecessary fields avoid করি আর bulk operation দিয়ে N query-কে 1-এ নামাই।"*

---

পরের গুরুত্বপূর্ণ topics:
- **JWT Authentication — কীভাবে কাজ করে**
- **REST API Design Best Practices**
- **SOLID Principles**
- **Database Indexing + Transaction**

কোনটা নিয়ে আগাবে?

## Authentication in DRF — JWT & OAuth2

---

## ১. Authentication Types in DRF

---

### 🔑 DRF-এ ৪ ধরনের Authentication:

```
DRF Authentication
├── 1. BasicAuthentication      → username/password (Base64)
├── 2. SessionAuthentication    → Django session cookie
├── 3. TokenAuthentication      → Simple static token
└── 4. JWTAuthentication        → JSON Web Token (Best)
```

---

### 💻 BasicAuthentication — সবচেয়ে সহজ:

```python
# settings.py
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
    ]
}

# প্রতিটা request-এ Header পাঠাতে হয়:
# Authorization: Basic c291cm92OjEyMzQ=
# (username:password → Base64 encoded)

# ❌ Banking-এ use করো না — password প্রতিটা request-এ যায়!
```

---

### 💻 SessionAuthentication — Browser-based:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ]
}

# Login করলে → Session cookie set হয়
# Browser automatically cookie পাঠায়
# CSRF protection দরকার

# ❌ Mobile app বা API-তে suitable না
# ✅ Django admin বা browser-based app-এ ঠিক আছে
```

---

### 💻 TokenAuthentication — Static Token:

```python
INSTALLED_APPS += ["rest_framework.authtoken"]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ]
}

# Token তৈরি করো
from rest_framework.authtoken.models import Token

token = Token.objects.create(user=user)
print(token.key)   # "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"

# Request Header:
# Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

# ❌ Token expire হয় না — security risk!
# ❌ Logout করলেও token valid থাকে DB-তে না মুছলে
# ✅ Simple internal tools-এ ঠিক আছে
```

---

### 📊 কোনটা কোথায়:

| Type | Security | Mobile | Expiry | Banking? |
|---|---|---|---|---|
| Basic | ❌ খুব কম | ❌ | ❌ | ❌ না |
| Session | মাঝারি | ❌ | ✅ | ❌ না |
| Token | মাঝারি | ✅ | ❌ | ❌ না |
| JWT | ✅ বেশি | ✅ | ✅ | ✅ হ্যাঁ |

---

## ২. JWT — কীভাবে কাজ করে এবং Implement করো

---

### 🔑 JWT কী:

> JWT = JSON Web Token — তিনটা অংশ নিয়ে তৈরি, **stateless** — Server-এ কিছু save করতে হয় না।

```
JWT Structure:

eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.abc123
│                    │                   │
└── Header           └── Payload         └── Signature
    (algorithm)          (data)              (verify করে)
```

```python
# Header — decoded
{
    "alg": "HS256",    # Algorithm
    "typ": "JWT"
}

# Payload — decoded
{
    "user_id": 42,
    "username": "sourov",
    "role": "customer",
    "exp": 1735689600,  # Expiry timestamp
    "iat": 1735686000   # Issued at
}

# Signature — কীভাবে তৈরি হয়:
HMACSHA256(
    base64(header) + "." + base64(payload),
    SECRET_KEY
)
```

---

### 🔄 JWT Flow — Step by Step:

```
Client                          Server
  │                               │
  │── POST /login {user, pass} ──→│
  │                               │ Verify credentials
  │                               │ Generate Access Token (15min)
  │                               │ Generate Refresh Token (7days)
  │←── {access, refresh} ────────│
  │                               │
  │── GET /api/accounts/ ────────→│
  │   Authorization: Bearer       │ Verify JWT signature
  │   <access_token>              │ Check expiry
  │←── {accounts data} ──────────│
  │                               │
  │ (15 min পরে token expire)     │
  │                               │
  │── POST /auth/refresh/ ───────→│
  │   {refresh: <refresh_token>}  │ Verify refresh token
  │←── {new access_token} ───────│
  │                               │
  │── POST /logout/ ─────────────→│
  │   {refresh: <refresh_token>}  │ Refresh token blacklist-এ
  │←── {success} ────────────────│
```

---

### 💻 JWT Implementation — Step by Step:

**Install:**
```bash
pip install djangorestframework-simplejwt
```

**settings.py:**
```python
INSTALLED_APPS = [
    ...
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",  # Logout-এর জন্য
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),   # Short-lived
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),       # Long-lived
    "ROTATE_REFRESH_TOKENS": True,     # Refresh করলে নতুন token
    "BLACKLIST_AFTER_ROTATION": True,  # পুরনো blacklist হয়
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}
```

---

### 💻 Custom JWT — Banking-এর জন্য:

```python
# authentication/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class BankingTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Custom claims — Banking info যোগ করো
        token["username"] = user.username
        token["role"] = user.profile.role           # customer/teller/admin
        token["account_id"] = user.profile.account_id
        token["branch_id"] = user.profile.branch_id
        token["permissions"] = list(user.get_all_permissions())

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Extra info response-এ যোগ করো
        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "role": self.user.profile.role,
            "account_id": self.user.profile.account_id,
        }
        data["token_type"] = "Bearer"

        return data


class BankingTokenView(TokenObtainPairView):
    serializer_class = BankingTokenSerializer
```

---

### 💻 URLs Setup:

```python
# urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from .views import BankingTokenView

urlpatterns = [
    # Login → tokens দেয়
    path("api/auth/login/", BankingTokenView.as_view()),

    # Refresh → নতুন access token
    path("api/auth/refresh/", TokenRefreshView.as_view()),

    # Logout → refresh token blacklist করে
    path("api/auth/logout/", TokenBlacklistView.as_view()),
]
```

---

### 💻 Custom Logout View:

```python
# authentication/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

class LogoutView(APIView):

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()   # Token blacklist-এ যোগ করো

            return Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_200_OK
            )

        except TokenError:
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )
```

---

### 💻 Protected View — JWT দিয়ে:

```python
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class AccountBalanceView(APIView):
    permission_classes = [IsAuthenticated]   # JWT verify হবে

    def get(self, request, account_id):
        # request.user → JWT থেকে automatically set
        user = request.user

        # JWT payload থেকে custom claim পাও
        account_id_from_token = request.auth.payload.get("account_id")

        # Security check — নিজের account কিনা
        if account_id != account_id_from_token:
            return Response(
                {"error": "Unauthorized"},
                status=403
            )

        account = Account.objects.get(account_id=account_id)
        return Response({"balance": account.balance})


# Custom Permission
class IsTeller(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.auth.payload.get("role") == "teller"
        )

class TransactionApprovalView(APIView):
    permission_classes = [IsAuthenticated, IsTeller]   # Teller only

    def post(self, request):
        # শুধু Teller access করতে পারবে
        ...
```

---

### ⚠️ JWT Security Best Practices:

```python
# ১. Short Access Token lifetime
ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)   # ✅
# ❌ না: timedelta(days=30) — compromise হলে ৩০ দিন exposed

# ২. HTTPS only — token কখনো HTTP-তে না
SECURE_SSL_REDIRECT = True

# ৩. Sensitive data payload-এ না
# ❌ Bad
token["password"] = user.password
token["pin"] = user.pin

# ✅ Good — শুধু identifier
token["user_id"] = user.id
token["role"] = user.role

# ৪. Token rotation
ROTATE_REFRESH_TOKENS = True      # প্রতিবার নতুন refresh token
BLACKLIST_AFTER_ROTATION = True   # পুরনো invalid

# ৫. Logout-এ blacklist
token.blacklist()   # DB-তে store করো
```

---

## ৩. OAuth2 — কীভাবে কাজ করে

---

### 🔑 এক কথায়:

> OAuth2 = Open Authorization — **Third-party app-কে** তোমার resource-এ **limited access** দেওয়ার standard protocol। তোমার password না দিয়েই।

সহজ analogy:
```
Hotel-এ check-in করলে একটা Key Card পাও
এই key card দিয়ে শুধু নিজের room খোলা যায়
Security room, Pool room খোলা যায় না

OAuth2 = সেই Key Card System
তুমি Google account-এর password না দিয়ে
"Google দিয়ে Login" করলে শুধু
নির্দিষ্ট কিছু access দিলে
```

---

### 🔄 OAuth2 Flow — Authorization Code (Most Secure):

```
User          Client App         Auth Server      Resource Server
  │               │              (Google/FB)      (API)
  │               │                   │               │
  │─ Login ──────→│                   │               │
  │               │── Redirect ──────→│               │
  │               │   /authorize      │               │
  │←─────── Login Page ──────────────│               │
  │                                   │               │
  │─ Google credentials ─────────────→│               │
  │                                   │ Verify        │
  │←── Consent Screen ───────────────│               │
  │    "Allow access to: email, name" │               │
  │                                   │               │
  │─ Allow ──────────────────────────→│               │
  │                                   │               │
  │←─────── Redirect with Code ───────│               │
  │         /callback?code=AUTH_CODE  │               │
  │               │                   │               │
  │               │── code + secret ─→│               │
  │               │                   │ Verify        │
  │               │←── Access Token ──│               │
  │               │                   │               │
  │               │── Bearer Token ───────────────────→│
  │               │                   │  Return Data  │
  │               │←──────────────────────────────────│
  │←─ Data ───────│                   │               │
```

---

### 💻 OAuth2 Implement — django-oauth-toolkit:

**Install:**
```bash
pip install django-oauth-toolkit
```

**settings.py:**
```python
INSTALLED_APPS = [
    ...
    "oauth2_provider",
    "rest_framework",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

OAUTH2_PROVIDER = {
    "ACCESS_TOKEN_EXPIRE_SECONDS": 3600,      # 1 hour
    "REFRESH_TOKEN_EXPIRE_SECONDS": 86400,    # 1 day
    "SCOPES": {
        "read": "Read access",
        "write": "Write access",
        "transactions": "View transactions",
        "transfer": "Transfer money",
        "admin": "Admin access",
    }
}
```

---

### 💻 OAuth2 Views:

```python
# urls.py
from django.urls import path, include
from oauth2_provider import urls as oauth2_urls

urlpatterns = [
    path("o/", include(oauth2_urls)),         # OAuth2 endpoints
    path("api/", include("accounts.urls")),
]

# Automatically generates:
# /o/authorize/    ← User consent
# /o/token/        ← Get token
# /o/revoke_token/ ← Revoke token
# /o/introspect/   ← Token info
```

---

### 💻 Scope-based Permission — Banking:

```python
from oauth2_provider.contrib.rest_framework import (
    TokenHasReadWriteScope,
    TokenHasScope
)

class AccountView(APIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request):
        # "read" scope দরকার
        return Response({"balance": 50000})

    def post(self, request):
        # "write" scope দরকার
        return Response({"status": "created"})


class TransferView(APIView):
    # "transfer" scope ছাড়া access নেই
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ["transfer"]

    def post(self, request):
        # শুধু transfer scope থাকলে আসতে পারবে
        amount = request.data.get("amount")
        return Response({"status": "transferred"})


class AdminView(APIView):
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ["admin"]

    def get(self, request):
        # Admin scope ছাড়া 403
        return Response({"all_accounts": [...]})
```

---

### 💻 Third-party Login — Google OAuth2:

```python
# social-auth-app-django use করে
# pip install social-auth-app-django

# settings.py
AUTHENTICATION_BACKENDS = [
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "Google Client ID"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "Google Client Secret"
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "email",
    "profile"
]

# Pipeline — Login হলে কী করবে
SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    "mybank.pipeline.create_bank_profile",   # Custom step
    "social_core.pipeline.social_auth.associate_user",
)


# Custom pipeline — Google login-এ bank profile তৈরি
def create_bank_profile(backend, user, response, *args, **kwargs):
    from accounts.models import UserProfile

    if not hasattr(user, "profile"):
        UserProfile.objects.create(
            user=user,
            email=response.get("email"),
            name=response.get("name"),
            auth_provider="google"
        )
```

---

### 📊 JWT vs OAuth2 — কোনটা কখন:

| | JWT | OAuth2 |
|---|---|---|
| **Use case** | API Authentication | Third-party Authorization |
| **Password share** | হ্যাঁ (নিজের system) | না |
| **Scope control** | Basic | Fine-grained ✅ |
| **Third-party** | ❌ | ✅ |
| **Complexity** | কম | বেশি |
| **Banking internal** | ✅ Best | ❌ Overkill |
| **Partner API** | মাঝারি | ✅ Best |
| **Social Login** | ❌ | ✅ |

---

### 🏦 Banking-এ কোনটা কোথায়:

```
UCB Banking System

Internal API (Mobile App ↔ Backend)
└── JWT Authentication ✅
    → Customer login করে JWT পায়
    → Balance check, Transaction করে

Partner Integration (Bkash, SSLCommerz)
└── OAuth2 ✅
    → Limited scope দেওয়া যায়
    → "শুধু payment verify করতে পারবে"
    → "balance দেখতে পারবে না"

Admin Dashboard
└── JWT + Role-based Permission ✅
    → role: "admin" claim check করে

Third-party Fintech App
└── OAuth2 Authorization Code ✅
    → User নিজে consent দেয়
    → "এই app আমার transaction দেখতে পারবে"
```

---

### 🎯 Interview Closing line:

> *"Banking system-এ internal API-তে JWT use করি — stateless, fast, আর mobile app-এর জন্য perfect। Access token 15 minutes, refresh token 7 days, logout-এ blacklist। Partner integration-এ OAuth2 — কারণ Bkash বা SSLCommerz-কে শুধু specific scope-এ access দেওয়া দরকার, full account access না। JWT payload-এ role আর branch_id রাখি যাতে প্রতিটা request-এ DB query না লাগে।"*

---

পরের গুরুত্বপূর্ণ topics:
- **REST API Design Best Practices**
- **Database Indexing + Transaction**
- **SOLID Principles**
- **Design Patterns — Singleton, Factory, Repository**

কোনটা নিয়ে আগাবে?

## Django/DRF — ৭টা Important Topic

---

## ১. Migration কী?

---

### 🔑 এক কথায়:

> Migration হলো Django-র **database schema version control** — Model-এ change করলে সেই change Database-এ apply করার mechanism।

সহজ analogy:
```
Git = Code-এর version control
Migration = Database-এর version control

models.py change করলে → migration file তৈরি হয়
migration apply করলে → Database table change হয়
```

---

### 💻 Migration Workflow:

```bash
# Step 1: Model বানাও বা change করো
# accounts/models.py

# Step 2: Migration file তৈরি করো
python manage.py makemigrations
# accounts/migrations/0001_initial.py তৈরি হলো

# Step 3: Database-এ apply করো
python manage.py migrate

# Status দেখো
python manage.py showmigrations
# accounts
#  [X] 0001_initial          ← applied
#  [ ] 0002_add_phone_field   ← not applied
```

---

### 💻 Migration File — ভেতরে কী থাকে:

```python
# accounts/migrations/0001_initial.py
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = []   # আগে কোন migration চালাতে হবে

    operations = [
        migrations.CreateTable(
            name="Account",
            fields=[
                ("id", models.AutoField(primary_key=True)),
                ("account_id", models.CharField(max_length=20)),
                ("name", models.CharField(max_length=100)),
                ("balance", models.DecimalField(
                    max_digits=15, decimal_places=2
                )),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
```

---

### 💻 Common Migration Operations:

```python
# Model-এ field যোগ করলে
class Account(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True)  # নতুন field

# makemigrations চালালে:
# 0002_account_phone.py তৈরি হয়
# ALTER TABLE accounts ADD COLUMN phone VARCHAR(15);

# Field rename
python manage.py makemigrations --name rename_phone_to_mobile

# Data migration — data manipulate করো
from django.db import migrations

def set_default_branch(apps, schema_editor):
    Account = apps.get_model("accounts", "Account")
    Account.objects.filter(branch=None).update(branch_id=1)

class Migration(migrations.Migration):
    dependencies = [("accounts", "0003_account_branch")]

    operations = [
        migrations.RunPython(
            set_default_branch,           # forward
            migrations.RunPython.noop     # backward (rollback)
        ),
    ]
```

---

### 💻 Migration Commands:

```bash
# Rollback — আগের migration-এ ফিরে যাও
python manage.py migrate accounts 0001

# Specific app-এর migration
python manage.py makemigrations accounts

# SQL দেখো — apply না করে
python manage.py sqlmigrate accounts 0001

# Fake migration — DB already আছে কিন্তু record নেই
python manage.py migrate --fake accounts 0001

# Squash — অনেক migration একটায় কমাও
python manage.py squashmigrations accounts 0001 0010
```

---

## ২. Signals কী?

---

### 🔑 এক কথায়:

> Signal হলো Django-র **event system** — কোনো কিছু ঘটলে (model save, delete) automatically অন্য code চালানো যায়, বিনা coupling-এ।

সহজ analogy:
```
Signal = WhatsApp notification

তুমি message পাঠালে (event)
তোমার phone-এ notification আসে (handler)
তুমি জানো না কে দেখবে — decoupled ✅
```

---

### 💻 Built-in Signals:

```python
# Model signals
pre_save     → save() এর আগে
post_save    → save() এর পরে
pre_delete   → delete() এর আগে
post_delete  → delete() এর পরে

# Request signals
request_started   → request আসার সময়
request_finished  → response যাওয়ার সময়
```

---

### 💻 Signal Use করো:

**উপায় ১ — `@receiver` decorator:**
```python
# accounts/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Account, Transaction

@receiver(post_save, sender=Account)
def account_created_handler(sender, instance, created, **kwargs):
    if created:
        # নতুন account তৈরি হলে
        print(f"New account: {instance.account_id}")

        # Welcome SMS পাঠাও
        send_sms(
            instance.phone,
            f"Welcome to UCB! Account: {instance.account_id}"
        )

        # Default settings তৈরি করো
        AccountSettings.objects.create(
            account=instance,
            daily_limit=50000,
            sms_alert=True
        )


@receiver(post_save, sender=Transaction)
def transaction_notification(sender, instance, created, **kwargs):
    if created:
        # Transaction হলে SMS alert
        send_sms(
            instance.account.phone,
            f"TXN: {instance.txn_type} {instance.amount} BDT. "
            f"Balance: {instance.balance_after} BDT"
        )


@receiver(pre_save, sender=Account)
def log_balance_change(sender, instance, **kwargs):
    if instance.pk:
        # Update হচ্ছে — আগের value দেখো
        old = Account.objects.get(pk=instance.pk)
        if old.balance != instance.balance:
            AuditLog.objects.create(
                account=instance,
                old_balance=old.balance,
                new_balance=instance.balance,
                changed_by="system"
            )
```

**apps.py-তে Register করো:**
```python
# accounts/apps.py
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = "accounts"

    def ready(self):
        import accounts.signals   # signals import করো ✅
```

---

### 💻 Custom Signal বানাও:

```python
# signals.py
from django.dispatch import Signal

# Custom signal define করো
fraud_detected = Signal()
large_transaction = Signal()

# যেখানে event হয় সেখানে send করো
def process_transaction(account, amount):
    if amount > 100000:
        large_transaction.send(
            sender=account.__class__,
            account=account,
            amount=amount
        )

    risk_score = fraud_checker.check(account, amount)
    if risk_score > 0.8:
        fraud_detected.send(
            sender=account.__class__,
            account=account,
            risk_score=risk_score
        )


# Handler
@receiver(fraud_detected)
def handle_fraud(sender, account, risk_score, **kwargs):
    account.freeze()
    notify_security_team(account, risk_score)
    logger.critical(f"FRAUD: {account.account_id}, score: {risk_score}")


@receiver(large_transaction)
def handle_large_transaction(sender, account, amount, **kwargs):
    # Bangladesh Bank reporting — ১ লাখের বেশি
    bangladesh_bank_report(account, amount)
```

---

### ⚠️ Signal-এর সতর্কতা:

```python
# ❌ Signal-এ heavy কাজ করো না — request block হবে
@receiver(post_save, sender=Transaction)
def bad_handler(sender, instance, **kwargs):
    generate_pdf_report()   # ❌ Slow! Request block হবে
    send_email()            # ❌ Slow!

# ✅ Celery task-এ পাঠাও — async
@receiver(post_save, sender=Transaction)
def good_handler(sender, instance, **kwargs):
    generate_pdf_report.delay(instance.id)   # ✅ Async
    send_email.delay(instance.account.email) # ✅ Async
```

---

## ৩. DRF কেন Use করো?

---

### 🔑 DRF = Django REST Framework:

```python
# Without DRF — manually সব করতে হয়
import json
from django.http import JsonResponse
from django.views import View

class AccountView(View):
    def get(self, request, account_id):
        try:
            account = Account.objects.get(account_id=account_id)
            # Manually serialize করো
            data = {
                "account_id": account.account_id,
                "name": account.name,
                "balance": str(account.balance),  # Decimal manually handle
            }
            return JsonResponse(data)
        except Account.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

    def post(self, request):
        # Manually parse request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Manually validate
        if not data.get("name"):
            return JsonResponse({"error": "Name required"}, status=400)
        # ...আরো অনেক কিছু manually 😫


# With DRF — সব ready ✅
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AccountView(APIView):
    def get(self, request, account_id):
        account = get_object_or_404(Account, account_id=account_id)
        serializer = AccountSerializer(account)
        return Response(serializer.data)   # ✅ Auto JSON

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():          # ✅ Auto validation
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

---

### 📊 DRF কী কী দেয়:

| Feature | DRF | Without DRF |
|---|---|---|
| Serialization | ✅ Auto | ❌ Manual |
| Validation | ✅ Built-in | ❌ Manual |
| Authentication | ✅ Multiple | ❌ Manual |
| Permissions | ✅ Class-based | ❌ Manual |
| Pagination | ✅ Built-in | ❌ Manual |
| Browsable API | ✅ GUI | ❌ না |
| Content Negotiation | ✅ Auto | ❌ Manual |
| Throttling | ✅ Built-in | ❌ Manual |

---

## ৪. APIView vs GenericAPIView

---

### 💻 APIView — Full Control:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AccountListView(APIView):
    """সব manually করতে হয় — কিন্তু full control"""

    def get(self, request):
        accounts = Account.objects.filter(is_active=True)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class AccountDetailView(APIView):

    def get_object(self, account_id):
        try:
            return Account.objects.get(account_id=account_id)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, account_id):
        account = self.get_object(account_id)
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    def put(self, request, account_id):
        account = self.get_object(account_id)
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, account_id):
        account = self.get_object(account_id)
        account.delete()
        return Response(status=204)
```

---

### 💻 GenericAPIView — Mixins দিয়ে DRY:

```python
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

# List + Create — দুটো method একটা class-এ ✅
class AccountListCreateView(ListCreateAPIView):
    queryset = Account.objects.filter(is_active=True)
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    # Override করে customize করা যায়
    def get_queryset(self):
        # নিজের account শুধু দেখাও
        return Account.objects.filter(
            user=self.request.user,
            is_active=True
        )

    def perform_create(self, serializer):
        # Save-এর সময় extra data যোগ করো
        serializer.save(
            user=self.request.user,
            created_by=self.request.user.username
        )


# Retrieve + Update + Delete
class AccountDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = "account_id"   # pk-র বদলে account_id দিয়ে খুঁজবে

    def perform_destroy(self, instance):
        # Hard delete না — soft delete করো
        instance.is_active = False
        instance.save()
```

---

### 📊 Generic Views — কোনটা কী:

| Class | Methods | কখন |
|---|---|---|
| `ListAPIView` | GET (list) | শুধু list |
| `CreateAPIView` | POST | শুধু create |
| `RetrieveAPIView` | GET (detail) | শুধু detail |
| `UpdateAPIView` | PUT/PATCH | শুধু update |
| `DestroyAPIView` | DELETE | শুধু delete |
| `ListCreateAPIView` | GET + POST | List + Create |
| `RetrieveUpdateDestroyAPIView` | GET+PUT+DELETE | Detail + Update + Delete |

---

## ৫. ViewSet vs APIView

---

### 💻 APIView — প্রতিটা URL আলাদা:

```python
# Views
class AccountListView(APIView): ...      # GET /accounts/
class AccountDetailView(APIView): ...    # GET /accounts/{id}/
class AccountCreateView(APIView): ...    # POST /accounts/

# URLs — manually লিখতে হয়
urlpatterns = [
    path("accounts/", AccountListView.as_view()),
    path("accounts/create/", AccountCreateView.as_view()),
    path("accounts/<str:id>/", AccountDetailView.as_view()),
]
```

---

### 💻 ViewSet — একটা Class-এ সব:

```python
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

class AccountViewSet(ModelViewSet):
    """CRUD সব এক জায়গায় ✅"""
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "account_id"

    # list()    → GET /accounts/
    # create()  → POST /accounts/
    # retrieve()→ GET /accounts/{id}/
    # update()  → PUT /accounts/{id}/
    # destroy() → DELETE /accounts/{id}/
    # সব automatically আছে ✅

    # Custom action — extra endpoint
    @action(detail=True, methods=["post"])
    def deposit(self, request, account_id=None):
        account = self.get_object()
        amount = request.data.get("amount")
        account.balance += amount
        account.save()
        return Response({"balance": account.balance})
    # → POST /accounts/{id}/deposit/

    @action(detail=True, methods=["get"])
    def statement(self, request, account_id=None):
        account = self.get_object()
        txns = account.transactions.all()
        serializer = TransactionSerializer(txns, many=True)
        return Response(serializer.data)
    # → GET /accounts/{id}/statement/

    def get_serializer_class(self):
        # Action অনুযায়ী আলাদা serializer
        if self.action == "list":
            return AccountListSerializer
        return AccountDetailSerializer

    def get_permissions(self):
        # Action অনুযায়ী আলাদা permission
        if self.action == "destroy":
            return [IsAdminUser()]
        return [IsAuthenticated()]


# Router — URLs automatically তৈরি হয় ✅
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("accounts", AccountViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]

# Generates:
# GET    /api/accounts/              → list
# POST   /api/accounts/              → create
# GET    /api/accounts/{id}/         → retrieve
# PUT    /api/accounts/{id}/         → update
# PATCH  /api/accounts/{id}/         → partial_update
# DELETE /api/accounts/{id}/         → destroy
# POST   /api/accounts/{id}/deposit/ → deposit (custom)
# GET    /api/accounts/{id}/statement/→ statement (custom)
```

---

### 📊 APIView vs ViewSet:

| | APIView | ViewSet |
|---|---|---|
| **Control** | ✅ Full | মাঝারি |
| **Code** | বেশি | কম ✅ |
| **URL** | Manual | Router auto ✅ |
| **Custom logic** | ✅ সহজ | `@action` দিয়ে |
| **Standard CRUD** | Repetitive | ✅ Built-in |
| **Complex API** | ✅ Better | কঠিন |

---

## ৬. Serializer vs ModelSerializer

---

### 💻 Serializer — সব manually:

```python
from rest_framework import serializers

class AccountSerializer(serializers.Serializer):
    # প্রতিটা field manually define করতে হয়
    account_id = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=100)
    balance = serializers.DecimalField(max_digits=15, decimal_places=2)
    is_active = serializers.BooleanField(default=True)

    def create(self, validated_data):
        # Manually create করতে হয়
        return Account.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Manually update করতে হয়
        instance.name = validated_data.get("name", instance.name)
        instance.balance = validated_data.get("balance", instance.balance)
        instance.save()
        return instance
```

---

### 💻 ModelSerializer — Auto:

```python
class AccountSerializer(serializers.ModelSerializer):
    # Model থেকে automatically field নেয়
    class Meta:
        model = Account
        fields = ["account_id", "name", "balance", "is_active"]
        read_only_fields = ["account_id", "created_at"]
        extra_kwargs = {
            "balance": {"min_value": 0},
            "name": {"min_length": 2}
        }
    # create() আর update() automatically আছে ✅


# Nested Serializer
class TransactionSerializer(serializers.ModelSerializer):
    # Related object-এর data include করো
    account = AccountSerializer(read_only=True)
    account_id = serializers.CharField(write_only=True)

    class Meta:
        model = Transaction
        fields = ["id", "account", "account_id", "amount", "txn_type"]


# Custom Field
class AccountDetailSerializer(serializers.ModelSerializer):
    # Computed field — Model-এ নেই
    full_name = serializers.SerializerMethodField()
    transaction_count = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ["account_id", "full_name", "balance", "transaction_count"]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_transaction_count(self, obj):
        return obj.transactions.count()
```

---

### 📊 Serializer vs ModelSerializer:

| | Serializer | ModelSerializer |
|---|---|---|
| **Field define** | Manual | Auto from Model ✅ |
| **create/update** | Manual | Auto ✅ |
| **Validation** | Manual | Auto ✅ |
| **Flexibility** | ✅ বেশি | কম |
| **Non-model data** | ✅ | ❌ |
| **Code** | বেশি | কম ✅ |

---

## ৭. Validation কোথায় করা উচিত?

---

### 🔑 Validation-এর ৩টা স্তর:

```
Request আসলো
     ↓
1. Serializer Validation  ← Data format, type, constraint
     ↓
2. Business Logic Validation ← Banking rules
     ↓
3. Database Constraint   ← Last resort, DB-level
```

---

### 💻 স্তর ১ — Serializer Validation:

```python
class WithdrawSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    pin = serializers.CharField(min_length=4, max_length=6)
    note = serializers.CharField(required=False, max_length=200)

    # Field-level validation
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be positive"
            )
        if value > 500000:
            raise serializers.ValidationError(
                "Single transaction limit 5 lakh BDT"
            )
        return value

    def validate_pin(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("PIN must be numeric")
        return value

    # Object-level validation — multiple fields একসাথে
    def validate(self, attrs):
        amount = attrs.get("amount")
        pin = attrs.get("pin")

        # PIN verify করো
        user = self.context["request"].user
        if not user.check_pin(pin):
            raise serializers.ValidationError({
                "pin": "Invalid PIN"
            })

        return attrs
```

---

### 💻 স্তর ২ — Business Logic Validation:

```python
class WithdrawView(APIView):

    def post(self, request, account_id):
        # Serializer validation আগে
        serializer = WithdrawSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data["amount"]

        # Business logic validation — View বা Service-এ
        account = Account.objects.get(account_id=account_id)

        # Rule 1: Balance check
        if account.balance < amount:
            raise InsufficientBalanceError(
                account_id, amount, account.balance
            )

        # Rule 2: Daily limit check
        today_total = Transaction.objects.filter(
            account=account,
            txn_type="DR",
            created_at__date=today()
        ).aggregate(Sum("amount"))["amount__sum"] or 0

        if today_total + amount > account.daily_limit:
            raise DailyLimitExceededError(
                account_id,
                account.daily_limit,
                amount
            )

        # Rule 3: Account status check
        if not account.is_active:
            raise AccountFrozenError(account_id, "Account inactive")

        # All good — proceed
        with transaction.atomic():
            account.balance -= amount
            account.save()
```

---

### 💻 স্তর ৩ — Model-level Validation:

```python
class Account(models.Model):
    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    # Model-level constraint — DB-তেও enforce হয়
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(balance__gte=0),
                name="balance_non_negative"
            )
        ]

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.balance < 0:
            raise ValidationError("Balance cannot be negative")
```

---

### 📊 Validation কোথায় কী:

| Validation Type | কোথায় | উদাহরণ |
|---|---|---|
| **Format/Type** | Serializer field | amount > 0, PIN numeric |
| **Cross-field** | Serializer `validate()` | PIN verify |
| **Business Rule** | View/Service | Daily limit, balance check |
| **Data Integrity** | Model `clean()` | Balance >= 0 |
| **DB Constraint** | Model `Meta.constraints` | Last resort |

---

### 🎯 Interview Closing line:

> *"Validation তিনটা স্তরে রাখি — Serializer-এ data format আর type, View বা Service layer-এ banking business rules, Model-এ data integrity constraint। Migration দিয়ে schema changes version control করি — production-এ কোনো manual SQL লাগে না। Signal use করি transaction notification আর audit log-এর জন্য, তবে heavy কাজ Celery-তে পাঠাই যাতে request block না হয়। ViewSet আর Router দিয়ে standard CRUD-এ code অনেক কমে যায়।"*

---

পরের গুরুত্বপূর্ণ topics:
- **Database Indexing + Transaction**
- **REST API Design Best Practices**
- **SOLID Principles**
- **Design Patterns — Singleton, Factory, Repository**
- **Celery + Redis**

কোনটা নিয়ে আগাবে?