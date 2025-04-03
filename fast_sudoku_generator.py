import copy
import os
import random
import time
import pandas as pd
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
import place_ID_changer
import printer

def clear_check(place):
    """Check if the Sudoku board is valid and complete"""
    for i in range(9):
        # Check rows
        rowset = set(place[i])
        if len(rowset) != 9 or 0 in rowset:
            return False
        
        # Check columns
        colset = set([place[j][i] for j in range(9)])
        if len(colset) != 9 or 0 in colset:
            return False
        
        # Check 3x3 blocks
        block_row, block_col = (i // 3) * 3, (i % 3) * 3
        blockset = set([place[block_row + j//3][block_col + j%3] for j in range(9)])
        if len(blockset) != 9 or 0 in blockset:
            return False
    
    return True

def is_valid(place, row, col, num):
    """Check if placing num at place[row][col] is valid"""
    # Check row
    for x in range(9):
        if place[row][x] == num:
            return False

    # Check column
    for x in range(9):
        if place[x][col] == num:
            return False

    # Check 3x3 box
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if place[i + start_row][j + start_col] == num:
                return False
    
    return True

def generate_base_board():
    """Generate a valid first row for the Sudoku board"""
    # Start with a random first row
    first_row = random.sample(range(1, 10), 9)
    place = [[0 for _ in range(9)] for _ in range(9)]
    place[0] = first_row
    return place

def shuffle_board(place):
    """Apply random transformations to a valid Sudoku board to create a new one"""
    # Create a copy of the board
    new_place = copy.deepcopy(place)
    
    # Shuffle digit mappings (1-9 → random permutation of 1-9)
    digit_mapping = list(range(1, 10))
    random.shuffle(digit_mapping)
    digit_mapping = [0] + digit_mapping  # Add 0 at index 0 for easier mapping
    
    for i in range(9):
        for j in range(9):
            if new_place[i][j] != 0:
                new_place[i][j] = digit_mapping[new_place[i][j]]
    
    # Randomly swap rows within the same block
    for block in range(3):
        base_row = block * 3
        row_order = list(range(3))
        random.shuffle(row_order)
        rows = [new_place[base_row + i] for i in range(3)]
        for i in range(3):
            new_place[base_row + i] = rows[row_order[i]]
    
    # Randomly swap columns within the same block
    for block in range(3):
        base_col = block * 3
        col_order = list(range(3))
        random.shuffle(col_order)
        for i in range(9):
            cols = [new_place[i][base_col + j] for j in range(3)]
            for j in range(3):
                new_place[i][base_col + j] = cols[col_order[j]]
    
    # Randomly swap 3x3 row blocks
    block_order = list(range(3))
    random.shuffle(block_order)
    blocks = [[new_place[block*3 + i] for i in range(3)] for block in range(3)]
    for block in range(3):
        for i in range(3):
            new_place[block*3 + i] = blocks[block_order[block]][i]
    
    # Randomly swap 3x3 column blocks
    block_order = list(range(3))
    random.shuffle(block_order)
    for i in range(9):
        cols = [[new_place[i][block*3 + j] for j in range(3)] for block in range(3)]
        for block in range(3):
            for j in range(3):
                new_place[i][block*3 + j] = cols[block_order[block]][j]
    
    # Randomly transpose the board
    if random.choice([True, False]):
        new_place = [list(row) for row in zip(*new_place)]
    
    return new_place

def backtrack_solve(place, row=0, col=0):
    """Solve the Sudoku board using backtracking"""
    # If we've filled all cells, we're done
    if row == 9:
        return True
    
    # Move to the next cell
    next_row, next_col = (row, col + 1) if col < 8 else (row + 1, 0)
    
    # If the current cell is already filled, move to the next cell
    if place[row][col] != 0:
        return backtrack_solve(place, next_row, next_col)
    
    # Try each number 1-9
    nums = list(range(1, 10))
    random.shuffle(nums)  # Randomize the order to generate different solutions
    
    for num in nums:
        if is_valid(place, row, col, num):
            place[row][col] = num
            
            # Recursively solve the rest of the board
            if backtrack_solve(place, next_row, next_col):
                return True
            
            # If we couldn't solve the board with this number, backtrack
            place[row][col] = 0
    
    # If we've tried all numbers and none worked, backtrack
    return False

def generate_sudoku_solution():
    """Generate a complete valid Sudoku solution board"""
    # Start with a base board (first row filled)
    place = generate_base_board()
    
    # Solve the board using backtracking
    backtrack_solve(place)
    
    # Verify the solution is valid
    if not clear_check(place):
        # This should never happen if backtrack_solve works correctly
        print("Warning: Generated an invalid solution. Retrying...")
        return generate_sudoku_solution()
    
    return place

def generate_multiple_solutions(count, base_solution=None):
    """Generate multiple Sudoku solutions by shuffling a base solution"""
    solutions = []
    
    # Generate a base solution if not provided
    if base_solution is None:
        base_solution = generate_sudoku_solution()
    
    # Generate the requested number of solutions
    for _ in range(count):
        # Create a new solution by shuffling the base solution
        new_solution = shuffle_board(base_solution)
        
        # Verify the solution is valid
        if not clear_check(new_solution):
            # This should never happen if shuffle_board works correctly
            print("Warning: Generated an invalid solution after shuffling. Retrying...")
            continue
        
        solutions.append(new_solution)
    
    return solutions

def worker_function(args):
    """Worker function for parallel generation"""
    count, worker_id, batch_size, output_dir = args
    
    # Generate a base solution
    base_solution = generate_sudoku_solution()
    
    # Generate solutions in batches
    solutions = []
    solution_ids = []
    
    start_time = time.time()
    for i in range(count):
        # Generate a new solution
        solution = shuffle_board(base_solution)
        
        # Convert to ID and add to list
        solution_id = place_ID_changer.place_to_id(solution)
        solutions.append(solution)
        solution_ids.append(solution_id)
        
        # Save batch to CSV when it reaches the batch size
        if len(solution_ids) >= batch_size:
            file_path = os.path.join(output_dir, f"sudoku_solutions_{worker_id}_{i//batch_size}.csv")
            pd.DataFrame(solution_ids, columns=["id"]).to_csv(file_path, index=False)
            
            # Clear the lists to free memory
            solutions = []
            solution_ids = []
        
        # Print progress every 1000 solutions
        if (i + 1) % 1000 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            print(f"Worker {worker_id}: Generated {i + 1} solutions. Rate: {rate:.2f} solutions/second")
    
    # Save any remaining solutions
    if solution_ids:
        file_path = os.path.join(output_dir, f"sudoku_solutions_{worker_id}_{count//batch_size}.csv")
        pd.DataFrame(solution_ids, columns=["id"]).to_csv(file_path, index=False)
    
    return f"Worker {worker_id} completed {count} solutions"

def generate_solutions_parallel(total_count, num_workers=None, batch_size=1000, output_dir=None):
    """Generate Sudoku solutions in parallel"""
    # Set default number of workers to CPU count
    if num_workers is None:
        num_workers = mp.cpu_count()
    
    # Set default output directory
    if output_dir is None:
        output_dir = os.path.dirname(__file__)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Calculate solutions per worker
    solutions_per_worker = total_count // num_workers
    remainder = total_count % num_workers
    
    # Prepare arguments for each worker
    worker_args = []
    for i in range(num_workers):
        # Add remainder solutions to the first worker
        count = solutions_per_worker + (remainder if i == 0 else 0)
        worker_args.append((count, i, batch_size, output_dir))
    
    # Start the workers
    print(f"Starting {num_workers} workers to generate {total_count} solutions...")
    start_time = time.time()
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(worker_function, worker_args))
    
    # Print results
    for result in results:
        print(result)
    
    elapsed = time.time() - start_time
    rate = total_count / elapsed
    print(f"Generated {total_count} solutions in {elapsed:.2f} seconds. Rate: {rate:.2f} solutions/second")

def print_sample_solutions(count=5):
    """Generate and print a few sample solutions"""
    print(f"Generating {count} sample Sudoku solutions:")
    solutions = generate_multiple_solutions(count)
    printer.multi_printer(solutions)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate valid Sudoku solution boards")
    parser.add_argument("--count", type=int, default=10000, help="Number of solutions to generate")
    parser.add_argument("--workers", type=int, default=None, help="Number of worker processes (default: CPU count)")
    parser.add_argument("--batch", type=int, default=1000, help="Batch size for saving solutions")
    parser.add_argument("--output", type=str, default=None, help="Output directory for solution files")
    parser.add_argument("--sample", action="store_true", help="Print a few sample solutions and exit")
    
    args = parser.parse_args()
    
    if args.sample:
        print_sample_solutions()
    else:
        generate_solutions_parallel(args.count, args.workers, args.batch, args.output)
