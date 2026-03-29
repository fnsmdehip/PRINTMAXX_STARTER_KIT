import { useRef, useEffect, useState, useCallback } from 'react';

interface SignatureCanvasProps {
  onSave: (dataUrl: string) => void;
  onCancel: () => void;
  partyName: string;
}

export default function SignatureCanvas({ onSave, onCancel, partyName }: SignatureCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [hasDrawn, setHasDrawn] = useState(false);

  const getCoords = useCallback((e: MouseEvent | TouchEvent): { x: number; y: number } | null => {
    const canvas = canvasRef.current;
    if (!canvas) return null;
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;

    if ('touches' in e) {
      const touch = e.touches[0];
      if (!touch) return null;
      return {
        x: (touch.clientX - rect.left) * scaleX,
        y: (touch.clientY - rect.top) * scaleY,
      };
    } else {
      return {
        x: (e.clientX - rect.left) * scaleX,
        y: (e.clientY - rect.top) * scaleY,
      };
    }
  }, []);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    // Set canvas resolution
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * 2;
    canvas.height = rect.height * 2;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 3;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    // Draw signature line
    ctx.strokeStyle = '#374151';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(40, canvas.height - 60);
    ctx.lineTo(canvas.width - 40, canvas.height - 60);
    ctx.stroke();

    // Reset for drawing
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 3;
  }, []);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const handleStart = (e: MouseEvent | TouchEvent) => {
      e.preventDefault();
      const coords = getCoords(e);
      if (!coords) return;
      setIsDrawing(true);
      setHasDrawn(true);
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(coords.x, coords.y);
    };

    const handleMove = (e: MouseEvent | TouchEvent) => {
      e.preventDefault();
      if (!isDrawing) return;
      const coords = getCoords(e);
      if (!coords) return;
      ctx.lineTo(coords.x, coords.y);
      ctx.stroke();
    };

    const handleEnd = (e: MouseEvent | TouchEvent) => {
      e.preventDefault();
      setIsDrawing(false);
    };

    canvas.addEventListener('mousedown', handleStart);
    canvas.addEventListener('mousemove', handleMove);
    canvas.addEventListener('mouseup', handleEnd);
    canvas.addEventListener('mouseleave', handleEnd);
    canvas.addEventListener('touchstart', handleStart, { passive: false });
    canvas.addEventListener('touchmove', handleMove, { passive: false });
    canvas.addEventListener('touchend', handleEnd, { passive: false });

    return () => {
      canvas.removeEventListener('mousedown', handleStart);
      canvas.removeEventListener('mousemove', handleMove);
      canvas.removeEventListener('mouseup', handleEnd);
      canvas.removeEventListener('mouseleave', handleEnd);
      canvas.removeEventListener('touchstart', handleStart);
      canvas.removeEventListener('touchmove', handleMove);
      canvas.removeEventListener('touchend', handleEnd);
    };
  }, [isDrawing, getCoords]);

  const handleClear = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // Redraw signature line
    ctx.strokeStyle = '#374151';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(40, canvas.height - 60);
    ctx.lineTo(canvas.width - 40, canvas.height - 60);
    ctx.stroke();
    setHasDrawn(false);
  };

  const handleSave = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    onSave(canvas.toDataURL('image/png'));
  };

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
      <div className="bg-navy-light rounded-2xl w-full max-w-lg overflow-hidden">
        <div className="p-4 border-b border-gray-700">
          <h3 className="text-white font-medium text-lg">Sign: {partyName}</h3>
          <p className="text-gray-400 text-sm mt-1">Draw your signature below</p>
        </div>

        <div className="p-4">
          <canvas
            ref={canvasRef}
            className="w-full bg-navy rounded-xl border border-gray-700 touch-none"
            style={{ height: '200px' }}
          />
        </div>

        <div className="p-4 border-t border-gray-700 flex gap-3">
          <button
            onClick={onCancel}
            className="flex-1 py-3 rounded-xl border border-gray-600 text-gray-300 font-medium active:scale-[0.98] transition-transform"
          >
            Cancel
          </button>
          <button
            onClick={handleClear}
            className="px-4 py-3 rounded-xl border border-gray-600 text-gray-300 font-medium active:scale-[0.98] transition-transform"
          >
            Clear
          </button>
          <button
            onClick={handleSave}
            disabled={!hasDrawn}
            className={`flex-1 py-3 rounded-xl font-medium active:scale-[0.98] transition-transform ${
              hasDrawn
                ? 'bg-coral text-white'
                : 'bg-gray-700 text-gray-500 cursor-not-allowed'
            }`}
          >
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
}
