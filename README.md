
# 🧠 Short-Circuit Boolean Expression Analyzer

A Python + Streamlit web app to **analyze boolean expressions** and visualize their **short-circuit evaluation behavior**. It determines which variables are actually *evaluated* during execution based on Python's short-circuiting rules for logical operators (`and`, `or`, `not`), and generates **minimal test cases** for functional validation.

---

## 🔍 Features

* **Analyze any boolean expression** with Python-style syntax and single-letter variables (`a`, `b`, etc.).
* Track **which variables are short-circuited** (not evaluated).
* Display a table of all **unique evaluation patterns**.
* Generate a minimal set of test cases (`n+1` for `n` variables) covering all logical branches.
* Interactive and intuitive **Streamlit UI**.
* Supports error detection for invalid syntax.

---

## 📦 Project Structure

```
short-circuit-analyzer/
├── app.py                 # Main Streamlit app
├── requirements.txt       # Required dependencies
└── README.md              # Project overview
```

---

## 🧪 How It Works

### 1. **Input**

Users enter a boolean expression (e.g., `(a or b) and c`), using:

* Operators: `and`, `or`, `not`
* Single-letter variable names

---

### 2. **Transformation**

The code uses regex to replace variables like `a`, `b`, `c` with calls to a `track()` function:

```python
a or b  -->  track('a') or track('b')
```

This tracks which variables are *actually evaluated* when short-circuiting occurs.

---

### 3. **Evaluation**

* All `2^n` combinations of variable truth values (`T`, `F`) are tested.
* The `track()` function logs whether each variable was used.
* If short-circuiting skips a variable, it is marked `_`.

A result row like:

```
['T', '_', 'F'] → a was True, b not evaluated, c was False
```

---

### 4. **Display**

* All unique evaluation patterns shown in a DataFrame (`T`, `F`, `_`)
* Styled using `pandas` and `streamlit`.

---

### 5. **Minimal Test Case Selection**

* Picks a minimal subset (`n+1`) of patterns that:

  * Cover **both True and False** evaluations for each variable.
  * Cover **both final outcomes** (`True`, `False`) of the expression.
* Useful for **unit test generation** or **logic verification**.

---

## 📊 Example

Input:

```
((a or b) and c) or d
```

Output:

| a   | b  | c  | d  | Result |
| --- | -- | -- | -- | ------ |
| \_  | T  | T  | \_ | T      |
| F   | F  | \_ | F  | F      |
| F   | \_ | F  | T  | T      |
| ... |    |    |    |        |

---

## 🔧 Requirements

* Python 3.8+
* Streamlit
* Pandas

Install with:

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the App

```bash
streamlit run app.py
```

---

## 📂 Sample `requirements.txt`

```
streamlit
pandas
```

---

## ✅ Use Cases

* Boolean logic education
* Unit test generation
* Compiler or interpreter design
* Digital logic circuit testing
* QA automation (minimal logical test coverage)


