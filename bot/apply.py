# bot/apply.py

from time import sleep
from selenium.webdriver.common.by import By
from bot.form_handler import collect_question_handlers
from bot.text_helpers import (
    make_cover_letter,
    answer_assignment_text,
    answer_assignment_numeric,
)

# Sensitive / personal / marks related questions skip karne ke liye
SKIP_KEYWORDS = [
    "stipend",
    "salary",
    "ctc",
    "package",
    "lpa",
    "cgpa",
    "percentage",
    "percent",
    "marks",
    "10th",
    "12th",
    "grade",
    "gpa",
]

def should_skip_question(question: str) -> bool:
    q = question.lower()
    return any(word in q for word in SKIP_KEYWORDS)

def apply_to_internship(driver, link: str, resume_text: str):
    """
    Single internship application:
    - internship page open
    - resume popup handle
    - relocation checkbox
    - cover letter (template-based)
    - assignment questions fill (template answers)
    - submit
    """

    driver.get(link)
    sleep(2)

    # Basic info scrape (profile, company, about, skills) – selectors tum adjust kar sakti ho
    try:
        card = driver.find_element(By.CSS_SELECTOR, 'div[id^="individual_internship"]')
        profile = card.find_element(By.CSS_SELECTOR, "div.heading_4_5.profile").text.strip()
        company = card.find_element(By.CSS_SELECTOR, "div.heading_6.company_name").text.strip()
    except Exception:
        profile = "Internship"
        company = "Company"

    try:
        about = driver.find_element(
            By.CSS_SELECTOR,
            "#details_container div.detail_view div.internship_details div:nth-child(2)",
        ).text.strip()
    except Exception:
        about = "No detailed description available."

    # Skills extract
    try:
        round_tabs = driver.find_elements(By.CSS_SELECTOR, ".round_tabs_container")
        if round_tabs:
            skills_texts = round_tabs[0].find_elements(By.CSS_SELECTOR, ".round_tabs")
            skills = "\n".join(x.text.strip() for x in skills_texts if x.text.strip())
        else:
            skills = ""
    except Exception:
        skills = ""

    is_job = "job" in link  # rough check

    # Agar Already Applied dikh raha ho to skip
    try:
        already_btns = driver.find_elements(By.XPATH, "//button[contains(text(),'Already Applied')]")
        for btn in already_btns:
            if btn.is_displayed():
                print("[INFO] Already applied, skipping:", link)
                return
    except Exception:
        pass

    # "Apply now" click
    try:
        apply_buttons = driver.find_elements(By.XPATH, "//button[contains(text(),'Apply now')]")
        if apply_buttons:
            apply_buttons[0].click()
            sleep(2)
    except Exception as e:
        print("[WARN] Could not click Apply now:", e)
        return

    # Resume intermediate popup
    try:
        if driver.current_url.startswith("https://internshala.com/student/resume"):
            try:
                proceed_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Proceed')]")
                proceed_btn.click()
                sleep(1)
            except Exception:
                pass
    except Exception:
        pass

    # Relocation checkbox
    try:
        checkbox = driver.find_element(By.NAME, "location_single")
        if checkbox.is_displayed():
            driver.execute_script("arguments[0].click();", checkbox)
            sleep(0.5)
    except Exception:
        pass

    # Cover letter
    cover_letter_text = ""
    try:
        textarea = driver.find_element(By.CSS_SELECTOR, "#cover_letter_holder textarea")
        if textarea.is_displayed():
            cover_letter_text = make_cover_letter(
                profile=profile,
                company=company,
                about=about,
                skills=skills,
                is_job=is_job,
            )
            textarea.clear()
            textarea.send_keys(cover_letter_text)
    except Exception as e:
        print("[WARN] Could not fill cover letter:", e)

    # Assignment questions
    handlers = {}
    try:
        handlers = collect_question_handlers(driver)
    except Exception as e:
        print("[WARN] Could not collect assignment questions:", e)

    for question, handler in handlers.items():
        try:
            if should_skip_question(question):
                print("[INFO] Skipping sensitive question:", question)
                # yahan agar tum report maintain karna chaho to failed/add logic laga sakti ho
                continue

            q_type = handler.get("type")

            if q_type == "radio":
                options = handler.get("options", [])
                if not options:
                    continue
                # Yes agar available ho
                choice = None
                for opt in options:
                    if opt.strip().lower() == "yes":
                        choice = opt
                        break
                if choice is None:
                    choice = options[0]
                handler["select"](choice)

            elif q_type == "numeric":
                numeric_ans = answer_assignment_numeric(question)
                handler["fill"](numeric_ans)

            else:
                text_ans = answer_assignment_text(question)
                handler["fill"](text_ans)

        except Exception as e:
            print("[ERROR] Failed on question:", question, "error:", e)
            # Yahan bhi chahe to failed report me add kar sakti ho
            continue

    # Submit
    try:
        submit_btn = driver.find_element(By.ID, "submit")
        submit_btn.click()
        sleep(3)
        print("[OK] Applied to:", link)
        # yahan success report me add kar sakti ho
    except Exception as e:
        print("[ERROR] Could not submit form:", e)
        # yahan failed report me add kar sakti ho
