import cv2
from PIL import Image
import os

def get_image_info(file_path):
    """读取并打印图片的基础信息"""
    if not os.path.exists(file_path):
        print(f"错误：找不到文件 '{file_path}'。")
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
    except Exception:
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
        print("错误：无法读取图片。")
        return
    h, w = img.shape[:2]
    if width is not None and height is None:
        height = int(h * (width / w))
    elif height is not None and width is None:
        width = int(w * (height / h))
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
    if left < 0 or top < 0 or right > w or bottom > h or left >= right or top >= bottom:
        print(f"错误：裁剪区域越界或坐标不合法！图片尺寸为 {w}x{h}。")
        return
    cropped = img[top:bottom, left:right]
    cv2.imwrite(output_path, cropped)
    print(f"成功：图片已裁剪并保存至 {output_path}")

def rotate_image(file_path, output_path, angle):
    """旋转图片（仅支持 90, 180, 270）"""
    if angle not in [90, 180, 270]:
        print("错误：旋转角度仅支持 90, 180 或 270 度。")
        return
    img = cv2.imread(file_path)
    if img is None:
        print("错误：无法读取图片。")
        return
    if angle == 90:
        rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        rotated = cv2.rotate(img, cv2.ROTATE_180)
    elif angle == 270:
        rotated = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imwrite(output_path, rotated)
    print(f"成功：图片已旋转 {angle} 度并保存至 {output_path}")

def flip_image(file_path, output_path, direction="horizontal"):
    """翻转图片"""
    img = cv2.imread(file_path)
    if img is None:
        print("错误：无法读取图片。")
        return
    if direction == "horizontal":
        flipped = cv2.flip(img, 1)
    elif direction == "vertical":
        flipped = cv2.flip(img, 0)
    else:
        print("错误：翻转方向仅支持 'horizontal' 或 'vertical'。")
        return
    cv2.imwrite(output_path, flipped)
    print(f"成功：图片已{direction}翻转并保存至 {output_path}")

def to_grayscale(file_path, output_path):
    """灰度化图片"""
    img = cv2.imread(file_path)
    if img is None:
        print("错误：无法读取图片。")
        return
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(output_path, gray)
    print(f"成功：图片已灰度化并保存至 {output_path}")

def convert_format(file_path, output_path):
    """格式转换（处理了透明 PNG 转 JPG 的情况）"""
    try:
        with Image.open(file_path) as img:
            # 如果是带透明通道的图片(RGBA)，且目标格式是 JPG，需要先转成 RGB
            if img.mode in ("RGBA", "LA") and output_path.lower().endswith(('.jpg', '.jpeg')):
                # 创建一个白色背景
                background = Image.new("RGB", img.size, (255, 255, 255))
                # 将透明图片贴到白色背景上
                background.paste(img, mask=img.split()[3]) 
                background.save(output_path, "JPEG")
            else:
                img.save(output_path)
        print(f"成功：图片格式已转换并保存至 {output_path}")
    except Exception as e:
        print(f"错误：格式转换失败。详细信息: {e}")

if __name__ == "__main__":
    test_image_path = "demo/test.jpg"
    
    print(">>> 1. 测试旋转 (90度)")
    rotate_image(test_image_path, "demo/rotated_90.jpg", 90)
    print("\n>>> 2. 测试旋转参数错误 (45度)")
    rotate_image(test_image_path, "demo/error_rot.jpg", 45)
    
    print("\n>>> 3. 测试水平翻转")
    flip_image(test_image_path, "demo/flipped_h.jpg", "horizontal")
    
    print("\n>>> 4. 测试灰度化")
    to_grayscale(test_image_path, "demo/gray.jpg")
    
    print("\n>>> 5. 测试格式转换 (JPG 转 PNG)")
    convert_format(test_image_path, "demo/converted.png")
    
    print("\n>>> 6. 测试透明通道处理 (先创建一个透明PNG，再转JPG)")
    # 程序化生成一个带透明度的 PNG 用于测试
    transparent_png = "demo/transparent.png"
    img = Image.new("RGBA", (100, 100), (255, 0, 0, 128)) # 半透明红色
    img.save(transparent_png)
    convert_format(transparent_png, "demo/transparent_to_jpg.jpg")
