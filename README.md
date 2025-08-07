# 🕷️ Web Parser with Selenium & BeautifulSoup

A simple website parser written in **Python**, using [**Selenium**](https://pypi.org/project/selenium/), [**BeautifulSoup**](https://pypi.org/project/beautifulsoup4/), [**Requests**](https://pypi.org/project/requests/), and [**webdriver-manager**](https://pypi.org/project/webdriver-manager/).

---

## 🚀 Installation & Usage

### 1. Clone the repository
```bash
git clone https://github.com/batya002/simon-parser.git
cd simon-parser
```

```bash
python -m venv venv
```

### for Linux / macOS
```bash
source venv/bin/activate
```

for Windows
```bash
venv\Scripts\activate
```

### Install dependencies
```bash
pip install selenium webdriver-manager beautifulsoup4 requests
```

### Run the script
```bash
python main.py
```

### 📦 Dependencies
selenium                # https://pypi.org/project/selenium/
webdriver-manager       # https://pypi.org/project/webdriver-manager/
beautifulsoup4          # https://pypi.org/project/beautifulsoup4/
requests                # https://pypi.org/project/requests/


### 📁 Project structure

simon-parser/
├── main.py          # Основной скрипт
├── README.md        # Документация
└── venv/            # Виртуальное окружение (не добавляй в git)
