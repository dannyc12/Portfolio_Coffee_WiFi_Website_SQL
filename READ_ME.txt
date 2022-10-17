**IMPORTANT VERSION CONTROL**
'requirements.txt' took a TON of troubleshooting to make the app run appropriately. Different versions of plugins
created different problems, and required other upgrading/downgrading other plugin versions.

ALSO,
If you try to run database methods inside your code (not inside a function) with app.run(debug=True), your methods
will run twice. It runs once, detects a change in the database, and will run again, throwing an error for
entries not found or entries duplicated

