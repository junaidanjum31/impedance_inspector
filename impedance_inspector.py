import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class ImpedanceInspectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Impedance Data Inspector")
        self.root.geometry("450x200")

        self.label = tk.Label(root, text="Upload a CSV file with freq, Z_real, Z_imag (with or without headers)")
        self.label.pack(pady=10)

        self.upload_btn = tk.Button(root, text="Upload CSV", command=self.load_csv)
        self.upload_btn.pack(pady=10)

        self.file_path_label = tk.Label(root, text="", fg="blue")
        self.file_path_label.pack(pady=5)

        self.plot_btn = tk.Button(root, text="Plot Impedance Data", command=self.plot_data, state=tk.DISABLED)
        self.plot_btn.pack(pady=10)

        self.df = None  # To store loaded data

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                # First try with headers
                df = pd.read_csv(file_path)
                if not all(col in df.columns for col in ['freq', 'Z_real', 'Z_imag']):
                    # Try assuming no header
                    df = pd.read_csv(file_path, header=None)
                    if df.shape[1] < 3:
                        messagebox.showerror("Error", "CSV must have at least 3 columns.")
                        return
                    df.columns = ['freq', 'Z_real', 'Z_imag']

                # Drop invalid data
                df = df.dropna()
                df = df[np.isfinite(df['freq']) & np.isfinite(df['Z_real']) & np.isfinite(df['Z_imag'])]

                self.df = df
                self.file_path_label.config(text=f"Loaded: {file_path.split('/')[-1]}")
                self.plot_btn.config(state=tk.NORMAL)

                # Print stats
                print(f"Z_real: min = {df['Z_real'].min()}, max = {df['Z_real'].max()}")
                print(f"Z_imag: min = {df['Z_imag'].min()}, max = {df['Z_imag'].max()}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")

    def plot_data(self):
        if self.df is None:
            return

        f = self.df['freq'].values
        Z_real = self.df['Z_real'].values
        Z_imag = self.df['Z_imag'].values
        Z = Z_real + 1j * Z_imag

        Z_mag = np.abs(Z)
        Z_phase = np.angle(Z, deg=True)

        # Nyquist Plot
        plt.figure(figsize=(6, 5))
        plt.plot(Z_real, -Z_imag, 'o-', label='Nyquist')
        plt.xlabel("Z' (Ohm)")
        plt.ylabel("-Z'' (Ohm)")
        plt.title("Nyquist Plot")
        plt.grid(True)
        plt.axis("equal")
        plt.tight_layout()
        plt.show()

        # Bode Plot
        plt.figure(figsize=(10, 4))

        plt.subplot(1, 2, 1)
        plt.semilogx(f, Z_mag, 'o-', color='blue')
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("|Z| (Ohm)")
        plt.title("Bode Magnitude")
        plt.grid(True)

        plt.subplot(1, 2, 2)
        plt.semilogx(f, Z_phase, 'o-', color='green')
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Phase (degrees)")
        plt.title("Bode Phase")
        plt.grid(True)

        plt.tight_layout()
        plt.show()

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ImpedanceInspectorApp(root)
    root.mainloop()
# This code provides a GUI application to inspect impedance data from CSV files.