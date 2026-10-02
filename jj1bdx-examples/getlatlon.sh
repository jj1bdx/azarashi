gnssstreamer --socket 172.29.189.81:50012 --msgfilter NAV-PVT --clioutput 4 --output "lambda msg: print(f'{msg.lat} {msg.lon}')"
