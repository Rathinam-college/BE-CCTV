import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from cctv.models import Biometric
from cctv.serializers import BiometricSerializer

def check():
    print("Attempting to query Biometric objects...")
    try:
        biometrics = list(Biometric.objects.all())
        print(f"Success! Found {len(biometrics)} biometric devices.")
        
        if biometrics:
            print("Attempting to serialize the first biometric device...")
            serializer = BiometricSerializer(biometrics[0])
            print("Serialized data:", serializer.data)
            print("Serialization success!")
        else:
            print("No biometric devices found in database to serialize.")
    except Exception as e:
        print("ERROR occurred:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check()
