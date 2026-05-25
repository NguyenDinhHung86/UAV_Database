#!/usr/bin/env python3
"""
UAV Database — Khởi chạy ứng dụng
"""
import sys
import os

# Đảm bảo đường dẫn đúng khi chạy từ bất kỳ thư mục nào
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import main

if __name__ == "__main__":
    main()
