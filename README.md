# Image Extractor Unrestricted

When the rest of the fully automated image extractors fail! You try this hybrid approach! you open up a new tab for the image , you can do default 60 tabs and the bot will take care of saving it for you. Use other image extractors for sites that have bad devs lol! 

## Features
- Automatically processes 60+ tabs
- Downloads full-size images
- Auto-reconnects if Chrome disconnects
- Continuous batch processing
- Smart image URL detection
- Robust error handling

## Requirements
- Python 3.8 or higher
- Google Chrome browser
- Git installed
- Windows operating system

## Installation

### Step 1: Install Python
1. Go to https://www.python.org/downloads/
2. Download the latest Python 3.8+ version
3. Run the installer
4. **IMPORTANT:** Check the box that says "Add Python to PATH"
5. Click "Install Now"

### Step 2: Install Git
1. Go to https://git-scm.com/download/win
2. Download and install Git (default settings are fine)
3. Restart your computer

### Step 3: Clone This Repository
1. Open Command Prompt (press Windows key, type "cmd", press Enter)
2. Navigate to where you want to install (e.g., `cd C:\`)
3. Run:
   ```bash
   git clone https://github.com/augmentom/Image-Extractor-Unrestricted.git
   ```
4. Navigate into the folder:
   ```bash
   cd Image-Extractor-Unrestricted
   ```

### Step 4: Create Virtual Environment
1. In Command Prompt (inside the Image-Extractor-Unrestricted folder):
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   ```bash
   venv\Scripts\activate
   ```
   You should see `(venv)` at the beginning of your prompt

### Step 5: Install Requirements
1. With the virtual environment active, run:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Step 1: Start Chrome with Remote Debugging
1. Press **Windows key + R** (or click Start → Run)
2. Copy and paste this command:
   ```bash
   chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\chrome_dev"
   ```
3. Press Enter
4. Chrome will open with remote debugging enabled

**Note:** If you don't have a D: drive, don't worry! Chrome will create the folder automatically. You can also change `D:\chrome_dev` to any location you prefer, such as:
- `C:\chrome_dev` (if you want it on your C: drive)
- `%USERPROFILE%\chrome_dev` (puts it in your user folder)
- Any folder path where you have write permissions

### Step 2: Open Your Image Tabs
1. Chrome will open with remote debugging enabled
2. Open 60+ tabs with images you want to download
3. Keep the first tab as your main/gallery tab
4. All other tabs will be processed automatically

### Step 3: Run the Script
1. In Command Prompt (with venv active and in the Image-Extractor-Unrestricted folder):
   ```bash
   python imagesaveradvanced.py
   ```

### Step 4: Watch It Work
- The script will detect when you have 60+ tabs
- It will wait 3 seconds, then start processing
- Images will be saved to `D:\ImageSaver\full_images`
- After processing, it waits for the next batch of 60 tabs

## Configuration

### Change Where Images Are Saved
Edit this line in the script:
```python
SAVE_DIR = r"D:\ImageSaver\full_images"
```
Change `D:\ImageSaver\full_images` to your preferred folder.

### Change Batch Size
Edit this line:
```python
TARGET_TAB_COUNT = 60
```
Change `60` to your preferred number of tabs.

### Change Delay Before Processing
Edit this line:
```python
TRIGGER_DELAY = 3
```
Change `3` to the number of seconds to wait.

### Chrome Profile
The script uses a separate Chrome profile. The default location is `D:\chrome_dev`, but you can change this to any folder:
- `C:\chrome_dev` (for C: drive)
- `%USERPROFILE%\chrome_dev` (for your user folder)
- Any custom path where you have write permissions

This prevents conflicts with your regular Chrome browser.

## Troubleshooting

### "Connection failed" Error
- Make sure Chrome is running with `--remote-debugging-port=9222 --user-data-dir="D:\chrome_dev"`
- Close and restart Chrome with the debugging flag
- Check if another Chrome instance is running

### "InvalidSessionIdException" Error
- The script will automatically try to reconnect
- If it keeps failing, restart Chrome and the script
- Don't close Chrome while the script is running

### No Images Found
- Some websites don't have direct image links
- The script looks for the largest image on the page
- Try tabs with direct image pages when possible

### Chrome Path Issues
If `chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\chrome_dev"` doesn't work:
1. Press **Windows key + R**
2. Try the full path:
   ```bash
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="D:\chrome_dev"
   ```
3. If you don't have a D: drive, change `D:\chrome_dev` to `C:\chrome_dev` or any folder you want

### Virtual Environment Issues
- Make sure you see `(venv)` at the beginning of your Command Prompt
- If not, run `venv\Scripts\activate` again
- If venv folder doesn't exist, run `python -m venv venv` first

## Tips for Best Results
1. Use websites with direct image pages (not galleries with thumbnails)
2. Open tabs in batches of 60+ for efficient processing
3. Keep Chrome open - don't minimize it to tray
4. Monitor the console output for progress
5. Press Ctrl+C in the Command Prompt to stop the script
6. The `--user-data-dir` creates a separate Chrome profile that won't interfere with your regular Chrome
7. If you don't have a D: drive, Chrome will create the folder or you can specify a different path
8. You can run this Chrome alongside your regular Chrome browser

## How It Works
1. Connects to Chrome via remote debugging
2. Monitors the number of open tabs
3. When 60+ tabs are detected, waits 3 seconds
4. Processes each tab (except the first one)
5. Finds the largest image on each page
6. Downloads the image to your save folder
7. Closes processed tabs
8. Waits for the next batch

## License
MIT License - feel free to use and modify as needed.

## Support
If you encounter issues:
1. Check the troubleshooting section above
2. Make sure all requirements are installed
3. Verify Chrome is running with debugging enabled
4. Check that you have enough disk space
