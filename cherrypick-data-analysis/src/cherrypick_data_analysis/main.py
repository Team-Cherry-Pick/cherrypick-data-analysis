import sys
import subprocess

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if "fmkorea" in mode:
            from fmkorea_crawler.fmkorea_total_crawl import crawl_start
            crawl_start(int(sys.argv[2]))

        elif mode == "serve":
            subprocess.run(["streamlit", "run", "src/cherrypick_data_analysis/data_analysis/app.py", "--server.address=0.0.0.0"])

        else:
            print(f"Unknown mode: {mode}")
    else:
        print("Usage: poetry run python main.py [crawl|fmkorea]")
