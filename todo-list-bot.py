import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv  # ✅ Added

load_dotenv()  # ✅ Load variables from .env

# Setup bot with message content intent
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# File to store tasks
TASK_FILE = "todo.json"

# Load tasks from file or start with an empty list
if os.path.exists(TASK_FILE):
    with open(TASK_FILE, "r") as f:
        todo_list = json.load(f)
else:
    todo_list = []

# Function to save tasks to file
def save_tasks():
    with open(TASK_FILE, "w") as f:
        json.dump(todo_list, f)

@bot.command()
async def add(ctx, *, task):
    todo_list.append(task)
    save_tasks()
    await ctx.send(f"✅ Task added: {task}")

@bot.command()
async def list(ctx):
    if not todo_list:
        await ctx.send("📭 Your to-do list is empty.")
    else:
        response = "\n".join([f"{i+1}. {t}" for i, t in enumerate(todo_list)])
        await ctx.send(f"📝 Your To-Do List:\n{response}")

@bot.command()
async def done(ctx, number: int):
    if 0 < number <= len(todo_list):
        task = todo_list.pop(number - 1)
        save_tasks()
        await ctx.send(f"✅ Completed: {task}")
    else:
        await ctx.send("❌ Invalid task number.")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
