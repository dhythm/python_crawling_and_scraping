import sys
import os

import cv2

try:
    cascade_path = sys.argv[1]
except IndexError:
    print('Usage: python extract_faces.py CASCADE_PATH IMAGE_PATH...', file=sys.stderr)
    exit(1)

# 出力先ディレクトリが存在しない場合は作成
output_dir = 'faces'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 特徴量ファイルが存在することを確認
classifier = cv2.CascadeClassifier(cascade_path)

for image_path in sys.argv[2:]:
    print('Processing', image_path, file=sys.stderr)

    # 画像ファイルの読込
    image = cv2.imread(image_path)
    # 処理高速化のため、グレースケールに変換
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 顔を検出
    faces = classifier.detectMultiScale(gray_image)

    # 拡張子以外のファイル名を取得
    image_name = os.path.splitext(os.path.basename(image_path))[0]

    for i, (x, y, w, h) in enumerate(faces):
        face_image = image[y:y + h, x: x + w]
        output_path = os.path.join(output_dir, '{0}_{1}.jpg'.format(image_name, i))
        cv2.imwrite(output_path, face_image)
