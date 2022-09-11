
import time
from pynput.keyboard import Controller,Key,Listener

start_time = time.time()

def on_press(key):
    try:
        log = "%s按压:"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))),format(key.char)
        write_log('\n'+str(log))
    except AttributeError:
        log = "%s按压:"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))),format(key)
        write_log('\n'+str(log))

# 监听释放
def on_release(key):
    global start_time
    log = "%s释放:"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))),format(key) 
    write_log('\n'+str(log))
    end_time = time.time()

    if end_time - start_time > 10 : 
        return False


def start_listen():
    with Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()


def write_log(log):
    filename = './log.txt'
    with open(filename, 'a') as file_object:
        file_object.write(log)


start_listen()