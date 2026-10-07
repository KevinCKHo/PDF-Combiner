"""PDF Combiner: a simple window for merging any number of PDF files."""

import os
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from merger import count_pages, merge_pdfs

APP_DIR = Path(__file__).parent
ICON_FILE = APP_DIR / "icon.ico"  # replace this file to change the window logo


class PdfCombinerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Combiner")
        # Size the window for the screen's scaling (e.g. 150% on high-res laptops)
        scale = self.root.winfo_fpixels("1i") / 96
        self.root.geometry(f"{int(820 * scale)}x{int(500 * scale)}")
        self.root.minsize(int(640 * scale), int(380 * scale))
        if ICON_FILE.exists():
            self.root.iconbitmap(default=str(ICON_FILE))

        self.files = []  # list of (path, page_count)

        self._build_ui()
        self._refresh()

    # ---------- layout ----------

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill="both", expand=True)

        ttk.Label(
            main,
            text="Add PDFs, put them in order, then click Combine.",
            font=("Segoe UI", 11),
        ).pack(anchor="w", pady=(0, 8))

        # Bottom bar (packed before the list so it always stays visible)
        bottom = ttk.Frame(main, padding=(0, 10, 0, 0))
        bottom.pack(side="bottom", fill="x")

        self.status = ttk.Label(bottom, text="")
        self.status.pack(side="left")

        self.combine_btn = ttk.Button(bottom, text="Combine PDFs", command=self.combine)
        self.combine_btn.pack(side="right")

        self.progress = ttk.Progressbar(bottom, mode="indeterminate", length=140)

        body = ttk.Frame(main)
        body.pack(fill="both", expand=True)

        # Buttons on the right (packed first so they are never cut off)
        buttons = ttk.Frame(body, padding=(12, 0, 0, 0))
        buttons.pack(side="right", fill="y")

        for text, command in [
            ("Add PDFs...", self.add_files),
            ("Remove", self.remove_selected),
            ("Move up", lambda: self.move_selected(-1)),
            ("Move down", lambda: self.move_selected(1)),
            ("Sort by name", self.sort_by_name),
            ("Clear all", self.clear_all),
        ]:
            ttk.Button(buttons, text=text, command=command, width=14).pack(fill="x", pady=3)

        # File list
        columns = ("num", "name", "pages", "folder")
        self.tree = ttk.Treeview(body, columns=columns, show="headings", selectmode="extended")
        self.tree.heading("num", text="#")
        self.tree.heading("name", text="File name")
        self.tree.heading("pages", text="Pages")
        self.tree.heading("folder", text="Folder")
        self.tree.column("num", width=40, anchor="center", stretch=False)
        self.tree.column("name", width=280)
        self.tree.column("pages", width=60, anchor="center", stretch=False)
        self.tree.column("folder", width=260)

        scroll = ttk.Scrollbar(body, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # Keyboard shortcuts
        self.tree.bind("<Delete>", lambda e: self.remove_selected())
        self.root.bind("<Control-o>", lambda e: self.add_files())

    # ---------- actions ----------

    def add_files(self):
        paths = filedialog.askopenfilenames(
            title="Choose PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )
        problems = []
        for path in paths:
            try:
                pages = count_pages(path)
            except Exception as e:
                problems.append(f"{Path(path).name}: {e}")
                continue
            self.files.append((path, pages))

        if problems:
            messagebox.showwarning(
                "Some files were skipped",
                "These files could not be read as PDFs:\n\n" + "\n".join(problems),
            )
        self._refresh()

    def remove_selected(self):
        indexes = self._selected_indexes()
        for i in reversed(indexes):
            del self.files[i]
        self._refresh()

    def move_selected(self, step):
        indexes = self._selected_indexes()
        if not indexes:
            return
        # Stop at the top/bottom edge
        if (step < 0 and indexes[0] == 0) or (step > 0 and indexes[-1] == len(self.files) - 1):
            return

        order = indexes if step < 0 else reversed(indexes)
        for i in order:
            self.files[i], self.files[i + step] = self.files[i + step], self.files[i]
        self._refresh(select=[i + step for i in indexes])

    def sort_by_name(self):
        self.files.sort(key=lambda f: Path(f[0]).name.lower())
        self._refresh()

    def clear_all(self):
        if self.files and messagebox.askyesno("Clear all", "Remove all files from the list?"):
            self.files.clear()
            self._refresh()

    def combine(self):
        if len(self.files) < 2:
            messagebox.showinfo("PDF Combiner", "Add at least two PDF files to combine.")
            return

        first = Path(self.files[0][0])
        output = filedialog.asksaveasfilename(
            title="Save combined PDF as",
            defaultextension=".pdf",
            initialdir=first.parent,
            initialfile="Combined.pdf",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not output:
            return

        inputs = [path for path, _ in self.files]
        if any(os.path.abspath(output) == os.path.abspath(p) for p in inputs):
            messagebox.showerror("PDF Combiner", "The output file can't be one of the input files.")
            return

        self._set_busy(True)
        threading.Thread(target=self._combine_worker, args=(inputs, output), daemon=True).start()

    def _combine_worker(self, inputs, output):
        try:
            merge_pdfs(inputs, output)
        except Exception as e:
            self.root.after(0, self._combine_done, None, e)
        else:
            self.root.after(0, self._combine_done, output, None)

    def _combine_done(self, output, error):
        self._set_busy(False)
        if error:
            messagebox.showerror("PDF Combiner", f"Could not combine the PDFs:\n\n{error}")
            return
        if messagebox.askyesno("Done", f"Saved:\n{output}\n\nOpen the combined PDF now?"):
            os.startfile(output)

    # ---------- helpers ----------

    def _selected_indexes(self):
        return sorted(self.tree.index(item) for item in self.tree.selection())

    def _set_busy(self, busy):
        if busy:
            self.combine_btn.config(state="disabled")
            self.progress.pack(side="right", padx=8)
            self.progress.start(12)
            self.status.config(text="Combining...")
        else:
            self.progress.stop()
            self.progress.pack_forget()
            self.combine_btn.config(state="normal")
            self._refresh()

    def _refresh(self, select=None):
        self.tree.delete(*self.tree.get_children())
        for n, (path, pages) in enumerate(self.files, start=1):
            p = Path(path)
            self.tree.insert("", "end", values=(n, p.name, pages, str(p.parent)))

        if select:
            items = self.tree.get_children()
            self.tree.selection_set([items[i] for i in select])

        total = sum(pages for _, pages in self.files)
        self.status.config(text=f"{len(self.files)} file(s), {total} page(s) total")


def main():
    # Make Windows show our icon in the taskbar instead of the Python one
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("PdfCombiner.App")
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # sharp text on high-res screens
    except Exception:
        pass

    root = tk.Tk()
    PdfCombinerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
