# ThaiMarkdownhelper 🇹🇭📄

**ThaiMarkdownhelper** คือเครื่องมือแปลงเอกสารเป็น **Markdown** ที่พัฒนาต่อยอดจาก **[Microsoft MarkItDown](https://github.com/microsoft/markitdown)** โดยได้รับการปรับปรุงและเพิ่มประสิทธิภาพสำหรับการใช้งานกับ**ภาษาไทย**โดยเฉพาะ พร้อมหน้าจอ **Web UI แบบลากวาง (Drag & Drop)** ใช้งานง่ายเพียงคลิกเดียว

[![GitHub license](https://img.shields.io/github/license/TipokSMiw/ThaiMarkdownhelper)](https://github.com/TipokSMiw/ThaiMarkdownhelper/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Powered by](https://img.shields.io/badge/powered%20by-Microsoft%20MarkItDown-0078D4.svg)](https://github.com/microsoft/markitdown)

---

## 🌟 จุดเด่นและฟีเจอร์ที่พัฒนาเพิ่ม (Key Features)

### 1. 🇹🇭 Thai Smart Engine (กู้คืนสระลอย/วรรณยุกต์เพี้ยนใน Digital PDF)
- **แก้ปัญหา Thai PUA Shift (`0xF700` – `0xF71A`)**: เอกสารที่เซฟจาก Microsoft Word, Excel หรือ InDesign มักมีปัญหาสระบนและวรรณยุกต์หลุดหาย (เช่น `ที่นี่` กลายเป็น `ทนี`) ระบบจะแปลงคืนเป็น Unicode ไทยมาตรฐานโดยอัตโนมัติ
- **กู้คืนข้อความเพี้ยนจาก CMap CID Fallback (อักษร Cyrillic)**: แก้ปัญหาบั๊กฟอนต์ Tahoma ใน PDF ที่ทำให้สระและวรรณยุกต์กลายเป็นอักษรรัสเซีย (เช่น `ผѬҖ` $\rightarrow$ `ผู้`, `จѼากัด` $\rightarrow$ `จำกัด`, `ใหญҕ` $\rightarrow$ `ใหญ่`)
- **แก้ปัญหาสระอำ (`ำ`) แตกตัว**: ซ่อมแซมสระอำที่ถูกแยกตัวเป็นพยัญชนะ + ช่องว่าง + สระอา (เช่น `ค า` $\rightarrow$ `คำ`, `ส า` $\rightarrow$ `สำ`)
- **ลบช่องว่างแทรกระหว่างสระและวรรณยุกต์**: จัดการคำที่มีการเคาะวรรณยุกต์แยก (เช่น `ผู ้` $\rightarrow$ `ผู้`)
- **ล้างขยะ Zero-Width Space (`\u200b`)**: กำจัดอักขระเคาะตัดบรรทัดที่ซ่อนอยู่ใน PDF ที่ส่งออกจาก Google Docs
- **ความแม่นยำสูง 99.9%**: ดึงข้อความดิจิทัลแท้ผ่าน PyMuPDF C-Engine ไม่ตัดคำเพี้ยน และแปลงเสร็จในเสี้ยววินาที


### 2. 🔍 Local Thai OCR (EasyOCR Engine)
- ทำงานแบบ **Offline 100% บนเครื่อง** ไม่ต้องเชื่อมต่อ Cloud API หรือเสียค่าบริการรายเดือน
- สกัดข้อความภาษาไทยและอังกฤษจากไฟล์รูปภาพ (`.png`, `.jpg`, `.jpeg`, `.webp`)
- ระบบ **Smart Hybrid**: หน้าที่มีตัวหนังสือดิจิทัลจะดึงแบบความเร็วสูง ส่วนหน้าที่เป็นภาพปกหรือเอกสารสแกนจะสลับไปทำ OCR ให้อัตโนมัติ

### 3. 🌐 Modern Web UI (ลากวางแล้วแปลงได้ทันที)
- **Drag & Drop Zone**: ลากไฟล์มาวาง หรือคลิกเลือกไฟล์ได้อย่างสะดวก
- **Dual View**: แสดงผลลัพธ์ทั้งแบบ **Preview (Rendered HTML)** และ **Raw Markdown**
- **One-Click Export**: ปุ่ม Copy to Clipboard และปุ่มดาวน์โหลดไฟล์ `.md` กลับลงเครื่องทันที
- **One-Click Windows Launcher**: มีไฟล์ `run_ui.bat` ให้ดับเบิลคลิกเปิดโปรแกรมได้ทันที

---

## 📁 รูปแบบไฟล์ที่รองรับ

| ประเภทไฟล์ | นามสกุล | การประมวลผล |
|---|---|---|
| **PDF Documents** | `.pdf` | Thai Smart Engine (Digital PUA + EasyOCR Fallback) |
| **Microsoft Word** | `.docx` | MarkItDown Native Parser |
| **Microsoft Excel** | `.xlsx`, `.xls`, `.csv` | MarkItDown Table Extractor |
| **Microsoft PowerPoint** | `.pptx` | MarkItDown Slide Extractor |
| **Images** | `.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp` | Local Thai + English OCR (EasyOCR) |
| **Text & Web** | `.txt`, `.html`, `.json`, `.xml` | MarkItDown Parser |

---

## 🚀 วิธีการติดตั้งและเริ่มใช้งาน (Quick Start)

### ความต้องการของระบบ (Prerequisites)
- ระบบปฏิบัติการ: Windows 10/11, macOS, หรือ Linux
- Python: **3.10 ขึ้นไป** (แนะนำ Python 3.11)

### 1. ติดตั้ง Dependencies
เปิด Terminal หรือ PowerShell ในโฟลเดอร์โปรเจกต์:

```powershell
# ติดตั้ง MarkItDown และ Dependencies ทั้งหมด
pip install -e ".\packages\markitdown[all]"

# ติดตั้ง PyMuPDF และ EasyOCR สำหรับระบบภาษาไทย
pip install pymupdf easyocr
```

### 2. เปิดใช้งานโปรแกรม

#### วิธีที่ 1: ดับเบิลคลิกไฟล์ Batch (สำหรับ Windows)
- ดับเบิลคลิกที่ไฟล์ **`run_ui.bat`**
- หน้าต่างเว็บเบราว์เซอร์จะเปิดขึ้นมาที่ `http://127.0.0.1:8080` ให้อัตโนมัติ

#### วิธีที่ 2: รันผ่าน Terminal / Command Line
```powershell
python app.py
```
จากนั้นเปิดเบราว์เซอร์แล้วไปที่: **`http://127.0.0.1:8080`**

---

## 📂 โครงสร้างของโปรเจกต์ (Project Structure)

```text
ThaiMarkdownhelper/
├── app.py                # Backend Web Server (Python Standard Library HTTP)
├── index.html            # Frontend Web UI (Drag & Drop, Markdown Viewer)
├── thai_ocr.py           # โมดูล Thai Smart Engine (PUA De-Shifter + EasyOCR)
├── run_ui.bat            # ตัวเปิดโปรแกรม One-Click สำหรับ Windows
├── packages/markitdown/  # ซอร์สโค้ดหลักของ Microsoft MarkItDown
├── LICENSE               # สัญญาอนุญาต MIT License ดั้งเดิมของ Microsoft
└── README.md             # เอกสารแนะนำโปรเจกต์
```

---

## 🙏 เครดิตและแหล่งอ้างอิง (Acknowledgements & Credits)

โปรเจกต์นี้พัฒนาต่อยอดจากและใช้งานไลบรารี Open Source ชั้นนำ:

* **[Microsoft MarkItDown](https://github.com/microsoft/markitdown)** - ไลบรารีหลักสำหรับการแปลงโครงสร้างเอกสารเป็น Markdown พัฒนาโดย Microsoft Corporation ภายใต้สัญญาอนุญาต [MIT License](https://github.com/microsoft/markitdown/blob/main/LICENSE)
* **[EasyOCR](https://github.com/JaidedAI/EasyOCR)** - เอนจิน Deep Learning OCR สำหรับภาษาไทยและภาษาอังกฤษ พัฒนาโดย Jaided AI
* **[PyMuPDF](https://github.com/pymupdf/PyMuPDF)** - ไลบรารีประสิทธิภาพสูงสำหรับการจัดการและเรนเดอร์ไฟล์ PDF
* **[Marked.js](https://github.com/markedjs/marked)** - ไลบรารี JavaScript สำหรับแปลง Markdown เป็น HTML บนหน้าเว็บ

---

## 📄 สัญญาอนุญาต (License)

โปรเจกต์นี้เผยแพร่ภายใต้สัญญาอนุญาต **[MIT License](LICENSE)** เช่นเดียวกับ Microsoft MarkItDown คุณสามารถนำไปใช้ ศึกษาต่อยอด หรือปรับแต่งได้อย่างอิสระ
