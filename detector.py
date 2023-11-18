import numpy as np
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2
from config import get_settings
from schemas.detection import Detection

SETTINGS = get_settings()


MARGIN = 10


class HandsDetector:
    def __init__(self) -> None:
        base_options = python.BaseOptions(model_asset_path=SETTINGS.model_version)
        options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
        self.model = vision.HandLandmarker.create_from_options(options=options)

    def detect_image(self, image_array:np.ndarray) -> Detection:

        height, width, _ = image_array.shape

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_array)
        detection_result = self.model.detect(mp_image)
        hand_landmarks_list = detection_result.hand_landmarks
        hand_landmarks_list_normalized = [[[landmark.x, landmark.y, landmark.z] for landmark in hand] for hand in hand_landmarks_list]

        label_list = detection_result.handedness
        label_names = [category[0].display_name for category in label_list]
        


        x_coordinates = [[landmark[0] for landmark in hand] for hand in hand_landmarks_list_normalized]
        y_coordinates = [[landmark[1] for landmark in hand] for hand in hand_landmarks_list_normalized]

        x_bbox = [int(min(hand) * width) for hand in x_coordinates]
        y_bbox = [int(min(hand) * height) - MARGIN for hand in y_coordinates]

        bbox = [[x, y] for x, y in zip(x_bbox, y_bbox)]
    
        detection = Detection(landmarks=hand_landmarks_list_normalized, labels=label_names, bbox=bbox)
        return detection
           

if __name__ == "__main__":
    image_file = "person.jpg"
    img = cv2.cvtColor(cv2.imread(image_file), cv2.COLOR_BGR2RGB)
    detector = HandsDetector()
    detector.detect_image(img)