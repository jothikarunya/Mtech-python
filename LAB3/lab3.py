import cv2
import matplotlib.pyplot as plt

image = cv2.imread(
    "4b1b27f75689a236e0881aeb5e5eac83.jpg"
)

if image is None:
    print("Image not found!")
else:
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(10, 10))
    plt.imshow(image_rgb)
    plt.title("Visualization of RGB Image")
    plt.axis("off")
    plt.show()

    #2.Image normalizaton
import cv2
import numpy as np
import matplotlib.pyplot as plt
img = cv2.imread("4b1b27f75689a236e0881aeb5e5eac83.jpg")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
mean = np.mean(img_rgb, axis=(0, 1))
std = np.std(img_rgb, axis=(0, 1))

print("Mean of R, G, B:", mean)
print("Standard deviation of R, G, B:", std)
normalized = (img_rgb - mean) / std
normalized_display = cv2.normalize(
    normalized, None, 0, 255, cv2.NORM_MINMAX
).astype(np.uint8)
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(img_rgb)
plt.title("Original Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(normalized_display)
plt.title("Normalized Image")
plt.axis("off")

plt.show()

#3.to print dimensions of image
import cv2
img = cv2.imread("4b1b27f75689a236e0881aeb5e5eac83.jpg")
height, width, channels = img.shape
total_pixels = height * width
print("Height:", height)
print("Width:", width)
print("Channels:", channels)
print("Data type:", img.dtype)
print("Total pixels:", total_pixels)

#4.visualizing small part of image
import cv2
import matplotlib.pyplot as plt
img = cv2.imread("4b1b27f75689a236e0881aeb5e5eac83.jpg")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
cropped = img_rgb[100:300, 150:350]
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(img_rgb)
plt.title("Original Image")
plt.axis("off")
plt.subplot(1, 2, 2)
plt.imshow(cropped)
plt.title("Cropped Region")
plt.axis("off")
plt.show()

#5.image slicing 
import cv2
import matplotlib.pyplot as plt
img = cv2.imread("4b1b27f75689a236e0881aeb5e5eac83.jpg")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
height, width, channels = img_rgb.shape
mid_h = height // 2
mid_w = width // 2
top_left = img_rgb[:mid_h, :mid_w]
top_right = img_rgb[:mid_h, mid_w:]
bottom_left = img_rgb[mid_h:, :mid_w]
bottom_right = img_rgb[mid_h:, mid_w:]
plt.figure(figsize=(10, 8))
plt.subplot(2, 2, 1)
plt.imshow(top_left)
plt.title("Top Left")
plt.axis("off")
plt.subplot(2, 2, 2)
plt.imshow(top_right)
plt.title("Top Right")
plt.axis("off")
plt.subplot(2, 2, 3)
plt.imshow(bottom_left)
plt.title("Bottom Left")
plt.axis("off")
plt.subplot(2, 2, 4)
plt.imshow(bottom_right)
plt.title("Bottom Right")
plt.axis("off")
plt.tight_layout()
plt.show()
top = cv2.hconcat([top_left, top_right])
bottom = cv2.hconcat([bottom_left, bottom_right])
merged = cv2.vconcat([top, bottom])
plt.figure(figsize=(6, 6))
plt.imshow(merged)
plt.title("Merged Image")
plt.axis("off")
plt.show()

#6. histogram
import cv2
import matplotlib.pyplot as plt
img = cv2.imread("4b1b27f75689a236e0881aeb5e5eac83.jpg")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
red_hist = cv2.calcHist([img_rgb], [0], None, [256], [0, 256])
green_hist = cv2.calcHist([img_rgb], [1], None, [256], [0, 256])
blue_hist = cv2.calcHist([img_rgb], [2], None, [256], [0, 256])
plt.figure(figsize=(10, 6))
plt.plot(red_hist, label="Red")
plt.plot(green_hist, label="Green")
plt.plot(blue_hist, label="Blue")
plt.title("Histogram of Each Color Channel")
plt.xlabel("Pixel Intensity")
plt.ylabel("Frequency")
plt.xlim([0, 256])
plt.legend()
plt.grid()
plt.show()

#7.converting to grayscale
import cv2
import matplotlib.pyplot as plt
img = cv2.imread("4b1b27f75689a236e0881aeb5e5eac83.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(gray, cmap="gray")
plt.title("Grayscale Image")
plt.axis("off")
plt.subplot(1, 2, 2)
plt.plot(hist)
plt.title("Grayscale Image Histogram")
plt.xlabel("Pixel Intensity")
plt.ylabel("Frequency")
plt.xlim([0, 256])
plt.grid()
plt.tight_layout()
plt.show()

#8.
import cv2
import matplotlib.pyplot as plt
img = cv2.imread("4b1b27f75689a236e0881aeb5e5eac83.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
h, w = img.shape[:2]
zoom_in = cv2.resize(img, (w * 2, h * 2), interpolation=cv2.INTER_CUBIC)
zoom_out = cv2.resize(img, (w // 2, h // 2), interpolation=cv2.INTER_AREA)
print("Original:", img.shape)
print("Zoomed in:", zoom_in.shape)
print("Zoomed out:", zoom_out.shape)
plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.imshow(img)
plt.title("Original")
plt.axis("off")
plt.subplot(1, 3, 2)
plt.imshow(zoom_in)
plt.title("Zoomed In (2x)")
plt.axis("off")
plt.subplot(1, 3, 3)
plt.imshow(zoom_out)
plt.title("Zoomed Out (2x)")
plt.axis("off")
plt.tight_layout()
plt.show()

#9.
import cv2
import matplotlib.pyplot as plt
img = cv2.imread("4b1b27f75689a236e0881aeb5e5eac83.jpg")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
pyramid_1 = cv2.pyrDown(img_rgb)
pyramid_2 = cv2.pyrDown(pyramid_1)
pyramid_3 = cv2.pyrDown(pyramid_2)
print("Original image shape :", img_rgb.shape)
print("Pyramid Level 1     :", pyramid_1.shape)
print("Pyramid Level 2     :", pyramid_2.shape)
print("Pyramid Level 3     :", pyramid_3.shape)
plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.imshow(img_rgb)
plt.title("Original Image")
plt.axis("off")
plt.subplot(2, 2, 2)
plt.imshow(pyramid_1)
plt.title("Pyramid Level 1")
plt.axis("off")
plt.subplot(2, 2, 3)
plt.imshow(pyramid_2)
plt.title("Pyramid Level 2")
plt.axis("off")
plt.subplot(2, 2, 4)
plt.imshow(pyramid_3)
plt.title("Pyramid Level 3")
plt.axis("off")
plt.tight_layout()
plt.show()