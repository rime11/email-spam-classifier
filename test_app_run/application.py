print("=== RUNNING NEW APPLICATION.PY ===")

from flask import Flask
import os, sys, logging 

#initialize falsk app
app = Flask(__name__)

# --- Logging setup ---
# Send all logs to stdout (so EB collects them into web.stdout.log)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,  # change to DEBUG for more detail
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

@app.route("/")
def test():
    return('Hellow new test app')

@app.route("/debug")
def debug():
    return f"Current dir: {os.getcwd()}, Python version: {os.sys.version}"

application = app  

if __name__=='__main__':
    logger.info("Starting Flask app locally...")
    app.run(host="0.0.0.0", port=5000)
 