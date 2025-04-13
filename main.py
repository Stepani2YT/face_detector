
import cv2
from datetime import date

open('access.log', 'w').write('')
open('access.log', 'w').close()

def face_capture(video, minNeighbors=4, cascade_file_path='default.xml', camera_index=0):
    cascade_path = f'filters/{cascade_file_path}'

    clf = cv2.CascadeClassifier(cascade_path)

    camera = cv2.VideoCapture(camera_index)

    if not camera.isOpened():
        if video == False:
            print("Ошибка: Не удалось открыть камеру.")
            return 
        elif video == True:
            print('Ошибка: Не удалось найти файл.')
            return 

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Ошибка: Не удалось получить кадр.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = clf.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=minNeighbors,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if len(faces) > 0:
            with open('access.log', 'a', encoding='UTF-8') as file:
                file.write(f'{date.today()} Обнаружено {len(faces)} лиц(o).\n')
                file.close()
            print(f'Обнаружено {len(faces)} лиц(o).')
        elif len(faces) == 0:
            with open('access.log', 'a', encoding='UTF-8') as file:
                file.write(f'{date.today()} Ничего не обноружено!!!\n')
            print('Ничего не обноружено!!!')

        for (x, y, width, height) in faces:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 2)
        
        cv2.imshow('Faces', frame)

        if cv2.waitKey(1) == ord('e'):
            break

    camera.release()
    cv2.destroyAllWindows()

def main():
    model = input('Введите имя модели: ')
    from os import path
    if path.exists(f'filters/{model}.xml'):
        pass
    else:
        print('Модель не обноружена!!!')
        input()
        exit(0)
    print('1 - video 2 - camera')
    mode = input('Введите режим: ')
    if mode == '1':
        video_file_name = input('Введите имя файла: ')
        face_capture(camera_index=video_file_name, video=True, cascade_file_path=f'{model}.xml')
    elif mode == '2':
        index = int(input('Введите индекс камеры: '))
        face_capture(camera_index=index, video=False, cascade_file_path=f'{model}.xml')

if __name__ == '__main__':
    main()