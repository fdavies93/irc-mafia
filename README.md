# IRC Mafia / Werewolf: Code Plan

## ToDo

* Stage 1: Basics
  * Create SQL database
    * Decide on tables to use and how we want to log data
    * Decide on fields to use in tables
	* Think about the ways in which we want to be able to look at the data in considering the above
  * Create core of IRC bot
    * Connecting to IRC server
    * Staying connected (responding to ping requests)
    * Processing commands differently to normal chat
    * Basic state machine to run Mafia game (I'll explain this on Monday; resource linked below)
	* Framework for different player types (i.e. Police / Mafia / Townsperson)
    * Connecting to SQL server
* Stage 2: Mafia
  * Making gameplay
    * Probably best if we start with Mafia and extend it to Werewolf. Mafia is a much simpler game, and once that's implemented it should be fairly easy to extend it to Werewolf, provided the Architect does their job well.
    * Also designing commands for the IRC bot.
	* And designing the different types of people.
	* And designing gameplay flow in general.
  * Interfacing
    * Uploading chat logs to the SQL server
	* Making sure communication from the bot to players is smooth
	* Wrapping the commands to and from the server in a way which works well for gameplay coders
  * Making SQL queries
    * This is up to the database operator! Consider what kind of data might be interesting to look at from the chat logs.
* Stage 3: Werewolf / Extension
  * Too early to plan this out in detail: we might not even get there! Take everything in this section as a suggestion.
  * Persistant users -- user stats.
  * Adding more roles and a new gameplay mode in the form of Werewolf.
  * Gameplay extensions could include more 'characters'.
  
## Roles

* *Software Architect (1 person, probably me (Frank)):* Writes and decides on the high-level structure of the code; vets new submissions to the repository to make sure they work with existing code. Needs to have some understanding of all areas of the code.
* *Gameplay coder (1+ people ):* Involves designing commands and states for the bot. Needs to be familiar with Python. Probably the role with the most scope for multiple coders without 'spoiling the broth'.
* *Interface coder (1+ people):* Writing the code to allow the Python bot, the SQL server, and the IRC chat to interface with one another. Needs to know basic Python and basic SQL but doesn't need to be extremely good at either. Should work closely with (or be the) Software Architect to make sure the interface code is convenient for the Gameplay coders to work with.
* *Database operator (1+ people):* Writing SQL queries to interrogate data from the chat logs in interesting ways. Also probably in charge of the design of the database tables. Needs to become the most familiar with SQL and databases.

**EVERYONE WORKING IN PYTHON NEEDS TO LEARN A LITTLE BIT ABOUT IRC COMMANDS AS WELL AS THEIR SPECIALISATION!**
  
## Resources

* [IRC Bot Tutorial](http://wiki.shellium.org/w/Writing_an_IRC_bot_in_Python)
* [State Machine: Wikipedia](https://en.wikipedia.org/wiki/Finite-state_machine)
* [W3Schools SQL Tutorial](http://www.w3schools.com/sql/)
* [Basic IRC tutorial] (http://www.irchelp.org/irchelp/irctutorial.html)
* [Another IRC tutorial] (https://www.hackthissite.org/pages/irc/reference.php) 

## Database Layout

(I'll leave this open to interpretation by the database people, but I think it's probably most useful if we just scoop everything users say and process it later. A rough idea of fields is below.)

### Chat Log

* ID (indexing)
* Username
* Message content
* Timestamp
* Whether it's a command or not (this can be done by SQL query too, but it's probably more trouble than it's worth to write a query when it's easier just to do it with the bot)

### Game Log

* ID (indexing)
* Username
* Timestamp
* Action (i.e. this table logs game commands)
* Role