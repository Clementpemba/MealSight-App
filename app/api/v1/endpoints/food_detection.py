from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
from pathlib import Path
from typing import List, Dict, Any
import uuid
import os

# Import your existing model.py function
from app.ai.model import detect_food

router = APIRouter()

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Nutrition database
FOOD_NUTRITION = {
    "Meat": {"calories": 250, "protein": 26, "carbs": 0, "fat": 17, "fiber": 0},
    "Nsima": {"calories": 180, "protein": 3, "carbs": 42, "fat": 1, "fiber": 2},
    "vegetables": {"calories": 65, "protein": 2, "carbs": 13, "fat": 0.5, "fiber": 4},
    "vegetable": {"calories": 65, "protein": 2, "carbs": 13, "fat": 0.5, "fiber": 4},
    "Rice": {"calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3, "fiber": 0.4},
    "Beans": {"calories": 120, "protein": 8, "carbs": 22, "fat": 0.5, "fiber": 6},
    "Fish": {"calories": 206, "protein": 22, "carbs": 0, "fat": 12, "fiber": 0},
    "Egg": {"calories": 155, "protein": 13, "carbs": 1.1, "fat": 11, "fiber": 0},
    "Chicken": {"calories": 239, "protein": 27, "carbs": 0, "fat": 14, "fiber": 0},
    "Bread": {"calories": 265, "protein": 9, "carbs": 49, "fat": 3.2, "fiber": 2},
    "Pasta": {"calories": 131, "protein": 5, "carbs": 25, "fat": 1.1, "fiber": 1.2},
    "Fruit": {"calories": 80, "protein": 0.5, "carbs": 20, "fat": 0.2, "fiber": 3},
    "default": {"calories": 150, "protein": 5, "carbs": 20, "fat": 5, "fiber": 2}
}

def generate_ai_feedback(detected_foods: List[str], nutrition_summary: Dict) -> Dict:
    """Generate AI feedback based on detected foods and nutrition"""
    total_calories = nutrition_summary.get("total_calories", 0)
    total_protein = nutrition_summary.get("total_protein", 0)
    total_carbs = nutrition_summary.get("total_carbs", 0)
    total_fat = nutrition_summary.get("total_fat", 0)
    total_fiber = nutrition_summary.get("total_fiber", 0)
    
    # Calculate balance score
    balance_score = 100
    
    if total_protein < 15:
        balance_score -= 15
    elif total_protein > 45:
        balance_score -= 5
    
    if total_carbs < 20:
        balance_score -= 10
    elif total_carbs > 80:
        balance_score -= 10
    
    if total_fat < 8:
        balance_score -= 10
    elif total_fat > 35:
        balance_score -= 10
    
    if total_calories < 300:
        balance_score -= 10
    elif total_calories > 900:
        balance_score -= 10
    
    if len(detected_foods) >= 3:
        balance_score += 10
    elif len(detected_foods) >= 2:
        balance_score += 5
    
    balance_score = max(0, min(100, balance_score))
    
    # Rating
    if balance_score >= 80:
        rating = "Excellent"
        rating_emoji = "🌟"
    elif balance_score >= 65:
        rating = "Good"
        rating_emoji = "👍"
    elif balance_score >= 50:
        rating = "Fair"
        rating_emoji = "📊"
    else:
        rating = "Needs Improvement"
        rating_emoji = "⚠️"
    
    # Generate insights
    insights = []
    recommendations = []
    
    if total_protein < 15:
        insights.append(f"Low protein ({total_protein}g). Protein helps muscle health and keeps you full.")
        recommendations.append("Add beans, eggs, fish, or lean meat to boost protein.")
    
    if total_carbs > 70:
        insights.append(f"High carbohydrates ({total_carbs}g). Great for energy, but balance with protein.")
    
    # Check for vegetables
    has_veggies = any(v.lower() in ['vegetables', 'vegetable', 'fruit'] for v in detected_foods)
    if has_veggies:
        insights.append("Great job including vegetables! They provide essential vitamins and fiber.")
    elif len(detected_foods) > 0:
        insights.append("No vegetables detected in this meal.")
        recommendations.append("Add colorful vegetables like greens, carrots, or tomatoes.")
    
    if total_fiber > 5:
        insights.append(f"Good fiber content ({total_fiber}g). Fiber aids digestion and heart health.")
    
    if total_fat > 30:
        recommendations.append("Try grilling, steaming, or baking instead of frying.")
    
    if len(detected_foods) == 1:
        insights.append("Single food item detected. Variety is key for complete nutrition.")
        recommendations.append("Combine different food groups: protein + carbs + vegetables.")
    elif len(detected_foods) >= 3:
        insights.append(f"Good variety! {len(detected_foods)} different foods detected.")
    
    # Summary
    if balance_score >= 80:
        summary = f"{rating_emoji} {rating}! This is a well-balanced meal with good nutrient distribution. Keep up the healthy eating habits!"
    elif balance_score >= 65:
        summary = f"{rating_emoji} {rating} meal. Overall balanced with minor adjustments for optimal nutrition."
    elif balance_score >= 50:
        summary = f"{rating_emoji} {rating} meal. A few improvements could make this more nutritious."
    else:
        summary = f"{rating_emoji} {rating}. This meal could benefit from better balance across food groups."
    
    # Pro tip
    nutritional_tip = "🥗 Fill half your plate with vegetables for optimal micronutrients."
    if has_veggies:
        nutritional_tip = "🥬 Dark leafy greens are rich in iron and calcium - excellent choice!"
    
    return {
        "rating": rating,
        "balance_score": balance_score,
        "summary": summary,
        "insights": insights[:3],
        "recommendations": recommendations[:2],
        "nutritional_tip": nutritional_tip
    }


@router.post("/detect-food")
async def detect_food_api(image: UploadFile = File(...)):
    """
    Detect food from uploaded image and return nutrition analysis with AI feedback
    """
    try:
        # Save uploaded image
        file_extension = Path(image.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        print(f"📁 Image saved: {file_path}")
        
        # Call YOUR model.py detect_food function
        detected_items = detect_food(str(file_path))
        print(f"🔍 Raw detection from model.py: {detected_items}")
        
        # Extract food names from the list of dictionaries
        detected_foods = []
        for item in detected_items:
            food_name = item.get("food", "")
            confidence = item.get("confidence", 0)
            if food_name and confidence > 0.3:  # Filter low confidence
                detected_foods.append(food_name)
                print(f"   ✅ {food_name} (confidence: {confidence})")
        
        # Remove duplicates while preserving order
        unique_foods = []
        for food in detected_foods:
            if food not in unique_foods:
                unique_foods.append(food)
        detected_foods = unique_foods
        
        # If nothing detected, return helpful message
        if not detected_foods:
            detected_foods = ["Unknown food item"]
            print("⚠️ No foods detected with sufficient confidence")
        
        print(f"🍽️ Final detected foods: {detected_foods}")
        
        # Build nutrition breakdown
        nutrition_breakdown = []
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        total_fiber = 0
        
        for food_name in detected_foods:
            # Find matching nutrition data (case-insensitive)
            nutrition_data = None
            for key in FOOD_NUTRITION:
                if key.lower() == food_name.lower():
                    nutrition_data = FOOD_NUTRITION[key]
                    break
            
            if nutrition_data is None:
                nutrition_data = FOOD_NUTRITION["default"]
                food_name = f"{food_name} (estimated)"
            
            total_calories += nutrition_data["calories"]
            total_protein += nutrition_data["protein"]
            total_carbs += nutrition_data["carbs"]
            total_fat += nutrition_data["fat"]
            total_fiber += nutrition_data.get("fiber", 2)
            
            nutrition_breakdown.append({
                "food": food_name,
                "nutrition": {
                    "calories": nutrition_data["calories"],
                    "protein": nutrition_data["protein"],
                    "carbs": nutrition_data["carbs"],
                    "fat": nutrition_data["fat"],
                    "fiber": nutrition_data.get("fiber", 2)
                }
            })
        
        nutrition_summary = {
            "total_calories": total_calories,
            "total_protein": total_protein,
            "total_carbs": total_carbs,
            "total_fat": total_fat,
            "total_fiber": total_fiber
        }
        
        # Generate AI feedback
        ai_feedback = generate_ai_feedback(detected_foods, nutrition_summary)
        
        # Return response
        response_data = {
            "detected_foods": detected_foods,
            "nutrition": nutrition_breakdown,
            "summary": nutrition_summary,
            "ai_feedback": ai_feedback
        }
        
        print(f"✅ Success! Returning analysis for {len(detected_foods)} foods")
        return response_data
        
    except Exception as e:
        print(f"❌ Error in detect_food_api: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Food detection failed: {str(e)}")


@router.get("/nutrition-info")
async def get_nutrition_info():
    """Get all available nutrition data"""
    return FOOD_NUTRITION