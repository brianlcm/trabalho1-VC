import cv2
import numpy as np

# Funcao que utiliza o descritor ORB para calcular os pontos de interesse e computar os descritores
def ORB_descriptor(img1_gray, img2_gray):

    # Chama a funcao para criar objeto ORB a partir do OpenCV
    orb = cv2.ORB_create()

    # Detecta e computa os pontos de interesse e descritores em cada imagem
    img1_keypoints, img1_descriptors = orb.detectAndCompute(img1_gray, None)
    img2_keypoints, img2_descriptors = orb.detectAndCompute(img2_gray, None)

    return img1_keypoints, img1_descriptors, img2_keypoints, img2_descriptors

# Funcao que utiliza o descritor SIFT para calcular os pontos de interesse e computar os descritores
def SIFT_descriptor(img1_gray, img2_gray):

    # Chama a funcao para criar objeto ORB a partir do OpenCV
    sift = cv2.SIFT_create()

    # Detecta e computa os pontos de interesse e descritores em cada imagem
    img1_keypoints, img1_descriptors = sift.detectAndCompute(img1_gray, None)
    img2_keypoints, img2_descriptors = sift.detectAndCompute(img2_gray, None)

    return img1_keypoints, img1_descriptors, img2_keypoints, img2_descriptors

def run_matching_images(img1, img2, pair_imgs):

    # Converte as imagens para escala de cinza
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Chama funcao para detectar e computar os pontos de interesse e descritores em cada imagem (ORB ou SIFT)
    img1_keypoints, img1_descriptors, img2_keypoints, img2_descriptors = ORB_descriptor(img1_gray, img2_gray)

    # Salva as imagens com os pontos de interesse
    cv2.imwrite('results\\pair_images_{}\\keypoints_img1.png'.format(pair_imgs),
                cv2.drawKeypoints(img1, img1_keypoints, img1))
    cv2.imwrite('results\\pair_images_{}\\keypoints_img2.png'.format(pair_imgs),
                cv2.drawKeypoints(img2, img2_keypoints, img2))
    
    # Chama a funcao BFMatcher do OpenCV para forcar a matching entre as duas imagens 
    matcher = cv2.BFMatcher(cv2.NORM_L2, True)
    matches = matcher.match(img1_descriptors,img2_descriptors)

    # Cria array com o mapeamento dos pontos de correspondencia encontrados entre as duas imagens
    pointsMap = np.array([
            [img1_keypoints[match.queryIdx].pt[0],
            img1_keypoints[match.queryIdx].pt[1],
            img2_keypoints[match.trainIdx].pt[0],
            img2_keypoints[match.trainIdx].pt[1]] for match in matches
        ])

    # Salva a imagens com todos os pontos de correspondencia
    matched_image = cv2.drawMatches(img1, img1_keypoints, img2, img2_keypoints, matches, None, flags=2)
    cv2.imwrite('results\\pair_images_{}\\matches_BFMatcher.png'.format(pair_imgs), matched_image)

    return pointsMap