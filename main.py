import subprocess
import sys

def main():
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=False)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()