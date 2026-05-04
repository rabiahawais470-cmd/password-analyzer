Password Analyzer — EXE build & run

Files produced
- dist/password-analyzer.exe
- dist/password-analyzer-win.zip

Run the EXE
- In PowerShell or CMD from the project root:

```powershell
.\dist\password-analyzer.exe
```

Open the app in a browser:

http://127.0.0.1:5000

Rebuild the EXE (if you need to reproduce)
- From the project root run:

```powershell
pyinstaller --onefile --add-data "templates;templates" --add-data "static;static" --name password-analyzer app.py
```

Notes
- The EXE runs the Flask development server (debug mode). For production, run behind a WSGI server.
