class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        """
            Khởi tạo button
                - image: Ảnh của button (Có thể là None)
                - pos: Tọa độ của button
                - text_input: Text của button
                - font: Font của text
                - base_color: Màu của text khi không hover
                - hovering_color: Màu của text khi hover
        """
        self.image = image
        self.x_pos, self.y_pos = pos
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        if self.image is None:
            self.image = self.text

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    # Kiểm tra xem chuột có nằm trong nút hay không
    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    # Thay đổi màu khi rê chuột lên nút
    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
