# Project Name

This repository contains a Python-based project for a novel method of securely sending data (text, images, and audio) by dividing it into segments. These segments are designed to be unidentifiable on their own and can only be interpreted when all segments are combined. 

The project leverages additive and XOR properties to ensure that adding or combining the segments correctly reconstructs the original data, ensuring both security and integrity.


---

## Collaborators

This project was developed as a group effort. The contributors are:

- **Abdul Moiz Sarwar** ([View Profile](https://github.com/Abdul-Moiz-Sarwar))
- **Iqra Bokhari** ([View Profile](https://github.com/iqrabokhari))
- **Numair Cheema** ([View Profile](https://github.com/collaborator2))

---

## Prerequisites

1. **Python**  
   Ensure Python is installed on your system. [Download Python](https://www.python.org/downloads/).

2. **VSCode**  
   Use Visual Studio Code (VSCode) as the recommended code editor. [Download VSCode](https://code.visualstudio.com/).

3. **FFmpeg**  
   - Download FFmpeg from this [ffmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z).
   - Extract the downloaded file to a desired location.
   - Add the `ffmpeg/bin` folder path to your system's environment variables.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # For Windows
   source venv/bin/activate  # For macOS/Linux
   ```

3. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Define environment variables in a `.env` file at the root of the project:
   ```env
   BASE_URL="http://127.0.0.1:8000"
   SECRET_KEY="any secret key for django"
   DEBUG="True"
   ALLOWED_HOSTS="*"
   ```

---

## Running the Project

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Open your browser and navigate to the base URL:
   ```
   http://127.0.0.1:8000
   ```

---

## Additional Notes

- Ensure the `.env` file is properly set up before running the project.
- Database is not required to run this project.
- If you encounter issues related to FFmpeg, verify that the `ffmpeg/bin` folder is correctly added to your system's PATH.
- Use `CTRL+C` in the terminal to stop the server.

---

Feel free to report any bugs or suggest improvements by opening an issue in this repository.

---