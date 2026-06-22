#!/usr/bin/env python3
"""
Simple server launcher for EduGuard backend.
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

import uvicorn
from main import app

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)
