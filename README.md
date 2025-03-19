## Khóa học

Cơ sở trí tuệ nhân tạo (2324II_AIT2004_1)

# Thông tin dự án
Dự án cờ vua sử dụng thuật toán Negamax cùng cắt tỉa Alpha Beta

## Mô tả
Dự án "CHESS AI" là một ứng dụng phát triển trò chơi cờ vua có trí tuệ nhân tạo tích hợp. Nhóm phát triển bao gồm các thành viên với phân công công việc cụ thể như phát triển giao diện, triển khai thuật toán AI,  và thiết kế đồ họa. Sử dụng ngôn ngữ Python và thư viện Pygame, dự án này cung cấp khả năng chơi cờ với máy ở mức độ từ cơ bản đến trung bình, với thuật toán tìm kiếm như Negamax và Alpha-Beta Pruning.

Vai trò của các file như sau:
- ChessMain: Điều khiển luồng chính của game, quản lý các sự kiện và cập nhật trạng thái của bàn cờ.
- ChessEngine: xây dựng lớp GameStae chịu trách nhiệm lưu trữ tất cả các trạng thái hiện tại của một ván cờ, xác định các nước đi hợp lệ ở trạng thái hiện tại, lưu trữ lịch sử di chuyển. Xây dựng lớp Move giúp quản lý và lưu trữ thông tin về các nước đi một cách có tổ chức và dễ dàng truy xuất.
- AIEngine: gồm các hàm và dữ liệu cần thiết về giá trị của quân cờ và giá trị của quân cờ đó tại một vị trí cụ thể trên bàn cờ để đánh giá các nước đi và tìm ra nước đi tốt nhất dựa trên thuật toán tìm kiếm
- Button: Lớp đại diện cho các nút trong giao diện người dùng, xử lý việc hiển thị và kiểm tra các sự kiện chuột.
- Config: Chứa các cấu hình và thông số kỹ thuật như kích thước màn hình, màu sắc, và các cài đặt khác.

# Cài đặt
```bash
git clone https://github.com/0402anhhuy/AIChess.git
pip install -r requirements.txt
python Chess/main.py
```
