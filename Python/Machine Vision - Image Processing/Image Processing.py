# Import libraries
import cv2 
import numpy as np

# Initialize a variable for counting no. of objects
numCoins = 0

# Load image 
image = cv2.imread('Coin Image.jpg')

# Convert image into grayscale
grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Grey Scale", grey)
cv2.waitKey(0)

# Apply filter on the greyscale image
blur = cv2.GaussianBlur(grey, (15, 15), 0)
cv2.imshow("Blurred", blur)
cv2.waitKey(0)

# Apply dilation on the blurred image
kernel = np.ones((5, 5), np.uint8)
dilation = cv2.dilate(blur, kernel, iterations=1)
cv2.imshow("Dilated", dilation)
cv2.waitKey(0)

# Detect edge from the dilated image
edges = cv2.Canny(dilation, 30, 150)
cv2.imshow("Edge Detect", edges)
cv2.waitKey(0)

# Find the contours of the image
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a dictionary to group the coin by their size
coinsBySize = {}

# Loop through the contours
for contour in contours:
    # Get the area of the contour
    area = cv2.contourArea(contour)

    # Filter noises
    if area <= 50:
        continue
    # Group the contours by size
    if area <= 100:
        if 'small' not in coinsBySize:
            coinsBySize['small'] = []
        coinsBySize['small'].append(contour)
    elif area <= 1000:
        if 'medium' not in coinsBySize:
            coinsBySize['medium'] = []
        coinsBySize['medium'].append(contour)
    else:
        if 'large' not in coinsBySize:
            coinsBySize['large'] = []
        coinsBySize['large'].append(contour)

# Print the number of coins in each group by looping the dictionary
for size, coins in coinsBySize.items():
    print(f'Number of {size} coins: {len(coins)}')
    numCoins += len(coins)
    
# Draw the contours with green line on the image    
for size, coins in coinsBySize.items():
    for coin in coins:
        cv2.drawContours(image, [coin], -1, (0, 255, 0), 2)


# Display the image
cv2.imshow(f"There are {numCoins} objects.", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Alternative code
""" 
import cv2
import numpy as np

def detect_coins(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
    
    # Apply Dilation
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(blurred, kernel, iterations=1)

    # Apply Canny edge detection
    edges = cv2.Canny(dilation, 30, 150)

    # Find contours of the coins
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize a list to store the detected coins
    coins = []

    # Loop over the contours
    for contour in contours:
        # Calculate the area of the contour
        area = cv2.contourArea(contour)

        # If the area is below a certain threshold, skip it (to remove noise)
        if area < 50:
            continue

        # Calculate the perimeter of the contour
        perimeter = cv2.arcLength(contour, True)

        # Approximate the contour to a polygon
        approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)

        # Calculate the number of vertices of the polygon
        vertices = len(approx)

        # Determine the size of the coin based on the number of vertices
        if vertices <= 15:
            size = "Small"
        elif vertices <= 16:
            size = "Medium"
        else:
            size = "Large"

        # Add the coin to the list
        coins.append((contour, size))

    # Draw the contours on the original image
    cv2.drawContours(image, [contour for contour, _ in coins], -1, (0, 255, 0), 2)

    # Display the image
    cv2.imshow("Coins", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Return the detected coins grouped by size
    return coins

# Path to the image
image_path = "/path/to/your/image.jpg"

# Detect coins and group them by size
detected_coins = detect_coins("Coin Image.jpg")

# Print the number of coins and their sizes
print("Number of coins:", len(detected_coins))
for i, (contour, size) in enumerate(detected_coins):
    print("Coin", i+1, "Size:", size)

"""