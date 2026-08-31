import os
import uuid

from fastapi import UploadFile, HTTPException, status

from backend.app.db.repositories.candidate_repository import (
    get_candidate_profile,
    update_resume_parsed_data,
    clear_resume_data,
)

from backend.app.services.resume_parser import parse_resume

from backend.app.services.s3_service import (
    upload_file_to_s3,
    delete_file_from_s3,
)
from backend.app.services.resume_extractor import (
    extract_pdf_text,
    extract_docx_text,
)


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def upload_resume_service(
    user_id: str,
    file: UploadFile,
):

    candidate = get_candidate_profile(user_id)

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found.",
        )

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File name is required.",
        )

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and DOCX resumes are supported.",
        )

    file_bytes = file.file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume must be smaller than 5 MB.",
        )

    # --------------------------------------------------------
    # Save old S3 key before replacing resume
    # --------------------------------------------------------

    old_resume_key = candidate.get(
        "resume_s3_key"
    )

    # --------------------------------------------------------
    # Generate new S3 key
    # --------------------------------------------------------

    file_id = uuid.uuid4()

    s3_key = (
        f"resumes/{user_id}/{file_id}{extension}"
    )

    # --------------------------------------------------------
    # Upload to S3
    # --------------------------------------------------------

    upload_file_to_s3(
        file_bytes=file_bytes,
        s3_key=s3_key,
        content_type=file.content_type,
    )

    try:

        # ----------------------------------------------------
        # Extract text
        # ----------------------------------------------------

        resume_text = extract_resume_text(
            file_bytes,
            extension,
        )

        # ----------------------------------------------------
        # Parse resume
        # ----------------------------------------------------

        parsed = parse_resume(
            resume_text
        )

        # ----------------------------------------------------
        # Save parsed data + S3 key
        # ----------------------------------------------------

        updated_candidate = update_resume_parsed_data(
            user_id=user_id,
            resume_s3_key=s3_key,
            resume_text=resume_text,
            parsed_role=parsed.candidate_role,
            parsed_skills=parsed.candidate_skills,
            parsed_experience=parsed.candidate_experience,
        )

        if not updated_candidate:
            raise Exception(
                "Failed to update candidate profile."
            )

    except Exception:

        # New upload failed → remove it
        delete_file_from_s3(
            s3_key
        )

        raise

    # --------------------------------------------------------
    # New resume successfully saved
    # Delete old resume
    # --------------------------------------------------------

    if old_resume_key:
        delete_file_from_s3(
            old_resume_key
        )

    return {
        "message": "Resume uploaded and parsed successfully.",
        "resume_key": s3_key,
        "parsed_resume": parsed.model_dump(),
    }


def delete_resume_service(
    user_id: str,
):

    candidate = get_candidate_profile(user_id)

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found.",
        )

    resume_key = candidate.get(
        "resume_s3_key"
    )

    if not resume_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found.",
        )

    # Delete S3 object
    delete_file_from_s3(
        resume_key
    )

    # Clear DB fields
    updated = clear_resume_data(
        user_id
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear resume data.",
        )

    return {
        "message": "Resume deleted successfully."
    }


def extract_resume_text(
    file_bytes: bytes,
    extension: str,
):

    if extension == ".pdf":
        return extract_pdf_text(file_bytes)

    if extension == ".docx":
        return extract_docx_text(file_bytes)

    raise ValueError(
        "Unsupported resume format."
    )