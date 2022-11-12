import PySimpleGUI as sg
from subprocess import run as run_command
from time import sleep
from playsound import playsound
import sys
from os import path


sg.theme('DarkBlue14')
minutes = [20, 25, 30, 35]

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return path.join(sys._MEIPASS, relative_path)
    return path.join(path.abspath("."), relative_path)

def shutdown(sec: int = 0, comment: str = "null"):
    run_command(["shutdown", "/s", "/t", str(sec), "/c", comment], shell=True)
    return


input_time = [[sg.Combo(list(map(str, minutes)), size=3, font=("meiryo", 15), key="-MIN-"),
               sg.Text("分", font=("meiryo", 14)),
               sg.Input(size=4, font=("meiryo", 15), key="-SEC-",
                        disabled_readonly_background_color="#b9d4f1"),
               sg.Text("秒", font=("meiryo", 14))]]

layout = [
    [sg.Text("時間を指定してください。", font=("meiryo", 14))],
    [sg.Column(input_time, justification="center")],
    [sg.Checkbox("終了後、シャットダウンする", default=True, font=(
        "游ゴシック Medium", 12), key="-SHUTDOWN-")],
    [sg.Checkbox("音を鳴らす", default=True, font=("meiryo", 11), key="-SOUND-")],
    [sg.Button("タイマー開始", font=("游ゴシック bold", 14), key="-START-"),
     sg.Text(text_color="red", key="-ERRORTEXT-")]
]
window = sg.Window("ShutDownTimer", layout, size=(
    390, 230), resizable=True, finalize=True)
started = False
shutdown_count_started = False

while True:
    if started:
        min = int(values["-MIN-"])
        sec = int(values["-SEC-"])

        if min + sec == 0:
            if shutdown_count_started:
                sleep(5)  # イベントループでsleepは使ってはいけない
                shutdown(4, "解除禁止^^")
            elif values["-SHUTDOWN-"]:
                shutdown(124, "2分後にシャットダウンします...")
                playsound(resource_path("timer_end.wav"))
                window["-MIN-"].update(2)
                window["-SEC-"].update(0)
                shutdown_count_started = True
            else:
                window["-MIN-"].update("", disabled=False)
                window["-SEC-"].update("", disabled=False)
                started = False
        elif sec == 0:
            window["-MIN-"].update(min - 1)
            window["-SEC-"].update(59)
        else:
            window["-SEC-"].update(sec - 1)
        event, values = window.read(timeout=1000)
    else:
        event, values = window.read()


    if event == "-START-":
        min_is_int = values["-MIN-"].isdecimal()
        sec_is_int = values["-SEC-"].isdecimal()

        if started or shutdown_count_started:
            pass
        elif not (min_is_int or sec_is_int):
            window["-ERRORTEXT-"].update("何も入力されていないか、\n無効な値が入力されています。")
        else:
            window["-ERRORTEXT-"].update("")
            window["-MIN-"].update(disabled=True)
            window["-SEC-"].update(disabled=True)
            started = True

            # 入力欄の片方に何も入力されていなかったときの処理
            if not min_is_int:
                window["-MIN-"].update("0")
            elif not sec_is_int:
                window["-SEC-"].update("0")
            event, values = window.read(timeout=0)

    if event == sg.WIN_CLOSED:
        break


window.close()
