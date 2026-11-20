import os
from dotenv import load_dotenv
import cv2
from inference_sdk import InferenceHTTPClient

load_dotenv()

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=os.getenv("ROBOFLOW_API_KEY")
)
print("api key", os.getenv("ROBOFLOW_API_KEY"))
image_path = "data/kaggle/Training/meningioma/Tr-me_0037.jpg"

result = CLIENT.infer(
    inference_input=image_path,
    model_id="brain-tumor-detection-1zpnr/1"
)

print(result)

image = cv2.imread(image_path)
img_height, img_width, _ = image.shape

for pred in result["predictions"]:
    x, y, w, h = int(pred["x"]), int(pred["y"]), int(pred["width"]), int(pred["height"])
    confidence = pred["confidence"]

    # Convert confidence to percentage (e.g., 48%)
    confidence_text = f"{int(confidence * 100)}%"

    # Define colors
    color = (0, 255, 0)  # Green
    text_color = (0, 0, 255)  # Red

    # Draw rectangle
    cv2.rectangle(image, (x - w // 2, y - h // 2), (x + w // 2, y + h // 2), color, 2)

    # Add text label with padding/margin
    text = f"{pred['class']} {confidence_text}"
    font_scale = 0.7
    thickness = 2

    # Get text size
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
    text_x, text_y = x - w // 2, y - h // 2 - 10  # Shift text slightly above the box

    # Ensure text is inside image
    text_y = max(text_y, text_size[1] + 5)  # Add top padding

    # Draw background for text
    cv2.rectangle(image, (text_x, text_y - text_size[1] - 5), (text_x + text_size[0] + 5, text_y + 5), color, -1)

    # Put text on image
    cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, thickness)

# Show the image
cv2.imshow("Detection Result", image)
while True:
    key = cv2.waitKey(1)  # Check for key press every 1 ms
    if key == 27:  # ESC key (keycode 27)
        break
cv2.destroyAllWindows()
