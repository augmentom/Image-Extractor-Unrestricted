# robust_batch.py
import os
import time
import requests
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

print("🛡️ ROBUST BATCH MODE")
print("Open 60+ tabs → I'll auto-process them!\n")

SAVE_DIR = r"D:\ImageSaver\full_images"
os.makedirs(SAVE_DIR, exist_ok=True)

TARGET_TAB_COUNT = 60
TRIGGER_DELAY = 3

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

def connect_to_chrome():
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("✅ Connected!")
        return driver
    except Exception as e:
        print("❌ Connection failed:", e)
        return None

driver = connect_to_chrome()
if not driver:
    exit()

processed_tabs = set()
saved_count = 0
batch_triggered = False
trigger_time = None

def is_image_url(url):
    if not url or not url.startswith("http"):
        return False
    clean = url.split('?')[0].split('#')[0].lower()
    return any(clean.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp'])

def find_full_image_url(page_url):
    try:
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")
            if href and is_image_url(href):
                return href
        imgs = driver.find_elements(By.TAG_NAME, "img")
        if imgs:
            def get_area(img):
                try:
                    return img.size['width'] * img.size['height']
                except:
                    return 0
            imgs.sort(key=get_area, reverse=True)
            src = imgs[0].get_attribute("src")
            if src:
                return urljoin(page_url, src)
    except:
        pass
    return None

def sanitize_filename(url):
    name = os.path.basename(urlparse(url).path)
    if not name or '.' not in name:
        name = f"image_{int(time.time() * 1000)}.jpg"
    return "".join(c for c in name if c.isalnum() or c in "._-")

def check_driver_connection():
    try:
        _ = driver.window_handles
        return True
    except:
        return False

try:
    while True:
        # Check if driver is still connected
        if not check_driver_connection():
            print("\n🔄 Lost connection to Chrome. Attempting to reconnect...")
            driver = connect_to_chrome()
            if not driver:
                print("❌ Failed to reconnect. Waiting 5 seconds...")
                time.sleep(5)
                continue
            processed_tabs.clear()  # Clear processed tabs since we have a new session
            batch_triggered = False
            trigger_time = None

        try:
            all_tabs = driver.window_handles
            if not all_tabs:
                time.sleep(1)
                continue

            # 🔑 ALWAYS treat the FIRST tab as the main/gallery tab
            main_window = all_tabs[0]
            detail_tabs = all_tabs[1:]  # everything else is a detail tab
            unprocessed_tabs = [t for t in detail_tabs if t not in processed_tabs]

            print(f"📊 Total tabs: {len(all_tabs)} | Detail tabs: {len(detail_tabs)} | Unprocessed: {len(unprocessed_tabs)}", end="\r")

            if not batch_triggered and len(unprocessed_tabs) >= TARGET_TAB_COUNT:
                batch_triggered = True
                trigger_time = time.time()
                print(f"\n🎯 {TARGET_TAB_COUNT}+ tabs detected! Waiting {TRIGGER_DELAY} sec...\n")

            if batch_triggered and time.time() - trigger_time >= TRIGGER_DELAY:
                print(f"\n🚀 Processing {len(unprocessed_tabs)} tabs...\n")
                tabs_to_process = unprocessed_tabs.copy()

                for tab in tabs_to_process:
                    # Check if driver is still connected before switching tabs
                    if not check_driver_connection():
                        print("\n⚠️ Driver disconnected during processing!")
                        break
                        
                    if tab not in driver.window_handles:
                        continue
                    try:
                        driver.switch_to.window(tab)
                        url = driver.current_url
                        full_url = find_full_image_url(url)
                        if full_url and is_image_url(full_url):
                            filename = sanitize_filename(full_url)
                            filepath = os.path.join(SAVE_DIR, filename)
                            resp = requests.get(full_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
                            with open(filepath, 'wb') as f:
                                f.write(resp.content)
                            saved_count += 1
                            print(f"✅ Saved: {filename}")
                        else:
                            print(f"⚠️ No image in: {url[:50]}")
                        processed_tabs.add(tab)
                    except Exception as e:
                        print(f"💥 Error: {str(e)[:70]}")
                    finally:
                        try:
                            # Only close if it's not the main window
                            if tab != main_window:
                                driver.close()
                        except:
                            pass

                    # Return to main tab
                    try:
                        if main_window in driver.window_handles:
                            driver.switch_to.window(main_window)
                    except:
                        pass

                print(f"\n📦 Batch done! Total saved: {saved_count}\n")
                print("🔄 Waiting for next batch of 60 tabs...")
                
                # Reset batch trigger but keep processed_tabs set
                batch_triggered = False
                trigger_time = None
                
                # Clean up processed_tabs by removing closed tabs
                try:
                    current_tabs = set(driver.window_handles)
                    processed_tabs.intersection_update(current_tabs)
                except:
                    processed_tabs.clear()

        except Exception as e:
            print(f"\n💥 Error in main loop: {str(e)[:70]}")
            print("🔄 Attempting to continue...")
            time.sleep(2)

        time.sleep(0.5)

except KeyboardInterrupt:
    print(f"\n🛑 Final count: {saved_count} images saved.")