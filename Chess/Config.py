class Config:
    # Kích thước tổng thể của bàn cờ (pixels)
    WIDTH = 768
    HEIGHT = 768

    # Số hàng và cột trên bàn cờ (8x8 ô)
    DIMENSION = 8

    # Kích thước mỗi ô vuông trên bàn cờ (pixels)
    SQ_SIZE = HEIGHT // DIMENSION

    # Số khung hình mỗi giây (tốc độ làm mới)
    MAX_FPS = 15

    # Kích thước khung hiển thị lịch sử nước đi
    MOVE_LOG_W = 350
    MOVE_LOG_H = HEIGHT

    # Màu ô tối trên bàn cờ (RGB)
    SQ_DARK_COLOR = (115, 149, 82)

    # Màu ô sáng trên bàn cờ (RGB)
    SQ_LIGHT_COLOR = (235, 236, 208)

    # Màu chữ trên nền sáng (để chữ dễ nhìn)
    TEXT_LIGHT_COLOR = (115, 149, 82)

    # Màu chữ trên nền tối (để chữ dễ nhìn)
    TEXT_DARK_COLOR = (235, 236, 208)

    # Font chữ
    FONT_NAME = "Trebuchet MS"
    FONT_SIZE = 20
    FONT_BOLD = False
    FONT_ITALIC = False

    # Thời gian chờ sau khi ván cờ kết thúc (giây)
    TIME_WHILE_END = 2

    # Màu nền menu hoặc màn hình trắng
    BACKGROUND_COLOR = "white"

    @staticmethod
    def get_font():
        return Config.FONT_NAME, Config.FONT_SIZE, Config.FONT_BOLD, Config.FONT_ITALIC