# // [TASK]: Create a script to run py-spy and generate a flamegraph
# // [GOAL]: Profile the application to identify performance bottlenecks
# // [ELITE_CURSOR_SNIPPET]: aihandle

#!/bin/bash

# Ensure py-spy is installed
pip install py-spy

# Run your application in the background
# Replace 'python your_app.py' with the command to start your FastAPI application
python api_server.py &

# Get the PID of your application
APP_PID=$!

echo "Application started with PID: $APP_PID"
echo "Profiling for 30 seconds..."

# Run py-spy to generate a flamegraph
py-spy record -o profile.svg --pid $APP_PID --duration 30

echo "Profiling complete. Flamegraph saved to profile.svg"

# Kill the application
kill $APP_PID