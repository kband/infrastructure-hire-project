# Locust.io load tester

## Quickstart

build the container ```docker build . -t locust``` and run it with ```docker run -p 8089:8089 -e TARGET_URL=https://ops-hire-project.cs1.nls.systems locust:latest``` connect to localhost:8089, and set the number of workers (21 is just enough to trip the cpu based autoscale group to kick in) and spawn rate (doesn't really matter, 0.25 is nice and slow)

This basic test will fire one request per worker, every second (regardless of response time), hitting /, /status and /slow/25 33% of the time each. "/slow/25" taking hundreds of milliseconds to run, the others single digit milliseconds.

