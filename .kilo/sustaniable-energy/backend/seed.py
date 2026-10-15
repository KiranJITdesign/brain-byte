import random
from datetime import datetime, timedelta
from models import Building, EnergyReading, Equipment, Room

FLOORS_SEED = [
  {
    "level": 0,
    "name": "Floor 0 (GF)",
    "dept": "Ground Floor — Auditorium, Workshop & Admin",
    "rooms": [
      {
        "id": 1001,
        "name": "A25 Boys & Girls Toilet / Maint.",
        "code": "A25/A26",
        "kind": "utility",
        "x": 12,
        "y": 12,
        "w": 175,
        "h": 48,
        "occupied_from": 7,
        "occupied_to": 20,
        "equipment": [
          {
            "id": 100101,
            "name": "Ceiling Fans x4",
            "kind": "fan",
            "power_kw": 0.3,
            "count": 4,
            "is_on": True,
            "start_hour": 6,
            "end_hour": 21,
            "always24x7": False
          },
          {
            "id": 100102,
            "name": "LED Tube Lights x8",
            "kind": "light",
            "power_kw": 0.32,
            "count": 8,
            "is_on": True,
            "start_hour": 6,
            "end_hour": 21,
            "always24x7": False
          },
          {
            "id": 100103,
            "name": "IP CCTV Dome Cam x1",
            "kind": "cctv",
            "power_kw": 0.01,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 100104,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          }
        ]
      },
      {
        "id": 1002,
        "name": "A19 Central Store & Lift",
        "code": "A19",
        "kind": "store",
        "x": 192,
        "y": 12,
        "w": 125,
        "h": 48,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 100201,
            "name": "Ceiling Fans x2",
            "kind": "fan",
            "power_kw": 0.15,
            "count": 2,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 100202,
            "name": "LED Tube Lights x4",
            "kind": "light",
            "power_kw": 0.16,
            "count": 4,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 100203,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 100204,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          }
        ]
      },
      {
        "id": 1003,
        "name": "A7 Principal Director's Office",
        "code": "A7",
        "kind": "office",
        "x": 455,
        "y": 12,
        "w": 133,
        "h": 85,
        "occupied_from": 9,
        "occupied_to": 18,
        "equipment": [
          {
            "id": 100301,
            "name": "Ceiling Fans x3",
            "kind": "fan",
            "power_kw": 0.22,
            "count": 3,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 100302,
            "name": "LED Tube Lights x6",
            "kind": "light",
            "power_kw": 0.24,
            "count": 6,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 100303,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 100304,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 100305,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 100306,
            "name": "PA Wall Speakers x2",
            "kind": "speaker",
            "power_kw": 0.12,
            "count": 2,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 100307,
            "name": "Split AC Units (2.5 kW)",
            "kind": "ac",
            "power_kw": 2.5,
            "count": 2,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 100308,
            "name": "Admin PCs x4",
            "kind": "computer",
            "power_kw": 0.6,
            "count": 25,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 19,
            "always24x7": False
          }
        ]
      },
      {
        "id": 1004,
        "name": "A1 Workshop",
        "code": "A1",
        "kind": "lab",
        "x": 12,
        "y": 66,
        "w": 62,
        "h": 300,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 100401,
            "name": "Ceiling Fans x8",
            "kind": "fan",
            "power_kw": 0.6,
            "count": 8,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 100402,
            "name": "LED Tube Lights x12",
            "kind": "light",
            "power_kw": 0.48,
            "count": 12,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 100403,
            "name": "IP CCTV Dome Cam x3",
            "kind": "cctv",
            "power_kw": 0.04,
            "count": 3,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 100404,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 100405,
            "name": "PA Wall Speakers x2",
            "kind": "speaker",
            "power_kw": 0.12,
            "count": 2,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 100406,
            "name": "CNC & Lathe Machines",
            "kind": "computer",
            "power_kw": 4.5,
            "count": 25,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 18,
            "always24x7": False
          }
        ]
      },
      {
        "id": 1005,
        "name": "A16 Auditorium",
        "code": "A16",
        "kind": "hall",
        "x": 142,
        "y": 198,
        "w": 130,
        "h": 168,
        "occupied_from": 10,
        "occupied_to": 16,
        "equipment": [
          {
            "id": 100501,
            "name": "Ceiling Fans x10",
            "kind": "fan",
            "power_kw": 0.75,
            "count": 10,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 22,
            "always24x7": False
          },
          {
            "id": 100502,
            "name": "LED Tube Lights x16",
            "kind": "light",
            "power_kw": 0.64,
            "count": 16,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 22,
            "always24x7": False
          },
          {
            "id": 100503,
            "name": "IP CCTV Dome Cam x4",
            "kind": "cctv",
            "power_kw": 0.06,
            "count": 4,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 100504,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 100505,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 22,
            "always24x7": False
          },
          {
            "id": 100506,
            "name": "PA Wall Speakers x6",
            "kind": "speaker",
            "power_kw": 0.36,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 22,
            "always24x7": False
          },
          {
            "id": 100507,
            "name": "Split AC Units (6 kW)",
            "kind": "ac",
            "power_kw": 6,
            "count": 4,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 22,
            "always24x7": False
          }
        ]
      },
      {
        "id": 1006,
        "name": "Badminton Court (Courtyard)",
        "code": "COURT",
        "kind": "hall",
        "x": 315,
        "y": 92,
        "w": 135,
        "h": 178,
        "occupied_from": 6,
        "occupied_to": 20,
        "equipment": [
          {
            "id": 100601,
            "name": "Ceiling Fans x4",
            "kind": "fan",
            "power_kw": 0.3,
            "count": 4,
            "is_on": True,
            "start_hour": 6,
            "end_hour": 21,
            "always24x7": False
          },
          {
            "id": 100602,
            "name": "LED Tube Lights x10",
            "kind": "light",
            "power_kw": 0.4,
            "count": 10,
            "is_on": True,
            "start_hour": 6,
            "end_hour": 21,
            "always24x7": False
          },
          {
            "id": 100603,
            "name": "IP CCTV Dome Cam x4",
            "kind": "cctv",
            "power_kw": 0.06,
            "count": 4,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 100604,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 100605,
            "name": "PA Wall Speakers x2",
            "kind": "speaker",
            "power_kw": 0.12,
            "count": 2,
            "is_on": True,
            "start_hour": 6,
            "end_hour": 21,
            "always24x7": False
          }
        ]
      },
      {
        "id": 1007,
        "name": "A8 Board Room",
        "code": "A8",
        "kind": "hall",
        "x": 492,
        "y": 104,
        "w": 96,
        "h": 90,
        "occupied_from": 10,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 100701,
            "name": "Ceiling Fans x4",
            "kind": "fan",
            "power_kw": 0.3,
            "count": 4,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 100702,
            "name": "LED Tube Lights x8",
            "kind": "light",
            "power_kw": 0.32,
            "count": 8,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 100703,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 100704,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 100705,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 100706,
            "name": "PA Wall Speakers x4",
            "kind": "speaker",
            "power_kw": 0.24,
            "count": 4,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 100707,
            "name": "Split AC Units (3 kW)",
            "kind": "ac",
            "power_kw": 3,
            "count": 2,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          }
        ]
      },
      {
        "id": 1008,
        "name": "A23 Reception Area & Cabin",
        "code": "A23",
        "kind": "office",
        "x": 486,
        "y": 242,
        "w": 102,
        "h": 124,
        "occupied_from": 8,
        "occupied_to": 19,
        "equipment": [
          {
            "id": 100801,
            "name": "Ceiling Fans x4",
            "kind": "fan",
            "power_kw": 0.3,
            "count": 4,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 100802,
            "name": "LED Tube Lights x8",
            "kind": "light",
            "power_kw": 0.32,
            "count": 8,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 100803,
            "name": "IP CCTV Dome Cam x3",
            "kind": "cctv",
            "power_kw": 0.04,
            "count": 3,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 100804,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 100805,
            "name": "PA Wall Speakers x2",
            "kind": "speaker",
            "power_kw": 0.12,
            "count": 2,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 100806,
            "name": "Split AC Units (1.5 kW)",
            "kind": "ac",
            "power_kw": 1.5,
            "count": 1,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 100807,
            "name": "Reception Desk & Kiosk",
            "kind": "computer",
            "power_kw": 0.8,
            "count": 25,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 20,
            "always24x7": False
          }
        ]
      },
      {
        "id": 1009,
        "name": "A6 Office All Inclusive & A15 Exam Control",
        "code": "A6/A15",
        "kind": "office",
        "x": 278,
        "y": 298,
        "w": 202,
        "h": 68,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 100901,
            "name": "Ceiling Fans x6",
            "kind": "fan",
            "power_kw": 0.45,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 100902,
            "name": "LED Tube Lights x10",
            "kind": "light",
            "power_kw": 0.4,
            "count": 10,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 100903,
            "name": "IP CCTV Dome Cam x3",
            "kind": "cctv",
            "power_kw": 0.04,
            "count": 3,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 100904,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 100905,
            "name": "Split AC Units (2.5 kW)",
            "kind": "ac",
            "power_kw": 2.5,
            "count": 2,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 100906,
            "name": "Exam Control PCs x10",
            "kind": "computer",
            "power_kw": 1.8,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          }
        ]
      }
    ]
  },
  {
    "level": 1,
    "name": "Floor 1 (ECE)",
    "dept": "1st Floor — Dept. of Electronics & Communication Engg.",
    "rooms": [
      {
        "id": 2001,
        "name": "Analog & System Design Lab",
        "code": "ANALOG",
        "kind": "lab",
        "x": 12,
        "y": 12,
        "w": 96,
        "h": 62,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 200101,
            "name": "Ceiling Fans x4",
            "kind": "fan",
            "power_kw": 0.3,
            "count": 4,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 200102,
            "name": "LED Tube Lights x6",
            "kind": "light",
            "power_kw": 0.24,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 200103,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 200104,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 200105,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 200106,
            "name": "PA Wall Speakers x2",
            "kind": "speaker",
            "power_kw": 0.12,
            "count": 2,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 200107,
            "name": "CRO & Signal Workstations",
            "kind": "computer",
            "power_kw": 2.4,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          }
        ]
      },
      {
        "id": 2002,
        "name": "ACS 12 PyNest Lab",
        "code": "ACS 12",
        "kind": "lab",
        "x": 112,
        "y": 12,
        "w": 205,
        "h": 62,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 200201,
            "name": "Ceiling Fans x8",
            "kind": "fan",
            "power_kw": 0.6,
            "count": 8,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 23,
            "always24x7": False
          },
          {
            "id": 200202,
            "name": "LED Tube Lights x12",
            "kind": "light",
            "power_kw": 0.48,
            "count": 12,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 23,
            "always24x7": False
          },
          {
            "id": 200203,
            "name": "IP CCTV Dome Cam x3",
            "kind": "cctv",
            "power_kw": 0.04,
            "count": 3,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 200204,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 200205,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 23,
            "always24x7": False
          },
          {
            "id": 200206,
            "name": "PA Wall Speakers x4",
            "kind": "speaker",
            "power_kw": 0.24,
            "count": 4,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 23,
            "always24x7": False
          },
          {
            "id": 200207,
            "name": "Split AC Units (4.5 kW)",
            "kind": "ac",
            "power_kw": 4.5,
            "count": 3,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 23,
            "always24x7": False
          },
          {
            "id": 200208,
            "name": "PyNest Lab PCs x40",
            "kind": "computer",
            "power_kw": 6,
            "count": 25,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 23,
            "always24x7": False
          }
        ]
      },
      {
        "id": 2003,
        "name": "AEC 9 Advance Comm. Lab",
        "code": "AEC 9",
        "kind": "lab",
        "x": 321,
        "y": 12,
        "w": 98,
        "h": 62,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 200301,
            "name": "Ceiling Fans x4",
            "kind": "fan",
            "power_kw": 0.3,
            "count": 4,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 200302,
            "name": "LED Tube Lights x6",
            "kind": "light",
            "power_kw": 0.24,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 200303,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 200304,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 200305,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 200306,
            "name": "PA Wall Speakers x2",
            "kind": "speaker",
            "power_kw": 0.12,
            "count": 2,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 200307,
            "name": "Split AC Units (2 kW)",
            "kind": "ac",
            "power_kw": 2,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 200308,
            "name": "RF & DSP Rigs x20",
            "kind": "computer",
            "power_kw": 2.5,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          }
        ]
      },
      {
        "id": 2004,
        "name": "A15 VLSI & Signal Processing Lab",
        "code": "A15",
        "kind": "lab",
        "x": 423,
        "y": 12,
        "w": 68,
        "h": 62,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 200401,
            "name": "Ceiling Fans x4",
            "kind": "fan",
            "power_kw": 0.3,
            "count": 4,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 200402,
            "name": "LED Tube Lights x6",
            "kind": "light",
            "power_kw": 0.24,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 200403,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 200404,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 200405,
            "name": "Split AC Units (2 kW)",
            "kind": "ac",
            "power_kw": 2,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 200406,
            "name": "FPGA & Cadence PCs x25",
            "kind": "computer",
            "power_kw": 3,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          }
        ]
      },
      {
        "id": 2005,
        "name": "A36 Laboratory",
        "code": "A36",
        "kind": "lab",
        "x": 495,
        "y": 12,
        "w": 93,
        "h": 62,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 200501,
            "name": "Ceiling Fans x4",
            "kind": "fan",
            "power_kw": 0.3,
            "count": 4,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 200502,
            "name": "LED Tube Lights x6",
            "kind": "light",
            "power_kw": 0.24,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 200503,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 200504,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 200505,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 200506,
            "name": "Lab PCs x20",
            "kind": "computer",
            "power_kw": 2.2,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          }
        ]
      },
      {
        "id": 2006,
        "name": "A3 Chemistry Lab & A33 Dept",
        "code": "A3/A33",
        "kind": "lab",
        "x": 12,
        "y": 162,
        "w": 62,
        "h": 204,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 200601,
            "name": "Ceiling Fans x6",
            "kind": "fan",
            "power_kw": 0.45,
            "count": 6,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 200602,
            "name": "LED Tube Lights x10",
            "kind": "light",
            "power_kw": 0.4,
            "count": 10,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 200603,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 200604,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 200605,
            "name": "PA Wall Speakers x2",
            "kind": "speaker",
            "power_kw": 0.12,
            "count": 2,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 200606,
            "name": "Fume Hoods & Analyzers",
            "kind": "computer",
            "power_kw": 1.8,
            "count": 25,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 17,
            "always24x7": False
          }
        ]
      },
      {
        "id": 2007,
        "name": "AEC 7 Embedded & AEC 6 Digital Lab",
        "code": "AEC 6/7",
        "kind": "lab",
        "x": 134,
        "y": 172,
        "w": 106,
        "h": 96,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 200701,
            "name": "Ceiling Fans x6",
            "kind": "fan",
            "power_kw": 0.45,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 200702,
            "name": "LED Tube Lights x8",
            "kind": "light",
            "power_kw": 0.32,
            "count": 8,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 200703,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 200704,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 200705,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 200706,
            "name": "PA Wall Speakers x2",
            "kind": "speaker",
            "power_kw": 0.12,
            "count": 2,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 200707,
            "name": "Split AC Units (3 kW)",
            "kind": "ac",
            "power_kw": 3,
            "count": 2,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 200708,
            "name": "Embedded Kits & PCs x30",
            "kind": "computer",
            "power_kw": 3.2,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          }
        ]
      },
      {
        "id": 2008,
        "name": "AEC 1, AEC 2 & AEC 3 Class Rooms",
        "code": "AEC 1-3",
        "kind": "classroom",
        "x": 496,
        "y": 94,
        "w": 92,
        "h": 146,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 200801,
            "name": "Ceiling Fans x9",
            "kind": "fan",
            "power_kw": 0.67,
            "count": 9,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 200802,
            "name": "LED Tube Lights x12",
            "kind": "light",
            "power_kw": 0.48,
            "count": 12,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 200803,
            "name": "IP CCTV Dome Cam x3",
            "kind": "cctv",
            "power_kw": 0.04,
            "count": 3,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 200804,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 200805,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 200806,
            "name": "PA Wall Speakers x6",
            "kind": "speaker",
            "power_kw": 0.36,
            "count": 6,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 18,
            "always24x7": False
          }
        ]
      },
      {
        "id": 2009,
        "name": "A17 Dept of Electronics & Comm. (ECE)",
        "code": "A17",
        "kind": "office",
        "x": 78,
        "y": 304,
        "w": 186,
        "h": 62,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 200901,
            "name": "Ceiling Fans x6",
            "kind": "fan",
            "power_kw": 0.45,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 200902,
            "name": "LED Tube Lights x8",
            "kind": "light",
            "power_kw": 0.32,
            "count": 8,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 200903,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 200904,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 200905,
            "name": "Split AC Units (2 kW)",
            "kind": "ac",
            "power_kw": 2,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 200906,
            "name": "Faculty PCs x12",
            "kind": "computer",
            "power_kw": 1.5,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          }
        ]
      },
      {
        "id": 2010,
        "name": "A35 Server Room",
        "code": "A35",
        "kind": "server",
        "x": 268,
        "y": 304,
        "w": 48,
        "h": 62,
        "occupied_from": 0,
        "occupied_to": 24,
        "equipment": [
          {
            "id": 201001,
            "name": "Ceiling Fans x2",
            "kind": "fan",
            "power_kw": 0.15,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": False
          },
          {
            "id": 201002,
            "name": "LED Tube Lights x2",
            "kind": "light",
            "power_kw": 0.08,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": False
          },
          {
            "id": 201003,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 201004,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 201005,
            "name": "Split AC Units (3.5 kW)",
            "kind": "ac",
            "power_kw": 3.5,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": False
          },
          {
            "id": 201006,
            "name": "Rack Servers & Switches",
            "kind": "computer",
            "power_kw": 5.5,
            "count": 25,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": False
          }
        ]
      },
      {
        "id": 2011,
        "name": "A2 Computer Center",
        "code": "A2",
        "kind": "lab",
        "x": 320,
        "y": 304,
        "w": 166,
        "h": 62,
        "occupied_from": 8,
        "occupied_to": 18,
        "equipment": [
          {
            "id": 201101,
            "name": "Ceiling Fans x8",
            "kind": "fan",
            "power_kw": 0.6,
            "count": 8,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 21,
            "always24x7": False
          },
          {
            "id": 201102,
            "name": "LED Tube Lights x10",
            "kind": "light",
            "power_kw": 0.4,
            "count": 10,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 21,
            "always24x7": False
          },
          {
            "id": 201103,
            "name": "IP CCTV Dome Cam x3",
            "kind": "cctv",
            "power_kw": 0.04,
            "count": 3,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 201104,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 201105,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 21,
            "always24x7": False
          },
          {
            "id": 201106,
            "name": "PA Wall Speakers x2",
            "kind": "speaker",
            "power_kw": 0.12,
            "count": 2,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 21,
            "always24x7": False
          },
          {
            "id": 201107,
            "name": "Split AC Units (4 kW)",
            "kind": "ac",
            "power_kw": 4,
            "count": 3,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 21,
            "always24x7": False
          },
          {
            "id": 201108,
            "name": "Central Center PCs x45",
            "kind": "computer",
            "power_kw": 5,
            "count": 25,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 21,
            "always24x7": False
          }
        ]
      }
    ]
  },
  {
    "level": 2,
    "name": "Floor 2 (ISE & Lib)",
    "dept": "2nd Floor — Dept. of Information Science & Central Library",
    "rooms": [
      {
        "id": 3001,
        "name": "AEC 3 NCC, Project Lab & Web Wizards",
        "code": "PROJ/WEB",
        "kind": "lab",
        "x": 12,
        "y": 12,
        "w": 132,
        "h": 105,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 300101,
            "name": "Ceiling Fans x6",
            "kind": "fan",
            "power_kw": 0.45,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 300102,
            "name": "LED Tube Lights x8",
            "kind": "light",
            "power_kw": 0.32,
            "count": 8,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 300103,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 300104,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 300105,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 300106,
            "name": "Project Workstations x20",
            "kind": "computer",
            "power_kw": 2.8,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          }
        ]
      },
      {
        "id": 3002,
        "name": "Dept of Mathematics",
        "code": "MATH",
        "kind": "office",
        "x": 150,
        "y": 12,
        "w": 42,
        "h": 68,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 300201,
            "name": "Ceiling Fans x3",
            "kind": "fan",
            "power_kw": 0.22,
            "count": 3,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 300202,
            "name": "LED Tube Lights x4",
            "kind": "light",
            "power_kw": 0.16,
            "count": 4,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 300203,
            "name": "IP CCTV Dome Cam x1",
            "kind": "cctv",
            "power_kw": 0.01,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 300204,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 300205,
            "name": "Faculty PCs x5",
            "kind": "computer",
            "power_kw": 0.6,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          }
        ]
      },
      {
        "id": 3003,
        "name": "A4 Library & Information Center",
        "code": "A4 LIB",
        "kind": "hall",
        "x": 196,
        "y": 12,
        "w": 392,
        "h": 68,
        "occupied_from": 8,
        "occupied_to": 20,
        "equipment": [
          {
            "id": 300301,
            "name": "Ceiling Fans x14",
            "kind": "fan",
            "power_kw": 1.05,
            "count": 14,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 21,
            "always24x7": False
          },
          {
            "id": 300302,
            "name": "LED Tube Lights x20",
            "kind": "light",
            "power_kw": 0.8,
            "count": 20,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 21,
            "always24x7": False
          },
          {
            "id": 300303,
            "name": "IP CCTV Dome Cam x6",
            "kind": "cctv",
            "power_kw": 0.09,
            "count": 6,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 300304,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 300305,
            "name": "PA Wall Speakers x4",
            "kind": "speaker",
            "power_kw": 0.24,
            "count": 4,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 21,
            "always24x7": False
          },
          {
            "id": 300306,
            "name": "Split AC Units (5 kW)",
            "kind": "ac",
            "power_kw": 5,
            "count": 3,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 21,
            "always24x7": False
          },
          {
            "id": 300307,
            "name": "Digital Library Terminals x24",
            "kind": "computer",
            "power_kw": 3,
            "count": 25,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 21,
            "always24x7": False
          }
        ]
      },
      {
        "id": 3004,
        "name": "A5 Physics Dept & Physics Lab",
        "code": "A5",
        "kind": "lab",
        "x": 12,
        "y": 182,
        "w": 62,
        "h": 184,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 300401,
            "name": "Ceiling Fans x6",
            "kind": "fan",
            "power_kw": 0.45,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 300402,
            "name": "LED Tube Lights x10",
            "kind": "light",
            "power_kw": 0.4,
            "count": 10,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 300403,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 300404,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 300405,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 300406,
            "name": "PA Wall Speakers x2",
            "kind": "speaker",
            "power_kw": 0.12,
            "count": 2,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 300407,
            "name": "Optics & Laser Setup",
            "kind": "computer",
            "power_kw": 1.5,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          }
        ]
      },
      {
        "id": 3005,
        "name": "APC 1 & AIS 3 Class Rooms",
        "code": "APC1/AIS3",
        "kind": "classroom",
        "x": 126,
        "y": 192,
        "w": 104,
        "h": 106,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 300501,
            "name": "Ceiling Fans x6",
            "kind": "fan",
            "power_kw": 0.45,
            "count": 6,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 300502,
            "name": "LED Tube Lights x8",
            "kind": "light",
            "power_kw": 0.32,
            "count": 8,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 300503,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 300504,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 300505,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 300506,
            "name": "PA Wall Speakers x4",
            "kind": "speaker",
            "power_kw": 0.24,
            "count": 4,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 17,
            "always24x7": False
          }
        ]
      },
      {
        "id": 3006,
        "name": "ACS 9 CompilerZone, AIS 2 & AIS 1",
        "code": "ACS9/AIS",
        "kind": "lab",
        "x": 496,
        "y": 96,
        "w": 92,
        "h": 146,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 300601,
            "name": "Ceiling Fans x8",
            "kind": "fan",
            "power_kw": 0.6,
            "count": 8,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 300602,
            "name": "LED Tube Lights x12",
            "kind": "light",
            "power_kw": 0.48,
            "count": 12,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 300603,
            "name": "IP CCTV Dome Cam x3",
            "kind": "cctv",
            "power_kw": 0.04,
            "count": 3,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 300604,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 300605,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 300606,
            "name": "PA Wall Speakers x4",
            "kind": "speaker",
            "power_kw": 0.24,
            "count": 4,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 300607,
            "name": "Split AC Units (3 kW)",
            "kind": "ac",
            "power_kw": 3,
            "count": 2,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 300608,
            "name": "CompilerZone PCs x30",
            "kind": "computer",
            "power_kw": 3.5,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          }
        ]
      },
      {
        "id": 3007,
        "name": "Dept of Information Science & Engg (ISE)",
        "code": "ISE DEPT",
        "kind": "office",
        "x": 78,
        "y": 304,
        "w": 192,
        "h": 62,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 300701,
            "name": "Ceiling Fans x6",
            "kind": "fan",
            "power_kw": 0.45,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 300702,
            "name": "LED Tube Lights x8",
            "kind": "light",
            "power_kw": 0.32,
            "count": 8,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 300703,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 300704,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 300705,
            "name": "Split AC Units (2 kW)",
            "kind": "ac",
            "power_kw": 2,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 300706,
            "name": "ISE Faculty PCs x14",
            "kind": "computer",
            "power_kw": 1.6,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          }
        ]
      },
      {
        "id": 3008,
        "name": "ACS 8 CodeHub & ACS 7 TechSphere Lab",
        "code": "ACS 7/8",
        "kind": "lab",
        "x": 322,
        "y": 304,
        "w": 168,
        "h": 62,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 300801,
            "name": "Ceiling Fans x8",
            "kind": "fan",
            "power_kw": 0.6,
            "count": 8,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 21,
            "always24x7": False
          },
          {
            "id": 300802,
            "name": "LED Tube Lights x10",
            "kind": "light",
            "power_kw": 0.4,
            "count": 10,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 21,
            "always24x7": False
          },
          {
            "id": 300803,
            "name": "IP CCTV Dome Cam x3",
            "kind": "cctv",
            "power_kw": 0.04,
            "count": 3,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 300804,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 300805,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 21,
            "always24x7": False
          },
          {
            "id": 300806,
            "name": "PA Wall Speakers x2",
            "kind": "speaker",
            "power_kw": 0.12,
            "count": 2,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 21,
            "always24x7": False
          },
          {
            "id": 300807,
            "name": "Split AC Units (3.5 kW)",
            "kind": "ac",
            "power_kw": 3.5,
            "count": 2,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 21,
            "always24x7": False
          },
          {
            "id": 300808,
            "name": "CodeHub & TechSphere PCs x36",
            "kind": "computer",
            "power_kw": 4.5,
            "count": 25,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 21,
            "always24x7": False
          }
        ]
      },
      {
        "id": 3009,
        "name": "ACS 6 Seminar Hall",
        "code": "ACS 6",
        "kind": "hall",
        "x": 494,
        "y": 274,
        "w": 94,
        "h": 92,
        "occupied_from": 10,
        "occupied_to": 16,
        "equipment": [
          {
            "id": 300901,
            "name": "Ceiling Fans x6",
            "kind": "fan",
            "power_kw": 0.45,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 300902,
            "name": "LED Tube Lights x10",
            "kind": "light",
            "power_kw": 0.4,
            "count": 10,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 300903,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 300904,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 300905,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 300906,
            "name": "PA Wall Speakers x4",
            "kind": "speaker",
            "power_kw": 0.24,
            "count": 4,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 300907,
            "name": "Split AC Units (4 kW)",
            "kind": "ac",
            "power_kw": 4,
            "count": 3,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 20,
            "always24x7": False
          }
        ]
      }
    ]
  },
  {
    "level": 3,
    "name": "Floor 3 (CSE)",
    "dept": "3rd Floor — Dept. of Computer Science & Food Tech",
    "rooms": [
      {
        "id": 4001,
        "name": "ACS 1, ACS 2 & ACS 3 Class Rooms",
        "code": "ACS 1-3",
        "kind": "classroom",
        "x": 12,
        "y": 12,
        "w": 298,
        "h": 58,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 400101,
            "name": "Ceiling Fans x9",
            "kind": "fan",
            "power_kw": 0.67,
            "count": 9,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 400102,
            "name": "LED Tube Lights x12",
            "kind": "light",
            "power_kw": 0.48,
            "count": 12,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 400103,
            "name": "IP CCTV Dome Cam x3",
            "kind": "cctv",
            "power_kw": 0.04,
            "count": 3,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 400104,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 400105,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 400106,
            "name": "PA Wall Speakers x6",
            "kind": "speaker",
            "power_kw": 0.36,
            "count": 6,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 18,
            "always24x7": False
          }
        ]
      },
      {
        "id": 4002,
        "name": "ACS 4, ACV 3 & AME 3 Class Rooms",
        "code": "ACS4/AME3",
        "kind": "classroom",
        "x": 314,
        "y": 12,
        "w": 274,
        "h": 58,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 400201,
            "name": "Ceiling Fans x9",
            "kind": "fan",
            "power_kw": 0.67,
            "count": 9,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 400202,
            "name": "LED Tube Lights x12",
            "kind": "light",
            "power_kw": 0.48,
            "count": 12,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 400203,
            "name": "IP CCTV Dome Cam x3",
            "kind": "cctv",
            "power_kw": 0.04,
            "count": 3,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 400204,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 400205,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 400206,
            "name": "PA Wall Speakers x6",
            "kind": "speaker",
            "power_kw": 0.36,
            "count": 6,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 17,
            "always24x7": False
          }
        ]
      },
      {
        "id": 4003,
        "name": "Loginware & Team Chakra Robotics AI Club",
        "code": "ROBOTICS",
        "kind": "lab",
        "x": 12,
        "y": 76,
        "w": 96,
        "h": 68,
        "occupied_from": 9,
        "occupied_to": 19,
        "equipment": [
          {
            "id": 400301,
            "name": "Ceiling Fans x4",
            "kind": "fan",
            "power_kw": 0.3,
            "count": 4,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 22,
            "always24x7": False
          },
          {
            "id": 400302,
            "name": "LED Tube Lights x6",
            "kind": "light",
            "power_kw": 0.24,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 22,
            "always24x7": False
          },
          {
            "id": 400303,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 400304,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 400305,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 22,
            "always24x7": False
          },
          {
            "id": 400306,
            "name": "Split AC Units (1.5 kW)",
            "kind": "ac",
            "power_kw": 1.5,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 22,
            "always24x7": False
          },
          {
            "id": 400307,
            "name": "Robotics & ROS Rigs x12",
            "kind": "computer",
            "power_kw": 2.4,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 22,
            "always24x7": False
          }
        ]
      },
      {
        "id": 4004,
        "name": "Cell & Molecular Biology R&D Lab",
        "code": "BIO R&D",
        "kind": "lab",
        "x": 12,
        "y": 162,
        "w": 62,
        "h": 204,
        "occupied_from": 9,
        "occupied_to": 18,
        "equipment": [
          {
            "id": 400401,
            "name": "Ceiling Fans x6",
            "kind": "fan",
            "power_kw": 0.45,
            "count": 6,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 400402,
            "name": "LED Tube Lights x10",
            "kind": "light",
            "power_kw": 0.4,
            "count": 10,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 400403,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 400404,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 400405,
            "name": "Split AC Units (3 kW)",
            "kind": "ac",
            "power_kw": 3,
            "count": 2,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 400406,
            "name": "PCR, Incubators & Centrifuges",
            "kind": "computer",
            "power_kw": 2.6,
            "count": 25,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 20,
            "always24x7": False
          }
        ]
      },
      {
        "id": 4005,
        "name": "Food Technology Lab",
        "code": "FOOD LAB",
        "kind": "lab",
        "x": 128,
        "y": 192,
        "w": 78,
        "h": 86,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 400501,
            "name": "Ceiling Fans x4",
            "kind": "fan",
            "power_kw": 0.3,
            "count": 4,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 400502,
            "name": "LED Tube Lights x6",
            "kind": "light",
            "power_kw": 0.24,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 400503,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 400504,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 400505,
            "name": "Split AC Units (2 kW)",
            "kind": "ac",
            "power_kw": 2,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          },
          {
            "id": 400506,
            "name": "Food Analyzers & Ovens",
            "kind": "computer",
            "power_kw": 2.2,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 17,
            "always24x7": False
          }
        ]
      },
      {
        "id": 4006,
        "name": "Food Tech 1-4, Optics Lab & CSE HOD Office",
        "code": "CSE HOD",
        "kind": "office",
        "x": 494,
        "y": 92,
        "w": 94,
        "h": 162,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 400601,
            "name": "Ceiling Fans x8",
            "kind": "fan",
            "power_kw": 0.6,
            "count": 8,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 400602,
            "name": "LED Tube Lights x12",
            "kind": "light",
            "power_kw": 0.48,
            "count": 12,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 400603,
            "name": "IP CCTV Dome Cam x3",
            "kind": "cctv",
            "power_kw": 0.04,
            "count": 3,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 400604,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 400605,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 400606,
            "name": "Split AC Units (3 kW)",
            "kind": "ac",
            "power_kw": 3,
            "count": 2,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 400607,
            "name": "HOD & Optics Lab PCs",
            "kind": "computer",
            "power_kw": 1.8,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          }
        ]
      },
      {
        "id": 4007,
        "name": "A8 CSE Faculty Room",
        "code": "A8 CSE",
        "kind": "office",
        "x": 82,
        "y": 304,
        "w": 158,
        "h": 62,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 400701,
            "name": "Ceiling Fans x6",
            "kind": "fan",
            "power_kw": 0.45,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 400702,
            "name": "LED Tube Lights x8",
            "kind": "light",
            "power_kw": 0.32,
            "count": 8,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 400703,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 400704,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 400705,
            "name": "PA Wall Speakers x2",
            "kind": "speaker",
            "power_kw": 0.12,
            "count": 2,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 400706,
            "name": "Split AC Units (2 kW)",
            "kind": "ac",
            "power_kw": 2,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 400707,
            "name": "CSE Faculty Laptops x18",
            "kind": "computer",
            "power_kw": 2,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          }
        ]
      },
      {
        "id": 4008,
        "name": "ACS 10 Laboratory",
        "code": "ACS 10",
        "kind": "lab",
        "x": 244,
        "y": 304,
        "w": 124,
        "h": 62,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 400801,
            "name": "Ceiling Fans x6",
            "kind": "fan",
            "power_kw": 0.45,
            "count": 6,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 400802,
            "name": "LED Tube Lights x8",
            "kind": "light",
            "power_kw": 0.32,
            "count": 8,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 400803,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 400804,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 400805,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 400806,
            "name": "PA Wall Speakers x2",
            "kind": "speaker",
            "power_kw": 0.12,
            "count": 2,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 400807,
            "name": "Split AC Units (3 kW)",
            "kind": "ac",
            "power_kw": 3,
            "count": 2,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 400808,
            "name": "ACS 10 Lab PCs x35",
            "kind": "computer",
            "power_kw": 4.2,
            "count": 25,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 20,
            "always24x7": False
          }
        ]
      },
      {
        "id": 4009,
        "name": "ACS 11 Pragma Lab",
        "code": "ACS 11",
        "kind": "lab",
        "x": 372,
        "y": 304,
        "w": 118,
        "h": 62,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 400901,
            "name": "Ceiling Fans x6",
            "kind": "fan",
            "power_kw": 0.45,
            "count": 6,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 22,
            "always24x7": False
          },
          {
            "id": 400902,
            "name": "LED Tube Lights x8",
            "kind": "light",
            "power_kw": 0.32,
            "count": 8,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 22,
            "always24x7": False
          },
          {
            "id": 400903,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 400904,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 400905,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 22,
            "always24x7": False
          },
          {
            "id": 400906,
            "name": "PA Wall Speakers x2",
            "kind": "speaker",
            "power_kw": 0.12,
            "count": 2,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 22,
            "always24x7": False
          },
          {
            "id": 400907,
            "name": "Split AC Units (3.5 kW)",
            "kind": "ac",
            "power_kw": 3.5,
            "count": 2,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 22,
            "always24x7": False
          },
          {
            "id": 400908,
            "name": "Pragma Lab PCs x40",
            "kind": "computer",
            "power_kw": 5,
            "count": 25,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 22,
            "always24x7": False
          }
        ]
      },
      {
        "id": 4010,
        "name": "AEC 5 Seminar Hall",
        "code": "AEC 5",
        "kind": "hall",
        "x": 494,
        "y": 274,
        "w": 94,
        "h": 92,
        "occupied_from": 10,
        "occupied_to": 16,
        "equipment": [
          {
            "id": 401001,
            "name": "Ceiling Fans x6",
            "kind": "fan",
            "power_kw": 0.45,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 401002,
            "name": "LED Tube Lights x10",
            "kind": "light",
            "power_kw": 0.4,
            "count": 10,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 401003,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 401004,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 401005,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 401006,
            "name": "PA Wall Speakers x4",
            "kind": "speaker",
            "power_kw": 0.24,
            "count": 4,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 401007,
            "name": "Split AC Units (4 kW)",
            "kind": "ac",
            "power_kw": 4,
            "count": 3,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          }
        ]
      }
    ]
  },
  {
    "level": 4,
    "name": "Floor 4 (AIC)",
    "dept": "4th Floor — Atal Incubation Centre (JIT Foundation)",
    "rooms": [
      {
        "id": 5001,
        "name": "AIC Hub & E2E / Praana / Ameliorate Biotech",
        "code": "AIC NORTH-W",
        "kind": "lab",
        "x": 12,
        "y": 12,
        "w": 294,
        "h": 58,
        "occupied_from": 9,
        "occupied_to": 18,
        "equipment": [
          {
            "id": 500101,
            "name": "Ceiling Fans x8",
            "kind": "fan",
            "power_kw": 0.6,
            "count": 8,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 500102,
            "name": "LED Tube Lights x12",
            "kind": "light",
            "power_kw": 0.48,
            "count": 12,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 500103,
            "name": "IP CCTV Dome Cam x4",
            "kind": "cctv",
            "power_kw": 0.06,
            "count": 4,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 500104,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 500105,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 500106,
            "name": "PA Wall Speakers x2",
            "kind": "speaker",
            "power_kw": 0.12,
            "count": 2,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 500107,
            "name": "Split AC Units (4 kW)",
            "kind": "ac",
            "power_kw": 4,
            "count": 3,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 500108,
            "name": "Biotech Startup Suites",
            "kind": "computer",
            "power_kw": 3.2,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          }
        ]
      },
      {
        "id": 5002,
        "name": "Next Big Innovations, Veripure, Bioaryha & Nuvohelix",
        "code": "AIC NORTH-E",
        "kind": "lab",
        "x": 310,
        "y": 12,
        "w": 278,
        "h": 58,
        "occupied_from": 9,
        "occupied_to": 18,
        "equipment": [
          {
            "id": 500201,
            "name": "Ceiling Fans x8",
            "kind": "fan",
            "power_kw": 0.6,
            "count": 8,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 500202,
            "name": "LED Tube Lights x12",
            "kind": "light",
            "power_kw": 0.48,
            "count": 12,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 500203,
            "name": "IP CCTV Dome Cam x4",
            "kind": "cctv",
            "power_kw": 0.06,
            "count": 4,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 500204,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 500205,
            "name": "Split AC Units (3.5 kW)",
            "kind": "ac",
            "power_kw": 3.5,
            "count": 2,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 500206,
            "name": "Incubation R&D Pods",
            "kind": "computer",
            "power_kw": 2.8,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          }
        ]
      },
      {
        "id": 5003,
        "name": "AIC Main Lounge & Language Lab",
        "code": "AIC LOUNGE",
        "kind": "hall",
        "x": 12,
        "y": 74,
        "w": 112,
        "h": 108,
        "occupied_from": 9,
        "occupied_to": 18,
        "equipment": [
          {
            "id": 500301,
            "name": "Ceiling Fans x6",
            "kind": "fan",
            "power_kw": 0.45,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 500302,
            "name": "LED Tube Lights x8",
            "kind": "light",
            "power_kw": 0.32,
            "count": 8,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 500303,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 500304,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 500305,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 500306,
            "name": "PA Wall Speakers x4",
            "kind": "speaker",
            "power_kw": 0.24,
            "count": 4,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 500307,
            "name": "Split AC Units (2.5 kW)",
            "kind": "ac",
            "power_kw": 2.5,
            "count": 2,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 500308,
            "name": "Language Audio Pods x20",
            "kind": "computer",
            "power_kw": 1.8,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          }
        ]
      },
      {
        "id": 5004,
        "name": "Plant & Microbial Tech / Inks & Sensor Lab",
        "code": "SENSOR LAB",
        "kind": "lab",
        "x": 12,
        "y": 190,
        "w": 62,
        "h": 176,
        "occupied_from": 9,
        "occupied_to": 18,
        "equipment": [
          {
            "id": 500401,
            "name": "Ceiling Fans x6",
            "kind": "fan",
            "power_kw": 0.45,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 500402,
            "name": "LED Tube Lights x10",
            "kind": "light",
            "power_kw": 0.4,
            "count": 10,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 500403,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 500404,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 500405,
            "name": "Split AC Units (2.5 kW)",
            "kind": "ac",
            "power_kw": 2.5,
            "count": 2,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 500406,
            "name": "Biosensor & Ink Plotters",
            "kind": "computer",
            "power_kw": 2.4,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          }
        ]
      },
      {
        "id": 5005,
        "name": "AIC SIF & Pranna Discoveries",
        "code": "AIC SIF",
        "kind": "lab",
        "x": 124,
        "y": 192,
        "w": 82,
        "h": 86,
        "occupied_from": 9,
        "occupied_to": 18,
        "equipment": [
          {
            "id": 500501,
            "name": "Ceiling Fans x4",
            "kind": "fan",
            "power_kw": 0.3,
            "count": 4,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 500502,
            "name": "LED Tube Lights x6",
            "kind": "light",
            "power_kw": 0.24,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 500503,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 500504,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 500505,
            "name": "Split AC Units (2 kW)",
            "kind": "ac",
            "power_kw": 2,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          },
          {
            "id": 500506,
            "name": "SIF Prototyping Gear",
            "kind": "computer",
            "power_kw": 1.6,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 18,
            "always24x7": False
          }
        ]
      },
      {
        "id": 5006,
        "name": "Training Hall & Tattva AI Startup Hub",
        "code": "TATTVA AI",
        "kind": "hall",
        "x": 494,
        "y": 88,
        "w": 94,
        "h": 158,
        "occupied_from": 9,
        "occupied_to": 18,
        "equipment": [
          {
            "id": 500601,
            "name": "Ceiling Fans x6",
            "kind": "fan",
            "power_kw": 0.45,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 500602,
            "name": "LED Tube Lights x10",
            "kind": "light",
            "power_kw": 0.4,
            "count": 10,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 500603,
            "name": "IP CCTV Dome Cam x3",
            "kind": "cctv",
            "power_kw": 0.04,
            "count": 3,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 500604,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 500605,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 500606,
            "name": "PA Wall Speakers x4",
            "kind": "speaker",
            "power_kw": 0.24,
            "count": 4,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 500607,
            "name": "Split AC Units (3.5 kW)",
            "kind": "ac",
            "power_kw": 3.5,
            "count": 2,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 500608,
            "name": "Tattva AI Servers & Desks",
            "kind": "computer",
            "power_kw": 3,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 20,
            "always24x7": False
          }
        ]
      },
      {
        "id": 5007,
        "name": "Autonomous System Lab",
        "code": "AUTO LAB",
        "kind": "lab",
        "x": 82,
        "y": 304,
        "w": 122,
        "h": 62,
        "occupied_from": 9,
        "occupied_to": 18,
        "equipment": [
          {
            "id": 500701,
            "name": "Ceiling Fans x4",
            "kind": "fan",
            "power_kw": 0.3,
            "count": 4,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 500702,
            "name": "LED Tube Lights x6",
            "kind": "light",
            "power_kw": 0.24,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 500703,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 500704,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 500705,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 500706,
            "name": "Split AC Units (2.5 kW)",
            "kind": "ac",
            "power_kw": 2.5,
            "count": 2,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 500707,
            "name": "Drone & Rover Simulators",
            "kind": "computer",
            "power_kw": 3.2,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          }
        ]
      },
      {
        "id": 5008,
        "name": "AIS 9 Vision Nest Lab",
        "code": "AIS 9",
        "kind": "lab",
        "x": 208,
        "y": 304,
        "w": 132,
        "h": 62,
        "occupied_from": 9,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 500801,
            "name": "Ceiling Fans x6",
            "kind": "fan",
            "power_kw": 0.45,
            "count": 6,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 23,
            "always24x7": False
          },
          {
            "id": 500802,
            "name": "LED Tube Lights x8",
            "kind": "light",
            "power_kw": 0.32,
            "count": 8,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 23,
            "always24x7": False
          },
          {
            "id": 500803,
            "name": "IP CCTV Dome Cam x3",
            "kind": "cctv",
            "power_kw": 0.04,
            "count": 3,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 500804,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 500805,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 23,
            "always24x7": False
          },
          {
            "id": 500806,
            "name": "PA Wall Speakers x2",
            "kind": "speaker",
            "power_kw": 0.12,
            "count": 2,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 23,
            "always24x7": False
          },
          {
            "id": 500807,
            "name": "Split AC Units (3.5 kW)",
            "kind": "ac",
            "power_kw": 3.5,
            "count": 2,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 23,
            "always24x7": False
          },
          {
            "id": 500808,
            "name": "Vision Nest GPU Workstations",
            "kind": "computer",
            "power_kw": 5.5,
            "count": 25,
            "is_on": True,
            "start_hour": 8,
            "end_hour": 23,
            "always24x7": False
          }
        ]
      },
      {
        "id": 5009,
        "name": "AIS 8 C-Brains Lab",
        "code": "AIS 8",
        "kind": "lab",
        "x": 344,
        "y": 304,
        "w": 146,
        "h": 62,
        "occupied_from": 9,
        "occupied_to": 18,
        "equipment": [
          {
            "id": 500901,
            "name": "Ceiling Fans x6",
            "kind": "fan",
            "power_kw": 0.45,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 500902,
            "name": "LED Tube Lights x8",
            "kind": "light",
            "power_kw": 0.32,
            "count": 8,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 500903,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 500904,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 500905,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 500906,
            "name": "PA Wall Speakers x2",
            "kind": "speaker",
            "power_kw": 0.12,
            "count": 2,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 500907,
            "name": "Split AC Units (3 kW)",
            "kind": "ac",
            "power_kw": 3,
            "count": 2,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 20,
            "always24x7": False
          },
          {
            "id": 500908,
            "name": "C-Brains Neural Rigs x30",
            "kind": "computer",
            "power_kw": 4,
            "count": 25,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 20,
            "always24x7": False
          }
        ]
      },
      {
        "id": 5010,
        "name": "AIC Seminar Hall",
        "code": "AIC SEM",
        "kind": "hall",
        "x": 494,
        "y": 274,
        "w": 94,
        "h": 92,
        "occupied_from": 10,
        "occupied_to": 17,
        "equipment": [
          {
            "id": 501001,
            "name": "Ceiling Fans x6",
            "kind": "fan",
            "power_kw": 0.45,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 501002,
            "name": "LED Tube Lights x10",
            "kind": "light",
            "power_kw": 0.4,
            "count": 10,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 501003,
            "name": "IP CCTV Dome Cam x2",
            "kind": "cctv",
            "power_kw": 0.03,
            "count": 2,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 501004,
            "name": "Smart DB & Meter Panel",
            "kind": "electrical",
            "power_kw": 0.05,
            "count": 1,
            "is_on": True,
            "start_hour": 0,
            "end_hour": 24,
            "always24x7": True
          },
          {
            "id": 501005,
            "name": "HD Ceiling Projector",
            "kind": "projector",
            "power_kw": 0.35,
            "count": 1,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 501006,
            "name": "PA Wall Speakers x6",
            "kind": "speaker",
            "power_kw": 0.36,
            "count": 6,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          },
          {
            "id": 501007,
            "name": "Split AC Units (4 kW)",
            "kind": "ac",
            "power_kw": 4,
            "count": 3,
            "is_on": True,
            "start_hour": 9,
            "end_hour": 19,
            "always24x7": False
          }
        ]
      }
    ]
  }
]


def seed(db) -> None:
    if db.query(Building).count():
        return

    for f in FLOORS_SEED:
        building = Building(name=f["name"], floor_level=f["level"], dept=f["dept"])
        for r in f["rooms"]:
            room = Room(
                code=r["code"],
                name=r["name"],
                kind=r["kind"],
                x=r["x"], y=r["y"], w=r["w"], h=r["h"],
                occupied_from=r["occupied_from"],
                occupied_to=r["occupied_to"],
            )
            room.equipment = [
                Equipment(
                    name=e["name"],
                    kind=e["kind"],
                    count=e.get("count", 1),
                    power_kw=e["power_kw"],
                    is_on=e["is_on"],
                    start_hour=e["start_hour"],
                    end_hour=e["end_hour"],
                )
                for e in r["equipment"]
            ]
            building.rooms.append(room)
        db.add(building)
    db.flush()

    midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    readings = []
    for room in db.query(Room).all():
        for h in range(24 * 7):
            ts = midnight - timedelta(hours=h + 1)
            kwh = sum(e.power_kw for e in room.equipment if e.start_hour <= ts.hour < e.end_hour)
            kwh *= (0.35 if ts.weekday() >= 5 else 1.0) * random.uniform(0.92, 1.08)
            readings.append(EnergyReading(room_id=room.id, ts=ts, kwh=round(kwh, 3)))
    db.add_all(readings)
    db.commit()
