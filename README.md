# 🤖 ID-Collector Bot

A high-performance, asynchronous Telegram bot designed for developers and power users to retrieve unique identifiers (IDs) and comprehensive metadata from various Telegram objects.

---

## 📌 Purpose

The bot automates the process of extracting:

- **Unique File IDs** for photos, videos, stickers, and documents.
- **Chat & User IDs** for personal accounts, groups, and channels.
- **Detailed Metadata:** Dimensions, duration, file size, coordinates, and contact details.
- **Contextual Info:** Extracts IDs from replied messages.

---

## 🛠 Available Commands

- `/start` — Initialize the bot and select interface language (EN/RU).
- `/help` — Show usage instructions and features.
- `/myid` — Display your personal ID and current chat identifiers.
- `/chatid` — Get detailed info about the current group or channel.
- `/id` — (Reply required) Get full metadata of the replied message.

> **Note:** Any media sent directly to the bot will be processed automatically.

---

## 🚀 Installation & Setup

### 1. Prerequisites

Ensure you have **Python 3.11+** installed. We recommend using **uv** for lightning-fast dependency management.

### 2. Install `uv` (Package Manager)

Choose the command for your operating system:

**Windows (PowerShell):**
powershell

```
powershell -c "ir | iex" (irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1))
```

Linux & macOS (Terminal):
Bash

```
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```

Using pip (Cross-platform):
Bash

```
pip install uv
```

3. Configuration

Clone the repository and create a .env file in the root directory:
Фрагмент кода

```
TG_TOKEN=your_bot_token_here
USE_PROXY=False
PROXY_URL=socks5://user:pass@host:port
```

4. Install Dependencies

Use uv to install all required packages (including aiogram, aiosqlite, and requests for external API calls):
Bash

# Syncing dependencies from requirements.txt

```
uv pip install -r requirements.txt
```

# Or manual installation of core requirements

```
uv pip install aiogram aiosqlite python-dotenv requests
```

5. Launch the Bot
   Bash

# Recommended way using uv

```
uv run run.py
```

# Or using standard python

```
python run.py
```
