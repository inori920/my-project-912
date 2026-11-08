import cv2
from PIL import Image
import os

def get_image_info(file_path):
    """读取并打印图片的基础信息"""
    if not os.path.exists(file_path):
        print(f"错误：找不到文件 '{file_path}'，请检查路径是否正确。")
        return

    try:
        file_size_bytes = os.path.getsize(file_path)
        if file_size_bytes < 1024 * 1024:
            file_size_str = f"{file_size_bytes / 1024:.2f} KB"
        else:
            file_size_str = f"{file_size_bytes / (1024 * 1024):.2f} MB"

        file_name = os.path.basename(file_path)
        
        with Image.open(file_path) as img:
            width, height = img.size
            img_format = img.format
            mode = img.mode

        print("=" * 30)
        print(f"文件名:   {file_name}")
        print(f"图片格式: {img_format}")
        print(f"尺寸:     {width} x {height} 像素")
        print(f"颜色模式: {mode}")
        print(f"文件大小: {file_size_str}")
        print("=" * 30)

    except Exception as e:
        print(f"错误：无法读取文件 '{file_path}'，它可能不是有效的图片。")

def resize_image(file_path, output_path, width=None, height=None):
    """缩放图片"""
    if not os.path.exists(file_path):
        print(f"错误：找不到文件 '{file_path}'。")
        return

    if (width is not None and width <= 0) or (height is not None and height <= 0):
        print("错误：指定的宽度和高度必须大于 0。")
        return

    img = cv2.imread(file_path)
    if img is None:
        print("错误：无法读取图片，请检查文件是否损坏或格式不支持。")
        return

    # 只给宽或高时，按比例缩放
    h, w = img.shape[:2]
    if width is not None and height is None:
        height = int(h * (width / w))
    elif height is not None and width is None:
        width = int(w * (height / h))

    # 进行缩放
    resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    cv2.imwrite(output_path, resized)
    print(f"成功：图片已缩放并保存至 {output_path}")

def crop_image(file_path, output_path, left, top, right, bottom):
    """裁剪图片"""
    if not os.path.exists(file_path):
        print(f"错误：找不到文件 '{file_path}'。")
        return

    img = cv2.imread(file_path)
    if img is None:
        print("错误：无法读取图片。")
        return

    h, w = img.shape[:2]
    # 检查越界
    if left < 0 or top < 0 or right > w or bottom > h or left >= right or top >= bottom:
        print(f"错误：裁剪区域越界或坐标不合法！图片尺寸为 {w}x{h}。")
        return

    # OpenCV 裁剪是使用数组切片 img[y:y+h, x:x+w]
    cropped = img[top:bottom, left:right]
    cv2.imwrite(output_path, cropped)
    print(f"成功：图片已裁剪并保存至 {output_path}")

if __name__ == "__main__":
    test_image_path = "demo/test.jpg"
    
    print(">>> 1. 测试读取图片信息")
    get_image_info(test_image_path)
    
    print("\n>>> 2. 测试缩放图片 (只给宽度 100，自动算高度)")
    resize_image(test_image_path, "demo/resized_100w.jpg", width=100)
    
    print("\n>>> 3. 测试缩放图片 (宽 150，高 150)")
    resize_image(test_image_path, "demo/resized_square.jpg", width=150, height=150)
    
    print("\n>>> 4. 测试参数错误 (宽度设为 -10)")
    resize_image(test_image_path, "demo/error_test.jpg", width=-10)
    
    print("\n>>> 5. 测试裁剪图片 (左:10, 上:10, 右:100, 下:100)")
    crop_image(test_image_path, "demo/cropped.jpg", 10, 10, 100, 100)
    
    print("\n>>> 6. 测试裁剪越界")
    crop_image(test_image_path, "demo/crop_error.jpg", 0, 0, 5000, 5000)
