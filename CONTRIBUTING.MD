# Contributing to Qord
As the library is currently under heavy development, Any kind of contribution made by you would be of great value.

By contributing, Not only do you support library but you also get shiny "Contributor" role in our Discord server that grants
you many perks across the server.

*Before you contribute, You should read this entire guide to get yourself familiar with the internal working of this library.*

## Usage
This library is fairly new and does not implement a feature rich API yet, So in order to get a simple bot running, you would have to do some
hacking with the internal components of the library. 

There is no front facing documentation for internal API but don't fret! You don't have to rely on reading the source code, 
Feel free to ping me (nerdguyahmad#3195) in our [Discord server](https://discord.gg/nE9cGtzayA) and ask me questions.

Before usage, Install this library using pip.
```
pip install -U qord
```

### Basic example
Here is a simple bot example:
```py
import qord
import logging

# I suggest enabling logging for better view of internal stuff
logging.basicConfig(level=logging.INFO) # Use logging.DEBUG for more secret stuff

client = qord.Client()

@client.event(qord.GatewayEvent.GATEWAY_DISPATCH)
async def on_gateway_dispatch(event):
  if event.title == "READY":
    user = event.data['user']
    print(f"Shard {event.shard.id} is ready as {user['username']}.")

client.start("BOT_TOKEN_HERE")
```
Keep reading further to understand above example.

Let's summarize the confusing parts:

- `client.event()` is used to register an event listener for a specific event.
- `qord.GatewayEvent` has the events names that you have to pass in `event()`.
- `GATEWAY_DISPATCH` event is called whenever *any* gateway event happens.
  - The `event` parameter is `events.GatewayDispatch` instance.
  - `event.title` is the name of event sent by Discord.
  - `event.data` is raw event data.
  - `event.shard` is the shard that had recieved the event.

### REST operations
REST operations are done using the `client._rest` attribute which is the instance of `RestClient` class. If you are aware of how discord.py REST operations
are done internally, then great. We have a similar fashion too.

We will extend the above example!

Let's first import the `Route` class that help us define a structure to specific endpoint.
```py
from qord.core.routes import Route
```

Now let us create a new `on_gateway_dispatch` event for messages handling. (You can do that in existing event too if you want).
```py
@client.event(qord.GatewayEvent.GATEWAY_DISPATCH)
async def on_gateway_dispatch(event):
  if event.title == "MESSAGE_CREATE":
    content = event.data['content']
    channel_id = event.data['channel_id']
    
    if content == "!ping":
      route = Route("POST", "/channels/{channel_id}", channel_id=channel_id)
      await client._rest.request(route, json={"content": "Pong!"})
```
Again, for summarizing the confusing aspects:

- We first got the message's content and the message's channel ID from `event.data`
- We checked if the content is `!ping`
- `Route` class allows us to define a specific endpoint from Discord REST API.
  - First parameter is the HTTP request method to perform on the route, `POST` in this case.
  - Second parameter is the actual route path, This is appended to `https://discord.com/api/v9`. In this case, It becomes `https://discord.com/api/v9/channels/{channel_id}`.
  - Keyword parameters are used for values for placeholders in the route's path. The placeholders will be used in future for ratelimit handling based on parameters passed.
  - You should not put the channel ID directly in path. Always use keyword parameters.
- `client._rest.request()` performs the actual HTTPs request on the route. `json` is the JSON body of the request.

Note that this might seem confusing at first sight but it's not, Feel free to ask your questions in the [Discord server](https://discord.gg/nE9cGtzayA).

### Gateway Events
As described before, gateway events are received and handled using the event mentioned and used above.

Finally, Consider reading [Discord Documentation](https://discord.dev) to get yourself more aware of how things are working underthehood. 

**References:**

- [Gateway Event Names](https://discord.dev/topics/gateway#commands-and-events)
- [Endpoint for sending messages](https://discord.dev/resources/channel#create-message)

## Contributions
You can contribute in three ways.

- Reporting bugs or suggesting features.
- Directly contributing to the codebase.
- Sending a "hi" in our [Discord server](https://discord.gg/nE9cGtzayA) :P

### Reporting bugs or suggesting features
You can report the bugs that you found and suggest more features by using [GitHub issues](https://github.com/nerdguyahmad/qord/issues). Simply create a new issue, Describe
your feature or bug and open the issue. Make sure to properly describe the bug. Again, if you are confused about your issue, Ask in the [Discord server](https://discord.gg/nE9cGtzayA)

### Directly contributing to the codebase
Use [GitHub pull request](https://github.com/nerdguyahmad/qord/pulls) for making code contributions. We assume you already know the basics about how pulls and forks
work on GitHub. However if this is your first time, don't fret! There are several articles online that explain it like 
[this one](https://www.dataschool.io/how-to-contribute-on-github/).

- Fork the repository.
- Make a new branch.
- Make the code changes.
- Open the pull request.

### Sending a "hi" in our Discord server.
Want to support this library and stay tuned about super secret updates? [Join the Discord server!](https://discord.gg/nE9cGtzayA). You should also ask your questions
about the library there.
