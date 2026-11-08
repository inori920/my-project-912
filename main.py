import cv2
from PIL import Image
import os

def get_image_info(file_path):
    """
    读取并打印图片的基础信息
    """
    # 1. 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误：找不到文件 '{file_path}'，请检查路径是否正确。")
        return

    try:
        # 2. 获取文件大小 (转换为 KB 或 MB，保留 2 位小数)
        file_size_bytes = os.path.getsize(file_path)
        if file_size_bytes < 1024 * 1024:
            file_size_str = f"{file_size_bytes / 1024:.2f} KB"
        else:
            file_size_str = f"{file_size_bytes / (1024 * 1024):.2f} MB"

        # 3. 获取文件名和格式
        file_name = os.path.basename(file_path)
        
        # 4. 使用 PIL 获取颜色模式和尺寸
        with Image.open(file_path) as img:
            width, height = img.size
            img_format = img.format
            mode = img.mode  # RGB, RGBA, L (灰度) 等

        # 5. 打印信息
        print("=" * 30)
        print(f"文件名:   {file_name}")
        print(f"图片格式: {img_format}")
        print(f"尺寸:     {width} x {height} 像素")
        print(f"颜色模式: {mode}")
        print(f"文件大小: {file_size_str}")
        print("=" * 30)

    except Exception as e:
        # 捕获不是有效图片的情况
        print(f"错误：无法读取文件 '{file_path}'，它可能不是有效的图片。")
        print(f"详细信息: {e}")

if __name__ == "__main__":
    # 测试运行
    test_image_path = "demo/test.jpg"
    print(f"正在读取图片: {test_image_path}")
    get_image_info(test_image_path)
