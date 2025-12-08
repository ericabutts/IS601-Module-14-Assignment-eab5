from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, schemas
from app.database import get_db
from app.calculation_factory import perform_calculation
from app.auth import get_current_user

router = APIRouter(prefix="/calculations", tags=["calculations"])


# ---------------------------------------------------------
# CREATE (Add)
# ---------------------------------------------------------
@router.post("/", response_model=schemas.CalculationRead)
def create_calculation(
    calc: schemas.CalculationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # calc.type is already uppercase from the Pydantic validator
    result = perform_calculation(calc.a, calc.b, calc.type)

    db_calc = models.Calculation(
        a=calc.a,
        b=calc.b,
        type=calc.type,   # store uppercase internally
        result=result,
        user_id=current_user.id
    )
    db.add(db_calc)
    db.commit()
    db.refresh(db_calc)
    return db_calc


# ---------------------------------------------------------
# BROWSE (Get all user’s calculations)
# ---------------------------------------------------------
@router.get("/user/{user_id}", response_model=List[schemas.CalculationRead])
def get_user_calculations(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    return db.query(models.Calculation).filter(models.Calculation.user_id == user_id).all()


# ---------------------------------------------------------
# READ (Get a single calculation)
# ---------------------------------------------------------
@router.get("/{calculation_id}", response_model=schemas.CalculationRead)
def get_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    calc = db.query(models.Calculation).filter(models.Calculation.id == calculation_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    if calc.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    return calc


# ---------------------------------------------------------
# EDIT (Update a calculation)
# ---------------------------------------------------------
@router.put("/{calculation_id}", response_model=schemas.CalculationRead)
def update_calculation(
    calculation_id: int,
    updates: schemas.CalculationUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    calc = db.query(models.Calculation).filter(models.Calculation.id == calculation_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    if calc.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    # Only update provided fields
    if updates.a is not None:
        calc.a = updates.a
    if updates.b is not None:
        calc.b = updates.b
    if updates.type is not None:
        calc.type = updates.type  # already uppercase from Pydantic validator

    # Recalculate result
    calc.result = perform_calculation(calc.a, calc.b, calc.type)

    db.commit()
    db.refresh(calc)
    return calc


# ---------------------------------------------------------
# DELETE
# ---------------------------------------------------------
@router.delete("/{calculation_id}", status_code=204)
def delete_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    calc = db.query(models.Calculation).filter(models.Calculation.id == calculation_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    if calc.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(calc)
    db.commit()
    return None
