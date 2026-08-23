#!/usr/bin/env python3
"""Generate a seed dataset covering every table referenced in the SQL interview wiki."""
import random, datetime as dt

random.seed(20260822)
TODAY = dt.date(2026, 7, 26)

def q(v):
    if v is None: return "NULL"
    if isinstance(v, bool): return "1" if v else "0"
    if isinstance(v, (int, float)): return str(v)
    if isinstance(v, dt.datetime): return "'" + v.strftime("%Y-%m-%d %H:%M:%S") + "'"
    if isinstance(v, dt.date): return "'" + v.strftime("%Y-%m-%d") + "'"
    return "'" + str(v).replace("'", "''") + "'"

OUT = []
def ddl(s): OUT.append(s)
def insert(table, cols, rows):
    if not rows: return
    OUT.append(f"-- {len(rows)} rows into {table}")
    B = 200
    for i in range(0, len(rows), B):
        chunk = rows[i:i+B]
        vals = ",\n".join("  (" + ", ".join(q(v) for v in r) + ")" for r in chunk)
        OUT.append(f"INSERT INTO {table} ({', '.join(cols)}) VALUES\n{vals};")

# ---------------------------------------------------------------- dimensions
from vocab import *          # LOCALE=en swaps the whole vocabulary to English
cn_name = person

# ---------------------------------------------------------------- categories
ddl("""CREATE TABLE categories (
  category_id   INTEGER PRIMARY KEY,
  category_name VARCHAR(50) NOT NULL
);""")
insert("categories", ["category_id","category_name"], CATS)

# ---------------------------------------------------------------- departments
ddl("""CREATE TABLE departments (
  dept_id   INTEGER PRIMARY KEY,
  dept_name VARCHAR(50) NOT NULL
);""")
insert("departments", ["dept_id","dept_name"], DEPTS)

# ---------------------------------------------------------------- users
ddl("""CREATE TABLE users (
  user_id         INTEGER PRIMARY KEY,
  user_name       VARCHAR(50),
  username        VARCHAR(50),
  first_name      VARCHAR(30),
  last_name       VARCHAR(30),
  phone           VARCHAR(20),
  email           VARCHAR(120),
  age             INTEGER,
  birth_date      DATE,
  gender          VARCHAR(10),
  city            VARCHAR(30),
  province        VARCHAR(30),
  address         VARCHAR(200),
  status          VARCHAR(20),
  register_ip     VARCHAR(45),
  register_date   DATE,
  register_time   TIMESTAMP,
  last_login_time TIMESTAMP,
  last_order_time TIMESTAMP
);""")

N_USERS = 300
users = []
for uid in range(1, N_USERS+1):
    name = cn_name()
    city, prov = random.choice(CITIES)
    age = random.randint(18, 62)
    birth = dt.date(TODAY.year - age, random.randint(1,12), random.randint(1,28))
    prefix = random.choice(["138","139","150","186","199","135","137"])
    phone = prefix + "".join(random.choice("0123456789") for _ in range(8))
    domain = random.choice(["gmail.com","163.com","qq.com","outlook.com","company.cn","foxmail.net","example.org"])
    local = random.choice(["user","admin","test","shop","dev","data","hello"]) + str(random.randint(1,9999))
    email = f"{local}@{domain}"
    if random.random() < 0.04: email = email.upper()
    # seed duplicate registrations (case-varied) so de-dup questions return rows
    if uid in (11,12, 47,48, 93,94, 150,151, 202,203, 261,262):
        email = "dup_user%d@example.com" % (uid // 2)
        if uid % 2 == 0: email = email.upper()
    username = local if random.random() > 0.08 else "admin_" + local
    status = random.choices([USER_STATUS[0], USER_STATUS[1], None], weights=[88,9,3])[0]
    reg_date = TODAY - dt.timedelta(days=random.randint(1, 900))
    reg_time = dt.datetime.combine(reg_date, dt.time(random.randint(0,23), random.randint(0,59), random.randint(0,59)))
    reg_ip = None if random.random() < 0.12 else f"{random.choice([192,10,172,203])}.{random.choice([168,0,16,45])}.{random.randint(0,255)}.{random.randint(1,254)}"
    last_login = reg_time + dt.timedelta(days=random.randint(0, 400)) if random.random() > 0.1 else None
    if last_login and last_login.date() > TODAY: last_login = dt.datetime.combine(TODAY, dt.time(12,0))
    addr = f"{prov}-{city}-{random.choice(DISTRICTS)}"
    fn, ln = name.split(" ", 1) if " " in name else (name[0], name[1:])
    users.append([uid, name, username, fn, ln, phone, email, age, birth,
                  random.choices(GENDERS, weights=[52,48])[0], city, prov, addr,
                  status, reg_ip, reg_date, reg_time, last_login, None])
insert("users", ["user_id","user_name","username","first_name","last_name","phone","email","age",
                 "birth_date","gender","city","province","address","status","register_ip",
                 "register_date","register_time","last_login_time","last_order_time"], users)

# ---------------------------------------------------------------- products
ddl("""CREATE TABLE products (
  product_id     INTEGER PRIMARY KEY,
  product_name   VARCHAR(200),
  name           VARCHAR(200),
  price          DECIMAL(10,2),
  category_id    INTEGER,
  category_big   VARCHAR(50),
  category_small VARCHAR(50),
  stock          INTEGER
);""")
products = []
pid = 0
for cid, cname in CATS:
    for i in range(22):
        pid += 1
        base = random.choice(NOUN[cid])
        pname = random.choice(ADJ) + (" " if LOCALE == "en" else "") + base
        if random.random() < 0.22:   # long names, for the LENGTH() question
            pname = pname + (" (" if LOCALE=="en" else "（") + random.choice(LONG_SUFFIX) + (")" if LOCALE=="en" else "）")
        price = round(random.uniform(9.9, 4999), 2)
        if random.random() < 0.03: pname, price = (None, price)
        if random.random() < 0.03: price = None
        products.append([pid, pname, pname, price, cid, CAT_BIG[cid], cname, random.randint(0, 800)])
insert("products", ["product_id","product_name","name","price","category_id","category_big","category_small","stock"], products)
PRICE = {p[0]: (p[3] or 100) for p in products}
PCAT  = {p[0]: p[4] for p in products}
N_PROD = pid

# ---------------------------------------------------------------- orders
ddl("""CREATE TABLE orders (
  order_id       INTEGER PRIMARY KEY,
  user_id        INTEGER,
  product_id     INTEGER,
  category_id    INTEGER,
  amount         DECIMAL(10,2),
  quantity       INTEGER,
  status         VARCHAR(20),
  pay_status     VARCHAR(20),
  payment_method VARCHAR(20),
  coupon_id      INTEGER,
  province       VARCHAR(30),
  buyer_nick     VARCHAR(50),
  order_date     DATE,
  order_time     TIMESTAMP,
  pay_time       TIMESTAMP,
  create_time    TIMESTAMP
);""")
STATUS = ORDER_STATUS
orders = []
oid = 0
user_last_order = {}
for u in users:
    uid, uname, prov, reg = u[0], u[1], u[11], u[15]
    n = random.choices([0,1,2,3,5,8,14], weights=[12,22,20,16,14,10,6])[0]
    span = max((TODAY - reg).days, 1)
    for _ in range(n):
        oid += 1
        d = reg + dt.timedelta(days=random.randint(0, span))
        t = dt.datetime.combine(d, dt.time(random.choices(range(24), weights=[2,1,1,1,1,2,4,7,9,11,12,13,14,12,11,11,12,14,16,18,17,13,8,4])[0],
                                          random.randint(0,59), random.randint(0,59)))
        p = random.randint(1, N_PROD)
        qty = random.choices([1,2,3,5],[70,18,8,4])[0]
        amt = round(PRICE[p] * qty * random.uniform(0.75, 1.0), 2)
        st = random.choice(STATUS)
        paid = st in (ORDER_STATUS[0], ORDER_STATUS[-1]) or random.random() < 0.55
        pay_t = t + dt.timedelta(minutes=random.randint(1, 240)) if paid else None
        coupon = random.randint(1000,1099) if random.random() < 0.32 else None
        orders.append([oid, uid, p, PCAT[p], amt, qty, st,
                       PAID if paid else UNPAID,
                       random.choice(PAYM) if paid else None,
                       coupon, prov, uname, d, t, pay_t, t])
        if paid and st == ORDER_STATUS[0]:
            user_last_order[uid] = max(user_last_order.get(uid, t), t)
# a couple of obvious brushing/fraud users for the fraud-detection question
for uid in (7, 42):
    base = dt.datetime(2026, 6, 12, 3, 0, 0)
    for k in range(14):
        oid += 1
        orders.append([oid, uid, 5, PCAT[5], 99.00, 1, ORDER_STATUS[0], PAID, PAYM[0], None,
                       users[uid-1][11], users[uid-1][1],
                       base.date(), base + dt.timedelta(minutes=k*3),
                       base + dt.timedelta(minutes=k*3+1), base + dt.timedelta(minutes=k*3)])
insert("orders", ["order_id","user_id","product_id","category_id","amount","quantity","status",
                  "pay_status","payment_method","coupon_id","province","buyer_nick",
                  "order_date","order_time","pay_time","create_time"], orders)
N_ORD = oid

# ---------------------------------------------------------------- order_details / order_items
ddl("""CREATE TABLE order_details (
  id         INTEGER PRIMARY KEY,
  order_id   INTEGER,
  user_id    INTEGER,
  product_id INTEGER,
  category_id INTEGER,
  quantity   INTEGER,
  price      DECIMAL(10,2)
);""")
details, did = [], 0
for o in orders:
    for _ in range(random.choices([1,2,3],[62,26,12])[0]):
        did += 1
        p = random.randint(1, N_PROD)
        details.append([did, o[0], o[1], p, PCAT[p], random.randint(1,3), PRICE[p]])
# give user 1 a small, exact basket and hand user 2 & 3 the identical set,
# so the "bought exactly the same products" question returns rows
details = [d for d in details if d[2] not in (1, 2, 3)]
TWIN_BASKET = [4, 19, 55]
for uid in (1, 2, 3):
    for p in TWIN_BASKET:
        did += 1
        details.append([did, oid + uid, uid, p, PCAT[p], 1, PRICE[p]])
insert("order_details", ["id","order_id","user_id","product_id","category_id","quantity","price"], details)

ddl("""CREATE VIEW order_items AS
  SELECT order_id, product_id, quantity FROM order_details;""")

# ---------------------------------------------------------------- employees
ddl("""CREATE TABLE employees (
  emp_id      INTEGER PRIMARY KEY,
  name        VARCHAR(50),
  dept_id     INTEGER,
  department  VARCHAR(50),
  gender      VARCHAR(10),
  salary      DECIMAL(10,2),
  hire_date   DATE,
  manager_id  INTEGER,
  buyer_nick  VARCHAR(50)
);""")
emps = [[1, person(), 1, DEPTS[0][1], GENDERS[0], 60000, dt.date(2015,3,1), None, None]]
DNAME = dict(DEPTS)
for eid in range(2, 61):
    d = random.randint(1,6)
    if eid <= 7:
        mgr, sal = 1, random.choice([32000, 35000, 28000])
    else:
        mgr, sal = random.randint(2,7), random.choice([8000,8000,12000,12000,15000,15000,9500,18000,22000,11000,13500])
    emps.append([eid, cn_name(), d, DNAME[d],
                 random.choices(GENDERS,weights=[55,45])[0], sal,
                 TODAY - dt.timedelta(days=random.randint(30, 2600)), mgr, None])
insert("employees", ["emp_id","name","dept_id","department","gender","salary","hire_date","manager_id","buyer_nick"], emps)
ddl("CREATE VIEW employee AS SELECT emp_id, name, dept_id, salary, hire_date, manager_id FROM employees;")

# ---------------------------------------------------------------- students / scores / courses
ddl("""CREATE TABLE students (
  student_id INTEGER PRIMARY KEY,
  name       VARCHAR(50),
  class_id   INTEGER,
  score      DECIMAL(5,2)
);""")
studs, scores_rows, sel_rows = [], [], []
sid_c = 0
for sid in range(1, 121):
    cls = (sid - 1) // 20 + 1
    studs.append([sid, cn_name(), cls, round(random.uniform(35, 99), 1)])
    for c in random.sample(COURSES, random.randint(2, 5)):
        sc = round(random.gauss(66 if cls != 3 else 52, 16), 1)
        sc = max(0, min(100, sc))
        scores_rows.append([sid, c, sc])
        sel_rows.append([sid, c])
insert("students", ["student_id","name","class_id","score"], studs)

ddl("""CREATE TABLE scores (
  student_id INTEGER,
  course_id  VARCHAR(20),
  score      DECIMAL(5,2)
);""")
insert("scores", ["student_id","course_id","score"], scores_rows)
ddl("CREATE VIEW score AS SELECT s.student_id, st.class_id, s.score FROM scores s JOIN students st ON s.student_id = st.student_id;")

ddl("""CREATE TABLE course_selection (
  student_id INTEGER,
  course_id  VARCHAR(20)
);""")
insert("course_selection", ["student_id","course_id"], sel_rows)

# ---------------------------------------------------------------- shops / reviews
ddl("""CREATE TABLE shops (
  shop_id   INTEGER PRIMARY KEY,
  shop_name VARCHAR(100)
);""")
shops = [[i, f"{random.choice(SHOP_ADJ)} {random.choice(SHOP_KIND)} {i}"] for i in range(1, 21)]
insert("shops", ["shop_id","shop_name"], shops)

ddl("""CREATE TABLE reviews (
  review_id   INTEGER PRIMARY KEY,
  user_id     INTEGER,
  product_id  INTEGER,
  shop_id     INTEGER,
  rating      INTEGER,
  content     VARCHAR(500),
  review_time TIMESTAMP
);""")
rev, rid = [], 0
CLEAN_SHOPS = {17, 18, 19, 20}      # these never receive a rating below 3
for _ in range(1400):
    rid += 1
    shop = random.randint(1, 20)
    rating = random.choices([1,2,3,4,5],[6,8,17,32,37])[0]
    if shop in CLEAN_SHOPS: rating = max(rating, 3)
    rev.append([rid, random.randint(1, N_USERS), random.randint(1, N_PROD), shop, rating,
                random.choice(REVIEW_TEXT),
                dt.datetime.combine(TODAY - dt.timedelta(days=random.randint(0,500)), dt.time(random.randint(0,23), random.randint(0,59)))])
insert("reviews", ["review_id","user_id","product_id","shop_id","rating","content","review_time"], rev)
ddl("CREATE VIEW review AS SELECT review_id, user_id, product_id, rating FROM reviews;")

# ---------------------------------------------------------------- articles / comments / likes
ddl("""CREATE TABLE articles (
  article_id INTEGER PRIMARY KEY,
  title      VARCHAR(200),
  tags       VARCHAR(300)
);""")
arts = [[i, ARTICLE_FMT.format(random.choice(ARTICLE_TOPIC), i),
         ",".join(random.sample(TAGS, random.randint(1,4)))] for i in range(1, 41)]
insert("articles", ["article_id","title","tags"], arts)

ddl("""CREATE TABLE comments (
  comment_id   INTEGER PRIMARY KEY,
  article_id   INTEGER,
  user_id      INTEGER,
  content      TEXT,
  comment_time TIMESTAMP,
  created_at   TIMESTAMP
);""")
SHORT = COMMENT_SHORT
LONG_SEED = COMMENT_LONG
cmts, cid = [], 0
for _ in range(900):
    cid += 1
    long = random.random() < 0.22
    body = (LONG_SEED if long else random.choice(SHORT))
    t = dt.datetime.combine(TODAY - dt.timedelta(days=random.randint(0, 400)), dt.time(random.randint(0,23), random.randint(0,59)))
    cmts.append([cid, random.randint(1,40), random.randint(1, N_USERS), body, t, t])
insert("comments", ["comment_id","article_id","user_id","content","comment_time","created_at"], cmts)

ddl("""CREATE TABLE likes (
  like_id    INTEGER PRIMARY KEY,
  article_id INTEGER,
  user_id    INTEGER,
  like_time  TIMESTAMP
);""")
lk, lid = [], 0
for _ in range(2600):
    lid += 1
    lk.append([lid, random.randint(1,40), random.randint(1,N_USERS),
               dt.datetime.combine(TODAY - dt.timedelta(days=random.randint(0,400)), dt.time(random.randint(0,23), random.randint(0,59)))])
insert("likes", ["like_id","article_id","user_id","like_time"], lk)

# ---------------------------------------------------------------- logs
ddl("""CREATE TABLE access_log (
  log_id      INTEGER PRIMARY KEY,
  user_id     INTEGER,
  session_id  VARCHAR(40),
  ip          VARCHAR(45),
  page        VARCHAR(60),
  access_time TIMESTAMP
);""")
PAGES = ["/home","/search","/product","/cart","/checkout","/pay","/profile","/orders"]
al, alid = [], 0
for s in range(1, 501):
    uid = random.randint(1, N_USERS)
    sess = f"S{s:05d}"
    start = dt.datetime.combine(TODAY - dt.timedelta(days=random.randint(0,60)), dt.time(random.randint(8,23), random.randint(0,59)))
    ip_pfx = random.choices(["192.168","10.0","172.16","203.99"], weights=[55,20,15,10])[0]
    ip = f"{ip_pfx}.{random.randint(0,255)}.{random.randint(1,254)}"
    for k in range(random.randint(1, 7)):
        alid += 1
        al.append([alid, uid, sess, ip, random.choice(PAGES), start + dt.timedelta(minutes=k*random.randint(1,9))])
insert("access_log", ["log_id","user_id","session_id","ip","page","access_time"], al)

ddl("""CREATE TABLE visit_log (
  id         INTEGER PRIMARY KEY,
  user_id    INTEGER,
  visit_time TIMESTAMP
);""")
vl, vid = [], 0
for d in range(60):
    day = TODAY - dt.timedelta(days=d)
    for h in range(24):
        for _ in range(max(0, int(random.gauss(6 if 9 <= h <= 22 else 1, 3)))):
            vid += 1
            vl.append([vid, random.randint(1,N_USERS), dt.datetime.combine(day, dt.time(h, random.randint(0,59)))])
insert("visit_log", ["id","user_id","visit_time"], vl)

ddl("""CREATE TABLE login_logs (
  id         INTEGER PRIMARY KEY,
  user_id    INTEGER,
  login_date DATE,
  login_time TIMESTAMP
);""")
ll, llid = [], 0
for u in users:
    uid, reg = u[0], u[15]
    streak_user = uid % 17 == 0            # guarantee some long login streaks
    d = reg
    while d <= TODAY:
        if streak_user or random.random() < 0.10:
            llid += 1
            ll.append([llid, uid, d, dt.datetime.combine(d, dt.time(random.randint(6,23), random.randint(0,59)))])
        d += dt.timedelta(days=1 if streak_user else random.randint(1, 14))
insert("login_logs", ["id","user_id","login_date","login_time"], ll)

# ---------------------------------------------------------------- social graph
ddl("""CREATE TABLE follow (
  follower_id INTEGER,
  followee_id INTEGER
);""")
edges = set()
for _ in range(2200):
    a, b = random.randint(1,N_USERS), random.randint(1,N_USERS)
    if a != b: edges.add((a,b))
for a, b in list(edges):                     # make ~30% mutual
    if random.random() < 0.30: edges.add((b,a))
insert("follow", ["follower_id","followee_id"], sorted(edges))

# ---------------------------------------------------------------- sales / inventory
ddl("""CREATE TABLE sales (
  sale_id     INTEGER PRIMARY KEY,
  product_id  INTEGER,
  category_id INTEGER,
  salesperson VARCHAR(50),
  sale_date   DATE,
  amount      DECIMAL(10,2),
  quantity    INTEGER
);""")
SALESPEOPLE = [cn_name() for _ in range(12)]
sl, slid = [], 0
d = dt.date(2025,1,1)
while d <= TODAY:
    for _ in range(random.randint(2, 9)):
        slid += 1
        p = random.randint(1, N_PROD)
        qty = random.randint(1, 12)
        sl.append([slid, p, PCAT[p], random.choice(SALESPEOPLE), d, round(PRICE[p]*qty, 2), qty])
    d += dt.timedelta(days=1)
insert("sales", ["sale_id","product_id","category_id","salesperson","sale_date","amount","quantity"], sl)

ddl("""CREATE TABLE inventory (
  product_id     INTEGER,
  as_of_date     DATE,
  stock_quantity INTEGER
);""")
inv = []
d = dt.date(2026,1,1)
while d <= TODAY:
    for p in range(1, N_PROD+1, 3):
        inv.append([p, d, random.randint(0, 500)])
    d += dt.timedelta(days=7)
insert("inventory", ["product_id","as_of_date","stock_quantity"], inv)

ddl("""CREATE TABLE monthly_sales (
  year_month VARCHAR(7) PRIMARY KEY,
  sales      DECIMAL(12,2)
);""")
ms, base = [], 800000.0
for y in (2024, 2025, 2026):
    for m in range(1, 13):
        if y == 2026 and m > 7: break
        base *= random.uniform(0.94, 1.12)
        ms.append([f"{y}-{m:02d}", round(base, 2)])
insert("monthly_sales", ["year_month","sales"], ms)

# ---------------------------------------------------------------- returns
ddl("""CREATE TABLE returns (
  return_id   INTEGER PRIMARY KEY,
  order_id    INTEGER,
  return_time TIMESTAMP
);""")
rt, rtid = [], 0
for o in orders:
    if random.random() < 0.09:
        rtid += 1
        rt.append([rtid, o[0], o[13] + dt.timedelta(days=random.randint(1, 20))])
insert("returns", ["return_id","order_id","return_time"], rt)

# ---------------------------------------------------------------- funnel events
ddl("""CREATE TABLE events (
  event_id   INTEGER PRIMARY KEY,
  user_id    INTEGER,
  session_id VARCHAR(40),
  event_type VARCHAR(20),
  event_time TIMESTAMP
);""")
ev, evid = [], 0
FUNNEL = ["view","add_cart","order","pay"]
for s in range(1, 701):
    uid = random.randint(1, N_USERS)
    sess = f"E{s:05d}"
    t = dt.datetime.combine(TODAY - dt.timedelta(days=random.randint(0,90)), dt.time(random.randint(8,23), random.randint(0,59)))
    depth = random.choices([1,2,3,4],[36,28,20,16])[0]
    for k in range(depth):
        evid += 1
        ev.append([evid, uid, sess, FUNNEL[k], t + dt.timedelta(minutes=k*random.randint(1,12))])
insert("events", ["event_id","user_id","session_id","event_type","event_time"], ev)
ddl("CREATE VIEW user_events AS SELECT user_id, session_id, event_type, event_time FROM events;")

# ---------------------------------------------------------------- ads
ddl("""CREATE TABLE impressions (
  impression_id   INTEGER PRIMARY KEY,
  content_id      INTEGER,
  user_id         INTEGER,
  impression_time TIMESTAMP
);""")
ddl("""CREATE TABLE clicks (
  click_id   INTEGER PRIMARY KEY,
  content_id INTEGER,
  user_id    INTEGER,
  click_time TIMESTAMP
);""")
imps, clks, iid, ckid = [], [], 0, 0
for c in range(1, 26):
    ctr = random.uniform(0.01, 0.22)
    for _ in range(random.randint(200, 900)):
        iid += 1
        u = random.randint(1, N_USERS)
        t = dt.datetime.combine(TODAY - dt.timedelta(days=random.randint(0,30)), dt.time(random.randint(0,23), random.randint(0,59)))
        imps.append([iid, c, u, t])
        if random.random() < ctr:
            ckid += 1
            clks.append([ckid, c, u, t + dt.timedelta(seconds=random.randint(2, 90))])
insert("impressions", ["impression_id","content_id","user_id","impression_time"], imps)
insert("clicks", ["click_id","content_id","user_id","click_time"], clks)

# ---------------------------------------------------------------- misc small tables
ddl("""CREATE TABLE blacklist (
  user_id     INTEGER PRIMARY KEY,
  reason      VARCHAR(100),
  created_at  TIMESTAMP
);""")
insert("blacklist", ["user_id","reason","created_at"],
       [[u, random.choice(BLACKLIST_REASONS), dt.datetime(2026,3,random.randint(1,28),10,0)]
        for u in sorted(random.sample(range(1, N_USERS+1), 18))])

ddl("""CREATE TABLE event_participation (
  user_id  INTEGER,
  event_id VARCHAR(10)
);""")
ep = set()
for e in ("A","B","C"):
    for u in random.sample(range(1, N_USERS+1), random.randint(80, 150)):
        ep.add((u, e))
insert("event_participation", ["user_id","event_id"], sorted(ep))

ddl("""CREATE TABLE exp_users (
  user_id    INTEGER PRIMARY KEY,
  group_flag VARCHAR(10)
);""")
insert("exp_users", ["user_id","group_flag"],
       [[u, "test" if u % 2 == 0 else "control"] for u in range(1, N_USERS+1)])

ddl("""CREATE TABLE stock_price (
  trade_date  DATE PRIMARY KEY,
  close_price DECIMAL(10,2)
);""")
sp, px = [], 128.40
d = dt.date(2026,1,1)
while d <= TODAY:
    if d.weekday() < 5:
        px = max(5, px * random.uniform(0.965, 1.037))
        sp.append([d, round(px, 2)])
    d += dt.timedelta(days=1)
insert("stock_price", ["trade_date","close_price"], sp)

ddl("""CREATE TABLE transactions (
  trans_id   INTEGER PRIMARY KEY,
  user_id    INTEGER,
  trans_date DATE,
  amount     DECIMAL(10,2)
);""")
tx, txid = [], 0
d = dt.date(2025,6,1)
while d <= TODAY:
    for _ in range(random.randint(1,4)):
        txid += 1
        tx.append([txid, random.randint(1,N_USERS), d, round(random.uniform(20, 6000), 2)])
    d += dt.timedelta(days=1)
insert("transactions", ["trans_id","user_id","trans_date","amount"], tx)

ddl("""CREATE TABLE videos (
  video_id         INTEGER PRIMARY KEY,
  title            VARCHAR(200),
  duration_seconds INTEGER
);""")
insert("videos", ["video_id","title","duration_seconds"],
       [[i, VIDEO_TITLE.format(i), random.choice([95, 372, 1284, 3661, 5405, 7322, 640, 45])] for i in range(1, 31)])

ddl("""CREATE TABLE tickets (
  ticket_id  INTEGER PRIMARY KEY,
  user_id    INTEGER,
  subject    VARCHAR(200),
  created_at TIMESTAMP
);""")
tk = []
for i in range(1, 241):
    d = TODAY - dt.timedelta(days=random.randint(0, 180))
    tk.append([i, random.randint(1,N_USERS), random.choice(TICKET_SUBJECTS),
               dt.datetime.combine(d, dt.time(random.randint(0,23), random.randint(0,59)))])
insert("tickets", ["ticket_id","user_id","subject","created_at"], tk)

ddl("""CREATE TABLE websites (
  site_id INTEGER PRIMARY KEY,
  url     VARCHAR(500)
);""")
insert("websites", ["site_id","url"], [[i, u] for i, u in enumerate([
 "https://www.example.com/path/to/page","http://blog.example.org/2026/07/post",
 "https://docs.postgresql.org/18/index.html","https://www.github.com/anthropics",
 "http://shop.taobao.com/item?id=123","https://news.ycombinator.com/",
 "https://www.zhihu.com/question/12345","http://localhost:8080/admin",
 "https://sub.domain.example.co.uk/a/b","https://www.bilibili.com/video/BV1x"], 1)])

ddl("""CREATE TABLE user_address (
  user_id   INTEGER PRIMARY KEY,
  province  VARCHAR(30),
  city      VARCHAR(30),
  district  VARCHAR(30),
  detail    VARCHAR(200)
);""")
insert("user_address", ["user_id","province","city","district","detail"],
       [[u[0], u[11], u[10], random.choice(DISTRICTS), f"{random.randint(1,999)} {random.choice(STREETS)}"]
        for u in users])

ddl("""CREATE TABLE user_activity (
  user_id       INTEGER,
  activity_date DATE,
  active_month  VARCHAR(7)
);""")
ua = set()
for u in users:
    uid, reg = u[0], u[15]
    loyal = uid % 11 == 0                    # guarantee some 6+ month streaks
    d = reg
    while d <= TODAY:
        if loyal or random.random() < 0.16:
            ua.add((uid, d, d.strftime("%Y-%m")))
        d += dt.timedelta(days=random.randint(3, 20) if not loyal else 12)
insert("user_activity", ["user_id","activity_date","active_month"], sorted(ua))

# ---------------------------------------------------------------- BOM
ddl("""CREATE TABLE parts (
  part_id VARCHAR(30) PRIMARY KEY,
  cost    DECIMAL(10,2)
);""")
ddl("""CREATE TABLE bom (
  part_id      VARCHAR(30),
  component_id VARCHAR(30),
  quantity     INTEGER
);""")
insert("parts", ["part_id","cost"], [["Screw",0.35],["Board",42.00],["Chip",118.50],["Case",23.80],
                                     ["Cable",6.20],["Battery",65.00],["Lens",210.00],["Sensor",88.00]])
insert("bom", ["part_id","component_id","quantity"], [
  ["ProductX","ModuleA",2], ["ProductX","ModuleB",1], ["ProductX","Case",1],
  ["ModuleA","Board",1], ["ModuleA","Chip",2], ["ModuleA","Screw",8],
  ["ModuleB","Battery",1], ["ModuleB","Cable",3], ["ModuleB","Sensor",2],
  ["ProductY","ModuleA",1], ["ProductY","Lens",2],
])

# ---------------------------------------------------------------- year-split copies
ddl("CREATE VIEW sales_2025 AS SELECT sale_id AS order_id, amount FROM sales WHERE sale_date < '2026-01-01';")
ddl("CREATE VIEW sales_2026 AS SELECT sale_id AS order_id, amount FROM sales WHERE sale_date >= '2026-01-01';")
ddl("CREATE VIEW orders_2025 AS SELECT order_id, user_id, amount FROM orders WHERE order_date < '2026-01-01';")
ddl("CREATE VIEW orders_2026 AS SELECT order_id, user_id, amount FROM orders WHERE order_date >= '2026-01-01';")
ddl("CREATE VIEW users_v1 AS SELECT user_id, user_name AS name, phone, register_time AS create_time FROM users WHERE user_id <= 250;")
ddl("CREATE VIEW users_v2 AS SELECT user_id, user_name AS name, phone, register_time AS create_time FROM users WHERE user_id >= 100;")
ddl("CREATE VIEW logs AS SELECT log_id AS id, user_id, page AS action, access_time AS log_time FROM access_log;")
ddl("CREATE VIEW daily_sales AS SELECT sale_date, SUM(amount) AS amount FROM sales GROUP BY sale_date;")
ddl("CREATE VIEW sales_person AS SELECT ROW_NUMBER() OVER (ORDER BY salesperson) AS id, salesperson AS name, SUM(amount) AS total_sales FROM sales GROUP BY salesperson;")

# ---------------------------------------------------------------- backfill last_order_time
for uid, t in user_last_order.items():
    OUT.append(f"UPDATE users SET last_order_time = {q(t)} WHERE user_id = {uid};")

# ---------------------------------------------------------------- indexes
for stmt in [
  "CREATE INDEX idx_orders_user ON orders(user_id);",
  "CREATE INDEX idx_orders_time ON orders(order_time);",
  "CREATE INDEX idx_orders_status_amount ON orders(status, amount);",
  "CREATE INDEX idx_od_order ON order_details(order_id);",
  "CREATE INDEX idx_od_user_prod ON order_details(user_id, product_id);",
  "CREATE INDEX idx_login_user_date ON login_logs(user_id, login_date);",
  "CREATE INDEX idx_reviews_prod ON reviews(product_id, rating);",
  "CREATE INDEX idx_events_user_time ON events(user_id, event_time);",
  "CREATE INDEX idx_follow_pair ON follow(follower_id, followee_id);",
  "CREATE INDEX idx_sales_prod_date ON sales(product_id, sale_date);",
  "CREATE INDEX idx_users_prov_reg ON users(province, register_time);",
]:
    OUT.append(stmt)

header = f"""-- =====================================================================
--  SQL Interview Practice Database
--  Seed data for the 9-chapter SQL interview question set
--  Generated {dt.date.today()}  |  reference "today" = {TODAY}
--  {len(users)} users · {len(orders)} orders · {len(details)} order lines
--  {len(products)} products · {len(sl)} sales · {len(ll)} logins
-- =====================================================================
"""
open("out/schema.sql","w").write(header + "\n\n".join(OUT) + "\n")
print("wrote out/schema.sql")
print(f"users={len(users)} orders={len(orders)} details={len(details)} sales={len(sl)} logins={len(ll)} visits={len(vl)}")
