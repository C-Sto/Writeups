from Crypto.Cipher import AES
import os

key = os.urandom(16)
def encrypt(key):
    # note -  don't just change this from base64 to text to see the plaintext. That's cheating, and you won't feel l33t
    msg2 = "QW5kIGFsbCB0aGUgZ2lybHMgc2F5IEknbSBwcmV0dHkgZmx5DQpGb3IgYSB3aGl0ZSBndXkuDQoNCkhlIG5lZWRzIHNvbWUgY29vbCB0" \
           "dW5lcw0KTm90IGp1c3QgYW55IHdpbGwgc3VmZmljZS4NCkJ1dCB0aGV5IGRpZG4ndCBoYXZlIEljZSBDdWJlDQpTbyBoZSBib3VnaHQg" \
           "VmFuaWxsYSBJY2UuDQpOb3cgY3J1aXNpbmcgaW4gaGlzIFBpbnRvLCBoZSBzZWVzIGhvbWllcyBhcyBoZSBwYXNzLg0KQnV0IGlmIGhl" \
           "IGxvb2tzIHR3aWNlDQpUaGV5J3JlIGdvbm5hIGtpY2sgaGlzIGxpbHkgYXNzLg0KDQpTbyBkb24ndCBkZWJhdGUsIGEgcGxheWVyIHN0" \
           "cmFpZ2h0DQpZb3Uga25vdyBoZSByZWFsbHkgZG9lc24ndCBnZXQgaXQgYW55d2F5Lg0KSGUncyBnb25uYSBwbGF5IHRoZSBmaWVsZCwg" \
           "YW5kIGtlZXAgaXQgcmVhbC4NCkZvciB5b3Ugbm8gd2F5LCBmb3IgeW91IG5vIHdheS4NClNvIGlmIHlvdSBkb24ndCByYXRlLCBqdXN0" \
           "IG92ZXJjb21wZW5zYXRlLg0KQXQgbGVhc3QgeW91J2xsIGtub3cgeW91IGNhbiBhbHdheXMgZ28gb24gUmlja2kgTGFrZS4NClRoZSB3" \
           "b3JsZCBsb3ZlcyB3YW5uYWJlJ3MuDQpTbyAoSGV5ISBIZXkhKSBkbyB0aGF0IGJyYW5kIG5ldyB0aGluZw0KDQpOb3cgaGUncyBnZXR0" \
           "aW5nIGEgdGF0dG9vLg0KWWVhaCBoZSdzIGdldHRpbicgaW5rIGRvbmUuDQpIZSBhc2tlZCBmb3IgYSAnMTMnLCBidXQgdGhleSBkcmV3" \
           "IGEgJzMxJy4NCkZyaWVuZHMgc2F5IGhlJ3MgdHJ5aW5nIHRvbyBoYXJkDQpBbmQgaGUncyBub3QgcXVpdGUgaGlwLg0KQnV0IGluIGhp" \
           "cyBvd24gbWluZA0KSGUncyB0aGUgZG9wZXN0IHRyaXAuDQoNCkdpdmUgaXQgdG8gbWUgYmFieS4gVWgtaHVoLiBVaC1odWguDQpHaXZl" \
           "IGl0IHRvIG1lIGJhYnkuIFVoLWh1aC4gVWgtaHVoLg0KR2l2ZSBpdCB0byBtZSBiYWJ5LiBVaC1odWguIFVoLWh1aC4NClVubywgZG9z" \
           "LCB0cmVzLCBjdWF0cm8sIGNpbmNvLCBjaW5jbywgc2Vpcy4=".decode('base64')
    message = raw_input("Enter some stuff to encrypt: ")+msg2
    while (len(message) % 16) != 0:
        message = message+'\x00'
    aes = AES.new(key, AES.MODE_ECB)
    return aes.encrypt(message).encode('hex')

#~~~~~~~~~~~~~~~~~~~~DO NOT EDIT ABOVE THIS LINE~~~~~~~~~~~~~~~~~~~


ui = ""
while ui != "!q" :
    enc = encrypt(key)
    spaced = [enc[i:i+32] for i in range(0,len(enc),32)]
    print "Encrypted spaced version: ", spaced, '\n'
    print "Encrypted version: ", enc, '\n'
    print "Length of ciphertext: ",  len(enc)/2
    ui = raw_input("Type !q to quit: ")
