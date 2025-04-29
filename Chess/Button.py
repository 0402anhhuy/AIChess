class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        """
            Khởi tạo button
                - image: Ảnh của button (Có thể là None nếu không sử dụng ảnh)
                - pos: Tọa độ trung tâm của button (x, y)
                - text_input: Văn bản hiển thị trên button
                - font: Font chữ của văn bản
                - base_color: Màu của văn bản khi không hover
                - hovering_color: Màu của văn bản khi hover
        """
        self.image = image  # Ảnh của button (nếu có)
        self.x_pos, self.y_pos = pos  # Tọa độ trung tâm của button
        self.font = font  # Font chữ của văn bản
        self.base_color = base_color  # Màu văn bản khi không hover
        self.hovering_color = hovering_color  # Màu văn bản khi hover
        self.text_input = text_input  # Văn bản hiển thị trên button
        self.text = self.font.render(self.text_input, True, self.base_color)  # Tạo văn bản với màu cơ bản

        # Nếu không có ảnh, sử dụng văn bản làm ảnh
        if self.image is None:
            self.image = self.text

        # Tạo hình chữ nhật bao quanh button dựa trên ảnh hoặc văn bản
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))  # Hình chữ nhật của button
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))  # Hình chữ nhật của văn bản

    def update(self, screen):
        """
            Hiển thị button lên màn hình.
                - screen: Màn hình để vẽ button.
        """
        if self.image is not None:  # Nếu có ảnh, vẽ ảnh
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)  # Vẽ văn bản lên màn hình

    # Hàm kiểm tra xem chuột có nằm trong button hay không
    def checkForInput(self, position):
        """
            Kiểm tra xem chuột có nằm trong button hay không.
                - position: Tọa độ của chuột (x, y).
                - Trả về: True nếu chuột nằm trong button, ngược lại False.
        """
        return self.rect.collidepoint(position)  # Kiểm tra va chạm giữa chuột và button

    # Hàm thay đổi màu sắc khi nhấp chuột vào quân cờ
    def changeColor(self, position):
        """
            Thay đổi màu của văn bản khi chuột di chuyển qua button.
                - position: Tọa độ của chuột (x, y).
        """
        if self.rect.collidepoint(position):  # Nếu chuột nằm trong button
            self.text = self.font.render(self.text_input, True, self.hovering_color)  # Đổi màu sang màu hover
        else:  # Nếu chuột không nằm trong button
            self.text = self.font.render(self.text_input, True, self.base_color)  # Đổi màu về màu cơ bản