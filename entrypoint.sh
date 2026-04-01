#!/bin/bash

nohup socat TCP-LISTEN:4000,bind=0.0.0.0,fork,reuseaddr TCP:127.0.0.1:50000 > /dev/null 2>&1 &

warp-svc