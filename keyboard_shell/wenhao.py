import win32api,win32con
import time

def get_new_mouse():
    coordinate=win32api.GetCursorPos()
    wide=coordinate[0]-30
    high=coordinate[1]
    new_coordinate=[]
    new_coordinate.append(wide)
    new_coordinate.append(high)
    new_coordinate=tuple(new_coordinate)
    return new_coordinate

def mouse_down():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

def mouse_up():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

key_map = {
    "0": 49, "1": 50, "2": 51, "3": 52, "4": 53, "5": 54, "6": 55, "7": 56, "8": 57, "9": 58,
    "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
    "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
    "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90
}

def key_down(key):
    key = key.upper()
    vk_code = key_map[key]
    win32api.keybd_event(vk_code,win32api.MapVirtualKey(vk_code,0),0,0)

def key_up(key):
    key = key.upper()
    vk_code = key_map[key]
    win32api.keybd_event(vk_code, win32api.MapVirtualKey(vk_code, 0), win32con.KEYEVENTF_KEYUP, 0)
 
 
def key_press(key):
    key_down(key)
    time.sleep(0.02)
    key_up(key)

def wenhao():
    key_press('g')
    time.sleep(0.02)
    mouse_down()
    time.sleep(0.02)
    new_place=get_new_mouse()
    win32api.SetCursorPos(new_place)
    time.sleep(0.02)
    mouse_up()

if __name__ == '__main__':
    time.sleep(6)
    for i in range(0,10):
        wenhao()
        time.sleep(0.5)
    print('done')
    exit()



