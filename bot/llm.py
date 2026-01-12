# llm.py

import json
import os
import time
import requests
from openai import OpenAI

# local imports (your project structure)
from .resume_handler import (
    Skills,
    Certifications,
    Projects,
    cover_letter_prompt_format,
    assignment_prompt_format,
    assignment_validation_prompt,
)

# ---------------------------------------------------------
# Check if GPT API is alive
# ---------------------------------------------------------

def is_gpt_api_alive() -> bool:
    try:
        res = requests.get(
            "https://text.pollinations.ai/prompt=Hello",
            timeout=5
        )
        return res.status_code == 200
    except requests.exceptions.RequestException:
        return False

# ---------------------------------------------------------
# ChatGPT Handler Class
# ---------------------------------------------------------

class chat:
    def __init__(self, browser_inst, use_api=True):
        self.main_page_url = "https://chatgpt.com/?model=auto"

        self.cover_letter_url = None
        self.assignment_url = None
        self.gpt_check_asg_url = None
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.use_api = use_api

        # only needed when browser-based ChatGPT is used
        if not self.use_api:
            config_dir = os.path.join(os.getcwd(), ".config")
            os.makedirs(config_dir, exist_ok=True)
            self.gpt_state_conf = os.path.join(config_dir, "chat_gpt_state.json")
            self.page = browser_inst.new_page()

    # -----------------------------------------------------
    # API MODE (Pollinations → ChatGPT proxy)
    # -----------------------------------------------------

    def get_gpt_api_resp(self, prompt, json_mode=False):
        print("📤 Sending prompt to GPT API")

        payload = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            "model": "openai",
            "jsonMode": json_mode,
        }

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print("ChatGPT API Error:", e)
            return ""

    # -----------------------------------------------------
    # COVER LETTER
    # -----------------------------------------------------

    def get_cover_letter(self, profile, company, about, skills, is_int_or_job):
        prompt = cover_letter_prompt_format(
            profile, company, about, skills, is_int_or_job
        )

        # ---------- API MODE ----------
        if self.use_api:
            resp = self.get_gpt_api_resp(prompt)
            if not resp:
                return ""

            if len(resp) > 2048:
                cover_lt = ""
                for x in resp.split("."):
                    if len(cover_lt) + len(x) + 1 <= 2000:
                        cover_lt += x + "."
                    else:
                        break
            else:
                cover_lt = resp

            return cover_lt

        # ---------- BROWSER MODE ----------
        self._goto_chat(self.cover_letter_url)

        self.page.wait_for_selector("#prompt-textarea", state="visible")
        self.page.locator("#prompt-textarea").fill(prompt)
        time.sleep(2)

        self.page.locator('[data-testid="send-button"]').click()
        print("✍️ Generating cover letter...")

        time.sleep(10)
        while self.page.locator('[data-testid="stop-button"]').is_visible():
            time.sleep(2)

        resp = self._read_last_response()

        self.cover_letter_url = self.page.url
        self.page.context.storage_state(path=self.gpt_state_conf)

        return resp

    # -----------------------------------------------------
    # ASSIGNMENT ANSWER
    # -----------------------------------------------------

    def get_assignment_answer(
        self, profile, company, about, skills, question, is_int_or_job
    ):
        prompt = assignment_prompt_format(
            profile, company, about, skills, question, is_int_or_job
        )

        # ---------- API MODE ----------
        if self.use_api:
            return self.get_gpt_api_resp(prompt)

        # ---------- BROWSER MODE ----------
        self._goto_chat(self.assignment_url)

        self.page.wait_for_selector("#prompt-textarea", state="visible")
        self.page.locator("#prompt-textarea").fill(prompt)
        time.sleep(1)

        self.page.locator('[data-testid="send-button"]').click()
        print("🧠 Solving assignment...")

        time.sleep(5)
        while self.page.locator('[data-testid="stop-button"]').is_visible():
            time.sleep(2)

        resp = self._read_last_response()

        self.assignment_url = self.page.url
        self.page.context.storage_state(path=self.gpt_state_conf)

        return resp

    # -----------------------------------------------------
    # ASSIGNMENT VALIDATION
    # -----------------------------------------------------

    def assmnt_is_valid(self, profile, question, is_int_or_job):
        prompt = assignment_validation_prompt(profile, question, is_int_or_job)

        # ---------- API MODE ----------
        if self.use_api:
            resp = self.get_gpt_api_resp(prompt, json_mode=True)
            try:
                return json.loads(resp)
            except Exception:
                return {"send_to_chatbot": True, "reason": ""}

        # ---------- BROWSER MODE ----------
        self._goto_chat(self.gpt_check_asg_url)

        self.page.wait_for_selector("#prompt-textarea", state="visible")
        self.page.locator("#prompt-textarea").fill(prompt)
        time.sleep(1)

        self.page.locator('[data-testid="send-button"]').click()
        print("🔍 Checking assignment validity...")

        time.sleep(5)
        while self.page.locator('[data-testid="stop-button"]').is_visible():
            time.sleep(2)

        resp = self._read_last_response()

        self.gpt_check_asg_url = self.page.url
        self.page.context.storage_state(path=self.gpt_state_conf)

        try:
            return json.loads(resp)
        except Exception as e:
            print("⚠️ JSON parse failed:", e)
            return {"send_to_chatbot": True, "reason": ""}

    # -----------------------------------------------------
    # INTERNAL HELPERS
    # -----------------------------------------------------

    def _goto_chat(self, url):
        try:
            if url:
                self.page.goto(url, timeout=30000, wait_until="networkidle")
            else:
                self.page.goto(self.main_page_url, timeout=30000, wait_until="networkidle")
        except TimeoutError:
            print("⚠️ ChatGPT page timeout, retrying...")
            self.page.goto(self.main_page_url, timeout=30000, wait_until="networkidle")

    def _read_last_response(self):
        resp = self.page.locator("div.text-base").all()[-3].inner_text()

        # cleanup junk UI text
        return (
            resp.replace("ChatGPT\nMemory updated\n\n", "")
            .replace("ChatGPT\n\n", "")
            .replace("\n\n4o mini", "")
            .replace("\n\n4o", "")
            .replace("\nIs this conversation helpful so far?", "")
            .replace("ChatGPT\njson\nCopy code\n", "")
            .replace(
                "Which response do you prefer?\nYour choice will help make ChatGPT better.\nChatGPT\nResponse 1",
                "",
            )
            .replace("ChatGPT\nResponse 2", "")
        )
# ---------------------------------------------------------
# PUBLIC FUNCTION USED BY apply.py
# ---------------------------------------------------------

def generate_answer(
    browser_inst,
    profile,
    company,
    about,
    skills,
    question=None,
    is_int_or_job="internship",
    use_api=True,
):
    """
    This function is used by apply.py
    It decides whether to generate:
    - Cover Letter (when question is None)
    - Assignment Answer (when question is provided)
    """

    gpt = chat(browser_inst, use_api=use_api)

    # COVER LETTER
    if question is None:
        return gpt.get_cover_letter(
            profile=profile,
            company=company,
            about=about,
            skills=skills,
            is_int_or_job=is_int_or_job,
        )

    # ASSIGNMENT ANSWER
    return gpt.get_assignment_answer(
        profile=profile,
        company=company,
        about=about,
        skills=skills,
        question=question,
        is_int_or_job=is_int_or_job,
    )
