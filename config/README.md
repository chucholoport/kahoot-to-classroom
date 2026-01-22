# Course Configuration (`config/`)

This directory contains configuration files (`.ini`) that define the basic parameters for each **group** and **course**.  
Each file follows the **INI format** and must be named:

```
<group>_<course>.ini
```

Example:
```
ISW28_OPERATING_SYSTEMS.ini
```

---

## Structure of a `.ini` file

Each configuration file currently has three main sections:

### `[course]`
- **course_id**: The unique identifier of the course in Google Classroom.  
  - You can obtain it directly from the course URL in Classroom:  
    ```
    https://classroom.google.com/c/1234567890123
    ```
    Here, the `course_id` is `1234567890123`.

### `[certs]`
- **credentials**: Path to the OAuth2 credentials file (`.json`) generated in Google Cloud Console.  
  - Typically stored in the `certs/` directory.  
  - Example:  
    ```
    certs/classroom_credentials.json
    ```

### `[data]`
- **student_list**: Path to the manual student roster file (`.txt`).  
  - Stored in the `data/` directory.  
  - File naming convention: `<GROUP>.txt` (only the group name, no course suffix).  
  - Example:  
    ```
    data/ISW17.txt
    ```
- **Format requirements**:  
  - Plain text (`.txt`).  
  - Only student names (no emails).  
  - One student per line.  
  - No blank lines or comments.

---

## Example

```ini
[course]
course_id = 1234567890123

[certs]
credentials = certs/classroom_credentials.json

[data]
student_list = data/ISW17.txt
```

---

## Usage in the project

1. Place the `.ini` file in the `config/` directory.  
2. Place the corresponding student list file in the `data/` directory.  
3. Run the main script specifying the configuration file:  
   ```bash
   python src/main.py ISW28_OPERATING_SYSTEMS.ini
   ```
4. The script will automatically load:
   - The `course_id` to identify the target course.  
   - The credentials path to authenticate with the Classroom API.  
   - The student list file to map grades to the correct roster.

---

## Scalability

- For each new group/subject, simply create a new `.ini` file following the same format.  
- Create the corresponding `.txt` file in the `data/` directory with the group name.  
- This design allows the project to scale globally without modifying the source code—just add more configurations here.