import pandas as pd
import qrcode
import os

def generate_qrs():
    # Read Excel file without header
    try:
        df = pd.read_excel('product_number.xlsx', header=None)
    except FileNotFoundError:
        print("Error: 'product_number.xlsx' not found.")
        return

    # Create directory for QR codes
    output_dir = 'qr_codes'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Found {len(df)} rows.")

    # Iterate through rows
    # Assuming column 0 is ID and column 1 is Product Number based on previous inspection
    for index, row in df.iterrows():
        product_number = str(row[1]).strip()
        
        # Skip empty product numbers
        if not product_number or product_number.lower() == 'nan':
            continue

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(product_number)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save image
        # Replace slashes in filename just in case
        safe_filename = product_number.replace('/', '_').replace('\\', '_')
        file_path = os.path.join(output_dir, f"{safe_filename}.png")
        img.save(file_path)
        print(f"Generated QR for: {product_number}")

    print("QR Code generation complete.")

if __name__ == "__main__":
    generate_qrs()
