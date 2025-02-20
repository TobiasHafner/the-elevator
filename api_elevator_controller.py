import threading
import time
import uuid
from hashlib import sha256

from flask import Flask, jsonify, request, Response, render_template_string, make_response

from elevator import Elevator
from elevator_scheduler import Scheduler
from fluctuating_request_controller import FluctuatingRequestController
from request_generator import RequestGenerator
from ride_log import RideLog
from scheduler_moves import Moves
from statistics import Statistics
from virtual_clock import VirtualClock

# Constants
FLOOR_COUNT = 16
MAX_LOAD = 1200
ITERATION_INTERVAL = 0.5
STOP_TIME = 1

# Initialize Flask app
app = Flask(__name__)

# Initialize Elevator and Scheduler
elevator = Elevator(FLOOR_COUNT, MAX_LOAD)
scheduler = Scheduler(elevator)
clock = VirtualClock(scale=24)
request_controller = FluctuatingRequestController(clock)
request_generator = RequestGenerator(FLOOR_COUNT, request_controller)
statistics = Statistics(clock)
ride_log = RideLog(clock)


def run_elevator():
    """ Runs the elevator continuously in a separate thread."""
    while True:
        # Generate random requests
        request = request_generator.generate_request()
        split = request.split()
        if len(split) != 0:
            start = int(split[0])
            end = int(split[1])
            scheduler.handle_request(start, end)
            statistics.track_ride(start, end)
            ride_log.log_ride(start, end)

        # Process elevator moves
        move = scheduler.get_next_move()
        match move:
            case Moves.UP:
                elevator.close_doors()
                elevator.move_up()
            case Moves.STOP:
                elevator.open_doors()
            case Moves.DOWN:
                elevator.close_doors()
                elevator.move_down()
            case Moves.STAY:
                elevator.close_doors()

        if (elevator.get_door_state()):
            time.sleep(STOP_TIME)
        time.sleep(ITERATION_INTERVAL)


@app.route('/elevator/stream', methods=['GET'])
def stream_elevator():
    """ Streams the elevator state in real-time. """

    def generate():
        while True:
            # Generate the full elevator status
            elevator_status = str(elevator)  # Assuming 'elevator' is a valid object
            scheduler_status = str(scheduler)  # Assuming 'scheduler' is a valid object
            current_time = f"Current Time: {str(clock)}"

            # Format the ASCII output correctly
            ascii_output = f"{current_time}\n\n{elevator_status}\n{scheduler_status}"

            # Properly format as SSE
            formatted_data = "\n".join([f"data: {line}" for line in ascii_output.split("\n")])
            yield f"{formatted_data}\n\n"

            time.sleep(ITERATION_INTERVAL)  # Assuming ITERATION_INTERVAL is defined

    return Response(generate(), mimetype='text/event-stream')


@app.route('/elevator')
def index():
    """ Serves a simple webpage to display elevator status."""
    return render_template_string('''
        <!DOCTYPE html>
<html>
<head>
    <title>Elevator Monitor</title>
    <style>
        body { font-family: monospace; white-space: pre-wrap; }
        pre { font-size: 16px; }
    </style>
</head>
<body>
    <h1>Realtime Elevator View</h1>
    <pre id="output">Connecting...</pre>
    <script>
        const output = document.getElementById("output");
        const eventSource = new EventSource("/elevator/stream");

        eventSource.onmessage = function(event) {
            output.textContent = event.data;  // Use textContent to preserve formatting
        };

        eventSource.onerror = function() {
            output.textContent = "Connection lost. Trying to reconnect...";
        };
    </script>
</body>
</html>
    ''')


@app.route('/elevator/current_time', methods=['GET'])
def get_current_time():
    """ Returns the current time of the virtual clock."""
    return jsonify(str(clock))


@app.route('/elevator/cabin_state', methods=['GET'])
def get_elevator_state():
    """ Returns the current state of the elevator."""
    return jsonify(elevator.get_state())


@app.route('/elevator/scheduler_state', methods=['GET'])
def get_scheduler_state():
    """ Returns the current state of the scheduler."""
    return jsonify(scheduler.get_state())


@app.route('/elevator/statistics', methods=['GET'])
def get_stats():
    """ Returns the current statistics of the elevator."""
    return jsonify(statistics.get())

@app.route('/elevator/log', methods=['GET'])
def get_log():
    """ Returns the current statistics of the elevator."""
    return jsonify(ride_log.get())


@app.route('/elevator/request_ride', methods=['GET'])
def request_ride():
    """ Handles ride requests with start and end floors."""
    start = request.args.get('start', type=int)
    end = request.args.get('end', type=int)

    if start is None or end is None:
        return jsonify({'error': 'Missing start or end floor'}), 400

    if not (0 <= start < FLOOR_COUNT and 0 <= end < FLOOR_COUNT):
        return jsonify({'error': 'Invalid floor range'}), 400

    scheduler.handle_request(start, end)
    statistics.track_ride(start, end)

    response = jsonify({'message': 'Ride requested successfully'});

    user_id = request.cookies.get("user_id")
    if not user_id:
        user_id = str(uuid.uuid4())
        response.set_cookie("user_id", user_id, max_age=60 * 60 * 24 * 365)

    id = sha256(user_id.encode("utf-8")).hexdigest()
    ride_log.log_ride(start, end, id)
    return response


if __name__ == "__main__":
    # Start the elevator loop in a separate thread
    elevator_thread = threading.Thread(target=run_elevator, daemon=True)
    elevator_thread.start()

    app.run(host='0.0.0.0', port=5000, debug=True)
