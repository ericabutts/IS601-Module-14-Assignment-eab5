# routes/calculations.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db
from app.calculation_factory import perform_calculation
from app.auth import get_current_user

router = APIRouter(prefix="/calculations", tags=["calculations"])


# ---------------------------------------------------------
# CREATE (Add)
# ---------------------------------------------------------
# POST /calculations
@router.post("/", response_model=schemas.CalculationRead)
def create_calculation(
    calc: schemas.CalculationCreate,  
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Convert enum to uppercase string
    operation_type = calc.type.value.upper()  # <-- key change
    result = perform_calculation(calc.a, calc.b, operation_type)  

    db_calc = models.Calculation(
        a=calc.a,
        b=calc.b,
        type=operation_type,   # store uppercase internally
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
    """Get all calculations for the logged-in user"""
    
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    return (
        db.query(models.Calculation)
        .filter(models.Calculation.user_id == user_id)
        .all()
    )


# ---------------------------------------------------------
# READ (Get a single calculation)
# ---------------------------------------------------------
@router.get("/{calculation_id}", response_model=schemas.CalculationRead)
def get_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    calc = db.query(models.Calculation).filter(
        models.Calculation.id == calculation_id
    ).first()

    if not calc:
        raise HTTPException(404, "Calculation not found")

    if calc.user_id != current_user.id:
        raise HTTPException(403, "Not allowed")

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
    calc = db.query(models.Calculation).filter(
        models.Calculation.id == calculation_id
    ).first()

    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    if calc.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    # Update fields
    calc.a = updates.a
    calc.b = updates.b
    calc.type = updates.type

    # Recalculate result
    calc.result = perform_calculation(
        calc.a,
        calc.b,
        calc.type.value
    )

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
    calc = db.query(models.Calculation).filter(
        models.Calculation.id == calculation_id
    ).first()

    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    if calc.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(calc)
    db.commit()
    return None
