# Internshala-Automation (Selenium + Templates)

## Background

While searching for internships on Internshala, I realised that applying manually is extremely repetitive and time‑consuming. Filtering internships, opening each listing, tailoring a cover letter, and answering assignment questions can easily take 7–15 minutes per application. When platforms themselves suggest applying to 15+ internships to get a single response, this turns into hours of boring, repetitive work.

As a Computer Science student who enjoys automation and web development, I wanted to reduce this friction.  
So I decided to build my own Internshala automation tool that:

- Opens Internshala with my logged‑in session  
- Uses my own resume data and fixed templates  
- Fills the application form automatically (including cover letter and common questions)  
- Submits multiple applications with minimal manual effort

The core idea of this project are **inspired by the open‑source project**  
[Eviltr0N/internshala-bot](https://github.com/Eviltr0N/internshala-bot),  
but this implementation is written separately using Selenium, with simplified logic and no paid AI APIs.

---

## Features

- Apply to multiple internships automatically after you manually set filters on Internshala.
- Uses saved login cookies so you do not need to log in every time.
- Template‑based cover letter generation using your own resume text.
- Automatically fills common assignment questions with resume‑aware English answers (no external API).
- Skips sensitive questions (salary, CGPA, marks, etc.) so that you can answer them manually later.
- Logs each application (success / basic failure reason) into a CSV file so you can track what was applied.
- Built entirely with **Python + Selenium** and designed to be easy to read, modify and extend.

> Note: This project **does not use ChatGPT / paid APIs**.  
> All answers are generated from predefined templates that you can customise in the code.

---

## Installation

### 1. Clone the repository
> git clone https://github.com/DrishtiSharma7/internshala-automation.git    
>cd internshala-automation
### 2. Create and activate virtual environment (optional but recommended)
>python3 -m venv venv    
>source venv/bin/activate   # macOS / Linux    
> .\venv\Scripts\activate  # Windows PowerShell    
### 3. Install dependencies
>pip install -r requirements.txt    
### requirements.txt typically contains:
>text    
>selenium==4.x.x    
>webdriver-manager==4.x.x    
>pandas           # only if you use the HTML report version    
>requests         # if you add any HTTP calls later    

Make sure you have Google Chrome installed and the correct ChromeDriver path configured in bot/browser.py.

## How to Use
 
### 1. Save your Internshala login session (cookies)
Run the login helper once:
>python3 -m bot.login    

This will:
* Open the Internshala login page in a real Chrome window.
* Ask you to log in manually (email/phone + password/OTP).
* After you press ENTER in the terminal, it will save a cookies.pkl file in the project root.
* Next runs will reuse these cookies to keep you logged in automatically.
### 2. Add your resume text
Create or edit the file:
>resume.ini
  
Fill it with your own information (skills, projects, brief summary etc.).
This text is used while building the cover letter and answers for the application form.
### 3. Apply filters on Internshala and scrape links
Run the main script:
>python3 main.py    

## Flow:

1. The script opens Internshala in a browser using Selenium.
2. You manually apply filters on the site (profile, location, stipend, etc.).
3. When you are satisfied with the filtered results, return to the terminal and press ENTER.
4. The script collects all internship links from the current results page.
5. Auto‑apply to internships
     * After scraping links, the script will:
     * Open each internship detail page.
     * Skip if you have already applied to that listing.
     * Extract profile, company, description and skills.
     * Fill the cover letter using a template defined in bot/text_helpers.py.
     * Detect all additional questions under the form using bot/form_handler_selenium.py.
     * For each question:
         - If it contains sensitive keywords (salary, CGPA, marks, etc.), it is skipped.
         - Otherwise, a template‑based English answer is chosen based on the question text.
     * Click the Submit button for that internship.
     * Log the result (Applied / Failed + reason) into applications_log.csv.

You can later open applications_log.csv in Excel/Sheets to review which internships were applied successfully.

## Configuration and Customisation

#Template answers    
All cover letter and assignment answers are defined in:
>bot/text_helpers.py    

You can:    
     * Edit the cover letter template to reflect your own degree, tech stack and tone.    
     * Extend the answer_assignment_text(question) function with new patterns and answers for more question types.    
     * Change the default numeric answer in answer_assignment_numeric(question) if needed.    

#Sensitive questions filtering    
Words like stipend, salary, ctc, cgpa, marks, percentage, etc. are treated as sensitive and skipped automatically.
These are defined in bot/apply.py in the SKIP_KEYWORDS list – feel free to update this list according to your preferences.

#Selectors    
The script assumes the current Internshala DOM structure (CSS selectors / XPaths).
If Internshala changes its UI, you may need to update selectors in:
>bot/scraper.py – for card and link extraction        
>bot/apply.py – for “Apply now”, “Submit”, cover letter textarea and checkboxes        
>bot/form_handler_selenium.py – for additional questions detection        

### Credits & Inspiration

- Original idea and high‑level flow are inspired by Eviltr0N/internshala-bot, an excellent Playwright‑based Internshala automation tool.
- This project re‑implements similar concepts using Selenium, template‑based responses and a simpler, beginner‑friendly code structure.
- All code in this repository is written and adapted independently to fit my use case, learning goals and environment.

### Disclaimer

- This project is for educational and personal use only.
- Use automated tools responsibly and always respect the terms of service of any platform you interact with.
- The author is not responsible for any misuse, account issues or consequences caused by running this script.
