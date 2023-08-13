import tkinter as tk
from core.video_player_app import VideoPlayerApp

def main():
    root = tk.Tk()
    app = VideoPlayerApp(root)
    app.run()

if __name__ == "__main__":
    main()
