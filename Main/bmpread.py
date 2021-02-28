

def BmpRead(f):
    ### BMPファイルヘッダ ###
    bfType         = f.read(2)
    bfSize         = f.read(4)
    bfReserved1    = f.read(2)
    bfReserved2    = f.read(2)
    bfOffBitsbfOffBits = f.read(4)


    ### BMPファイルヘッダ ###
    bfType         = f.read(2)
    bfSize         = f.read(4)
    bfReserved1    = f.read(2)
    bfReserved2    = f.read(2)
    bfOffBitsbfOffBits = f.read(4)

    ### 情報ヘッダ ###
    bcSize         = f.read(4)
    bcWidth        = f.read(4)
    bcHeight       = f.read(4)
    bcPlanes       = f.read(2)
    bcBitCount     = f.read(2)
    biCompression  = f.read(4)
    biSizeImage    = f.read(4)
    biXPixPerMeter = f.read(4)
    biYPixPerMeter = f.read(4)
    biClrUsed      = f.read(4)
    biCirImportant = f.read(4)


    with f:
        data = f.read()
        textEdit.setText(data)