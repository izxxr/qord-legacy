# qord
A high level library for building Discord bots.

**💡 Features:**

- Object Oriented interface for wrapping complex data models.
- User friendly, consistent and feature rich API design.
- Complete abstraction of all complex steps in building a bot.
- Robust handling and prevention of HTTPs ratelimits.

## 🏃 Quickstart
Here are the steps to get started with using Qord.

### 🔌 Installation
You can install Qord using the Python's favorite package manager, pip.
```sh
pip install qord
```

### 🎛️ Basic usage
Before building a complex bot with Qord, We have a quick example that provides basic overview of
the Qord's API by building a simple *"Ping Pong"* bot.

```py
import qord

client = qord.Client()

@client.listener(qord.GatewayEvents.MESSAGE_CREATE)
async def on_message_create(event):
  message = event.message
  
  if message.author.is_me():
    # Don't respond to ourselves.
    return
    
  if message.content == "!ping":
    await message.channel.send_message("🏓 Pong!")

if __name__ == "__main__":
  client.start(BOT_TOKEN)
```
