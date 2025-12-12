# The Elevator

This project you are looking at contains a fully simulated elevator system with a virtual clock, scheduler, a virtual population of people using the elevator, ride logging, and a real-time ASCII-art stream. A REST-API is provided allowing to query the ride logs, the current state of the system as well as to request rides.

This project can be used as:
- A mock data generator
- A mock API endpoint returning deterministic, structured JSON suitable for automated testing, prototyping, or UI development.
- Something interesting to run in the background that you can use to kill time while looking at ASCII art

## Getting Started
This project is designed to run as a standalone Python application using a virtual environment. Follow the steps below to set up the environment, install all dependencies, and launch the elevator simulation server.

1. Clone the Repository:
```bash
git clone git@github.com:TobiasHafner/the-elevator.git
cd elevator_project
```

2. Create a Virtual Environment...
```bash
python3 -m venv .venv
```

... and activate it.

**Linux / macOS**
```bash
source .venv/bin/activate
```

**Windows**
```powershell
.venv\Scripts\Activate.ps1
```

3. Install Dependencies
This project uses PEP 621 and pyproject.toml to define its dependencies.

Install everything with:
```bash
pip install -e .
```
The -e (editable mode) allows you to run the project directly from the source without reinstalling after changes.

Alternatively, to install only the declared dependencies:
```bash
pip install .
```

4. Launch the Application
The project provides an entry point via Python’s module system.
From inside the activated virtual environment, run:
```bash
python -m app.main
```

The server will typically start on: `http://127.0.0.1:5000`.
To open the live ASCII-art in browser: `http://localhost:5000/elevator`

5. Stopping the Server
Simply use `Ctrl + C`.

## API Documentation
All endpoints are prefixed with: `/elevator`.

### GET `/elevator/stream`
This endpoint continuously streams ASCII-art frames of the elevator simulation using Server-Sent Events (SSE). The ASCII-art is thereby sent as a single string containing all the formatting required.

- Returns text/event-stream
- Sends a new frame each simulation tick
- Ideal for dashboards or live monitoring

### GET `/elevator`
Serves a simple HTML page that displays the real-time elevator state streamed from `/elevator/stream`.
Great for debugging and procrastination.

### GET `/elevator/current_time`
This endpoint returns the current time and date in the simulation.
The string returned is of the form: '"HH:MM:SS"'. Example: "12:03:22"

### GET `/elevator/cabin_state`
Returns the current elevator cabin state. This includes wether the doors are open or closed, the number of floors the elevator serves, the current load of the cabin in kg, the maximum load allowed as well as the floor the cabin is currently at.

Example:
```json
{
  "doors_open": false,
  "floor_count": 17,
  "load": 0,
  "max_load": 1200,
  "position": 8
}
```

### GET `/elevator/scheduler_state`
Returns internal scheduler data. This data consists of the number of floors the elevator serves followed by sections dedicated to each of the floors. For each floor three types of requests are listed. First, the requests to travel from the current floor to floors of lower numbers. The list contains the floor numbers of the destination floors. Second, requests to travel to floors above the current one. Here as well the destination floor numbers are listed. The third kind of requests listed are requests to stop at the current floor. Here only the number of requests is reported. Finally each of the floor sections reports the number of the floor it is associated with.

```json
{
  "floor_count": 2,
  "floors": [
    {
      "down_requests": [],
      "floor": 1,
      "stop_requests": 0,
      "up_requests": []
    },
    {
      "down_requests": [],
      "floor": 0,
      "stop_requests": 0,
      "up_requests": []
    }
  ]
}
```

### GET `/elevator/statistics`
Returns aggregated statistical data collected throughout the simulation. These statistics summarize how the elevator has been used over time. The following data is provided:
- **average_distance**: Average travel distance in floors across all recorded rides.
- **average_from_distance_by_floor**: Average distance traveled from each floor. This describes how far passengers starting at a given floor typically travel.
- **average_to_distance_by_floor**: Average distance traveled to each floor. This describes how far passengers ending at a given floor typically traveled.
- **departures**: Departures per floor. The number of rides that originated at each floor.
- **destinations**: Destinations per floor. The number of rides that ended at each floor.
- **hourly_heatmap**: Hourly heatmap. A histogram of ride frequency grouped by hour of the day in simulation time.
- **total_rides**: Total number of rides performed so far.

Below is an example for a two-story simulation:

```json
{
  "average_distance": 3.2,
  "average_from_distance_by_floor": {
    "0": 3.0,
    "1": 3.4
  },
  "average_to_distance_by_floor": {
    "0": 3.5,
    "1": 2.9
  },
  "departures": {
    "0": 58,
    "1": 62
  },
  "destinations": {
    "0": 61,
    "1": 59
  },
  "hourly_heatmap": {
    "0": 2,
    "1": 4,
    "2": 5,
    "3": 3,
    "4": 2,
    "5": 6,
    "6": 8,
    "7": 12,
    "8": 14,
    "9": 9,
    "10": 8,
    "11": 7
  },
  "total_rides": 120
}
```

### GET `/elevator/log`
Returns a chronological list of all recorded elevator rides. Each entry represents a completed (or logged) ride, together with metadata about the rider, timing information, and the associated floors.

Every ride entry contains the following fields:
- **start**: The floor where the ride began.
- **end**: The floor where the ride ended.
- **person_id**: A persistent anonymized identifier. This identifier is stable across sessions, allowing repeated rides by the same simulated user to be recognized.
- **role**: The simulated role of the passenger (e.g., "OfficeRole" or other behavior models). This can be used to study different mobility patterns of the simulated population.
- **real_time**: The real-world Unix timestamp (in seconds) at which the ride was logged. This enables correlation between simulation events and actual time.
- **virtual_time**: The time within the simulation’s virtual clock when the ride occurred.

Example of a log consisting of two rides:
```json
[
  {
    "start": 9,
    "end": 7,
    "person_id": "920cb2bf-c1f8-4868-a56a-64d8b624fcd2",
    "role": "OfficeRole",
    "real_time": 1765554689,
    "virtual_time": 263
  },
  {
    "start": 1,
    "end": 0,
    "person_id": "53ad716e-343f-47a5-b3ad-7deac2696b10",
    "role": "OfficeRole",
    "real_time": 1765554702,
    "virtual_time": 275
  }
]
```

The ride log can store up to 1000 entries after which it operates as a FiFo queue.

### GET `/elevator/population`
Returns a summary of the current simulated population inside the building. Each entry corresponds to a role type and indicates how many simulated people of that role are currently active in the building model. These roles represent different categories of occupants, each with its own mobility pattern and behavior. The exact set of roles may vary depending on the simulation configuration.

```json
{
  "CleaningRole": 11,
  "ExecutiveRole": 2,
  "MaintenanceRole": 10,
  "OfficeRole": 45,
  "ResearchRole": 24,
  "SecurityRole": 4,
  "StorageRole": 4
}
```

### GET `/elevator/population`
Triggers a simulated ride request in the elevator system. This endpoint behaves like a user pressing a “call button” on a specific floor and selecting a destination floor inside the cabin. It is used both for interactive control of the simulation and for generating synthetic ride activity when using the system as a mock API / load generator.

**Parameters**:
- **start**: The floor where the passenger begins the ride.
- **end**: The floor the passenger wants to travel to.

Both parameters are always required and must be within the valid range of floors for the current building configuration.

**Behavior**:
When a valid request is sent:
1. The scheduler is notified of the ride request (scheduler.handle_request(start, end)).
2. Statistics are updated to reflect the new trip.
3. A persistent user ID cookie is created if the client does not already have one (the cookie lasts one year).
4. A hashed person_id is generated from that cookie to consistently identify the same passenger.
5. The ride is appended to the ride log for analytics.

**Successful Response**:
```json
{
  "message": "Ride requested successfully"
}
```

A cookie named user_id may also be included in the response headers if none existed previously.

**Error Cases**:
If either parameter is missing:
```json
{
    "error": "Missing start or end floor"
}
```

If a floor is outside the building’s valid range:
```json
{
    "error": "Invalid floor range"
}
```

**Example**:
```bash
http://localhost:5000/elevator/request_ride?start=1&end=0
```
