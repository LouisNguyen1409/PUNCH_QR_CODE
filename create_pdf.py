from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import os

def create_qr_pdf():
    output_filename = "product_qr_codes.pdf"
    qr_dir = "qr_codes"
    
    c = canvas.Canvas(output_filename, pagesize=A4)
    width, height = A4
    
    # Layout configuration
    margin_x = 1.5 * cm
    margin_y = 2 * cm
    cols = 3
    rows = 6
    
    # Calculate cell size
    cell_width = (width - 2 * margin_x) / cols
    cell_height = (height - 2 * margin_y) / rows
    
    # Image size inside cell
    img_size = 3.5 * cm
    
    qr_files = sorted([f for f in os.listdir(qr_dir) if f.endswith('.png')])
    
    print(f"Found {len(qr_files)} QR codes.")
    
    x_offset = margin_x
    y_offset = height - margin_y - cell_height
    
    count = 0
    
    for qr_file in qr_files:
        product_name = os.path.splitext(qr_file)[0]
        # Restore original characters if we replaced them
        product_name_display = product_name.replace('_', '/')
        
        # Center image in cell
        img_x = x_offset + (cell_width - img_size) / 2
        img_y = y_offset + (cell_height - img_size) / 2 + 0.5 * cm # Shift up for text
        
        # Draw Image
        img_path = os.path.join(qr_dir, qr_file)
        c.drawImage(img_path, img_x, img_y, width=img_size, height=img_size)
        
        # Draw Text (Product Number)
        c.setFont("Helvetica", 8)
        text_x = x_offset + cell_width / 2
        text_y = img_y - 0.5 * cm
        c.drawCentredString(text_x, text_y, product_name_display)
        
        # Move to next position
        count += 1
        x_offset += cell_width
        
        # Check if row is full
        if count % cols == 0:
            x_offset = margin_x
            y_offset -= cell_height
            
        # Check if page is full
        if count % (cols * rows) == 0:
            c.showPage()
            x_offset = margin_x
            y_offset = height - margin_y - cell_height
            
    c.save()
    print(f"PDF created: {output_filename}")

if __name__ == "__main__":
    create_qr_pdf()
