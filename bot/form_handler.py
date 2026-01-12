# bot/form_handler_selenium.py

from typing import Dict, Any, Union, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

QuestionHandler = Dict[str, Any]

def collect_question_handlers(driver: WebDriver) -> Dict[str, QuestionHandler]:
    """
    Internshala ke additional questions ko Selenium se detect karna.

    Return format:
    {
      "question text": {
         "type": "radio" | "text" | "numeric",
         "options": [...],        # sirf radio
         "fill": callable(value), # text/numeric
         "select": callable(opt)  # radio
      },
      ...
    }
    """
    handlers: Dict[str, QuestionHandler] = {}

    # Saare additional questions container
    containers = driver.find_elements(By.CSS_SELECTOR, ".form-group.additional_question")

    for index, container in enumerate(containers):
        try:
            label_el = container.find_element(By.CSS_SELECTOR, ".assessment_question label")
            question_text = label_el.text.strip()
        except Exception:
            continue

        if not question_text:
            continue

        # 1) Radio
        try:
            radio_group = container.find_element(By.CSS_SELECTOR, ".radio_group")
        except Exception:
            radio_group = None

        if radio_group:
            radio_elements = radio_group.find_elements(By.CSS_SELECTOR, ".radio")
            options_info: List[Dict[str, Any]] = []

            for opt_index, el in enumerate(radio_elements):
                try:
                    opt_label = el.find_element(By.TAG_NAME, "label").text.strip()
                except Exception:
                    opt_label = f"Option {opt_index + 1}"
                options_info.append({"index": opt_index, "text": opt_label})

            def select_option(option_text: str, idx: int = index, opts=options_info):
                chosen_index = 0
                opt_text_lower = option_text.strip().lower()
                for opt in opts:
                    if opt["text"].strip().lower() == opt_text_lower:
                        chosen_index = opt["index"]
                        break

                all_containers = driver.find_elements(By.CSS_SELECTOR, ".form-group.additional_question")
                if idx < len(all_containers):
                    radios = all_containers[idx].find_elements(By.CSS_SELECTOR, ".radio")
                    if chosen_index < len(radios):
                        try:
                            radios[chosen_index].find_element(By.TAG_NAME, "label").click()
                        except Exception:
                            pass

            handlers[question_text] = {
                "type": "radio",
                "options": [o["text"] for o in options_info],
                "select": select_option,
            }
            continue

        # 2) Textarea
        try:
            textarea = container.find_element(By.TAG_NAME, "textarea")
        except Exception:
            textarea = None

        if textarea is not None:
            def fill_text(value: str, idx: int = index):
                all_containers = driver.find_elements(By.CSS_SELECTOR, ".form-group.additional_question")
                if idx < len(all_containers):
                    try:
                        ta = all_containers[idx].find_element(By.TAG_NAME, "textarea")
                        ta.clear()
                        ta.send_keys(value)
                    except Exception:
                        pass

            handlers[question_text] = {
                "type": "text",
                "fill": fill_text,
            }
            continue

        # 3) Numeric input
        try:
            num_input = container.find_element(By.CSS_SELECTOR, 'input[type="number"]')
        except Exception:
            num_input = None

        if num_input is not None:
            def fill_numeric(value: Union[int, float, str], idx: int = index):
                all_containers = driver.find_elements(By.CSS_SELECTOR, ".form-group.additional_question")
                if idx < len(all_containers):
                    try:
                        inp = all_containers[idx].find_element(By.CSS_SELECTOR, 'input[type="number"]')
                        inp.clear()
                        inp.send_keys(str(value))
                    except Exception:
                        pass

            handlers[question_text] = {
                "type": "numeric",
                "fill": fill_numeric,
            }
            continue

        # Unknown
        print(f"[WARN] Unknown question type: {question_text!r}")

    return handlers
