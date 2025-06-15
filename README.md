# 📱 TikTok Session ID Checker

A fast, multi-threaded Python tool to check TikTok `sessionid` cookies and sort them into valid, banned, bad, or error lists.

---

## ⚡️ Features

✅ Multi-threaded for speed  
✅ Simple input: just a file with session IDs  
✅ Auto-saves results to organized files:  
- `Valids.txt`  
- `MightBeBanned.txt`  
- `Bads.txt`  
- `toCheckAgain[Error].txt`  
✅ Live progress with colorful output

---

## 📂 Input File Format

Each line must contain **one TikTok session ID**:

```
ba189c0cf73f2a80d61eea2c72ceff81
7b487de5ef4c09335533999473cadb5b
fb7997272b49f667bd1952ebf8c68063
...
```

---

## 🚀 How to Use

### 1️⃣ Clone the repo

```bash
git clone https://github.com/YOUR-USERNAME/tiktok-session-checker.git
cd tiktok-session-checker
```

---

### 2️⃣ Install dependencies

```bash
pip install httpx colorama
```

---

### 3️⃣ Prepare your session ID file

Put your session IDs in `sessions.txt` (one per line).

---

### 4️⃣ Run the checker

```bash
python checker.py
```

When prompted:

```
Enter accounts file path [e.g., sessions.txt]:
```

Type your file name (e.g., `sessions.txt`) and press Enter.

---

## 📄 Output Files

| File | Description |
|------|--------------|
| `Valids.txt` | Valid session IDs with usernames |
| `MightBeBanned.txt` | Session IDs that might be banned |
| `Bads.txt` | Invalid or expired session IDs |
| `toCheckAgain[Error].txt` | Session IDs with request errors |

---

## ⚙️ Configuration

Default threads: **10**  
Change it in the script if needed:

```python
checker = TikTokChecker(file_path=path, threads=10)
```

---

## 🛠️ Requirements

- Python 3.8+
- `httpx`
- `colorama`

Install them with:

```bash
pip install -r requirements.txt
```

*(create `requirements.txt` with `httpx` and `colorama`)*

---

## ⚖️ Disclaimer

This tool is for **educational purposes only**.  
Use responsibly and comply with TikTok’s Terms of Service.

---

## ⭐️ License

MIT License — see `LICENSE`.

---

## 📣 Author

Made with ❤️ by @DudeGeorges

---
