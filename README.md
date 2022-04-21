# Quick Overview
<p>This bot is a Telegram Helper for the beauty shops.</p>
<p>It works with polling connections (simple repetitive HTTPS GET requests) to <strong>Telegram API Servers</strong> 
for receiving and sending <i>messages</i>. Firstly, <strong>bot</strong> asks a <strong>Telegram Server</strong> 
for updates, and if any new <i>messages</i> are there (i.e. <strong>user</strong> have sent a <i>message</i>
to bot via <strong>Telegram Server</strong>), <strong>bot</strong> retrieves <i>message</i> and processes it 
with Python. Then <strong>bot</strong> sends response <i>message</i> back to <strong>Telegram Server</strong>. 
Then <strong>Telegram Server</strong> sends this response message back to <strong>user</strong>.</p>
<p>Current configuration of the bot allows you to run it with Python command locally at your system, 
yet Internet connection is required to pass GET requests to Telegram Servers.</p>
<p>It is also possible to configure bot to use WebHooks (for vice-versa scenario where <strong>Telegram 
Server</strong> sends updates to <strong>bot</strong> without constant polling, 
and the <strong>bot</strong> simply listens for updates), but it only seems sensible at production version 
and at the stage of deployment.</p>
<p>Uses SQLAlchemy and PostgreSQL Database for CRUD operations.</p>
#Project files
<ul>
  <li>requirements.txt: </li>
  <li>settings.py: creates credentials and parameters for the bot. Create a .env file with your credentials
      and then pass them into this file.</li>
  <li>migrate.py : creates (or recreates if already exists) Database Tables. Be careful since it may 
      completely erase data!</li>
  <li>loader.py: creates a bot instance and its environment (like dispatcher, database cursor, in-memory storage)
      dialogs registry, filters and middlewares.</li>
  <li>bot.py: this file is the main file that initiates on-line connection to Telegram Servers, i.e. bot 
      is <strong>live!</strong></li>
</ul>
<ul>
  <li>filters: here you can create custom filters for incoming messages. Use filters as function decorator</li>
  <li>handlers: here you can create commands and functional words/scenarios for the bot</li>
  <li>keyboards: inline, menu (bottomed at dialog), dialog (dynamic keyboard). 
      Often used as user's shortcut for command</li>
  <li>middlewares: middlewares over requests and messages</li>
  <li>models: ORM tables for the database. Created with SQLAlchemy</li>
  <li>states: used to set in-memory state for the user and temporarily store data about user's messages</li>
</ul>
