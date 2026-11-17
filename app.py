"""
Manipal Hospitals Smart Queue System
====================================
Old Airport Road, Bengaluru • NABH Accredited • 700+ Beds • 60+ Specialties

This module provides the core queue priority management logic,
unit tests, and a built-in local development server.
"""

from __future__ import annotations
import sys
import webbrowser
import http.server
import socketserver
from dataclasses import dataclass
from typing import List, Optional, Literal


PriorityType = Literal["Normal", "Urgent"]


@dataclass
class Doctor:
    id: int
    name: str
    dept: str
    location: str = "Old Airport Road"
    room: str = "Room 101"


@dataclass
class Appointment:
    time: str
    patient: str
    doctor: str
    dept: str
    emergency: bool = False
    priority: PriorityType = "Normal"
    status: str = "Waiting"  # Waiting, In Consultation, Completed, Deferred


DOCTORS: List[Doctor] = [
    Doctor(id=1, name="Dr. Devi Shetty", dept="Cardiac Surgery", room="Room 101"),
    Doctor(id=2, name="Dr. Manish Rai", dept="Cardiology", room="Room 204"),
    Doctor(id=3, name="Dr. Sudarshan Ballal", dept="Nephrology", room="Room 305"),
    Doctor(id=4, name="Dr. Triage Team", dept="ER / Emergency", room="ER Bay 1"),
]

TIME_SLOTS = [
    "09:00", "09:20", "09:40", "10:00", "10:20",
    "10:40", "11:00", "11:20", "11:40", "12:00"
]


def parse_token(label: str) -> Optional[int]:
    """
    Parses a token string like '#25' to integer 25.
    Returns None for invalid labels.
    """
    if not isinstance(label, str):
        return None
    if not label.startswith("#"):
        return None
    digits = label[1:]
    if not digits.isdigit():
        return None
    return int(digits)


def urgent_first_then_time(a: Appointment, b: Appointment) -> int:
    """
    Sort comparator: Urgent/Emergency appointments are prioritized before Normal.
    Within the same priority, earlier appointment times come first.
    Returns negative if a < b, positive if a > b, 0 if equal.
    """
    a_priority_val = 0 if (a.priority == "Urgent" or a.emergency) else 1
    b_priority_val = 0 if (b.priority == "Urgent" or b.emergency) else 1

    if a_priority_val != b_priority_val:
        return a_priority_val - b_priority_val

    if a.time < b.time:
        return -1
    elif a.time > b.time:
        return 1
    return 0


class SmartQueue:
    """
    In-memory smart queue for hospital appointment management.
    """

    def __init__(self, avg_consult_mins: int = 7) -> None:
        self.avg_consult_mins = avg_consult_mins
        self.current_token: int = 22
        self.served_count: int = 0
        self.appointments: List[Appointment] = [
            Appointment(time="10:00", patient="#21", doctor="Dr. Manish Rai", dept="Cardiology", priority="Normal"),
            Appointment(time="10:20", patient="#22", doctor="Dr. Manish Rai", dept="Cardiology", priority="Normal"),
            Appointment(time="10:40", patient="Emergency", doctor="Triage", dept="ER", emergency=True, priority="Urgent"),
            Appointment(time="11:00", patient="#23", doctor="Dr. Manish Rai", dept="Cardiology", priority="Normal"),
        ]

    def add_appointment(self, appointment: Appointment) -> None:
        self.appointments.append(appointment)
        # Re-sort to maintain priority order
        from functools import cmp_to_key
        self.appointments.sort(key=cmp_to_key(urgent_first_then_time))

    def next_patient(self) -> Optional[Appointment]:
        if not self.appointments:
            return None
        served = self.appointments.pop(0)
        served.status = "Completed"
        self.served_count += 1

        parsed = parse_token(served.patient)
        if parsed is not None:
            self.current_token = parsed
        else:
            self.current_token += 1

        return served

    def estimate_wait_time(self, ahead_count: int) -> int:
        return max(0, ahead_count * self.avg_consult_mins)


# ----------------------------------------------------
# Self Tests (Equivalent to original TypeScript tests)
# ----------------------------------------------------
def run_tests() -> None:
    print("Running Smart Queue verification tests...")
    assert parse_token("#25") == 25, "parse_token should parse number correctly"
    assert parse_token("A25") is None, "parse_token should reject invalid token prefix"
    assert parse_token("#abc") is None, "parse_token should return None for non-numeric tokens"

    # Urgent before normal
    a1 = Appointment(time="09:00", patient="#1", doctor="D", dept="X", priority="Urgent")
    a2 = Appointment(time="08:00", patient="#2", doctor="D", dept="X", priority="Normal")
    assert urgent_first_then_time(a1, a2) < 0, "Urgent must come before Normal regardless of time"

    # Earlier time when same priority
    a3 = Appointment(time="09:00", patient="#1", doctor="D", dept="X", priority="Normal")
    a4 = Appointment(time="09:30", patient="#2", doctor="D", dept="X", priority="Normal")
    assert urgent_first_then_time(a3, a4) < 0, "Earlier time should come first when priorities are equal"

    print("All tests passed successfully! (5/5 checks passed)")


def start_server(port: int = 8000) -> None:
    """
    Starts an HTTP server to serve the Smart Queue System web app locally.
    """
    handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            url = f"http://localhost:{port}"
            print("\n" + "=" * 60)
            print("  MANIPAL HOSPITALS - SMART QUEUE SYSTEM")
            print("=" * 60)
            print(f"  Live Server running at: {url}")
            print("  Press Ctrl+C to stop the server.")
            print("=" * 60 + "\n")
            webbrowser.open(url)
            httpd.serve_forever()
    except OSError as e:
        print(f"Port {port} in use or unavailable: {e}")
        print("You can open index.html directly in your browser or with VS Code Live Server.")


if __name__ == "__main__":
    run_tests()
    if "--test-only" not in sys.argv:
        start_server()
