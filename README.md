# GitHub_repo_generator_GUI
This tool's core code is owned and created by https://github.com/Shpota

 
### **📌 Steps to Upload Your `.exe` File and Edit `README.md` on GitHub**  

#### **✅ 1. Move the `.exe` File to Your Project Folder**  
- Go to your **`dist/`** folder.  
- Copy **your `.exe` file`** (e.g., `GitRepoGenerator.exe`).  
- Paste it into your **GitHub project folder** (where your `.py` files are).  

#### **✅ 2. Edit `README.md`**  
- Open the `README.md` file in a text editor (or create one if it doesn’t exist).  
- Add details like:  
  - How to use the `.exe`  
  - Requirements (e.g., **Git must be installed**)  
  - Installation steps  

Here’s an example of what you can add to `README.md`:  

```md
# Git Repository Generator

A simple GUI tool to generate Git repositories with automated commit history.

## 🔹 Features
- Create a local Git repository with a custom commit history
- Configure commits per day, frequency, and weekends
- Supports pushing to remote GitHub repositories

## 📥 Download & Run
### **Option 1: Run the EXE (No Python Needed)**
1. **Download** the latest release: [GitRepoGenerator.exe](./GitRepoGenerator.exe)
2. **Make sure Git is installed** on your system.  
   - To check, open `cmd` and run:
     ```sh
     git --version
     ```
   - If Git is not installed, download it from [git-scm.com](https://git-scm.com/downloads).
3. **Double-click** `GitRepoGenerator.exe` to run the program.

### **Option 2: Run from Python Source Code**
1. Install Python (if not installed).
2. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/yourrepo.git
   cd yourrepo
   ```
3. Install dependencies:
   ```sh
   pip install tk
   ```
4. Run the script:
   ```sh
   python git_repo_gui.py
   ```

## 🛠 Requirements
- Windows OS
- **Git** installed and available in the system PATH

## 📜 License
This project is open-source and free to use.
```

#### **✅ 3. Upload Everything to GitHub**
1. **Open Command Prompt** in your project folder.  
2. Run the following commands:  

   ```sh
   git add GitRepoGenerator.exe README.md
   git commit -m "Added executable and updated README"
   git push origin main
   ```
