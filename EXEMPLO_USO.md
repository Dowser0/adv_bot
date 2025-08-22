# Usage Example - Multiple Windows WoW Bot

## 🎯 Scenario: Multiple WoW Accounts

Imagine you have 3 World of Warcraft accounts running simultaneously for:
- **Account 1**: Farming resources
- **Account 2**: Crafting items
- **Account 3**: Doing quests

## 🚀 Step by Step

### 1. Preparation
```
1. Open World of Warcraft
2. Login to multiple accounts
3. Configure the '0' key for the desired ability in each account
4. Position windows so they don't overlap
```

### 2. Run the Bot
```bash
python adv_bot.py
```

### 3. Configure Windows (Option 1)
```
=== WOW WINDOWS FOUND (3) ===
1. World of Warcraft - Account1
2. World of Warcraft - Account2  
3. World of Warcraft - Account3

Options:
1. Select specific windows
2. Use all windows
3. Cancel

Choose an option (1-3): 2
All 3 windows selected!
```

### 4. Start Bot (Option 2)
```
=== WORLD OF WARCRAFT BOT - MULTIPLE WINDOWS ===
Using 3 WoW windows
Presses '0' every 2-12 seconds (random)
Press 'ESC' to stop the bot
Move mouse to upper left corner for emergency stop
Bot starting in 3 seconds...

Starting in 3...
Starting in 2...
Starting in 1...
Bot started! Switching between windows and pressing '0'...
```

### 5. Automatic Execution
```
Key '0' pressed in window 'World of Warcraft - Account1' at 14:30:15
Next action in 7.3 seconds

Key '0' pressed in window 'World of Warcraft - Account2' at 14:30:22
Next action in 4.1 seconds

Key '0' pressed in window 'World of Warcraft - Account3' at 14:30:26
Next action in 9.8 seconds

Key '0' pressed in window 'World of Warcraft - Account1' at 14:30:36
Next action in 3.2 seconds
```

## 🔄 How Window Switching Works

```
Window Cycle:
Account1 → Account2 → Account3 → Account1 → Account2 → Account3...

Time between actions: 2-12 seconds (random)
Total time per cycle: 6-36 seconds (variable)
```

## ⚙️ Recommended Settings

### For Intensive Farming
```
Base Interval: 1 second
Random Range: 0-3 seconds
Total: 1-4 seconds between actions
```

### For Crafting
```
Base Interval: 3 seconds  
Random Range: 0-5 seconds
Total: 3-8 seconds between actions
```

### For Quests
```
Base Interval: 5 seconds
Random Range: 0-10 seconds  
Total: 5-15 seconds between actions
```

## 🎮 Usage Examples

### Example 1: Specific Selection
```
Choose an option (1-3): 1

Enter the numbers of the windows you want to use (separated by comma):
Example: 1,3,5
Selection: 1,3

2 windows selected!
```

### Example 2: All Windows
```
Choose an option (1-3): 2
All 3 windows selected!
```

## 🛡️ Security Tips

1. **Don't run for too long** - Use larger intervals
2. **Monitor windows** - Make sure they don't freeze
3. **Use ESC to stop** - Always have total control
4. **Test first** - Use on secondary accounts
5. **Keep mouse visible** - For emergency stop

## 🔧 Customizations

### Change Base Interval
```
Choose an option (1-5): 3
Enter new base interval in seconds: 1.5
Base interval changed to 1.5 seconds
```

### Change Random Range  
```
Choose an option (1-5): 4
Enter new random range in seconds: 5
Random range changed to 5 seconds
```

## 📊 Monitoring

The bot shows:
- ✅ Which window is active
- ✅ Time of each action
- ✅ Next interval
- ✅ Execution status
- ✅ Window errors

## 🚨 Emergency Stop

- **ESC**: Stops the bot immediately
- **Mouse to upper left corner**: Stops the bot
- **Ctrl+C**: Interrupts the program
- **Alt+F4**: Closes the terminal

## 💡 Advanced Tips

1. **Use multiple monitors** for better organization
2. **Configure different keyboard shortcuts** for each account
3. **Monitor system performance** 
4. **Take regular breaks** to avoid detection
5. **Use during low traffic hours** on the server
