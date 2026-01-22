# Student Data (`data/`)

This directory contains **manual student lists** that mirror the roster as it appears in Google Classroom.  
These lists are used as references for grading automation and group management.

---

## How to obtain the student list

You have two options:

1. **Export directly from Google Classroom**  
   - Go to your course in Classroom.  
   - Open the "People" tab.  
   - Copy the list of student names exactly as they appear.  
   - Save them into a plain text file (`.txt`) inside the `data/` directory.

2. **Create manually**  
   - Write the student names exactly as they appear in Classroom.  
   - Paste them into a `.txt` file.  
   - Ensure the format matches the Classroom roster (one student per line).

---

## File format requirements

- Files must be plain text (`.txt`).  
- **Only student names** are allowed (no emails).  
- **No blank lines** are allowed.  
- **No comments** or extra symbols should be included.  
- Each line must represent a single student entry.  
- Example:

  ```txt
  Alice Johnson
  Bob Martinez
  Carla López
  ```

---

## Usage in the project

- Place the `.txt` file in the `data/` directory.  
- Reference it in your configuration (`.ini`) or scripts when mapping grades to students.  
- The automation will rely on these lists to ensure consistency with Classroom rosters.

---

## Scalability

- Create one `.txt` file per group.    
  ```
  ISW28.txt
  ISW27.txt
  ```
- This design allows both **online exports** and **manual lists** to coexist seamlessly.
```