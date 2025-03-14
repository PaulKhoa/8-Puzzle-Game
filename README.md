# 8-Puzzle Solver

## 🧩 Giới thiệu
**8-Puzzle** là một trò chơi sắp xếp ô số cổ điển trên một lưới 3x3 với một ô trống, trong đó người chơi cần sắp xếp các số theo thứ tự tăng dần bằng cách di chuyển ô trống.  

Dự án này triển khai thuật toán tìm kiếm để giải bài toán 8-Puzzle, bao gồm:
- **BFS (Breadth-First Search)** - Tìm kiếm theo chiều rộng  
- **DFS (Depth-First Search)** - Tìm kiếm theo chiều sâu  
- **UCS (Uniform Cost Search)** - Tìm kiếm theo chi phí đồng nhất  
- **A* (A-star Search)** - Tìm kiếm A* với heuristic  
- **Greedy Best-First Search** - Tìm kiếm tham lam  

## 📌 Cách hoạt động
- Chương trình yêu cầu đầu vào là trạng thái ban đầu của bảng 8-Puzzle.  
- Người dùng có thể chọn thuật toán để tìm đường giải tối ưu.  
- Chương trình xuất ra các bước di chuyển từ trạng thái ban đầu đến trạng thái đích.
