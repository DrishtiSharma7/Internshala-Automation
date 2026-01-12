# bot/text_helpers.py

def make_cover_letter(profile: str, company: str, about: str, skills: str, is_job: bool) -> str:
    role_type = "job" if is_job else "internship"

    skills_clean = skills.replace("\n", ", ").strip() or "web development, JavaScript, React.js, Next.js and related technologies"
    about_short = about[:300].replace("\n", " ")

    return (
        f"Dear Hiring Manager,\n\n"
        f"I am Drishti Sharma and I am excited to apply for the {profile} {role_type} at {company}. "
        f"I am currently pursuing B.Tech in Computer Science and have hands‑on experience in frontend "
        f"and web development through internships and academic projects.\n\n"
        f"My skills include {skills_clean}. I have worked as a Frontend Development Intern at Aakash + BYJU'S "
        f"and Prodigy Infotech, where I built and optimised responsive user interfaces using React.js, "
        f"JavaScript, HTML and CSS, and improved performance and user experience.\n\n"
        f"From the description, I understand that this role involves {about_short}... "
        f"I am confident that I can contribute with clean, reliable code and a strong focus on user experience, "
        f"while also learning from your team.\n\n"
        f"Thank you for considering my application.\n"
        f"Regards,\n"
        f"Drishti Sharma"
    )


def _norm(text: str) -> str:
    return text.strip().lower()


def answer_assignment_text(question: str) -> str:
    q = _norm(question)

    # 1) Why should you be hired / why you
    if "why should you be hired " in q or "why should we hire you " in q:
        return (
            "I should be hired for this internship because I have both a strong theoretical base in "
            "computer science and practical experience in web development. I have worked as a Frontend "
            "Development Intern at Aakash + BYJU'S and Prodigy Infotech, where I built and optimised "
            "responsive UIs and integrated APIs. I have also completed projects like a full‑stack virtual "
            "classroom and an Internshala automation script using Python and Selenium. These experiences "
            "show that I can understand requirements, design a solution and deliver it within deadlines. "
            "I am consistent, eager to learn and comfortable taking responsibility for my work."
        )

    # 2) Why this internship / company
    elif "why this internship" in q or "why do you want to" in q or "why do you want this" in q:
        return (
            "This internship aligns very well with my interests in web and software development and with "
            "the skills I have been building through my B.Tech and internships. I enjoy working on real‑world "
            "applications where I can improve user experience, performance and reliability. Your organisation "
            "provides an environment where I can learn from experienced professionals, work on meaningful "
            "projects and apply technologies like JavaScript, React.js, Next.js and related tools. This makes "
            "this opportunity an ideal next step in my growth as a developer."
        )

    # 3) Relevant skills / experience
    elif "relevant skills" in q or "skills do you have" in q or "experience do you have" in q:
        return (
            "I am pursuing B.Tech in Computer Science and have a good understanding of Data Structures and "
            "Algorithms, Object‑Oriented Programming, Operating Systems and Database Management Systems. "
            "My technical skills include JavaScript, HTML, CSS, React.js, Next.js, Node.js and MySQL. "
            "During my internships at Aakash + BYJU'S and Prodigy Infotech, I engineered interactive web "
            "applications, optimised UI performance and worked with cross‑functional teams. I have also built "
            "projects like a full‑stack virtual classroom and an Internshala automation script, which show my "
            "ability to design, implement and debug practical solutions."
        )

    # 4) Project / achievement
    elif "project" in q or "describe a project" in q or "tell us about a project" in q:
        return (
            "One of my key projects is 'ZERORA Virtual Classroom', a full‑stack web application built using "
            "the MERN stack with Next.js. I implemented teacher and student modules and optimised the system "
            "to handle multiple concurrent users with low latency for live whiteboard and comments. "
            "Another important project is my Internshala automation script, where I used Python and Selenium "
            "to automate the entire application process and significantly reduce the time per application. "
            "These projects improved my understanding of web architectures, state management, API integration, "
            "performance optimisation and debugging."
        )

    # 5) Availability / joining
    elif "availability" in q or "available" in q or "when can you start" in q or "start the internship" in q:
        return (
            "I am available to start the internship as per the timeline mentioned in the posting and I can "
            "commit for the full duration. I am used to balancing academics, internships and personal projects, "
            "so I can manage my schedule to give consistent time and focus to the internship without major "
            "interruptions."
        )

    # 6) Comfort with remote / onsite / timings
    elif "relocate" in q or "relocation" in q or "work from home" in q or "remote" in q or "working hours" in q:
        return (
            "Yes, I am comfortable with the work mode and timings mentioned for this internship. I have worked "
            "both independently and in teams, using tools like Git, GitHub, Jira and VS Code to collaborate and "
            "track progress. I am flexible with my schedule and can adjust my routine to ensure smooth "
            "communication and on‑time delivery of tasks."
        )

    # 7) Problem‑solving / coding practice
    elif "problem solving" in q or "dsa" in q or "data structures" in q or "coding practice" in q:
        return (
            "I actively practise Data Structures and Algorithms and have solved over 300 problems on LeetCode "
            "and more than 100 problems on Coding Ninjas, reaching Expert Level 8. This practice has improved "
            "my understanding of algorithms, complexity and debugging. When I face a new problem, I break it into "
            "smaller parts, think of edge cases and then choose an approach that is both correct and efficient. "
            "This mindset helps me write reliable and maintainable code in real projects as well."
        )

    # 8) Teamwork / responsibilities
    elif "team" in q or "teamwork" in q or "responsibility" in q or "leadership" in q:
        return (
            "I have handled responsibilities as Joint‑Core (Event Coordinator) for my college computer science "
            "department, where I helped organise multiple technical events and festivals attended by more than "
            "1,000 people. I coordinated with different teams, managed schedules and handled last‑minute issues. "
            "In my internships, I have collaborated with cross‑functional teams and regularly shared progress "
            "updates. Overall, I communicate clearly, respect deadlines and take ownership of my work, which "
            "helps the team trust and rely on me."
        )

    # Default fallback
    else:
        return (
            "Thank you for the question. Based on my background in computer science, my internships in frontend "
            "development and the projects I have completed, I am confident that I can learn quickly and contribute "
            "effectively to this role. I am sincere, disciplined and open to feedback, which helps me continuously "
            "improve my work during the internship."
        )


def answer_assignment_numeric(question: str) -> str:
    return "1"
