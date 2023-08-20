import tkinter as tk

def create_gui_elements(app):
        """Creates and configures all the GUI elements for the VideoPlayerApp."""

        # Set the main window's title, geometry, icon, and position
        app.root.title("Video Player with Point Drawing")
        app.root.geometry("1000x600")
        app.root.iconbitmap("sdaia.jpeg")
        app.root.resizable(False, False)
        screen_width = app.root.winfo_screenwidth()
        screen_height = app.root.winfo_screenheight()
        x = (screen_width - 1000) // 2
        y = (screen_height - 600) // 2
        app.root.geometry(f"1000x600+{x}+{y}")

        # Create the canvas to display the video
        app.canvas = tk.Canvas(app.root, width=app.video_width, height=app.video_height)
        app.canvas.grid(row=0, column=0, columnspan=8, sticky='S')

        # Create playback control buttons
        app.rewind_5_seconds_button = tk.Button(app.root, text="<<", width=1, command=app.rewind_n_seconds)
        app.play_button = tk.Button(app.root, text="Play", command=app.toggle_playback, width=4)
        app.forward_5_seconds_button = tk.Button(app.root, text=">>", width=1, command=app.forward_n_seconds)
        app.load_button = tk.Button(app.root, text="Load Video", command=app.load_video)

        # Position the playback control buttons
        app.rewind_5_seconds_button.grid(row=2, column=1, sticky=tk.E)
        app.play_button.grid(row=2, column=2, columnspan=2)
        app.forward_5_seconds_button.grid(row=2, column=4, sticky=tk.W)
        app.load_button.grid(row=2, column=0, sticky=tk.W)

        # Speed control elements
        app.speed_label = tk.Label(app.root, text="Speed:")
        app.speed_combo = tk.Spinbox(app.root, values=list(app.speed_dict.keys()), width=4)
        app.speed_label.grid(row=1, column=7, sticky=tk.E)
        app.speed_combo.grid(row=1, column=8, sticky=tk.W)
        app.speed = app.speed_combo.get()

        # Points display and labels
        app.points_label = tk.Label(app.root, text="Points:")
        app.points_text = tk.Text(app.root, width=15, height=3)
        app.points_label.grid(row=1, column=9, sticky=tk.W)
        app.points_text.grid(row=2, column=9, sticky=tk.W)

        # Lists for entering and leaving points
        app.entering_text = tk.Text(app.root, width=15, height=35)
        app.leaving_text = tk.Text(app.root, width=15, height=35)
        app.label_inside_text = tk.Label(app.entering_text, text="Entering:")
        app.label_inside_leaving_text = tk.Label(app.leaving_text, text="Leaving:")
        app.entering_text.grid(row=0, column=8, sticky=tk.W)
        app.leaving_text.grid(row=0, column=9, sticky=tk.W)
        app.label_inside_text.place(x=0, y=0)
        app.label_inside_leaving_text.place(x=0, y=0)

        # Zoom control elements
        app.zoom_spinbox_label = tk.Label(app.root, text="Zoom:")
        app.zoom_spinbox = tk.Spinbox(app.root, values=list(app.zoom_map.keys()), width=4)
        app.zoom_spinbox_label.grid(row=2, column=7, sticky=tk.E)
        app.zoom_spinbox.grid(row=2, column=8, sticky=tk.W)
        app.zoom = app.zoom_spinbox.get()

        app.reset_button = tk.Button(app.root, text="Reset Json", command=app.reset_json_file)
        app.reset_button.grid(row=3, column=8, sticky=tk.W, columnspan=2)

        # Timer label for displaying current playback time
        app.timer_label = tk.Label(app.root, text="00:00", font=("Helvetica", 16))
        app.timer_label.grid(row=1, column=2, columnspan=2)

        # Button to save the points to JSON
        app.print_button = tk.Button(app.root, text="Save to Json", command=app.save_points_to_json)
        app.print_button.grid(row=3, column=9, sticky=tk.W)

        # Progress bar for video playback
        app.progress_bar = tk.Scale(app.root, from_=0, to=100, orient=tk.HORIZONTAL, length=app.video_width,
                                command=app.seek_to_progress, showvalue=0)
        app.progress_bar.grid(row=3, column=0, columnspan=7)

        # Configure the grid layout
        app.root.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        app.root.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        # Bind events for canvas interactions and window close
        app.canvas.bind("<Button-1>", app.on_canvas_click)
        app.canvas.bind("<Button-2>", app.on_canvas_click)
        app.canvas.bind("<Button-3>", app.on_canvas_click)
        app.root.protocol("WM_DELETE_WINDOW", app.on_close)