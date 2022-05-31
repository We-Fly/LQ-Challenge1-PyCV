import cv2
import imutils
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from cv2 import imread


def getCntShapeName(cnt) -> str:
    # https://www.jianshu.com/p/2731f42882f4
    # 初始化图片名称与大概的形状
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)

    if len(approx) == 3:
        shapeName = "Triangle"

    # 如果形状有 4 个顶点，则它是正方形或矩形
    elif len(approx) == 4:
        # 计算轮廓的边界框并使用边界框计算纵横比
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)

        # 正方形将具有大约等于 1 的纵横比，否则，形状为矩形
        shapeName = "Rectangle" if 0.95 <= ar <= 1.05 else "Rectangle"

    # 如果形状是五边形，它将有 5 个顶点
    elif len(approx) == 5:
        shapeName = "五边形"

    # 否则，我们假设形状是圆形
    else:
        shapeName = "Circle"

    # 返回形状的名称
    return shapeName


def getCntShapeColor(cnt, img) -> str:
    M = cv2.moments(cnt)
    cX = int(M["m10"] / (M["m00"] + 1))
    cY = int(M["m01"] / (M["m00"] + 1))
    (b, g, r) = img[cY][cX]

    if r > (g + b):
        color = "RED"
    elif g > (r + b):
        color = "GREEN"
    elif b > (r + g):
        color = "BLUE"
    else:
        color = "NULL"
    return color


def putChineseText(img, text, position=(100, 100), textColor=(0, 255, 0), textSize=20) -> np.ndarray:
    if isinstance(img, np.ndarray):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "src/shapedetect/AR-PL-Ukai.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text(position, text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


class Picture:  # 针对图片的操作

    def __init__(self, path_to_img) -> None:  # 初始化函数，要实例化一个新的对象需要输入文件路径
        self.resized = None
        self.cnts = None
        self.ratio = 1
        self.raw = None
        if isinstance(path_to_img, str):
            self.raw = imread(path_to_img, cv2.IMREAD_COLOR)
        elif isinstance(path_to_img, np.ndarray):  # 判断是否OpenCV图片类型
            self.raw = path_to_img
        self.modify = self.raw

    def putText(self, string_to_write,  # 要放的字
                put_where=(100, 100),  # 坐标
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,  # 字体
                fontScale=1,  # 大小
                color=(255, 0, 0),  # 颜色
                thickness=2,  # 粗细
                lineType=cv2.LINE_AA  # 线型
                ) -> None:  # 实现 放一个文字，至少需要输入一个string
        self.modify = cv2.putText(self.raw, string_to_write, put_where, fontFace, fontScale, color, thickness, lineType)

    def show(self) -> None:  # 实现 展示图片
        cv2.imshow("image", self.modify)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def resize(self, width) -> None:  # 缩放，输入宽度px
        self.resized = imutils.resize(self.raw, width)
        self.modify = imutils.resize(self.modify, width)
        self.ratio = self.raw.shape[0] / float(self.modify.shape[0])

    def gray(self) -> None:  # 黑白
        self.modify = cv2.cvtColor(self.modify, cv2.COLOR_BGR2GRAY)

    def blur(self, ksize=(5, 5), sigmaX=0) -> None:  # 高斯模糊
        self.modify = cv2.GaussianBlur(self.modify, ksize, sigmaX)

    def threshold(self, thresh=60, maxval=255) -> None:  # 二值化
        self.modify = cv2.threshold(self.modify, thresh, maxval, cv2.THRESH_BINARY)[1]

    def getCnts(self, resize=300, thresh=60, maxval=255):
        self.resize(resize)
        self.gray()
        self.blur()
        # self.threshold(thresh, maxval)
        edge = cv2.Canny(self.modify, 75, 200)
        # cv2.imshow("canny", edge)
        self.cnts = cv2.findContours(edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]

    def drawShape(self, resize=300, thresh=60, maxval=255):
        self.getCnts(resize, thresh, maxval)
        for c in self.cnts:
            # compute the center of the contour, then detect the name of the
            # shape using only the contour

            M = cv2.moments(c)
            cX = int(M["m10"] / (M["m00"] + 1))
            cY = int(M["m01"] / (M["m00"] + 1))
            shape = getCntShapeName(c)

            # multiply the contour (x, y)-coordinates by the resize ratio,
            # then draw the contours and the name of the shape on the image
            c = c.astype("float")
            # c *= self.ratio
            c = c.astype("int")
            cv2.drawContours(self.resized, [c], -1, (0, 255, 0), 2)
            # cv2.putText(self.resized, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.5, (255, 255, 255), 2)
            (b, g, r) = self.resized[cY][cX]
            if r > (g + b):
                color = "RED"
            elif g > (r + b):
                color = "GREEN"
            elif b > (r + g):
                color = "BLUE"
            else:
                color = "NULL"
            # print(r, g, b)
            self.resized = putChineseText(self.resized, shape + color, (cX, cY), textColor=(255, 0, 255), textSize=20)
            # show the output image
            # cv2.imshow("Image", self.resized)
            # cv2.waitKey(0)

    def getShape(self, resize=300, thresh=60, maxval=255):
        self.getCnts(resize, thresh, maxval)
        for c in self.cnts:
            # compute the center of the contour, then detect the name of the
            # shape using only the contour

            M = cv2.moments(c)
            cX = int(M["m10"] / (M["m00"] + 1))
            cY = int(M["m01"] / (M["m00"] + 1))
            shape = getCntShapeName(c)

            # multiply the contour (x, y)-coordinates by the resize ratio,
            # then draw the contours and the name of the shape on the image
            c = c.astype("float")
            # c *= self.ratio
            c = c.astype("int")
            cv2.drawContours(self.resized, [c], -1, (0, 255, 0), 2)
            # cv2.putText(self.resized, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.5, (255, 255, 255), 2)
            (b, g, r) = self.resized[cY][cX]
            if r > (g + b):
                color = "RED"
            elif g > (r + b):
                color = "GREEN"
            elif b > (r + g):
                color = "BLUE"
            else:
                color = "NULL"
            # print(r, g, b)
            self.resized = putChineseText(self.resized, shape + color, (cX, cY), textColor=(255, 0, 255), textSize=20)
            # show the output image
            # cv2.imshow("Image", self.resized)
            # cv2.waitKey(0)
            sendData = str("!"+color+","+shape+"*")
            print(str("!"+color+","+shape+"*"))
            print("x:"+str(cX)+" y:"+str(cY))
            return sendData