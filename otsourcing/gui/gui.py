from queue import  Queue, Empty
from typing import Set
from pynput import keyboard
import tkinter as tk
import tkinter.scrolledtext as st
from multiprocessing import Manager, Process

from otsourcing.services.hotkeys import Hotkeys


def subprocess_run(process_pool, fn):
    process = Process(target=fn)
    process_pool.add(process)
    process.start()


def exit(process_pool, root):
    for process in process_pool:
        process.terminate()
    root.destroy()


def update_output_command_queue(root, text_area, output_command_queue: Queue):
    try:
        while not output_command_queue.empty():
            text = output_command_queue.get_nowait()
            print(text)
            text_area.configure(state='normal')
            text_area.insert(tk.END, f"{text}\n")
            # Making the text read only
            text_area.see("end")
            text_area.configure(state='disabled')
    except Empty:
        ...
    root.after(500, lambda: update_output_command_queue(
        root, text_area, output_command_queue))


def start_gui(process_pool, subprocess_cls):
    manager = Manager()
    input_command_queue = manager.Queue(10)
    output_command_queue = manager.Queue(10)
    hotkeys = Hotkeys(input_command_queue)
    hotkeys.run()
    subprocess_cls = subprocess_cls(input_command_queue, output_command_queue)
    root = tk.Tk()
    frm = tk.ttk.Frame(root, padding=10)
    frm.grid()
    tk.ttk.Button(frm, text="Start", command=lambda: subprocess_run(process_pool,
        subprocess_cls.run)).grid(column=0, row=0)
    tk.ttk.Button(frm, text="Play/Pause", command=lambda: input_command_queue.put(
        keyboard.Key.pause)).grid(column=1, row=0)

    tk.ttk.Button(frm, text="Quit", command=lambda: exit(process_pool,
        root)).grid(column=2, row=0)

    tk.ttk.Label(root,
                 text="Output Command Queue",
                 font=("Times New Roman", 15),
                 foreground="black").grid(column=0,
                                          row=1)
    text_area = st.ScrolledText(root,
                                width=30,
                                height=8,
                                font=("Times New Roman",
                                      15))
    text_area.grid(column=0, row=2)
    update_output_command_queue(root, text_area, output_command_queue)

    text_area.configure(state='disabled')
    root.wm_attributes("-topmost", 1)
    root.mainloop()
