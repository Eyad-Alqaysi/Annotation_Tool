import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import json
import os
from core.point_data import PointData
from gui.gui_elements import create_gui_elements


class VideoPlayerApp:
    def __init__(self, root):
        """Initialize the video player app with default settings."""
        self.root = root
        self.video_path = ""
        self.video_capture = None
        self.video_width = 700
        self.video_height = 500
        self.speed = 33
        self.current_frame = 0
        self.is_playing = False
        self.points = []
        self.points_ID = 1
        self.leaving_counter, self.entering_counter = 0, 0
        self.all_frames = []
        self.current_photo = None
        self.point_photos = {}
        self.zoom = 100
        self.n_sec = 1 # change to 1 second

        json_files_dir = '../json_files'
        if not os.path.exists(json_files_dir):
            os.makedirs(json_files_dir)
            with open('../json_files/virtual_gate.json', 'w+') as f:
                f.write('{}')
            
            


        self.zoom_map = {
            0: 200,
            1: 175,
            2: 150,
            3: 125,
            4: 100,
            5: 75,
            6: 50,
            7: 25,
        }
        self.speed_dict = {
            0.1: (1 / 30 * 1000) / 0.1,
            0.2: (1 / 30 * 1000) / 0.2,
            0.3: (1 / 30 * 1000) / 0.3,
            0.4: (1 / 30 * 1000) / 0.4,
            0.5: (1 / 30 * 1000) / 0.5,
            0.6: (1 / 30 * 1000) / 0.6,
            0.7: (1 / 30 * 1000) / 0.7,
            0.8: (1 / 30 * 1000) / 0.8,
            0.9: (1 / 30 * 1000) / 0.9,
            1: (1 / 30 * 1000) / 1,
            1.1: (1 / 30 * 1000) / 1.1,
            1.2: (1 / 30 * 1000) / 1.2,
            1.3: (1 / 30 * 1000) / 1.3,
            1.4: (1 / 30 * 1000) / 1.4,
            1.5: (1 / 30 * 1000) / 1.5,
            1.6: (1 / 30 * 1000) / 1.6,
            1.7: (1 / 30 * 1000) / 1.7,
            1.8: (1 / 30 * 1000) / 1.8,
            1.9: (1 / 30 * 1000) / 1.9,
            2: (1 / 30 * 1000) / 2,
        }
        
        create_gui_elements(self)
        self.update()
        

    def load_video(self):
        """Load a video file and initialize all relevant parameters."""
        if self.points:
            if tk.messagebox.askyesno("Changes", "Do you want to save the points before load?"):
                self.save_points_to_json()
        
        self.reset_everything()

        self.video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.avi *.mp4 *.mov")])
        if self.video_path:
            self.video_capture = cv2.VideoCapture(self.video_path)
            self.video_width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.video_height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.current_frame = 0
            self.all_frames.clear()
            self.capture_all_frames()
            self.progress_bar.config(to=len(self.all_frames))
        self.read_points_from_json()
        self.show_frame()

    def read_points_from_json(self, file_path='../json_files/virtual_gate.json'):
        """Load point data from a JSON file given a specific path."""
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        video_key = self.video_path.split('/')[-1]
        if video_key in data:
            print(video_key)
            # Extract points from the data
            points_data = data[video_key]['points']
            # Clear the current points
            self.points = []
            # Iterate through each point and create PointData object
            for p in points_data:
                point_data = PointData(p["point_id"], p["frame"], p["x"], p["y"], p["state"])
                self.points.append(point_data)
            

    def capture_all_frames(self):
        """Capture all frames from the video and store them in a list."""
        while True:
            ret, frame = self.video_capture.read()
            if ret:
                self.all_frames.append(frame)
            else:
                break

    def reset_everything(self):
        """Reset all parameters to their default values."""
        
        self.video_path = ""
        self.video_capture = None
        self.video_width = 720
        self.video_height = 600
        self.speed = 33
        self.current_frame = 0
        self.is_playing = False
        self.points = []
        self.points_ID = 1
        self.leaving_counter, self.entering_counter = 0, 0
        self.all_frames = []
        self.current_photo = None
        self.point_photos = {}

        self.canvas.delete("all")
        self.points_text.delete(1.0, tk.END)
        self.entering_text.delete(1.0, tk.END)
        self.leaving_text.delete(1.0, tk.END)
        self.timer_label.config(text="00:00")
        self.progress_bar.set(0)
        self.play_button.config(text="Play")

    def toggle_playback(self):
        """Toggle between play and pause."""
        if not self.is_playing:
            self.is_playing = True
            self.play_button.config(text="Pause")
        else:
            self.is_playing = False
            self.play_button.config(text="Play")

    def show_frame(self):
        """Show the current frame on the canvas."""
        if self.video_capture and self.current_frame < len(self.all_frames):
            frame = self.all_frames[self.current_frame]
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            image = image.resize((self.video_width, self.video_height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image=image)
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            self.canvas.photo = photo
            
            for point_data in self.points:
                if self.current_frame in point_data.points_by_frame:
                    x, y, state = point_data.points_by_frame[self.current_frame]
                    print(f"Drawing point {point_data.point_id} at ({x},{y}) with state {state}")
                    color = "green" if state == "Entering" else "red"
                    point_id = f"point_{point_data.point_id}"
                    self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, tags=(point_id,))

    def on_canvas_click(self, event):
        """Handle mouse clicks on the video canvas for point placement or removal."""
        if self.video_capture:
            x, y = event.x, event.y

            if 0 <= x <= self.video_width and 0 <= y <= self.video_height:
                if event.num == 3:
                    existing_point = self.get_existing_point(x, y)

                    if existing_point:
                        self.points.remove(existing_point)
                        if existing_point.state == "Entering":
                            self.entering_counter -= 1
                        elif existing_point.state == "Leaving":
                            self.leaving_counter -= 1
                        self.canvas.delete(f"point_{existing_point.point_id}")

                        if existing_point.point_id in self.point_photos:
                            del self.point_photos[existing_point.point_id]

                        self.update_points_text()
                        self.update_entering_text()
                        self.update_leaving_text()
                        return

                else:
                    color = "green" if event.num == 1 else "red"

                    if color == "green":
                        point_info = (self.points_ID, self.current_frame, x, y, "Entering")
                        self.entering_counter += 1
                    elif color == "red":
                        point_info = (self.points_ID, self.current_frame, x, y, "Leaving")
                        self.leaving_counter += 1
                    else:
                        return

                    point_id = f"point_{self.points_ID}"
                    new_point = PointData(*point_info)
                    self.points.append(new_point)

                    self.points_ID += 1

                    self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, tags=(point_id,))

                    zoom_on_map = int(self.zoom_spinbox.get())
                    zoom = int(self.zoom_map[zoom_on_map])
                    half_of_zoom = zoom // 2

                    if self.video_capture.isOpened():
                        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
                        ret, frame = self.video_capture.read()
                        if ret:
                            # Calculate the region of interest for zoomed image
                            x1 = max(0, x - half_of_zoom)
                            y1 = max(0, y - half_of_zoom)
                            x2 = min(self.video_width, x + half_of_zoom)
                            y2 = min(self.video_height, y + half_of_zoom)

                            # Capture the zoomed image if the region is valid
                            if x1 < x2 and y1 < y2:
                                img = frame[y1:y2, x1:x2]
                                pil_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                                zoomed_image = pil_image.resize((105, 105), Image.LANCZOS)

                                new_point.photo = ImageTk.PhotoImage(image=zoomed_image)

                                self.point_photos[new_point.point_id] = new_point.photo

                                self.update_entering_text()
                                self.update_leaving_text()
                            else:
                                print("Error capturing zoomed image: Invalid region.")

                        else:
                            print("Error capturing frame.")

                    self.update_points_text()

    def get_existing_point(self, x, y):
        """Retrieve a point close to the given coordinates, if it exists."""
        closest_point = None
        closest_distance = float('inf')
        for point_data in self.points:
            distance = ((x - point_data.x) ** 2 + (y - point_data.y) ** 2) ** 0.5
            if distance < 5 and distance < closest_distance:
                closest_point = point_data
                closest_distance = distance
        return closest_point

    def update_entering_text(self):
        """Update the entering text box with the entering points."""
        self.entering_text.delete(1.0, tk.END)
        for point_data in reversed(self.points):
            if point_data.state == "Entering":
                if point_data.point_id in self.point_photos:
                    self.entering_text.image_create(tk.END, image=point_data.photo)

    def update_leaving_text(self):
        """Update the leaving text box with the leaving points."""
        self.leaving_text.delete(1.0, tk.END)
        for point_data in reversed(self.points):
            if point_data.state == "Leaving":
                if point_data.point_id in self.point_photos:
                    self.leaving_text.image_create(tk.END, image=point_data.photo)

    def update_points_text(self):
        """Update the points text box with the entering and leaving points."""
        self.points_text.delete(1.0, tk.END)
        self.points_text.insert(tk.END, f"Entering: {self.entering_counter}")
        self.points_text.insert(tk.END, f"\nLeaving: {self.leaving_counter}")

    def update_timer_label(self, elapsed_time):
        """Update the timer label with the elapsed time."""
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        time_string = f"{minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=time_string)

    def update_progress_bar(self):
        """Update the progress bar with the current frame."""
        if self.video_capture:
            total_frames = len(self.all_frames)
            if total_frames > 0:
                progress = (self.current_frame)
                self.progress_bar.set(progress)

    def seek_to_frame(self, frame_num):
        """Move the video playback to a specific frame."""
        if self.video_capture:
            self.current_frame = frame_num
            self.show_frame()

            elapsed_time = int(self.current_frame / self.video_capture.get(cv2.CAP_PROP_FPS))
            self.update_timer_label(elapsed_time)
            self.update_progress_bar()

    def seek_to_progress(self, progress):
        """Move the video playback to a specific progress point."""
        total_frames = len(self.all_frames)
        if total_frames > 0:
            frame_num = int(progress)
            self.seek_to_frame(frame_num)

    def rewind_n_seconds(self):
        """Rewind the video by a specific number of seconds."""
        fps = self.video_capture.get(cv2.CAP_PROP_FPS)
        current_time = self.current_frame / fps
        new_time = max(0, current_time - self.n_sec)  
        new_frame = int(new_time * fps)
        self.seek_to_frame(new_frame)

    def forward_n_seconds(self):
        """Fast-forward the video by a specific number of seconds."""
        fps = self.video_capture.get(cv2.CAP_PROP_FPS)
        total_frames = len(self.all_frames)
        current_time = self.current_frame / fps
        new_time = min(current_time + self.n_sec, total_frames / fps) 
        new_frame = int(new_time * fps)
        self.seek_to_frame(new_frame)


    def update(self):
        """Update the video frame and UI elements based on the current playback state."""
        if self.is_playing and self.video_capture:
            total_frames = len(self.all_frames)
            if total_frames > 0:
                self.current_frame += 1
                if self.current_frame >= total_frames:
                    self.is_playing = False
                    self.play_button.config(text="Play")
                    self.current_frame = total_frames - 1

                self.seek_to_frame(self.current_frame)

        self.speed = float(self.speed_combo.get())
        delay = int(self.speed_dict[self.speed])
        self.root.after(delay, self.update)

    def save_points_to_json(self):
        """
        Save point data to a JSON file.
        First file for points, second file for counters.
        """
        data = {
            self.video_path.split('/')[-1]: {
                "points": [
                    {
                        "point_id": point_data.point_id,
                        "frame": point_data.frame,
                        "x": point_data.x,
                        "y": point_data.y,
                        "state": point_data.state
                    }
                    for point_data in self.points
                ]
            },
        }

        counter_data = {
            self.video_path.split("/")[-1]: {
                "entering_counter": self.entering_counter,
                "leaving_counter": self.leaving_counter
            }
        }

        json_files_dir = '../json_files'

        file_path = os.path.join(json_files_dir, 'virtual_gate.json')

        if os.path.exists(file_path):
            with open(file_path, "r") as json_file:
                existing_data = json.load(json_file)
                existing_data.update(data)

            with open(file_path, "w") as json_file:
                json.dump(existing_data, json_file, indent=4)

            counters_path = os.path.splitext(file_path)[0] + "_counters.json"
            if os.path.exists(counters_path):
                with open(counters_path, "r") as counters_file:
                    existing_counters_data = json.load(counters_file)
                    existing_counters_data.update(counter_data)

                with open(counters_path, "w") as counters_file:
                    json.dump(existing_counters_data, counters_file, indent=4)
            else:
                with open(counters_path, "w") as counters_file:
                    json.dump(counter_data, counters_file, indent=4)

        else:
            with open(file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)

            counters_path = os.path.splitext(file_path)[0] + "_counters.json"
            with open(counters_path, "w") as counters_file:
                json.dump(counter_data, counters_file, indent=4)

        tk.messagebox.showinfo("File Saved", f"Points saved to '{file_path}'\nCounters saved to '{counters_path}'")

        print(f"Points saved to '{file_path}'")
        print(f"Counters saved to '{counters_path}'")

    
    def on_close(self):
        """Handle the user closing the window."""
        if self.points:
            if tk.messagebox.askyesno("Unsaved Changes", "Do you want to save the points before exiting?"):
                self.save_points_to_json()
        self.root.destroy()

    def bind_keyboard_events(self):
        """Bind keyboard shortcuts to specific functions."""
        self.root.bind("<Escape>", lambda event: self.on_close())
        self.root.bind("<l>", lambda event: self.load_video())
        self.root.bind("<space>", lambda event: self.toggle_playback())
        self.root.bind("<Left>", lambda event: self.rewind_n_seconds())
        self.root.bind("<Right>", lambda event: self.forward_n_seconds())
        self.root.bind("<p>", lambda event: self.save_points_to_json())

    def run(self):
        """Start the main application loop."""
        self.bind_keyboard_events()
        self.root.mainloop()