import tkinter as tk
from tkinter import ttk, messagebox
from tasks import TaskManager
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.mgr = TaskManager()
        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        top = tk.Frame(self.root)
        top.pack(fill='x', padx=8, pady=6)

        tk.Label(top, text="Search:").pack(side='left')
        self.search_var = tk.StringVar()
        tk.Entry(top, textvariable=self.search_var).pack(side='left', padx=4)
        tk.Button(top, text="Go", command=self.on_search).pack(side='left', padx=4)
        tk.Button(top, text="Clear", command=self.on_clear).pack(side='left')

        toolbar = tk.Frame(self.root)
        toolbar.pack(fill='x', padx=8)
        tk.Button(toolbar, text="Add Task", command=self.open_add).pack(side='left')
        tk.Button(toolbar, text="Edit", command=self.open_edit).pack(side='left', padx=4)
        tk.Button(toolbar, text="Complete", command=self.mark_complete).pack(side='left', padx=4)
        tk.Button(toolbar, text="Delete", command=self.delete_task).pack(side='left', padx=4)

        cols = ("title", "due", "status")
        self.tree = ttk.Treeview(self.root, columns=cols, show='headings', selectmode='browse')
        self.tree.heading('title', text='Title')
        self.tree.heading('due', text='Due Date')
        self.tree.heading('status', text='Status')
        self.tree.pack(fill='both', expand=True, padx=8, pady=8)

        self.tree.bind("<Double-1>", self.view_details)

    def refresh(self, tasks=None):
        for i in self.tree.get_children():
            self.tree.delete(i)
        tasks = tasks if tasks is not None else self.mgr.get_all()
        for t in tasks:
            due = t.due_date or "-"
            self.tree.insert('', 'end', iid=str(t.id), values=(t.title, due, t.status))

    def on_search(self):
        k = self.search_var.get().strip()
        if not k:
            self.refresh()
            return
        res = self.mgr.search(k)
        self.refresh(res)

    def on_clear(self):
        self.search_var.set("")
        self.refresh()

    def get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return int(sel[0])

    def open_add(self):
        self._open_editor()

    def open_edit(self):
        sel = self.get_selected_id()
        if not sel:
            messagebox.showinfo("Select", "Select a task first")
            return
        task = self.mgr.find(sel)
        if task:
            self._open_editor(task)

    def _open_editor(self, task=None):
        win = tk.Toplevel(self.root)
        win.transient(self.root)
        win.grab_set()
        win.title("Add Task" if task is None else "Edit Task")

        tk.Label(win, text="Title").grid(row=0,column=0,sticky='w')
        title_var = tk.StringVar(value=task.title if task else "")
        tk.Entry(win, textvariable=title_var, width=40).grid(row=0,column=1)

        tk.Label(win, text="Description").grid(row=1,column=0,sticky='nw')
        desc_text = tk.Text(win, height=6, width=40)
        if task:
            desc_text.insert('1.0', task.description)
        desc_text.grid(row=1,column=1)

        tk.Label(win, text="Due (YYYY-MM-DD)").grid(row=2,column=0,sticky='w')
        due_var = tk.StringVar(value=task.due_date if task else "")
        tk.Entry(win, textvariable=due_var).grid(row=2,column=1,sticky='w')

        def save():
            title = title_var.get().strip()
            if not title:
                messagebox.showwarning("Validation", "Title required")
                return
            desc = desc_text.get('1.0','end').strip()
            due = due_var.get().strip() or None
            if due:
                try:
                    datetime.strptime(due, DATE_FORMAT)
                except ValueError:
                    messagebox.showwarning("Validation", "Due date must be YYYY-MM-DD")
                    return
            if task:
                self.mgr.update(task.id, title=title, description=desc, due_date=due)
            else:
                self.mgr.add_task(title, description=desc, due_date=due)
            win.destroy()
            self.refresh()

        tk.Button(win, text="Save", command=save).grid(row=3,column=1,sticky='e', pady=6)

    def mark_complete(self):
        sel = self.get_selected_id()
        if not sel:
            messagebox.showinfo("Select", "Select a task")
            return
        self.mgr.mark_complete(sel)
        self.refresh()

    def delete_task(self):
        sel = self.get_selected_id()
        if not sel:
            messagebox.showinfo("Select", "Select a task")
            return
        if messagebox.askyesno("Confirm","Delete selected task?"):
            self.mgr.delete(sel)
            self.refresh()

    def view_details(self, event):
        sel = self.get_selected_id()
        if not sel:
            return
        t = self.mgr.find(sel)
        if not t:
            return
        msg = f"Title: {t.title}\n\nDescription:\n{t.description}\n\nDue: {t.due_date}\nStatus: {t.status}\nCreated: {t.created_at}"
        messagebox.showinfo("Task Details", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()
