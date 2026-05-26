import tkinter as tk
from tkinter import messagebox


class BracketFrame(tk.LabelFrame):
    def __init__(self, parent, label):
        super().__init__(parent, text=label)
        self.entries = []

        row = tk.Frame(self)
        row.pack(pady=5)
        tk.Label(row, text="(100%").pack(side=tk.LEFT)

        self.entry_container = tk.Frame(row)
        self.entry_container.pack(side=tk.LEFT)

        tk.Label(row, text=" )").pack(side=tk.LEFT)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=2)
        tk.Button(btn_frame, text="+ Add %", command=self.add_entry
                  ).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="- Remove %", command=self.remove_entry
                  ).pack(side=tk.LEFT, padx=2)

        self.add_entry()

    def add_entry(self, value=""):
        group = tk.Frame(self.entry_container)
        group.pack(side=tk.LEFT)
        tk.Label(group, text=" - ").pack(side=tk.LEFT)
        entry = tk.Entry(group, width=6)
        entry.pack(side=tk.LEFT)
        tk.Label(group, text="%").pack(side=tk.LEFT)
        if value:
            entry.insert(0, str(value))
        self.entries.append(entry)

    def remove_entry(self):
        if len(self.entries) > 1:
            e = self.entries.pop()
            e.master.destroy()

    def get_values(self):
        vals = []
        for e in self.entries:
            raw = e.get().strip().rstrip("%")
            try:
                vals.append(float(raw))
            except ValueError:
                return None
        return vals


class App:
    def __init__(self, root):
        self.root = root
        root.title("Percentage Calculator")
        root.geometry("620x420")
        root.update_idletasks()
        x = (root.winfo_screenwidth() - 620) // 2
        y = (root.winfo_screenheight() - 420) // 2
        root.geometry(f"620x420+{x}+{y}")

        tk.Label(root, text="x * (100% - [...]) * (100% - [...]) = input",
                 font=("Segoe UI", 11)).pack(pady=(15, 10))

        input_frame = tk.Frame(root)
        input_frame.pack(pady=5)
        tk.Label(input_frame, text="Input (result):").pack(side=tk.LEFT)
        self.input_entry = tk.Entry(input_frame, width=15)
        self.input_entry.pack(side=tk.LEFT, padx=5)

        self.b1 = BracketFrame(root, "Bracket 1")
        self.b1.pack(pady=8, padx=20, fill=tk.X)

        self.b2 = BracketFrame(root, "Bracket 2")
        self.b2.pack(pady=8, padx=20, fill=tk.X)

        tk.Button(root, text="Calculate x", command=self.calculate,
                  font=("Segoe UI", 10)).pack(pady=10)

        result_frame = tk.Frame(root)
        result_frame.pack(pady=5, padx=20, fill=tk.X)

        tk.Label(result_frame, text="Formula:").pack(anchor=tk.W)
        self.formula_entry = tk.Entry(result_frame, state="readonly",
                                      readonlybackground="#f0f0f0")
        self.formula_entry.pack(fill=tk.X, pady=2, ipady=2)

        tk.Label(result_frame, text="Result:").pack(anchor=tk.W)
        self.result_entry = tk.Entry(result_frame, state="readonly",
                                     readonlybackground="#f0f0f0")
        self.result_entry.pack(fill=tk.X, pady=2, ipady=2)

    def calculate(self):
        try:
            input_val = float(self.input_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input value")
            return

        b1_vals = self.b1.get_values()
        if b1_vals is None:
            messagebox.showerror("Error", "Invalid percentage in Bracket 1")
            return

        b2_vals = self.b2.get_values()
        if b2_vals is None:
            messagebox.showerror("Error", "Invalid percentage in Bracket 2")
            return

        b1_sum = sum(b1_vals)
        b2_sum = sum(b2_vals)

        if b1_sum >= 100:
            messagebox.showerror("Error", "Bracket 1 sum cannot reach or exceed 100%")
            return
        if b2_sum >= 100:
            messagebox.showerror("Error", "Bracket 2 sum cannot reach or exceed 100%")
            return

        multiplier = (1 - b1_sum / 100) * (1 - b2_sum / 100)

        if multiplier == 0:
            messagebox.showerror("Error", "Multiplier is zero — no x satisfies the equation")
            return

        x = input_val / multiplier

        b1_str = " - ".join(f"{v}%" for v in b1_vals)
        b2_str = " - ".join(f"{v}%" for v in b2_vals)
        formula = f"x * (100% - {b1_str}) * (100% - {b2_str}) = {input_val}"
        result_text = f"x = {x}"

        self.formula_entry.config(state="normal")
        self.formula_entry.delete(0, tk.END)
        self.formula_entry.insert(0, formula)
        self.formula_entry.config(state="readonly")

        self.result_entry.config(state="normal")
        self.result_entry.delete(0, tk.END)
        self.result_entry.insert(0, result_text)
        self.result_entry.selection_range(0, tk.END)
        self.result_entry.config(state="readonly")
        self.result_entry.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
