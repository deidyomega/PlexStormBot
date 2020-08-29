# Plexstorm ChatBot

## How to use:
1. Download the [plexbot.zip](https://github.com/deidyomega/PlexStormBot/releases/download/v0.2/plexbot.zip)
2. Unzip file somewhere
3. fill in settings.yml
4. Start app.exe
5. ??
6. Profit

### Feature Requests / Issues
Go here: https://github.com/deidyomega/PlexStormBot/issues

In the title please note if this is a feature request or a bug

Sample YML file:

    username: "bot@bot.com"
    password: "supersecretbotpassword"
    channel: "sexylady"

    # Commands can be single message, or if really long, multi line
    # Commands are execute by typing ! then command name --> !hello
    commands:
    - hello: "Hello"
    - info:
        - "This"
        - "is"
        - "3 messages posted at the same time"

    # The command MUST match the tipmenu item identically
    # This will fire off ONLY if someone tips, AND the tip
    # menu item matches the command name
    tip_commands:
        - "Boop!": "I was booped"

    # spin is SPECIAL, it randomly selects an item !spin to use
    spin:
        - "Remove Article of Clothing"
        - "Spanks x3"
        - "Spanks x5"
        - "Spanks x10"
        - "Dance"
        - "BJ"
        - "Better Luck Next Time!"
        - "Snapchat"
        - "Video (msg me in discord)"


# DEVELOPERS:
I would love help!

Install ==> pip install -r requirements.txt
Run ==> python app.py

Build from source:
* pyinstaller --onefile --paths venv\Lib\site-packages .\app.py

(note -> paths should include path to YOUR site-packages)
