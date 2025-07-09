Field	Your Entry
Name	Tashoy Miller
GitHub Username	tashoym94
Preferred Feature Track	Data / Visual / Interactive / Smart
Team Interest	Yes / No — If Yes: Project Owner or Contributor

✍️ Section 1: Week 11 Reflection
Answer each prompt with 3–5 bullet points:

Key Takeaways: What did you learn about capstone goals and expectations?
This week I learned: 
- The team portion of the project is NOT optional.
- What the required components of the project are and what the optional features to choose from are. 
- The timeline and milestones that must be met for success in the project.

Concept Connections: Which Week 1–10 skills feel strongest? Which need more practice?
- The skills that felt the strongest were APIs and SQL and Queries. Machine Learning was very math heavy and I need alot of practice.  

Early Challenges: Any blockers (e.g., API keys, folder setup)?
- So far the challenges I have encountered are my API key was not working when I was initially trying to test my Tkinter window and I spent over 6 hours combing through the code trying to find the error and then I decided to try a different API key from a previous assignment from a few back and that API key worked. I then did some research on Google and found out that sometimes the API keys aren't active right away. 

Support Strategies: Which office hours or resources can help you move forward?
- I still work with my partner group from the first round of partners and that holds me accountable. In our group we have people at different skill levels so I am able to ask my questions in a smaller group vs asking in the connect channel. Also, if as I'm working on the project I encounter any issues that my small group is unable  to help me with then I will join Office Hours. 

🗂️ Section 3: High-Level Architecture Sketch
Add a diagram or a brief outline that shows:

Core modules and folders

Feature modules

Data flow between components

``
WEATHER-PROJECT/
├── data/                        # Handles data storage and access
│   ├── data.py                 # Data loading and processing functions
│   ├── open_weather_*.txt      # API or forecast data
│   └── weather_history.txt     # Historical weather records
│
├── docs/                       # Project documentation
│   ├── LICENSE
│   └── Week11_Reflection.md
│
├── features/                   # Feature engineering modules
│   ├── __init__.py
│
├── gui/                        # GUI interfaces
│   ├── __init__.py
│   ├── gui_main.py             # Main GUI implementation
│   └── v2gui_main.py           # Alternative/new GUI version
│
├── screenshots/                # UI screenshots (for docs)
│
├── tests/                      # Unit tests for modules
│   ├── __init__.py
│   └── features_test.py        # Tests for feature logic
│
├── .env                        # Environment variables (e.g., API keys)
├── .gitignore
├── 10637-2024.csv              # External CSV data (likely weather)
├── config.py                   # Global configuration/settings
├── main.py                     # Entry point, ties data + features + GUI
├── README.md
└── requirements.txt            # Python dependencies


graph TD
    A[data.py] -->|loads| B[main.py]
    A -->|reads| C[weather_history.txt]
    A -->|reads| D[open_weather_*.txt]

    B --> E[features/]
    B --> F[gui/gui_main.py]
    B --> G[config.py]

    E -->|feature data| F
    F -->|displays| H[User GUI]

    subgraph Tests
        I[features_test.py] --> E
    end
[Add your architecture diagram or outline here]
```

📊 Section 4: Data Model Plan
Fill in your planned data files or tables:

File/Table Name	Format (txt, json, csv, other)	Example Row
weather_history.txt	txt	2025-06-09,New Brunswick,78,Sunny

- I have not made any decisions on this part of the project as of yet. 

📆 Section 5: Personal Project Timeline (Weeks 12–17)
Customize based on your availability:

Week	Monday	Tuesday	Wednesday	Thursday	Key Milestone
12	API setup	Error handling	Tkinter shell	Buffer day	Basic working app
13	Feature 1			Integrate	Feature 1 complete
14	Feature 2 start		Review & test	Finish	Feature 2 complete
15	Feature 3	Polish UI	Error passing	Refactor	All features complete
16	Enhancement	Docs	Tests	Packaging	Ready-to-ship app
17	Rehearse	Buffer	Showcase	–	Demo Day

⚠️ Section 6: Risk Assessment
Identify at least 3 potential risks and how you’ll handle them.

Risk	Likelihood (High/Med/Low)	Impact (High/Med/Low)	Mitigation Plan
API Rate Limit	Medium	Medium	Add delays or cache recent results
Bad code structure  Medium Medoum  Follow Naming conventions 
Error Handling Medium Medium Use try/except blocks

🤝 Section 7: Support Requests
What specific help will you ask for in office hours or on Slack?
- I am not aure at the moment but as I am working on the project and need help I  will seek it.












