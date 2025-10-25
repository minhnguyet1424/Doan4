import os
from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill
from datetime import datetime
import re

class ExcelReport:
    def __init__(self, file_path, sheet_name="Sheet1", 
                 tieu_de_base="Báo cáo", header=None):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.tieu_de_base = tieu_de_base
        self.header = header  # header tuỳ chỉnh cho mỗi chức năng

        if os.path.exists(file_path):
            self.wb = load_workbook(file_path)
            if sheet_name in self.wb.sheetnames:
                self.ws = self.wb[sheet_name]
            else:
                self.ws = self.wb.create_sheet(sheet_name)
        else:
            self.wb = Workbook()
            self.ws = self.wb.active
            self.ws.title = sheet_name

        self.tieu_de = self._get_next_tieu_de()

    def _get_next_tieu_de(self):
        count = 0
        pattern = re.compile(rf"{re.escape(self.tieu_de_base)} (\d+)")
        for row in self.ws.iter_rows(min_row=1, max_col=1):
            cell_val = str(row[0].value)
            match = pattern.match(cell_val)
            if match:
                count = max(count, int(match.group(1)))

        new_number = count + 1
        self.ws.append([f"{self.tieu_de_base} {new_number}"])
        self._write_header()
        return f"{self.tieu_de_base} {new_number}"

    def _write_header(self):
        # Nếu header không được truyền thì dùng mặc định
        header = self.header or [
            "STT", "Thời gian", "Thông tin", "Mật khẩu",
            "Kết quả mong đợi", "Kết quả thực tế", "Trạng thái"
        ]
        self.ws.append(header)

    def add_row(self, *values):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = list(values)
        # nếu cột 2 là thời gian thì tự chèn thời gian
        if len(row) > 1:
            row.insert(1, now)
        self.ws.append(row)
        # nếu có cột "Trạng thái" thì tô màu
        status_col = len(row)
        status = row[-1]
        fill = PatternFill(
            start_color="C6EFCE" if status.lower() == "pass" else "FFC7CE",
            end_color="C6EFCE" if status.lower() == "pass" else "FFC7CE",
            fill_type="solid",
        )
        self.ws[f"{chr(64 + status_col)}{self.ws.max_row}"].fill = fill

    def save(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.wb.save(self.file_path)

