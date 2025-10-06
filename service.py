from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import io
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter

app = FastAPI(title="Rechenaufgaben PDF Generator Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://www.grundschullottchen.de/", # TODO: This should be in some form of config file
    ],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/generate-math-tasks")
def get_pdf(operators: List[str] = Query(["+"])):
    template_path = os.path.join(os.path.dirname(__file__), "template.pdf") 
    if not os.path.exists(template_path):
        return JSONResponse({"error": "Template not found"}, status_code=404)

    packet = io.BytesIO()
    c = canvas.Canvas(packet)
    c.setFont("Helvetica", 14) # TODO: Check which font should be used
    
    # TODO: Generate and Write Tasks    
    c.save()

    packet.seek(0)
    new_pdf = PdfReader(packet)

    existing_pdf = PdfReader(open(template_path, "rb"))
    output = PdfWriter()

    # TODO: Extend Option for multiple Pages of Files
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    output_path = f"/tmp/{name}_{thema}.pdf"
    with open(output_path, "wb") as f_out:
        output.write(f_out)

    return FileResponse(output_path, media_type="application/pdf", filename=f"{name}_{thema}.pdf")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("pdf_service:app", host="0.0.0.0", port=8000, reload=True)
