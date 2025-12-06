import random
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. CORE LOGIC (The "Meta-System" Engine) ---

class NumeralSystem:
    def __init__(self, id, name, base, logic, symbol_map, zero_symbol=None, digit_renderer=None):
        self.id = id
        self.name = name
        self.base = base
        self.logic = logic  # 'additive' or 'positional'
        # Ensure map keys are integers
        self.symbol_map = {int(k): v for k, v in symbol_map.items()} 
        self.zero_symbol = zero_symbol
        self.digit_renderer = digit_renderer

# Database of Systems
SYSTEM_DB = {
    "roman": NumeralSystem("roman", "Roman Numerals", 10, "additive", 
                           {1000: 'M', 900: 'CM', 500: 'D', 400: 'CD', 100: 'C', 90: 'XC', 50: 'L', 40: 'XL', 10: 'X', 9: 'IX', 5: 'V', 4: 'IV', 1: 'I'}),
    "mayan": NumeralSystem("mayan", "Mayan Numerals", 20, "positional", {}, zero_symbol="Θ", digit_renderer="mayan"),
    "babylonian": NumeralSystem("babylonian", "Babylonian", 60, "positional", {}, zero_symbol="Empty", digit_renderer="cuneiform"),
}

class Transpiler:
    @staticmethod
    def to_system(number: int, system_id: str):
        sys = SYSTEM_DB.get(system_id)
        if not sys:
            return {"error": "System not found"}
            
        if number == 0:
            return {
                "result": sys.zero_symbol if sys.zero_symbol else "N/A", 
                "steps": ["Value is 0."] if sys.zero_symbol else ["System has no concept of zero."]
            }

        if sys.logic == "additive":
            return Transpiler._convert_additive(number, sys)
        elif sys.logic == "positional":
            return Transpiler._convert_positional(number, sys)

    @staticmethod
    def _convert_additive(number, sys):
        steps = []
        result = ""
        n = number
        # Sort descending
        for value in sorted(sys.symbol_map.keys(), reverse=True):
            symbol = sys.symbol_map[value]
            while n >= value:
                result += symbol
                n -= value
                steps.append(f"Add {symbol} ({value}). Remaining: {n}")
        return {"result": result, "steps": steps, "is_positional": False}

    @staticmethod
    def _convert_positional(number, sys):
        steps = []
        digits = []
        n = number
        
        # Simple decomposition for positional
        while n > 0:
            remainder = n % sys.base
            digits.insert(0, remainder)
            steps.append(f"Extracted digit {remainder} (Value: {remainder} * {sys.base}^x)")
            n //= sys.base
        
        # If result is empty (input was 0 handled above, but just in case)
        if not digits: digits = [0]
            
        steps.reverse() # Logical order
        return {"result": digits, "steps": steps, "is_positional": True, "renderer": sys.digit_renderer}

class PuzzleGenerator:
    @staticmethod
    def generate(system_id: str):
        sys = SYSTEM_DB.get(system_id)
        if not sys: return {}
        
        type_ = random.choice(["conversion", "sequence"])
        
        if type_ == "conversion":
            target = random.randint(1, 50)
            conversion = Transpiler.to_system(target, system_id)
            return {
                "type": "conversion",
                "question": f"Convert the number {target} into {sys.name}.",
                "target": target,
                "answer_display": conversion['result'],
                "hint": f"This is a Base-{sys.base} system."
            }
        else:
            start = random.randint(1, 15)
            step = random.randint(1, 3)
            seq = [start, start + step, start + 2*step]
            # Convert sequence to system format for display
            seq_display = []
            for num in seq:
                res = Transpiler.to_system(num, system_id)
                val = res['result']
                # Format for text display
                if isinstance(val, list): val = f"[{', '.join(map(str, val))}]"
                seq_display.append(val)
                
            return {
                "type": "sequence",
                "question": f"Find the next number: {', '.join(seq_display)}, ...",
                "target": start + 3*step,
                "answer_display": str(Transpiler.to_system(start + 3*step, system_id)['result']),
                "hint": f"The sequence increases by {step}."
            }

# --- 2. API ENDPOINTS ---

class ConvertRequest(BaseModel):
    number: int
    system_id: str

@app.get("/systems")
def get_systems():
    """Return list of available systems for the frontend dropdown."""
    return [{"id": k, "name": v.name, "base": v.base} for k, v in SYSTEM_DB.items()]

@app.post("/convert")
def convert_number(req: ConvertRequest):
    """Convert Arabic number to target system."""
    return Transpiler.to_system(req.number, req.system_id)

@app.get("/puzzle/{system_id}")
def get_puzzle(system_id: str):
    """Generate a random puzzle."""
    return PuzzleGenerator.generate(system_id)

# --- 3. SERVE STATIC FILES (The Frontend) ---
app.mount("/", StaticFiles(directory="static", html=True), name="static")