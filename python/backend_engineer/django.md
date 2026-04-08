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