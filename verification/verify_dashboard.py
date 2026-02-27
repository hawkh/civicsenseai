from playwright.sync_api import sync_playwright

def verify_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(60000)

        try:
            print("Navigating to app...")
            page.goto("http://localhost:5173", wait_until="networkidle")

            # Auth Screen
            print("Checking Auth Screen...")
            page.screenshot(path="verification/1_auth_screen.png")

            # Button text is "SECURE ENTRY" (case insensitive in get_by_text usually needs regex or exact match, but Playwright handles text well)
            # The code says: <span ...>Secure Entry</span>
            connect_btn = page.get_by_text("Secure Entry")
            if connect_btn.is_visible():
                print("Clicking Secure Entry...")
                connect_btn.click()
                # Wait for timeout in AuthScreen (1500ms) + buffer
                page.wait_for_timeout(3000)

            # Home Screen
            print("Checking Home Screen...")
            page.screenshot(path="verification/2_home_screen.png")

            # Dashboard
            # Sidebar nav item "My Dashboard"
            dashboard_btn = page.get_by_text("My Dashboard")
            if dashboard_btn.is_visible():
                 print("Clicking My Dashboard...")
                 dashboard_btn.click()
                 page.wait_for_timeout(2000)
            else:
                 print("Dashboard button not found on Home screen.")

            print("Checking Dashboard Screen...")
            page.screenshot(path="verification/3_dashboard_optimized.png")

            # Check if we see the Hub title
            if page.get_by_text("Hub").is_visible():
                print("SUCCESS: Dashboard loaded.")
            else:
                print("WARNING: Dashboard title 'Hub' not found.")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_dashboard()
