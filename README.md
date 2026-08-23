# SQL Interview Playground · SQL 面试题练习台

---

## Download · 下载

| File | |
|---|---|
| **[`sql-practice-en.html`](sql-practice-en.html)** | English |
| **[`sql-practice-zh.html`](sql-practice-zh.html)** | 中文版  |

> **If progress doesn't save**, your browser is blocking `localStorage` on `file://` URLs —
> the page shows a red banner when this happens. Serve it locally instead:
> ```bash
> python3 -m http.server 8000
> # then open http://localhost:8000/sql-practice-en.html
> ```

---

## What it does

**177 questions across 9 chapters** — filtering, aggregation, joins and set operations,
subqueries and CTEs, window functions, date/string functions, business analytics,
performance tuning, and cross-database differences.

**Problems are posed, not answered.** Each one gives you the table schema, a few rows of sample
input and a few rows of sample output — never the SQL. Sample inputs are trimmed to the columns
that actually appear in the output, so wide tables stay readable.

**Answers are graded on data, not text.** Write your query, hit *Check answer*, and your result
set is compared against the reference. All of these pass:

- rows in a different order
- columns in a different order
- different column names (alias however you like)
- `12000` / `12000.0` / `'12000'` — numeric forms are unified, tolerance `1e-6`

Two independent checks must both pass: the multiset of row signatures, and the multiset of
per-column value vectors. The second exists so that swapping values *between* two columns inside
a row can't slip past the first.

**Every submission is logged** with its timestamp and verdict, and failures record *why*
(wrong column count, wrong row count, which rows disagree).

**A contents heatmap** shows all 177 problems at a glance:

| | |
|---|---|
| 🟢 green | right on the first submission, no hint |
| 🟡 yellow | right, but after a hint or earlier wrong attempts |
| 🔴 red | submitted, not yet right |
| ⚪ grey | not attempted |

Any status can be overridden by hand. Star problems for review, write notes on them, filter by
any of it. Everything is saved to `localStorage` and survives closing the tab; export/import
moves it as JSON.

Of the 177: **146 are auto-graded**, 11 are demos (`EXPLAIN` plans — no single correct result
set), and 20 are discussion questions with no SQL to write.

---

## The dataset

38 tables and 14 views of a self-consistent e-commerce world:

```
users → orders → order_details
employees · departments · students · scores · course_selection
products · categories · reviews · shops
login_logs · visit_log · access_log · events · follow
sales · inventory · returns · impressions · clicks
stock_price · transactions · bom / parts · articles · comments · likes
```

It is **deliberately seeded** so the awkward questions actually return rows: real login streaks,
users active 6+ consecutive months, duplicate email registrations, shops that never received a
bad review, and two planted order-brushing accounts (14 identical-amount orders inside one hour).

The English and Chinese datasets are generated from the same script with different vocabulary,
so `status` is `'Completed'` in one and `'已完成'` in the other. **The reference answers differ
accordingly** — don't mix a query from one version with the other's database.

### Using it in a real database

```bash
# PostgreSQL
psql -U postgres -d yourdb -f data/en/schema-postgres.sql

# SQLite — or just open the prebuilt file
sqlite3 mydb.db < data/en/schema-sqlite.sql
sqlite3 data/en/practice.db
```

Swap `en` for `zh` for the Chinese dataset.

### Regenerating it

```bash
cd tools
LOCALE=en python3 gen.py      # writes out/schema.sql
LOCALE=zh python3 gen.py
```

`vocab.py` holds the per-locale vocabulary; `gen.py` holds the structure and the seeding logic.
Change the seed or the row counts to get a different world.

---

## Notes

- The playground runs **SQLite**, so reference solutions use SQLite dialect (`strftime` rather
  than `DATE_FORMAT`, and so on). The cross-database differences are themselves chapter IX.
- Grading judges output, so a query that is *logically* looser can still pass when it happens to
  produce the same rows — on question I.1, `amount > 50` yields the same top 10 as `amount > 100`.
- The questions come from a widely circulated SQL interview collection. The **dataset, grading
  engine, and interface here are original work**; the question wording has been rewritten for
  the English edition.

## License

[MIT](LICENSE) for the code, dataset and interface.
