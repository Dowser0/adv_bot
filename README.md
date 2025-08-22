# World of Warcraft Bot - Multiple Windows

This is an intelligent Python bot that interacts with multiple World of Warcraft windows, automatically pressing the '0' key with **random intervals** and **switching between windows** for more natural behavior.

## ⚠️ IMPORTANT WARNING

**Use this bot at your own risk!** Using bots may violate WoW's Terms of Service and result in account ban. This project is for educational purposes only.

## 🔥 NEW FEATURES: Multiple Windows!

- ✅ **Automatic detection** of WoW windows
- ✅ **Selection of multiple windows** for the bot
- ✅ **Automatic switching** between selected windows
- ✅ **Configurable intervals** (default: 2 seconds)
- ✅ **Intelligent randomization** (0-10 additional seconds)
- ✅ **Dynamic total interval** (2-12 seconds variable)
- ✅ **More natural behavior** and less detectable

## 📋 Requirements

- Python 3.7 or higher
- Windows (tested on Windows 10)
- World of Warcraft installed
- Multiple WoW instances running (optional)

## 🚀 Installation

1. **Clone or download this project**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or use the automatic installer:
   ```bash
   install.bat
   ```

## 🎮 How to use

1. **Run the bot:**
   ```bash
   python adv_bot.py
   ```

2. **Choose an option:**
   - **Option 1**: Configure WoW windows
   - **Option 2**: Start bot
   - **Option 3**: Change base interval
   - **Option 4**: Change random range
   - **Option 5**: Exit

3. **Window configuration:**
   - The bot will automatically detect all WoW windows
   - You can select specific windows or use all of them
   - The bot will switch between selected windows

4. **Before starting:**
   - Open World of Warcraft (one or more instances)
   - Make sure the '0' key is configured for the desired ability
   - Configure windows using option 1

5. **Controls:**
   - **ESC**: Stop the bot
   - **Mouse to upper left corner**: Emergency stop
   - **Ctrl+C**: Interrupt the program

## 🔧 Features

- ✅ **Automatic detection** of WoW windows
- ✅ **Selection of multiple windows** for the bot
- ✅ **Automatic switching** between selected windows
- ✅ Automatically presses the '0' key
- ✅ **Configurable base interval** (default: 2 seconds)
- ✅ **Intelligent randomization** (0-10 additional seconds)
- ✅ **Dynamic total interval** (2-12 seconds variable)
- ✅ **More natural behavior** and less detectable
- ✅ Emergency stop with ESC
- ✅ User-friendly command line interface
- ✅ Activity logs with timestamp
- ✅ **Shows next interval** before each pause
- ✅ **Support for multiple instances** of WoW

## 🎲 How randomization works

```
Base Interval: 2 seconds
Random Range: 0-10 seconds
Total Interval: 2-12 seconds (variable)

Examples of possible intervals:
- 2.0 seconds (2 + 0)
- 5.3 seconds (2 + 3.3)
- 8.7 seconds (2 + 6.7)
- 12.0 seconds (2 + 10.0)
```

## 🔄 How window switching works

1. **Detection**: The bot automatically finds all WoW windows
2. **Selection**: You choose which windows to use
3. **Execution**: The bot switches between selected windows
4. **Action**: In each window, presses '0' and waits for interval
5. **Cycle**: Continues switching between windows indefinitely

## 🛡️ Security Features

- **FAILSAFE**: Move mouse to upper left corner to stop immediately
- **Pause between actions**: Prevents system overload
- **Key control**: Easy to stop with ESC
- **Randomization**: Less predictable behavior
- **Window validation**: Checks if windows still exist

## 📝 Customization

You can easily modify the code to:
- **Change base interval** (ex: 1 second, 3 seconds)
- **Modify random range** (ex: 0-5 seconds, 0-15 seconds)
- Press other keys
- Add more features
- Modify bot behavior
- **Configure switching patterns** between windows

## 🐛 Troubleshooting

**Problem**: Bot doesn't work
- **Solution**: Make sure WoW is running and dependencies are installed

**Problem**: Permission error
- **Solution**: Run PowerShell as administrator

**Problem**: Key not pressed
- **Solution**: Check if WoW is active and if the '0' key is configured

**Problem**: Intervals too long
- **Solution**: Use option 4 to reduce random range

**Problem**: No windows found
- **Solution**: Make sure WoW is running and windows are visible

**Problem**: Error switching windows
- **Solution**: Check if WoW windows are still open

## 📞 Support

This is an educational project. For questions or issues, consult the documentation of the libraries used:
- [pyautogui](https://pyautogui.readthedocs.io/)
- [keyboard](https://github.com/boppreh/keyboard)
- [pywin32](https://github.com/mhammond/pywin32)

## 📄 License

This project is open source and available for educational use. 