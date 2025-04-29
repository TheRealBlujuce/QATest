import time
from playwright.sync_api import sync_playwright

def run_test():
    with sync_playwright() as p:
        # Launch browser and create a new page
        browser = p.chromium.launch(headless=False)  # Set headless=True for headless mode
        page = browser.new_page()

        # --- Step 1: Sign Up ---
        page.goto('https://familytools.app/sign_in')
        page.fill('input[name="Email"]', 'willmarda@outlook.com')
        page.fill('input[name="Password"]', 'IcuI4cu4Fam!')
        page.click('button:text("Sign In")')
        page.screenshot(path='signin_success.png')  # Take screenshot after sign up

        # --- Step 2: Add a Calendar Event ---
        page.click('a:has-text("Calendar")')

        # --- Ensure we are in the correct month (April) ---
        # Check if the calendar is showing the correct month, and if not, change it
        current_month = page.locator('text=April')  # Adjust the text to match current UI's month element
        if current_month.is_visible():
            page.click('text=Next Month')  # Click "Next Month" to move to April if it's stuck in March

        # Create a new event

        page.click('text=Add Event')
        page.fill('input[name="Name"]', 'Test Event')
        page.fill('input[name="Location/Note"]', 'Home')  # Adjust date as necessary
        page.click('text=Assign To')
        page.click('text=Willem')
        page.click('button:text("Add")')

        # Wait for event to appear on the calendar
        page.wait_for_selector('text=Test Event')
        page.screenshot(path='event_created.png')

        # --- Step 3: Drag-and-Drop Event in Month View ---
        event = page.locator('text=Test Event')
        target_day = page.locator('text=27')  # Choose another day to drag event

        print("Added Test Event!")

        # Perform drag-and-drop
        event.drag_to(target_day)  # Perform drag-and-drop
        page.screenshot(path='event_dragged.png')

        print("Done Dragging Test Event!")
        
        # --- Step 4: Move Event by 3 Hours in Day View ---
        # Click the dropdown to open view options
        button = page.locator('button:has(span.block.truncate:text("Month View"))')

        # Debugging: Check if button is clickable
        if button.is_visible() and button.is_enabled():
            print("Button is visible and enabled.")
        else:
            print("Button is not visible or enabled.")

        # Click the button that contains the "Month View" text to open the dropdown
        button.click()


        # Wait for the dropdown to appear and ensure it's visible
        page.locator('text=Day View').wait_for(state="visible", timeout=5000)  # Timeout after 5 seconds

        # Click on the "Day View" option from the dropdown
        page.locator('text=Day View').click()

        page.locator('button:has(span:has-text("Next month"))').click()
        page.locator('button:has(span:has-text("Next month"))').click()

        # Ensure that the page has fully switched to the Day View before proceeding
        page.wait_for_selector('td.fc-timegrid-slot[data-time="10:00:00"]', timeout=5000)  # Wait until the 10 AM slot is available

        # Drag the event to a new time slot (e.g., 10:00 AM)
        time = page.locator('td.fc-timegrid-slot[data-time="10:00:00"]:nth-of-type(2)')
        event = page.locator('text=Test Event')

        if time.is_visible():
            print("Found 10am!")
        else:
            print("Cound not find 10am")

        
        event.drag_to(time)
        page.screenshot(path='event_moved_3_hours.png')

        event.click()
        page.click('text=Delete')
        page.wait_for_selector('button[exid="modalSubmit"]')
        page.locator('button[exid="modalSubmit"]').click()

        # # --- Step 5: Delete Family ---
        page.locator('a[href="/auth/user/settings/profile"]:has-text("Settings")').click()
        page.click('text=Family')
        page.click('text=Family Members')

        # Locate the <li> first, e.g., the one that contains the user name "Willem M"
        li = page.locator('li:has-text("Willem")')

        # Inside that <li>, find the button with the SVG that has the xmlns attribute
        button_in_li = li.locator('button:has(svg[xmlns="http://www.w3.org/2000/svg"])')

        # Click the button
        if button_in_li.is_visible():
            print("Button inside the correct <li> found!")
            button_in_li.click()
        else:
            print("Button inside <li> not found.")

        # page.click('text=Remove Willem M from Family')
        page.click('text=Delete Family')
        page.fill('input[name="Password"]', 'IcuI4cu4Fam!')

        page.wait_for_selector('button[exid="modalSubmit"]')

        ## Wait for the Authenticate button to appear and click it
        page.locator('button:has-text("Authenticate")').click()


        page.wait_for_selector('button[exid="modalSubmit"]')
        # Wait for the REMOVE WILLEM M button to appear and click it
        # page.locator('button[exid="modalSubmit"]:has-text("REMOVE WILLEM M")').click()
        page.locator('button[exid="modalSubmit"]:has-text("DELETE FAMILY")').click()

        # Wait for a specific amount of time (in milliseconds, e.g., 2 seconds)
        page.wait_for_timeout(4000))  # 2000 milliseconds = 2 seconds

        page.screenshot(path='family_deleted.png')

        # # Verify deletion was successful (e.g., success message)
        # page.wait_for_selector('text=Family deleted successfully')
        # assert 'Family deleted successfully' in page.text_content()

        # # --- Step 6: Attempt to Re-Log In ---
        page.click('text=Logout')
        
        # Attempt to login again after deletion
        page.click('text=Login')
        page.fill('input[name="Email"]', 'willmarda@outlook.com')
        page.fill('input[name="Password"]', 'IcuI4cu4Fam!')
        page.click('button:text("Sign In")')

        # # Verify login fails
        # page.wait_for_selector('text=Account no longer exists')  # Adjust message as per app behavior
        # assert 'Account no longer exists' in page.text_content()

        page.wait_for_timeout(2000)  # 2000 milliseconds = 2 seconds

        # Cleanup
        browser.close()

if __name__ == '__main__':
    run_test()
