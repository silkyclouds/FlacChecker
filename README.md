<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>FLAC Checker</h1>

<h2>Description</h2>
<p>FLAC Checker is a tool designed to efficiently identify and handle potentially corrupted FLAC audio files in your collection. FLAC files, while a popular lossless audio format, can become corrupted due to various reasons such as incomplete internet downloads, interruptions during file transfers, disk errors, or other unexpected scenarios. Manually identifying these files in a large collection can be tedious. FLAC Checker streamlines this process, making it easier to maintain the integrity of your FLAC collection.</p>

<h2>Features</h2>
<ul>
    <li><strong>Efficiency</strong>: The script remembers files it has already processed. When run multiple times, it avoids re-checking previously scanned files.</li>
    <li><strong>Logging</strong>: Comprehensive logging is provided, which includes progress logs as well as a main log detailing the status of each file.</li>
    <li><strong>Interactive Deletion</strong>: After the scan, the script prompts the user for the deletion of directories containing corrupted files.</li>
    <li><strong>Docker Support</strong>: A Dockerfile is provided for easy setup and execution.</li>
</ul>

<h2>Requirements</h2>
<ul>
    <li>Python 3.x</li>
    <li>FLAC files to be checked</li>
    <li>Docker (if using the Docker setup)</li>
</ul>

<h2>Usage</h2>

<h3>Traditional Setup</h3>
<ol>
    <li>Clone the repository or download the <code>flac_checker.py</code> script.</li>
    <li>Navigate to the directory containing the script using your terminal or command prompt.</li>
    <li>Run the script with the following command:</li>
</ol>
<code>
python3 flac_checker.py [path_to_music_folder] [path_to_corrupted_flacs_folder] [path_to_log_file]
</code>
<p>Replace the placeholders (<code>[...]</code>) with appropriate paths. For example:</p>
<code>
python3 flac_checker.py /music /corrupted_flacs /app/flac_checker.log
</code>

<h3>Docker Setup</h3>
<ol>
    <li>Clone the repository.</li>
    <li>Navigate to the directory containing the <code>flac_checker.py</code> script and the Dockerfile.</li>
    <li>Build the Docker image:</li>
</ol>
<code>
docker build -t flac_checker:latest .
</code>
<ol start="4">
    <li>Run the Docker container:</li>
</ol>
<code>
docker run -v [path_to_music_folder]:/app/music -v [path_to_corrupted_flacs_folder]:/app/corrupted_flacs -v [path_to_log_file]:/app/flac_checker.log flac_checker:latest
</code>
<p>Replace the placeholders (<code>[...]</code>) with appropriate paths. For example:</p>
<code>
docker run -v /music:/app/music -v /corrupted_flacs:/app/corrupted_flacs -v /app/flac_checker.log:/app/flac_checker.log flac_checker:latest
</code>

<h2>Contributing</h2>
<p>Feel free to fork this repository, make changes, and submit pull requests. Any contributions are welcome!</p>

</body>
</html>
