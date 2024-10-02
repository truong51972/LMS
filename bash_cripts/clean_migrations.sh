#!/bin/bash

# Xóa các tệp .py trong thư mục migrations, trừ __init__.py, và bỏ qua thư mục .venv
find . -path "./.venv" -prune -o -path "*/migrations/*.py" -not -name "__init__.py" -exec rm -f {} +

# Xóa các tệp .pyc trong thư mục migrations và bỏ qua thư mục .venv
find . -path "./.venv" -prune -o -path "*/migrations/*.pyc" -exec rm -f {} +
