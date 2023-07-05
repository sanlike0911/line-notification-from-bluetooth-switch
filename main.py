import evdev
import requests
import time
import configparser

# global variables: line notification settings 
glbLineNotifyToken = ""
glbLineNotifyUrl = ""

def initialize():
    global glbLineNotifyToken
    global glbLineNotifyUrl

    result = False
    try:
        # get line notify settings
        iniFile = configparser.ConfigParser()
        iniFile.read('config.ini', encoding='utf-8')
        config = iniFile['lineNotify']

        # set line notification settings 
        glbLineNotifyToken = config.get('token')
        glbLineNotifyUrl = config.get('url')

        print(glbLineNotifyToken)
        print(glbLineNotifyUrl)

        result = True
    except Exception as e:
        print("Faild to load config file:", e)

    return result

def main():
    result = initialize()
    if result:
        while True:
            try:
                device = evdev.InputDevice('/dev/input/event2')
                print(device)

                pressed = set()
                keyHoldTime = {}
                threshold = 1.0  # 長押しの閾値（1秒）を設定

                for event in device.read_loop():
                    if event.type == evdev.ecodes.EV_KEY:
                        keyEvent = evdev.ecodes.KEY[event.code]
                        if event.value == 1:  # キーが押された場合
                            pressed.add(keyEvent)
                            keyHoldTime[keyEvent] = time.time()
                            # print("キーが押されました:", keyEvent)
                        elif event.value == 0:  # キーが離された場合
                            if keyEvent in pressed:
                                pressed.remove(keyEvent)
                                holdTime = time.time() - keyHoldTime[keyEvent]
                                # print("キーが離されました:", keyEvent)
                                if holdTime >= threshold:
                                    # print("キーが長押しされました:", keyEvent)
                                    sendLineNotify("至急ヘルプを求めます！！ じぃじぃより")
                                if len(pressed) == 0:
                                    break
            except Exception:
                print('Retry...')
                time.sleep(1)

def sendLineNotify(message):
    global glbLineNotifyToken
    global glbLineNotifyUrl
    headers = {'Authorization': f'Bearer {glbLineNotifyToken}'}
    data = {'message': f'message: {message}'}
    requests.post(glbLineNotifyUrl, headers = headers, data = data)

if __name__ == "__main__":
    main()