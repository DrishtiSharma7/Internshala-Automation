# bot/resume_handler.py

import os
from rich import print

config_file = 'resume.ini'

if not os.path.exists(config_file):
    with open(config_file, 'w', encoding='latin-1') as file:
        
        file.write('\n#RESUME CONFIG FILE \n\n')
        file.write('SKILLS = """\n\n\nTECHNICAL SKILLS\n• Web Software Development: JavaScript, HTML, CSS, MySQL, React.js, Next.js, Node.js\n• Programming Languages: Python, JavaScript\n• Core: Data Structures and Algorithms (DSA), Object-oriented Programming (OOPS), Operating System, Database Management System (DBMS)\n• Tools & Version Control: GitHub, VS Code, Bitbucket, Jira, Git\n• Languages: English, Hindi\n\nSOFT SKILLS & INTERESTS\n• Communication and Emotional Intelligence \n• Problem-Solving and Debugging\n• Teamwork and Collaboration \n• Traveling, Reading, Listening to Music\n• Technology and Time Management \n• Sketching, Calligraphy\n\n\n"""')
        file.write('WORKEXPERIENCE="""\n\n\n1. AAKASH + BYJUS (GURUGRAM) | FRONTEND DEVELOPMENT INTERN | August 2025 - September 2025\n• Developed and optimized responsive UI components using React.js, accelerating performance and user experience by 94.2%.\n• Orchestrated API integration and UI streamlining to reduce loading time by 97% and boost overall efficiency.\n• Authored and delivered weekly progress reports, resulting in the achievement of 98% of project milestones on schedule while ensuring higher-fidelity project tracking.\n\n2. PRODIGY INFOTECH | WEB DEVELOPMENT INTERN | September 2023 - October 2023    \n• Engineered an interactive web application : Tic Tac Toe, Stopwatch, Landing Page, Weather Forecast, using HTML, CSS, and JavaScript, incorporating real-time data updates, enhanced user engagement by 80%.\n• Collaborated with cross-functional teams to design and deploy front-end features and interactive components, driving an 86.9% improvement in UX.\n\n\n"""')
        file.write('CERTIFICATES = """\n\n\n1. Joint-Core (Event Coordinator) | SIET Computer Science\n• Coordinated scheduling for multiple annual college festivals and Tech Events, securing diverse talent, managing stage setup, and ensuring smooth transitions. Events attracted 1,000+ attendees.\n2. Google Analytics for Beginners | Google Analytics Academy\n• Completed the Google Analytics Individual Qualification (GAIQ) certification, demonstrating proficiency in digital analytics and data-driven decision-making.\n3. Python Skill Up | GeeksforGeeks (National Skill Up)\n• Completed a comprehensive Python programming course covering fundamentals, data structures, OOP, and practical applications, enhancing coding proficiency.\n4. Full Stack Web Development | GeeksforGeeks (National Skill Up)\n• Completed a full-stack web development curriculum covering HTML, CSS, JavaScript, React.js, Node.js, Express, and MongoDB, building multiple projects to demonstrate skills.\n4. Full Stack Web Development | GeeksforGeeks (National Skill Up)\n• Completed a full-stack web development curriculum covering HTML, CSS, JavaScript, React.js, Node.js, Express, and MongoDB, building multiple projects to demonstrate skills.\n\n\n"""')
        file.write('PROJECTS = """\n\n\n1. PORTFOLIO WEBSITE (January 2026)\n• Designed and developed a personal portfolio website using React.js and hosted on GitHub Pages to showcase projects and skills.\n• Achieved a 40% increase in visitor engagement through responsive design and optimized performance across devices.\n\n2. ZERORA VIRTUAL CLASSROOM (October 2025)\n• Architected a Full-Stack Virtual Classroom platform (MERN stack with Next.js) for 50+ potential concurrent users.\n• Implemented teacher and student modules, achieving 99.8% uptime and <500ms real-time synchronization latency for live whiteboard and comment features, ensuring a seamless learning experience.\n\n3. INTERNSHALLA AUTOMATION (May 2025)\n• Developed a Python automation script using Selenium and AI to reduce application time by 90% (from 15 mins to <1.5 mins per application).\n• Automated 100% of the application process (form filling, filtering, submission), successfully handling 200+ applications during testing.\n\n4. HEALTHCARE ANDROID APPLICATION (November 2024)\n• Built an Android application that provides 3 core user services (symptom tracking, scheduling, health tips) facilitating user health monitoring.\n• Amplified navigation efficiency by 25% through a user-friendly interface design, and integrated 2 key features (reminders and emergency contact) for more safety.\n\n\n"""')

        print('\nPlease Open [bold green]"resume.ini" [/]file using any text editor and add your [bold yellow]Skills, Certificates and Projects.[/] After adding those restart the script.\n')
        exit()


with open(config_file, 'r', encoding='latin-1', errors='ignore') as file:
    config_data = file.read().replace(";", "#")

try:
    exec(config_data)
except (IndentationError,SyntaxError) as e:
    print('[blod red]There is some indentation error with resume.ini file make sure you follow proper python indentation in resume.ini file.\n\nIt contains three multiline string variables. EDIT YOUR RESUME.INI FILE and RUN again. If you think you messed up everything then you can deleate the "resume.ini file and RUN again to recreate it then edit it."[/]')
    exit()

try:
    Skills = SKILLS
except:
    print("[bold red]Your skills dosent found in resume.ini file\n If you want to continue without skills press Enter else add skills and restart script.\n\n[/]")
    _ = input("Press Enter: ")
    Skills = '\nNO skills specified assume skills accordingly'

try:
    Certifications = CERTIFICATES
except:
    print("[bold red]Your Certifications dosent found in resume.ini file\n If you want to continue without Certifications press Enter else add skills and restart script.\n\n[/]")
    _ = input("Press Enter: ")
    Certifications = 'No certificates assume accordingly'

try:
    Projects = PROJECTS
except:
    print("[bold red]Your projects dosent found in resume.ini file\n If you want to continue without projects press Enter else add skills and restart script.\n\n[/]")
    _ = input("Press Enter: ")
    Projects = "No projects specified assume accordingly"

def cover_letter_prompt_format(profile, company, about, skills, int_or_job):
    prompt=f'''
I want you to write a cover letter for a {int_or_job}, \
I will provide you The {int_or_job} description, their skill requirements. \
I will also give you my skills, my certifications, my projects. \
You have to understand the {int_or_job} description and my whole portfolio then mention \
key things from my portfolio that are relavent to the {int_or_job} description. \
Keep cover letter simple but effective. \
Use general Indian english so it looks like its written by human. \
Below My skills, certifications, projects and {int_or_job} description, their skill requirements are attached. \
Dont use email formatting as I am not sending this in an email. \
Also Don't include header(such as Dear Hiring Manager... etc) and footer(such as Sincerly...etc). \
If my skill set lacks any of their skill requirement then assume that I possess that skill too. \


My Skills
```
{Skills}
```
Certifications
```
{Certifications}
```
My Projects
```
{Projects}
```

{int_or_job} Description
```
{profile}

{about}

Skills Required
{skills}
```
Company Name: {company}

Important - The letter must be less than 2000 characters.
'''
    return prompt

#====================================================================

def assignment_prompt_format(profile, company, about, skills, question, int_or_job):
    prompt=f'''
I am applying for an {int_or_job} whose description is attached below and their skills requirement too. \
They are asking that `{question}` \
I have attached my skills, certifications, projects also. \
I want you to understand their requirements and their question and answer it accordingly while keeping in mind my portfolio. \
If they are asking about any working shift or relocation to other place then i am totally confortable in all situations. \
If they are asking that about scheduled classes, assignments, or exams in the next 6 months then I dont have any of those as I am recently graduated and I can devote my time fully on {int_or_job}. \
Use general Indian english so it looks like its written by human & don't exhagurate your words. \
If my skill set lacks any of their skill requirement then assume that I possess that skill too. \
Keep Your answer to the point, short and precise.

My Skills
```
{Skills}
```
Certifications
```
{Certifications}
```
My Projects
```
{Projects}
```

{int_or_job} Description
```
{profile}

{about}

Skills Required
{skills}
```
Company Name: {company}

Important - In your response just give me answer following previous instructions and do not \
include question or any other text in you response besides answer of the question.
'''

    return prompt


def assignment_validation_prompt(profile, question, int_or_job):
    header=f'''

I am making a project which answers {int_or_job} Assignment Questions while applying for {int_or_job} Using an AI chatbot. The Ai chatbot has given My Personal portifolio which includes My Skills. Projects and Certification. It also given My working shifts and If I can relocate or not. I dont want that Ai chatbot will answer questions related to Personal things or related to information which is not inside the portfolio which is given to the Chatbot.You have to act as Moderator that I will give you question which will then passed to Ai chatbot, You have to check if the Question is related to :- 
`
Any personal information such as asking Grades/Percentages/CGPA.
If Question Contains any link/Url.
Asking question related Salary/Stipend.
Asking for LinkedIn/Github Profile Links.
Asking for Personal Achivements which are not related to {int_or_job} Profile.

`
If the question is related to above mention things then It should not answered by Ai chatbot and You have to Give Your Response In JSON Format. Here is Your Response Format - 
`
{{
"send_to_chatbot": true / false,
"reason": Reason which thing is asked
}}
`
Here are few Examples - 
Example - 1
"""
Profile - Data Analytics
Question - Candidates who have completed graduation or are in their last year of graduation (2024) would be considered for the internship. Please state your year of passing. Also, mention if you scored more than 70% in 10th, 12th, and graduation.
"""
Your Response Should be - 
""
{{"send_to_chatbot": false, "reason":"Asking For Educational Details"}}
""
Example - 2
"""
Profile - Machine Learning
Question - Provide us your Linkedin and Github.
"""
Your Response Should be - 
""
{{"send_to_chatbot": false, "reason":"Asking For Linkedin/Github"}}
""
Example - 3

"""
Profile - Machine Learning
Question - What will be the answer of this question https://docs.google.com/document/yup/sheisgorgeous.
"""
Your Response Should be - 
""
{{"send_to_chatbot": false, "reason":"Contains Link"}}
""
Example - 3

"""
Profile - Ai Engineer
Question - How do you ensure that you are aware of the latest trends, breakthroughs, and news in the field of artificial intelligence?.
"""
Your Response Should be - 
""
{{"send_to_chatbot": true, "reason":""}}
""

Example - 4

"""
Profile - Backend Engineer
Question - Have you posses any preoir experience in the same field? If yes please mention.
"""
Your Response Should be - 
""
{{"send_to_chatbot": true, "reason":""}}
""
'''

    footer = f'''
Now here is the question which you have to check - 
```
Profile - {profile}
Question -  {question}

```
Keep in mind you should only give response in desired format.
'''

    return header + footer