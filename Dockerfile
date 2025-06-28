FROM python:3.11-slim

WORKDIR /app

# Install uv globally
RUN pip install --no-cache-dir uv

# Copy all files
COPY . /app

# Create .venv and install project dependencies into it
RUN uv venv && \
    uv pip install --editable .

# Expose Streamlit port
EXPOSE 8501

# Use Streamlit from the virtual environment
CMD [".venv/bin/streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
