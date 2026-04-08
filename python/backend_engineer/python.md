## Python কেন use করো backend-এ?

এটা একটা **very common interview question** — এবং তোমাকে confident ও structured ভাবে answer দিতে হবে।

---

### ✅ Strong Answer Structure (STAR-style নয়, Point-based):

---

**১. Simple & Readable Syntax**
Python-এর syntax অনেক clean। Code লেখা ও maintain করা সহজ, তাই team-এ কাজ করার সময় productivity বাড়ে।

---

**২. Powerful Frameworks আছে**
Backend development-এর জন্য mature framework আছে:
- **Django** → full-featured, batteries included, rapid development
- **FastAPI** → modern, async support, automatic API docs
- **Flask** → lightweight, microservices-এর জন্য ভালো

---

**৩. Database Integration সহজ**
PostgreSQL, MySQL, MongoDB — সব কিছুর সাথে Python সহজে কাজ করে। Django ORM বা SQLAlchemy দিয়ে complex query লেখা অনেক সুবিধাজনক।

---

**৪. Security Features**
Django-তে built-in থাকে:
- CSRF protection
- SQL Injection prevention
- Authentication system

Banking sector-এ এটা খুব important।

---

**৫. Scalability & Performance**
Async support (FastAPI, asyncio) দিয়ে high-traffic handle করা যায়। Celery দিয়ে background task চালানো যায় — যেটা banking transaction processing-এ useful।

---

**৬. Rich Ecosystem**
Data processing, automation, API integration — সব কাজে Python-এর library পাওয়া যায়। Financial sector-এ data analysis এর দরকার হয়, সেখানে Python এগিয়ে।

---

### 🎯 Interview-এ যা বলবে (Closing line):

> *"Python choose করার কারণ হলো এটা development speed, security, আর maintainability — তিনটাই একসাথে দেয়। Banking sector-এর মতো critical system-এ এই balance অনেক important।"*

---

আরো কোন question practice করতে চাও? যেমন — Django vs FastAPI, REST API design, authentication/JWT, database optimization?



## Python Interpreted মানে কী?

---

### 🔑 Core Concept:

**Interpreted** মানে হলো — Python code **line by line** পড়া হয় এবং **সাথে সাথে execute** করা হয়। আগে থেকে পুরো code compile করে machine code বানানো হয় না।

---

### ⚖️ Compiled vs Interpreted — পার্থক্য:

| | Compiled (C, Java) | Interpreted (Python) |
|---|---|---|
| কীভাবে চলে | আগে পুরোটা compile → তারপর run | Line by line পড়ে সাথে সাথে run |
| Error কখন ধরে | Compile time-এ | Runtime-এ |
| Speed | তুলনামূলক দ্রুত | কিছুটা ধীর |
| Flexibility | কম | বেশি |

---

### 🔄 Python-এ আসলে কী হয় পর্দার পেছনে:

```
তোমার .py file
      ↓
CPython interpreter পড়ে
      ↓
Bytecode (.pyc) এ convert হয়
      ↓
Python Virtual Machine (PVM) execute করে
```

> Python technically **bytecode-compiled + interpreted** — কিন্তু interview-এ "interpreted language" বলাই standard।

---

### 🏦 Banking Context-এ এর প্রভাব:

**সুবিধা →**
- Rapid development — features তাড়াতাড়ি deploy করা যায়
- Debugging সহজ — error exactly কোন line-এ সেটা দেখা যায়
- Dynamic typing — flexible code লেখা যায়

**অসুবিধা →**
- C বা Java-র তুলনায় কিছুটা slow
- কিন্তু banking app-এ **bottleneck সাধারণত database বা network**, Python-এর speed নয় — তাই practically সমস্যা হয় না

---

### 🎯 Interview-এ Closing line:

> *"Python interpreted হওয়ায় development cycle অনেক fast হয়। আর banking system-এ যেখানে frequently নতুন feature add করতে হয়, সেখানে এটা একটা বড় advantage।"*

---

পরের question practice করবে? **GIL (Global Interpreter Lock)** নিয়ে জিজ্ঞেস করতে পারে — ওটা একটু tricky কিন্তু important।



## Mutable vs Immutable

---

### 🔑 এক কথায়:

| | মানে | উদাহরণ |
|---|---|---|
| **Mutable** | Create করার পরেও **change করা যায়** | list, dict, set |
| **Immutable** | Create করার পর **change করা যায় না** | int, string, tuple |

---

### 💻 Code দিয়ে বোঝো:

**Mutable — List:**
```python
my_list = [1, 2, 3]
my_list[0] = 99
print(my_list)  # [99, 2, 3] ✅ change হয়ে গেছে
```

**Immutable — String:**
```python
name = "Sourov"
name[0] = "T"  # ❌ TypeError! change করা যাবে না
```

**Immutable — Tuple:**
```python
point = (10, 20)
point[0] = 99  # ❌ TypeError!
```

---

### 🧠 Memory-তে আসলে কী হয়:

**Mutable:**
```
my_list → [1, 2, 3]   (same memory address, value change হয়)
my_list → [99, 2, 3]  ← same object, modified
```

**Immutable:**
```python
x = "hello"
x = "world"   # "hello" object নষ্ট হয়নি
              # x এখন নতুন object "world" কে point করছে
```
> Immutable object **নিজে বদলায় না** — নতুন object তৈরি হয়।

---

### ⚠️ Tricky Interview Trap:

```python
a = [1, 2, 3]
b = a          # same object!

b.append(99)
print(a)       # [1, 2, 3, 99] 😱

# কারণ — a আর b একই memory location point করছে
```

**Fix:**
```python
b = a.copy()   # এখন আলাদা object
```

---

### 🏦 Banking Context-এ কেন Important:

- **Transaction data** → Tuple use করো, কেউ accidentally change করতে পারবে না
- **Config values** → Immutable রাখলে system safer হয়
- **User session data** → Dict (mutable) use করো কারণ update দরকার হয়

---

### 🎯 Interview Closing line:

> *"Immutable objects thread-safe — banking system-এ concurrent requests handle করার সময় immutable data race condition থেকে রক্ষা করে।"*

---

এরপর **`*args` vs `**kwargs`**, অথবা **List vs Tuple কোনটা কখন use করবে** — এগুলো জিজ্ঞেস করতে পারে। Practice করবে?


## List vs Tuple vs Set vs Dict

---

### 🗺️ এক নজরে চারটা:

| Feature | List | Tuple | Set | Dict |
|---|---|---|---|---|
| **Syntax** | `[1,2,3]` | `(1,2,3)` | `{1,2,3}` | `{"k":"v"}` |
| **Mutable** | ✅ হ্যাঁ | ❌ না | ✅ হ্যাঁ | ✅ হ্যাঁ |
| **Ordered** | ✅ হ্যাঁ | ✅ হ্যাঁ | ❌ না | ✅ হ্যাঁ (Python 3.7+) |
| **Duplicate** | ✅ allowed | ✅ allowed | ❌ না | Key-এ না |
| **Indexing** | ✅ হ্যাঁ | ✅ হ্যাঁ | ❌ না | Key দিয়ে |
| **Speed** | মাঝারি | দ্রুত | সবচেয়ে দ্রুত (lookup) | দ্রুত (lookup) |

---

### 💻 Code Example:

```python
# List — ordered, changeable
transactions = [500, 1000, 250, 1000]
transactions.append(750)        # add করা যায়
print(transactions[0])          # 500 — index কাজ করে

# Tuple — fixed data
account_info = ("Sourov", "UCB", "SB-001")
# account_info[0] = "X"  ❌ পারবে না

# Set — unique values only
visited_branches = {"Dhaka", "Chittagong", "Dhaka"}
print(visited_branches)  # {"Dhaka", "Chittagong"} — duplicate নেই

# Dict — key-value pair
user = {
    "name": "Sourov",
    "balance": 50000,
    "account": "SB-001"
}
print(user["balance"])   # 50000
```

---

### ⚠️ Tricky Interview Questions:

**১. Empty set কীভাবে বানাবে?**
```python
s = set()    # ✅ সঠিক
s = {}       # ❌ এটা empty dict হয়ে যাবে!
```

**২. List থেকে duplicate সরাবে কীভাবে?**
```python
nums = [1, 2, 2, 3, 3, 3]
unique = list(set(nums))
print(unique)  # [1, 2, 3]
```

**৩. Tuple কি সত্যিই সবসময় immutable?**
```python
t = ([1, 2], [3, 4])  # tuple-এর ভেতরে list
t[0].append(99)       # ✅ এটা কিন্তু কাজ করবে!
print(t)              # ([1, 2, 99], [3, 4])
# Tuple immutable — কিন্তু ভেতরের list mutable থাকে
```

---

### 🏦 Banking System-এ কোনটা কোথায়:

| Use Case | Data Structure | কেন |
|---|---|---|
| Transaction history | **List** | Order important, duplicate থাকতে পারে |
| Account holder info | **Tuple** | Fixed data, change হওয়া উচিত না |
| Active session IDs | **Set** | Duplicate চাই না, fast lookup দরকার |
| User profile | **Dict** | Key দিয়ে দ্রুত access দরকার |
| Branch codes (fixed) | **Tuple** | Immutable — accidental change এড়াতে |

---

### 🎯 Interview Closing line:

> *"Data structure choice করার সময় তিনটা জিনিস দেখি — data কি change হবে, order important কিনা, আর lookup speed কেমন দরকার। Banking system-এ wrong data structure মানেই performance আর security risk।"*

---

এরপর সম্ভাব্য প্রশ্ন:
- **`dict.get()` vs `dict[]` — পার্থক্য কী?**
- **List Comprehension**
- **OOP concepts**

কোনটা নিয়ে আগাবে?




## Deep Copy vs Shallow Copy

---

### 🔑 এক কথায়:

| | মানে |
|---|---|
| **Shallow Copy** | নতুন object তৈরি হয়, কিন্তু **ভেতরের objects একই** থাকে |
| **Deep Copy** | নতুন object তৈরি হয়, ভেতরের **সব objects-ও নতুন** হয় |

---

### 🧠 Visual দিয়ে বোঝো:

```
Original:    [1, 2, [10, 20]]
              ↑        ↑
           simple   nested list

Shallow Copy:  নতুন box, কিন্তু nested list-এর arrow একই জায়গায়
Deep Copy:     নতুন box, nested list-ও আলাদা নতুন copy
```

---

### 💻 Code Example:

```python
import copy

original = [1, 2, [10, 20]]

# Shallow Copy
shallow = copy.copy(original)

# Deep Copy
deep = copy.deepcopy(original)
```

**Shallow-এ কী হয়:**
```python
shallow[0] = 99
print(original)   # [1, 2, [10, 20]] ✅ outer change হয়নি

shallow[2].append(30)
print(original)   # [1, 2, [10, 20, 30]] 😱 nested list change হয়ে গেছে!
```

**Deep-এ কী হয়:**
```python
deep[2].append(30)
print(original)   # [1, 2, [10, 20]] ✅ কিছুই change হয়নি
```

---

### ⚠️ Tricky Point — `=` vs Shallow vs Deep:

```python
a = [1, 2, [10, 20]]

b = a               # copy না! same object
c = copy.copy(a)    # shallow copy
d = copy.deepcopy(a)  # deep copy

b[0] = 99
print(a)  # [99, 2, [10, 20]] 😱 a-ও change হয়েছে

c[2].append(30)
print(a)  # [99, 2, [10, 20, 30]] 😱 nested change হয়েছে

d[2].append(50)
print(a)  # [99, 2, [10, 20, 30]] ✅ কোনো change নেই
```

---

### 🏦 Banking Context-এ কেন Critical:

```python
# একজন user-এর account object
account = {
    "name": "Sourov",
    "balance": 50000,
    "transactions": [500, 1000, 250]
}

# Audit log বানাচ্ছো — snapshot দরকার
audit = copy.copy(account)       # ❌ Dangerous!
audit = copy.deepcopy(account)   # ✅ Safe
```

> Shallow copy নিলে পরে কেউ transaction list update করলে **audit log-ও বদলে যাবে** — banking-এ এটা catastrophic।

---

### 📊 কোনটা কখন use করবে:

| Situation | Use |
|---|---|
| Simple flat data (nested নেই) | `copy.copy()` — faster |
| Nested data আছে | `copy.deepcopy()` — safe |
| Same object reference চাও | `=` assignment |
| List এর quick copy | `list[:]` বা `list.copy()` — shallow |

---

### 🎯 Interview Closing line:

> *"Banking system-এ transaction history বা audit trail-এর মতো sensitive data copy করার সময় সবসময় deep copy use করবো। Shallow copy-তে original data corrupt হওয়ার risk থাকে যেটা financial system-এ কোনোভাবেই acceptable না।"*

---

পরের সম্ভাব্য প্রশ্ন:
- **`is` vs `==` — পার্থক্য কী?**
- **OOP — Class, Object, Inheritance**
- **Decorator কী?**

কোনটা নিয়ে আগাবে?





## `*args` and `**kwargs`

---

### 🔑 এক কথায়:

| | মানে | কী pass করে |
|---|---|---|
| `*args` | Variable number of **arguments** | Tuple হিসেবে |
| `**kwargs` | Variable number of **keyword arguments** | Dict হিসেবে |

> সহজ কথা — function-এ **কতটা input আসবে জানো না** তখন এগুলো use করো।

---

### 💻 `*args` — Example:

```python
def total_deposit(*args):
    print(args)        # (500, 1000, 250) — tuple
    return sum(args)

total_deposit(500, 1000, 250)   # ✅
total_deposit(100, 200)         # ✅ যেকোনো সংখ্যক argument
```

**ভেতরে loop করা যায়:**
```python
def show_transactions(*args):
    for amount in args:
        print(f"Transaction: {amount} BDT")

show_transactions(500, 1000, 750, 250)
# Transaction: 500 BDT
# Transaction: 1000 BDT
# Transaction: 750 BDT
# Transaction: 250 BDT
```

---

### 💻 `**kwargs` — Example:

```python
def create_account(**kwargs):
    print(kwargs)   # {'name': 'Sourov', 'balance': 50000} — dict

create_account(name="Sourov", balance=50000, branch="Dhaka")
```

**ভেতরে access করা:**
```python
def user_profile(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

user_profile(name="Sourov", account="SB-001", balance=50000)
# name: Sourov
# account: SB-001
# balance: 50000
```

---

### 💻 একসাথে use করা:

```python
def process(*args, **kwargs):
    print("Amounts:", args)    # tuple
    print("Info:", kwargs)     # dict

process(500, 1000, name="Sourov", branch="Dhaka")
# Amounts: (500, 1000)
# Info: {'name': 'Sourov', 'branch': 'Dhaka'}
```

---

### ⚠️ Order মানতে হবে — এটা Fixed:

```python
def func(normal, *args, **kwargs):
#         ↑         ↑        ↑
#    regular    *args    **kwargs
#    আগে        মাঝে      শেষে
    pass
```

```python
# ✅ সঠিক
def func(a, b, *args, **kwargs): pass

# ❌ ভুল — *args আগে regular argument পরে হবে না
def func(*args, a, b): pass
```

---

### 🏦 Banking Context-এ Real Use:

```python
# বিভিন্ন ধরনের transaction একটা function দিয়ে handle করা
def process_transaction(account_id, *amounts, **metadata):
    total = sum(amounts)
    print(f"Account: {account_id}")
    print(f"Total: {total} BDT")
    print(f"Type: {metadata.get('type', 'N/A')}")
    print(f"Branch: {metadata.get('branch', 'N/A')}")

process_transaction(
    "SB-001",
    500, 1000, 250,           # *args
    type="deposit",            # **kwargs
    branch="Dhaka",
    approved_by="Manager"
)
```

---

### ⚠️ Tricky Interview Question:

```python
# List বা Dict unpack করে pass করতে পারো
amounts = [500, 1000, 250]
info = {"branch": "Dhaka", "type": "deposit"}

process_transaction("SB-001", *amounts, **info)
#                              ↑           ↑
#                         list unpack   dict unpack
```

---

### 🎯 Interview Closing line:

> *"`*args` আর `**kwargs` use করলে function অনেক flexible হয় — banking system-এ যেখানে বিভিন্ন ধরনের transaction আর metadata handle করতে হয়, সেখানে এটা code reusability অনেক বাড়িয়ে দেয়।"*

---

পরের সম্ভাব্য প্রশ্ন:
- **Decorator কী?**
- **OOP — Class, Inheritance, Polymorphism**
- **Exception Handling**

কোনটা নিয়ে আগাবে?




## Decorator কী?

---

### 🔑 এক কথায়:

> Decorator হলো এমন একটা function যেটা **অন্য একটা function-কে wrap করে** — original function না বদলেই তার আগে/পরে **extra কাজ যোগ করা যায়।**

সহজ analogy:
```
ফোন = তোমার original function
কভার = decorator
কভার লাগালে ফোনের কাজ একই, শুধু extra protection যোগ হলো
```

---

### 💻 Decorator ছাড়া — সমস্যা কী:

```python
def process_payment():
    print("Payment processing...")

# প্রতিটা function-এ manually log করতে হচ্ছে
print("LOG: function শুরু হলো")
process_payment()
print("LOG: function শেষ হলো")

# ১০০টা function থাকলে ১০০ বার এটা লিখতে হবে 😫
```

---

### 💻 Decorator দিয়ে — Solution:

```python
# Step 1: Decorator বানাও
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"LOG: {func.__name__} শুরু হলো")
        result = func(*args, **kwargs)
        print(f"LOG: {func.__name__} শেষ হলো")
        return result
    return wrapper

# Step 2: @ দিয়ে apply করো
@logger
def process_payment():
    print("Payment processing...")

@logger
def check_balance():
    print("Balance checking...")

# এখন যেকোনো function-এ @logger লাগালেই হবে ✅
process_payment()
# LOG: process_payment শুরু হলো
# Payment processing...
# LOG: process_payment শেষ হলো
```

---

### 🧠 Decorator আসলে কী করে পর্দার পেছনে:

```python
@logger
def process_payment():
    ...

# এটা আসলে এর সমান:
process_payment = logger(process_payment)
```

> `@logger` মানে হলো — **"process_payment কে logger-এর ভেতরে ঢুকিয়ে দাও"**

---

### 🏦 Banking-এ Real Life Examples:

**১. Authentication Decorator:**
```python
def require_auth(func):
    def wrapper(user, *args, **kwargs):
        if not user.get("is_authenticated"):
            print("❌ Access Denied! Login করুন।")
            return None
        return func(user, *args, **kwargs)
    return wrapper

@require_auth
def transfer_money(user, amount):
    print(f"✅ {amount} BDT transfer হয়েছে")

# Test
transfer_money({"is_authenticated": False}, 5000)
# ❌ Access Denied! Login করুন।

transfer_money({"is_authenticated": True}, 5000)
# ✅ 5000 BDT transfer হয়েছে
```

**২. Transaction Log Decorator:**
```python
import datetime

def transaction_log(func):
    def wrapper(*args, **kwargs):
        time = datetime.datetime.now()
        print(f"[{time}] Transaction শুরু")
        result = func(*args, **kwargs)
        print(f"[{time}] Transaction সম্পন্ন")
        return result
    return wrapper

@transaction_log
def withdraw(amount):
    print(f"{amount} BDT উত্তোলন হয়েছে")

withdraw(10000)
```

**৩. Multiple Decorator একসাথে:**
```python
@transaction_log
@require_auth
def transfer_money(user, amount):
    print(f"{amount} BDT transfer হয়েছে")

# নিচ থেকে উপরে apply হয় — আগে auth চেক, তারপর log
```

---

### ⚠️ Tricky Interview Question:

```python
def decorator_a(func):
    def wrapper():
        print("A শুরু")
        func()
        print("A শেষ")
    return wrapper

def decorator_b(func):
    def wrapper():
        print("B শুরু")
        func()
        print("B শেষ")
    return wrapper

@decorator_a
@decorator_b
def hello():
    print("Hello!")

hello()
```

**Output কী হবে?**
```
A শুরু
B শুরু
Hello!
B শেষ
A শেষ
```
> নিচের decorator আগে apply হয়, কিন্তু উপরের decorator আগে execute হয় — **onion-এর মতো।**

---

### 📊 Banking-এ Decorator কোথায় use হয়:

| Decorator | কাজ |
|---|---|
| `@require_auth` | Login ছাড়া access বন্ধ |
| `@transaction_log` | সব transaction record রাখা |
| `@retry(3)` | Failed request আবার try করা |
| `@cache` | Same result বারবার calculate না করা |
| `@rate_limit` | একজন user বেশি request করতে না পারা |

---

### 🎯 Interview Closing line:

> *"Decorator হলো Python-এর সবচেয়ে elegant feature গুলোর একটা। Banking system-এ authentication, logging, rate limiting — এই কাজগুলো আলাদা করে রাখা যায় decorator দিয়ে, যেটা code-কে clean আর maintainable রাখে। এটা essentially AOP — Aspect Oriented Programming।"*

---

পরের সম্ভাব্য প্রশ্ন:
- **OOP — Class, Inheritance, Polymorphism**
- **Exception Handling — try/except/finally**
- **Generator vs Iterator**

কোনটা নিয়ে আগাবে?



## Generator কী? `yield` কেন use করি?

---

### 🔑 এক কথায়:

> Generator হলো এমন একটা function যেটা **একসাথে সব data return না করে**, **একটা একটা করে** দেয় — এবং মাঝখানে **pause** করে থাকতে পারে।

সহজ analogy:
```
Normal function  = পুরো বই একসাথে print করে দেওয়া
Generator        = বই পড়তে পড়তে একটা একটা page দেওয়া
                   পরের page চাইলে তখন দেবে
```

---

### 💻 Normal function vs Generator — পার্থক্য:

**Normal function — সব একসাথে:**
```python
def get_transactions():
    return [100, 200, 300, 400, 500]  # সব একসাথে memory-তে

txns = get_transactions()
print(txns)  # [100, 200, 300, 400, 500]
```

**Generator — একটা একটা করে:**
```python
def get_transactions():
    yield 100   # pause — পরেরটা চাইলে তখন দেবে
    yield 200
    yield 300
    yield 400
    yield 500

gen = get_transactions()
print(next(gen))  # 100
print(next(gen))  # 200
print(next(gen))  # 300
```

---

### 🧠 `yield` আসলে কী করে:

```
function call হলো
    ↓
100 yield করলো → pause ⏸️ (memory-তে state save থাকে)
    ↓
next() call হলো
    ↓
200 yield করলো → pause ⏸️
    ↓
next() call হলো
    ↓
300 yield করলো → pause ⏸️
    ↓
আর কিছু নেই → StopIteration ❌
```

> `return` দিলে function **শেষ** হয়ে যায়।
> `yield` দিলে function **pause** হয়, পরে আবার সেখান থেকে **resume** করে।

---

### 💻 Loop দিয়ে use করা:

```python
def get_transactions():
    transactions = [100, 200, 300, 400, 500]
    for t in transactions:
        yield t

for txn in get_transactions():
    print(f"Processing: {txn} BDT")

# Processing: 100 BDT
# Processing: 200 BDT
# Processing: 300 BDT
# ...
```

---

### 🏦 Banking-এ Real Use — কেন Critical:

**সমস্যা — ১০ লাখ transaction একসাথে load করলে:**
```python
# ❌ Bad — সব memory-তে load হয়
def get_all_transactions():
    return [tx for tx in database]  # 1,000,000 records!
    # RAM crash করতে পারে 😱

# ✅ Good — একটা একটা করে process
def get_all_transactions():
    for tx in database:
        yield tx   # শুধু একটা record memory-তে থাকে
```

**Real Example:**
```python
def process_large_report(account_id):
    # ধরো ১০ লাখ transaction আছে
    for transaction in fetch_from_db(account_id):
        yield {
            "id": transaction.id,
            "amount": transaction.amount,
            "date": transaction.date
        }

# Use করা:
for record in process_large_report("SB-001"):
    send_to_audit_log(record)   # একটা একটা করে — RAM safe ✅
```

---

### ⚠️ Tricky Interview Questions:

**১. Generator exhausted হয়ে যায়:**
```python
def gen():
    yield 1
    yield 2

g = gen()
list(g)   # [1, 2]
list(g)   # [] 😱 — আবার use করা যাবে না!

# নতুন করে call করতে হবে
g = gen()  # fresh generator
```

**২. Generator Expression — List Comprehension-এর মতো:**
```python
# List Comprehension — সব memory-তে
amounts = [x * 2 for x in range(1000000)]   # ❌ Heavy

# Generator Expression — lazy
amounts = (x * 2 for x in range(1000000))   # ✅ Light
#           ↑ শুধু [] এর বদলে ()
```

**৩. `return` vs `yield`:**
```python
def func():
    yield 1
    yield 2
    return   # generator শেষ — StopIteration raise করে
    yield 3  # এটা কখনো execute হবে না
```

---

### 📊 Generator vs Normal Function vs List:

| | Normal Function | List | Generator |
|---|---|---|---|
| Memory | একবারে সব | একবারে সব | একটা একটা করে |
| Speed | দ্রুত (small data) | দ্রুত (small data) | দ্রুত (large data) |
| Reusable | ✅ | ✅ | ❌ একবার শেষ |
| Infinite sequence | ❌ | ❌ | ✅ সম্ভব |

---

### 💻 Infinite Generator — Bonus:

```python
def transaction_id_generator(start=1):
    current = start
    while True:         # অসীম loop — কিন্তু memory safe!
        yield f"TXN-{current:06d}"
        current += 1

gen = transaction_id_generator()
print(next(gen))  # TXN-000001
print(next(gen))  # TXN-000002
print(next(gen))  # TXN-000003
# যতবার দরকার ততবার নতুন ID পাবে
```

---

### 🎯 Interview Closing line:

> *"Generator use করার মূল কারণ হলো memory efficiency। Banking system-এ লাখ লাখ transaction process করতে হয় — সব একসাথে load করলে server crash করবে। Generator দিয়ে একটা একটা করে process করলে same কাজ হয়, কিন্তু memory usage minimal থাকে। এটাই lazy evaluation-এর power।"*

---

পরের সম্ভাব্য প্রশ্ন:
- **OOP — Class, Inheritance, Polymorphism**
- **Exception Handling — try/except/finally**
- **Django/REST API related প্রশ্ন**

কোনটা নিয়ে আগাবে?



## Iterator vs Iterable

---

### 🔑 এক কথায়:

| | মানে | উদাহরণ |
|---|---|---|
| **Iterable** | যেটার উপর দিয়ে loop করা যায় | list, tuple, string, dict |
| **Iterator** | যেটা একটা একটা করে item **deliver** করে | `iter()`, Generator |

সহজ analogy:
```
Iterable  = বইয়ের তাক (সব বই আছে)
Iterator  = তাক থেকে একটা একটা বই তুলে দেওয়া লোক
            পরেরটা চাইলে তখন দেবে
```

---

### 🧠 দুটো Magic Method জানতে হবে:

| Method | কে implement করে | কাজ |
|---|---|---|
| `__iter__()` | Iterable | Iterator return করে |
| `__next__()` | Iterator | পরের item return করে |

> **Iterable** → `__iter__()` থাকে
> **Iterator** → `__iter__()` + `__next__()` দুটোই থাকে

---

### 💻 Code দিয়ে বোঝো:

```python
# List একটা Iterable — loop করা যায়
transactions = [100, 200, 300]

for t in transactions:       # ✅ কাজ করে
    print(t)

# কিন্তু next() সরাসরি call করা যাবে না
print(next(transactions))    # ❌ TypeError!
```

**Iterator বানাতে হবে:**
```python
transactions = [100, 200, 300]

# iter() দিয়ে Iterable → Iterator বানাও
iterator = iter(transactions)

print(next(iterator))   # 100
print(next(iterator))   # 200
print(next(iterator))   # 300
print(next(iterator))   # ❌ StopIteration — শেষ হয়ে গেছে
```

---

### 🧠 for loop আসলে পর্দার পেছনে কী করে:

```python
for t in [100, 200, 300]:
    print(t)

# Python আসলে এটাই করে:
_iter = iter([100, 200, 300])   # ১. Iterator বানায়
while True:
    try:
        t = next(_iter)          # ২. একটা একটা নেয়
        print(t)
    except StopIteration:        # ৩. শেষ হলে loop বন্ধ
        break
```

> **for loop আসলে iter() আর next() এর shortcut!**

---

### 💻 নিজে Iterator বানানো:

```python
class TransactionIterator:
    def __init__(self, transactions):
        self.transactions = transactions
        self.index = 0

    def __iter__(self):         # Iterable হওয়ার জন্য
        return self

    def __next__(self):         # Iterator হওয়ার জন্য
        if self.index >= len(self.transactions):
            raise StopIteration
        value = self.transactions[self.index]
        self.index += 1
        return value

# Use করা:
txns = TransactionIterator([500, 1000, 250])

for t in txns:
    print(f"{t} BDT")
# 500 BDT
# 1000 BDT
# 250 BDT
```

---

### ⚠️ Tricky Interview Questions:

**১. Iterator কি Iterable?**
```python
# ✅ হ্যাঁ! Iterator সবসময় Iterable
# কারণ Iterator-এ __iter__() থাকে

my_iter = iter([1, 2, 3])
for x in my_iter:    # ✅ কাজ করে — Iterator-ও Iterable
    print(x)

# কিন্তু সব Iterable Iterator না!
my_list = [1, 2, 3]
next(my_list)        # ❌ TypeError — List Iterator না
```

**২. Iterator একবার শেষ হলে:**
```python
nums = iter([1, 2, 3])

list(nums)   # [1, 2, 3]
list(nums)   # [] 😱 exhausted!

# Iterable বারবার use করা যায়
my_list = [1, 2, 3]
list(my_list)   # [1, 2, 3]
list(my_list)   # [1, 2, 3] ✅ fresh থাকে
```

**৩. String-ও Iterable:**
```python
name = "UCB"
it = iter(name)

print(next(it))  # U
print(next(it))  # C
print(next(it))  # B
```

---

### 📊 সব কিছু এক জায়গায়:

| | `__iter__` | `__next__` | `next()` চলে | বারবার loop |
|---|---|---|---|---|
| **List** | ✅ | ❌ | ❌ | ✅ |
| **String** | ✅ | ❌ | ❌ | ✅ |
| **Generator** | ✅ | ✅ | ✅ | ❌ |
| **iter(list)** | ✅ | ✅ | ✅ | ❌ |

---

### 🏦 Banking Context-এ:

```python
class AccountStatement:
    """Bank statement — Iterable"""
    def __init__(self, account_id):
        self.transactions = fetch_from_db(account_id)

    def __iter__(self):
        # প্রতিবার fresh Iterator দেয়
        return iter(self.transactions)

statement = AccountStatement("SB-001")

# বারবার loop করা যাবে ✅
for txn in statement:
    print(txn)

for txn in statement:   # আবারও কাজ করবে ✅
    generate_pdf(txn)
```

---

### 🎯 Interview Closing line:

> *"Iterable মানে loop করার capability, Iterator মানে actual delivery mechanism। Python-এর for loop এই দুটোকে একসাথে use করে। Banking system-এ large dataset handle করার সময় custom Iterator বানালে memory efficient ভাবে data process করা যায় — সব একসাথে load না করেই।"*

---

পরের সম্ভাব্য প্রশ্ন:
- **OOP — Class, Inheritance, Polymorphism**
- **Exception Handling**
- **Django REST API**

কোনটা নিয়ে আগাবে?



## GIL — Global Interpreter Lock

---

### 🔑 এক কথায়:

> GIL হলো CPython-এর একটা **lock** যেটা নিশ্চিত করে যে **একসাথে শুধুমাত্র একটাই Python thread** execute হতে পারবে — এমনকি multi-core processor থাকলেও।

সহজ analogy:
```
ধরো একটা office-এ একটাই কলম আছে
যে কলম ধরেছে সে কাজ করতে পারবে
বাকিরা অপেক্ষা করবে

সেই কলম = GIL
কর্মীরা  = Threads
```

---

### 🧠 কেন GIL বানানো হয়েছিল:

```
Python-এ memory management হয়
Reference Counting দিয়ে —

x = [1, 2, 3]   → reference count = 1
y = x            → reference count = 2
del x            → reference count = 1
del y            → reference count = 0 → memory free

সমস্যা:
দুটো thread একসাথে reference count
বাড়ালে/কমালে → data corrupt হবে 😱

Solution:
GIL — একসাথে একটাই thread চলবে
Reference count সবসময় safe থাকবে ✅
```

---

### 💻 GIL-এর প্রভাব দেখো:

```python
import threading
import time

# CPU-bound task — calculation
def count_up():
    total = 0
    for i in range(10_000_000):
        total += i
    return total

# Single thread
start = time.time()
count_up()
count_up()
print(f"Single: {time.time() - start:.2f}s")   # ~2.0s

# Two threads — faster হওয়ার কথা, কিন্তু...
start = time.time()
t1 = threading.Thread(target=count_up)
t2 = threading.Thread(target=count_up)
t1.start(); t2.start()
t1.join(); t2.join()
print(f"Multi: {time.time() - start:.2f}s")    # ~2.0s 😱

# GIL-এর কারণে দুটো thread একসাথে চলতে পারছে না!
# কোনো benefit নেই CPU-bound কাজে
```

---

### ⚠️ CPU-bound vs I/O-bound — Critical Difference:

| কাজের ধরন | GIL-এর প্রভাব | Threading কাজ করে? |
|---|---|---|
| **CPU-bound** (calculation, image processing) | ❌ Blocked | ❌ না |
| **I/O-bound** (database, API call, file read) | ✅ Release হয় | ✅ হ্যাঁ |

```python
# I/O-bound — GIL release হয়!
import requests

def fetch_data():
    # Network wait করার সময় GIL release হয়
    # অন্য thread সেই সময় কাজ করতে পারে ✅
    response = requests.get("https://api.bank.com/transactions")
    return response.json()

# Banking API call — Threading এখানে কাজ করবে ✅
```

---

### 💻 GIL থেকে বাঁচার উপায়:

**১. Multiprocessing — CPU-bound কাজে:**
```python
from multiprocessing import Process

# প্রতিটা Process-এর নিজস্ব GIL থাকে
# সত্যিকারের parallel execution সম্ভব

def calculate_interest(account_ids):
    for id in account_ids:
        # heavy calculation
        pass

# ৪টা core — ৪টা process
p1 = Process(target=calculate_interest, args=(accounts[:250],))
p2 = Process(target=calculate_interest, args=(accounts[250:500],))
p1.start(); p2.start()
p1.join(); p2.join()
# সত্যিকারের parallel ✅
```

**২. Threading — I/O-bound কাজে:**
```python
import threading

def check_transaction_status(txn_id):
    # Database/API call — I/O bound
    result = db.query(f"SELECT * FROM txn WHERE id={txn_id}")
    return result

# ১০০০টা transaction একসাথে check
threads = []
for txn_id in transaction_ids:
    t = threading.Thread(target=check_transaction_status, args=(txn_id,))
    threads.append(t)
    t.start()

# GIL release হবে I/O wait-এ — effectively parallel ✅
```

**৩. AsyncIO — Modern Solution:**
```python
import asyncio

async def fetch_balance(account_id):
    # Async I/O — GIL issue নেই
    result = await db.fetch(f"SELECT balance FROM accounts WHERE id={account_id}")
    return result

async def main():
    # হাজারটা account একসাথে check
    tasks = [fetch_balance(id) for id in account_ids]
    results = await asyncio.gather(*tasks)   # ✅ Efficient
```

---

### 📊 কোন situation-এ কী use করবে:

| Situation | Solution | কেন |
|---|---|---|
| Heavy calculation (interest) | **Multiprocessing** | GIL bypass করে |
| Database queries | **Threading / AsyncIO** | I/O-bound, GIL release হয় |
| Multiple API calls | **AsyncIO** | Most efficient |
| Simple scripts | **Single thread** | GIL issue নেই |

---

### 🏦 Banking Context-এ:

```python
# ❌ ভুল approach — CPU-bound-এ threading
def calculate_all_interests():
    threads = [threading.Thread(target=calculate, args=(acc,))
               for acc in accounts]
    # GIL-এর কারণে actually slower হবে!

# ✅ সঠিক — CPU-bound-এ multiprocessing
from multiprocessing import Pool

with Pool(4) as p:
    results = p.map(calculate_interest, accounts)

# ✅ সঠিক — I/O-bound-এ asyncio
async def process_transactions():
    async with aiohttp.ClientSession() as session:
        tasks = [verify_transaction(session, txn)
                 for txn in transactions]
        return await asyncio.gather(*tasks)
```

---

### 🎯 Interview Closing line:

> *"GIL CPython-এর একটা necessary limitation — memory safety-র জন্য দরকার। Banking system-এ CPU-heavy কাজ যেমন interest calculation-এ multiprocessing use করবো, আর database query বা API call-এর মতো I/O-bound কাজে asyncio use করবো। GIL জেনে সঠিক tool choose করাটাই আসল skill।"*

---

পরের সম্ভাব্য প্রশ্ন:
- **OOP — Class, Inheritance, Polymorphism**
- **Exception Handling**
- **Django REST API, JWT Authentication**

কোনটা নিয়ে আগাবে?



## Multithreading vs Multiprocessing

---

### 🔑 এক কথায়:

| | মানে | Memory | GIL |
|---|---|---|---|
| **Multithreading** | একটা process-এর ভেতরে **multiple threads** | Shared | ❌ আটকায় |
| **Multiprocessing** | **Multiple আলাদা processes** | আলাদা আলাদা | ✅ প্রতিটার নিজস্ব |

সহজ analogy:
```
Multithreading  = একটা রেস্তোরাঁয় অনেক waiter
                  সবাই একই kitchen share করে
                  একসময় একজনই kitchen use করতে পারে (GIL)

Multiprocessing = অনেকগুলো আলাদা রেস্তোরাঁ
                  প্রতিটার নিজস্ব kitchen আছে
                  সবাই সত্যিকারের parallel কাজ করতে পারে
```

---

### 🧠 Memory Model — গুরুত্বপূর্ণ পার্থক্য:

```
Multithreading:
┌─────────────────────────┐
│        Process          │
│  ┌──────┐  ┌──────┐    │
│  │Thread│  │Thread│    │
│  │  1   │  │  2   │    │
│  └──────┘  └──────┘    │
│     ↕ Shared Memory ↕  │
│  [balance, transactions]│
└─────────────────────────┘

Multiprocessing:
┌───────────┐  ┌───────────┐
│ Process 1 │  │ Process 2 │
│  [data1]  │  │  [data2]  │
│  Own GIL  │  │  Own GIL  │
└───────────┘  └───────────┘
  আলাদা memory   আলাদা memory
```

---

### 💻 Code Comparison:

**Multithreading:**
```python
import threading
import time

def fetch_transactions(account_id):
    # I/O bound — database call
    time.sleep(1)  # simulate DB query
    print(f"Account {account_id} fetched")

start = time.time()

threads = []
for acc_id in ["SB-001", "SB-002", "SB-003"]:
    t = threading.Thread(target=fetch_transactions, args=(acc_id,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Time: {time.time() - start:.2f}s")  # ~1s ✅ (not 3s)
# I/O-bound — threading কাজ করে
```

**Multiprocessing:**
```python
from multiprocessing import Pool
import time

def calculate_interest(account):
    # CPU bound — heavy calculation
    total = sum(i * account["balance"] for i in range(1_000_000))
    return total

accounts = [
    {"id": "SB-001", "balance": 50000},
    {"id": "SB-002", "balance": 75000},
    {"id": "SB-003", "balance": 30000},
]

start = time.time()

with Pool(3) as pool:
    results = pool.map(calculate_interest, accounts)

print(f"Time: {time.time() - start:.2f}s")  # Faster ✅
# CPU-bound — multiprocessing কাজ করে
```

---

### ⚠️ Shared Memory সমস্যা — Race Condition:

```python
import threading

balance = 10000  # shared variable

def withdraw(amount):
    global balance
    if balance >= amount:
        # ⚠️ এখানে দুটো thread একসাথে ঢুকলে সমস্যা!
        balance -= amount
        print(f"{amount} withdrawn. Balance: {balance}")

# দুটো thread একসাথে withdraw করলে:
t1 = threading.Thread(target=withdraw, args=(8000,))
t2 = threading.Thread(target=withdraw, args=(8000,))
t1.start()
t2.start()
t1.join(); t2.join()

# Balance negative হয়ে যেতে পারে 😱
```

**Fix — Lock দিয়ে:**
```python
import threading

balance = 10000
lock = threading.Lock()

def withdraw(amount):
    global balance
    with lock:   # একসময় একটাই thread ঢুকতে পারবে
        if balance >= amount:
            balance -= amount
            print(f"{amount} withdrawn. Balance: {balance}")
        else:
            print("Insufficient balance")

t1 = threading.Thread(target=withdraw, args=(8000,))
t2 = threading.Thread(target=withdraw, args=(8000,))
t1.start(); t2.start()
t1.join(); t2.join()
# ✅ Safe — race condition নেই
```

---

### 💻 Multiprocessing-এ Data Share করা:

```python
from multiprocessing import Pool, Manager

def process_account(args):
    account_id, shared_results = args
    result = calculate_interest(account_id)
    shared_results[account_id] = result

with Manager() as manager:
    results = manager.dict()   # shared dict across processes

    with Pool(4) as pool:
        pool.map(process_account,
                [(acc, results) for acc in account_ids])

    print(dict(results))
```

> Multiprocessing-এ সরাসরি memory share হয় না — **Manager** বা **Queue** দিয়ে communicate করতে হয়।

---

### 📊 কোনটা কখন use করবে:

| Task | Threading | Multiprocessing | AsyncIO |
|---|---|---|---|
| Database queries | ✅ Best | ❌ Overkill | ✅ Better |
| API calls | ✅ Good | ❌ Overkill | ✅ Best |
| Interest calculation | ❌ GIL blocks | ✅ Best | ❌ না |
| File read/write | ✅ Good | ❌ Overkill | ✅ Good |
| Image/PDF processing | ❌ | ✅ Best | ❌ |
| 1000+ concurrent users | ❌ Heavy | ❌ Heavy | ✅ Best |

---

### 🏦 Banking System-এ Real Use Case:

```python
# ১. Monthly interest calculation — CPU bound
#    → Multiprocessing
from multiprocessing import Pool

def calculate_monthly_interest(account):
    principal = account["balance"]
    rate = account["rate"]
    return principal * rate / 12

with Pool(8) as pool:   # 8 core use করো
    interests = pool.map(calculate_monthly_interest, all_accounts)

# ২. Transaction verification — I/O bound
#    → AsyncIO
import asyncio
import aiohttp

async def verify_transaction(session, txn_id):
    async with session.get(f"/api/verify/{txn_id}") as resp:
        return await resp.json()

async def verify_all():
    async with aiohttp.ClientSession() as session:
        tasks = [verify_transaction(session, id)
                 for id in transaction_ids]
        return await asyncio.gather(*tasks)   # হাজারটা একসাথে ✅

# ৩. Real-time balance update — Thread + Lock
#    → Threading with Lock
lock = threading.Lock()

def update_balance(account_id, amount):
    with lock:
        account = db.get(account_id)
        account.balance += amount
        db.save(account)   # safe ✅
```

---

### 📊 Overhead Comparison:

| | Threading | Multiprocessing |
|---|---|---|
| Start করতে সময় | কম (fast) | বেশি (slow) |
| Memory use | কম (shared) | বেশি (separate) |
| Communication | সহজ (shared memory) | কঠিন (IPC দরকার) |
| Crash isolation | ❌ একটা crash করলে সব | ✅ আলাদা থাকে |
| True parallel | ❌ GIL আটকায় | ✅ হ্যাঁ |

---

### 🎯 Interview Closing line:

> *"Choice টা নির্ভর করে কাজের ধরনের উপর। Banking system-এ interest calculation বা statement generation-এর মতো CPU-heavy কাজে multiprocessing, database query বা payment gateway call-এর মতো I/O-bound কাজে asyncio, আর real-time balance update-এ threading with lock use করবো। Wrong choice করলে হয় performance কমবে, না হয় race condition থেকে data corrupt হবে।"*

---

পরের সম্ভাব্য প্রশ্ন:
- **OOP — Class, Inheritance, Polymorphism**
- **Exception Handling — try/except/finally**
- **Django REST API, JWT Authentication**
- **Database — ORM, Query Optimization**

কোনটা নিয়ে আগাবে?



## Async vs Sync Execution

---

### 🔑 এক কথায়:

| | মানে | কাজের ধরন |
|---|---|---|
| **Sync** | একটা শেষ হলে পরেরটা শুরু | Sequential — একটার পর একটা |
| **Async** | একটা wait করার সময় অন্যটা শুরু | Concurrent — একসাথে অনেকটা |

সহজ analogy:
```
Sync  = একজন cashier
        একজনের কাজ শেষ হলে পরের জন
        বাকিরা queue-এ দাঁড়িয়ে 😫

Async = একজন cashier
        একজনের cheque verify হওয়ার সময়
        পরের জনের কাজ শুরু করে দেয় ✅
        wait-এর সময় নষ্ট হয় না
```

---

### 💻 Sync — সমস্যাটা দেখো:

```python
import time

def fetch_account(account_id):
    time.sleep(2)   # DB query — 2 সেকেন্ড লাগে
    return {"id": account_id, "balance": 50000}

def main():
    start = time.time()

    acc1 = fetch_account("SB-001")   # 2s অপেক্ষা
    acc2 = fetch_account("SB-002")   # আরো 2s অপেক্ষা
    acc3 = fetch_account("SB-003")   # আরো 2s অপেক্ষা

    print(f"Total time: {time.time() - start:.1f}s")
    # Total time: 6.0s 😫

main()
```

> ৩টা account fetch করতে **6 সেকেন্ড** — কারণ একটা শেষ না হলে পরেরটা শুরুই হয় না।

---

### 💻 Async — সমাধান:

```python
import asyncio

async def fetch_account(account_id):
    await asyncio.sleep(2)   # DB query simulate
    return {"id": account_id, "balance": 50000}

async def main():
    start = asyncio.get_event_loop().time()

    # তিনটা একসাথে শুরু হয়
    acc1, acc2, acc3 = await asyncio.gather(
        fetch_account("SB-001"),
        fetch_account("SB-002"),
        fetch_account("SB-003"),
    )

    print(f"Total time: {asyncio.get_event_loop().time() - start:.1f}s")
    # Total time: 2.0s ✅

asyncio.run(main())
```

> একই কাজ **2 সেকেন্ডে** — ৩টা একসাথে wait করছে।

---

### 🧠 পর্দার পেছনে কী হয় — Event Loop:

```
Event Loop সবকিছু control করে

async main() শুরু
    ↓
fetch_account("SB-001") শুরু → await হলো ⏸️
    ↓ (wait না করে পরেরটা)
fetch_account("SB-002") শুরু → await হলো ⏸️
    ↓
fetch_account("SB-003") শুরু → await হলো ⏸️
    ↓
2 সেকেন্ড পরে তিনটাই একসাথে resume ▶️
    ↓
সব result collect করে return
```

> **Event Loop** একটাই thread-এ সব manage করে — GIL কোনো সমস্যা না।

---

### 🔑 `async` / `await` — এর মানে:

```python
# async — এই function-টা pauseable
async def fetch_data():
    ...

# await — এখানে pause করো, result আসলে resume করো
result = await fetch_data()

# await ছাড়া call করলে coroutine object পাবে, execute হবে না!
result = fetch_data()   # ❌ coroutine object — execute হয়নি!
```

---

### ⚠️ Tricky Interview Questions:

**১. Async মানে কি Parallel?**
```python
# ❌ না — Async concurrent, parallel না
# একটাই thread — একসাথে একটাই চলে
# কিন্তু wait-এর সময় switch করে

# Parallel = সত্যিকারের একসাথে (multiprocessing)
# Concurrent = চালাকি করে একসাথের মতো দেখায় (async)
```

**২. Sync function-কে async-এ call করলে:**
```python
import asyncio

def slow_sync():
    time.sleep(3)   # Blocking! Event loop আটকে যাবে
    return "done"

async def main():
    # ❌ এভাবে call করলে পুরো event loop block হবে
    result = slow_sync()

    # ✅ সঠিক উপায় — thread pool-এ দাও
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, slow_sync)
```

**৩. `asyncio.gather` vs `asyncio.wait`:**
```python
# gather — সব শেষ হলে একসাথে result দেয়
results = await asyncio.gather(task1(), task2(), task3())

# wait — যেটা আগে শেষ হয় সেটা আগে নাও
done, pending = await asyncio.wait(
    [task1(), task2(), task3()],
    return_when=asyncio.FIRST_COMPLETED
)
```

---

### 🏦 Banking System-এ Real Use Case:

**Payment Processing:**
```python
import asyncio
import aiohttp

async def verify_account(session, account_id):
    async with session.get(f"/api/accounts/{account_id}") as resp:
        return await resp.json()

async def check_fraud(session, txn_id):
    async with session.get(f"/api/fraud-check/{txn_id}") as resp:
        return await resp.json()

async def get_exchange_rate(session, currency):
    async with session.get(f"/api/rates/{currency}") as resp:
        return await resp.json()

async def process_payment(txn_id, account_id, currency):
    async with aiohttp.ClientSession() as session:

        # তিনটা API call একসাথে — কেউ কাউকে wait করছে না
        account, fraud_check, rate = await asyncio.gather(
            verify_account(session, account_id),
            check_fraud(session, txn_id),
            get_exchange_rate(session, currency)
        )

        if account["valid"] and not fraud_check["suspicious"]:
            amount = txn["amount"] * rate["value"]
            return {"status": "approved", "amount": amount}
        return {"status": "rejected"}

# Sync হলে: 3 × 500ms = 1500ms
# Async হলে: max(500ms) = 500ms ✅
```

---

### 📊 Sync vs Async vs Threading vs Multiprocessing:

| | Sync | Async | Threading | Multiprocessing |
|---|---|---|---|---|
| **কাজের ধরন** | যেকোনো | I/O-bound | I/O-bound | CPU-bound |
| **Thread** | ১টা | ১টা | অনেক | অনেক process |
| **GIL** | আটকায় | আটকায় না | আটকায় | নেই |
| **Memory** | কম | কম | মাঝারি | বেশি |
| **Complexity** | সহজ | মাঝারি | কঠিন | কঠিন |
| **Best for** | Simple logic | API/DB calls | File/Network | Calculation |

---

### 🏦 Django-তে Async View:

```python
# Django 3.1+ async view support
from django.http import JsonResponse
import asyncio
import aiohttp

async def get_account_summary(request, account_id):
    async with aiohttp.ClientSession() as session:

        # একসাথে সব data fetch করো
        balance, transactions, loans = await asyncio.gather(
            fetch_balance(session, account_id),
            fetch_transactions(session, account_id),
            fetch_loans(session, account_id)
        )

    return JsonResponse({
        "balance": balance,
        "transactions": transactions,
        "loans": loans
    })
    # Sync হলে 3x slow হতো ❌
```

---

### 🎯 Interview Closing line:

> *"Sync execution simple কিন্তু I/O-heavy system-এ bottleneck তৈরি করে। Banking system-এ একটা payment process করতে account verification, fraud check, exchange rate — একসাথে অনেক API call দরকার। Async দিয়ে এগুলো concurrently চালালে response time কয়েকগুণ কমে যায়। Django আর FastAPI দুটোতেই async support আছে, আর FastAPI originally async-first।"*

---

পরের সম্ভাব্য প্রশ্ন:
- **OOP — Class, Inheritance, Polymorphism**
- **Exception Handling — try/except/finally**
- **Django REST API, JWT Authentication**
- **Database Query Optimization**

কোনটা নিয়ে আগাবে?





## `asyncio` কী?

---

### 🔑 এক কথায়:

> `asyncio` হলো Python-এর built-in library যেটা **Event Loop** চালায় — async/await দিয়ে লেখা coroutine গুলোকে **একটাই thread-এ** efficiently manage করে।

সহজ analogy:
```
asyncio = একজন super-efficient manager

সে একসাথে ১০০ জনের কাজ track করে
কেউ wait করছে → অন্যজনকে কাজ দেয়
কেউ ready → সাথে সাথে resume করায়

কখনো বসে থাকে না — সবসময় কাউকে না কাউকে কাজ দেয়
```

---

### 🧠 asyncio-র ৪টা মূল Building Block:

```
┌─────────────────────────────────┐
│           asyncio               │
│                                 │
│  1. Event Loop  ← সব কিছুর boss│
│  2. Coroutine   ← async def     │
│  3. Task        ← scheduled job │
│  4. Future      ← pending result│
└─────────────────────────────────┘
```

---

### 💻 ১. Coroutine — async function:

```python
import asyncio

# async def দিয়ে coroutine বানাও
async def fetch_balance(account_id):
    await asyncio.sleep(1)   # I/O simulate
    return 50000

# সরাসরি call করলে execute হয় না!
result = fetch_balance("SB-001")
print(result)   # <coroutine object> 😱

# asyncio.run() দিয়ে চালাতে হবে
result = asyncio.run(fetch_balance("SB-001"))
print(result)   # 50000 ✅
```

---

### 💻 ২. Event Loop — সব কিছুর boss:

```python
import asyncio

async def task_one():
    print("Task 1: শুরু")
    await asyncio.sleep(2)    # 2s wait — pause ⏸️
    print("Task 1: শেষ")

async def task_two():
    print("Task 2: শুরু")
    await asyncio.sleep(1)    # 1s wait — pause ⏸️
    print("Task 2: শেষ")

async def main():
    await asyncio.gather(task_one(), task_two())

asyncio.run(main())

# Output:
# Task 1: শুরু
# Task 2: শুরু      ← Task 1 wait-এ থাকায় Task 2 শুরু হলো
# Task 2: শেষ      ← 1s পরে
# Task 1: শেষ      ← 2s পরে
```

**Event Loop timeline:**
```
0s   → Task1 শুরু → await → pause ⏸️
       Task2 শুরু → await → pause ⏸️
1s   → Task2 resume → শেষ ✅
2s   → Task1 resume → শেষ ✅

Total: 2s (Sync হলে 3s লাগতো)
```

---

### 💻 ৩. Task — scheduled coroutine:

```python
import asyncio

async def verify_transaction(txn_id):
    await asyncio.sleep(1)
    print(f"TXN {txn_id} verified")
    return True

async def main():
    # create_task — immediately schedule করে
    task1 = asyncio.create_task(verify_transaction("T001"))
    task2 = asyncio.create_task(verify_transaction("T002"))
    task3 = asyncio.create_task(verify_transaction("T003"))

    # সব শেষ হওয়ার জন্য wait করো
    results = await asyncio.gather(task1, task2, task3)
    print(results)   # [True, True, True]

asyncio.run(main())
# সবগুলো ~1s-এ শেষ ✅
```

**`await coroutine` vs `create_task` পার্থক্য:**
```python
async def main():
    # ❌ Sequential — একটার পর একটা
    await verify_transaction("T001")   # 1s
    await verify_transaction("T002")   # আরো 1s
    # Total: 2s

    # ✅ Concurrent — একসাথে
    t1 = asyncio.create_task(verify_transaction("T001"))
    t2 = asyncio.create_task(verify_transaction("T002"))
    await t1
    await t2
    # Total: 1s
```

---

### 💻 ৪. gather vs wait vs shield:

```python
import asyncio

# gather — সব শেষ হলে একসাথে result
results = await asyncio.gather(
    fetch_balance("SB-001"),
    fetch_balance("SB-002"),
    fetch_balance("SB-003")
)
# [50000, 75000, 30000]

# gather — error handle করা
results = await asyncio.gather(
    fetch_balance("SB-001"),
    fetch_balance("INVALID"),   # এটা fail করবে
    return_exceptions=True       # crash না করে exception return করবে
)
# [50000, Exception(...), ...]  ✅

# wait — প্রথমটা শেষ হলেই নাও
done, pending = await asyncio.wait(
    [task1, task2, task3],
    return_when=asyncio.FIRST_COMPLETED
)

# shield — cancel হলেও এই task চলবে
result = await asyncio.shield(critical_task())
```

---

### 🏦 Banking-এ Real Example:

**Payment Processor:**
```python
import asyncio
import aiohttp   # async HTTP client

async def verify_sender(session, account_id):
    async with session.get(f"/api/accounts/{account_id}") as r:
        return await r.json()

async def fraud_check(session, amount, account_id):
    async with session.post("/api/fraud", json={
        "amount": amount,
        "account": account_id
    }) as r:
        return await r.json()

async def get_rate(session, currency):
    async with session.get(f"/api/rates/{currency}") as r:
        return await r.json()

async def process_payment(account_id, amount, currency="USD"):
    async with aiohttp.ClientSession() as session:

        # তিনটা API call একসাথে চলবে ✅
        sender, fraud, rate = await asyncio.gather(
            verify_sender(session, account_id),
            fraud_check(session, amount, account_id),
            get_rate(session, currency)
        )

        # Validate
        if not sender["active"]:
            return {"status": "rejected", "reason": "Account inactive"}

        if fraud["risk_score"] > 0.8:
            return {"status": "rejected", "reason": "Fraud suspected"}

        final_amount = amount * rate["value"]
        return {
            "status": "approved",
            "amount": final_amount,
            "currency": currency
        }

# Sync হলে: 3 × 300ms = 900ms
# Async হলে: max(300ms) = 300ms ✅
```

**Bulk Transaction Processing:**
```python
async def process_bulk_transactions(transactions):
    # সব transaction একসাথে process করো
    tasks = [
        asyncio.create_task(process_payment(
            txn["account"],
            txn["amount"]
        ))
        for txn in transactions
    ]

    # সব শেষ হওয়ার জন্য wait — error গুলো collect করো
    results = await asyncio.gather(*tasks, return_exceptions=True)

    success = [r for r in results if not isinstance(r, Exception)]
    failed = [r for r in results if isinstance(r, Exception)]

    print(f"✅ Success: {len(success)}")
    print(f"❌ Failed: {len(failed)}")
    return results
```

---

### ⚠️ Common Mistakes:

```python
# ❌ Mistake 1: Blocking call async-এ
async def bad():
    import time
    time.sleep(3)        # পুরো event loop block! 😱
    # ✅ Use করো: await asyncio.sleep(3)

# ❌ Mistake 2: asyncio.run() এর ভেতরে আবার run()
async def main():
    asyncio.run(other())   # ❌ nested run — error!
    # ✅ Use করো: await other()

# ❌ Mistake 3: coroutine await না করা
async def main():
    fetch_balance("SB-001")        # ❌ execute হয়নি!
    await fetch_balance("SB-001")  # ✅
```

---

### 📊 asyncio কোথায় কাজ করে, কোথায় না:

| কাজ | asyncio কাজ করে? | কারণ |
|---|---|---|
| Database query | ✅ | I/O bound |
| HTTP API call | ✅ | I/O bound |
| File read/write | ✅ | I/O bound |
| Interest calculation | ❌ | CPU bound |
| Image processing | ❌ | CPU bound |
| WebSocket | ✅ | I/O bound |

---

### 💻 FastAPI-তে asyncio — Real World:

```python
from fastapi import FastAPI
import asyncio
import aiohttp

app = FastAPI()

@app.get("/account/{account_id}/summary")
async def account_summary(account_id: str):
    # Multiple DB calls একসাথে
    balance, txns, loans = await asyncio.gather(
        get_balance(account_id),
        get_transactions(account_id),
        get_loans(account_id)
    )
    return {
        "balance": balance,
        "recent_transactions": txns,
        "active_loans": loans
    }
# Response time: max(individual) — not sum ✅
```

---

### 🎯 Interview Closing line:

> *"asyncio হলো Python-এর async programming-এর core engine। Banking system-এ একটা request handle করতে account verification, fraud check, notification — সব একসাথে দরকার। asyncio দিয়ে এগুলো concurrently চালালে response time কয়েকগুণ কমে। FastAPI asyncio-র উপরে built — তাই high-traffic banking API-তে FastAPI আর asyncio combination অনেক powerful।"*

---

এখন পর্যন্ত Python core অনেকটা cover হয়েছে। পরের important topics:

- **OOP — Class, Inheritance, Polymorphism**
- **Exception Handling**
- **Django/FastAPI REST API**
- **JWT Authentication**
- **Database — ORM, Query Optimization**

কোনটা নিয়ে আগাবে?



## Event Loop কীভাবে কাজ করে

---

### 🔑 এক কথায়:

> Event Loop হলো asyncio-র **heart** — এটা একটা infinite loop যেটা সবসময় দেখছে **"কোন task ready? কোনটা waiting?"** — ready হলে run করায়, waiting হলে skip করে পরেরটা দেখে।

সহজ analogy:
```
Event Loop = Airport control tower

অনেক plane (tasks) আছে
কেউ runway-তে আসতে ready ✅
কেউ fuel নিচ্ছে — wait ⏸️
কেউ clearance পাচ্ছে — wait ⏸️

Control tower সবসময় check করে —
"কে ready? তাকে land করাও।"
কেউ idle থাকে না।
```

---

### 🧠 Event Loop-এর ভেতরের Structure:

```
┌─────────────────────────────────────────┐
│              EVENT LOOP                 │
│                                         │
│  ┌─────────────┐   ┌─────────────────┐  │
│  │  Ready Queue│   │  Waiting Pool   │  │
│  │             │   │                 │  │
│  │  Task A ✅  │   │  Task B ⏸️ I/O  │  │
│  │  Task C ✅  │   │  Task D ⏸️ I/O  │  │
│  │             │   │  Task E ⏸️ I/O  │  │
│  └─────────────┘   └─────────────────┘  │
│         ↓                  ↓            │
│    Execute করো      I/O শেষ হলে        │
│                     Ready Queue-এ দাও  │
└─────────────────────────────────────────┘
```

---

### 💻 Step by Step — কী হয়:

```python
import asyncio

async def fetch_account(name, delay):
    print(f"{name}: শুরু হলো")
    await asyncio.sleep(delay)    # ← এখানে pause, control ছেড়ে দেয়
    print(f"{name}: শেষ হলো")
    return f"{name} done"

async def main():
    await asyncio.gather(
        fetch_account("SB-001", 3),
        fetch_account("SB-002", 1),
        fetch_account("SB-003", 2),
    )

asyncio.run(main())
```

**Event Loop Timeline:**
```
Time 0s:
  → SB-001 শুরু → await sleep(3) → Waiting Pool-এ ⏸️
  → SB-002 শুরু → await sleep(1) → Waiting Pool-এ ⏸️
  → SB-003 শুরু → await sleep(2) → Waiting Pool-এ ⏸️

Time 1s:
  → SB-002 ready! → Ready Queue-এ ✅
  → SB-002 execute → "SB-002: শেষ হলো" print

Time 2s:
  → SB-003 ready! → Ready Queue-এ ✅
  → SB-003 execute → "SB-003: শেষ হলো" print

Time 3s:
  → SB-001 ready! → Ready Queue-এ ✅
  → SB-001 execute → "SB-001: শেষ হলো" print

Total: 3s (Sync হলে: 3+1+2 = 6s)
```

---

### 🔄 Event Loop-এর Infinite Cycle:

```python
# Event Loop আসলে এটাই করে (simplified):

while True:
    # ১. Ready queue-এ কি কেউ আছে?
    if ready_queue:
        task = ready_queue.pop()
        task.run_until_next_await()   # পরের await পর্যন্ত চালাও

    # ২. Waiting pool check করো
    # কোনো I/O complete হয়েছে?
    completed = check_io_completion()
    for task in completed:
        ready_queue.append(task)      # Ready queue-এ দাও

    # ৩. কিছু না থাকলে
    if not ready_queue and not waiting_pool:
        break                         # সব শেষ — loop বন্ধ
```

---

### 🧠 await হলে ঠিক কী হয়:

```python
async def fetch_balance(account_id):
    print("Step 1: DB query পাঠালাম")

    result = await db.query(account_id)
    # ↑ এখানে কী হয়:
    # ১. DB-তে query পাঠানো হলো
    # ২. "আমি wait করছি" — Event Loop-কে জানালো
    # ৩. Control ছেড়ে দিলো ← এটাই key!
    # ৪. Event Loop অন্য task চালালো
    # ৫. DB response আসলে Event Loop resume করালো

    print("Step 2: Result পেলাম")
    return result
```

```
fetch_balance() চলছে
       ↓
"Step 1" print হলো
       ↓
await db.query() → PAUSE ⏸️
       ↓
Event Loop → অন্য task চালাও
       ↓        ↓
   Task B    Task C
   চলছে      চলছে
       ↓
DB response এলো → fetch_balance() RESUME ▶️
       ↓
"Step 2" print হলো
```

---

### ⚠️ Event Loop Block হলে কী হয়:

```python
import asyncio
import time

async def bad_task():
    print("Bad task শুরু")
    time.sleep(3)          # ❌ Blocking call!
    # Event Loop পুরো আটকে গেছে
    # অন্য কোনো task চলতে পারছে না 😱
    print("Bad task শেষ")

async def good_task():
    print("Good task শুরু")
    await asyncio.sleep(3)  # ✅ Non-blocking
    # Event Loop free — অন্যরা চলতে পারে
    print("Good task শেষ")

async def main():
    await asyncio.gather(bad_task(), other_task())
    # bad_task চলার সময় other_task আটকে থাকবে 😱
```

**Rule:**
```
Event Loop-এ কখনো blocking call দেবে না:
❌ time.sleep()      → ✅ await asyncio.sleep()
❌ requests.get()    → ✅ await aiohttp.get()
❌ file.read()       → ✅ await aiofiles.read()
❌ db.execute()      → ✅ await async_db.execute()
```

---

### 💻 Event Loop Manually Control করা:

```python
import asyncio

async def process_payment(txn_id):
    await asyncio.sleep(1)
    return f"TXN-{txn_id} processed"

# Method 1 — asyncio.run() (Recommended, Python 3.7+)
result = asyncio.run(process_payment("001"))

# Method 2 — Manual (পুরোনো code-এ দেখবে)
loop = asyncio.get_event_loop()
result = loop.run_until_complete(process_payment("001"))
loop.close()

# Method 3 — Already running loop-এ task add করা
async def main():
    loop = asyncio.get_running_loop()

    # Background-এ task চালাও — await না করে
    task = loop.create_task(process_payment("002"))

    # অন্য কাজ করো...
    await asyncio.sleep(0)   # একবার control ছাড়ো

    result = await task
```

---

### 💻 Real Banking Example — Event Loop-এর power:

```python
import asyncio
import aiohttp

async def single_payment_check(session, txn_id):
    """একটা transaction verify করো"""
    async with session.get(f"/api/verify/{txn_id}") as resp:
        return await resp.json()

async def process_all_transactions(txn_ids):
    """হাজারটা transaction একসাথে verify"""

    async with aiohttp.ClientSession() as session:
        # ১০০০টা task তৈরি করো
        tasks = [
            asyncio.create_task(
                single_payment_check(session, txn_id)
            )
            for txn_id in txn_ids
        ]

        # Event Loop সব manage করবে —
        # কেউ wait করলে অন্যজন চলবে
        results = await asyncio.gather(*tasks, return_exceptions=True)

    success = sum(1 for r in results if not isinstance(r, Exception))
    print(f"✅ {success}/{len(txn_ids)} verified")
    return results

# ১০০০টা API call:
# Sync হলে:  1000 × 300ms = 300,000ms = 5 minutes 😫
# Async হলে: ~300ms (সব একসাথে) ✅
asyncio.run(process_all_transactions(range(1000)))
```

---

### 📊 Event Loop — States of a Task:

```
Task তৈরি হলো
      ↓
  PENDING ⏳
      ↓
 RUNNING ▶️  ← Event Loop চালাচ্ছে
      ↓
  await হলো?
  ↙         ↘
হ্যাঁ         না
  ↓            ↓
WAITING ⏸️   DONE ✅
  ↓
I/O শেষ
  ↓
RUNNING ▶️ (resume)
```

---

### 🎯 Interview Closing line:

> *"Event Loop হলো single-threaded concurrency-র secret weapon। এটা একটাই thread-এ হাজারটা I/O operation manage করে — কেউ wait করলে সাথে সাথে অন্যজনকে চালায়। Banking system-এ একটা payment process করতে যত external call দরকার — account check, fraud detection, notification — সব Event Loop concurrently handle করে। Blocking call না করাটাই Event Loop-এর সবচেয়ে important rule।"*

---

Python async পুরো series এখন প্রায় complete। পরের important topics:

- **OOP — Class, Inheritance, Polymorphism**
- **Exception Handling — try/except/finally**
- **Django REST API + JWT**
- **Database ORM + Query Optimization**

কোনটা নিয়ে আগাবে?




## Context Manager কী?

---

### 🔑 এক কথায়:

> Context Manager হলো এমন একটা mechanism যেটা **কোনো resource automatically setup আর cleanup** করে — তুমি ভুলে গেলেও সে নিজেই বন্ধ করে দেয়।

সহজ analogy:
```
Context Manager = Hotel room

Check-in করো  → room ready হয়  (setup)
কাজ করো       → room use করো
Check-out করো → room clean হয়  (cleanup)

তুমি চলে গেলেও hotel নিজেই
light বন্ধ করে, দরজা lock করে ✅
```

---

### 💻 ছাড়া vs সহ — পার্থক্য:

**Context Manager ছাড়া — সমস্যা:**
```python
# ❌ Dangerous
file = open("transactions.txt", "r")
data = file.read()
# এখানে error হলে file কখনো close হবে না! 😱
file.close()   # এই line-এ পৌঁছাবেই না
```

**Context Manager দিয়ে — Safe:**
```python
# ✅ Safe
with open("transactions.txt", "r") as file:
    data = file.read()
    # error হলেও file automatically close হবে ✅
# এখানে এসে file already closed
```

> `with` block শেষ হলে — **error হোক বা না হোক** — cleanup automatically হয়।

---

### 🧠 পর্দার পেছনে কী হয়:

```python
with open("file.txt") as f:
    data = f.read()

# Python আসলে এটাই করে:
f = open("file.txt")
f.__enter__()        # setup — file open
try:
    data = f.read()
finally:
    f.__exit__()     # cleanup — file close (সবসময়)
```

**দুটো Magic Method:**
```
__enter__() → with block শুরুতে call হয় → resource দেয়
__exit__()  → with block শেষে call হয়  → cleanup করে
```

---

### 💻 নিজে Context Manager বানানো — Class দিয়ে:

```python
class DatabaseConnection:

    def __init__(self, db_url):
        self.db_url = db_url
        self.connection = None

    def __enter__(self):
        print(f"✅ DB Connected: {self.db_url}")
        self.connection = create_connection(self.db_url)
        return self.connection        # as clause-এ এটা পাবে

    def __exit__(self, exc_type, exc_value, traceback):
        print("🔒 DB Connection closed")
        self.connection.close()

        if exc_type:
            print(f"❌ Error হয়েছিল: {exc_value}")
            return False   # Exception re-raise করবে
        return True

# Use করা:
with DatabaseConnection("postgresql://ucb_db") as conn:
    conn.execute("SELECT * FROM transactions")
    # error হলেও connection close হবে ✅

# ✅ DB Connected: postgresql://ucb_db
# 🔒 DB Connection closed
```

---

### 💻 নিজে Context Manager বানানো — `contextlib` দিয়ে (সহজ):

```python
from contextlib import contextmanager

@contextmanager
def db_transaction(conn):
    print("Transaction শুরু")
    try:
        yield conn          # ← এখানে with block চলে
        conn.commit()
        print("✅ Commit হলো")
    except Exception as e:
        conn.rollback()
        print(f"❌ Rollback হলো: {e}")
        raise
    finally:
        print("Transaction শেষ")

# Use করা:
with db_transaction(connection) as conn:
    conn.execute("INSERT INTO transactions VALUES (...)")
    conn.execute("UPDATE accounts SET balance = balance - 500")
    # error হলে → rollback ✅
    # success হলে → commit ✅
```

**`yield` এর আগে = `__enter__`**
**`yield` এর পরে = `__exit__`**

---

### 🏦 Banking-এ Real Use Cases:

**১. Transaction Management:**
```python
from contextlib import contextmanager

@contextmanager
def atomic_transaction(db):
    """সব হবে, নইলে কিছুই হবে না"""
    transaction = db.begin()
    try:
        yield transaction
        transaction.commit()     # সব ঠিক → save
    except Exception:
        transaction.rollback()   # যেকোনো error → সব undo
        raise
    finally:
        transaction.close()

# Use:
with atomic_transaction(db) as txn:
    txn.debit("SB-001", 5000)    # account থেকে কাটো
    txn.credit("SB-002", 5000)   # অন্য account-এ দাও
    # debit হয়ে credit না হলে → rollback ✅
    # দুটোই হবে অথবা কোনোটাই না
```

**২. File Report Generation:**
```python
@contextmanager
def generate_report(filename):
    print(f"📄 {filename} তৈরি হচ্ছে")
    file = open(filename, "w")
    try:
        yield file
    except Exception as e:
        print(f"❌ Report failed: {e}")
        raise
    finally:
        file.close()
        print(f"✅ {filename} সংরক্ষণ হয়েছে")

with generate_report("monthly_statement.txt") as report:
    report.write("Account: SB-001\n")
    report.write("Balance: 50,000 BDT\n")
```

**৩. API Rate Limiting:**
```python
@contextmanager
def rate_limited_session(max_calls=100):
    session = create_session()
    call_count = 0

    class LimitedSession:
        def get(self, url):
            nonlocal call_count
            if call_count >= max_calls:
                raise Exception("Rate limit exceeded!")
            call_count += 1
            return session.get(url)

    try:
        yield LimitedSession()
    finally:
        session.close()
        print(f"Total API calls: {call_count}")

with rate_limited_session(max_calls=50) as session:
    for account in accounts:
        session.get(f"/api/balance/{account}")
```

---

### 💻 Multiple Context Managers একসাথে:

```python
# ✅ একসাথে অনেক resource manage করো
with open("input.txt") as infile, \
     open("output.txt", "w") as outfile, \
     db_transaction(conn) as txn:

    data = infile.read()
    processed = process(data)
    outfile.write(processed)
    txn.execute("UPDATE log SET status='done'")

# তিনটাই automatically close/commit হবে ✅
```

---

### ⚠️ Tricky Interview Questions:

**১. `__exit__` এর parameters:**
```python
def __exit__(self, exc_type, exc_value, traceback):
    #              ↑            ↑           ↑
    #         Exception    Exception    Stack trace
    #         type         message

    if exc_type is None:
        print("কোনো error হয়নি")
    else:
        print(f"Error: {exc_value}")

    return True   # True → exception suppress করো
    return False  # False → exception re-raise করো
```

**২. Async Context Manager:**
```python
class AsyncDBConnection:
    async def __aenter__(self):
        self.conn = await create_async_connection()
        return self.conn

    async def __aexit__(self, *args):
        await self.conn.close()

# Use:
async def main():
    async with AsyncDBConnection() as conn:
        await conn.execute("SELECT * FROM accounts")
```

---

### 📊 কোথায় Context Manager দেখবে:

| Use Case | Context Manager |
|---|---|
| File handling | `open()` |
| DB connection | `db.connect()` |
| DB transaction | `db.transaction()` |
| Thread lock | `threading.Lock()` |
| Temp directory | `tempfile.TemporaryDirectory()` |
| Mock in tests | `unittest.mock.patch()` |
| Async session | `aiohttp.ClientSession()` |

---

### 🎯 Interview Closing line:

> *"Context Manager banking system-এ অপরিহার্য — কারণ এখানে resource leak মানে security risk। DB connection না বন্ধ হলে connection pool শেষ হয়, transaction rollback না হলে data inconsistent হয়। Context Manager দিয়ে নিশ্চিত করা যায় যে error হোক বা না হোক, resource সবসময় properly cleanup হবে।"*

---

এখন পর্যন্ত Python core অনেকটাই cover হয়েছে। পরের গুরুত্বপূর্ণ topics:

- **OOP — Class, Inheritance, Polymorphism**
- **Exception Handling — try/except/finally**
- **Django REST API + JWT Authentication**
- **Database ORM + Query Optimization**

কোনটা নিয়ে আগাবে?




## `__init__` vs `__new__`

---

### 🔑 এক কথায়:

| | কাজ | কখন call হয় |
|---|---|---|
| `__new__` | Object **তৈরি** করে | `__init__` এর আগে |
| `__init__` | Object **initialize** করে | `__new__` এর পরে |

সহজ analogy:
```
__new__  = বাড়ি তৈরি করা (construction)
           memory-তে জায়গা বরাদ্দ হয়

__init__ = বাড়িতে আসবাবপত্র সাজানো (decoration)
           object-এর data set করা হয়
```

---

### 🧠 কোনটা আগে — কোনটা পরে:

```python
account = BankAccount("Sourov", 50000)

# Python আসলে এটাই করে:
# Step 1: __new__ → object তৈরি করো (empty shell)
obj = BankAccount.__new__(BankAccount)

# Step 2: __init__ → সেই object-এ data ভরো
BankAccount.__init__(obj, "Sourov", 50000)
```

---

### 💻 সাধারণ use — `__init__`:

```python
class BankAccount:

    def __init__(self, name, balance):
        # Object তৈরি হয়ে গেছে, এখন data set করছি
        self.name = name
        self.balance = balance
        print(f"Account initialized: {name}")

    def deposit(self, amount):
        self.balance += amount

acc = BankAccount("Sourov", 50000)
# Account initialized: Sourov

print(acc.name)     # Sourov
print(acc.balance)  # 50000
```

> 99% ক্ষেত্রে শুধু `__init__` দরকার।

---

### 💻 `__new__` কীভাবে কাজ করে:

```python
class BankAccount:

    def __new__(cls, name, balance):
        print(f"1. __new__ called — object তৈরি হচ্ছে")
        instance = super().__new__(cls)  # actual object তৈরি
        return instance                  # অবশ্যই return করতে হবে

    def __init__(self, name, balance):
        print(f"2. __init__ called — data set হচ্ছে")
        self.name = name
        self.balance = balance

acc = BankAccount("Sourov", 50000)
# 1. __new__ called — object তৈরি হচ্ছে
# 2. __init__ called — data set হচ্ছে
```

---

### ⚠️ `__new__` return না করলে:

```python
class Broken:

    def __new__(cls):
        print("__new__ called")
        # ❌ কিছু return করলাম না

    def __init__(self):
        print("__init__ called")

obj = Broken()
# __new__ called
# __init__ called হবে না! 😱
print(obj)   # None
```

> `__new__` যদি instance return না করে → `__init__` কখনো call হবে না।

---

### 🏦 Real Use Cases — কখন `__new__` দরকার:

**১. Singleton Pattern — একটাই instance:**
```python
class DatabaseConnection:
    """পুরো system-এ একটাই DB connection থাকবে"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("✅ নতুন connection তৈরি হচ্ছে")
            cls._instance = super().__new__(cls)
        else:
            print("♻️ Existing connection দেওয়া হচ্ছে")
        return cls._instance

    def __init__(self):
        self.url = "postgresql://ucb_db"

# Test:
conn1 = DatabaseConnection()   # ✅ নতুন connection তৈরি
conn2 = DatabaseConnection()   # ♻️ Existing connection

print(conn1 is conn2)   # True — একই object! ✅
# Banking-এ DB connection pool এভাবেই manage হয়
```

**২. Immutable Class — change করা যাবে না:**
```python
class TransactionID(str):
    """Transaction ID immutable হওয়া উচিত"""

    def __new__(cls, value):
        # str immutable — __new__-এ value set করতে হয়
        if not value.startswith("TXN-"):
            value = f"TXN-{value}"
        return super().__new__(cls, value)

    def __init__(self, value):
        # str already set হয়ে গেছে __new__-এ
        pass

txn = TransactionID("001")
print(txn)          # TXN-001
print(type(txn))    # <class 'TransactionID'>

# Immutable — change করা যাবে না
# txn[0] = "X"  ❌ str immutable
```

**৩. Object Creation Control:**
```python
class PremiumAccount:
    """শুধু নির্দিষ্ট শর্তে account খোলা যাবে"""
    _account_count = 0
    MAX_ACCOUNTS = 100   # সর্বোচ্চ ১০০টা premium account

    def __new__(cls, name, balance):
        if balance < 100000:
            print(f"❌ Minimum balance 1 lakh required")
            return None   # Object তৈরিই হবে না

        if cls._account_count >= cls.MAX_ACCOUNTS:
            print(f"❌ Premium account limit reached")
            return None

        cls._account_count += 1
        return super().__new__(cls)

    def __init__(self, name, balance):
        if self is None:
            return
        self.name = name
        self.balance = balance

# Test:
acc1 = PremiumAccount("Sourov", 50000)
# ❌ Minimum balance 1 lakh required
# acc1 = None

acc2 = PremiumAccount("Karim", 200000)
# ✅ Object তৈরি হলো
print(acc2.name)    # Karim
```

---

### 📊 `__init__` vs `__new__` — পুরো পার্থক্য:

| | `__init__` | `__new__` |
|---|---|---|
| **কাজ** | Initialize | Create |
| **Parameter** | `self` (object) | `cls` (class) |
| **Return** | কিছু না | Instance অবশ্যই |
| **কখন** | `__new__` এর পরে | সবার আগে |
| **Use করি** | সবসময় | বিশেষ ক্ষেত্রে |
| **Override করি?** | ✅ সবসময় | ❌ কদাচিৎ |

---

### ⚠️ Tricky Interview Question:

```python
class MyClass:

    def __new__(cls):
        print("__new__")
        return 42   # ❌ instance না, int return করলাম

    def __init__(self):
        print("__init__")

obj = MyClass()
# __new__
# __init__ call হবে না!
# কারণ __new__ MyClass instance return করেনি

print(obj)    # 42
print(type(obj))  # <class 'int'>
```

> `__new__` যদি **ওই class-এর instance** return না করে — `__init__` call হয় না।

---

### 💻 Metaclass-এ `__new__` — Advanced:

```python
# Django Model, SQLAlchemy — এভাবে কাজ করে
class ModelMeta(type):

    def __new__(mcs, name, bases, namespace):
        # Class তৈরির সময় fields automatically detect করো
        fields = {
            k: v for k, v in namespace.items()
            if not k.startswith("_")
        }
        namespace["_fields"] = fields
        return super().__new__(mcs, name, bases, namespace)

class Account(metaclass=ModelMeta):
    name = "CharField"
    balance = "DecimalField"
    created_at = "DateTimeField"

print(Account._fields)
# {'name': 'CharField', 'balance': 'DecimalField', ...}
# Django ORM এভাবেই model fields track করে
```

---

### 🎯 Interview Closing line:

> *"`__init__` হলো daily driver — object-এর data set করার জন্য। `__new__` হলো advanced tool — object creation control করার জন্য। Banking system-এ Singleton pattern দিয়ে DB connection manage করা, বা minimum balance enforce করে account creation control করা — এগুলোতে `__new__` এর real value। কিন্তু সাধারণত `__init__` দিয়েই সব কাজ হয়।"*

---

পরের গুরুত্বপূর্ণ topics:
- **OOP — Inheritance, Polymorphism, Encapsulation**
- **Exception Handling — try/except/finally**
- **Django REST API + JWT**
- **Database ORM + Query Optimization**

কোনটা নিয়ে আগাবে?




## OOP-এর ৪টা Pillar

---

### 🔑 এক নজরে:

```
OOP-এর ৪ Pillar
├── 1. Encapsulation  → data লুকিয়ে রাখো
├── 2. Inheritance    → parent থেকে নাও
├── 3. Polymorphism   → একই নাম, আলাদা কাজ
└── 4. Abstraction    → complexity লুকাও
```

---

## ১. Encapsulation — Data লুকিয়ে রাখো

> Object-এর data বাইরে থেকে directly access করতে দেবে না — শুধু নির্দিষ্ট method দিয়ে access করো।

```python
class BankAccount:

    def __init__(self, name, balance):
        self.name = name
        self.__balance = balance      # __ দিয়ে private করলাম
        self.__pin = "1234"           # বাইরে থেকে দেখা যাবে না

    # Getter — balance দেখার একমাত্র রাস্তা
    def get_balance(self):
        return self.__balance

    # Setter — balance change-এর একমাত্র রাস্তা
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.__balance += amount
        return self.__balance

    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError("Insufficient balance")
        self.__balance -= amount

acc = BankAccount("Sourov", 50000)

# ❌ Direct access blocked
# print(acc.__balance)   # AttributeError!
# print(acc.__pin)       # AttributeError!

# ✅ Method দিয়ে access
print(acc.get_balance())   # 50000
acc.deposit(10000)
print(acc.get_balance())   # 60000
```

**Python-এ Access Levels:**
```python
class Account:
    def __init__(self):
        self.name = "Sourov"      # Public   → সবাই দেখতে পারে
        self._balance = 50000     # Protected → convention, সরাসরি না
        self.__pin = "1234"       # Private   → class-এর বাইরে যাবে না
```

---

## ২. Inheritance — Parent থেকে নাও

> একটা class আরেকটা class-এর property আর method নিতে পারে — code repeat করতে হয় না।

```python
# Parent class
class Account:

    def __init__(self, account_id, name, balance):
        self.account_id = account_id
        self.name = name
        self._balance = balance

    def deposit(self, amount):
        self._balance += amount
        print(f"✅ {amount} deposited. Balance: {self._balance}")

    def get_balance(self):
        return self._balance

    def __str__(self):
        return f"Account[{self.account_id}] - {self.name}"


# Child class — Account-এর সব পাচ্ছে + নিজের কিছু
class SavingsAccount(Account):

    def __init__(self, account_id, name, balance, interest_rate):
        super().__init__(account_id, name, balance)  # parent init
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self._balance * self.interest_rate
        self._balance += interest
        print(f"✅ Interest {interest} added")


# Child class — আলাদা ধরনের account
class LoanAccount(Account):

    def __init__(self, account_id, name, balance, loan_amount):
        super().__init__(account_id, name, balance)
        self.loan_amount = loan_amount

    def repay(self, amount):
        self.loan_amount -= amount
        print(f"✅ {amount} repaid. Remaining: {self.loan_amount}")


# Use:
savings = SavingsAccount("SB-001", "Sourov", 50000, 0.05)
savings.deposit(10000)        # Parent-এর method ✅
savings.add_interest()        # নিজের method ✅

loan = LoanAccount("LN-001", "Karim", 0, 100000)
loan.repay(10000)
```

**Multiple Inheritance:**
```python
class Timestamped:
    def __init__(self):
        self.created_at = datetime.now()

class Auditable:
    def audit_log(self, action):
        print(f"AUDIT: {action} at {datetime.now()}")

# দুটো থেকেই নেওয়া
class PremiumAccount(Account, Timestamped, Auditable):
    def transfer(self, target, amount):
        self.audit_log(f"Transfer {amount} to {target}")
        self._balance -= amount
```

---

## ৩. Polymorphism — একই নাম, আলাদা কাজ

> একই method name — আলাদা class-এ আলাদা কাজ করে।

**Method Overriding:**
```python
class Account:
    def calculate_fee(self):
        return 0

class SavingsAccount(Account):
    def calculate_fee(self):       # Override করলাম
        return 50   # flat fee

class CurrentAccount(Account):
    def calculate_fee(self):       # Override করলাম
        return 200  # বেশি fee

class PremiumAccount(Account):
    def calculate_fee(self):       # Override করলাম
        return 0    # no fee

# Polymorphism-এর power:
accounts = [
    SavingsAccount(),
    CurrentAccount(),
    PremiumAccount(),
    SavingsAccount(),
]

# একই method call — আলাদা আলাদা result ✅
for acc in accounts:
    print(f"Fee: {acc.calculate_fee()} BDT")

# Fee: 50 BDT
# Fee: 200 BDT
# Fee: 0 BDT
# Fee: 50 BDT
```

**Duck Typing — Python-এর বিশেষ Polymorphism:**
```python
# Python-এ inheritance ছাড়াও polymorphism সম্ভব
class BkashPayment:
    def process(self, amount):
        print(f"Bkash: {amount} BDT sent")

class NagadPayment:
    def process(self, amount):
        print(f"Nagad: {amount} BDT sent")

class BankTransfer:
    def process(self, amount):
        print(f"Bank: {amount} BDT transferred")

# একই function — যেকোনো payment method চলবে
def make_payment(payment_method, amount):
    payment_method.process(amount)   # type check করে না!

make_payment(BkashPayment(), 500)
make_payment(NagadPayment(), 1000)
make_payment(BankTransfer(), 5000)
```

> **"If it walks like a duck and quacks like a duck — it's a duck"**
> Python শুধু দেখে method আছে কিনা — class কী সেটা গুরুত্বপূর্ণ না।

---

## ৪. Abstraction — Complexity লুকাও

> ব্যবহারকারীকে **কী করছে** দেখাও — **কীভাবে করছে** লুকাও।

```python
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    """Abstract class — blueprint মাত্র, সরাসরি use করা যাবে না"""

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def process_payment(self, amount):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    # Concrete method — সবার জন্য একই
    def execute(self, amount):
        self.connect()
        result = self.process_payment(amount)
        self.disconnect()
        return result


# Concrete class — নিজস্ব implementation
class VisaGateway(PaymentGateway):

    def connect(self):
        print("Visa API-তে connect হলো")

    def process_payment(self, amount):
        print(f"Visa-তে {amount} BDT charge হলো")
        return {"status": "success", "amount": amount}

    def disconnect(self):
        print("Visa connection বন্ধ হলো")


class MastercardGateway(PaymentGateway):

    def connect(self):
        print("Mastercard API-তে connect হলো")

    def process_payment(self, amount):
        print(f"Mastercard-এ {amount} BDT charge হলো")
        return {"status": "success", "amount": amount}

    def disconnect(self):
        print("Mastercard connection বন্ধ হলো")


# ❌ Abstract class সরাসরি use করা যাবে না
# gateway = PaymentGateway()   # TypeError!

# ✅ Concrete class use করো
visa = VisaGateway()
visa.execute(5000)
# Visa API-তে connect হলো
# Visa-তে 5000 BDT charge হলো
# Visa connection বন্ধ হলো
```

---

### 🏦 সব Pillar একসাথে — Real Banking System:

```python
from abc import ABC, abstractmethod

# Abstraction — blueprint
class Account(ABC):

    def __init__(self, account_id, name, balance):
        self.account_id = account_id
        self.name = name
        self._balance = balance          # Encapsulation — protected
        self.__transaction_log = []      # Encapsulation — private

    # Encapsulation — getter
    def get_balance(self):
        return self._balance

    # Abstraction — subclass নিজে implement করবে
    @abstractmethod
    def calculate_interest(self):
        pass

    # Concrete method — সবার জন্য একই
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Invalid amount")
        self._balance += amount
        self.__log(f"Deposit: {amount}")

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("Insufficient balance")
        self._balance -= amount
        self.__log(f"Withdraw: {amount}")

    # Encapsulation — private method
    def __log(self, action):
        self.__transaction_log.append(action)
        print(f"LOG: {action}")


# Inheritance — Account থেকে নিচ্ছে
class SavingsAccount(Account):

    def __init__(self, account_id, name, balance):
        super().__init__(account_id, name, balance)
        self.interest_rate = 0.06

    # Polymorphism — নিজের মতো implement করলো
    def calculate_interest(self):
        return self._balance * self.interest_rate


# Inheritance — Account থেকে নিচ্ছে
class CurrentAccount(Account):

    def __init__(self, account_id, name, balance):
        super().__init__(account_id, name, balance)
        self.interest_rate = 0.02

    # Polymorphism — আলাদা implementation
    def calculate_interest(self):
        return self._balance * self.interest_rate

    def overdraft(self, amount):
        # Current account-এ extra feature
        self._balance -= amount
        print(f"Overdraft: {amount} BDT")


# Use:
accounts = [
    SavingsAccount("SB-001", "Sourov", 50000),
    CurrentAccount("CA-001", "Karim", 100000),
]

# Polymorphism — একই loop, আলাদা result
for acc in accounts:
    interest = acc.calculate_interest()
    print(f"{acc.name}: Interest = {interest} BDT")

# Sourov: Interest = 3000.0 BDT
# Karim:  Interest = 2000.0 BDT
```

---

### 📊 ৪টা Pillar — এক নজরে:

| Pillar | কী করে | Keyword | Banking Example |
|---|---|---|---|
| **Encapsulation** | Data লুকায় | `__`, getter/setter | Balance সরাসরি change করতে দেয় না |
| **Inheritance** | Code reuse | `class Child(Parent)` | SavingsAccount, CurrentAccount |
| **Polymorphism** | Same interface, different behavior | Override | সব account-এর `calculate_interest()` আলাদা |
| **Abstraction** | Complexity লুকায় | `ABC`, `@abstractmethod` | Payment gateway-র details লুকানো |

---

### 🎯 Interview Closing line:

> *"OOP-এর এই ৪টা pillar মিলে একটা maintainable, secure system তৈরি হয়। Banking-এ Encapsulation মানে balance সরাসরি touch করতে না দেওয়া, Inheritance মানে common account logic একবার লেখা, Polymorphism মানে সব account type একইভাবে treat করা, Abstraction মানে payment gateway-র complexity আড়াল করা। এই চারটা ঠিকমতো use করলে code হয় clean, secure আর scalable।"*

---

পরের গুরুত্বপূর্ণ topics:
- **Exception Handling — try/except/finally**
- **Django REST API + JWT Authentication**
- **Database ORM + Query Optimization**
- **SOLID Principles**

কোনটা নিয়ে আগাবে?



## Inheritance Types in Python

---

### 🔑 Python-এ ৫ ধরনের Inheritance:

```
1. Single       → A → B
2. Multiple     → A, B → C
3. Multilevel   → A → B → C
4. Hierarchical → A → B, C, D
5. Hybrid       → উপরের combination
```

---

## ১. Single Inheritance — সবচেয়ে সহজ

> একটা child, একটা parent।

```python
# Parent
class Account:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self._balance = balance

    def get_balance(self):
        return self._balance

    def deposit(self, amount):
        self._balance += amount
        print(f"✅ {amount} deposited")

# Child — Account থেকে সব পাচ্ছে
class SavingsAccount(Account):

    def __init__(self, account_id, balance, interest_rate):
        super().__init__(account_id, balance)   # parent init
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self._balance * self.interest_rate
        self._balance += interest
        print(f"✅ Interest {interest:.2f} added")

# Use:
acc = SavingsAccount("SB-001", 50000, 0.06)
acc.deposit(10000)          # Parent method ✅
acc.add_interest()          # Child method ✅
print(acc.get_balance())    # Parent method ✅
```

---

## ২. Multiple Inheritance — দুই Parent

> একটা child, একাধিক parent।

```python
class Auditable:
    """সব action log করে"""
    def __init__(self):
        self.logs = []

    def log(self, action):
        self.logs.append(action)
        print(f"AUDIT: {action}")

    def get_logs(self):
        return self.logs


class Notifiable:
    """সব event-এ notification পাঠায়"""
    def notify(self, message, channel="SMS"):
        print(f"NOTIFY [{channel}]: {message}")


# দুটো parent থেকেই নিচ্ছে
class PremiumAccount(Account, Auditable, Notifiable):

    def __init__(self, account_id, balance):
        Account.__init__(self, account_id, balance)
        Auditable.__init__(self)

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("Insufficient balance")
        self._balance -= amount
        self.log(f"Withdraw: {amount} BDT")          # Auditable ✅
        self.notify(f"{amount} BDT withdrawn")        # Notifiable ✅

# Use:
acc = PremiumAccount("PR-001", 100000)
acc.withdraw(5000)
# AUDIT: Withdraw: 5000 BDT
# NOTIFY [SMS]: 5000 BDT withdrawn

print(acc.get_logs())   # Auditable method ✅
```

---

### ⚠️ Multiple Inheritance-এর বড় সমস্যা — Diamond Problem:

```
     Account
    /       \
Savings   Current
    \       /
   HybridAccount   ← কোন Account.__init__() চলবে?
```

```python
class Account:
    def __init__(self):
        print("Account init")

class SavingsAccount(Account):
    def __init__(self):
        super().__init__()
        print("Savings init")

class CurrentAccount(Account):
    def __init__(self):
        super().__init__()
        print("Current init")

class HybridAccount(SavingsAccount, CurrentAccount):
    def __init__(self):
        super().__init__()
        print("Hybrid init")

h = HybridAccount()
# Account init      ← একবারই চলে ✅
# Current init
# Savings init
# Hybrid init
```

**Python MRO দিয়ে solve করে:**
```python
# MRO = Method Resolution Order
# কোন class-এর method আগে দেখবে সেটা নির্ধারণ করে

print(HybridAccount.__mro__)
# [HybridAccount, SavingsAccount, CurrentAccount, Account, object]
#       ↑               ↑               ↑            ↑
#    আগে দেখে         তারপর          তারপর        শেষে

# Left → Right, তারপর Parent
```

---

## ৩. Multilevel Inheritance — দাদা → বাবা → ছেলে

> Chain of inheritance।

```python
# Level 1 — দাদা
class Account:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self._balance = balance

    def get_balance(self):
        return self._balance


# Level 2 — বাবা
class SavingsAccount(Account):
    def __init__(self, account_id, balance, interest_rate):
        super().__init__(account_id, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self._balance * self.interest_rate
        self._balance += interest
        return interest


# Level 3 — ছেলে
class StudentSavingsAccount(SavingsAccount):
    def __init__(self, account_id, balance, student_id):
        super().__init__(account_id, balance, interest_rate=0.08)
        self.student_id = student_id
        self.monthly_limit = 10000   # ছাত্রদের extra limit

    def withdraw(self, amount):
        if amount > self.monthly_limit:
            print(f"❌ Monthly limit {self.monthly_limit} exceeded")
            return
        self._balance -= amount
        print(f"✅ {amount} withdrawn")

# Use:
acc = StudentSavingsAccount("ST-001", 20000, "STD-123")

# দাদার method ✅
print(acc.get_balance())

# বাবার method ✅
acc.add_interest()

# নিজের method ✅
acc.withdraw(5000)
acc.withdraw(15000)   # ❌ Monthly limit exceeded
```

---

## ৪. Hierarchical Inheritance — এক Parent, অনেক Child

> একটা parent থেকে অনেক child।

```python
# একটাই Parent
class Account:
    def __init__(self, account_id, name, balance):
        self.account_id = account_id
        self.name = name
        self._balance = balance

    def deposit(self, amount):
        self._balance += amount

    def get_balance(self):
        return self._balance


# Child 1
class SavingsAccount(Account):
    def calculate_interest(self):
        return self._balance * 0.06


# Child 2
class CurrentAccount(Account):
    def calculate_interest(self):
        return self._balance * 0.02

    def overdraft(self, amount):
        self._balance -= amount   # Current account-এ allowed
        print(f"Overdraft: {amount}")


# Child 3
class FixedDepositAccount(Account):
    def __init__(self, account_id, name, balance, months):
        super().__init__(account_id, name, balance)
        self.months = months
        self.locked = True

    def calculate_interest(self):
        return self._balance * 0.09   # FD-তে সবচেয়ে বেশি

    def withdraw(self, amount):
        if self.locked:
            print("❌ FD locked — mature হওয়ার আগে তোলা যাবে না")
            return


# Child 4
class LoanAccount(Account):
    def __init__(self, account_id, name, loan_amount):
        super().__init__(account_id, name, 0)
        self.loan_amount = loan_amount

    def calculate_emi(self, months):
        return self.loan_amount / months


# Polymorphism দিয়ে সবাইকে একসাথে handle:
accounts = [
    SavingsAccount("SB-001", "Sourov", 50000),
    CurrentAccount("CA-001", "Karim", 100000),
    FixedDepositAccount("FD-001", "Rina", 200000, 12),
]

# একই loop — সবার interest আলাদা আলাদা ✅
for acc in accounts:
    print(f"{acc.name}: {acc.calculate_interest():.2f} BDT")

# Sourov: 3000.00 BDT
# Karim:  2000.00 BDT
# Rina:   18000.00 BDT
```

---

## ৫. Hybrid Inheritance — সব মিলিয়ে

> একাধিক type-এর combination।

```python
# Base
class Account:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self._balance = balance

    def get_balance(self):
        return self._balance


# Level 2 — Hierarchical
class SavingsAccount(Account):
    def interest(self):
        return self._balance * 0.06

class CurrentAccount(Account):
    def interest(self):
        return self._balance * 0.02


# Level 3 — Multiple (SavingsAccount + CurrentAccount)
# এটাই Hybrid — Multilevel + Multiple একসাথে
class HybridAccount(SavingsAccount, CurrentAccount):

    def __init__(self, account_id, balance):
        super().__init__(account_id, balance)

    def total_interest(self):
        # MRO অনুযায়ী SavingsAccount-এর interest()
        return self.interest()

# MRO check:
print(HybridAccount.__mro__)
# [HybridAccount, SavingsAccount, CurrentAccount, Account, object]

acc = HybridAccount("HB-001", 100000)
print(acc.total_interest())   # 6000.0 — Savings rate ✅
```

---

### 📊 সব Types এক নজরে:

| Type | Structure | কখন use করবে | Banking Example |
|---|---|---|---|
| **Single** | A → B | সবচেয়ে সাধারণ | Account → SavingsAccount |
| **Multiple** | A,B → C | আলাদা features combine | Account + Auditable + Notifiable |
| **Multilevel** | A → B → C | Specialization বাড়াতে | Account → Savings → StudentSavings |
| **Hierarchical** | A → B,C,D | Same base, different types | Account → Savings, Current, FD, Loan |
| **Hybrid** | সব মিলিয়ে | Complex system | উপরের সব একসাথে |

---

### ⚠️ `super()` কীভাবে কাজ করে — MRO অনুযায়ী:

```python
class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        super().show()   # MRO-তে পরেরজনকে call করে
        print("B")

class C(A):
    def show(self):
        super().show()
        print("C")

class D(B, C):
    def show(self):
        super().show()
        print("D")

D().show()
# MRO: D → B → C → A
# A
# C
# B
# D
```

---

### 🎯 Interview Closing line:

> *"Python-এ inheritance type choice করি requirement অনুযায়ী। Banking system-এ সাধারণত Hierarchical সবচেয়ে বেশি use হয় — একটা base Account class থেকে Savings, Current, FD, Loan — সব আলাদা আলাদা। Multiple inheritance-এ Diamond problem হতে পারে — Python MRO দিয়ে সেটা solve করে। `super()` সবসময় MRO follow করে — তাই multiple inheritance-এও safe।"*

---

পরের গুরুত্বপূর্ণ topics:
- **Exception Handling — try/except/finally**
- **SOLID Principles**
- **Django REST API + JWT**
- **Database ORM + Query Optimization**

কোনটা নিয়ে আগাবে?


## Method Overloading vs Overriding

---

## ১. Method Overloading — Python-এ possible?

> **Overloading** মানে — একই নামের method, কিন্তু **আলাদা আলাদা parameter** দিয়ে call করা যাবে।

---

### ❌ Python-এ Traditional Overloading নেই:

```python
class Account:
    def deposit(self, amount):
        print(f"Depositing {amount}")

    def deposit(self, amount, currency):   # ❌ আগেরটা replace হয়ে গেছে!
        print(f"Depositing {amount} {currency}")

acc = Account()
acc.deposit(500)          # ❌ TypeError! — শুধু শেষেরটা survive করে
acc.deposit(500, "BDT")   # ✅ এটা কাজ করে
```

> Python-এ **একই নামে দুটো method লিখলে দ্বিতীয়টা প্রথমটাকে replace করে।**

---

### ✅ Python-এ Overloading-এর বিকল্প:

**উপায় ১ — Default Parameter:**
```python
class Account:
    def deposit(self, amount, currency="BDT", note=None):
        if note:
            print(f"Note: {note}")
        print(f"Depositing {amount} {currency}")

acc = Account()
acc.deposit(500)                        # ✅ Depositing 500 BDT
acc.deposit(500, "USD")                 # ✅ Depositing 500 USD
acc.deposit(500, "BDT", "Salary")       # ✅ Note: Salary
```

**উপায় ২ — `*args` / `**kwargs`:**
```python
class Calculator:
    def add(self, *args):
        return sum(args)

calc = Calculator()
print(calc.add(10, 20))           # 30
print(calc.add(10, 20, 30))       # 60
print(calc.add(10, 20, 30, 40))   # 100
```

**উপায় ৩ — `@singledispatch` (Functional Overloading):**
```python
from functools import singledispatch

@singledispatch
def process_payment(amount):
    print(f"Default: {amount}")

@process_payment.register(str)
def _(amount):
    print(f"String amount: {float(amount)} BDT")

@process_payment.register(dict)
def _(amount):
    print(f"Dict: {amount['value']} {amount['currency']}")

process_payment(500)                           # Default: 500
process_payment("1000.50")                     # String amount: 1000.5 BDT
process_payment({"value": 500, "currency": "USD"})  # Dict: 500 USD
```

**উপায় ৪ — `isinstance` দিয়ে:**
```python
class Account:
    def transfer(self, target):
        if isinstance(target, str):
            # account ID দিয়ে transfer
            print(f"Transfer to account ID: {target}")
        elif isinstance(target, Account):
            # Account object দিয়ে transfer
            print(f"Transfer to: {target.name}")
        elif isinstance(target, list):
            # Multiple accounts-এ transfer
            for acc in target:
                print(f"Split transfer to: {acc}")
```

---

## ২. Method Overriding — কী এবং কেন:

> **Overriding** মানে — child class parent-এর method-কে **নিজের মতো করে rewrite** করে।

---

### 💻 Basic Override:

```python
class Account:
    def calculate_interest(self):
        return 0    # Default — কোনো interest নেই

class SavingsAccount(Account):
    def calculate_interest(self):      # ← Override করলাম
        return self._balance * 0.06    # নিজের logic

class CurrentAccount(Account):
    def calculate_interest(self):      # ← Override করলাম
        return self._balance * 0.02    # আলাদা logic

class FixedDeposit(Account):
    def calculate_interest(self):      # ← Override করলাম
        return self._balance * 0.09    # সবচেয়ে বেশি
```

---

### 💻 `super()` দিয়ে Parent-এর কাজও রাখা:

```python
class Account:
    def withdraw(self, amount):
        self._balance -= amount
        print(f"{amount} BDT withdrawn")

class SavingsAccount(Account):
    def withdraw(self, amount):
        # নিজের extra check
        if amount > 50000:
            print("❌ Single withdrawal limit 50,000 BDT")
            return

        # Parent-এর কাজও করো
        super().withdraw(amount)     # ← parent method call
        print("SMS sent to customer")

acc = SavingsAccount("SB-001", 100000)
acc.withdraw(10000)
# 10000 BDT withdrawn        ← parent-এর কাজ
# SMS sent to customer       ← নিজের extra কাজ

acc.withdraw(60000)
# ❌ Single withdrawal limit 50,000 BDT
```

---

### ⚠️ Tricky — Override না করলে কী হয়:

```python
class Account:
    def get_type(self):
        return "Generic Account"

class SavingsAccount(Account):
    pass   # override করিনি

class CurrentAccount(Account):
    def get_type(self):              # override করেছি
        return "Current Account"

s = SavingsAccount()
c = CurrentAccount()

print(s.get_type())   # "Generic Account" — parent-এর চলে
print(c.get_type())   # "Current Account" — নিজেরটা চলে
```

---

### 💻 `__str__` এবং `__repr__` Override:

```python
class Account:
    def __init__(self, account_id, name, balance):
        self.account_id = account_id
        self.name = name
        self._balance = balance

    # Override — print() করলে কী দেখাবে
    def __str__(self):
        return f"[{self.account_id}] {self.name} — {self._balance} BDT"

    # Override — debug-এ কী দেখাবে
    def __repr__(self):
        return f"Account(id={self.account_id}, name={self.name})"

acc = Account("SB-001", "Sourov", 50000)
print(acc)       # [SB-001] Sourov — 50000 BDT
print(repr(acc)) # Account(id=SB-001, name=Sourov)
```

---

### 💻 Abstract Method Override — বাধ্যতামূলক:

```python
from abc import ABC, abstractmethod

class PaymentGateway(ABC):

    @abstractmethod
    def process(self, amount):
        pass   # Child-কে অবশ্যই implement করতে হবে

class BkashGateway(PaymentGateway):
    def process(self, amount):          # ✅ Override বাধ্যতামূলক
        print(f"Bkash: {amount} sent")

class NagadGateway(PaymentGateway):
    def process(self, amount):          # ✅ Override বাধ্যতামূলক
        print(f"Nagad: {amount} sent")

# ❌ Override না করলে error
class BadGateway(PaymentGateway):
    pass

bg = BadGateway()   # TypeError: Can't instantiate abstract class!
```

---

### 📊 Overloading vs Overriding — পার্থক্য:

| | Overloading | Overriding |
|---|---|---|
| **কোথায়** | Same class | Parent → Child |
| **Python-এ** | ❌ Directly নেই | ✅ পুরোপুরি আছে |
| **কেন** | Different inputs handle | Behavior customize |
| **Method নাম** | Same | Same |
| **Parameter** | আলাদা | Same |
| **Inheritance** | লাগে না | লাগে |

---

### 🎯 Interview Closing line:

> *"Python-এ traditional method overloading নেই — কারণ same name-এ দুটো method লিখলে দ্বিতীয়টা প্রথমটাকে replace করে। তবে default parameter, `*args`, আর `isinstance` দিয়ে same effect পাওয়া যায়। Method overriding Python-এ পুরোপুরি supported — banking system-এ প্রতিটা account type-এর আলাদা interest calculation, withdraw limit — এগুলো overriding দিয়েই implement করি। Abstract method দিয়ে override বাধ্যতামূলক করা যায়।"*

---

পরের topics:
- **Exception Handling — try/except/finally**
- **SOLID Principles**
- **Django REST API + JWT**
- **Database ORM + Query Optimization**

কোনটা নিয়ে আগাবে?

## Exception Handling Best Practices & Custom Exception

---

## ১. Exception Handling — Basics থেকে Best Practice

---

### 🔑 Basic Structure:

```python
try:
    # ঝুঁকিপূর্ণ কাজ
except SpecificException as e:
    # নির্দিষ্ট error handle
except AnotherException as e:
    # আরেকটা error handle
else:
    # কোনো error হয়নি → এটা চলবে
finally:
    # error হোক বা না হোক → সবসময় চলবে
```

---

### 💻 `else` আর `finally` — কীভাবে কাজ করে:

```python
def withdraw(balance, amount):
    try:
        if amount > balance:
            raise ValueError("Insufficient balance")
        balance -= amount

    except ValueError as e:
        print(f"❌ Error: {e}")

    else:
        # try সফল হলে চলে — exception হলে চলে না
        print(f"✅ Withdrawal successful")
        send_sms("Withdrawal done")   # success হলেই SMS

    finally:
        # সবসময় চলে — error হোক বা না হোক
        print("📝 Transaction logged")
        close_db_connection()         # resource cleanup

withdraw(50000, 10000)
# ✅ Withdrawal successful
# 📝 Transaction logged

withdraw(50000, 60000)
# ❌ Error: Insufficient balance
# 📝 Transaction logged   ← তবুও চলে
```

---

### ✅ Best Practices:

---

**১. Broad Exception ধরা যাবে না:**
```python
# ❌ Bad — সব ধরে নেয়, কী হলো বোঝা যায় না
try:
    process_payment(amount)
except Exception:
    print("Something went wrong")

# ✅ Good — নির্দিষ্ট exception ধরো
try:
    process_payment(amount)
except ValueError as e:
    print(f"Invalid amount: {e}")
except ConnectionError as e:
    print(f"DB connection failed: {e}")
except TimeoutError as e:
    print(f"Request timed out: {e}")
```

---

**২. Bare `except` কখনো না:**
```python
# ❌ Worst — KeyboardInterrupt, SystemExit সব ধরে!
try:
    transfer_money(amount)
except:
    pass    # Silent failure — debugging nightmare 😱

# ✅ Always specify
try:
    transfer_money(amount)
except Exception as e:
    logger.error(f"Transfer failed: {e}")
    raise   # re-raise করো
```

---

**৩. Exception চেপে রাখা যাবে না:**
```python
# ❌ Bad — error হলো কিন্তু কেউ জানলো না
try:
    debit_account("SB-001", 5000)
except Exception:
    pass   # 😱 Silent failure

# ✅ Good — log করো, re-raise করো
try:
    debit_account("SB-001", 5000)
except Exception as e:
    logger.error(f"Debit failed: {e}", exc_info=True)
    raise   # caller-কে জানাও
```

---

**৪. Exception-এ Cleanup নিশ্চিত করো:**
```python
# ❌ Bad — exception হলে connection কখনো বন্ধ হবে না
conn = get_db_connection()
result = conn.execute(query)   # এখানে error হলে?
conn.close()                   # এই line কখনো আসবে না 😱

# ✅ Good — finally বা context manager
try:
    conn = get_db_connection()
    result = conn.execute(query)
finally:
    conn.close()   # সবসময় বন্ধ হবে ✅

# আরো ভালো — context manager
with get_db_connection() as conn:
    result = conn.execute(query)
# automatically closed ✅
```

---

**৫. Exception Chaining — কোথা থেকে এলো বলো:**
```python
# ❌ Bad — original error হারিয়ে যায়
try:
    user = db.get_user(user_id)
except DatabaseError as e:
    raise ValueError("User not found")   # original error গেল কোথায়?

# ✅ Good — `from` দিয়ে chain করো
try:
    user = db.get_user(user_id)
except DatabaseError as e:
    raise ValueError("User not found") from e   # chain ✅

# Output:
# DatabaseError: connection refused
# The above exception was the direct cause of:
# ValueError: User not found
```

---

**৬. Logging সঠিকভাবে:**
```python
import logging

logger = logging.getLogger(__name__)

def process_transaction(txn_id, amount):
    try:
        validate_amount(amount)
        execute_transaction(txn_id, amount)

    except ValidationError as e:
        # User-এর ভুল — WARNING
        logger.warning(f"Invalid transaction {txn_id}: {e}")
        raise

    except DatabaseError as e:
        # System-এর সমস্যা — ERROR + full traceback
        logger.error(
            f"DB error for txn {txn_id}",
            exc_info=True    # ← full stack trace log হবে
        )
        raise

    except Exception as e:
        # Unexpected — CRITICAL
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        raise
```

---

## ২. Custom Exception — কীভাবে বানাবে

---

### 🔑 কেন Custom Exception:

```
Built-in exceptions অনেক generic:
ValueError, TypeError, RuntimeError...

Banking system-এ দরকার specific errors:
InsufficientBalanceError
AccountFrozenError
DailyLimitExceededError
FraudDetectedError
```

---

### 💻 Basic Custom Exception:

```python
# Base Exception class থেকে inherit করো
class BankingError(Exception):
    """সব banking error-এর base"""
    pass

class InsufficientBalanceError(BankingError):
    pass

class AccountFrozenError(BankingError):
    pass

# Use:
def withdraw(account, amount):
    if account.frozen:
        raise AccountFrozenError("Account is frozen")
    if account.balance < amount:
        raise InsufficientBalanceError("Not enough balance")

try:
    withdraw(account, 5000)
except InsufficientBalanceError as e:
    print(f"Balance কম: {e}")
except AccountFrozenError as e:
    print(f"Account frozen: {e}")
```

---

### 💻 Rich Custom Exception — Extra Info সহ:

```python
class InsufficientBalanceError(Exception):

    def __init__(self, account_id, requested, available):
        self.account_id = account_id
        self.requested = requested
        self.available = available
        self.shortfall = requested - available

        # Parent-এ message পাঠাও
        super().__init__(
            f"Account {account_id}: "
            f"Requested {requested} BDT, "
            f"Available {available} BDT, "
            f"Shortfall {self.shortfall} BDT"
        )

    def __str__(self):
        return (
            f"InsufficientBalance | "
            f"Account: {self.account_id} | "
            f"Need: {self.shortfall} BDT more"
        )


# Use:
try:
    raise InsufficientBalanceError("SB-001", 10000, 3000)
except InsufficientBalanceError as e:
    print(e)                    # Custom message
    print(e.shortfall)          # 7000 — extra info access ✅
    print(e.account_id)         # SB-001
```

---

### 💻 Full Banking Exception Hierarchy:

```python
# ── Base
class BankingError(Exception):
    """সব UCB banking error-এর root"""

    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code
        self.message = message

    def to_dict(self):
        """API response-এর জন্য"""
        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "code": self.error_code
        }


# ── Account Errors
class AccountError(BankingError):
    """Account সংক্রান্ত সব error"""
    pass

class AccountNotFoundError(AccountError):
    def __init__(self, account_id):
        super().__init__(
            f"Account {account_id} not found",
            error_code="ACC_001"
        )
        self.account_id = account_id

class AccountFrozenError(AccountError):
    def __init__(self, account_id, reason):
        super().__init__(
            f"Account {account_id} is frozen: {reason}",
            error_code="ACC_002"
        )

class AccountClosedError(AccountError):
    def __init__(self, account_id):
        super().__init__(
            f"Account {account_id} is permanently closed",
            error_code="ACC_003"
        )


# ── Transaction Errors
class TransactionError(BankingError):
    """Transaction সংক্রান্ত সব error"""
    pass

class InsufficientBalanceError(TransactionError):
    def __init__(self, account_id, requested, available):
        self.requested = requested
        self.available = available
        self.shortfall = requested - available
        super().__init__(
            f"Insufficient balance in {account_id}. "
            f"Need {self.shortfall} BDT more",
            error_code="TXN_001"
        )

class DailyLimitExceededError(TransactionError):
    def __init__(self, account_id, limit, attempted):
        super().__init__(
            f"Daily limit {limit} BDT exceeded. "
            f"Attempted: {attempted} BDT",
            error_code="TXN_002"
        )
        self.limit = limit
        self.attempted = attempted

class InvalidAmountError(TransactionError):
    def __init__(self, amount):
        super().__init__(
            f"Invalid amount: {amount}. Must be positive",
            error_code="TXN_003"
        )


# ── Security Errors
class SecurityError(BankingError):
    """Security সংক্রান্ত error"""
    pass

class FraudDetectedError(SecurityError):
    def __init__(self, account_id, risk_score):
        super().__init__(
            f"Fraud suspected on {account_id}. "
            f"Risk score: {risk_score}",
            error_code="SEC_001"
        )
        self.risk_score = risk_score

class UnauthorizedAccessError(SecurityError):
    def __init__(self, user_id, resource):
        super().__init__(
            f"User {user_id} unauthorized to access {resource}",
            error_code="SEC_002"
        )
```

---

### 💻 Real Use — Transfer Money:

```python
def transfer_money(from_id, to_id, amount):

    # Validation
    if amount <= 0:
        raise InvalidAmountError(amount)

    # Account check
    from_acc = db.get_account(from_id)
    if not from_acc:
        raise AccountNotFoundError(from_id)

    if from_acc.frozen:
        raise AccountFrozenError(from_id, "Suspicious activity")

    # Balance check
    if from_acc.balance < amount:
        raise InsufficientBalanceError(from_id, amount, from_acc.balance)

    # Daily limit check
    if from_acc.today_total + amount > from_acc.daily_limit:
        raise DailyLimitExceededError(
            from_id,
            from_acc.daily_limit,
            amount
        )

    # Fraud check
    risk = fraud_service.check(from_id, amount)
    if risk > 0.8:
        raise FraudDetectedError(from_id, risk)

    # Execute transfer
    from_acc.balance -= amount
    to_acc.balance += amount
    db.save()


# API Layer-এ handle করো:
from django.http import JsonResponse

def transfer_view(request):
    try:
        transfer_money(
            request.data["from"],
            request.data["to"],
            request.data["amount"]
        )
        return JsonResponse({"status": "success"})

    except InvalidAmountError as e:
        return JsonResponse(e.to_dict(), status=400)

    except AccountNotFoundError as e:
        return JsonResponse(e.to_dict(), status=404)

    except InsufficientBalanceError as e:
        return JsonResponse({
            **e.to_dict(),
            "shortfall": e.shortfall   # extra info ✅
        }, status=422)

    except FraudDetectedError as e:
        logger.critical(f"FRAUD: {e}", exc_info=True)
        return JsonResponse(e.to_dict(), status=403)

    except BankingError as e:
        # যেকোনো banking error — catch-all
        logger.error(f"Banking error: {e}")
        return JsonResponse(e.to_dict(), status=500)

    except Exception as e:
        # Unexpected system error
        logger.critical(f"Unexpected: {e}", exc_info=True)
        return JsonResponse({"error": "System error"}, status=500)
```

---

### 📊 Exception Hierarchy — Visual:

```
Exception
└── BankingError
    ├── AccountError
    │   ├── AccountNotFoundError     (ACC_001)
    │   ├── AccountFrozenError       (ACC_002)
    │   └── AccountClosedError       (ACC_003)
    ├── TransactionError
    │   ├── InsufficientBalanceError (TXN_001)
    │   ├── DailyLimitExceededError  (TXN_002)
    │   └── InvalidAmountError       (TXN_003)
    └── SecurityError
        ├── FraudDetectedError       (SEC_001)
        └── UnauthorizedAccessError  (SEC_002)
```

---

### 📊 Best Practices Summary:

| ❌ করো না | ✅ করো |
|---|---|
| Bare `except:` | Specific exception ধরো |
| Exception চেপে রাখো | Log করো, re-raise করো |
| Generic `Exception` ধরো | Custom exception বানাও |
| `finally`-তে business logic | `finally`-তে শুধু cleanup |
| Error message ছাড়া raise | Meaningful message দাও |
| Exception chain ভাঙো | `raise X from Y` করো |

---

### 🎯 Interview Closing line:

> *"Banking system-এ exception handling শুধু crash থেকে বাঁচা না — এটা security আর auditability-র অংশ। Custom exception hierarchy বানালে error code দিয়ে specific problem identify করা যায়, API response consistent হয়, আর log দেখে exactly কোথায় কী হয়েছে বোঝা যায়। `InsufficientBalanceError` ধরলে shortfall কতটুকু সেটাও জানা যায় — generic `ValueError` দিয়ে এটা সম্ভব না।"*

---

পরের গুরুত্বপূর্ণ topics:
- **SOLID Principles**
- **Django REST API + JWT**
- **Database ORM + Query Optimization**
- **Design Patterns — Singleton, Factory**

কোনটা নিয়ে আগাবে?

পাইথনে **Duck Typing (ডাক টাইপিং)** হলো একটি প্রোগ্রামিং কনসেপ্ট যেখানে কোনো অবজেক্টের **টাইপ (Type)** বা **ক্লাস (Class)** কী, তার চেয়ে বড় কথা হলো সেই অবজেক্টটি কী **কাজ (Behavior)** করতে পারে।

এর মূল মন্ত্রটি হলো:
> *"যদি এটি হাঁসের মতো হাঁটে এবং হাঁসের মতো প্যাক প্যাক (quack) করে, তবে এটি একটি হাঁস।"*

সহজ কথায়, পাইথন চেক করে না যে আপনি কোন ক্লাসের অবজেক্ট ব্যবহার করছেন; সে শুধু দেখে আপনি যে মেথড বা প্রপার্টি কল করছেন, সেটি ওই অবজেক্টের মধ্যে আছে কি না।

---

### একটি সহজ উদাহরণ
ধরা যাক, আমাদের একটি ফাংশন আছে যা কোনো কিছুকে "হাঁটানো"র কাজ করে। পাইথনে আমরা এভাবে কোডটি লিখতে পারি:

```python
class Duck:
    def walk(self):
        print("হাঁসটি হাঁটছে...")

class Person:
    def walk(self):
        print("মানুষটি হাঁসের মতো নকল করে হাঁটছে!")

def perform_walk(thing):
    # এখানে আমরা চেক করছি না 'thing' কি Duck নাকি Person
    # আমরা শুধু 'walk' মেথডটি কল করছি
    thing.walk()

# দুটি ভিন্ন ক্লাস হওয়া সত্ত্বেও একই ফাংশন দিয়ে কাজ করছে
perform_walk(Duck())
perform_walk(Person())
```

### ডাক টাইপিং কেন ব্যবহার করবেন?
* **ফ্লেক্সিবিলিটি:** আপনার কোড নির্দিষ্ট কোনো ক্লাসের ওপর নির্ভরশীল থাকে না। যতক্ষণ অবজেক্টের প্রয়োজনীয় মেথডটি থাকছে, ততক্ষণ কোড কাজ করবে।
* **সহজ কোডিং:** ইন্টারফেস বা অ্যাবস্ট্রাক্ট ক্লাস নিয়ে খুব বেশি মাথা ঘামাতে হয় না।
* **Pythonic Way:** এটি পাইথনের একটি আদর্শ পদ্ধতি যা কোডকে আরও ডাইনামিক করে তোলে।

---

### Duck Typing বনাম Static Typing

| বৈশিষ্ট্য | স্ট্যাটিক টাইপিং (যেমন: Java/C++) | ডাক টাইপিং (Python) |
| :--- | :--- | :--- |
| **টাইপ চেকিং** | কোড রান করার আগেই টাইপ চেক করা হয়। | কোড রান করার সময় আচরণ চেক করা হয়। |
| **গুরুত্ব** | অবজেক্টের **পরিচয় (Identity)** বা ক্লাস বড়। | অবজেক্টের **কাজ (Behavior)** বড়। |
| **নির্ভরযোগ্যতা** | টাইপ ভুল হলে কম্পাইল এরর দেয়। | মেথড না থাকলে রানটাইমে `AttributeError` দেয়। |

---

### একটি ছোট সতর্কতা
ডাক টাইপিং খুব শক্তিশালী হলেও এতে কিছুটা ঝুঁকি থাকে। ধরুন, আপনি এমন একটি অবজেক্ট পাঠালেন যাতে `walk()` মেথডটি নেই, তখন পাইথন একটি এরর থ্রো করবে। 

এই জন্য পাইথনে প্রায়ই **EAFP** (*Easier to Ask for Forgiveness than Permission*) স্টাইল ব্যবহার করা হয়। অর্থাৎ, আগে কাজটা করার চেষ্টা করা হয়, আর যদি না হয় তবে এরর হ্যান্ডেল করা হয়।

আপনি কি আপনার প্রজেক্টের কোনো নির্দিষ্ট লজিক বা এরর হ্যান্ডলিং নিয়ে ডাক টাইপিং প্রয়োগ করার কথা ভাবছেন?

পাইথনে কোনো কোড কাজ করছে কি না বা কোথায় সমস্যা হচ্ছে তা দেখার জন্য আমরা সাধারণত `print()` ব্যবহার করি। কিন্তু প্রফেশনাল সফটওয়্যার ডেভেলপমেন্টে `logging` মডিউল ব্যবহার করা অনেক বেশি কার্যকর। 

সহজ কথায় বলতে গেলে: **Print** হলো আপনার সেই বন্ধু যে চিৎকার করে সব বলে দেয়, আর **Logging** হলো আপনার সেই ডায়েরি যা সবকিছু সময় এবং গুরুত্ব অনুযায়ী গুছিয়ে লিখে রাখে।

নিচে এদের মূল পার্থক্যগুলো বিস্তারিত আলোচনা করা হলো:

---

### ১. ডিবাগিং এবং লেভেলিং (Levels)
`print()` এর কোনো লেভেল নেই। আপনি যা প্রিন্ট করবেন তা একইভাবেই স্ক্রিনে আসবে। কিন্তু `logging`-এ তথ্যের গুরুত্ব অনুযায়ী বিভিন্ন লেভেল থাকে:

* **DEBUG:** বিস্তারিত তথ্য (সাধারণত সমস্যা খুঁজতে ব্যবহৃত হয়)।
* **INFO:** কাজ ঠিকঠাক চলছে কি না তার নিশ্চয়তা।
* **WARNING:** কোনো সমস্যা হতে পারে এমন সংকেত।
* **ERROR:** বড় কোনো সমস্যা যেখানে সফটওয়্যারের একটি অংশ কাজ করছে না।
* **CRITICAL:** মারাত্মক এরর, যার ফলে পুরো প্রোগ্রাম বন্ধ হয়ে যেতে পারে।



---

### ২. তথ্যের গন্তব্য (Destination)
* **print():** এটি শুধুমাত্র কনসোল বা টার্মিনালে আউটপুট দেখায়। আপনি যদি প্রোগ্রাম বন্ধ করে দেন, তবে সেই তথ্য হারিয়ে যায়।
* **logging:** আপনি চাইলে আউটপুট কনসোলে দেখাতে পারেন, আবার ফাইলে (.log file) সেভ করে রাখতে পারেন, এমনকি ইমেইল বা সার্ভারেও পাঠাতে পারেন।

---

### ৩. মেটাডেটা (Metadata)
`print()` শুধু আপনার দেওয়া মেসেজটি দেখায়। অন্যদিকে `logging` স্বয়ংক্রিয়ভাবে নিচের তথ্যগুলো যোগ করতে পারে:
* কত তারিখে এবং কয়টার সময় মেসেজটি জেনারেট হয়েছে।
* কোডটি কোন ফাইল বা কত নম্বর লাইনে আছে।
* কোন ফাংশন থেকে লগটি আসছে।

---

### কোড উদাহরণ

**Print এর ব্যবহার:**
```python
def add(a, b):
    print(f"Adding {a} and {b}") # সবসময় দেখাবে
    return a + b

add(5, 10)
```

**Logging এর ব্যবহার:**
```python
import logging

# কনফিগারেশন সেট করা
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def add(a, b):
    logging.info(f"Adding {a} and {b}") # এটি টাইমস্ট্যাম্পসহ দেখাবে
    return a + b

add(5, 10)
```

---

### একনজরে তুলনা

| বৈশিষ্ট্য | Print | Logging |
| :--- | :--- | :--- |
| **উদ্দেশ্য** | দ্রুত কিছু চেক করা বা আউটপুট দেখানো। | সিস্টেমের স্টেট মনিটর করা এবং ডিবাগিং। |
| **কন্ট্রোল** | আলাদা করে বন্ধ করা কঠিন (সব ডিলিট করতে হয়)। | একটি কোড চেঞ্জ করেই সব লগ বন্ধ বা চালু করা যায়। |
| **আউটপুট** | শুধু স্ট্যান্ডার্ড আউটপুট (টার্মিনাল)। | ফাইল, সকেট, ইমেইল, কনসোল ইত্যাদি। |
| **পারফরম্যান্স** | বড় অ্যাপ্লিকেশনে এটি স্লো হতে পারে। | অনেক বেশি অপ্টিমাইজড। |

### কখন কোনটি ব্যবহার করবেন?
* যখন ছোট কোনো স্ক্রিপ্ট লিখছেন বা খুব দ্রুত কিছু টেস্ট করতে চাচ্ছেন, তখন **print** ঠিক আছে।
* যখন কোনো বড় প্রজেক্ট বা এমন কোনো অ্যাপ্লিকেশন তৈরি করছেন যা দীর্ঘক্ষণ চলবে (যেমন: ওয়েব সার্ভার), তখন অবশ্যই **logging** ব্যবহার করা উচিত।

আপনি কি আপনার বর্তমানে করা কোনো প্রজেক্টে `logging` সেটআপ করার কথা ভাবছেন? ওহ, আর একটি কথা—প্রোডাকশনে কিন্তু `print` রাখা বেশ অপেশাদার কাজ হিসেবে ধরা হয়!

## Python Memory Management & Garbage Collection

---

## ১. Python Memory Management

---

### 🔑 Memory-তে কী হয়:

```
Python Memory
├── Stack Memory   → variables, function calls
├── Heap Memory    → actual objects
└── Memory Manager → সব control করে
```

---

### 🧠 Reference Counting — মূল mechanism:

> Python প্রতিটা object-এর জন্য একটা **counter** রাখে — কতজন সেই object-কে point করছে। Counter 0 হলে memory free।

```python
import sys

# Object তৈরি হলো — ref count = 1
account = {"name": "Sourov", "balance": 50000}
print(sys.getrefcount(account))   # 2 (account + getrefcount নিজে)

# আরেকটা reference — ref count = 2
backup = account
print(sys.getrefcount(account))   # 3

# Reference সরালে — ref count = 1
del backup
print(sys.getrefcount(account))   # 2

# সব reference গেলে — ref count = 0 → memory free
del account
# object automatically destroyed ✅
```

---

### 💻 Reference Counting — ধাপে ধাপে:

```python
# Step 1: Object তৈরি → count = 1
x = [1, 2, 3]          # ref count: 1

# Step 2: নতুন reference → count = 2
y = x                  # ref count: 2

# Step 3: Function-এ পাঠালে → count = 3
def show(data):
    print(data)        # ref count: 3 (inside function)
show(x)               # function শেষে → count: 2

# Step 4: List-এ রাখলে → count = 3
container = [x]        # ref count: 3

# Step 5: Delete করলে → count কমে
del y                  # ref count: 2
del container          # ref count: 1
del x                  # ref count: 0 → memory free! ✅
```

---

### 🏦 Memory-তে Object-এর Structure:

```
প্রতিটা Python object-এ থাকে:
┌─────────────────────────┐
│  ob_refcnt  (ref count) │ ← কতজন point করছে
│  ob_type    (type info) │ ← int/str/list?
│  ob_value   (actual data)│ ← আসল value
└─────────────────────────┘
```

---

### 💻 Python Memory Pool — Small Object Optimization:

```python
# Python ছোট integer (-5 থেকে 256) cache করে রাখে
a = 100
b = 100
print(a is b)    # True ← same object! (cached)

a = 1000
b = 1000
print(a is b)    # False ← আলাদা object (not cached)

# String interning — short strings cache হয়
s1 = "hello"
s2 = "hello"
print(s1 is s2)  # True ← same object

s1 = "hello world"
s2 = "hello world"
print(s1 is s2)  # False ← আলাদা (space আছে বলে)
```

> Python ছোট object বারবার তৈরি না করে **pool** থেকে দেয় — performance বাড়ে।

---

### 🔑 Memory-র তিনটা জায়গা:

```python
# ১. Stack — local variables
def process_payment(amount):
    tax = amount * 0.05        # Stack-এ
    total = amount + tax       # Stack-এ
    return total
# function শেষে Stack automatically clear ✅

# ২. Heap — objects
account = {                    # Heap-এ
    "name": "Sourov",
    "balance": 50000
}

# ৩. Global/Static — module level
MAX_TRANSFER_LIMIT = 500000    # Global memory-তে
```

---

## ২. Garbage Collection

---

### 🔑 কেন শুধু Reference Counting যথেষ্ট না:

```python
# ⚠️ Circular Reference — Reference Counting-এর দুর্বলতা
class Account:
    def __init__(self, name):
        self.name = name
        self.linked_account = None

acc1 = Account("Sourov")
acc2 = Account("Karim")

# Circular reference তৈরি করলাম
acc1.linked_account = acc2    # acc1 → acc2
acc2.linked_account = acc1    # acc2 → acc1

del acc1   # ref count = 1 (acc2 এখনো point করছে)
del acc2   # ref count = 1 (acc1 এখনো point করছে)

# দুটোরই ref count = 1, কিন্তু কেউ use করছে না!
# Reference Counting দিয়ে এটা free হবে না 😱
# Memory leak!
```

---

### 🔄 Python GC — Cyclic Garbage Collector:

```python
import gc

# GC manually চালানো
gc.collect()   # circular reference খুঁজে free করে

# GC info দেখা
print(gc.get_count())      # (generation 0, 1, 2) count
print(gc.get_threshold())  # (700, 10, 10) — default threshold
```

---

### 🧠 Generational GC — কীভাবে কাজ করে:

```
Python GC-তে ৩টা Generation আছে:

Generation 0 (নতুন objects)
├── সবচেয়ে বেশি check হয়
├── Threshold: 700 objects
└── বেশিরভাগ object এখানেই মরে

Generation 1 (কিছুদিনের পুরনো)
├── Gen 0 survive করলে আসে
├── Threshold: 10 collections
└── কম check হয়

Generation 2 (দীর্ঘস্থায়ী objects)
├── Gen 1 survive করলে আসে
├── সবচেয়ে কম check হয়
└── Global objects, module-level data
```

```
নতুন object তৈরি হলো
        ↓
  Generation 0
  (700 objects হলে GC চলে)
        ↓
   বেঁচে গেল?
   ↙        ↘
  না          হ্যাঁ
  ↓            ↓
Free       Generation 1
           (10 Gen0 collections হলে GC চলে)
                ↓
           বেঁচে গেল?
           ↙        ↘
          না          হ্যাঁ
          ↓            ↓
        Free       Generation 2
                   (দীর্ঘস্থায়ী objects)
```

---

### 💻 GC Generations — Code দিয়ে:

```python
import gc

# Threshold দেখো
print(gc.get_threshold())    # (700, 10, 10)
#                                ↑    ↑   ↑
#                              Gen0 Gen1 Gen2

# Threshold change করা
gc.set_threshold(1000, 15, 15)

# কোন generation-এ কতটা আছে
print(gc.get_count())        # (245, 3, 1)

# Manually collect করো
collected = gc.collect(0)    # শুধু Gen 0
collected = gc.collect(1)    # Gen 0 + 1
collected = gc.collect()     # সব generation
print(f"Collected: {collected} objects")
```

---

### 💻 Circular Reference — GC কীভাবে খোঁজে:

```python
import gc

class Transaction:
    def __init__(self, txn_id):
        self.txn_id = txn_id
        self.related = None

# Circular reference
t1 = Transaction("TXN-001")
t2 = Transaction("TXN-002")
t1.related = t2
t2.related = t1

# GC track করছে কিনা দেখো
print(gc.is_tracked(t1))   # True

del t1, t2

# GC manually চালাও
before = gc.get_count()
gc.collect()
after = gc.get_count()
print(f"Freed circular references ✅")
```

---

### 💻 `__del__` — Object destroy হওয়ার আগে:

```python
class DatabaseConnection:
    def __init__(self, url):
        self.url = url
        self.conn = connect(url)
        print(f"✅ Connected: {url}")

    def __del__(self):
        # Object destroy হওয়ার আগে call হয়
        if self.conn:
            self.conn.close()
        print(f"🔒 Connection closed: {self.url}")

conn = DatabaseConnection("postgresql://ucb_db")
del conn
# 🔒 Connection closed: postgresql://ucb_db ✅
```

> ⚠️ `__del__` depend করা risky — **context manager বেশি reliable।**

---

### 💻 `weakref` — Memory Leak এড়ানো:

```python
import weakref

class Account:
    def __init__(self, name):
        self.name = name

acc = Account("Sourov")

# Strong reference — ref count বাড়ে
strong_ref = acc        # ref count: 2

# Weak reference — ref count বাড়ে না
weak_ref = weakref.ref(acc)   # ref count: 2 (unchanged!)

print(weak_ref())       # <Account: Sourov> — access ✅

del acc
del strong_ref          # ref count: 0 → memory free

print(weak_ref())       # None — object gone ✅
# Circular reference হয় না ✅
```

---

### 🏦 Banking System-এ Memory Best Practices:

**১. Large data — Generator use করো:**
```python
# ❌ Bad — সব memory-তে
def get_all_transactions():
    return list(db.query("SELECT * FROM transactions"))
    # ১০ লাখ record → RAM crash 😱

# ✅ Good — একটা একটা করে
def get_all_transactions():
    for txn in db.query("SELECT * FROM transactions"):
        yield txn   # memory efficient ✅
```

**২. Connection — Context Manager দিয়ে:**
```python
# ✅ Context manager — leak হবে না
with db.get_connection() as conn:
    result = conn.execute(query)
# automatically closed, memory freed ✅
```

**৩. Cache — `__slots__` দিয়ে memory save:**
```python
# ❌ Normal class — প্রতিটা object-এ __dict__ থাকে
class Transaction:
    def __init__(self, id, amount, date):
        self.id = id
        self.amount = amount
        self.date = date

# ✅ __slots__ — __dict__ নেই, memory কম লাগে
class Transaction:
    __slots__ = ["id", "amount", "date"]  # fixed attributes

    def __init__(self, id, amount, date):
        self.id = id
        self.amount = amount
        self.date = date

# লাখ লাখ Transaction object-এ
# __slots__ দিয়ে ~40% memory save হয় ✅
```

**৪. GC disable — Performance critical section:**
```python
import gc

# Bulk processing-এর আগে GC pause করো
gc.disable()

try:
    # High-performance bulk transaction processing
    for txn in massive_transaction_batch:
        process(txn)
finally:
    gc.enable()
    gc.collect()   # শেষে একবারে clean ✅
```

---

### 📊 Memory Management Summary:

| Mechanism | কী করে | কখন চলে |
|---|---|---|
| **Reference Counting** | ref=0 হলে free করে | Real-time, সবসময় |
| **Cyclic GC** | Circular reference খোঁজে | Threshold-এ |
| **Memory Pool** | Small object cache করে | Automatically |
| **`__del__`** | Cleanup callback | Object destroy-এ |
| **`weakref`** | Ref count না বাড়িয়ে reference | Manually |
| **`__slots__`** | `__dict__` সরায় | Class definition-এ |

---

### 🎯 Interview Closing line:

> *"Python memory management দুটো layer-এ কাজ করে — Reference Counting real-time-এ object free করে, আর Cyclic GC circular reference handle করে। Banking system-এ লাখ লাখ transaction object তৈরি হয় — `__slots__` দিয়ে memory 40% কমানো যায়, Generator দিয়ে bulk data process করলে RAM-এ চাপ পড়ে না। Performance critical section-এ GC temporarily disable করলে throughput বাড়ে।"*

---

পরের গুরুত্বপূর্ণ topics:
- **SOLID Principles**
- **Django REST API + JWT**
- **Database ORM + Query Optimization**
- **Design Patterns — Singleton, Factory**

কোনটা নিয়ে আগাবে?


তোমার demo response একদম 🔥 — একই style maintain করে নিচে **interview-ready answers** দিলাম 👇

---

# 🧠 Lambda Function, Map, Filter, Reduce

---

## 🔑 Lambda Function কী

### এক কথায়:

> **Lambda function হলো ছোট, anonymous (নাম ছাড়া) function — এক লাইনে লেখা যায়**

---

### 🧾 Syntax:

```python
lambda arguments: expression
```

---

### 🧠 Example:

```python
# Normal function
def add(x, y):
    return x + y

# Lambda version
add = lambda x, y: x + y

print(add(2, 3))   # 5
```

---

### 🎯 কখন ব্যবহার করবো:

* ছোট function
* একবারই ব্যবহার হবে
* inline logic দরকার

---

### ⚠️ Limitations:

```
❌ multiple statements লেখা যায় না
❌ complex logic এর জন্য না
❌ readability খারাপ হতে পারে
```

---

### 🎯 Interview line:

> *"Lambda function is useful for short, one-time operations, especially when used with functions like map, filter, and reduce."*

---

# ⚙️ Map, Filter, Reduce

---

## 🧩 ১. map() — Apply function to all items

---

### 🔑 এক কথায়:

> **map() একটা function সব element-এর উপর apply করে**

---

### 🧠 Structure:

```python
map(function, iterable)
```

---

### 💻 Example:

```python
nums = [1, 2, 3, 4]

result = map(lambda x: x * 2, nums)
print(list(result))   # [2, 4, 6, 8]
```

---

### 📊 Visualization:

```
[1, 2, 3, 4]
   ↓ ×2
[2, 4, 6, 8]
```

---

### 🎯 Use case:

* transformation (data modify করা)

---

## 🧩 ২. filter() — Select condition-based items

---

### 🔑 এক কথায়:

> **filter() condition অনুযায়ী element select করে**

---

### 🧠 Structure:

```python
filter(function, iterable)
```

---

### 💻 Example:

```python
nums = [1, 2, 3, 4, 5, 6]

result = filter(lambda x: x % 2 == 0, nums)
print(list(result))   # [2, 4, 6]
```

---

### 📊 Visualization:

```
[1, 2, 3, 4, 5, 6]
   ↓ even?
[2, 4, 6]
```

---

### 🎯 Use case:

* filtering data (e.g. active users, valid transactions)

---

## 🧩 ৩. reduce() — Aggregate to single value

---

### 🔑 এক কথায়:

> **reduce() সব element combine করে একটা single value বানায়**

---

### 🧠 Import:

```python
from functools import reduce
```

---

### 💻 Example:

```python
from functools import reduce

nums = [1, 2, 3, 4]

result = reduce(lambda x, y: x + y, nums)
print(result)   # 10
```

---

### 📊 Visualization:

```
Step 1: 1 + 2 = 3
Step 2: 3 + 3 = 6
Step 3: 6 + 4 = 10
```

---

### 🎯 Use case:

* sum, product, aggregation

---

# ⚖️ Quick Comparison

| Function | কাজ       |
| -------- | --------- |
| map      | transform |
| filter   | select    |
| reduce   | aggregate |

---

# ⚡ List Comprehension

---

## 🔑 এক কথায়:

> **List comprehension হলো concise way to create list using a single line**

---

### 🧠 Syntax:

```python
[expression for item in iterable if condition]
```

---

### 💻 Example 1 — map এর alternative:

```python
nums = [1, 2, 3, 4]

result = [x * 2 for x in nums]
print(result)   # [2, 4, 6, 8]
```

---

### 💻 Example 2 — filter এর alternative:

```python
nums = [1, 2, 3, 4, 5, 6]

result = [x for x in nums if x % 2 == 0]
print(result)   # [2, 4, 6]
```

---

### 💻 Example 3 — combined:

```python
nums = [1, 2, 3, 4, 5]

result = [x * 2 for x in nums if x % 2 == 0]
print(result)   # [4, 8]
```

---

### 📊 Visualization:

```
[1,2,3,4,5]
 → even? → [2,4]
 → ×2    → [4,8]
```

---

### 🎯 কেন ব্যবহার করবো:

```
✅ readable (most cases)
✅ faster than map/filter (in many cases)
✅ pythonic way
```

---

# ⚠️ Common Mistake (Interview trap)

```python
# ❌ Over complex list comprehension
[x * 2 if x % 2 == 0 else x + 1 for x in nums if x > 10]
```

👉 বেশি complex হলে normal loop use করা better

---

# 🏦 Real Banking Example

```python
transactions = [100, -50, 200, -10, 500]

# শুধু credit (positive)
credits = list(filter(lambda x: x > 0, transactions))

# 10% tax apply
taxed = list(map(lambda x: x * 0.9, credits))

# total balance
from functools import reduce
total = reduce(lambda x, y: x + y, taxed)

print(total)
```

---

### ✅ Same using list comprehension:

```python
total = sum([x * 0.9 for x in transactions if x > 0])
```

---

# 🎯 Interview Closing Line

> *"Lambda, map, filter, and reduce are functional programming tools in Python. তবে production code-এ আমি সাধারণত list comprehension prefer করি readability এবং maintainability-এর জন্য. Reduce কম use করি, কারণ built-in functions like sum(), max() বেশি readable."*

---

## 🚀 Pro Tip (Important for UCB interview)

যদি interviewer জিজ্ঞেস করে:
👉 *“Which one do you prefer?”*

তুমি বলবে:

> *"For simple transformations and filtering, I prefer list comprehension. For aggregation, I use built-in functions like sum instead of reduce for better readability."*

---

চাও হলে আমি তোমার জন্য next topics দিতে পারি:

* Decorator (🔥 very important)
* Generator vs Iterator
* GIL (must for backend)
* Async vs Thread vs Process

বললেই same style-এ বানিয়ে দিব 🚀


তোমার আগের answer-এর মতো same **interview-ready structured style**-এ নিচে দিলাম 👇

---

# 🧠 Time Complexity কীভাবে measure করো

---

## 🔑 এক কথায়:

> **Time complexity measure করি input size (n) বাড়লে algorithm কত দ্রুত slow হয় সেটা দিয়ে (Big-O notation ব্যবহার করে)**

---

## 📊 Big-O Notation

| Complexity | Meaning            |
| ---------- | ------------------ |
| O(1)       | constant           |
| O(log n)   | logarithmic        |
| O(n)       | linear             |
| O(n log n) | efficient sort     |
| O(n²)      | slow (nested loop) |

---

## 🧠 Example:

```python
# O(n)
for i in range(n):
    print(i)

# O(n²)
for i in range(n):
    for j in range(n):
        print(i, j)
```

---

## 🔍 কীভাবে calculate করি (Step by Step)

---

### ১. Loop count করো

```python
for i in range(n):   # → O(n)
    pass
```

---

### ২. Nested loop দেখো

```python
for i in range(n):
    for j in range(n):
        pass
# → O(n * n) = O(n²)
```

---

### ৩. Ignore constants

```python
for i in range(n):
    pass

for i in range(n):
    pass

# → O(2n) = O(n)
```

---

### ৪. Worst case ধরো

```python
def search(arr, target):
    for x in arr:
        if x == target:
            return True
    return False

# Worst case → O(n)
```

---

## ⚡ Real Example (Banking)

```python
# transaction search
def find_txn(txns, txn_id):
    for txn in txns:
        if txn["id"] == txn_id:
            return txn
```

👉 যদি list use করো → **O(n)**
👉 যদি dict use করো → **O(1)** ✅

---

## 🎯 Interview Line

> *"I measure time complexity using Big-O notation by analyzing loops, nested operations, and worst-case scenarios. I always try to reduce O(n²) to O(n) or O(log n) using better data structures."*

---

# ⚡ Python Performance Optimize কীভাবে করো

---

## 🔑 এক কথায়:

> **Performance optimize করি — better algorithm + better data structure + profiling + async/concurrency দিয়ে**

---

# 🚀 ১. Right Data Structure ব্যবহার

---

### 🧠 Example:

```python
# ❌ slow (O(n))
if x in list_data:
    pass

# ✅ fast (O(1))
if x in set_data:
    pass
```

---

### 🎯 Key:

```text
list   → search O(n)
set    → search O(1)
dict   → lookup O(1)
```

---

# 🚀 ২. Avoid Nested Loop

---

```python
# ❌ O(n²)
for a in list1:
    for b in list2:
        if a == b:
            print(a)

# ✅ O(n)
set2 = set(list2)
for a in list1:
    if a in set2:
        print(a)
```

---

# 🚀 ৩. Built-in Function use করো

---

```python
# ❌ manual sum
total = 0
for x in nums:
    total += x

# ✅ optimized (C-level)
total = sum(nums)
```

---

# 🚀 ৪. List Comprehension > Loop

---

```python
# ❌
result = []
for x in nums:
    result.append(x * 2)

# ✅
result = [x * 2 for x in nums]
```

---

# 🚀 ৫. Generator ব্যবহার (memory efficient)

---

```python
# ❌ memory heavy
nums = [x * 2 for x in range(1000000)]

# ✅ generator
nums = (x * 2 for x in range(1000000))
```

---

# 🚀 ৬. Async Programming (I/O bound)

---

```python
# ❌ sync API call
requests.get(url)

# ✅ async
await aiohttp.get(url)
```

👉 Banking system-এ:

* payment API
* fraud check
* notification

সব parallel করা যায় ✅

---

# 🚀 ৭. Caching ব্যবহার

---

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_user(id):
    return db_call(id)
```

👉 repeated DB call avoid ✅

---

# 🚀 ৮. Profiling করো (real measurement)

---

```python
import time

start = time.time()

# code

print(time.time() - start)
```

---

👉 Advanced tools:

* cProfile
* line_profiler

---

# 🚀 ৯. Database Optimization (Very Important)

---

```python
# ❌ N+1 query problem
for user in users:
    get_orders(user.id)

# ✅ JOIN / prefetch
```

---

👉 Index ব্যবহার:

```sql
CREATE INDEX idx_user_email ON users(email);
```

---

# 🚀 ১০. GIL workaround (CPU bound)

---

```python
from multiprocessing import Pool
```

👉 CPU heavy হলে:

* threading ❌
* multiprocessing ✅

---

# 🏦 Real Banking Example

```python
# millions of transactions

# ❌ slow
for txn in txns:
    if txn["status"] == "SUCCESS":
        process(txn)

# ✅ optimized
success_txns = [t for t in txns if t["status"] == "SUCCESS"]
```

---

# ⚠️ Common Mistake (Interview Trap)

```python
# premature optimization ❌
```

👉 আগে measure করো → পরে optimize করো

---

# 🎯 Final Interview Closing Line

> *"I focus on optimizing performance by choosing the right data structures, reducing time complexity, and using Python built-ins. For I/O-heavy systems like banking APIs, I use async programming, and for CPU-heavy tasks, I use multiprocessing. I always rely on profiling before optimization."*

---

## 🚀 Pro Tip (UCB interview killer line)

👉 যদি জিজ্ঞেস করে:
**"Real life example?"**

তুমি বলবে:

> *"In a transaction system, instead of scanning a list (O(n)), I use a dictionary for O(1) lookup. Also, for multiple external API calls like payment verification, I use asyncio to reduce response time significantly."*

---

চাও হলে next topics:

* GIL deep dive (🔥 very important)
* Thread vs Async vs Process
* Django vs FastAPI performance
* Caching strategies (Redis)

বললেই same style-এ দেব 🚀


একই clean, interview-ready style-এ নিচে দিলাম 👇

---

# 🧠 Thread Safety কী?

---

## 🔑 এক কথায়:

> **Thread-safe মানে — multiple thread একসাথে run করলেও data corrupt হবে না, result consistent থাকবে**

---

## 🧠 সহজভাবে:

```
একই resource (variable / data) অনেক thread use করছে
→ কিন্তু কোনো conflict হচ্ছে না ✅
→ result সবসময় ঠিক আসছে ✅
```

---

## 💻 Example (Thread-safe না হলে সমস্যা):

```python
import threading

counter = 0

def increment():
    global counter
    for _ in range(100000):
        counter += 1

t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)

t1.start()
t2.start()

t1.join()
t2.join()

print(counter)   # Expected: 200000 ❌ (often wrong)
```

👉 এখানে problem হচ্ছে:

* `counter += 1` **atomic না**
* multiple thread একই সাথে modify করছে 😱

---

## 🔒 Thread-safe করার উপায় (Lock ব্যবহার)

```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100000):
        with lock:              # critical section
            counter += 1

t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)

t1.start()
t2.start()

t1.join()
t2.join()

print(counter)   # ✅ always correct
```

---

## 🧠 Key Concept:

```text
Critical Section → যেখানে shared resource modify হয়
Lock → এক সময়ে একটাই thread ঢুকতে পারবে
```

---

## 🎯 Interview Line:

> *"Thread safety ensures that shared data remains consistent when accessed by multiple threads. It is typically achieved using synchronization mechanisms like locks."*

---

# ⚠️ Race Condition কী?

---

## 🔑 এক কথায়:

> **Race condition তখন হয় যখন multiple thread একই data modify করতে গিয়ে unpredictable result দেয়**

---

## 🧠 সহজ analogy:

```
2 জন cashier একই account update করছে

Thread A → balance +100
Thread B → balance +200

দুজন একসাথে update করলে
→ final balance wrong হতে পারে 😱
```

---

## 💻 Real Example:

```python
balance = 100

def deposit_100():
    global balance
    temp = balance
    temp += 100
    balance = temp

def deposit_200():
    global balance
    temp = balance
    temp += 200
    balance = temp
```

👉 Expected:

```
100 + 100 + 200 = 400
```

👉 But possible result:

```
300 ❌
```

---

## 📊 Race Condition Flow:

```
Thread A: read balance = 100
Thread B: read balance = 100

Thread A: write 200
Thread B: write 300  ❌ (A-এর update overwrite)
```

---

## 🔥 Root Cause:

```text
Non-atomic operations
Shared mutable state
No synchronization
```

---

## 🔒 Solution:

```python
lock = threading.Lock()

def safe_deposit(amount):
    global balance
    with lock:
        balance += amount
```

---

## ⚡ Atomic vs Non-Atomic

```python
# ❌ Non-atomic
counter += 1

# Actually:
# 1. read
# 2. add
# 3. write
```

👉 এই ৩টা step-এর মাঝে context switch হলে race condition হয়

---

# 🏦 Real Banking Example

```python
# ❌ Race condition risk
withdraw(amount):
    if balance >= amount:
        balance -= amount
```

👉 Problem:

* 2টা withdrawal একসাথে হলে
* balance negative হতে পারে 😱

---

### ✅ Fix:

```python
with lock:
    if balance >= amount:
        balance -= amount
```

---

# ⚖️ Thread Safety vs Race Condition

| Topic          | Meaning                              |
| -------------- | ------------------------------------ |
| Thread Safety  | Safe execution with multiple threads |
| Race Condition | Unsafe execution → wrong result      |

---

# 🎯 Final Interview Closing Line

> *"Race condition occurs when multiple threads access shared data without proper synchronization, leading to inconsistent results. Thread safety is achieved by controlling access to critical sections using locks, semaphores, or other synchronization techniques."*

---

## 🚀 Pro Tip (Important)

👉 যদি interviewer জিজ্ঞেস করে:
**"Python-এ GIL থাকলে race condition হয়?"**

তুমি বলবে:

> *"Yes, GIL does not prevent race conditions. It only ensures one thread executes Python bytecode at a time, but operations like `counter += 1` are not atomic, so race conditions can still occur."*

---

চাও হলে next:

* GIL deep dive (🔥 must)
* Thread vs Async vs Multiprocessing
* Deadlock vs Starvation

বললেই next level prep করে দিব 🚀




তোমার style maintain করে **interview-ready Singleton pattern** নিচে দিলাম 👇

---

# 🧠 Singleton Pattern implement করো

---

## 🔑 এক কথায়:

> **Singleton pattern ensures — পুরো application-এ class-এর একটাই instance থাকবে**

---

## 🧠 কেন দরকার?

```text
✅ Database connection
✅ Logger
✅ Config manager
```

👉 multiple instance হলে:

* memory waste ❌
* inconsistent state ❌

---

# 🧩 Method 1 — `__new__` override (Most common)

---

### 💻 Implementation:

```python id="c6h0pw"
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


# Test
a = Singleton()
b = Singleton()

print(a is b)   # True ✅
```

---

### 🧠 কী হচ্ছে এখানে:

```text
__new__ → object create করার আগেই call হয়
একবার instance তৈরি হলে
→ পরেরবার same instance return করে
```

---

# 🧩 Method 2 — Class Method (Lazy Initialization)

---

```python id="c8qk5o"
class Singleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


# Test
a = Singleton.get_instance()
b = Singleton.get_instance()

print(a is b)   # True ✅
```

---

# 🧩 Method 3 — Decorator

---

```python id="7qk7fb"
def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


@singleton
class Database:
    pass


a = Database()
b = Database()

print(a is b)   # True ✅
```

---

# 🧩 Method 4 — Metaclass (Advanced 🔥)

---

```python id="ehjv1h"
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=SingletonMeta):
    pass


a = Logger()
b = Logger()

print(a is b)   # True ✅
```

---

# ⚠️ Thread-Safe Singleton (Important 🔥)

👉 Interview-এ এইটা বললে impression strong হবে

```python id="b0k8r2"
import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:   # critical section
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

---

### 🧠 কেন double check?

```text
First check → performance
Second check → correctness (race condition avoid)
```

---

# 🏦 Real Banking Example

```python id="df7h1r"
class DBConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating DB connection...")
            cls._instance = super().__new__(cls)
        return cls._instance


db1 = DBConnection()
db2 = DBConnection()

# Only one connection created ✅
```

---

# ⚠️ Common Mistake

```python id="7m3q2v"
# ❌ __init__ control না করলে
# multiple initialization হতে পারে
```

👉 Fix:

```python id="7tp9px"
def __init__(self):
    if hasattr(self, "_initialized"):
        return
    self._initialized = True
```

---

# ⚖️ Comparison

| Method       | Difficulty | Use case            |
| ------------ | ---------- | ------------------- |
| **new**      | Easy       | most common         |
| Class method | Easy       | controlled access   |
| Decorator    | Medium     | reusable            |
| Metaclass    | Hard       | advanced frameworks |

---

# 🎯 Interview Closing Line

> *"Singleton pattern ensures a single instance across the application. In Python, I typically implement it using `__new__` or a metaclass. For multithreaded environments like backend systems, I ensure thread safety using locks to prevent race conditions."*

---

## 🚀 Pro Tip (UCB interview killer)

👉 যদি interviewer জিজ্ঞেস করে:
**"Where have you used it?"**

তুমি বলবে:

> *"In backend systems, I use Singleton for database connections, configuration management, and logging to ensure consistent state and avoid unnecessary resource usage."*

---

চাও হলে next high-impact topics:

* Decorator (🔥 must)
* Context Manager
* Dependency Injection (very important for backend)
* Design patterns (Factory, Strategy)

বললেই next level prep 🚀
