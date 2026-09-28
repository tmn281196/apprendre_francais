# Học tiếng Pháp

Trang luyện nói tiếng Pháp. Toàn bộ là file tĩnh (HTML, CSS, JS, JSON), không có backend, không có bước dựng;
đăng trên GitHub Pages: https://tmn281196.github.io/apprendre_francais/

| Trang | Nội dung |
|---|---|
| `fr-matrix` | ~2900 câu các bài Speaking Matrix dịch sang tiếng Pháp, ngắt khối kèm nghĩa tiếng Việt |

## Cấu trúc

```
src/            cả site, đăng nguyên thư mục này
  index.html            trang mục lục
  fr-matrix/            data.json (bài, câu tiếng Pháp, khối), vi.json (nghĩa tiếng Việt)
data/
  fr.json               bản dịch tiếng Pháp, khóa là câu tiếng Anh của trang en-matrix
tools/
  fr-matrix.py          dựng src/fr-matrix/data.json, vi.json (Python 3)
```

## Xem thử

Trang đọc dữ liệu bằng `fetch`, nên phải mở qua http chứ không mở file trực tiếp:

```bash
python -m http.server -d src
```

rồi vào http://localhost:8000.

## Đăng lên GitHub Pages

Đẩy lên nhánh `main` là xong: `.github/workflows/pages.yml` đăng nguyên `src/`.

## Sửa nội dung

- Câu tiếng Pháp: sửa `data/fr.json` (mỗi câu: `fr` và `c` = danh sách `[khối, nghĩa]`, ghép các khối bằng dấu
  cách phải ra đúng `fr`), rồi dựng lại từ `data.json` của trang en-matrix (repo english_study):

  ```bash
  python tools/fr-matrix.py ../english_study/src/en-matrix/data.json
  ```

  Khung bài (năm cuốn, INPUT/OUTPUT, tên bài tiếng Việt) lấy từ en-matrix; câu tiếng Pháp và nghĩa do máy dịch
  từ câu tiếng Anh, nên có thể còn chỗ chưa tự nhiên.
