# PDF Combiner — User Manual

PDF Combiner joins several PDF files into one PDF, in the order you choose. There is no limit on the number of files.

![PDF Combiner window](docs/screenshot.png)

## Contents

1. [Before you start](#1-before-you-start)
2. [Install](#2-install)
3. [Start the app](#3-start-the-app)
4. [Combine PDFs step by step](#4-combine-pdfs-step-by-step)
5. [Buttons and shortcuts](#5-buttons-and-shortcuts)
6. [Change the logo](#6-change-the-logo)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Before you start

You need:

- **Windows 10 or 11.** The app also runs on macOS and Linux, but the double-click launcher is for Windows only.
- **Python 3.9 or newer.** Get it from [python.org/downloads](https://www.python.org/downloads/). During installation, tick **"Add python.exe to PATH"**.

To check whether Python is installed, open **Command Prompt** and type:

```
py --version
```

If you see a version number such as `Python 3.14.0`, Python is installed.

## 2. Install

1. On the project's GitHub page, click the green **Code** button, then **Download ZIP**.
2. Right-click the downloaded ZIP file, choose **Extract All...**, and extract it to a folder you can find again, such as your Desktop.

If you use git, you can clone the project instead:

```
git clone <this repository's URL>
```

## 3. Start the app

Open the project folder and double-click **`Run PDF Combiner.bat`**.

The first time you run it, the launcher installs the one library the app needs (`pypdf`). This takes a few seconds and needs an internet connection. After that, the PDF Combiner window opens.

To start the app from a terminal instead:

```
py -m pip install -r requirements.txt
py app.py
```

## 4. Combine PDFs step by step

1. **Add your files.** Click **Add PDFs...**. In the file window, select one or more PDFs. To select several files, hold **Ctrl** and click each one. Then click **Open**.
   - To add files from another folder, click **Add PDFs...** again. New files go to the end of the list.
   - You can add the same file more than once if you want it to appear twice.
2. **Check the list.** Each row shows the file's position (**#**), name, number of pages, and folder. The bottom-left corner shows the total number of files and pages.
3. **Set the order.** The combined PDF follows the list from top to bottom.
   - Click a file, then click **Move up** or **Move down**.
   - To move several files together, select them with **Ctrl**+click or **Shift**+click first.
   - **Sort by name** puts all files in alphabetical order.
4. **Remove files you don't need.** Select them and click **Remove** or press **Delete**.
5. **Combine.** Click **Combine PDFs**, choose a folder and file name, and click **Save**.
6. When it finishes, the app asks whether to open the new PDF. Click **Yes** to view it.

Your original PDF files are never changed or deleted.

## 5. Buttons and shortcuts

| Button / key | What it does |
|---|---|
| **Add PDFs...** / **Ctrl+O** | Add one or more PDF files to the end of the list |
| **Remove** / **Delete** | Remove the selected files from the list (the files themselves are not deleted) |
| **Move up** | Move the selected files one place up |
| **Move down** | Move the selected files one place down |
| **Sort by name** | Sort the whole list alphabetically by file name |
| **Clear all** | Empty the list (asks you to confirm first) |
| **Combine PDFs** | Join all files in the list into one new PDF |

## 6. Change the logo

The icon in the window's top-left corner and in the taskbar comes from **`icon.ico`** in the project folder.

To use your own logo:

1. Create or convert your image to an `.ico` file. Free online converters work, or any image editor that can save `.ico`. Include a 256×256 size for the sharpest result.
2. Name it `icon.ico` and replace the existing file in the project folder.
3. Restart the app.

If `icon.ico` is missing, the app uses the default icon.

## 7. Troubleshooting

**"Python was not found" or the window flashes and closes**
Python is not installed or was not added to PATH. Reinstall Python from python.org and tick **"Add python.exe to PATH"**.

**`ModuleNotFoundError: No module named 'pypdf'`**
The library is not installed for the copy of Python you're using. In the project folder, run:

```
py -m pip install -r requirements.txt
```

If you run the app from VS Code, make sure VS Code is using the same Python: press **Ctrl+Shift+P**, choose **Python: Select Interpreter**, and pick the version where you installed pypdf.

**"Some files were skipped"**
The listed files could not be read as PDFs. They may be damaged, password-protected, or not real PDFs (for example, an image renamed to `.pdf`). Open them in a PDF viewer to check.

**"The output file can't be one of the input files"**
You chose to save over one of the PDFs in your list. Choose a different file name.

**"Could not combine the PDFs"**
The message below it gives the reason. Common causes:
- The output file is open in another program (such as a PDF viewer). Close it and try again.
- You don't have permission to save in that folder. Choose another folder, such as Documents or Desktop.

**The window or text looks blurry or too small**
This can happen with display scaling above 100%. Make sure you're using the latest version of the app from GitHub. It adjusts to your screen's scaling.
