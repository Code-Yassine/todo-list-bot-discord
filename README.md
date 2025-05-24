# 📝 Discord To-Do List Bot

A simple Discord bot to manage a shared to-do list using Python and the `discord.py` library.

## ⚙️ Features

### 📌 Core Functionality
- **Add tasks** with `/add <task>`
- **List all tasks** with `/list`
- **Complete tasks** with `/done <number>`
- **Persistent storage** (automatically saves to `todo.json`)
- **Data backups** (automatic daily backups)

### 🎨 Enhanced Experience
- Beautiful embed messages
- Task count tracking
- Error handling with helpful feedback
- Slash command support (modern Discord standard)

## 🚀 Setup

### 1. Clone the repo

```bash
git clone https://github.com/Code-Yassine/todo-list-bot-discord.git
cd todo-list-bot-discord
```

### 2.Install dependencies

```bash
pip install discord.py python-dotenv typing-extensions
```

### 3. Add your bot token securely
Create a file named .env in the project folder and add:
```bash
DISCORD_BOT_TOKEN=your_real_token_here
```

### 4. Run the bot
run the bot
```bash
python todo-list-bot.py
```
