import PySimpleGUI as sg
import textwrap
import os
import io
import shutil
import subprocess
import shlex
import cv2
import glob
from PIL import Image, ImageFilter, ImageOps,ImageTk
import threading
import time
from datetime import datetime as dt ,timedelta
# import requests
import math 
import fractions
import numpy as np
from moviepy.editor import AudioFileClip, VideoFileClip 
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import pandas as pd
import webbrowser
# import roop.roop.core as core
# import roop.roop.swapper as swapper
# import roop.roop.analyser as analyser
import os
import uuid
import psutil

import roop.core as core
# import roop.swapper as swapper
# import roop.analyser as analyser
# from progress_bar_custom import progress_bar_custom,progress_bar_custom_download
# import util.add_watermark
# util.add_watermark.set_oritation('DR')
# from util.add_watermark import watermark_image

image_file_ext = {
    ("IMAGE Files", "*.png"),
    ("IMAGE Files", "*.jpg"),
    ("IMAGE Files", "*.jpeg"),
}

video_file_ext = {
    ("Video Files", "*.mp4"),
    ("Video Files", "*.webm"),
    ("Video Files", "*.gif"),
}

# -------------------------------------------------------------------
# Constants, defaults, Base64 icons
USE_FADE_IN = True
WIN_MARGIN = 60

# colors
WIN_COLOR = "#282828"
TEXT_COLOR = "#ffffff"

DEFAULT_DISPLAY_DURATION_IN_MILLISECONDS = 10000

# Base64 Images to use as icons in the window
img_error = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAA3NCSVQICAjb4U/gAAAACXBIWXMAAADlAAAA5QGP5Zs8AAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAIpQTFRF////20lt30Bg30pg4FJc409g4FBe4E9f4U9f4U9g4U9f4E9g31Bf4E9f4E9f4E9f4E9f4E9f4FFh4Vdm4lhn42Bv5GNx5W575nJ/6HqH6HyI6YCM6YGM6YGN6oaR8Kev9MPI9cbM9snO9s3R+Nfb+dzg+d/i++vt/O7v/fb3/vj5//z8//7+////KofnuQAAABF0Uk5TAAcIGBktSYSXmMHI2uPy8/XVqDFbAAAA8UlEQVQ4y4VT15LCMBBTQkgPYem9d9D//x4P2I7vILN68kj2WtsAhyDO8rKuyzyLA3wjSnvi0Eujf3KY9OUP+kno651CvlB0Gr1byQ9UXff+py5SmRhhIS0oPj4SaUUCAJHxP9+tLb/ezU0uEYDUsCc+l5/T8smTIVMgsPXZkvepiMj0Tm5txQLENu7gSF7HIuMreRxYNkbmHI0u5Hk4PJOXkSMz5I3nyY08HMjbpOFylF5WswdJPmYeVaL28968yNfGZ2r9gvqFalJNUy2UWmq1Wa7di/3Kxl3tF1671YHRR04dWn3s9cXRV09f3vb1fwPD7z9j1WgeRgAAAABJRU5ErkJggg=='
img_success = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAA3NCSVQICAjb4U/gAAAACXBIWXMAAAEKAAABCgEWpLzLAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAHJQTFRF////ZsxmbbZJYL9gZrtVar9VZsJcbMRYaMZVasFYaL9XbMFbasRZaMFZacRXa8NYasFaasJaasFZasJaasNZasNYasJYasJZasJZasJZasJZasJZasJYasJZasJZasJZasJZasJaasJZasJZasJZasJZ2IAizQAAACV0Uk5TAAUHCA8YGRobHSwtPEJJUVtghJeYrbDByNjZ2tvj6vLz9fb3/CyrN0oAAADnSURBVDjLjZPbWoUgFIQnbNPBIgNKiwwo5v1fsQvMvUXI5oqPf4DFOgCrhLKjC8GNVgnsJY3nKm9kgTsduVHU3SU/TdxpOp15P7OiuV/PVzk5L3d0ExuachyaTWkAkLFtiBKAqZHPh/yuAYSv8R7XE0l6AVXnwBNJUsE2+GMOzWL8k3OEW7a/q5wOIS9e7t5qnGExvF5Bvlc4w/LEM4Abt+d0S5BpAHD7seMcf7+ZHfclp10TlYZc2y2nOqc6OwruxUWx0rDjNJtyp6HkUW4bJn0VWdf/a7nDpj1u++PBOR694+Ftj/8PKNdnDLn/V8YAAAAASUVORK5CYII='
patreon = b'iVBORw0KGgoAAAANSUhEUgAAAFwAAAAZCAYAAAC8ekmHAAAACXBIWXMAAC4jAAAuIwF4pT92AAAF8WlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMxNDggNzkuMTY0MDM2LCAyMDE5LzA4LzEzLTAxOjA2OjU3ICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjEuMCAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDIyLTExLTI4VDE3OjQ5OjEwKzAyOjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyMi0xMS0yOFQxODowMjo1MCswMjowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyMi0xMS0yOFQxODowMjo1MCswMjowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHBob3Rvc2hvcDpJQ0NQcm9maWxlPSJzUkdCIElFQzYxOTY2LTIuMSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo4NDM1ODVmZS1iOTMwLTcwNGItYmYwMy1mNTgzNDZiOTQ2ZjMiIHhtcE1NOkRvY3VtZW50SUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDowYmMyNTI5Zi02YTg0LWM2NDMtOTI0Ny0yYmFiN2FlZTgzNzkiIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDo0NWZlNjdhOC0yZGI5LTdlNDQtODM0ZS03YmY1MzA3MTk1NTkiPiA8eG1wTU06SGlzdG9yeT4gPHJkZjpTZXE+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJjcmVhdGVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjQ1ZmU2N2E4LTJkYjktN2U0NC04MzRlLTdiZjUzMDcxOTU1OSIgc3RFdnQ6d2hlbj0iMjAyMi0xMS0yOFQxNzo0OToxMCswMjowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIDIxLjAgKFdpbmRvd3MpIi8+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJzYXZlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDo4NDM1ODVmZS1iOTMwLTcwNGItYmYwMy1mNTgzNDZiOTQ2ZjMiIHN0RXZ0OndoZW49IjIwMjItMTEtMjhUMTg6MDI6NTArMDI6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCAyMS4wIChXaW5kb3dzKSIgc3RFdnQ6Y2hhbmdlZD0iLyIvPiA8L3JkZjpTZXE+IDwveG1wTU06SGlzdG9yeT4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz4gLKG0AAALtElEQVRoge2ae5RV1X3HP/u87rn33MfM3BkYhmGY8JhBIMFRUWiBMWpkWWtDtIrRmj6URqJNzUqbtqxkta6ExD9c6rKUZag0sZrGphURbVBriVJQiOIMOqAgMDPMMMMwb+7r3PPa/eNyh8fM8MjCNNV+1zpr3bvPvvu392f/9m//zr5HrFy5Etu2FymK8hgwG5CAz0WSQGK6Gblt5m2ZAxUNlpUfEher7f8DUgEBYq8IlD93VXu75vv+tUKI16SUH5NNiSwodOL6mOz8JktejhJsU6S4TnNdd9XHbAwpJUjpSCkNKeWnycNHJCUI1FUaMH/sCic9UYjRjM51f1T9X6GTnzRJ5HwtCILTCoUQSClJp9O4rks4HCYcDiOlRAhBEAQ4joPjOEgpMQyDUCiEoiiMFS4EkiAITrs+zdLOLCgCqa+vJx6P09PTQ29vL5qmkc1myWazVFRUUFdXB0BHRwe9vb1YljUyMf+v8aWdCSifz6NpGitWrKC2tpaXX36ZdevWIaVE13XuvPNOrr32WsrKygAYGBhgy5YtbNiwgVQqRSwWO8OLCzH81OtiSyiCgYEcqqZQkggR+L+5kz4KeBGKrusA6LpONpvFNE3uu+8+GhsbT6tfUVHB8uXLqaqq4vHHHx+pe7LdIujgYwEeSMi7PndfWUVfPuDFg0PElOC89pX/DY0JPAgCfL+QiruuSyqVYtmyZaNgn6rFixezZ88eNm3ahK7rpwy4CJxRwIUobKZDw3k0Q0UGEj/tgCowYiGiplboj4TjWReZcwuEFYEeNYiGdQIpsQdzrFo0he0Hj7LxxVaGqitJlJrkbY+842GYGvnjDiBJlEUQimA4nUdmvUJHTJVYNISuFLIJhCCVc/EyTsGerhKJGZiaihCQsz1ytocR0cmnHXB8CKlE4yaGIgjO4lTjenhRrutiWRZLliw55+w1NjaydetWbNvGNM0zgI8OKX4gkcCNc8pp7kpTV27x9YWT2dtv89B/HWLgeJ6SqIHt+iysiXPrnAqqSywODtk88kYrx4ZsMFSu++wEakpDDJZq3Lu0msikWn7UdJRp5TrlIYUP+mxW3TyLsKHx7Tc66esc4Kr6Mu69spqIafBUUxc/b+7GSpgYmsLgYI5JpSbfvP4zTE/GeHF/H//01mEcQ0PVFGYkw0yM6OzsSvNXS6fTMCnGj5u6eeH9HqLREOpZFtd5AU8kEiSTyXMCr6mpIR6P093dTSgUOg14MAZw2y3E+tVXT6WmJMzhtEdfKsuq+WUsryuhYV0zQ0N5ZlSGeeqL9UhF4XBPH1+fHWXlvCuY98Nm2tqHuarKQgWmlCf4o/m1ZKXKI6/1c3vdVNb+bj27juaoLjHp7B2k/8hh/mDBDJ6+ZQ57+h1Sg338x/JLeLDS4u9ebSWjwOemRHn7Ty8n5wt2t/ew/ndqWDazhN/7yR68YZvfmlvOupvq2NaZJm7qmNJh422XcH9M5x+2HSGRMMYNnecEXoReDDFnk+u6eJ53Rhvje7hE4geSWMSk1PRo+O4LtO/upKw2Qf+au3l4STlf/dl+MsRY8tR7dG97B3p7IG7x7rp7eLSxgi/9qIvVr7ZxR8MU3mnazx+ufh5qqiBrY1xZCcDGt5r53r82g51i3rxqnr5lDl/ZsIen/34jZDPc8OXF/PyBG3i+6RC7Oz2evXUOnZmA6X/xDOw/wMLrG3jzb27mgYY4j21q47hbGMOOln385Y9/CceH+emDt7B6cRU/3PIeGW8SYeVXBK7rOgMDA7S1tVFVVXVW4Hv37qWvrw9d188P+InvZTGNf3l9D+1v7iJy1XwG7Djrm3pZXhfjq+4xuruiRE1Yfe8S5tVMoDWrUFFahpIagsFOqJmLrqlougLlScIz5pIbzBQyKd/joX97A4wITJjNHUsbAOju7OSmm2ahV9eT8Qox4FIzzV7V5ZJkmLuefB3aPsL47QW8dcyg+VieP54V4bGnjhCzLgPgkQ3bQfGgbi7Pd0huv1xjkttHR9pCliTA9y4cuKZpOI7DSy+9xIIFC1AUZVzgmzdvJpPJkEwmzxs4QN6BtqEUJMtRklOgJ01byiESjkF/H5OmTqPlgSV4iuDVli5yPT0EU8OoYQvyGXDswiYtAUUgNB00A01V6M/YeIoKVdNALSWsK4Bk1XWzKEsmkVLguS4Hhxza+tOUBy4Ah450QtUUjLLJONleDh13uDIagdwgwnfxPB9bASZ9BmLlaAqg6ASBB/ksUpSe2IEvEDhALBZjx44drF27lvvvv39M2GvXrmXnzp0kEokzfn8yLWQs4IHEMKDWMsBT8BCQs6mN6mQDAYNZfvD5GmwEk//kSeg7CsdyVD58F1+4bHIhi5A+mga244Ht4rgenAhtqhAohkGgqJDPoWoabjbLNaueASsKUROCAFIu5DPMaig80E2zDN50ctieC57HtHiIgbQPdh48F1VVUDUDhAJ5m6IbBpKT47wQ4MVyKSWKohCJRNi0aROtra0sXbqUmTNnAnDgwAFeeeUVmpubicViqKo6DnA5NnAp6R92uOMLDfz1lkN0fNBFckaSuy+bwBPb9kPKxjJNQr4Dg10Qn8Jnv3QZd109i/fbukEAXkBv2mNOVSmEDTzHHRmsKkBIClBNjSd2tPG1hvl85yuNfPf5Q6DGwRTUX5Jg2IUP+/PsHXT529sW8swHr+Ed7GPhFRO4dILBn23pBC9AVRUKWa+EwIcRuIJCsUQGFwj8VAVBgKZpxGIxdu/eTUtLC6WlpQAMDg7i+z6JRAJVVcc4KxkfeLGjg5k8x4BNK69hEIvP11jsT8M3frodKqI8uO0IX5xdydCz36JpWCFuqvT54HluYdB+wEO/OMBzt9Yz/I8r+CinccUTbzNg+2iicJ6DlJiWzvv7+7hn44c8efMi7rl+IQfTgtq4QnkEGte/x9H2w/z+07t492tXMLTmTt4fkiyaFGLjgeOseXEnJBMoeqhgV568AgrAFQqr9rw9PAgCVFUdidXFQ6lieUlJCZ7nkUqlAAiHw2iaNvLb0ToBPBgHOJLq8hiPPvc6P2tq5fvLLufb76R45JW92D1HMOc20NKRZtajb/LNS8NEghwP7+ihbzjHnAkGGAK9xGRD81FmtfdwQ0UW2/EJdffw3LsuLe3d4ObQ1AIjo8Rk/dY2tu7rZEW9zsSIzg5b4d9bumna344+cQofdNtM/sFWvvG5EDOjgi9vtnn2P3dDkIXZDWz+qJ8bu46SyaRRIpUEls5/tw9x4z/vYiCVRimvRHKewIvgivBOTfOKdVVVRVXVU7id7XH9LB4eFD4bCkxIhDjU0sPtve9BqgcR0zFmNyCtcgzfoXXA5r6ftMJQN8RCEI5zLG+iT6xFURR0E/b15dm3bwByQ+hxnY7e47R3Z9ArpiJ0g8B3EUj0khAfDft864XDMNxbiDkRHbUsiRKOY2iCwTx856VO6O8C1Ucpi6FPnA2RGB3d/bSmcmgl1ehmBFTJkf4MHW059MQUtHAE6bnnB1zTNIQQrFmzhrKyMjo6OrAsa+TY9sJ17pDiBRRirGWg10+HoHZkIqVjAxJNB6bVgFJ7ciAyAEUhcB3wPHRThanFOqB6eVQJ6DVIzwHfQyJASnRDwPRaENMKcVgIEAqB54DrFlZETSXUVhf6pigEgQ92DqGBXmqBXkrgu+A4qCqoJRHQS5C+C54LY5znjAJeDCFNTU3k83ksy8KyLIIguOjAVVUgEVy9fhfDB/ZBVD0Bxh8JN6fJcyjskoy+V5ghcPOjyx37tP6MqFi3mFKeek9SgIZ7wuaZ9oLT25VjlZ3npgkQjUaJRqMA5/WUOb7O4uEUxvrhoWMIP446sRTpeQXPPUt7F13ndKSLZ1OTUr4NXHPRWhylswNHgmIqEEsWlruX56QXf4IkAVX8UlNV9Xue5/06gBtIKcYNS65zRu8+gXLF9zVN037hed4iKeVjwBwu8nspp7wmkUFKS366/rUvvpeyR6jqA9IJtv8Pox7WnXQ/LA4AAAAASUVORK5CYII='
GRAY_9900 = '#0A0A0A'


def flatten_ui_elements(window):
    for widget_key in window.key_dict.keys():
        try: 
            window[widget_key].Widget.config(relief='flat')
        except:
            # print("error",widget_key)
            pass

def display_notification(title, message, icon, display_duration_in_ms=DEFAULT_DISPLAY_DURATION_IN_MILLISECONDS, use_fade_in=True, alpha=0.9, location=None):

    # Compute location and size of the window
    message = textwrap.fill(message, 50)
    win_msg_lines = message.count("\n") + 1

    screen_res_x, screen_res_y = sg.Window.get_screen_size()
    win_margin = WIN_MARGIN  # distance from screen edges
    win_width, win_height = 500, 100 + (14.8 * win_msg_lines)
    win_location = location if location is not None else (screen_res_x - win_width - win_margin, screen_res_y - win_height - win_margin)

    layout = [[sg.Graph(canvas_size=(win_width, win_height), graph_bottom_left=(0, win_height), graph_top_right=(win_width, 0), key="-GRAPH-",
                        background_color=WIN_COLOR, enable_events=True)]]

    window = sg.Window(title, layout, background_color=WIN_COLOR, no_titlebar=True,
                       location=win_location, keep_on_top=True, alpha_channel=0, margins=(0, 0), element_padding=(0, 0),
                       finalize=True)

    window["-GRAPH-"].draw_rectangle((win_width, win_height), (-win_width, -win_height), fill_color=WIN_COLOR, line_color=WIN_COLOR)
    window["-GRAPH-"].draw_image(data=icon, location=(20, 20))
    window["-GRAPH-"].draw_text(title, location=(64, 20), color=TEXT_COLOR, font=("Arial", 12, "bold"), text_location=sg.TEXT_LOCATION_TOP_LEFT)
    window["-GRAPH-"].draw_text(message, location=(64, 44), color=TEXT_COLOR, font=("Arial", 9), text_location=sg.TEXT_LOCATION_TOP_LEFT)

    # change the cursor into a "hand" when hovering over the window to give user hint that clicking does something
    window['-GRAPH-'].set_cursor('hand2')

    if use_fade_in == True:
        for i in range(1,int(alpha*100)):               # fade in
            window.set_alpha(i/100)
            event, values = window.read(timeout=20)
            if event != sg.TIMEOUT_KEY:
                window.set_alpha(1)
                break
        event, values = window(timeout=display_duration_in_ms)
        if event == sg.TIMEOUT_KEY:
            for i in range(int(alpha*100),1,-1):       # fade out
                window.set_alpha(i/100)
                event, values = window.read(timeout=20)
                if event != sg.TIMEOUT_KEY:
                    break
    else:
        window.set_alpha(alpha)
        event, values = window()

    window.close()

def show_media(window,values,source_file_path,target_file_path):
    if values['-SHOW_MEDIA-'] == True:
        try:
            display_image(window["-source_image-"],source_file_path,(300,300))
            display_image(window["-target_image-"],target_file_path,(300,300))  
            display_image(window["-OUTPUT_FILE-"],swaped_file_path,(400,400))
        except:
            print("values['-SHOW_MEDIA-'] == True: ERROR Image not Loaded")

    if values['-SHOW_MEDIA-'] == False:
        try:
            display_image(window["-source_image-"],'input_placeholder.png',(300,300))
            display_image(window["-target_image-"],'input_placeholder.png',(300,300))  
            display_image(window["-OUTPUT_FILE-"],'output_placeholder.png',(400,400))                
        except:
            print("values['-SHOW_MEDIA-'] == False: ERROR Image not Loaded")

def display_image(event_name,image,size):
    image_bio_data = get_img_data(image,size)
    event_name.update(data=image_bio_data)  

def set_swaped_video_location(file):
    global swaped_video_location
    swaped_video_location = file

def get_swaped_video_location():
    return swaped_video_location     

def set_video_frame_count(frame_count):
    global video_frame_count_for_progress_bar
    video_frame_count_for_progress_bar = frame_count

def get_video_frame_count():
    return video_frame_count_for_progress_bar   

def set_video_frame_index(frame_index):
    global video_frame_index_for_progress_bar
    video_frame_index_for_progress_bar = frame_index

def get_video_frame_index():
    return video_frame_index_for_progress_bar  
   
def swap_video(pic_a_path,video_path,output,temp_results,crop_size_p,watermark,use_mask,suffix,window):
    # crop_size = crop_size_p
    # opt = TestOptions().parse()
    # opt.Arc_path = 'arcface_model/arcface_checkpoint.tar'
    # opt.crop_size = crop_size
    # start_epoch, epoch_iter = 1, 0
    # torch.nn.Module.dump_patches = True
    # if crop_size == 512:
    #     opt.which_epoch = 550000
    #     opt.name = '512'
    #     mode = 'ffhq'
    # else:
    #     mode = 'None'
    # model = create_model(opt)
    # model.eval()

    # #AKA app
    # detect_model = Face_detect_crop(name='antelope', root='./insightface_func/models')
    # detect_model.prepare(ctx_id= 0, det_thresh=0.6, det_size=(640,640),mode=mode)
    # with torch.no_grad():
    #     pic_a = pic_a_path
    #     # img_a = Image.open(pic_a).convert('RGB')
    #     img_a_whole = cv2.imread(pic_a)
    #     img_a_align_crop, _ = detect_model.get(img_a_whole,crop_size)
    #     img_a_align_crop_pil = Image.fromarray(cv2.cvtColor(img_a_align_crop[0],cv2.COLOR_BGR2RGB)) 
    #     img_a = transformer_Arcface(img_a_align_crop_pil)
    #     img_id = img_a.view(-1, img_a.shape[0], img_a.shape[1], img_a.shape[2])

    #     # convert numpy to tensor
    #     img_id = img_id.cuda()

    #     #create latent id
    #     img_id_downsample = F.interpolate(img_id, size=(112,112))
    #     latend_id = model.netArc(img_id_downsample)
    #     latend_id = F.normalize(latend_id, p=2, dim=1)
    #     threading.Thread(target=video_swap(video_path, latend_id, model, detect_model, output, pic_a_path, suffix, temp_results, crop_size, watermark, use_mask,window), daemon=True).start() 
        # window.write_event_value('-VIDEO-SWAPED-',get_swaped_video_location())
        window.write_event_value('-VIDEO-SWAPED-','')

def video_swap(video_path, id_vetor, swap_model, detect_model, save_path,pic_a_path, suffix ,temp_results_dir='./temp_results', crop_size=224, no_simswaplogo = False,use_mask = True,window='window'):


    print('************ Swap parameters START ************')
    print(f'crop_size:{crop_size}')
    print(f'use_mask_p:{use_mask}')
    print(f'no_watermark:{no_simswaplogo}')
    print('************ Swap parameters END ************')
    
    video_forcheck = VideoFileClip(video_path)
    if video_forcheck.audio is None:
        no_audio = True
    else:
        no_audio = False
    del video_forcheck
    if not no_audio:
        video_audio_clip = AudioFileClip(video_path)

    video = cv2.VideoCapture(video_path)
    logoclass = watermark_image('./simswaplogo/simswaplogo.png')
    ret = True
    frame_index = 0
    
    # set_video_frame_index(frame_index)

    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # set_video_frame_count(frame_count)
    # video_WIDTH = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))

    # video_HEIGHT = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    fps = video.get(cv2.CAP_PROP_FPS)
    if  os.path.exists(temp_results_dir):
            shutil.rmtree(temp_results_dir)

    spNorm =SpecificNorm()
    if use_mask:
        n_classes = 19
        net = BiSeNet(n_classes=n_classes)
        net.cuda()
        save_pth = os.path.join('./parsing_model/checkpoint', '79999_iter.pth')
        net.load_state_dict(torch.load(save_pth))
        net.eval()
    else:
        net =None

    
    start_time = dt.today().timestamp()

    pbar_progress_bar_key = '-pbar_progress_bar_video_face_swap-'
    pbar_percentage_key = '-pbar_percentage_video_face_swap-'
    pbar_index_range_video_key = '-pbar_index_range_video_face_swap-'
    pbar_iteration_per_sec_key = '-pbar_it_per_sec_video_face_swap-'
    pbar_estimated_time_key = '-pbar_estimated_time_video_face_swap-'

    for frame_index in tqdm(range(frame_count)):

        progress_bar_custom(frame_index,frame_count,start_time,window,pbar_progress_bar_key,pbar_percentage_key,pbar_index_range_video_key,pbar_iteration_per_sec_key,pbar_estimated_time_key)

        ret, frame = video.read()
        if  ret:
            detect_results = detect_model.get(frame,crop_size)

            if detect_results is not None:
                if not os.path.exists(temp_results_dir):
                        os.mkdir(temp_results_dir)
                frame_align_crop_list = detect_results[0]
                frame_mat_list = detect_results[1]
                swap_result_list = []
                frame_align_crop_tenor_list = []
                for frame_align_crop in frame_align_crop_list:

                    # BGR TO RGB
                    # frame_align_crop_RGB = frame_align_crop[...,::-1]

                    frame_align_crop_tenor = _totensor(cv2.cvtColor(frame_align_crop,cv2.COLOR_BGR2RGB))[None,...].cuda()

                    swap_result = swap_model(None, frame_align_crop_tenor, id_vetor, None, True)[0]
                    cv2.imwrite(os.path.join(temp_results_dir, 'frame_{:0>7d}.png'.format(frame_index)), frame)
                    swap_result_list.append(swap_result)
                    frame_align_crop_tenor_list.append(frame_align_crop_tenor)

                    

                reverse2wholeimage(frame_align_crop_tenor_list,swap_result_list, frame_mat_list, crop_size, frame, logoclass,\
                    os.path.join(temp_results_dir, 'frame_{:0>7d}.png'.format(frame_index)),no_simswaplogo,pasring_model =net,use_mask=use_mask, norm = spNorm)

            else:
                if not os.path.exists(temp_results_dir):
                    os.mkdir(temp_results_dir)
                frame = frame.astype(np.uint8)
                if not no_simswaplogo:
                    frame = logoclass.apply_frames(frame)
                cv2.imwrite(os.path.join(temp_results_dir, 'frame_{:0>7d}.png'.format(frame_index)), frame)
        else:
            break
    video.release()

    # image_filename_list = []
    path = os.path.join(temp_results_dir,'*.png')
    image_filenames = sorted(glob.glob(path))

    clips = ImageSequenceClip(image_filenames,fps = fps)

    if not no_audio:
        clips = clips.set_audio(video_audio_clip)

    source = os.path.basename(pic_a_path)
    target = os.path.basename(video_path)

    # print(f"{save_path}{source}_to_{target}{suffix}.mp4 saved")
    # clips.write_videofile(f"{save_path}{source}_to_{target}{suffix}.mp4",audio_codec='aac')

    print(f"FPS: {round(fps,2)}")
    video_file_out = uuid.uuid4()



    swaped_video_location = f"{save_path}{video_file_out}.mp4"
    set_swaped_video_location(swaped_video_location)
    clips.write_videofile(f"{swaped_video_location}",audio_codec='aac')


    # swaped_video_location = f"{save_path}{video_file_out}.webm"
    # set_swaped_video_location(swaped_video_location)
    # clips.write_videofile(f"{swaped_video_location}",codec='libvpx-vp9',
    #                  threads='12', bitrate='2500k',
    #                  ffmpeg_params=[
    #                      '-tile-columns', '6', '-frame-parallel', '0',
    #                      '-auto-alt-ref', '1', '-lag-in-frames', '25', '-g',
    #                      '128', '-pix_fmt', 'yuv420p', '-row-mt', '1']
    #                      )

    print(f"{swaped_video_location} saved")

def swap_video_512_v2(pic_a_path,video_path,output,temp_results,crop_size_p,watermark,use_mask,suffix,window):
    crop_size = crop_size_p
    opt = TestOptions().parse()
    opt.which_epoch = 390000
    opt.new_model = True
    opt.Arc_path = 'arcface_model/arcface_checkpoint.tar'
    opt.checkpoints_dir ='./checkpoints/simswap_512_test' 
    opt.crop_size = crop_size
    opt.isTrain = False
    start_epoch, epoch_iter = 1, 0
    torch.nn.Module.dump_patches = True

    torch.nn.Module.dump_patches = True
    if crop_size == 512:
      if opt.name == str(512):
        opt.which_epoch = 550000
        mode = 'ffhq'
      else:
        opt.Gdeep = True
        opt.new_model = True
        mode = 'None'

    if opt.new_model == True:
        model = fsModel()
        model.initialize(opt)
        model.netG.eval()
    else:            
        model = create_model(opt)
        model.eval()

    #AKA app
    detect_model = Face_detect_crop(name='antelope', root='./insightface_func/models')
    detect_model.prepare(ctx_id= 0, det_thresh=0.6, det_size=(640,640),mode=mode)
    with torch.no_grad():
        pic_a = pic_a_path
        # img_a = Image.open(pic_a).convert('RGB')
        img_a_whole = cv2.imread(pic_a)
        img_a_align_crop, _ = detect_model.get(img_a_whole,crop_size)
        img_a_align_crop_pil = Image.fromarray(cv2.cvtColor(img_a_align_crop[0],cv2.COLOR_BGR2RGB)) 
        img_a = transformer_Arcface(img_a_align_crop_pil)
        img_id = img_a.view(-1, img_a.shape[0], img_a.shape[1], img_a.shape[2])

        # convert numpy to tensor
        img_id = img_id.cuda()

        #create latent id
        img_id_downsample = F.interpolate(img_id, size=(112,112))
        latend_id = model.netArc(img_id_downsample)
        latend_id = F.normalize(latend_id, p=2, dim=1)

        threading.Thread(target=video_swap_512_v2(video_path, latend_id, model, detect_model, output, pic_a_path, suffix, temp_results, crop_size, watermark, use_mask,window,new_model=opt.new_model), daemon=True).start() 
        window.write_event_value('-VIDEO-SWAPED-',get_swaped_video_location())

def video_swap_512_v2(video_path, id_vetor, swap_model, detect_model, save_path,pic_a_path, suffix ,temp_results_dir='./temp_results', crop_size=224, no_simswaplogo = False,use_mask = True,window='window', new_model=False):



    print('************ Swap parameters START ************')
    print(f'crop_size:{crop_size}')
    print(f'use_mask_p:{use_mask}')
    print(f'no_watermark:{no_simswaplogo}')
    print('************ Swap parameters END ************')
    
    video_forcheck = VideoFileClip(video_path)
    if video_forcheck.audio is None:
        no_audio = True
    else:
        no_audio = False

    del video_forcheck

    if not no_audio:
        video_audio_clip = AudioFileClip(video_path)

    video = cv2.VideoCapture(video_path)
    logoclass = watermark_image('./simswaplogo/simswaplogo.png')
    ret = True
    frame_index = 0
    
    # set_video_frame_index(frame_index)

    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # set_video_frame_count(frame_count)
    # video_WIDTH = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))

    # video_HEIGHT = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    fps = video.get(cv2.CAP_PROP_FPS)
    if  os.path.exists(temp_results_dir):
            shutil.rmtree(temp_results_dir)

    spNorm =SpecificNorm()
    if use_mask:
        n_classes = 19
        net = BiSeNet(n_classes=n_classes)
        net.cuda()
        save_pth = os.path.join('./parsing_model/checkpoint', '79999_iter.pth')
        net.load_state_dict(torch.load(save_pth))
        net.eval()
    else:
        net =None

    
    start_time = dt.today().timestamp()

    pbar_progress_bar_key = '-pbar_progress_bar_video_face_swap-'
    pbar_percentage_key = '-pbar_percentage_video_face_swap-'
    pbar_index_range_video_key = '-pbar_index_range_video_face_swap-'
    pbar_iteration_per_sec_key = '-pbar_it_per_sec_video_face_swap-'
    pbar_estimated_time_key = '-pbar_estimated_time_video_face_swap-'

    for frame_index in tqdm(range(frame_count)):

        progress_bar_custom(frame_index,frame_count,start_time,window,pbar_progress_bar_key,pbar_percentage_key,pbar_index_range_video_key,pbar_iteration_per_sec_key,pbar_estimated_time_key)

        ret, frame = video.read()
        if  ret:
            detect_results = detect_model.get(frame,crop_size)

            if detect_results is not None:
                if not os.path.exists(temp_results_dir):
                        os.mkdir(temp_results_dir)
                frame_align_crop_list = detect_results[0]
                frame_mat_list = detect_results[1]
                swap_result_list = []
                frame_align_crop_tenor_list = []
                for frame_align_crop in frame_align_crop_list:

                    # BGR TO RGB
                    # frame_align_crop_RGB = frame_align_crop[...,::-1]

                    frame_align_crop_tenor = _totensor(cv2.cvtColor(frame_align_crop,cv2.COLOR_BGR2RGB))[None,...].cuda()

                    if new_model == True:
                        swap_result = swap_result_new_model(frame_align_crop, swap_model, id_vetor)
                    else:
                        swap_result = swap_model(None, frame_align_crop_tenor, id_vetor, None, True)[0]

                    cv2.imwrite(os.path.join(temp_results_dir, 'frame_{:0>7d}.jpg'.format(frame_index)), frame)
                    swap_result_list.append(swap_result)
                    frame_align_crop_tenor_list.append(frame_align_crop_tenor)

                    

                reverse2wholeimage(frame_align_crop_tenor_list,swap_result_list, frame_mat_list, crop_size, frame, logoclass,\
                    os.path.join(temp_results_dir, 'frame_{:0>7d}.jpg'.format(frame_index)),no_simswaplogo,pasring_model =net,use_mask=use_mask, norm = spNorm)

            else:
                if not os.path.exists(temp_results_dir):
                    os.mkdir(temp_results_dir)
                frame = frame.astype(np.uint8)
                if not no_simswaplogo:
                    frame = logoclass.apply_frames(frame)
                cv2.imwrite(os.path.join(temp_results_dir, 'frame_{:0>7d}.jpg'.format(frame_index)), frame)
        else:
            break

    video.release()

    # image_filename_list = []
    path = os.path.join(temp_results_dir,'*.jpg')
    image_filenames = sorted(glob.glob(path))

    clips = ImageSequenceClip(image_filenames,fps = fps)

    if not no_audio:
        clips = clips.set_audio(video_audio_clip)

    source = os.path.basename(pic_a_path)
    target = os.path.basename(video_path)

    # print(f"{save_path}{source}_to_{target}{suffix}.mp4 saved")
    print(f"FPS: {round(fps,2)}")
    video_file_out = uuid.uuid4()



    swaped_video_location = f"{save_path}{video_file_out}_512_v2.mp4"
    set_swaped_video_location(swaped_video_location)

    print(f"{swaped_video_location} saved")
    clips.write_videofile(f"{swaped_video_location}",audio_codec='aac')

    # swaped_video_location = f"{save_path}{source}_to_{target}{suffix}.mp4"
    # set_swaped_video_location(swaped_video_location)
    # clips.write_videofile(f"{save_path}{source}_to_{target}{suffix}.mp4",audio_codec='aac')
    pass

def swap_image_thread(source_file_path,target_file_path,save_path, suffix , crop_size_p, no_simswaplogo,use_mask_p,window,crop_512_version,source_file_list_with_path,target_file_list_with_path):
    # print('crop_512_version:', crop_512_version)

    print('swap_image_thread-source_file_list_with_path',source_file_list_with_path)
    print('swap_image_thread-source_file_path',source_file_path)

    if crop_512_version == 2:
        thread=threading.Thread(target=image_swap_512(source_file_path,target_file_path,save_path,suffix ,crop_size_p,no_simswaplogo,use_mask_p,source_file_list_with_path,target_file_list_with_path), daemon=True)
        thread.start()
        window.write_event_value('-IMAGE-SWAPED-',get_swaped_file_loc_512())        
    elif crop_512_version == 1:
        crop_swap_ver = 1
        thread=threading.Thread(target=image_swap(
            source_file_path,target_file_path,save_path,suffix ,crop_size_p,no_simswaplogo,use_mask_p,source_file_list_with_path,target_file_list_with_path,crop_swap_ver,window), daemon=True)
        thread.start()
        window.write_event_value('-IMAGE-SWAPED-',get_swaped_file_loc())   
    else:
        print('failed to swap image')
        window.write_event_value('-IMAGE-SWAPED-',"")   

def image_bio(filename,size):
    if os.path.exists(filename):
        image1 = Image.open(filename)
        image1.thumbnail(size)
        bio = io.BytesIO()
        image1.save(bio,format="PNG")
        del image1
        return bio.getvalue()

def get_img_data(filename,size, first=False):
    """Generate image data using PIL"""
    try:
        img = Image.open(filename)
    except:
        img = Image.open('input_placeholder.png')
        print('No Image found')
        
    img.thumbnail(size)
    if first:                     # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)

def download(URL, filelocation,window):
    multipliers = {
        'kilobyte':  1024,
        'megabyte':  1024 ** 2,
        'gigabyte':  1024 ** 3,
        'terabyte':  1024 ** 4,
        'petabyte':  1024 ** 5,
        'exabyte':   1024 ** 6,
        'zetabyte':  1024 ** 7,
        'yottabyte': 1024 ** 8,
        'kb': 1024,
        'mb': 1024**2,
        'gb': 1024**3,
        'tb': 1024**4,
        'pb': 1024**5,
        'eb': 1024**6,
        'zb': 1024**7,
        'yb': 1024**8,
    }    
    file_name =URL.rsplit('/', 1)[1]
    r = requests.get(URL, stream=True)
    total_size_in_bytes= int(r.headers.get('content-length', 0))
    block_size = multipliers['megabyte'] 
    dl = 0
    start_time = dt.today().timestamp()

    pbar_progress_bar_key = '-pbar_progress_bar_source_download-'
    pbar_percentage_key = '-pbar_percentage_source_download-'
    pbar_index_range_video_key = '-pbar_index_range_source_download-'
    pbar_iteration_per_sec_key = '-pbar_it_per_sec_source_download-'
    pbar_estimated_time_key = '-pbar_estimated_time_source_download-'

    with open(filelocation+file_name, 'wb') as f:
        for chunk in r.iter_content(block_size):
            dl += len(chunk)

            progress_bar_custom_download(dl,total_size_in_bytes,start_time,window,pbar_progress_bar_key,pbar_percentage_key,pbar_index_range_video_key,pbar_iteration_per_sec_key,pbar_estimated_time_key)

            if chunk:
                f.write(chunk)

def createNewDownloadThread(URL, filelocation,window):
    file_name =URL.rsplit('/', 1)[1]    
    download_thread = threading.Thread(target=download, args=(URL, filelocation,window), daemon=True)
    download_thread.start()
    if download_thread.is_alive():
        d_thread = True
        print("Downloading file...")
    else:
        print("Dead")
    while d_thread:
        if not download_thread.is_alive():
            d_thread = False
            print("File Downloaded")
            window.write_event_value('-FILE_DOWNLOADED-', filelocation+file_name)
            return 'File Downloaded'

def addto(result,event_name,window):
    global sum_p
    if result == True:
        window[event_name].update(disabled=False)
        window[event_name].update(checkbox_color='#1DD05D')
        sum_p = sum_p + 1
        window["-VERIFY_PRECENT-"].update(f'{round((sum_p/1*100))}%')

    if result == False:
        window[event_name].update(disabled=False)
        window[event_name].update(checkbox_color='#DB1D2F')

def verify(img1_path, img2_path,window):
    models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "SFace", "Dlib"]
    metrics = ["cosine", "euclidean", "euclidean_l2"]
    # img1_path = "./test/j/F8C16EC4-59C6-47D5-9E69-4D8CF76A5379.jpeg"
    # img2_path = "./test/j/ff9d96418185c03fdf59179602d9c6fa.jpg"
    model = 0
    metric = 0
    global sum_p
    sum_p = 0




    window["-VERIFY_PRECENT-"].update('0%')

    # window["-VGG-Face-C-MODEL-"].update(False,disabled=True)
    # window["-VGG-Face-L-MODEL-"].update(False,disabled=True)
    # window["-VGG-Face-L2-MODEL-"].update(False,disabled=True)

    # window["-Facenet-C-MODEL-"].update(False,disabled=True)
    # window["-Facenet-L-MODEL-"].update(False,disabled=True)
    # window["-Facenet-L2-MODEL-"].update(False,disabled=True)

    # window["-Facenet512-C-MODEL-"].update(False,disabled=True)
    # window["-Facenet512-L-MODEL-"].update(False,disabled=True)
    window["-Facenet512-L2-MODEL-"].update(False,disabled=True)

    # window["-ArcFace-C-MODEL-"].update(False,disabled=True)
    # window["-ArcFace-L-MODEL-"].update(False,disabled=True)
    # window["-ArcFace-L2-MODEL-"].update(False,disabled=True)

    # window["-SFace-C-MODEL-"].update(False,disabled=True)
    # window["-SFace-L-MODEL-"].update(False,disabled=True)
    # window["-SFace-L2-MODEL-"].update(False,disabled=True)





    # result1 = DeepFace.verify(img1_path, img2_path, model_name = models[0],distance_metric = metrics[0])
    # addto(result1['verified'],"-VGG-Face-C-MODEL-")

    # result2 = DeepFace.verify(img1_path, img2_path, model_name = models[0],distance_metric = metrics[1])
    # addto(result2['verified'],"-VGG-Face-L-MODEL-")
    
    # result3 = DeepFace.verify(img1_path, img2_path, model_name = models[0],distance_metric = metrics[2])
    # addto(result3['verified'],"-VGG-Face-L2-MODEL-",window)

    # result4 = DeepFace.verify(img1_path, img2_path, model_name = models[1],distance_metric = metrics[0])
    # addto(result4['verified'],"-Facenet-C-MODEL-")

    # result5 = DeepFace.verify(img1_path, img2_path, model_name = models[1],distance_metric = metrics[1])
    # addto(result5['verified'],"-Facenet-L-MODEL-")

    # result6 = DeepFace.verify(img1_path, img2_path, model_name = models[1],distance_metric = metrics[2])
    # addto(result6['verified'],"-Facenet-L2-MODEL-",window)

    # result7 = DeepFace.verify(img1_path, img2_path, model_name = models[2],distance_metric = metrics[0])
    # addto(result7['verified'],"-Facenet512-C-MODEL-")

    # result8 = DeepFace.verify(img1_path, img2_path, model_name = models[2],distance_metric = metrics[1])
    # addto(result8['verified'],"-Facenet512-L-MODEL-")

    result9 = DeepFace.verify(img1_path, img2_path, model_name = models[2],distance_metric = metrics[2])
    addto(result9['verified'],"-Facenet512-L2-MODEL-",window)

    # result19 = DeepFace.verify(img1_path, img2_path, model_name = models[6],distance_metric = metrics[0])
    # addto(result19['verified'],"-ArcFace-C-MODEL-")

    # result20 = DeepFace.verify(img1_path, img2_path, model_name = models[6],distance_metric = metrics[1])
    # addto(result20['verified'],"-ArcFace-L-MODEL-")

    # result21 = DeepFace.verify(img1_path, img2_path, model_name = models[6],distance_metric = metrics[2])
    # addto(result21['verified'],"-ArcFace-L2-MODEL-",window)

    # result22 = DeepFace.verify(img1_path, img2_path, model_name = models[7],distance_metric = metrics[0])
    # addto(result22['verified'],"-SFace-C-MODEL-")

    # result23 = DeepFace.verify(img1_path, img2_path, model_name = models[7],distance_metric = metrics[1])
    # addto(result23['verified'],"-SFace-L-MODEL-")

    # result24 = DeepFace.verify(img1_path, img2_path, model_name = models[7],distance_metric = metrics[2])
    # addto(result24['verified'],"-SFace-L2-MODEL-",window)
    pass

def watermark_parameters(event, values):
    global watermark
    
    if values['-WETMARK-'] == True:
        watermark = False
    if values['-WETMARK-'] == False:
        watermark = True
    if values['-DR-'] == True:
            util.add_watermark.set_oritation('DR')
    if values['-UR-'] == True:
            util.add_watermark.set_oritation('UR')
    if values['-DL-'] == True:
            util.add_watermark.set_oritation('DL')        
    if values['-UL-'] == True:
            util.add_watermark.set_oritation('UL') 
    if event == '-WETM_SIZE-':
            s = values['-WETM_SIZE-']
            util.add_watermark.set_size(s)      
    if event == '-DEG-':
            angle = values['-DEG-']
            util.add_watermark.set_angle(int(angle))

def swap_parameters(event, values):
    global crop_size
    global use_mask
    use_mask = values['-USE_MASK-']

    if values['-224-'] == True:
        crop_size = 224
    if values['-512-'] == True:
        crop_size = 512
    if values['-512_V2-'] == True:  
        crop_size = 512

def get_crop_512_version(values):
    if values['-512-'] == True:
        return 1
    if values['-512_V2-'] == True:
        return 2

def format_sec(sec):
    # sec = round(sec,2)
    formated_sec_step_1 = str(timedelta(seconds=sec))
    formated_sec = pd.to_datetime(formated_sec_step_1).strftime('%H:%M:%S')
    return formated_sec

def get_videofile_info(video_file):
    clip = VideoFileClip(video_file)

    # cap = cv2.VideoCapture(video_file)

    # fps = cap.get(cv2.CAP_PROP_FPS)

    # frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # duration = (frame_count / fps)

    # # dura = timedelta(seconds=duration)

    duration_full = format_sec(clip.duration)
    fps = clip.fps
    frame_count = int(clip.fps * clip.duration)

    # clip.save_frame(f"./processing_media/target_image.png", t=1)

    info = {
        'duration':duration_full,
        'frame_count':frame_count,
        'fps':fps,
        'size':clip.size
    }
    return info

def save_target_image_from_video(target_file_path,window,values):
    clip = VideoFileClip(target_file_path)
    clip.save_frame("./processing_media/target_image.png", t=1)

    file_target_image_frame ="./processing_media/target_image.png"
    if values['-SHOW_MEDIA-']:
        display_image(window['-target_image-'],file_target_image_frame,(300,300))    

def save_image_from_video_and_show(file_path,flie_name,window,values,window_name,size):
    clip = VideoFileClip(file_path)
    image_frame =f"./processing_media/{flie_name}.png"
    clip.save_frame(image_frame, t=1)
    if values['-SHOW_MEDIA-']:
        display_image(window[window_name],image_frame,(size))  

def video_cut_sec_end_chooser(values):
    if values['-video_cut_1sec-'] == True:
        return 1
    if values['-video_cut_3sec-'] == True:
        return 3
    if values['-video_cut_5sec-'] == True:
        return 5

def video_cutter(video_file,output="./processing_media/target_video_cut.mp4",start_time=0,end_time=3,r_width=128):
    
    print('video_cutter-r_width',r_width)
    call = shlex.split(
        f"ffmpeg -y -i  '{video_file}' -ss {start_time} -t {end_time} -vf scale=-2:{r_width} {output}")
    print(call)
    subprocess.call(call) 
    return output

def video_processing_resize_slide(percent,w,h):
    percent = int(float(percent))
    w = int((percent * float(w / 100)))
    h = int((float(h) * float(percent / 100)))
    
    def round_to_ceil_even(f):
        if (math.floor(f)%2 == 0): 
            return math.floor(f)
        else: 
            return math.floor(f)+1   

    even_w = round_to_ceil_even(w)
    even_h= round_to_ceil_even(h)

    return (even_w,even_h)

def disable_enable(window,state):
    window['-target_preview-'].update(disabled=state)
    window['-slider_video_resize_pre-'].update(disabled=state)
    window['-video_cut_custom_cut-'].update(disabled=state)
    window['-SWAP-'].update(disabled=state)
    window['-output_preview-'].update(disabled=state)

def slider(key,target_key,values,event,window):
    if event == key:
        slider = int(values[key])
        window[target_key].update(value=slider)    

def main(): 
    ver = '0.5.3'
    sg.theme('Dark Gray 15')
    global media_swap    
    media_swap = 'video_media'
    isSwaping = False
    output_target_video_cut = "./processing_media/target_video_cut.mp4"
    source_file_path= ''
    target_file_path=''
    selected_source_folder=''
    selected_target_folder=''
    loaded_target_type=0
    loaded_source_type=0
    global swaped_file_path   
    swaped_file_path=''
   
  

    def browse_layout(frame_name,file_name_,type_,visible_,disabled=False):
        file_name=f'-{file_name_}-'
        file_names=f'-{file_name_}s-'
        last_file_name = f'-last_{file_name_}-'
        clear_history= f'-clear_history_{file_name_}s-'

        if type_ == 'image':
            browse_type = sg.FileBrowse(initial_folder='./demo_file',k=f'-{file_name_}_FileBrowse-',file_types=(image_file_ext),disabled=disabled) 
        if type_ == 'video':
            browse_type = sg.FileBrowse(initial_folder='./demo_file',k=f'-{file_name_}_FileBrowse-',file_types=(video_file_ext),disabled=disabled) 
            type_ = 'image'
        if type_ == 'folder':
            browse_type = sg.FolderBrowse(disabled=disabled)

        layout = sg.Frame(frame_name,[
                                [
                                    sg.Combo(sorted(sg.user_settings_get_entry(file_names, [])),
                                        default_value=sg.user_settings_get_entry(last_file_name, ''), size=(50, 1), key=file_name,expand_x=True,enable_events=True,disabled=disabled), browse_type                               
                                ],
                                [ 
                                    sg.B('Clear History',k=clear_history,disabled=disabled)
                                ]
                            ],expand_x=True,k=f'-{file_name_}_frame_{type_}-',visible=visible_)
        # print(f'-{file_name_}_frame_{type_}-')
        return layout

    def browse_events(file_name_,loaded_source_type_,image_):
        # print('event trigger',file_name_)
        file_name=f'-{file_name_}-'
        file_names=f'-{file_name_}s-'
        last_file_name = f'-last_{file_name_}-'

        # print('file_names',file_names)

        source_file_list_with_path = []
        loaded_source_type = loaded_source_type_


        sg.user_settings_set_entry(file_names,
        list(set(sg.user_settings_get_entry(file_names, []) + [values[file_name], ])))

        sg.user_settings_set_entry(last_file_name, values[file_name])

        window[file_name].update(values=list(set(sg.user_settings_get_entry(file_names, []) + [values[file_name], ])),value=values[file_name])
        source_file_path = values[file_name]

        if values['-SHOW_MEDIA-']:
            display_image(window[image_],source_file_path,(300,300))



        last_path = os.path.dirname(source_file_path)
        window[f"-{file_name_}_FileBrowse-"].InitialFolder = last_path

        return source_file_list_with_path,loaded_source_type,source_file_path

    def browse_events_video(file_name_,loaded_source_type_):


        file_name=f'-{file_name_}-'
        file_names=f'-{file_name_}s-'
        last_file_name = f'-last_{file_name_}-'

        loaded_source_type = loaded_source_type_

        sg.user_settings_set_entry(file_names,
        list(set(sg.user_settings_get_entry(file_names, []) + [values[file_name], ])))

        sg.user_settings_set_entry(last_file_name, values[file_name])

        window[file_name].update(values=list(set(sg.user_settings_get_entry(file_names, []) + [values[file_name], ])),value=values[file_name])

        target_file_path = values[file_name]



        save_target_image_from_video(target_file_path,window,values)

        last_path = os.path.dirname(target_file_path)
        window[f"-{file_name_}_FileBrowse-"].InitialFolder = last_path

        duration = get_videofile_info(target_file_path)['duration']
        frame_count = get_videofile_info(target_file_path)['frame_count']
        fps = round(get_videofile_info(target_file_path)['fps'])
        size = get_videofile_info(target_file_path)['size']

        window['-video_cut_original_duration-'].update(f"Duration: {duration}")     
        window['-video_cut_original_frame_count-'].update(f"Frame Count: {frame_count}")     
        window['-video_cut_original_fps-'].update(f"FPS Count: {fps}")     
        window['-display_video_resize_pre-'].update(f'{size[0]} X {size[1]}')


        if values['-video_cut_auto-']==True:
            disable_enable(window,True)

            end_time = video_cut_sec_end_chooser(values)
            target_file_path = video_cutter(target_file_path,output_target_video_cut,0,end_time,size[0])    


        save_target_image_from_video(target_file_path,window,values)
        disable_enable(window,False)
        display_notification("video cut endded successfully", '', img_success, 100, use_fade_in=False,alpha=1, location=(500,500))  

        return loaded_source_type,target_file_path,size

    def clear_history(file_name_):
        file_name=f'-{file_name_}-'
        file_names=f'-{file_name_}s-'
        last_file_name = f'-last_{file_name_}-'
        clear_history= f'-clear_history_{file_name_}s-'

        # print('clear_history_file_names',clear_history)

        #clear but save last entry
        # sg.user_settings_set_entry('-source_file_names-', [values['-source_file_name-']])
        # sg.user_settings_set_entry('-last_source_file_name-', values['-source_file_name-'])
        # window['-source_file_name-'].update(values=[], value=values['-source_file_name-'])

        #clear all
        sg.user_settings_set_entry(file_names, [])
        sg.user_settings_set_entry(last_file_name, '')
        window[file_name].update(values=[], value='')
    

    source_image_browse_layout = browse_layout('Image','source_file_name','image',True)
    target_image_browse_layout = browse_layout('Image','target_file_name','image',False)
    target_video_browse_layout = browse_layout('Video','target_video_name','video',True)
    output_folder_browse_layout = browse_layout('Folder','output_folder_name','folder',True,True)

    # source_folder_browse_layout = browse_layout('Folder','source_folder_name','folder',False)

    #Source
    left_col = [
        #Source display
        [
            sg.Frame('Source',[
                    [sg.Image(image_bio('input_placeholder.png',(300,300)),expand_x=True,k='-source_image-')],
                ],expand_x=True,element_justification='center',vertical_alignment='center',s=(300,300),visible=True
            ),
        ],

        #Source broswer
        [
            sg.Frame('',[
                    [
                        sg.Radio('Folder','source_type_browse_radio',enable_events=True,k='-source_type_browse_radio_folder-',disabled=True),
                        sg.Radio('Image','source_type_browse_radio',default=True,enable_events=True,k='-source_type_browse_radio_image-'),
                    ],
                    [
                        source_image_browse_layout,
                        # source_folder_browse_layout
                    ],
                ],expand_x=True,element_justification='right',
            ),
        ],        

        #Source controls
        [
            sg.Button('Preview',k='-source-preview-',expand_x=True),
            sg.Button('Open Folder',k='-source_reveal_folder-',expand_x=True),
            sg.Button('Download',k='-DOWNLOAD_SOURCE_FILE-',expand_x=True,disabled=True),                         
        ], 
        
        #Source Options
        [
           sg.Frame('Options',[
                [
                    sg.Checkbox('Show Media',default=True,enable_events=True,k="-SHOW_MEDIA-"),
                ]

                ],expand_x=True,visible=False,#element_justification='center',vertical_alignment='center'     
            ),        
        ],     
       
        #Source resize
        [
            sg.Frame('Resize',[
                [   
                    sg.Text('0 x 0',k='-display_source_resize-',expand_x=True,s=(12,1),justification='center',font='Any 12'),
                    sg.Text('100%',s=(5,1),font='Any 12',k='-display_source_resize_percentage-'),
                    sg.Slider(default_value=100,range=((10,100)),resolution=1,
                    disable_number_display=True,
                    orientation='horizontal',enable_events=True,k='-slider_source_resize-',expand_x=True,disabled=True),
                    # sg.OptionMenu(values=(320, 640, 720),default_value=720,k='-target_resize_preset-'),                    

                ]

            ],visible=False,expand_x=True,#element_justification='center'
        ),                                 
        ],   

        #terminal     
        [
            sg.MLine( k='-ML2-', reroute_stdout=True,write_only=False,reroute_cprint=True,
            background_color='black', text_color='white', autoscroll=True, auto_refresh=True,expand_x=True,expand_y=True,visible=True)
        ],

    ]

    #Target
    center_col = [   
        #target display
        [
                sg.Frame('Target',[
                    [sg.Image(image_bio('input_placeholder.png',(300,300)),expand_x=True,k='-target_image-')],               
                ],expand_x=True,element_justification='center',vertical_alignment='center',s=(300,300),visible=True

            ), 
        ], 

        #Target broswer
        [
                sg.Frame('',[
                    [
                        sg.Radio('Video Folder','media_swap',default=False,enable_events=True,k='-MEDIA_SWAP_vid_folder-',disabled=True),                        
                        sg.Radio('Image Folder','media_swap',default=False,enable_events=True,k='-MEDIA_SWAP_img_folder-',disabled=True),   
                        sg.Radio('Video','media_swap',default=True,enable_events=True,k='-MEDIA_SWAP_VID-'),     
                        sg.Radio('Image','media_swap',default=False,enable_events=True,k='-MEDIA_SWAP_IMG-'),
                    ],
                    [
                        target_image_browse_layout,
                        target_video_browse_layout                        
                    ],                     
                ],expand_x=True,element_justification='right',#vertical_alignment='center',s=(300,300)
                
            ), 
        ],    

        #Target controls
        [
            sg.Button('Preview',k='-target_preview-',expand_x=True) ,
            sg.Button('Open Folder',k='-target_reveal_folder-',expand_x=True),
            sg.Button('Download',k='-DOWNLOAD_TARGET_FILE-',expand_x=True,disabled=True),                                       
        ],  

        #Target resize
        [
            sg.Frame('Resize',[
                [   
                    sg.Text('0 x 0',k='-display_video_resize_pre-',expand_x=True,s=(12,1),justification='center',font='Any 12'),
                    sg.Text('100%',s=(5,1),font='Any 12',k='-display_target_resize_percentage-'),
                    sg.Slider(default_value=100,range=((10,100)),resolution=1,
                    disable_number_display=True,
                    orientation='horizontal',enable_events=True,k='-slider_video_resize_pre-',expand_x=True),
                    # sg.OptionMenu(values=(320, 640, 720),default_value=720,k='-target_resize_preset-'),                    
                ]
            ],expand_x=True,#element_justification='center'
        ),                                 
        ],   

        #Target Video cut
        [
                sg.Frame('Video cut',[
                    [
                        sg.Text("Duration: 00:00:00",k='-video_cut_original_duration-',justification='left'),
                        sg.Text("Frame Count: 0",k='-video_cut_original_frame_count-',justification='center'),
                        sg.Text("FPS: 0",k='-video_cut_original_fps-',justification='right'),
                    ],
                    [  
                        sg.Checkbox('Auto',k='-video_cut_auto-',default=False),
                        sg.Radio('1s','video_cut',default=True,enable_events=True,k='-video_cut_1sec-'),
                        sg.Radio('3s','video_cut',default=False,enable_events=True,k='-video_cut_3sec-'),
                        sg.Radio('5s','video_cut',default=False,enable_events=True,k='-video_cut_5sec-'),
                        sg.VerticalSeparator(),
                        # sg.Radio('Manual','video_cut',default=False,enable_events=True,k='-video_cut_custom_time-'),
                        # sg.Button('Cut',expand_x=True,k='-video_cut_preset_cut-'),
                        sg.Text('Start'),sg.In('00:00:00',size=(10, 2),justification='center',k='-video_cut_custom_start_time-'),
                        sg.Text('End'),sg.In('1',size=(5, 2),justification='center',k='-video_cut_custom_end_time-'),
                        sg.Button('Cut',expand_x=True,k='-video_cut_custom_cut-')
                    ],
                    
                ],expand_x=True
            )
        ],      

        #Swaping
        [
            sg.Frame('Swaping',[
                    # [
                    #     sg.Frame('Batch',[
                    #         [
                    #             sg.Checkbox('',k='-batch-',default=False,disabled=True),
                    #         ]
                    #     ],expand_x=True,expand_y=True,element_justification='center',visible=True),
                    # sg.Frame('Kernel Mask Size',[
                    #     [

                    #         sg.Text('Left'),sg.In(40,s=(3,1),justification='center',enable_events=True,k='-mask_kernel_size_left-'),
                    #         sg.Text('Right'),sg.In(40,s=(3,1),justification='center',enable_events=True,k='-mask_kernel_size_right-'),

                    #     ]

                    # ],expand_x=True,expand_y=True,element_justification='center',visible=True
                    # ),  
                    #     sg.Frame('Crop Masking',[
                    #         [
                    #             sg.Radio('224','Crop_size',default=True,enable_events=True,k='-224-'),
                    #             sg.Radio('512','Crop_size',enable_events=True,k='-512-'),
                    #             sg.Radio('512-V2','Crop_size',enable_events=True,k='-512_V2-'),
                    #             sg.Checkbox('use_mask',default=True,enable_events=True,k="-USE_MASK-"),
                    #             # sg.Button('Swap',k='-SWAP-',expand_x=True,expand_y=True),
                    #         ]
                    #     ],expand_x=True,expand_y=True,visible=True),            
                    # ],   
                    # [
                    #     sg.Frame('GPU',[
                    #         [
                    #             sg.Checkbox('',k='-gpu-',default=True,disabled=False),
                    #         ]
                    #     ],expand_x=True,expand_y=True,element_justification='center',visible=True),
                    # sg.Frame('Kernel Mask Size',[
                    #     [

                    #         sg.Text('Left'),sg.In(40,s=(3,1),justification='center',enable_events=True,k='-mask_kernel_size_left-'),
                    #         sg.Text('Right'),sg.In(40,s=(3,1),justification='center',enable_events=True,k='-mask_kernel_size_right-'),

                    #     ]

                    # ],expand_x=True,expand_y=True,element_justification='center',visible=True
                    # ),  
                    #     sg.Frame('Crop Masking',[
                    #         [
                    #             sg.Radio('224','Crop_size',default=True,enable_events=True,k='-224-'),
                    #             sg.Radio('512','Crop_size',enable_events=True,k='-512-'),
                    #             sg.Radio('512-V2','Crop_size',enable_events=True,k='-512_V2-'),
                    #             sg.Checkbox('use_mask',default=True,enable_events=True,k="-USE_MASK-"),
                    #             # sg.Button('Swap',k='-SWAP-',expand_x=True,expand_y=True),
                    #         ]
                    #     ],expand_x=True,expand_y=True,visible=True),            
                    # ],   
                    [  
                        sg.Checkbox('GPU',k='-use_gpu-',default=True,disabled=True),
                        sg.Checkbox('Keep Frames',default=False,k="-keep_frames-"),
                        sg.Checkbox('Keep FPS',default=True,k="-keep_fps-"),
                        sg.Checkbox('',default=False,k="-use_max_memory-"),
                        sg.Text('Set Max Memory'),sg.In(16,size=(10, 2),justification='center',k='-max_memory-'),sg.Text('GB'),
                        # sg.VerticalSeparator(),
                        sg.Text('GPU Threads',visible=False),sg.In(1,size=(5, 2),justification='center',k='-gpu_threads-',visible=False),
                    ],             
                    [
                        sg.Button('Swap',k='-SWAP-',expand_x=True,expand_y=True),
                        # sg.Button('Play',k='-play_output_preview-',expand_x=True,visible=False),
                    ]          

                ],expand_x=True,element_justification='center'
            )  
        ],
    ]
    
    #Output
    right_col = [
        #Output display
        [
            sg.Frame('Output',[
                    # [sg.Text('FileName',k='-OUTPUT_IN-',enable_events=True,expand_x=True)],
                    [sg.Image(image_bio('output_placeholder.png',(400,400)),expand_x=True,k='-OUTPUT_FILE-')],
                ],expand_x=True,element_justification='center',vertical_alignment='center',s=(400,400),visible=True
            )    
        ],

        #Output broswer
        [
            sg.Frame('',[
                    [
                        output_folder_browse_layout
                    ]
                ],expand_x=True,element_justification='center',visible=False
            )    
        ], 

        #Output controls
        [
            sg.Button('Preview',k='-output_preview-',expand_x=True),
            sg.Button('Open Folder',k='-output_reveal_folder-',expand_x=True),
        ],          

        #Output Wetmark
        [
            sg.Frame('Wetmark',[
                    [
                        sg.Checkbox('',default=False,enable_events=True,k="-WETMARK-"),
                        sg.Radio('DR','wetmark_dir',default=True,enable_events=True,k='-DR-'),
                        sg.Radio('DL','wetmark_dir',enable_events=True,k='-DL-'),
                        sg.Radio('UL','wetmark_dir',enable_events=True,k='-UL-'),
                        sg.Radio('UR','wetmark_dir',enable_events=True,k='-UR-'),
                        sg.In(0,s=(4,1),justification='center',enable_events=True,k='-DEG-'),
                        sg.Slider(default_value=0.5,range=((0.1,0.9)),resolution=.1,orientation='horizontal',enable_events=True,k='-WETM_SIZE-',expand_x=True)
                    ]
                ],expand_x=True,visible=False
            )  
        ],  

        [
            sg.Frame('Post Process',[
                    [
                        sg.Text('0 x 0',k='-post_process_file_size_display-',expand_x=True)
                    ],
                    [
                        sg.Input(k='-post_process_file_input-',enable_events=True,expand_x=True),sg.FileBrowse(initial_folder='./output/videos',k=f'-post_process_FileBrowse-',file_types=(video_file_ext)) 
                    ],
                ],expand_x=True,visible=False
            )
        ],

        [
            sg.Frame('CodeFormer ',[

                    [
                        sg.Checkbox('',default=False,enable_events=True,k="-watermark_check-"),
                        sg.T('Visibility',s=(10,1),k='-watermark_font_size_display-'),
                        sg.Slider(default_value=20,range=((0,300)),resolution=1,orientation='horizontal',enable_events=True,
                        disable_number_display=True,k='-watermark_font_size-',expand_x=True,s=(10,15),relief='flat'),
                        sg.T('Weight ',s=(10,1),k='-watermark_font_size_display2-'),
                        sg.Slider(default_value=20,range=((0,300)),resolution=1,orientation='horizontal',enable_events=True,
                        disable_number_display=True,k='-watermark_font_size-',expand_x=True,s=(10,15),relief='flat')
                    ]
                ],expand_x=True,visible=False
            )  
        ],      
        #watermark new
        [
            sg.Frame('Watermark',[
                    [
                        sg.I('github.com/diStyApps/seait',k='-watermark_text-',expand_x=True)
                    ],
                    [
                        sg.Checkbox('',default=True,enable_events=True,k="-watermark_check-"),
                        sg.T('Position'),sg.Combo(values=('Top center', 'Bottom center','Centered', 'Top left','Top right','Bottom left','Bottom right'),default_value='Bottom center', readonly=True, k='-watermark_positions-'),
                        sg.T('Color'),sg.In('#817d73',s=(10,1),justification='center',k='-watermark_font_color-'),
                        sg.T('Size: 20',s=(10,1),k='-watermark_font_size_display-'),sg.Slider(default_value=20,range=((0,300)),resolution=1,orientation='horizontal',enable_events=True,
                        disable_number_display=True,k='-watermark_font_size-',expand_x=True,s=(10,15),relief='flat')
                    ]
                ],expand_x=True,visible=False
            )  
        ],            



        #crop  
        [
            sg.Frame('Crop',[
                    [
                        sg.Frame('',[
                            [
                                sg.T('X')
                            ],
                            [
                                sg.In(0,s=(10,1),key='-crop_input_x-',justification='center',k='-crop_x-',expand_x=True),
                            ],
                            [
                                sg.Slider(default_value=0,range=((0,300)),resolution=1,orientation='horizontal',disable_number_display=True,enable_events=True,k='-crop_slider_x-',expand_x=True,s=(10,12)),                        
                            ]
                        ],expand_x=True,element_justification='center'),

                        sg.Frame('',[
                            [
                                sg.T('Y')
                            ],
                            [
                                sg.In(0,s=(10,1),key='-crop_input_y-',justification='center',k='-crop_y-',expand_x=True),
                            ],
                            [
                                sg.Slider(default_value=0,range=((0,300)),resolution=1,orientation='horizontal',disable_number_display=True,enable_events=True,k='-crop_slider_y-',expand_x=True,s=(10,12)),                        
                            ]
                        ],expand_x=True,element_justification='center'),

                        sg.Frame('',[
                            [
                                sg.T('W')
                            ],
                            [
                                sg.In(0,s=(10,1),key='-crop_input_w-',justification='center',k='-crop_w-',expand_x=True),
                            ],
                            [
                                sg.Slider(default_value=0,range=((0,300)),resolution=1,orientation='horizontal',disable_number_display=True,enable_events=True,k='-crop_slider_w-',expand_x=True,s=(10,12)),                        
                            ]
                        ],expand_x=True,element_justification='center'),

                        sg.Frame('',[
                            [
                                sg.T('H')
                            ],
                            [
                                sg.In(0,s=(10,1),key='-crop_input_h-',justification='center',k='-crop_h-',expand_x=True),
                            ],
                            [
                                sg.Slider(default_value=0,range=((0,300)),resolution=1,orientation='horizontal',disable_number_display=True,enable_events=True,k='-crop_slider_h-',expand_x=True,s=(10,12)),                        
                            ]
                        ],expand_x=True,element_justification='center'),
                    ],
                    [
                        sg.B('Test',k='-crop_and_put_logo_test-',expand_x=True),
                        sg.B('Crop',k='-crop_and_put_logo-',expand_x=True),
                        sg.B('img',k='-crop_show_image-',expand_x=True,disabled=True),
                        sg.B('vid',k='-crop_show_video-',expand_x=True,disabled=True)
                    ]
                ],expand_x=True,visible=False
            )  
        ],

        #delogo
        [
            sg.Frame('Delogo',[
                    [
                        sg.Frame('',[
                            [
                                sg.T('X')
                            ],
                            [
                                sg.In(0,s=(10,1),key='-delogo_input_x-',justification='center',expand_x=True),
                            ],
                            [
                                sg.Slider(default_value=0,range=((0,608)),resolution=1,orientation='horizontal',disable_number_display=True,enable_events=True,k='-delogo_slider_x-',expand_x=True,s=(10,12)),                        
                            ]
                        ],expand_x=True,element_justification='center'),

                        sg.Frame('',[
                            [
                                sg.T('Y')
                            ],
                            [
                                sg.In(0,s=(10,1),key='-delogo_input_y-',justification='center',expand_x=True),
                            ],
                            [
                                sg.Slider(default_value=0,range=((0,1080)),resolution=1,orientation='horizontal',disable_number_display=True,enable_events=True,k='-delogo_slider_y-',expand_x=True,s=(10,12)),                        
                            ]
                        ],expand_x=True,element_justification='center'),

                        sg.Frame('',[
                            [
                                sg.T('W')
                            ],
                            [
                                sg.In(0,s=(10,1),key='-delogo_input_w-',justification='center',expand_x=True),
                            ],
                            [
                                sg.Slider(default_value=0,range=((0,500)),resolution=1,orientation='horizontal',disable_number_display=True,enable_events=True,k='-delogo_slider_w-',expand_x=True,s=(10,12)),                        
                            ]
                        ],expand_x=True,element_justification='center'),
                        
                        sg.Frame('',[
                            [
                                sg.T('H')
                            ],
                            [
                                sg.In(0,s=(10,1),key='-delogo_input_h-',justification='center',expand_x=True),
                            ],
                            [
                                sg.Slider(default_value=0,range=((0,500)),resolution=1,orientation='horizontal',disable_number_display=True,enable_events=True,k='-delogo_slider_h-',expand_x=True,s=(10,12)),                        
                            ]
                        ],expand_x=True,element_justification='center'),
                    ],
                    [
                        sg.T('Show: '),sg.Checkbox('',default=False,enable_events=True,k="-show_delogo-"),
                        sg.B('Test',k='-delogo_test_go-',expand_x=True),
                        sg.B('Delogo',k='-delogo_go-',expand_x=True),
                        sg.B('img',k='-delogo_show_image-',expand_x=True,disabled=True),
                        sg.B('vid',k='-delogo_show_video-',expand_x=True,disabled=True)
                    ]
                ],expand_x=True,visible=False
            )  
        ], 

        #Output Final
        [
           sg.Frame('Final',[
                [                   
                    sg.Frame('Save Image',[
                        [
                            sg.Radio('PNG','save_image_final',default=True,enable_events=True,k='-save_image_png-',disabled=True),
                            sg.Radio('JPG','save_image_final',enable_events=True,k='-save_image_jpg-',disabled=True),                            
                            sg.Button('Save',expand_x=True,disabled=True),
                        ]

                    ],expand_x=True,expand_y=True,#element_justification='center'
                ), 
                    sg.Frame('Save Video',[
                        [
                            sg.Radio('MP4','save_video_final',default=True,enable_events=True,k='-save_video_mp4-',disabled=True),
                            sg.Radio('WEBM','save_video_final',enable_events=True,k='-save_video_webm-',disabled=True),
                            sg.Radio('GIF','save_video_final',enable_events=True,k='-save_video_gif-',disabled=True),                            
                            sg.Button('Save',expand_x=True,disabled=True),
                        ]

                    ],expand_x=True,expand_y=True,#element_justification='center'
                ),                                   
                ],
                ],expand_x=True,visible=False#element_justification='center',vertical_alignment='center'     
            ),
        ],              
    ]

    layout = [
            # [sg.HorizontalSeparator()],

            [
                        sg.Frame('',[
                    [
                            sg.Text('Help support this project'),
                            sg.Button(image_data=patreon,key='PATREON_BTN_KEY',button_color=(GRAY_9900)),            
                    ],
                    ],expand_x=True,element_justification='r',border_width=0,pad=(0,0),relief=sg.RELIEF_FLAT
                ),
            ],        
            [
                        sg.Frame('Video Swaping',[
                        [
                            sg.Text('0%',k='-pbar_percentage_video_face_swap-',size=(5, 1)),
                            sg.ProgressBar(12, orientation='h', size=(15, 15),expand_x=True, key='-pbar_progress_bar_video_face_swap-'),
                            sg.Text('0/0',k='-pbar_index_range_video_face_swap-',expand_x=True,size=(5, 1)),
                            sg.Text('0.0 it/s',k='-pbar_it_per_sec_video_face_swap-',expand_x=False,size=(10, 1)),
                            sg.Text('00:00:00 / 00:00:00 < 00:00:00',k='-pbar_estimated_time_video_face_swap-',expand_x=False),
                        ],
                    ],expand_x=True
                ),



            ],                  
            [
                #Source
                sg.Column(left_col, key='c1', element_justification='l', expand_x=True,expand_y=True),
                #Target
                sg.Column(center_col, key='c2', element_justification='c', expand_x=True,expand_y=True),
                #Output
                sg.Column(right_col, key='c3', element_justification='r', expand_x=True,expand_y=True)
            ],

            #video Swaping progressbar
      

            #downloading progressbar
            [

                        sg.Frame('Download',[
                        [
                            sg.Text('0%',k='-pbar_percentage_source_download-',size=(5, 1)),
                            sg.ProgressBar(12, orientation='h', size=(15, 15),expand_x=True, key='-pbar_progress_bar_source_download-'),
                            sg.Text('0/0',k='-pbar_index_range_source_download-',expand_x=True,size=(5, 1)),
                            sg.Text('0.0 it/s',k='-pbar_it_per_sec_source_download-',expand_x=False,size=(10, 1)),
                            sg.Text('00:00:00 / 00:00:00 < 00:00:00',k='-pbar_estimated_time_source_download-',expand_x=False),
                        ],
                    ],expand_x=True,visible=False
                )                         
            ],            
            ]

    window = sg.Window(f'FaceSwap Suite Ver {ver}',layout,finalize=True, resizable=True)
    window.Maximize()
    flatten_ui_elements(window)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        def setup():
            swap_parameters(event, values)
            watermark_parameters(event, values) 
            set_mask_kernel_size((int(values['-mask_kernel_size_left-']),int(values['-mask_kernel_size_right-'])))
        # setup()
        
        slider('-delogo_slider_x-','-delogo_input_x-',values,event,window)
        slider('-delogo_slider_y-','-delogo_input_y-',values,event,window)
        slider('-delogo_slider_h-','-delogo_input_h-',values,event,window)
        slider('-delogo_slider_w-','-delogo_input_w-',values,event,window)

        slider('-crop_slider_x-','-crop_input_x-',values,event,window)
        slider('-crop_slider_y-','-crop_input_y-',values,event,window)
        slider('-crop_slider_h-','-crop_input_h-',values,event,window)
        slider('-crop_slider_w-','-crop_input_w-',values,event,window)


        if event == '-SHOW_MEDIA-':
            show_media(window,values,source_file_path,target_file_path)

        if event == '-MEDIA_SWAP_IMG-':
            if values['-MEDIA_SWAP_IMG-'] == True:
                media_swap ='image_media'              
                window["-target_video_name_frame_image-"].update(visible = False)
                window["-target_file_name_frame_image-"].update(visible = True)

        if event == '-MEDIA_SWAP_VID-':
            if values['-MEDIA_SWAP_VID-'] == True:
                media_swap ='video_media'             
                window["-target_file_name_frame_image-"].update(visible = False)
                window["-target_video_name_frame_image-"].update(visible = True)

        # if event == '-source_type_browse_radio_image-':
        #     window["-source_frame_folder-"].update(visible = False)
        #     window["-source_frame_image-"].update(visible = True)

        # if event == '-source_type_browse_radio_folder-':
        #     window["-source_frame_image-"].update(visible = False)
        #     window["-source_frame_folder-"].update(visible = True)            
            pass

        if event == '-source_file_name-':  
            source_file_list_with_path,loaded_source_type,source_file_path = browse_events('source_file_name','file',"-source_image-")

        if event == '-target_file_name-':  
            target_file_list_with_path,loaded_target_type,target_file_path = browse_events('target_file_name','file',"-target_image-")

        if event == '-target_video_name-':  
            window['-target_video_name-'].update(disabled=True)
            loaded_source_type,target_file_path,size = browse_events_video('target_video_name','file')
            window['-target_video_name-'].update(disabled=False)

        if event == '-clear_history_source_file_names-':
            clear_history('source_file_name')

        if event == '-clear_history_target_file_names-':
            clear_history('target_file_name')  

        if event == '-clear_history_target_video_names-':
            clear_history('target_video_name')  

        if event == '-source-preview-':    
            os.popen(os.path.abspath(source_file_path))   

        if event == '-source_reveal_folder-':
            if loaded_source_type == 'file':
                os.startfile(os.path.dirname(source_file_path))   
            if loaded_source_type == 'folder':
                os.startfile(os.path.abspath(selected_source_folder))     

        if event == '-select_target_folder_input-':
            window["-select_target_file_input-"].update(visible = False)
            window["-select_target_video_input-"].update(visible = False)
            window["-select_target_folder_input-"].update(visible = True)

            
            selected_target_folder = values['-select_target_folder_input-']
            display_image(window["-target_image-"],'input_placeholder.png',(300,300))

            target_file_list = os.listdir(selected_target_folder)
            target_file_path=''
            target_file_list_with_path = []
            loaded_target_type = 'folder'

            for f_ in target_file_list:
                target_files_path_ = os.path.join(selected_target_folder, f_)
                target_file_list_with_path.append(target_files_path_)

        if event == '-target_preview-':    
            os.popen(os.path.abspath(target_file_path))

        if event == '-target_reveal_folder-':    
            if loaded_target_type == 'file':
                os.startfile(os.path.dirname(target_file_path))   
            if loaded_target_type == 'folder':
                os.startfile(os.path.abspath(os.path.dirname(target_file_path))) 

        #output 
        if event == '-output_preview-': 
            print('-output_preview-')
            print(swaped_file_path)
            # print(os.path.dirname(swaped_file_path))
            os.popen(os.path.abspath(swaped_file_path))   

        if event == '-play_output_preview-': 
            print('-play_output_preview-')
            print(swaped_file_path)
            # print(os.path.dirname(swaped_file_path))
            os.popen(os.path.abspath(swaped_file_path))   

        if event == '-output_reveal_folder-':    
            startfile_path = os.path.dirname(swaped_file_path)        

            os.startfile(os.path.abspath(startfile_path))

        if event =='-video_cut_1sec-':
            window['-video_cut_custom_end_time-'].update(value=1)
        if event =='-video_cut_3sec-':
            window['-video_cut_custom_end_time-'].update(value=3)
        if event =='-video_cut_5sec-':
            window['-video_cut_custom_end_time-'].update(value=5)

        #video editig
        if event == '-slider_video_resize_pre-':
            percent = values['-slider_video_resize_pre-']
            resized=video_processing_resize_slide(percent,size[0],size[1])     
            int_percent = int(percent)
            window['-display_video_resize_pre-'].update(f'{resized[0]} X {resized[1]}')
            window['-display_target_resize_percentage-'].update(f'{int_percent}%')

        if event == '-video_cut_custom_cut-':   
            target_file_path = values['-target_video_name-']

            start_time = values['-video_cut_custom_start_time-']
            end_time = values['-video_cut_custom_end_time-']

            disable_enable(window,True)
            try:
                target_file_path = video_cutter(target_file_path,output_target_video_cut,start_time,end_time,resized[1])
            except:
                target_file_path = video_cutter(target_file_path,output_target_video_cut,start_time,end_time,size[1])
            
            display_notification("video cut ended successfully", '', img_success, 100, use_fade_in=False,alpha=1, location=(500,500))  

            disable_enable(window,False)

            save_target_image_from_video(target_file_path,window,values)

        #swaping
        if event == '-IMAGE-SWAPED-':
            print('-IMAGE-SWAPED- triggerd')
            disable_enable(window,False)

            # if values['-512_V2-'] == True:
            #     swaped_file_path = get_swaped_file_loc_512()
            # else:
            #     swaped_file_path = get_swaped_file_loc()

            if values['-target_file_name-']:
                if values['-SHOW_MEDIA-']:
                    display_image(window["-OUTPUT_FILE-"],swaped_file_path,(400,550))
                pass


            display_notification('Image swaped completed successfully', '', img_success, 100, use_fade_in=False,alpha=1, location=(500,500))   
         
        if event == '-VIDEO-SWAPED-':
            disable_enable(window,False)
            print('video swaped',values['-VIDEO-SWAPED-'])
            # swaped_file_path = values['-VIDEO-SWAPED-']
            # # os.popen(values['-VIDEO-SWAPED-'][1:])
            # # print('-VIDEO-SWAPED-','event',event,'values',values,get_swaped_video_location())
            # swaped_file_path_full = os.path.abspath(swaped_file_path)

            # print(swaped_file_path_full)


            # window['-post_process_file_input-'].update(value=swaped_file_path_full)

            # window.write_event_value('-post_process_file_input-',swaped_file_path_full)


            display_notification('Video swaped completed successfully', '', img_success, 10000, use_fade_in=False,alpha=1, location=(500,500))   

        if event == '-SHOW_SWAPED_IMAGE-':
            print(swaped_file_path)
            im = Image.open(swaped_file_path)
            im.show()            

        if event == '-SWAP-':

            isSwaping = True
            disable_enable(window,True)
            dir_path = "output"
            dir_temp= "temp"
            out_filename = uuid.uuid4()
            # full_path = os.path.join(dir_path, sub_dir, f"{out_filename}.mp4")
            # dir_temp = os.path.join(dir_path)
            current_dir = os.getcwd()
            dir_temp = os.path.join(current_dir, dir_path)
            # print('dir_temp',dir_temp)
            # print('gpu_threads',int(values['-gpu_threads-']))

            args = {}
            cores_count = max(psutil.cpu_count() - 2, 2)
            core.args['source_img'] = source_file_path
            core.args['target_path'] = target_file_path
            core.args['frame_paths'] = dir_temp
            core.args['cores_count'] =  cores_count
            core.args['keep_frames'] = values['-keep_frames-']
            core.args['keep_fps'] = values['-keep_fps-']
            core.args['gpu'] = values['-use_gpu-']
            # core.args['gpu_threads'] = int(values['-gpu_threads-'])
            if values['-use_max_memory-']:
                core.args['max_memory'] = (int(values['-max_memory-'])*1000)
                print('max_memory',core.args['max_memory'])
            # print('args',core.args['gpu_threads'] )
            # # core.start_image_swap(args)
            # core.start_video_swap(args)
            # # swapper.process_img(source_file_path,target_file_path,full_path)
    

            if media_swap == 'video_media':
                sub_dir = "videos"
                full_path = os.path.join(dir_path, sub_dir, f"{out_filename}.mp4")
                core.args['output_file'] = full_path
                # core.start_video_swap(args)
                core.start()
                swaped_file_path = full_path
                window.write_event_value('-VIDEO-SWAPED-',"")   

                # if values['-512_V2-'] == True:
                #     download_thread = threading.Thread(target=swap_video_512_v2 ,args=(source_file_path,target_file_path,"./output/videos/" ,'./temp_results',crop_size,watermark,use_mask,'_224',window), daemon=True)
                #     download_thread.start() 
                #     if download_thread.is_alive():
                #         d_thread = True
                #         print("Swaping")
                #     else:
                #         print("Dead")
                #     # while d_thread:
                #     #     if not download_thread.is_alive():
                #     #         d_thread = False
                #     #         print("File Downloaded")
                # else:
                #     download_thread = threading.Thread(target=swap_video ,args=(source_file_path,target_file_path,"./output/videos/" ,'./temp_results',crop_size,watermark,use_mask,'_224',window), daemon=True)
                #     download_thread.start() 
                #     if download_thread.is_alive():
                #         d_thread = True
                #         print("Swaping")
                #     else:
                #         print("Dead")
                #     # while d_thread:
                #     #     if not download_thread.is_alive():
                #     #         d_thread = False
                #     #         print("File Downloaded")                        

            if media_swap == 'image_media':
                sub_dir = "images"
                full_path = os.path.join(current_dir,dir_path, sub_dir, f"{out_filename}.png")
                print('full_path',full_path)
                core.args['output_file'] = full_path
                # core.start_image_swap(args)
                core.start()
                swaped_file_path = full_path
                window.write_event_value('-IMAGE-SWAPED-',"")   


                # # selected_source_folder,fnames= '',''
                # crop_512_version=get_crop_512_version(values)
                # threading.Thread(target=swap_image_thread, args=(
                #     source_file_path,target_file_path,"./output/images/" , 'imgswp' ,crop_size,watermark,use_mask,window,crop_512_version,source_file_list_with_path,target_file_list_with_path), daemon=True).start() 
                # print('swap swap_image_thread')                 


        #crop abd watermark
        if event == '-watermark_font_size-':
            font_size_display=int(values['-watermark_font_size-'])
            window['-watermark_font_size_display-'].update(value=f'Size: {font_size_display}')

        if event == '-post_process_file_input-':
            watermark_crop_file_input =values['-post_process_file_input-']
            size = get_videofile_info(watermark_crop_file_input)['size']
            video_w = size[0]
            video_h = size[1]

            window['-post_process_file_size_display-'].update(value=f'{video_w} x {video_h}')

            window['-delogo_slider_x-'].update(range=((0,video_w)))
            window['-delogo_slider_y-'].update(range=((0,video_h)))

            window['-crop_slider_x-'].update(range=((0,video_w)))
            window['-crop_slider_y-'].update(range=((0,video_h)))
            

        if event == '-crop_and_put_logo_test-':
            crop_x = values['-crop_input_x-']
            crop_y = values['-crop_input_y-']
            crop_w = values['-crop_input_w-']
            crop_h = values['-crop_input_h-']


            watermark_crop_file_output = os.path.basename(watermark_crop_file_input)            

            if values['-watermark_check-']:
                watermark_test = values['-watermark_text-']
            if values['-watermark_check-']==False:
                watermark_test = ''

            watermark_font_size = int(values['-watermark_font_size-'])
            watermark_font_color = values['-watermark_font_color-']
        
            watermark_output_file = f'watermark_and_crop/{watermark_crop_file_output}'

            watermark_get_position = values['-watermark_positions-']

            if watermark_get_position == 'Top center':
                position = 'x=(w-text_w)/2:y=10'

            if watermark_get_position == 'Bottom center':
                position = 'x=(w-text_w)/2:y=h-th-10'

            if watermark_get_position == 'Centered':
                position = 'x=(w-text_w)/2:y=(h-text_h)/2'

            if watermark_get_position == 'Top left':
                position = 'x=10:y=10'

            if watermark_get_position == 'Top right':
                position = 'x=w-tw-10:y=10'

            if watermark_get_position == 'Bottom left':
                position = 'x=10:y=h-th-10'

            if watermark_get_position == 'Bottom right':
                position = 'x=w-tw-10:y=h-th-10'

            part_1 = f"ffmpeg -y -t 1 -i '{watermark_crop_file_input}' -filter_complex"

            part_2 = f"drawtext=fontfile=fonts/roboto.ttf:text='{watermark_test}'"

            part_3 = f":{position}:fontsize={watermark_font_size}:fontcolor={watermark_font_color}"

            fin = f'"crop=in_w-{crop_w}:in_h-{crop_h}:{crop_x}:{crop_y},{part_2}{part_3}" {watermark_output_file}'

            call_string = f'{part_1} {fin}'

            call = shlex.split(call_string)
            subprocess.call(call)        

            processing_file_name = 'crop_watermark_video_frame'

            window["-crop_and_put_logo-"].update(disabled = False)
            try:
                save_image_from_video_and_show(f'{watermark_output_file}',processing_file_name,window,values,'-OUTPUT_FILE-',(400,400))
                window["-crop_show_image-"].update(disabled = False)
                window["-crop_show_video-"].update(disabled = False)
            except:
                window["-crop_show_image-"].update(disabled = True)
                window["-crop_show_video-"].update(disabled = True)                
                print('Try Onther Size')


        if event == '-crop_and_put_logo-':
            crop_x = values['-crop_input_x-']
            crop_y = values['-crop_input_y-']
            crop_w = values['-crop_input_w-']
            crop_h = values['-crop_input_h-']


            watermark_crop_file_output = os.path.basename(watermark_crop_file_input)            

            if values['-watermark_check-']:
                watermark_test = values['-watermark_text-']
            if values['-watermark_check-']==False:
                watermark_test = ''

            watermark_font_size = int(values['-watermark_font_size-'])
            watermark_font_color = values['-watermark_font_color-']
        
            watermark_output_file = f'watermark_and_crop/{watermark_crop_file_output}'

            watermark_get_position = values['-watermark_positions-']

            if watermark_get_position == 'Top center':
                position = 'x=(w-text_w)/2:y=10'

            if watermark_get_position == 'Bottom center':
                position = 'x=(w-text_w)/2:y=h-th-10'

            if watermark_get_position == 'Centered':
                position = 'x=(w-text_w)/2:y=(h-text_h)/2'

            if watermark_get_position == 'Top left':
                position = 'x=10:y=10'

            if watermark_get_position == 'Top right':
                position = 'x=w-tw-10:y=10'

            if watermark_get_position == 'Bottom left':
                position = 'x=10:y=h-th-10'

            if watermark_get_position == 'Bottom right':
                position = 'x=w-tw-10:y=h-th-10'

            part_1 = f"ffmpeg -y -i '{watermark_crop_file_input}' -filter_complex"

            part_2 = f"drawtext=fontfile=fonts/roboto.ttf:text='{watermark_test}'"

            part_3 = f":{position}:fontsize={watermark_font_size}:fontcolor={watermark_font_color}"

            fin = f'"crop=in_w-{crop_w}:in_h-{crop_h}:{crop_x}:{crop_y},{part_2}{part_3}" {watermark_output_file}'

            call_string = f'{part_1} {fin}'

            call = shlex.split(call_string)
            subprocess.call(call)        

            processing_file_name = 'crop_watermark_video_frame'

            window["-crop_and_put_logo-"].update(disabled = False)
            try:
                save_image_from_video_and_show(f'{watermark_output_file}',processing_file_name,window,values,'-OUTPUT_FILE-',(400,400))
                window["-crop_show_image-"].update(disabled = False)
                window["-crop_show_video-"].update(disabled = False)
            except:
                window["-crop_show_image-"].update(disabled = True)
                window["-crop_show_video-"].update(disabled = True)                
                print('Try Onther Size')

        if event == '-crop_show_video-':
            delogo_file_input=values['-post_process_file_input-']
            delogo_file_output = os.path.basename(delogo_file_input)
            delogo_file = f"watermark_and_crop/{delogo_file_output}"

            print(delogo_file)
            os.popen(os.path.abspath(delogo_file))

        if event == '-crop_show_image-':
            croped_file = f"processing_media/{processing_file_name}.png"
            os.popen(os.path.abspath(croped_file))

        #delogo
        if event == '-delogo_test_go-':

            x=values['-delogo_input_x-']
            y=values['-delogo_input_y-']
            w=values['-delogo_input_w-']
            h=values['-delogo_input_h-']

            show_delogo=values['-show_delogo-']

            delogo_file_input=values['-post_process_file_input-']
            delogo_file_output = os.path.basename(delogo_file_input)

            if show_delogo:
                show_delogo=1
            if show_delogo == False:
                show_delogo=0            

            wm = "drawtext=text='github.com/diStyApps/seait':x=5:y=5:fontsize=60:fontcolor=white"
            window["-delogo_go-"].update(disabled = True)
            #with watermark
            # code = f"ffmpeg -y -i '{delogo_file_input}' -filter_complex delogo=x={x}:y={y}:w={w}:h={h}:show={show_delogo},{wm} delogo/de_{delogo_file_output}"
            code = f"ffmpeg -y -t 1 -i '{delogo_file_input}' -filter_complex delogo=x={x}:y={y}:w={w}:h={h}:show={show_delogo} delogo/de_{delogo_file_output}"
            call = shlex.split(code)
            print('delogo_go',call)
            subprocess.call(call) 
            window["-delogo_go-"].update(disabled = False)
            processing_file_name = 'delogo_video_frame'
            try:
                save_image_from_video_and_show(f'delogo/de_{delogo_file_output}',processing_file_name,window,values,'-OUTPUT_FILE-',(400,400))
                window["-delogo_show_image-"].update(disabled = False)
                window["-delogo_show_video-"].update(disabled = False)
            except:
                window["-delogo_show_image-"].update(disabled = True)
                window["-delogo_show_video-"].update(disabled = True)                
                print('Try Onther Size')

        if event == '-delogo_go-':

            x=values['-delogo_input_x-']
            y=values['-delogo_input_y-']
            w=values['-delogo_input_w-']
            h=values['-delogo_input_h-']

            show_delogo=values['-show_delogo-']

            delogo_file_input=values['-post_process_file_input-']
            delogo_file_output = os.path.basename(delogo_file_input)

            if show_delogo:
                show_delogo=1
            if show_delogo == False:
                show_delogo=0            

            wm = "drawtext=text='github.com/diStyApps/seait':x=5:y=5:fontsize=60:fontcolor=white"
            window["-delogo_go-"].update(disabled = True)
            #with watermark
            # code = f"ffmpeg -y -i '{delogo_file_input}' -filter_complex delogo=x={x}:y={y}:w={w}:h={h}:show={show_delogo},{wm} delogo/de_{delogo_file_output}"
            code = f"ffmpeg -y -i '{delogo_file_input}' -filter_complex delogo=x={x}:y={y}:w={w}:h={h}:show={show_delogo} delogo/de_{delogo_file_output}"
            call = shlex.split(code)
            print('delogo_go',call)
            subprocess.call(call) 
            window["-delogo_go-"].update(disabled = False)
            processing_file_name = 'delogo_video_frame'
            try:
                save_image_from_video_and_show(f'delogo/de_{delogo_file_output}',processing_file_name,window,values,'-OUTPUT_FILE-',(400,400))
                window["-delogo_show_image-"].update(disabled = False)
                window["-delogo_show_video-"].update(disabled = False)
            except:
                window["-delogo_show_image-"].update(disabled = True)
                window["-delogo_show_video-"].update(disabled = True)                
                print('Try Onther Size')

        if event == '-delogo_show_video-':
            delogo_file_input=values['-post_process_file_input-']
            delogo_file_output = os.path.basename(delogo_file_input)
            delogo_file = f"delogo/de_{delogo_file_output}"
            os.popen(os.path.abspath(delogo_file))

        if event == '-delogo_show_image-':
            delogo_file = f"processing_media/{processing_file_name}.png"
            os.popen(os.path.abspath(delogo_file))


        #dowloading
        if event == '-DOWNLOAD_SOURCE_FILE-':
            url_a =values['-select_source_file_input-']
            # verify(target_file_path, source_file_path)
            # print('verify',target_file_path,target_file_path)
            threading.Thread(target=createNewDownloadThread, args=(url_a, 'C:/Users/user/miniconda/deepface/down/',window), daemon=True).start()

        if event == '-FILE_DOWNLOADED-':
            # verify(target_file_path, source_file_path)
            # print('file_down',values['-FILE_DOWNLOADED-'])  
            #     
            # if values['-SHOW_MEDIA-'] == True:
            target_file_path = values['-FILE_DOWNLOADED-']
            image_bio_data = get_img_data(target_file_path,(500,300))
            window["-source_image-"].update(data=image_bio_data)  
        #VERIFY
        if event == '-VERIFY_IDENTITY-':
            if values['-SOURCE_AND_RESUALT_VERIFY-'] == True:
                threading.Thread(target=verify, args=(source_file_path,swaped_file_path,window), daemon=True).start()

            if values['-SOURSE_AND_TARGET_VERIFY-'] == True:
                threading.Thread(target=verify, args=(source_file_path,target_file_path,window), daemon=True).start()
        if event == 'PATREON_BTN_KEY':
            webbrowser.open("https://www.patreon.com/distyx")   

    window.close()

if __name__ == '__main__':
    main()
