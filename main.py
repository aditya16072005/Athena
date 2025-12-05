import React, { useState, useEffect, useMemo } from 'react';
import { Book, Calculator, Brain, ArrowRight, RefreshCw, ChevronRight, Info, Globe, ScrollText, Check, X } from 'lucide-react';

/**
 * --- META-SYSTEM ARCHITECTURE (The "Backend" Logic) ---
 * This configuration acts as the database and logic controller.
 * Instead of hardcoding "Roman Logic", we define parameters.
 */
const SYSTEM_DB = {
  roman: {
    id: 'roman',
    name: 'Roman Numerals',
    region: 'Ancient Rome',
    base: 10,
    logic: 'additive', // Additive systems sum up symbols (e.g., X + I + I = XII)
    zero: null, // Romans had no zero
    symbols: { 1000: 'M', 900: 'CM', 500: 'D', 400: 'CD', 100: 'C', 90: 'XC', 50: 'L', 40: 'XL', 10: 'X', 9: 'IX', 5: 'V', 4: 'IV', 1: 'I' },
    desc: "A system based on additive and subtractive principles using letters from the Latin alphabet.",
    color: "bg-red-900"
  },
  mayan: {
    id: 'mayan',
    name: 'Mayan Numerals',
    region: 'Mesoamerica',
    base: 20,
    logic: 'positional', // Positional systems use place value (like 1s, 10s, 100s, but here 1s, 20s, 400s)
    layout: 'vertical', // Mayan numbers are stacked vertically
    zero: 'Θ', // Shell symbol
    digitRenderer: 'mayan', // Special flag to render dots/bars dynamically
    desc: "A vigesimal (base-20) positional notation used by the Maya civilization, employing a shell for zero.",
    color: "bg-emerald-900"
  },
  babylonian: {
    id: 'babylonian',
    name: 'Babylonian Cuneiform',
    region: 'Mesopotamia',
    base: 60,
    logic: 'positional',
    layout: 'horizontal',
    zero: 'Empty Space', 
    digitRenderer: 'cuneiform', // Special renderer for wedges
    desc: "A sexagesimal (base-60) system. The first known positional numeral system, using a stylus to press wedges into clay.",
    color: "bg-yellow-900"
  },
  binary: {
    id: 'binary',
    name: 'Digital Binary',
    region: 'Modern Computing',
    base: 2,
    logic: 'positional',
    layout: 'horizontal',
    zero: '0',
    symbols: { 0: '0', 1: '1' },
    desc: "The base-2 system that underpins all modern digital computing.",
    color: "bg-slate-800"
  }
};

/**
 * --- THE TRANSPILER ENGINE ---
 * A universal converter that takes a Schema and an Input and produces an Output.
 */
const Engine = {
  toSystem: (number, systemId) => {
    const sys = SYSTEM_DB[systemId];
    if (!sys) return { result: '?', steps: [] };
    
    if (number === 0 && sys.zero) return { result: sys.zero, steps: ['Value is 0, returning zero symbol.'] };
    if (number === 0 && !sys.zero) return { result: 'N/A', steps: ['This system does not have a concept of Zero.'] };

    if (sys.logic === 'additive') {
      return Engine.convertAdditive(number, sys);
    } else if (sys.logic === 'positional') {
      return Engine.convertPositional(number, sys);
    }
  },

  convertAdditive: (num, sys) => {
    let n = num;
    let result = "";
    let steps = [];
    
    // Sort symbols descending
    const sortedValues = Object.keys(sys.symbols).map(Number).sort((a, b) => b - a);

    for (let val of sortedValues) {
      while (n >= val) {
        result += sys.symbols[val];
        n -= val;
        steps.push(`Add ${sys.symbols[val]} (${val}). Remaining: ${n}`);
      }
    }
    return { result, steps };
  },

  convertPositional: (num, sys) => {
    let n = num;
    let digits = [];
    let steps = [];

    // 1. Decompose into base powers
    let power = 0;
    while (Math.pow(sys.base, power + 1) <= n) {
      power++;
    }

    steps.push(`Highest power of ${sys.base} fitting in ${num} is ${sys.base}^${power}`);

    for (let p = power; p >= 0; p--) {
      const placeValue = Math.pow(sys.base, p);
      const digit = Math.floor(n / placeValue);
      n %= placeValue;
      digits.push(digit);
      steps.push(`Place ${sys.base}^${p} (${placeValue}): ${digit} units. Remainder: ${n}`);
    }

    return { result: digits, steps, isPositionalRaw: true };
  }
};

/**
 * --- PROCEDURAL PUZZLE GENERATOR ---
 * Infinite content generation based on the active system rules.
 */
const generatePuzzle = (systemId) => {
  const types = ['conversion', 'sequence'];
  const type = types[Math.floor(Math.random() * types.length)];
  const sys = SYSTEM_DB[systemId];
  
  if (type === 'conversion') {
    const target = Math.floor(Math.random() * 50) + 1;
    return {
      type: 'conversion',
      question: `Convert the number ${target} into ${sys.name}.`,
      target: target,
      answer: Engine.toSystem(target, systemId),
      hint: `Remember, this is a Base-${sys.base} system.`
    };
  } else {
    // Sequence Puzzle
    const start = Math.floor(Math.random() * 20) + 1;
    const step = Math.floor(Math.random() * 3) + 1;
    const seq = [start, start + step, start + (step * 2)];
    
    const renderedSeq = seq.map(n => {
        const out = Engine.toSystem(n, systemId);
        // Helper to format result for text display
        if(out.isPositionalRaw) {
             if (sys.digitRenderer === 'mayan') return `[${out.result.join(',')}]`;
             return out.result.join('-');
        }
        return out.result;
    });

    return {
      type: 'sequence',
      question: `Find the next number: ${renderedSeq.join(', ')}, ...`,
      target: start + (step * 3), // Internal numeric answer
      answer: Engine.toSystem(start + (step * 3), systemId),
      hint: `Identify the gap between the numbers. It seems to be increasing by ${step}.`
    };
  }
};


/**
 * --- UI COMPONENTS ---
 */

// Helper to render special glyphs (Mayan/Cuneiform)
const GlyphRenderer = ({ value, type }) => {
  if (type === 'mayan') {
    // Mayan: Bars (5) and Dots (1)
    const bars = Math.floor(value / 5);
    const dots = value % 5;
    return (
      <div className="flex flex-col items-center justify-center p-1 border border-stone-600 rounded bg-stone-100 min-w-[40px] shadow-sm">
        <div className="flex gap-1 mb-1">
          {Array(dots).fill(0).map((_, i) => (
            <div key={i} className="w-3 h-3 bg-black rounded-full"></div>
          ))}
        </div>
        <div className="flex flex-col gap-1">
          {Array(bars).fill(0).map((_, i) => (
            <div key={i} className="w-8 h-2 bg-black rounded-sm"></div>
          ))}
        </div>
        {value === 0 && <span className="text-xl">Θ</span>}
      </div>
    );
  }
  if (type === 'cuneiform') {
    // Simple visual approximation for Cuneiform using text characters for MVP
    // 10 is < (Pretend), 1 is Y
    const tens = Math.floor(value / 10);
    const ones = value % 10;
    return (
      <div className="flex gap-1 font-serif font-bold text-xl text-stone-800 p-1 border border-stone-400 bg-amber-50 rounded">
        {Array(tens).fill(0).map((_, i) => <span key={`t-${i}`}>&lt;</span>)}
        {Array(ones).fill(0).map((_, i) => <span key={`o-${i}`}>Y</span>)}
        {value === 0 && <span className="text-sm italic">space</span>}
      </div>
    );
  }
  return <span className="text-xl font-mono">{value}</span>;
};

// Component to display the result of the engine
const ResultDisplay = ({ output, system }) => {
  if (!output) return null;

  // Additive Systems (Roman)
  if (!output.isPositionalRaw) {
    return <div className="text-5xl font-serif text-slate-800 tracking-widest mt-4">{output.result}</div>;
  }

  // Positional Systems (Mayan, Babylonian)
  return (
    <div className={`flex ${system.layout === 'vertical' ? 'flex-col gap-2' : 'flex-row gap-4'} mt-4 items-center`}>
      {output.result.map((digit, idx) => (
        <div key={idx} className="flex flex-col items-center">
          <GlyphRenderer value={digit} type={system.digitRenderer} />
          <span className="text-xs text-slate-400 mt-1">{Math.pow(system.base, output.result.length - 1 - idx)}s place</span>
        </div>
      ))}
    </div>
  );
};

export default function AthenaApp() {
  const [activeTab, setActiveTab] = useState('explorer');
  const [activeSystemId, setActiveSystemId] = useState('roman');
  
  // Converter State
  const [inputNum, setInputNum] = useState(10);
  
  // Puzzle State
  const [currentPuzzle, setCurrentPuzzle] = useState(null);
  const [puzzleAnswer, setPuzzleAnswer] = useState('');
  const [puzzleFeedback, setPuzzleFeedback] = useState(null);

  const activeSystem = SYSTEM_DB[activeSystemId];
  const conversionResult = useMemo(() => Engine.toSystem(inputNum, activeSystemId), [inputNum, activeSystemId]);

  // Load a puzzle on mount or system change
  useEffect(() => {
    loadNewPuzzle();
  }, [activeSystemId]);

  const loadNewPuzzle = () => {
    setCurrentPuzzle(generatePuzzle(activeSystemId));
    setPuzzleAnswer('');
    setPuzzleFeedback(null);
  };

  const checkAnswer = () => {
    // Simple numeric check for MVP
    const userInt = parseInt(puzzleAnswer);
    if (!isNaN(userInt) && userInt === currentPuzzle.target) {
      setPuzzleFeedback('correct');
    } else {
      setPuzzleFeedback('incorrect');
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans flex flex-col md:flex-row">
      
      {/* SIDEBAR NAVIGATION */}
      <aside className="w-full md:w-64 bg-slate-900 text-slate-100 flex-shrink-0 flex flex-col">
        <div className="p-6 border-b border-slate-800">
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <Globe className="text-blue-400" /> ATHENA
          </h1>
          <p className="text-slate-400 text-xs mt-1">Numeral System Explorer</p>
        </div>

        <nav className="flex-1 p-4 space-y-2">
          <button 
            onClick={() => setActiveTab('explorer')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${activeTab === 'explorer' ? 'bg-blue-600 text-white' : 'hover:bg-slate-800 text-slate-300'}`}
          >
            <Book size={18} /> Library
          </button>
          <button 
             onClick={() => setActiveTab('converter')}
             className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${activeTab === 'converter' ? 'bg-blue-600 text-white' : 'hover:bg-slate-800 text-slate-300'}`}
          >
            <Calculator size={18} /> Transpiler
          </button>
          <button 
             onClick={() => setActiveTab('practice')}
             className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${activeTab === 'practice' ? 'bg-blue-600 text-white' : 'hover:bg-slate-800 text-slate-300'}`}
          >
            <Brain size={18} /> Olympiad Zone
          </button>
        </nav>

        <div className="p-4 border-t border-slate-800">
          <label className="text-xs text-slate-500 uppercase font-semibold tracking-wider">Active Civilization</label>
          <div className="grid grid-cols-2 gap-2 mt-2">
            {Object.values(SYSTEM_DB).map(sys => (
              <button 
                key={sys.id}
                onClick={() => setActiveSystemId(sys.id)}
                className={`text-xs p-2 rounded border transition-all ${activeSystemId === sys.id ? 'bg-blue-500/20 border-blue-500 text-blue-300' : 'border-slate-700 text-slate-400 hover:border-slate-500'}`}
              >
                {sys.name}
              </button>
            ))}
          </div>
        </div>
      </aside>

      {/* MAIN CONTENT AREA */}
      <main className="flex-1 overflow-y-auto">
        
        {/* HEADER */}
        <header className={`${activeSystem.color} text-white p-8 shadow-lg`}>
          <div className="max-w-4xl mx-auto">
            <h2 className="text-4xl font-serif mb-2">{activeSystem.name}</h2>
            <div className="flex items-center gap-4 text-white/80 text-sm">
              <span className="flex items-center gap-1"><Globe size={14}/> {activeSystem.region}</span>
              <span className="flex items-center gap-1"><ScrollText size={14}/> Base-{activeSystem.base}</span>
              <span className="uppercase tracking-wider px-2 py-0.5 bg-black/20 rounded">{activeSystem.logic}</span>
            </div>
          </div>
        </header>

        <div className="max-w-4xl mx-auto p-8">
          
          {/* VIEW: EXPLORER */}
          {activeTab === 'explorer' && (
            <div className="space-y-8 animate-fade-in">
              <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                <h3 className="text-xl font-bold text-slate-800 mb-4 flex items-center gap-2">
                  <Info className="text-blue-600"/> System Overview
                </h3>
                <p className="text-slate-600 leading-relaxed text-lg">
                  {activeSystem.desc}
                </p>
                <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-slate-50 p-4 rounded-lg">
                    <span className="block text-xs font-bold text-slate-400 uppercase">Logic Type</span>
                    <span className="text-slate-800 font-medium capitalize">{activeSystem.logic} Notation</span>
                  </div>
                  <div className="bg-slate-50 p-4 rounded-lg">
                    <span className="block text-xs font-bold text-slate-400 uppercase">Base (Radix)</span>
                    <span className="text-slate-800 font-medium">Base {activeSystem.base}</span>
                  </div>
                </div>
              </div>

              {/* Dynamic Symbol Table */}
              <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                <h3 className="text-xl font-bold text-slate-800 mb-4">Symbol Map</h3>
                {activeSystem.logic === 'additive' ? (
                  <div className="flex flex-wrap gap-4">
                    {Object.entries(activeSystem.symbols).sort((a,b) => b[0]-a[0]).map(([val, sym]) => (
                      <div key={val} className="flex flex-col items-center bg-slate-50 p-3 rounded-lg border border-slate-100 min-w-[80px]">
                        <span className="text-2xl font-serif text-slate-800">{sym}</span>
                        <span className="text-xs text-slate-500 font-mono mt-1">{val}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                   <div className="bg-slate-50 p-8 rounded-lg text-center border-dashed border-2 border-slate-200 text-slate-500">
                     <p>This is a positional system.</p>
                     <p className="text-sm mt-2">Values depend on their slot (e.g., {activeSystem.base}s place, 1s place).</p>
                     {activeSystem.digitRenderer === 'mayan' && <p className="mt-4 text-xs">Uses Dots (1) and Bars (5) stacked.</p>}
                   </div>
                )}
              </div>
            </div>
          )}

          {/* VIEW: CONVERTER */}
          {activeTab === 'converter' && (
            <div className="space-y-8 animate-fade-in">
              <div className="bg-white p-8 rounded-xl shadow-lg border border-slate-200 flex flex-col items-center">
                <label className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-2">Enter Arabic Number</label>
                <div className="flex items-center gap-4 w-full max-w-md">
                  <input 
                    type="number" 
                    value={inputNum}
                    onChange={(e) => setInputNum(parseInt(e.target.value) || 0)}
                    className="w-full text-center text-4xl font-bold text-slate-800 p-4 border-b-2 border-blue-500 focus:outline-none bg-transparent"
                  />
                </div>
                
                <div className="my-8 flex flex-col items-center justify-center w-full">
                  <ArrowRight className="text-slate-300 rotate-90 mb-4" size={32} />
                  <div className="p-8 bg-slate-50 rounded-2xl w-full flex flex-col items-center min-h-[200px] justify-center border border-slate-200">
                     <ResultDisplay output={conversionResult} system={activeSystem} />
                     <span className="text-xs text-slate-400 mt-6 uppercase tracking-widest">{activeSystem.name} Output</span>
                  </div>
                </div>
              </div>

              {/* Debugger / Logic Revealer */}
              <div className="bg-slate-900 text-slate-300 p-6 rounded-xl font-mono text-sm shadow-inner">
                <h4 className="text-blue-400 font-bold mb-4 flex items-center gap-2">
                  <Calculator size={16}/> ENGINE LOGIC TRACE
                </h4>
                <ul className="space-y-2">
                  {conversionResult.steps.map((step, i) => (
                    <li key={i} className="flex gap-3">
                      <span className="text-slate-600 select-none">{(i+1).toString().padStart(2, '0')}</span>
                      <span>{step}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {/* VIEW: PRACTICE ZONE */}
          {activeTab === 'practice' && currentPuzzle && (
            <div className="space-y-6 animate-fade-in">
              <div className="flex justify-between items-center">
                 <h3 className="text-xl font-bold text-slate-800">Linguistics Olympiad Challenge</h3>
                 <button onClick={loadNewPuzzle} className="text-sm text-blue-600 flex items-center gap-1 hover:underline">
                   <RefreshCw size={14}/> New Puzzle
                 </button>
              </div>

              <div className="bg-white p-8 rounded-xl shadow-md border-l-4 border-blue-500">
                <span className="text-xs font-bold text-blue-500 uppercase tracking-widest mb-2 block">{currentPuzzle.type} Puzzle</span>
                <p className="text-2xl font-medium text-slate-800 mb-6">{currentPuzzle.question}</p>
                
                <div className="flex gap-4 items-center">
                  <input 
                    type="text" 
                    placeholder="Enter numeric answer..."
                    className="p-3 border border-slate-300 rounded-lg flex-1"
                    value={puzzleAnswer}
                    onChange={(e) => setPuzzleAnswer(e.target.value)}
                  />
                  <button 
                    onClick={checkAnswer}
                    className="bg-blue-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-blue-700 transition-colors"
                  >
                    Check
                  </button>
                </div>

                {/* Feedback Area */}
                {puzzleFeedback && (
                  <div className={`mt-6 p-4 rounded-lg flex items-start gap-3 ${puzzleFeedback === 'correct' ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
                    {puzzleFeedback === 'correct' ? <Check className="mt-1"/> : <X className="mt-1"/>}
                    <div>
                      <p className="font-bold">{puzzleFeedback === 'correct' ? 'Correct!' : 'Try Again.'}</p>
                      {puzzleFeedback === 'correct' && (
                        <p className="text-sm mt-1">
                          You successfully analyzed the {activeSystem.name} pattern.
                        </p>
                      )}
                      {puzzleFeedback === 'incorrect' && (
                        <p className="text-sm mt-1">Hint: {currentPuzzle.hint}</p>
                      )}
                    </div>
                  </div>
                )}
              </div>
              
              <div className="bg-blue-50 p-4 rounded-lg text-blue-800 text-sm flex gap-3">
                 <Info size={16} className="flex-shrink-0 mt-0.5"/>
                 <p>
                   These puzzles are procedurally generated by the engine. The system creates a valid conversion using the Schema, masks part of it, and asks you to solve for the missing variable.
                 </p>
              </div>
            </div>
          )}

        </div>
      </main>
    </div>
  );
}
