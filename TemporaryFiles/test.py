from tqdm import tqdm
import time

# Your slow program
def slow_program():
    for i in tqdm(range(10)):#, desc="Processing", unit="iteration"):
        # Simulate a slow operation
        time.sleep(0.1)

# Run the slow program
slow_program()