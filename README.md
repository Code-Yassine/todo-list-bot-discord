# 📝 Discord To-Do List Bot

A simple Discord bot to manage a shared to-do list using Python and the `discord.py` library.

## ⚙️ Features

- `!add <task>` — Add a new task to the list
- `!list` — View the current to-do list
- `!done <task_number>` — Mark a task as completed (removes it)
- Tasks are saved to a file (`todo.json`) so they persist between restarts

## 🚀 Setup

### 1. Clone the repo

```bash
git clone https://github.com/Code-Yassine/todo-list-bot-discord.git
cd todo-list-bot-discord
```

### 2.Install dependencies

```bash
pip install discord.py python-dotenv
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
