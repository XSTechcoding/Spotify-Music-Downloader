import tkinter as tk
from tkinter import Entry, Label, Button, StringVar, messagebox, filedialog
from subprocess import Popen, PIPE

class SpotifyDownloaderApp:
    def __init__(self, master):
        self.master = master
        master.title("Spotify Downloader")

        self.label_url = Label(master, text="Enter Spotify URL or Playlist URL:")
        self.label_url.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.url_entry = Entry(master, width=40)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)

        self.label_folder = Label(master, text="Download Folder:")
        self.label_folder.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.folder_entry = Entry(master, width=30)
        self.folder_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.browse_button = Button(master, text="Browse", command=self.browse_folder)
        self.browse_button.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        self.download_button = Button(master, text="Download", command=self.download_song)
        self.download_button.grid(row=3, column=1, padx=10, pady=10)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        self.folder_entry.delete(0, tk.END)
        self.folder_entry.insert(0, folder_selected)

    def download_song(self):
        spotify_url = self.url_entry.get()
        download_folder = self.folder_entry.get()

        if not spotify_url:
            self.show_error("Please enter a Spotify URL or Playlist URL.")
            return

        if not download_folder:
            self.show_error("Please select a download folder.")
            return

        try:
            command = [
                "spotdl",
                "--output", download_folder,
                "--overwrite", "skip",
                spotify_url
            ]
            process = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            while True:
                output = process.stdout.readline().strip()
                error = process.stderr.readline().strip()

                if not output and not error and process.poll() is not None:
                    break

                print(output)  # Print output to console instead of log window
                if error:
                    print(f"[ERROR] {error}")

                self.master.update_idletasks()

            if process.returncode == 0:
                self.show_success("Download successful!")
            else:
                self.show_error("Error during download. Check the console output for details.")

        except Exception as e:
            self.show_error(f"An error occurred: {str(e)}")

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def show_success(self, message):
        messagebox.showinfo("Success", message)


if __name__ == "__main__":
    root = tk.Tk()
    app = SpotifyDownloaderApp(root)
    root.mainloop()
    
