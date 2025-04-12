class Config:
    # Kích thước tổng thể của bàn cờ (pixels)
    WIDTH = 768       # Chiều rộng bàn cờ
    HEIGHT = 768      # Chiều cao bàn cờ

    # Số hàng và cột trên bàn cờ
    DIMENSION = 8     # Bàn cờ 8x8 ô

    # Kích thước mỗi ô vuông trên bàn cờ (pixels)
    SQ_SIZE = HEIGHT // DIMENSION

    # Số khung hình mỗi giây (tốc độ làm mới)
    MAX_FPS = 15

    # Kích thước khung hiển thị lịch sử nước đi
    MOVE_LOG_W = 350  # Chiều rộng khung log
    MOVE_LOG_H = HEIGHT  # Chiều cao khung log = chiều cao bàn cờ

    # Màu ô tối trên bàn cờ (RGB)
    SQ_DARK_COLOR = (115, 149, 82)

    # Màu ô sáng trên bàn cờ (RGB)
    SQ_LIGHT_COLOR = (235, 236, 208)

    # Màu chữ trên nền sáng (để chữ dễ nhìn)
    TEXT_LIGHT_COLOR = (115, 149, 82)

    # Màu chữ trên nền tối (để chữ dễ nhìn)
    TEXT_DARK_COLOR = (235, 236, 208)
