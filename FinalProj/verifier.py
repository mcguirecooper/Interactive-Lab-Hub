from ecdsa import VerifyingKey

print("""\
   _____  _                       _                      __      __          _   __  _             
  / ____|(_)                     | |                     \ \    / /         (_) / _|(_)            
 | (___   _   __ _  _ __    __ _ | |_  _   _  _ __  ___   \ \  / /___  _ __  _ | |_  _   ___  _ __ 
  \___ \ | | / _` || '_ \  / _` || __|| | | || '__|/ _ \   \ \/ // _ \| '__|| ||  _|| | / _ \| '__|
  ____) || || (_| || | | || (_| || |_ | |_| || |  |  __/    \  /|  __/| |   | || |  | ||  __/| |   
 |_____/ |_| \__, ||_| |_| \__,_| \__| \__,_||_|   \___|     \/  \___||_|   |_||_|  |_| \___||_|   
              __/ |                                                                                
             |___/                                                                                 
""")

importet_vk = VerifyingKey.from_string(bytes.fromhex(input("🔑 Enter the Verifying Key: ")))
imported_signature = bytes.fromhex(input("📝 Enter the Signature: "))
imported_msg = input("📊 Enter the Report: ")

try:
    importet_vk.verify(imported_signature, imported_msg.encode('UTF-8'))
    print("✅ Verification successful")
except:
    print("❌ Verification Error! The report and the signature do not match. The accuracy of the report might be compromised. Please contact our support team.")