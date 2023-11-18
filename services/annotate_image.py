from schemas.detection import Detection
import io
from mediapipe.framework.formats import landmark_pb2
from mediapipe import solutions
import cv2
import numpy as np
from PIL import Image

class AnnotateImage:
    def annotate(self,img_array: np.ndarray, detection:Detection) -> io.BytesIO:
        annotate_image = img_array.copy()
        for idx,hand in enumerate(detection.landmarks):
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(
                    x=landmark[0], y=landmark[1], z=landmark[2]
                )
                for landmark in hand
            ])
            solutions.drawing_utils.draw_landmarks(
                annotate_image,
                hand_landmarks_proto,
                solutions.hands.HAND_CONNECTIONS,
                solutions.drawing_styles.get_default_hand_landmarks_style(),
                solutions.drawing_styles.get_default_hand_connections_style()
            )
            cv2.putText(annotate_image, f"{detection.labels[idx]}", tuple(detection.bbox[idx]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(annotate_image, f"{round((detection.scores[idx]*100),2)}%", (int(detection.bbox[idx][0]), int(detection.bbox[idx][1]) + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        img_pil = Image.fromarray(annotate_image)
        image_stream = io.BytesIO()
        img_pil.save(image_stream, format="JPEG")
        image_stream.seek(0)
        return image_stream