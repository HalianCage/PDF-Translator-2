# legend_utils.py

# Install dependencies
# These should be run once in your main application setup or environment:
# !pip install PyPDF2 pikepdf PyMuPDF reportlab opencv-python-headless python-abbreviate

import fitz  # PyMuPDF
import cv2
import numpy as np
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, grey, whitesmoke
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from PyPDF2 import PdfReader, PdfWriter
import io
import pikepdf

# Setup abbreviation tool
try:
    import abbreviate
    abbr_tool = abbreviate.Abbreviate()
except ImportError:
    abbr_tool = None
    print("Warning: 'python-abbreviate' not found. Using fallback.")

# Paragraph style for wrapping
styles = getSampleStyleSheet()
styleN = styles["Normal"]
styleN.fontName = "Helvetica"
styleN.fontSize = 9
styleN.wordWrap = 'CJK'

def refine_abbreviation(term, used_codes, max_len=4, abbr_tool=None):
    if abbr_tool:
        candidate = abbr_tool.abbreviate(term, target_len=max_len)
    else:
        candidate = "".join(w[0].upper() for w in term.split())
    if not candidate:
        candidate = term[:max_len].upper()
    if len(candidate) > max_len + 2:
        candidate = candidate[:max_len]
    if candidate in used_codes:
        for k, v in used_codes.items():
            if k == term:
                return v
        idx = 1
        new_code = f"{candidate}{idx}"
        while new_code in used_codes.values():
            idx += 1
            new_code = f"{candidate}{idx}"
        candidate = new_code
    used_codes[term] = candidate
    return candidate


def create_canvas_with_image(img_cv, legend_panel=None):
    if legend_panel is not None:
        final_img_cv = np.concatenate((img_cv, legend_panel), axis=1)
    else:
        final_img_cv = img_cv
    final_pil = Image.fromarray(cv2.cvtColor(final_img_cv, cv2.COLOR_BGR2RGB))
    img_buffer = io.BytesIO()
    final_pil.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    temp_packet = io.BytesIO()
    c = canvas.Canvas(temp_packet, pagesize=(final_img_cv.shape[1], final_img_cv.shape[0]))
    c.drawImage(ImageReader(img_buffer), 0, 0, width=final_img_cv.shape[1], height=final_img_cv.shape[0])
    return c, temp_packet, final_img_cv.shape

def compress_pdf(input_stream, output_path):
    with pikepdf.open(input_stream) as pdf:
        pdf.save(output_path, compress_streams=True)

def add_legends_to_pdf(input_pdf, output_pdf, terms_per_page, styleN, abbr_tool, avg_font_size):
    doc = fitz.open(input_pdf)
    output_writer = PdfWriter()

    for page_num, page in enumerate(doc):
        terms = terms_per_page.get(page_num, [])
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        cropped_img = _crop_blank_margins(img_cv)
        bg_color_bgr = _get_corner_color(page)
        page_width, page_height = cropped_img.shape[1], cropped_img.shape[0]
        used_codes = {}

        if len(terms) >= 5:
            legend_width = _calculate_dynamic_legend_width(terms, page_width)
            final_font_size = _determine_legend_font_size(avg_font_size)
            legend_data = _create_legend_table(terms, styleN, used_codes, abbr_tool=abbr_tool)
            table = Table(legend_data, colWidths=[60, legend_width - 60])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), final_font_size),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, black),
                ('VALIGN', (0, 1), (-1, -1), 'TOP'),
            ]))
            table, adjusted_font_size = _adjust_legend_size_to_fit(page_height, table, final_font_size, legend_width)
            legend_panel = np.full((cropped_img.shape[0], legend_width, 3), bg_color_bgr, dtype=np.uint8)
            temp_canvas, temp_packet, _ = create_canvas_with_image(cropped_img, legend_panel)
            table_width, table_height = table.wrap(legend_width - 20, page_height)
            legend_x = cropped_img.shape[1] + 10
            legend_y = page_height - table_height - 20
            table.wrapOn(temp_canvas, legend_width - 20, page_height)
            table.drawOn(temp_canvas, legend_x, legend_y)
            temp_canvas.save()
            temp_packet.seek(0)
            new_pdf = PdfReader(temp_packet)
            output_writer.add_page(new_pdf.pages[0])
        else:
            temp_canvas, temp_packet, _ = create_canvas_with_image(cropped_img)
            temp_canvas.save()
            temp_packet.seek(0)
            new_pdf = PdfReader(temp_packet)
            output_writer.add_page(new_pdf.pages[0])

    output_stream = io.BytesIO()
    output_writer.write(output_stream)
    output_stream.seek(0)
    compress_pdf(output_stream, output_pdf)
    print(f"\n📦 Compressed PDF saved as: {output_pdf}")


# Helper function to remove the extra whitespace surrounding the image
def _crop_blank_margins(img_cv, margin=10):
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    coords = cv2.findNonZero(binary)
    if coords is None:
        return img_cv
    x, y, w, h = cv2.boundingRect(coords)
    x1 = max(0, x - margin)
    y1 = max(0, y - margin)
    x2 = min(img_cv.shape[1], x + w + margin)
    y2 = min(img_cv.shape[0], y + h + margin)
    return img_cv[y1:y2, x1:x2]


# Helper function to get the color of the image background; Used to generate the new canvas for the legend
def _get_corner_color(page):
    pix = page.get_pixmap(matrix=fitz.Matrix(1, 1))
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    arr = np.array(img)
    corner = arr[0:50, -50:, :]
    avg_color = tuple(np.mean(corner, axis=(0, 1)).astype(int))
    return avg_color

# Helper function to get the most optimized legend width
def _calculate_dynamic_legend_width(terms, page_width, max_percentage=0.4, min_width=100):
    if not terms:
        return min_width
    longest_term = max(terms, key=len)
    estimated_width = len(longest_term) * 6
    max_width = int(page_width * max_percentage)
    final_width = min(max(estimated_width + 40, min_width), max_width)
    return final_width


# Helper function to determine the font size to use for the legend
def _determine_legend_font_size(avg_font_size, min_font_size=7):
    return max(avg_font_size, min_font_size)

# Helper function to create the legend's data list
def _create_legend_table(terms, styleN, used_codes, max_len=4, abbr_tool=None):
    legend_data = [["Code", "Meaning"]]
    for term in terms:
        abbr = refine_abbreviation(term, used_codes, max_len, abbr_tool)
        meaning_para = Paragraph(term, styleN)
        legend_data.append([abbr, meaning_para])
    return legend_data


# Helper function to adjust the legend if it's height exceeds the page height
def _adjust_legend_size_to_fit(page_height, table, initial_font_size, max_width, min_font_size=5):
    font_size = initial_font_size
    width, height = table.wrap(max_width, page_height)
    while height > page_height and font_size > min_font_size:
        font_size -= 1
        table.setStyle([('FONTSIZE', (0, 0), (-1, -1), font_size)])
        width, height = table.wrap(max_width, page_height)
    if height > page_height:
        print("Warning: Legend still exceeds page height after adjustments.")
    return table, font_size