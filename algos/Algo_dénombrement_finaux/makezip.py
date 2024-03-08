import zipfile as zf

cz = zf.ZipFile("champion.zip", "w", zf.ZIP_DEFLATED)
cz.write("champion.c")
cz.write("interface.cc")
cz.write("calcul_score.h")
cz.write("calcul_score.c")
cz.write("api.h")
cz.write("_lang")
cz.close()
print("OK")
