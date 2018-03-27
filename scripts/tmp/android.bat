set PATH=h:\sdk\depot_tools\;%PATH%
rmdir %SharedTecINT% /s /q
toolchain\python\python.exe build_boost_android.py
toolchain\python\python.exe build_android.py