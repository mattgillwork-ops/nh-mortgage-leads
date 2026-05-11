echo '#!/bin/bash' > stress_test.sh
echo 'for i in {1..10}; do ./send_payload.sh & done' >> stress_test.sh
echo './check_inbox.sh' >> stress_test.sh
chmod +x stress_test.sh
