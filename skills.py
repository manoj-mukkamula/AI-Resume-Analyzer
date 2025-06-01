# skills.py

software_skills = [

    # === Programming Languages ===
    "python", "java", "c", "c++", "c#", "javascript", "typescript", "go", "ruby", "swift",
    "kotlin", "php", "r", "scala", "perl", "bash", "shell scripting", "vb.net", "assembly",

    # === Web Development (Frontend) ===
    "html", "css", "scss", "sass", "less", "bootstrap", "tailwind css", "material ui", 
    "javascript", "typescript", "jquery", "react", "next.js", "vue.js", "nuxt.js", "angular", 
    "svelte", "backbone.js", "ember.js",

    # === Web Development (Backend) ===
    "node.js", "express.js", "django", "flask", "spring boot", "spring mvc", 
    "asp.net", ".net core", "php", "laravel", "codeigniter", "ruby on rails", 
    "fastapi", "kotlin", "go", "graphql", "rest api", "rpc",

    # === Databases ===
    "mysql", "postgresql", "sqlite", "oracle", "mssql", "mariadb", "mongodb", 
    "cassandra", "firebase", "dynamodb", "couchdb", "neo4j", "redis", "elasticsearch",

    # === DevOps & CI/CD ===
    "git", "github", "gitlab", "bitbucket", "docker", "kubernetes", "jenkins", 
    "travis ci", "circleci", "azure devops", "ansible", "puppet", "chef", 
    "terraform", "vagrant", "nexus", "artifact registry", "helm",

    # === Cloud Platforms ===
    "aws", "amazon web services", "ec2", "s3", "lambda", "rds", "cloudwatch", 
    "azure", "google cloud", "gcp", "firebase", "heroku", "render", 
    "vercel", "netlify", "digitalocean", "linode", "cloudflare",

    # === Data Science & ML ===
    "numpy", "pandas", "scikit-learn", "matplotlib", "seaborn", "tensorflow", 
    "keras", "pytorch", "xgboost", "lightgbm", "opencv", "mlops", "nltk", "spacy", 
    "huggingface", "transformers", "gensim", "textblob", "label studio",

    # === Data Analysis & BI ===
    "excel", "power bi", "tableau", "looker", "qlikview", "sql", "pandas", 
    "matplotlib", "jupyter", "apache spark", "hadoop", "hive", "databricks",

    # === Software Testing ===
    "selenium", "cypress", "junit", "pytest", "testng", "jest", "mocha", "chai", 
    "postman", "soapui", "jmeter", "robot framework", "playwright",

    # === Mobile App Development ===
    "android", "android studio", "kotlin", "java", "ios", "swift", 
    "flutter", "react native", "xamarin", "cordova", "ionic",

    # === API & Integration ===
    "rest api", "graphql", "soap", "json", "xml", "axios", "postman", 
    "swagger", "openapi", "oauth", "jwt", "webhooks", "grpc",

    # === Operating Systems & Environments ===
    "linux", "ubuntu", "red hat", "debian", "centos", "windows", "macos", "unix", 
    "shell scripting", "powershell", "wsl",

    # === IDEs & Tools ===
    "vscode", "intellij idea", "pycharm", "eclipse", "netbeans", "android studio", 
    "xcode", "r studio", "spyder", "sublime text", "notepad++",

    # === Version Control ===
    "git", "svn", "mercurial", "github", "gitlab", "bitbucket",

    # === Project Management & Methodologies ===
    "agile", "scrum", "kanban", "waterfall", "jira", "confluence", 
    "trello", "asana", "monday.com", "clickup", "pmi", "safe agile",

    # === Software Architecture & Design ===
    "microservices", "monolithic", "event-driven", "domain-driven design", 
    "mvc", "mvvm", "design patterns", "oop", "solid principles",

    # === Cybersecurity Basics ===
    "owasp", "encryption", "jwt", "ssl", "firewalls", "vulnerabilities", 
    "penetration testing", "burpsuite", "wireshark", "nmap",

    # === Algorithms & Data Structures ===
    "arrays", "linked list", "stacks", "queues", "hash tables", "graphs", 
    "trees", "binary tree", "sorting", "searching", "recursion", "dynamic programming",

    # === Soft Skills & Professional Skills ===
    "problem solving", "communication", "teamwork", "leadership", "time management", 
    "critical thinking", "analytical skills", "collaboration", "attention to detail",

    # === Others ===
    "chatgpt", "openai", "ai", "ml", "nlp", "blockchain", "web3", "firebase", 
    "stripe", "paypal integration", "unit testing", "integration testing", "refactoring"
]

# Alias map for normalization (key: alias, value: canonical skill)
alias_map = {
    "html5": "html",
    "html4": "html",
    "html3": "html",
    "css3": "css",
    "js": "javascript",
    "nodejs": "node.js",
    "expressjs": "express.js",
    "reactjs": "react",
    "py": "python",
    "tf": "tensorflow",
    "keraslib": "keras",
    "aws": "amazon web services",
    "gcp": "google cloud",
    "nlp": "natural language processing",  # if used elsewhere
    "rdbms": "sql","html5": "html",
    "css3": "css",
    "react.js": "react",
    "vue.js": "vue",
    "restful apis": "rest api",
    # Add more aliases here as needed
}
