#!/bin/bash
rsync -rvzP ./dist/ lukas@lw1.at:/srv/server/RadioStats/dist/ --fuzzy --delete-after -v
