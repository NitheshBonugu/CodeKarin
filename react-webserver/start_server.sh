#!/bin/bash

python3 -m http.server 80 -d tmp &

serve -s build -l 443
