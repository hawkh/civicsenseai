
from playwright.sync_api import sync_playwright, expect

def test_upload(page):
    print("Navigating to home...")
    # Try IPv6 loopback as curl showed it works
    page.goto("http://[::1]:5173/", timeout=60000, wait_until="domcontentloaded")

    # Wait for loading
    page.wait_for_timeout(2000)

    # Handle Auth
    if page.get_by_text("Secure Entry").is_visible():
        print("Logging in...")
        page.get_by_text("Secure Entry").click()
        page.wait_for_timeout(2000)

    print("Clicking Report button on Home Screen...")
    # The big button on Home Screen
    page.get_by_role("button", name="Report", exact=True).click()

    print("Waiting for Report Screen...")
    expect(page.get_by_text("Report Issue")).to_be_visible()

    print("Uploading file...")
    # Find input type=file
    with page.expect_file_chooser() as fc_info:
        page.get_by_text("Upload Photo").click()
    file_chooser = fc_info.value
    file_chooser.set_files("/home/jules/verification/test_image.png")

    print("Waiting for image to appear...")
    # The image appears in a div with an X button
    # There is an img tag with src starting with data:image
    expect(page.locator("img[alt='evidence']")).to_be_visible()

    print("Taking screenshot...")
    page.screenshot(path="/home/jules/verification/verification.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        # Grant permissions for geolocation as ReportScreen requests it
        context = browser.new_context(permissions=['geolocation'])
        page = context.new_page()
        try:
            test_upload(page)
            print("Verification successful!")
        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="/home/jules/verification/failure.png")
        finally:
            browser.close()
