SakuraBot
===

SakuraBot is a bot created for Discord Hackweek by famous1622 and SnowyTSW.

Features:

* Twitch Channel Follower Sync

* Kicking members from VC when they lose permissions to connect to it

* Private Channels from in chat

Commands:
* &settings
    * shows your current settings
    * use &help settings to get the commands to set these
    * booleans will toggle, strings and role names are set by placing their value afterwards

* &privatechan
    * Works with the Manage Channels permission, or a role called "PrivateChan"
    * &privatechan create (Users ...)
        * creates a private channel with only you, SakuraBot, and the users listed
    * &privatechan add [User]
        * adds a user to a private channel
    * &privatechan kick [user]
        * removes a user from a private channel
    * &privatechan close
        * deletes the private channel
    * &privatechan name [name]
        * renames the private channel
    * &privatechan desc [description]
        * changes the private channels description
    * &privatechan invitelink [maxuses (defaults to 1)]
        * generates an invite link to the server that gives access to the private channel

* &mytwitchis [accountname]
    * Temporary work around for giving Twitch followers a role. Could be removed if Discord had an endpoint for bots to get user profiles, or some other way of getting connected accounts without requiring the user to sign in to an application.

* &followerrefresh
    * refreshes twitch followers manually for a guild, otherwise it occurs when a user sets their username or every 5 minutes
    
To run it:
===

1. Rename SECRET.example.py to SECRET.py and put in the required information (Discord bot token and twitch client id)

2. Install the requirements.txt (preferably into a virtualenv) using pip

3. `python main.py`

4. ???

5. Profit.