#!/bin/bash
rsync -rvzP ./build/ lukas@lw1.at:/srv/server/RadioStats/dist/ --fuzzy --delete-after -v
