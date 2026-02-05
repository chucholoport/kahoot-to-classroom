import os
import sys
import json
import tempfile
import requests

from google.oauth2 import service_account
from googleapiclient.discovery import build


def connect_classroom(credentials_path: str, course_id: str):

    # Download credentials JSON from URL
    cred_path = os.path.abspath(credentials_path)
    if not os.path.exists(cred_path):
        sys.stderr.write(f"error: credentials file not found at {cred_path}\n")
        sys.exit(os.EX_NOINPUT)


    # Load credentials
    try:
        creds = service_account.Credentials.from_service_account_file(
            cred_path,
            scopes=["https://www.googleapis.com/auth/classroom.rosters.readonly"]
        )
    except Exception as e:
        sys.stderr.write(f"error: invalid credentials file\n{e}\n")
        sys.exit(os.EX_DATAERR)

    # Build Classroom service
    service = build("classroom", "v1", credentials=creds)

    # Fetch student list
    try:
        students = []
        request = service.courses().students().list(courseId=course_id)
        while request is not None:
            response = request.execute()
            for student in response.get("students", []):
                profile = student.get("profile", {})
                name = profile.get("name", {}).get("fullName", "")
                students.append(name)
            request = service.courses().students().list_next(request, response)
    except Exception as e:
        sys.stderr.write(f"error: cannot fetch students for course {course_id}\n{e}\n")
        sys.exit(os.EX_UNAVAILABLE)

    return students

