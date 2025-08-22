# WoW Bot - Graphical User Interface

A modern, user-friendly graphical interface for the World of Warcraft Multiple Windows Bot.

## 🎨 **Features**

### **Modern Design**
- ✅ Clean, professional interface
- ✅ Color-coded status indicators
- ✅ Responsive layout
- ✅ Professional styling

### **Real-time Monitoring**
- ✅ Live status updates
- ✅ Current window display
- ✅ Next action countdown
- ✅ Progress bar visualization
- ✅ Real-time activity log

### **Easy Configuration**
- ✅ One-click window detection
- ✅ Visual window selection
- ✅ Instant interval adjustment
- ✅ Apply settings with one click

### **Advanced Controls**
- ✅ Start/Stop buttons
- ✅ Emergency stop
- ✅ Progress tracking
- ✅ Log management

## 🚀 **Installation**

### **Option 1: Automatic Installer**
```bash
install_gui.bat
```

### **Option 2: Manual Installation**
```bash
pip install -r requirements.txt
```

## 🎮 **How to Use**

### **1. Launch the GUI**
```bash
python adv_bot_gui.py
```

### **2. Configure Windows**
- Click **"Detect Windows"** to find WoW instances
- Click **"Select All"** to use all windows
- Or manually select specific windows

### **3. Adjust Settings**
- Set **Base Interval** (default: 2 seconds)
- Set **Random Range** (default: 0-10 seconds)
- Click **"Apply"** to save changes

### **4. Start the Bot**
- Click **"Start Bot"** to begin
- Monitor progress in real-time
- Use **"Stop Bot"** to stop safely

## 🖥️ **Interface Sections**

### **Status Section**
- **Bot Status**: Shows if bot is running/stopped
- **Windows**: Number of detected WoW windows
- **Selected**: Number of windows selected for bot
- **Current**: Currently active window
- **Next Action**: Time until next action

### **Configuration Section**
- **WoW Windows List**: Shows all detected windows
- **Window Controls**: Detect, Select All, Clear Selection
- **Interval Settings**: Base interval and random range
- **Apply Button**: Save configuration changes

### **Control Section**
- **Start Bot**: Begin bot operation
- **Stop Bot**: Safely stop bot
- **Emergency Stop**: Immediate stop
- **Progress Bar**: Visual countdown to next action

### **Activity Log**
- **Real-time Log**: Live activity feed
- **Color-coded Messages**: Different colors for different message types
- **Log Controls**: Clear log, save log to file
- **Timestamp**: Every message includes time

### **Information Section**
- **Controls**: Keyboard shortcuts and emergency procedures
- **Disclaimer**: Educational use warning

## 🎯 **Color Coding**

### **Message Types**
- **INFO**: Black - General information
- **SUCCESS**: Green - Successful actions
- **WARNING**: Orange - Warnings and stops
- **ERROR**: Red - Errors and issues

### **Status Colors**
- **Running**: Green - Bot is active
- **Stopped**: Red - Bot is inactive
- **Progress**: Blue - Countdown progress

## 🔧 **Advanced Features**

### **Multi-threading**
- Bot runs in separate thread
- GUI remains responsive
- Safe start/stop operations

### **Window Management**
- Automatic window detection
- Smart window switching
- Error handling for closed windows

### **Progress Tracking**
- Visual progress bar
- Real-time countdown
- Smooth animations

### **Log Management**
- Persistent logging
- Export to file
- Clear log option

## 🚨 **Safety Features**

### **Emergency Controls**
- **ESC Key**: Stop bot immediately
- **Emergency Stop Button**: GUI emergency stop
- **Mouse to Corner**: pyautogui failsafe
- **Window Close Protection**: Prevents accidental closure

### **Validation**
- Input validation for intervals
- Window existence checking
- Error handling and recovery

## 📱 **System Requirements**

- **OS**: Windows 10/11
- **Python**: 3.7 or higher
- **Memory**: 100MB RAM
- **Display**: 800x600 minimum resolution

## 🎮 **Recommended Usage**

### **For Beginners**
1. Use default settings
2. Select all detected windows
3. Start with longer intervals
4. Monitor the log for activity

### **For Advanced Users**
1. Customize intervals for your needs
2. Select specific windows
3. Use shorter intervals for farming
4. Monitor system performance

### **For Multiple Accounts**
1. Open multiple WoW instances
2. Detect all windows
3. Select all or specific ones
4. Start bot and monitor

## 🔍 **Troubleshooting**

### **Common Issues**

**Problem**: GUI doesn't start
- **Solution**: Check Python installation and dependencies

**Problem**: No windows detected
- **Solution**: Make sure WoW is running and visible

**Problem**: Bot won't start
- **Solution**: Select windows first, check intervals

**Problem**: GUI freezes
- **Solution**: Use emergency stop, restart application

### **Performance Tips**
- Close unnecessary applications
- Use reasonable intervals
- Monitor system resources
- Take regular breaks

## 📊 **Monitoring**

### **Real-time Information**
- Bot status and activity
- Window switching progress
- Action timing and intervals
- Error messages and warnings

### **Log Analysis**
- Activity patterns
- Error frequency
- Performance metrics
- Usage statistics

## 🎨 **Customization**

### **Visual Options**
- Window size and layout
- Color schemes
- Font sizes
- Button styles

### **Functional Options**
- Default intervals
- Auto-start settings
- Log retention
- Export formats

## 🚀 **Getting Started**

1. **Install Dependencies**: Run `install_gui.bat`
2. **Launch GUI**: Run `python adv_bot_gui.py`
3. **Detect Windows**: Click "Detect Windows"
4. **Select Windows**: Choose which windows to use
5. **Adjust Settings**: Set your preferred intervals
6. **Start Bot**: Click "Start Bot"
7. **Monitor**: Watch the real-time activity
8. **Stop**: Use "Stop Bot" when done

## ⚠️ **Important Notes**

- **Educational Use Only**: This is for learning purposes
- **Use at Own Risk**: May violate WoW Terms of Service
- **Test First**: Try on secondary accounts
- **Monitor Performance**: Watch for system issues
- **Take Breaks**: Don't run continuously

## 🎯 **Perfect For**

- **Multi-account players**
- **Resource farming**
- **Crafting automation**
- **Quest completion**
- **Learning automation**
- **Testing purposes**

The GUI makes the WoW bot much easier to use while providing professional monitoring and control features! 🎮✨

