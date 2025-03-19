class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        """
            Khởi tạo button
                - image: Ảnh của button
                - pos: Tọa độ của button
                - text_input: Text của button
                - font: Font của text
                - base_color: Màu của text khi không hover
                - hovering_color: Màu của text khi hover
        """
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
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

    def checkForInput(self, position):
        """
            Kiểm tra xem chuột có nằm trong button không
                - Lấy tọa độ chuột (X, Y)
                - Lấy tọa độ các cạnh của button
                - So sánh tọa độ chuột với tọa độ các cạnh của button
                - Nếu tọa độ chuột nằm trong button thì trả về True
                - Ngược lại trả về False
        """
        mouse_x = position[0]
        mouse_y = position[1]

        button_left = self.rect.left   
        button_right = self.rect.right
        button_top = self.rect.top
        button_bottom = self.rect.bottom

        is_inside_x = button_left <= mouse_x <= button_right
        is_inside_y = button_top <= mouse_y <= button_bottom

        if is_inside_x and is_inside_y:
            return True
        else:
            return False

    def changeColor(self, position):
        """
            Kiểm tra xem chuột có nằm trong button không
                - Lấy tọa độ chuột (X, Y)
                - Lấy tọa độ các cạnh của button
                - So sánh tọa độ chuột với tọa độ các cạnh của button
                - Nếu tọa độ chuột nằm trong button thì thay đổi màu của text
                - Ngược lại giữ nguyên màu của text
        """
        mouse_x = position[0]
        mouse_y = position[1]

        button_left = self.rect.left
        button_right = self.rect.right
        button_top = self.rect.top
        button_bottom = self.rect.bottom

        is_inside_x = button_left <= mouse_x <= button_right
        is_inside_y = button_top <= mouse_y <= button_bottom

        if is_inside_x and is_inside_y:
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

