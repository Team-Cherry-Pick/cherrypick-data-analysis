import sys
import subprocess

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1]

        if mode == "fmkorea":
            from fmkorea_crawler import fmkorea_crawl
            fmkorea_crawl()

        elif mode == "serve":
            import data_analysis
            subprocess.run(["streamlit", "run", "src/cherrypick_data_analysis/data_analysis/app.py"])

        else:
            print(f"Unknown mode: {mode}")
    else:
        print("Usage: poetry run python main.py [crawl|fmkorea]")
