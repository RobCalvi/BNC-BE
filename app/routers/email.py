# routers/email.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.email import Email
from app.services.email import EmailService
from .dependencies import get_email_service
from app.db import MongoClient, get_mongo_client
from fastapi.responses import FileResponse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64
from pathlib import Path
from models.email import EmlRequest


router = APIRouter(prefix="/emails", tags=["emails"])

@router.post("/", response_model=Email)
async def create_email(email: Email, service: EmailService = Depends(get_email_service), client: MongoClient = Depends(get_mongo_client)):
    return await service.create_email(client, email)

@router.get("/", response_model=List[Email])
async def list_emails(skip: int = 0, limit: int = 10, service: EmailService = Depends(get_email_service), client: MongoClient = Depends(get_mongo_client)):
    return await service.list_emails(client, skip, limit)

@router.get("/{email_id}", response_model=Email)
async def get_email(email_id: str, service: EmailService = Depends(get_email_service), client: MongoClient = Depends(get_mongo_client)):
    email = await service.get_email(client, email_id)
    if email is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
    return email

@router.patch("/{email_id}", response_model=Email)
async def update_email(email_id: str, updates: dict, service: EmailService = Depends(get_email_service), client: MongoClient = Depends(get_mongo_client)):
    updated = await service.update_email(client, email_id, updates)
    if not updated:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not update email.")
    return await service.get_email(client, email_id)

@router.delete("/{email_id}", response_model=dict)
async def delete_email(email_id: str, service: EmailService = Depends(get_email_service), client: MongoClient = Depends(get_mongo_client)):
    deleted = await service.delete_email(client, email_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
    return {"message": "Email deleted successfully"}

@router.get("/company/{company_id}", response_model=List[Email])
async def get_emails_by_company_id(
    company_id: str,
    skip: int = 0,
    limit: int = 10,
    service: EmailService = Depends(get_email_service),
    client: MongoClient = Depends(get_mongo_client)
):
    emails = await service.get_emails_by_company_id(client, company_id, skip, limit)
    return emails

@router.post("/generate-eml/")
async def generate_eml(request: EmlRequest):
    try:
        print("Received payload:", request)  # Log payload
        # Extract request data
        subject = request.subject
        to_email = request.to_email
        html_body = request.html_body
        images = request.images

        # Debug print image base64 data
        print(f"Number of images: {len(images)}")
        for idx, image in enumerate(images):
            print(f"Image {idx}: {image[:30]}...")  # Print the first 30 characters of the base64 string

        # Existing logic
        msg = MIMEMultipart("related")
        msg["Subject"] = subject
        msg["To"] = to_email
        msg["From"] = "sender@example.com"

        # Add HTML content
        html_content = MIMEText(html_body, "html")
        msg.attach(html_content)

        # Attach inline images
        for idx, image_base64 in enumerate(images):
            try:
                img_data = base64.b64decode(image_base64)
                mime_img = MIMEImage(img_data)
                mime_img.add_header("Content-ID", f"<image{idx}>")
                mime_img.add_header("Content-Disposition", "inline", filename=f"image{idx}.png")
                msg.attach(mime_img)
            except Exception as e:
                print(f"Error decoding image {idx}: {e}")
                raise HTTPException(status_code=400, detail=f"Invalid image data at index {idx}")

        # Write the .eml file
        eml_path = Path("output_email.eml")
        with eml_path.open("wb") as f:
            f.write(msg.as_bytes())

        print("EML file generated successfully.")
        return FileResponse(eml_path, filename="generated_email.eml")

    except Exception as e:
        print(f"Error generating EML: {e}")
        raise HTTPException(status_code=500, detail=str(e))
