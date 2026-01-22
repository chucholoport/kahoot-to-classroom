# Kahoot to Classroom

This project transforms Kahoot reports into organized grades and uploads them automatically to **Google Classroom** using its API.  
There are two modes of operation: **autograde** (automated) and **manual mode** (local reports only).

---

## Requirements

- **Python 3.8+**
- Library **pandas**
- Credentials for the **Google Classroom API**
- Configuration files `.ini` with course parameters

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## Modes of Use

### 1. Autograde (automated)

This mode connects directly to Google Classroom and uploads Kahoot grades to the corresponding course.  
The `-r` (reports) parameter is **mandatory**.

#### Script: `autograde.sh`

```bash
./autograde.sh -c config/ISW17.ini -r reports/ISW17_Kahoot.xlsx
./autograde.sh -h
```

- `-c <config.ini>` → mandatory, defines course and parameters.  
- `-r <report.xlsx>` → mandatory, one or more Kahoot reports.  
- `-h` → shows help.

The script processes the reports and uploads the grades directly via the API to Classroom.

---

### 2. Manual mode (local reports only)

In this mode **Classroom is not updated**.  
The script generates reports ordered according to the student list in Classroom, but the teacher must upload them manually.

Example:

```bash
python3 src/main.py -c config/ISW17.ini -r reports/ISW17_Kahoot.xlsx
```

- Produces an Excel/CSV file with grades.  
- Student order follows the official Classroom list.  
- No API calls are made.

---

## Quick Comparison

| Feature                  | Autograde (API) | Manual mode |
|---------------------------|-----------------|-------------|
| Automatic upload to Classroom | ✅ Yes | ❌ No |
| Uses official API      | ✅ Yes | ❌ No |
| Local reports          | ✅ Yes | ✅ Yes |
| Ordered by Classroom   | ✅ Yes | ✅ Yes |
| Teacher intervention   | Minimal | High |

---

## Important Notes

- The `.sh` scripts are wrappers for `src/main.py`.  
- The configuration `.ini` file must contain credentials and course parameters.  
- In autograde mode, grades are reflected directly in Classroom.  
- In manual mode, reports are generated locally and must be uploaded manually.

---

## Author

jesus.loport ([GitHub](https://github.com/chucholoport)|[LinkedIn](https://www.linkedin.com/in/jesus-salvador-lopez-ortega))  