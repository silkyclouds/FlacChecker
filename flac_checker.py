import os
import subprocess
import sys
import multiprocessing
import shutil
import time

total_files_analyzed = multiprocessing.Value('i', 0)
total_corrupted_files = multiprocessing.Value('i', 0)
corrupted_folders = set()

def check_flac_file(file_path, output_folder, log_file, already_processed_files):
    with total_files_analyzed.get_lock():
        total_files_analyzed.value += 1

    # If the file has already been processed, display it and don't process it again
    if file_path in already_processed_files:
        print(f"Already processed: {file_path}")
        return None

    print(f"Processing: {file_path}")  # Display the file being processed

    if os.path.getsize(file_path) < 1024:
        print(f"Corrupted FLAC file (too small): {file_path}")
        with open(log_file, 'a') as log:
            log.write(f"Corrupted FLAC file (too small): {file_path}\n")
        with total_corrupted_files.get_lock():
            total_corrupted_files.value += 1
        return "File too small"

    result = subprocess.run(["file", "--mime-type", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if "audio/flac" not in result.stdout:
        print(f"Corrupted FLAC file (no header): {file_path}")
        with open(log_file, 'a') as log:
            log.write(f"Corrupted FLAC file (no header): {file_path}\n")
        with total_corrupted_files.get_lock():
            total_corrupted_files.value += 1
        return "No FLAC header"

    return None

def scan_folder_for_flac(input_folder, output_folder, log_file, already_processed_files):
    with open(log_file, 'a') as log:
        log.write("Starting FLAC file checking script...\n")

        for root, _, files in os.walk(input_folder):
            for file in files:
                if file.endswith(".flac"):
                    file_path = os.path.join(root, file)
                    log.write(f"Checking {file_path}...\n")

                    corruption_reason = check_flac_file(file_path, output_folder, log_file, already_processed_files)

                    if corruption_reason:
                        corrupted_folders.add(root)
                        relative_path = os.path.relpath(root, input_folder)
                        new_output_folder = os.path.join(output_folder, relative_path)
                        if not os.path.exists(new_output_folder):
                            os.makedirs(new_output_folder)

                        shutil.move(file_path, os.path.join(new_output_folder, os.path.basename(file_path)))
                        log.write(f"Corrupted FLAC file moved ({corruption_reason}): {file_path}\n")

def log_progress(log_progress_file, total_files_analyzed, total_corrupted_files):
    while True:
        with open(log_progress_file, 'a') as log:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            log.write(f"{timestamp} - {total_corrupted_files.value}/{total_files_analyzed.value}\n")
        time.sleep(10)

def get_already_processed_files(log_file):
    if os.path.exists(log_file):
        with open(log_file, 'r') as log:
            return {line.split("Checking ")[-1].rstrip("...\n") for line in log if "Checking" in line}
    return set()

def prompt_to_delete_corrupted_folders():
    for folder in corrupted_folders:
        # Check if the folder doesn't contain other subfolders
        if not any(os.path.isdir(os.path.join(folder, subfolder)) for subfolder in os.listdir(folder)):
            response = input(f"Do you want to delete the folder {folder} as it contains corrupted files? (yes/no) ")
            if response.lower() == "yes":
                shutil.rmtree(folder)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 flac_checker.py /music /corrupted_flacs /app/flac_checker.log")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    log_file = sys.argv[3]

    log_progress_file = "/app/progress.log"

    already_processed_files = get_already_processed_files(log_file)

    p = multiprocessing.Process(target=log_progress, args=(log_progress_file, total_files_analyzed, total_corrupted_files))
    p.start()

    scan_folder_for_flac(input_folder, output_folder, log_file, already_processed_files)

    p.terminate()

    prompt_to_delete_corrupted_folders()
