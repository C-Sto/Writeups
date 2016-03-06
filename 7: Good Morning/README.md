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