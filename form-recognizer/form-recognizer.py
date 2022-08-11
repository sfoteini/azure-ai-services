from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv('KEY')
endpoint = os.getenv('ENDPOINT')

# Create a Form Recognizer Client
form_recognizer_client = FormRecognizerClient(endpoint, AzureKeyCredential(key))

# Specify the URL of the receipt you will be recognizing
receiptUrl = ""

# Start the recognition
poller = form_recognizer_client.begin_recognize_receipts_from_url(receiptUrl)
results = poller.result()

# Get the first receipt in the results (we have only one!)
receipt = results[0].fields

print("\n" + "-"*16 + "\n")

# General information
receipt_type = receipt.get("ReceiptType")
print(f"Receipt Type: {receipt_type.value} (confidence {receipt_type.confidence*100 :.2f}%)")
receipt_date = receipt.get("TransactionDate")
print(f"Transaction Date: {receipt_date.value} (confidence {receipt_date.confidence*100 :.2f}%)")
print()

# Receipt items
print("Receipt Items:")
for idx, items in enumerate(receipt.get("Items").value):
    print("...Item #{}".format(idx + 1))
    for item_name, item in items.value.items():
        print(f"......{item_name}: {item.value} (confidence {item.confidence*100 :.2f}%)")
print()

# Total price
subtotal = receipt.get("Subtotal")
print(f"Subtotal: {subtotal.value} (confidence {subtotal.confidence*100 :.2f}%)")
tax = receipt.get("Tax")
print(f"Tax: {tax.value} (confidence {tax.confidence*100 :.2f}%)")
total = receipt.get("Total")
print(f"Total: {total.value} (confidence {total.confidence*100 :.2f}%)")

print("\n" + "-"*16 + "\n")