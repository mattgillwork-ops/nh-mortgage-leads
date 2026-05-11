echo '#!/bin/bash' > send_payload.sh
echo 'curl -X POST http://localhost:2525/inbound -H "Content-Type: application/json" -d '\''{"key":"value"}'\'' >> payload.log' >> send_payload.sh
chmod +x send_payload.sh
