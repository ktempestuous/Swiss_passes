import subprocess
import os
import time
import platform

# Step 1: Run Scrapy Spiders
def run_scrapy_spider_parent():
    # run spider from project's root directory
    command = ['scrapy', 'crawl', 'passes_parent']
    try:
        print("Running Scrapy spider...")
        subprocess.run(command, check=True)
        print("Scrapy spider finished.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the Scrapy spider: {e}")
        exit(1)

def run_scrapy_spider_child():
    # run spider from project's root directory
    command = ['scrapy', 'crawl', 'passes_child', '-o', 'full_pass_data.json']
    try:
        print("Running Scrapy spider...")
        subprocess.run(command, check=True)
        print("Scrapy spider finished.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the Scrapy spider: {e}")
        exit(1)

# Main function to execute both tasks sequentially
def main():
    # Step 1: run the parent Scrapy spider
    run_scrapy_spider_parent()
    print("Ran parent spider script")
    
    # wait
    time.sleep(2) 
    
    # Step 2: run the child Scrapy spider
    run_scrapy_spider_child()
    print("Ran child spider script")

# run main function
if __name__ == "__main__":
    main()

