import mysql.connector
import numpy as np
from ultralytics import YOLO
from PIL import Image
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.preprocessing import image
from keras.models import Model
from sklearn.metrics.pairwise import cosine_similarity
import os
import shutil
import cv2

yolo_model_path ='runs/detect/train2/weights/best.pt'
destination_path = 'runs/find/'
origin_path = 'data/cropped/'
LIMIT = 100


def delete_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"The folder {folder_path} has been deleted.")
    else:
        print(f"The folder {folder_path} does not exist.")

def clean_destination():
    delete_folder(destination_path)
    creer_fichiers(destination_path)

def creer_fichiers(chemin_fichier):
    '''Créer les dossier et fichiers nécessaires pour le fichier txt ou les images
    chemin_fichier : str'''

    dossier = os.path.dirname(chemin_fichier)
    if not os.path.exists(dossier):
        os.makedirs(dossier)

def create_connection_bdd():
    cnx = mysql.connector.connect(user='root', password='TO52',
                                  host='localhost',
                                  database='clothes_detection')
    return cnx


def construct_query(cat, brand, size):
    query = "SELECT absolute_path FROM clothes NATURAL JOIN category cat "
    where_category = f"WHERE cat.id_category = {cat} "
    where_brand = ""
    where_size = ""
    first = True

    if brand != 'all':
        query = query + "NATURAL JOIN brand "
        for bd in brand:
            if first:
                where_brand = f"AND (brand = '{bd}' "
                first = False
            else:
                where_brand = where_brand + f"OR brand = '{bd}' "
        if len(brand) > 0:
            where_brand = where_brand + ") "

    first = True
    if size != 'all':
        query = query + "NATURAL JOIN size "
        for sz in size:
            if first:
                where_size = f"AND (size = '{sz}' "
                first = False
            else:
                where_size = where_size + f"OR size = '{sz}' "
        if len(size) > 0:
            where_size = where_size + ") "

    query = query + where_category + where_brand + where_size + "LIMIT " + str(LIMIT)

    return query


def get_sizes_bdd():
    cnx = create_connection_bdd()
    cursor = cnx.cursor()
    cursor.execute("SELECT DISTINCT size FROM size")
    sizes = cursor.fetchall()
    sizes = [size[0] for size in sizes]
    cnx.close()
    return sizes

def get_brands_bdd():
    cnx = create_connection_bdd()
    cursor = cnx.cursor()
    cursor.execute("SELECT DISTINCT brand FROM brand")
    brands = cursor.fetchall()
    brands = [brand[0] for brand in brands]
    cnx.close()
    return brands

def get_images_bdd(cat, brand, size):
    cnx = create_connection_bdd()
    cursor = cnx.cursor()
    query = construct_query(cat, brand, size)
    print(query)
    cursor.execute(query)
    paths = cursor.fetchall()
    paths = [path[0] for path in paths]
    correct_paths = [origin_path + path for path in paths]
    cnx.close()
    return correct_paths

def get_category_bdd(cat):
    cnx = create_connection_bdd()
    cursor = cnx.cursor()
    cursor.execute("SELECT category FROM category WHERE id_category = " + str(cat))
    category = cursor.fetchall()
    cnx.close()
    return category[0][0]

def predict_category(image_path):
    cat, bbox = None, None
    model = YOLO(yolo_model_path)
    results = model.predict(source=image_path, save=True)
    for result in results:
        classe = result.boxes.cls  # class, (N, )
        bounding_box = result.boxes.xyxy[0]
        bbox = bounding_box.tolist()
        cat = int(classe.item())
    return cat, bbox

def crop_image(image_path, bbox):
    chemin_depart = image_path
    chemin_arrivee = destination_path + 'cropped_image.jpg'
    im = np.array(Image.open(chemin_depart))
    im_trim = im[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])] #y1:y2, x1:x2
    Image.fromarray(im_trim).save(chemin_arrivee)
    return chemin_arrivee


def extract_features(img_path, model):
    # Extraction des caractéristiques avec VGG16
    img = image.load_img(img_path, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    vgg16_feature = model.predict(img_data)

    # Extraction de l'histogramme de couleurs
    img_bgr = cv2.imread(img_path)
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    hist_h = cv2.calcHist([img_hsv], [0], None, [50], [0, 256])
    hist_s = cv2.calcHist([img_hsv], [1], None, [60], [0, 256])
    hist_v = cv2.calcHist([img_hsv], [2], None, [60], [0, 256])
    hist_h = cv2.normalize(hist_h, hist_h).flatten()
    hist_s = cv2.normalize(hist_s, hist_s).flatten()
    hist_v = cv2.normalize(hist_v, hist_v).flatten()
    color_hist = np.concatenate((hist_h, hist_s, hist_v))

    return vgg16_feature, color_hist

def get_similar_images(paths, goal, limite):
    similarities = [0 for i in range(len(paths))]
    i = 0
    base_model = VGG16(weights='imagenet')
    model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
    new_image_features, new_image_color_hist = extract_features(goal, model)
    for path in paths:
        feature, color_hist = extract_features(path, model)
        similarity_features = cosine_similarity(new_image_features, feature).tolist()[0][0]
        similarity_color = cv2.compareHist(new_image_color_hist, color_hist, cv2.HISTCMP_CORREL)
        combined_similarity = (similarity_features + similarity_color) / 2
        combined_similarity = round(combined_similarity, 4)
        print(f"Similarité combinée : {combined_similarity}")
        similarities[i] = combined_similarity
        name = str(combined_similarity).replace("0.", "")
        shutil.copy2(path, "./runs/find/" + name + '.jpg')
        i += 1
    indices = np.argsort(similarities)[::-1][:limite]
    new_paths = [[paths[i], similarities[i]] for i in indices]
    return new_paths