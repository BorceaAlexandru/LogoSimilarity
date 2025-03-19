import cv2

def extract(image_path):
    try:
        #incarcare imagine
        img=cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"Could not read image: {image_path}")
            return None, None

        #orb
        orb=cv2.ORB_create()

        #keypoints
        keypoints, descriptors = orb.detectAndCompute(img, None)
        return keypoints, descriptors
    except Exception as e:
        print(f"Error extracting features from {image_path}: {e}")
        return None, None

def compare_features(descriptors1, descriptors2):
    try:
        #initializare
        bf=cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        #potrivire descriptori
        matches=bf.match(descriptors1, descriptors2)

        #sortare dupa distanta
        matches=sorted(matches, key=lambda x: x.distance)

        #nr de potriviri bune
        return len(matches)
    except Exception as e:
        print(f"Error comparing features: {e}")
        return 0