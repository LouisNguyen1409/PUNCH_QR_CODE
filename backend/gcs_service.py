import os
import json
from google.cloud import storage
from datetime import datetime
import glob

BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "qr-code-scanner-app-data")
LOCAL_DIR = "local_data"

class GCSService:
    def __init__(self):
        self.client = None
        self.bucket = None
        try:
            # Explicitly check for credentials to avoid long timeouts/errors if missing
            if os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or os.getenv("GCLOUD_PROJECT"):
                self.client = storage.Client()
                self.bucket = self.client.bucket(BUCKET_NAME)
                # Check if bucket exists, if not try to create (optional, might fail permissions)
                if not self.bucket.exists():
                    print(f"Bucket {BUCKET_NAME} does not exist. Attempting to create...")
                    try:
                        self.bucket = self.client.create_bucket(BUCKET_NAME)
                    except:
                        print("Could not create bucket. Ensure it exists.")
                print(f"Connected to GCS Bucket: {BUCKET_NAME}")
            else:
                print("No GCS Credentials found. Switching to Local Storage.")
        except Exception as e:
            print(f"GCS Connection Failed (Using Local Storage): {e}")

        if not os.path.exists(LOCAL_DIR):
            os.makedirs(LOCAL_DIR)

    def save_scan(self, data: dict):
        # Sanitize timestamp for filename
        ts_str = data.get('timestamp', datetime.now().isoformat())
        filename = f"scan_{ts_str.replace(':', '-').replace('.', '-')}.json"

        if self.bucket:
            try:
                blob = self.bucket.blob(filename)
                blob.upload_from_string(json.dumps(data), content_type='application/json')
                print(f"Saved to GCS: {filename}")
                return True
            except Exception as e:
                print(f"GCS Upload Error: {e}")
                # Fallback to local

        # Local save
        try:
            with open(os.path.join(LOCAL_DIR, filename), 'w') as f:
                json.dump(data, f)
            print(f"Saved to Local: {filename}")
        except Exception as e:
            print(f"Local Save Error: {e}")
        return True

    def get_history(self):
        scans = []
        if self.bucket:
            try:
                # List blobs. Prefix can be used if we organize folders.
                # max_results for pagination
                blobs = list(self.client.list_blobs(BUCKET_NAME, max_results=100))
                # Sort by time created (updated) descending
                blobs.sort(key=lambda x: x.updated or x.name, reverse=True)
                
                for blob in blobs:
                    try:
                        # Download as string
                        content = blob.download_as_text()
                        data = json.loads(content)
                        scans.append(data)
                    except Exception as e:
                        print(f"Error reading blob {blob.name}: {e}")
                        continue
                return scans
            except Exception as e:
                print(f"GCS Read Error: {e}")
        
        # Local read
        try:
            files = glob.glob(os.path.join(LOCAL_DIR, "*.json"))
            files.sort(reverse=True) # Filenames have timestamps, so sort works
            for f in files[:100]:
                try:
                    with open(f, 'r') as f_in:
                        scans.append(json.load(f_in))
                except:
                    continue
        except Exception as e:
            print(f"Local Read Error: {e}")
            
        return scans
