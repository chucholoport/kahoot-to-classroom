# Certificates and Credentials (`certs/`)

This directory stores the **OAuth2 credential files** (`.json`) required to authenticate with Google Classroom API. Each file is generated in **Google Cloud Console** and should be referenced in your `.ini` configuration files under `[auth]`.

---

## Steps to Generate Credentials in Google Cloud

### 1. Create a Project
- Go to Google Cloud Console [(console.cloud.google.com in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fconsole.cloud.google.com%2F").  
- Click **Select Project → New Project**.  
- Give it a descriptive name (e.g., `Classroom-Automations`).  

### 2. Enable Required APIs
- Navigate to **APIs & Services → Library**.  
- Enable the following APIs:
  - **Google Classroom API**  
  - (Optional, depending on use case) **Google Drive API** if you plan to handle file attachments.  

### 3. Configure OAuth Consent Screen
- Go to **APIs & Services → OAuth consent screen**.  
- Choose **External** (if multiple accounts will use it).  
- Fill in:
  - App name (e.g., *Classroom Automations*).  
  - Support email.  
  - Authorized domains (optional for local testing).  
- Add **Scopes**:
  - `https://www.googleapis.com/auth/classroom.coursework.students` (grading student submissions).  
  - `https://www.googleapis.com/auth/classroom.courses.readonly` (read course info).  
  - (Optional) `https://www.googleapis.com/auth/classroom.rosters.readonly` (read student rosters).  
- Add **Test users** (emails of accounts that will use the app during development).  

### 4. Create OAuth Client ID
- Go to **APIs & Services → Credentials → Create Credentials → OAuth client ID**.  
- Select **Desktop App** as the application type.  
- Name it descriptively (e.g., `Classroom_Desktop_Client`).  
- Download the generated `.json` file.  

---

## File Placement

- Place the downloaded `.json` file inside the `certs/` directory.  
- Example:
  ```
  project/
   ├─ certs/
   │   └─ classroom_credentials.json
   ├─ config/
   │   └─ ISW28_OPERATING_SYSTEMS.ini
   ├─ src/
   │   └─ main.py
  ```

- Reference it in your `.ini` file:
  ```ini
  [auth]
  credentials = certs/classroom_credentials.json
  ```

---

## Usage Notes
- The first time you run your script, it will open a browser window for authorization.  
- A `token.json` will be generated at project root to store the access/refresh tokens.  
- If you change scopes, delete `token.json` and reauthorize.  

---

## ⚠️ Security Considerations
- Never commit `.json` credential files to public repositories.  
- Use `.gitignore` to exclude `certs/`.  
- Rotate credentials if compromised.  
