import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from dotenv import load_dotenv
from typing import List, Optional
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Constants
TASK_FILE = "data/todo.json"
BACKUP_DIR = "data/backups"
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(os.path.dirname(TASK_FILE), exist_ok=True)

# Setup bot with required intents
intents = discord.Intents.default()
intents.message_content = True

class ToDoBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None,  # We'll implement a custom one
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="/help"
            )
        )
        self.todo_list: List[str] = []
        self.load_tasks()
        
    def load_tasks(self):
        """Load tasks from JSON file with error handling"""
        try:
            if os.path.exists(TASK_FILE):
                with open(TASK_FILE, "r") as f:
                    self.todo_list = json.load(f)
                    logger.info(f"Loaded {len(self.todo_list)} tasks from file")
            else:
                self.todo_list = []
                logger.info("No task file found, starting with empty list")
        except Exception as e:
            logger.error(f"Error loading tasks: {e}")
            self.todo_list = []
            
    def save_tasks(self):
        """Save tasks to JSON file with backup and error handling"""
        try:
            # Create backup before saving
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(BACKUP_DIR, f"todo_backup_{timestamp}.json")
            if os.path.exists(TASK_FILE):
                os.rename(TASK_FILE, backup_path)
                
            # Save current tasks
            with open(TASK_FILE, "w") as f:
                json.dump(self.todo_list, f, indent=2)
                
            logger.info(f"Saved {len(self.todo_list)} tasks to file")
        except Exception as e:
            logger.error(f"Error saving tasks: {e}")

bot = ToDoBot()

@bot.event
async def on_ready():
    """Called when the bot is ready and connected"""
    logger.info(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    logger.info(f'Connected to {len(bot.guilds)} guilds')
    
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} slash commands")
    except Exception as e:
        logger.error(f"Error syncing commands: {e}")

@bot.tree.command(name="add", description="Add a new task to your to-do list")
@app_commands.describe(task="The task you want to add")
async def add_task(interaction: discord.Interaction, task: str):
    """Add a task to the to-do list"""
    bot.todo_list.append(task)
    bot.save_tasks()
    
    embed = discord.Embed(
        title="✅ Task Added",
        description=task,
        color=discord.Color.green()
    )
    embed.set_footer(text=f"You now have {len(bot.todo_list)} tasks")
    
    await interaction.response.send_message(embed=embed)
    logger.info(f"User {interaction.user} added task: {task}")

@bot.tree.command(name="list", description="Show all tasks in your to-do list")
async def list_tasks(interaction: discord.Interaction):
    """List all tasks"""
    if not bot.todo_list:
        embed = discord.Embed(
            title="📭 Your To-Do List",
            description="Your to-do list is empty!",
            color=discord.Color.blue()
        )
    else:
        tasks = "\n".join([f"{i+1}. {t}" for i, t in enumerate(bot.todo_list)])
        embed = discord.Embed(
            title=f"📝 Your To-Do List ({len(bot.todo_list)} tasks)",
            description=tasks,
            color=discord.Color.blue()
        )
    
    await interaction.response.send_message(embed=embed)
    logger.info(f"User {interaction.user} viewed their task list")

@bot.tree.command(name="done", description="Mark a task as completed")
@app_commands.describe(task_number="The number of the task to complete")
async def complete_task(interaction: discord.Interaction, task_number: int):
    """Mark a task as completed"""
    if 0 < task_number <= len(bot.todo_list):
        task = bot.todo_list.pop(task_number - 1)
        bot.save_tasks()
        
        embed = discord.Embed(
            title="✅ Task Completed",
            description=task,
            color=discord.Color.green()
        )
        embed.set_footer(text=f"You have {len(bot.todo_list)} tasks remaining")
        
        await interaction.response.send_message(embed=embed)
        logger.info(f"User {interaction.user} completed task: {task}")
    else:
        embed = discord.Embed(
            title="❌ Error",
            description="Invalid task number. Use /list to see your tasks.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.warning(f"User {interaction.user} tried to complete invalid task #{task_number}")

@bot.tree.command(name="help", description="Show help information for the bot")
async def help_command(interaction: discord.Interaction):
    """Show help information"""
    embed = discord.Embed(
        title="📋 To-Do Bot Help",
        description="A simple bot to manage your to-do list",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="/add [task]",
        value="Add a new task to your list",
        inline=False
    )
    embed.add_field(
        name="/list",
        value="Show all your current tasks",
        inline=False
    )
    embed.add_field(
        name="/done [number]",
        value="Mark a task as completed",
        inline=False
    )
    embed.add_field(
        name="/help",
        value="Show this help message",
        inline=False
    )
    
    embed.set_footer(text="Made with ❤️ by your friendly neighborhood bot developer")
    
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors gracefully"""
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="❌ Command Not Found",
            description=f"Use `/help` to see available commands",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="❌ Missing Argument",
            description=str(error),
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        logger.error(f"Error in command {ctx.command}: {error}", exc_info=True)
        embed = discord.Embed(
            title="❌ Unexpected Error",
            description="An error occurred while processing your command.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

if __name__ == "__main__":
    try:
        bot.run(os.getenv("DISCORD_BOT_TOKEN"))
    except Exception as e:
        logger.critical(f"Bot crashed: {e}", exc_info=True)