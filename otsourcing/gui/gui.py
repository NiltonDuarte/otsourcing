from datetime import datetime
from functools import partial
from queue import Queue, Empty
from typing import Set
from pynput import keyboard
import tkinter as tk
import tkinter.scrolledtext as st
from multiprocessing import Manager, Process
from otsourcing.app import OtSorcing
from otsourcing.data_model.command_message import CommandType

from otsourcing.services.hotkeys import Hotkeys


def subprocess_run(process_pool, fn):
    process = Process(target=fn)
    process_pool.add(process)
    process.start()


def exit(process_pool, root):
    for process in process_pool:
        process.terminate()
    root.destroy()


def update_output_command_queue(text_area, cmd):
    text = str(cmd)
    text_area.configure(state='normal')
    text_area.insert(
        tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {text}\n")
    # Making the text read only
    text_area.see("end")
    text_area.configure(state='disabled')


def handle_output_command_queue(root, text_area, style, output_command_queue: Queue):
    _map = {
        CommandType.STRING_MESSAGE: [partial(update_output_command_queue, text_area)],
        CommandType.TOGGLE_ATK_MESSAGE: [partial(
            update_output_command_queue, text_area), partial(update_toggle_btn, style, "ToggleAtk")],
        CommandType.TOGGLE_PAUSE_MESSAGE: [partial(
            update_output_command_queue, text_area), partial(update_toggle_btn, style, "TogglePause")]
    }
    try:
        while not output_command_queue.empty():
            cmd = output_command_queue.get_nowait()
            print(cmd)
            for handler in _map[cmd.type]:
                handler(cmd)
    except Empty:
        ...
    root.after(500, lambda: handle_output_command_queue(
        root, text_area, style, output_command_queue))


class MultiQueueBroker:
    def __init__(self, queues) -> None:
        self.queues = queues

    def put(self, *args, **kwargs):
        for queue in self.queues:
            queue.put(*args, **kwargs)

    def put_nowait(self, *args, **kwargs):
        for queue in self.queues:
            queue.put_nowait(*args, **kwargs)


def create_toggle_pause_btn(frm, style, input_queues):
    style.configure("TogglePause.TButton", background="#f00")
    toggle_pause_btn = tk.ttk.Button(
        frm, text="Play/Pause",
        style="TogglePause.TButton",
        command=lambda: input_queues.put(
            keyboard.Key.pause)
    )
    toggle_pause_btn.grid(column=0, row=1)


def create_toggle_atk_btn(frm, style, input_queues):
    style.configure("ToggleAtk.TButton", background="#f00")
    toggle_atk_btn = tk.ttk.Button(frm, text="Toggle Atk", style="ToggleAtk.TButton",
                                   command=lambda: input_queues.put(
                                       'd'))
    toggle_atk_btn.grid(column=1, row=1)
    return toggle_atk_btn


def update_toggle_btn(style, style_name, cmd):
    if cmd.toggle_state:
        style.configure(f"{style_name}.TButton", background="#fff")
    else:
        style.configure(f"{style_name}.TButton", background="#f00")


def start_gui(process_pool, ot_sorcing: OtSorcing):
    manager = Manager()
    input_command_queue_heal = manager.Queue(10)
    input_command_queue_cavebot = manager.Queue(10)
    input_command_queue_attack = manager.Queue(10)
    output_command_queue = manager.Queue(10)
    input_queues = MultiQueueBroker(
        [input_command_queue_heal, input_command_queue_attack, input_command_queue_cavebot])
    hotkeys = Hotkeys(input_queues)
    hotkeys.run()
    heal_app = ot_sorcing.healing_app(
        "heal", input_command_queue_heal, output_command_queue)
    cavebot_app = ot_sorcing.cavebot_app(
        "cb", input_command_queue_cavebot, output_command_queue)
    attack_app = ot_sorcing.attack_app(
        "atk", input_command_queue_attack, output_command_queue)

    root = tk.Tk()
    frm = tk.ttk.Frame(root, padding=10)
    frm.grid()
    style = tk.ttk.Style()
    tk.ttk.Button(frm, text="Start Heal",
                  command=lambda: subprocess_run(
                      process_pool,
                      heal_app.run
                  )).grid(column=0, row=0)
    tk.ttk.Button(frm, text="Start Atk",
                  command=lambda: subprocess_run(
                      process_pool,
                      attack_app.run
                  )).grid(column=1, row=0)
    tk.ttk.Button(frm, text="Start Cb",
                  command=lambda: subprocess_run(
                      process_pool,
                      cavebot_app.run
                  )).grid(column=2, row=0)

    create_toggle_pause_btn(frm, style, input_queues)
    create_toggle_atk_btn(frm, style, input_queues)
    tk.ttk.Button(frm, text="Quit",
                  command=lambda: exit(process_pool,
                                       root)).grid(column=2, row=1)

    tk.ttk.Label(root,
                 text="Output Command Queue",
                 font=("Times New Roman", 15),
                 foreground="black").grid(column=0,
                                          row=3)
    text_area = st.ScrolledText(root,
                                width=30,
                                height=4,
                                font=("Times New Roman",
                                      15))
    text_area.grid(column=0, row=2)
    handle_output_command_queue(
        root, text_area, style, output_command_queue)

    text_area.configure(state='disabled')
    root.wm_attributes("-topmost", 1)
    root.mainloop()
