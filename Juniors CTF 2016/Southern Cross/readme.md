## Task Text

### Southern Cross

- Wow, what's this, Soos?
- It's the Confederacy's cipher disk with a help of which southerners encrypted their messages.
- How does it work?
- Look, Dipper. We need to encode the phrase MABLE EATS SPRINKLES. We don't need any spaces so just delete them. We get MABLEEATSSPRINKLES. Then we have too choose a key. Let it be GRAVITY. And let's go !!!


You see, we've encrypted the phrase and here it is RBZTXYZJSKZBLQCEN
- Cool!
- Now I'll encode a famous story and you'll try to decode it. By the way, it's much more interesting to read the whole story over, isn't it?
....
- That's complicated. Maybe I have to find a key at first. I'd better look for someone who is able to solve this...
- Don't forget to reach to the end of the text! The ending is greatly important.

Turn left Turn right

M. Iu. Lupanov, K. A. Koliado, S. A. Kostiuchenkov

## Solution

It's a simple cipher - all we need to do is find a word that decodes the text to english looking text. See attached python file for the script that will try to crack the code `crack.py`

Once the text is english and readable (takes a minute or two using rockyou.txt), we take the last few words and submit as flag... profit!