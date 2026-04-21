
#!/bin/bash
pgrep -af uvicorn || echo "Server not running"
