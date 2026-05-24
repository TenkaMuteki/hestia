import cv2
from ultralytics import YOLO

def main():
    # 1. Load the YOLO model (nano version 'n' is best for real-time webcam FPS)
    # The framework automatically downloads the weights on the first run
    model = YOLO("yolov8n.pt")

    # 2. Initialize webcam (0 is usually the default built-in camera)
    cap = cv2.VideoCapture(0)
    
    # Optional: Set explicit resolution for better performance or clarity
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run inference filtered to people
        results = model(frame, stream=True, classes=[0])

        for r in results:
            # 1. Get the total count of detections for this frame
            person_count = len(r.boxes)
            
            # 2. Render the bounding boxes
            annotated_frame = r.plot()
            
            # 3. Overlay the counter text onto the image
            cv2.putText(
                annotated_frame, 
                f"People Count: {person_count}", 
                (20, 50),                   # Coordinates (X, Y) top-left corner
                cv2.FONT_HERSHEY_SIMPLEX,   # Font style
                1.0,                        # Font scale (size)
                (0, 255, 0),                # Text color in BGR (Green)
                2,                          # Line thickness
                cv2.LINE_AA                 # Anti-aliased line (smoother text)
            )

        # Display the frame with the text overlay
        cv2.imshow("YOLOv8 Webcam - Counting", annotated_frame)
        
        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()