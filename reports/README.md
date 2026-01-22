# Kahoot Reports (`reports/`)

This directory contains **exported reports from Kahoot**.  
These files are used to analyze student performance and integrate results into the grading workflow.

---

## How to export reports manually

1. Log in to [Kahoot](https://kahoot.com) with your account.  
2. Go to the **Reports** section (accessible from the left sidebar).  
3. Select the quiz/game session you want to export.  
4. Click on **Export** or **Download**.  
5. Choose the **Excel (.xlsx)** format.  
6. Save the file into the `reports/` directory of this project.

---

## File format requirements

- Reports must be exported as **Excel files (`.xlsx`)**.  
- Each file should contain the full session data provided by Kahoot (questions, answers, scores, participants).  
- Do not modify the structure of the exported file.  
- Naming convention:  
  ```
  <GROUP>_<QUIZNAME>.xlsx
  ```
  Example:  
  ```
  ISW17_SEMANA_2_Schedulers.xlsx
  ```

---

## Usage in the project

- Place the `.xlsx` file in the `reports/` directory.  
- Reference it in your scripts or workflows when analyzing Kahoot results.  
- The automation will later parse these files to integrate scores with Classroom rosters.

---

## Scalability

- One file per Kahoot session.  
- Keep all reports in this folder for traceability.  
- Future versions of the project may include **direct API integration** with Kahoot to automate report retrieval, but for now manual export is required.