echo '#!/bin/bash' > check_inbox.sh
echo 'curl http://localhost:2525/tru/Inbox/' >> check_inbox.sh
chmod +x check_inbox.sh
