import cv2
from skimage import metrics

# Set the paths to the two video files
video1_path = r'Z:\mp4\P-1425-66940.mp4'
video2_path = r'Z:\mp4\P-1425-66937.mp4'

# Open the video files
video1 = cv2.VideoCapture(video1_path)
video2 = cv2.VideoCapture(video2_path)

# Initialize variables for storing frame differences
ssim_scores = []
mse_scores = []

# Process frames from both videos
while True:
    # Read frames from both videos
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()

    # Check for the end of either video
    if not ret1 or not ret2:
        break

    # Convert frames to grayscale
    frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Calculate SSIM (Structural Similarity Index) between frames
    ssim = metrics.structural_similarity(frame1_gray, frame2_gray)

    # Calculate MSE (Mean Squared Error) between frames
    mse = ((frame1_gray - frame2_gray) ** 2).mean()

    # Store the scores
    ssim_scores.append(ssim)
    mse_scores.append(mse)

# Calculate the average SSIM and MSE scores
average_ssim = sum(ssim_scores) / len(ssim_scores)
average_mse = sum(mse_scores) / len(mse_scores)

# Output the results
print(f"Average SSIM Score: {average_ssim}")
print(f"Average MSE Score: {average_mse}")

# Release video captures
video1.release()
video2.release()
