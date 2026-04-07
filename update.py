
from subprocess import run as srun
import logging
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)

UPSTREAM_REPO = os.getenv("UPSTREAM_REPO")
UPSTREAM_BRANCH = os.getenv("UPSTREAM_BRANCH", "master")

if UPSTREAM_REPO is not None:
    if os.path.exists('.git'):
        srun(["rm", "-rf", ".git"])

    update = srun([f"git init -q \
                     && git add . \
                     && git commit -sm update -q \
                     && git remote add origin {UPSTREAM_REPO} \
                     && git fetch origin -q \
                     && git reset --hard origin/{UPSTREAM_BRANCH} -q"], shell=True)

    if update.returncode == 0:
        logging.info('Successfully updated with latest commit from UPSTREAM_REPO')
    else:
        logging.error('Something went wrong while updating, check UPSTREAM_REPO if valid or not!')
