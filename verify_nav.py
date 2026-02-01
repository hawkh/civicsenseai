import os
import time
from playwright.sync_api import sync_playwright, expect

def verify_nav():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Set viewport to desktop to see sidebar
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        try:
            # Navigate to home
            print("Navigating to http://localhost:5173/")
            page.goto("http://localhost:5173/", timeout=60000)

            # Wait for authentication or home screen
            print("Checking for Auth Screen...")
            page.wait_for_selector("text=CIVIC SENSE", timeout=10000)

            # Perform Login
            print("Logging in...")
            page.get_by_role("button", name="Secure Entry").click()

            # Wait for Home Screen (which has the sidebar)
            print("Waiting for Home Screen...")
            page.wait_for_selector("text=New Report", timeout=10000)

            # Verify Sidebar Nav Items
            print("Verifying Nav Items...")
            expect(page.get_by_text("New Report")).to_be_visible()
            expect(page.get_by_text("My Dashboard")).to_be_visible()
            expect(page.get_by_text("Digital ID")).to_be_visible()

            # Click "My Dashboard"
            print("Navigating to Dashboard...")
            page.get_by_text("My Dashboard").click()

            # Verify Dashboard loaded
            # DashboardScreen has "Hub" and "Active Stream"
            print("Verifying Dashboard...")
            expect(page.get_by_text("Active Stream")).to_be_visible()

            # Wait for CSS transitions (300ms)
            print("Waiting for transitions...")
            time.sleep(1.0)

            # Screenshot
            os.makedirs("/home/jules/verification", exist_ok=True)
            screenshot_path = "/home/jules/verification/nav_verification_delayed.png"
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")

        except Exception as e:
            print(f"Error: {e}")
            try:
                os.makedirs("/home/jules/verification", exist_ok=True)
                page.screenshot(path="/home/jules/verification/error.png")
            except:
                pass
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    verify_nav()
