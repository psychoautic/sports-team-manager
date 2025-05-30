import customtkinter as ctk

class NumberCounter(ctk.CTkFrame):
    def __init__(self, master=None, min_value=0, max_value=99, initial=0, **kwargs):
        super().__init__(master, **kwargs)
        self.min_value = min_value
        self.max_value = max_value

        self.value = ctk.IntVar(value=initial)

        self.entry = ctk.CTkEntry(self, textvariable=self.value, width=60, justify="center")
        self.entry.pack(side="left", padx=5)

        self.btn_minus = ctk.CTkButton(self, text="-", width=30, command=self.decrement)
        self.btn_minus.pack(side="left", padx=2)

        self.btn_plus = ctk.CTkButton(self, text="+", width=30, command=self.increment)
        self.btn_plus.pack(side="left", padx=2)

    def get(self):
        return self.value.get()

    def set(self, value):
        self.value.set(value)

    def increment(self):
        if self.value.get() < self.max_value:
            self.value.set(self.value.get() + 1)

    def decrement(self):
        if self.value.get() > self.min_value:
            self.value.set(self.value.get() - 1)
