# smithsonian-ocr

Demo to more efficiently transcribe documents by leveraging OCR.

Frontend is hosted on Netlify. Backend is currently being hosted on Digital Ocean.

To get back the hOCR format/transcription of the image, you can hit the following endpoint: http://157.230.218.186:5000/get-hOCR/<id>, where <id> is the id of the particular document you are trying to transcribe. For example, if the image I'd like to transcribe is https://transcription.si.edu/view/24154/NASM-NASM.XXXX.0450-M0000244-00090, then I would use the last reference page as the id argument (NASM-NASM.XXXX.0450-M0000244-00090).
  
  
